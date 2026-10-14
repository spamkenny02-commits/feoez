#!/usr/bin/env python3
"""Relocate verified directory blocks, optionally enlarge plain labels.
Copies opaque data unchanged except expressly selected letter/space strings.
Old blocks remain intact. Updates ALL directory aliases of each moved block.
"""
import argparse,hashlib,json
from pathlib import Path
from pointers import analyze,MASTER,COUNT,FREE_START,FREE_END,file_to_cpu
from extract import MAP,encode,decode
from insert import make_ips,apply_ips

class RelocationError(ValueError):pass

def position(payload,relative,index):
    if not 1<=index<=255:raise RelocationError('String IDs must be 1..255')
    group=(index-1)//16
    if group>=len(relative):raise RelocationError('String group outside table')
    p=relative[group]
    for _ in range((index-1)%16):
        end=payload.find(b'\x00',p)
        if end<0:raise RelocationError('Unterminated preceding string')
        if any(v>=0xe0 for v in payload[p:end]):raise RelocationError('Dictionary-coded preceding string unsupported for editing')
        p=end+1
    end=payload.find(b'\x00',p)
    if end<0:raise RelocationError('Unterminated target string')
    if group+1<len(relative) and end>=relative[group+1]:raise RelocationError('String ID crosses next group')
    return p,end

def run_plan(original,plan):
    audit=analyze(original);out=bytearray(original);edits=[];used=set();ranges=[]
    for job in plan:
        block_id=int(job['block_id']);dest=int(str(job['destination']),0)
        block=next((b for b in audit['blocks'] if block_id in b['block_ids']),None)
        if block is None or not block['main_text_pool']:raise RelocationError('Only audited main text blocks may be moved')
        source=int(block['offset'],16);length=block['length']
        if source in used:raise RelocationError('Same aliased block requested twice')
        used.add(source);payload=bytearray(original[source:source+length]);relative=list(map(lambda v:int(v,16),block['relative_offsets']));strings=[];seen=set()
        for edit in job.get('replacements',[]):
            idx=int(edit['string_id'])
            if idx in seen:raise RelocationError('Duplicate replacement ID')
            seen.add(idx);p,end=position(payload,relative,idx);old=bytes(payload[p:end])
            if not old or any(v not in MAP for v in old):raise RelocationError('Only plain letter/space labels may be edited')
            try:new=encode(edit['text'])
            except (AssertionError,KeyError,ValueError) as e:raise RelocationError('Unsupported character') from e
            if not new or any(v not in MAP for v in new):raise RelocationError('New label must contain only letters/spaces')
            if len(new)>4096:raise RelocationError('Label is excessively long')
            delta=len(new)-len(old);payload[p:end]=new
            for i,v in enumerate(relative):
                if p<v<end:raise RelocationError('Group pointer inside replacement')
                if v>p:relative[i]+=delta
                if not 0<=relative[i]<=65535:raise RelocationError('Relative pointer overflow')
                payload[2*i:2*i+2]=relative[i].to_bytes(2,'little')
            strings.append({'string_id':idx,'original':decode(old),'replacement':edit['text'],'old_length':len(old),'new_length':len(new),'delta':delta})
        if len(payload)>65535:raise RelocationError('Block exceeds conservative 16-bit size limit')
        if not FREE_START<=dest<dest+len(payload)<=FREE_END:raise RelocationError('Destination outside approved unused range')
        if any(dest<e and dest+len(payload)>a for a,e in ranges):raise RelocationError('Relocated blocks overlap')
        if any(out[dest:dest+len(payload)]):raise RelocationError('Destination contains data')
        ranges.append((dest,dest+len(payload)));out[dest:dest+len(payload)]=payload
        address=file_to_cpu(dest)
        for slot in block['directory_slots']:
            s=int(slot,16)
            if out[s:s+3]!=file_to_cpu(source).to_bytes(3,'little'):raise RelocationError('Directory alias changed unexpectedly')
            out[s:s+3]=address.to_bytes(3,'little')
        edits.append({'source':hex(source),'destination':hex(dest),'cpu_address':hex(address),'old_size':length,'new_size':len(payload),'block_ids_updated':block['block_ids'],'directory_slots_updated':block['directory_slots'],'old_relative_offsets':block['relative_offsets'],'new_relative_offsets':[f'0x{v:04X}' for v in relative],'strings':strings})
    if sum(original)&65535!=int.from_bytes(original[0xffde:0xffe0],'little'):raise RelocationError('Source checksum convention mismatch')
    checksum=sum(out)&65535;out[0xffdc:0xffde]=(checksum^65535).to_bytes(2,'little');out[0xffde:0xffe0]=checksum.to_bytes(2,'little')
    result=bytes(out)
    if sum(result)&65535!=checksum:raise RelocationError('Checksum failed')
    for edit in edits:
        s=int(edit['source'],16)
        if result[s:s+edit['old_size']]!=original[s:s+edit['old_size']]:raise RelocationError('Old block unexpectedly altered')
    allowed=ranges+[(0xffdc,0xffe0)]+[(int(s,16),int(s,16)+3) for e in edits for s in e['directory_slots_updated']]
    diffs=[i for i,(a,b) in enumerate(zip(original,result)) if a!=b]
    if any(not any(a<=i<e for a,e in allowed) for i in diffs):raise RelocationError('Unexpected changed address')
    return result,{'source_sha256':hashlib.sha256(original).hexdigest(),'output_sha256':hashlib.sha256(result).hexdigest(),'edits':edits,'changed_bytes':len(diffs),'source_blocks_preserved':True,'full_game_emulator_validation':False,'scope':'Directory path and targeted CPU routines; no rendering/peripheral validation'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('rom',type=Path);ap.add_argument('plan',type=Path);ap.add_argument('--ips-out',type=Path);ap.add_argument('--rom-out',type=Path);ap.add_argument('--report',type=Path);a=ap.parse_args()
    if not a.ips_out and not a.rom_out:ap.error('Set --ips-out or --rom-out')
    inputs={a.rom.resolve(),a.plan.resolve()};outputs=[p.resolve() for p in [a.ips_out,a.rom_out,a.report] if p]
    if len(set(outputs))!=len(outputs) or any(p in inputs for p in outputs):raise RelocationError('Cannot overwrite input or duplicate outputs')
    source=a.rom.read_bytes();result,report=run_plan(source,json.loads(a.plan.read_text()));patch=make_ips(source,result)
    if apply_ips(source,patch)!=result:raise RelocationError('IPS reconstruction mismatch')
    if a.rom_out:a.rom_out.write_bytes(result)
    if a.ips_out:a.ips_out.write_bytes(patch)
    if a.report:a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
