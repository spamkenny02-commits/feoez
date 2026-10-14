#!/usr/bin/env python3
"""Conservative, fixed-length insertion for this exact source ROM.
Only letters/space bytes may change. All commands retain value and position.
CSV IDs, offsets, lengths, originals are validated against a fresh extraction.
Whole-message relocation and variable-length editing are intentionally unsupported.
"""
import argparse,csv,hashlib,json,re
from pathlib import Path
from extract import EXPECTED,START,END,MAP,encode

REVIEWED_OFFSETS={0x600002,0x600008,0x600014,0x600028}
class InsertionError(ValueError):pass

def digest(b):return hashlib.sha256(b).hexdigest()

def load_rows(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def make_ips(original,modified):
    if len(original)!=len(modified):raise InsertionError('ROM length changed')
    patch=bytearray(b'PATCH');i=0
    while i<len(original):
        if original[i]==modified[i]:i+=1;continue
        start=i
        while i<len(original) and original[i]!=modified[i] and i-start<65535:i+=1
        # IPS reserves this address for its EOF marker.
        if start==0x454f46:raise InsertionError('Reserved IPS offset')
        patch+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+modified[start:i]
    return bytes(patch+b'EOF')

def apply_ips(original,patch):
    if not patch.startswith(b'PATCH'):raise InsertionError('Invalid IPS header')
    out=bytearray(original);p=5
    while patch[p:p+3]!=b'EOF':
        if p+5>len(patch):raise InsertionError('Truncated IPS')
        offset=int.from_bytes(patch[p:p+3],'big');n=int.from_bytes(patch[p+3:p+5],'big');p+=5
        if n==0:raise InsertionError('RLE not supported by test reader')
        if p+n>len(patch) or offset+n>len(out):raise InsertionError('IPS record out of bounds')
        out[offset:offset+n]=patch[p:p+n];p+=n
    if p+3!=len(patch):raise InsertionError('Trailing IPS data')
    return bytes(out)

def insert(original,reference,edited,structures):
    if digest(original)!=EXPECTED:raise InsertionError('ROM SHA-256 does not match supported source')
    if len(reference)!=len(edited):raise InsertionError('Missing or added CSV rows')
    base={r['id']:r for r in reference}
    if len(base)!=len(reference):raise InsertionError('Duplicate reference IDs')
    ids=[r['id'] for r in edited]
    if len(set(ids))!=len(ids) or set(ids)!=set(base):raise InsertionError('Duplicate or unknown edited IDs')
    protected=[(int(s['offset'],16),int(s['offset'],16)+s['length']) for s in structures]
    out=bytearray(original);edits=[];spans=[]
    for r in edited:
        ref=base[r['id']]
        for field in ['offset','length','raw_hex','english_tokens']:
            if r.get(field)!=ref[field]:raise InsertionError('Altered immutable CSV field '+field+' in '+r['id'])
        o=int(ref['offset'],16);raw=bytes.fromhex(ref['raw_hex']);n=int(ref['length'])
        if not START<=o<o+n<=END or n!=len(raw) or original[o:o+n]!=raw:raise InsertionError('Original bytes mismatch: '+r['id'])
        if encode(ref['english_tokens'])!=raw:raise InsertionError('Original tokens mismatch')
        if any(o<end and o+n>start for start,end in protected):raise InsertionError('Fragment overlaps protected table')
        spans.append((o,o+n))
        translation=r.get('french','')
        if not translation:continue
        try:new=encode(translation)
        except (AssertionError,KeyError,ValueError) as e:raise InsertionError('Unsupported character or invalid token: '+r['id']) from e
        if len(new)!=n:raise InsertionError('Fixed length required: '+r['id']+f' ({len(new)} != {n})')
        for old,value in zip(raw,new):
            if old not in MAP:
                if value!=old:raise InsertionError('Control byte changed or moved: '+r['id'])
            elif value not in MAP:raise InsertionError('Cannot introduce a control byte: '+r['id'])
        if o not in REVIEWED_OFFSETS:raise InsertionError('Fragment not yet reviewed for insertion: '+r['id'])
        if any(x not in MAP for x in raw):raise InsertionError('Reviewed insertion must contain only letters/spaces')
        out[o:o+n]=new
        edits.append({'id':r['id'],'offset':ref['offset'],'original':ref['english_tokens'],'replacement':translation,'length':n})
    spans.sort()
    if any(a[1]>b[0] for a,b in zip(spans,spans[1:])):raise InsertionError('Overlapping fragments')
    # Source uses the raw sum of its 7MB, confirmed against its stored checksum.
    # The two complement words always sum to 0x01FE bytewise, so this is stable.
    checksum_changed=False
    if bytes(out)!=original:
        stored=int.from_bytes(original[0xffde:0xffe0],'little')
        complement=int.from_bytes(original[0xffdc:0xffde],'little')
        if stored!=(sum(original)&0xffff) or stored^complement!=0xffff:raise InsertionError('Unsupported checksum convention')
        checksum=sum(out)&0xffff
        out[0xffdc:0xffde]=(checksum^0xffff).to_bytes(2,'little');out[0xffde:0xffe0]=checksum.to_bytes(2,'little')
        if sum(out)&0xffff!=checksum:raise InsertionError('Checksum regeneration failed')
        checksum_changed=True
    result=bytes(out)
    for a,end in protected:
        if result[a:end]!=original[a:end]:raise InsertionError('Protected table differs after insertion')
    diffs=[i for i,(a,b) in enumerate(zip(original,result)) if a!=b]
    if any(not (0xffdc<=i<0xffe0 or any(int(e['offset'],16)<=i<int(e['offset'],16)+e['length'] for e in edits)) for i in diffs):raise InsertionError('Unexpected modification')
    return result,{'input_sha256':digest(original),'output_sha256':digest(result),'rom_size':len(result),'edits':edits,'changed_bytes':len(diffs),'changed_offsets':[f'0x{x:06X}' for x in diffs],'checksum_regenerated':checksum_changed,'protected_tables_unchanged':len(protected),'runtime_emulator_validation':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('rom',type=Path);ap.add_argument('csv',type=Path);ap.add_argument('--reference',type=Path,default=Path(__file__).parent/'output/english_fragments.csv');ap.add_argument('--structures',type=Path,default=Path(__file__).parent/'output/structure_inventory.json');ap.add_argument('--rom-out',type=Path);ap.add_argument('--ips-out',type=Path);ap.add_argument('--report',type=Path);args=ap.parse_args()
    if not args.rom_out and not args.ips_out:ap.error('Set --rom-out or --ips-out')
    # Re-extract independently to prevent edited references from relaxing the guards.
    import tempfile,subprocess,sys
    with tempfile.TemporaryDirectory() as temp:
        subprocess.run([sys.executable,str(Path(__file__).parent/'extract.py'),str(args.rom),'--out',temp],check=True,stdout=subprocess.DEVNULL)
        canonical=load_rows(Path(temp)/'english_fragments.csv')
        structures=json.loads((Path(temp)/'structure_inventory.json').read_text())
        if load_rows(args.reference)!=canonical:raise InsertionError('Reference differs from fresh source extraction')
        if json.loads(args.structures.read_text())!=structures:raise InsertionError('Structure inventory differs from fresh source extraction')
        original=args.rom.read_bytes();result,report=insert(original,canonical,load_rows(args.csv),structures)
    patch=make_ips(original,result)
    if apply_ips(original,patch)!=result:raise InsertionError('IPS self-validation failed')
    outputs=[p.resolve() for p in [args.rom_out,args.ips_out,args.report] if p]
    inputs={p.resolve() for p in [args.rom,args.csv,args.reference,args.structures]}
    if len(set(outputs))!=len(outputs) or any(p in inputs for p in outputs):raise InsertionError('Output paths must be distinct and cannot overwrite inputs')
    if args.rom_out:args.rom_out.write_bytes(result)
    if args.ips_out:args.ips_out.write_bytes(patch)
    if args.report:args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
