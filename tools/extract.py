#!/usr/bin/env python3
"""First-pass lossless text inventory for the supplied English Tengai Makyou Zero.
Offsets are FILE offsets. Null-delimited fragments are NOT validated dialogue IDs.
No ROM writes. Unknown bytes remain <XX>, including possible command arguments.
"""
import argparse, csv, hashlib, json, re
from collections import Counter
from pathlib import Path

EXPECTED='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
START, END=0x600000,0x6ad527
MAP={0x20:' ', **{i:chr(i+17) for i in range(0x30,0x4a)}, **{i:chr(i+17) for i in range(0x50,0x6a)}}
# Contextual guesses, kept separate from the reversible authoritative decoding.
GUESSES={0x1f:'0',0x2f:'1',**{i:str(i-0x1f) for i in range(0x21,0x29)},0x16:"'",0x1c:'-',0x1d:'.',0x1b:',',0x10:'!',0x2e:'?'}
def decode(raw,preview=False):
    return ''.join(MAP[x] if x in MAP else '\n' if x==1 else GUESSES[x] if preview and x in GUESSES else f'<{x:02X}>' for x in raw)
def encode(text):
    inverse={v:k for k,v in MAP.items()}; result=bytearray(); i=0
    while i<len(text):
        if text[i]=='<':
            assert re.fullmatch(r'<[0-9A-F]{2}>',text[i:i+4]); result.append(int(text[i+1:i+3],16));i+=4
        else:
            result.append(1 if text[i]=='\n' else inverse[text[i]]);i+=1
    return bytes(result)
def quality(raw):
    letters=sum(x in MAP and x!=32 for x in raw)
    # Short names are useful, but unidentified binary bytes lower confidence.
    return letters>=2 and letters/max(1,len(raw))>=0.50

def main():
    ap=argparse.ArgumentParser();ap.add_argument('rom',type=Path);ap.add_argument('--out',type=Path,default=Path('output'));args=ap.parse_args()
    b=args.rom.read_bytes();sha=hashlib.sha256(b).hexdigest()
    if sha!=EXPECTED:raise SystemExit('Unsupported ROM SHA-256: '+sha)
    out=args.out;out.mkdir(parents=True,exist_ok=True)
    raw_region=b[START:END]
    assert encode(decode(raw_region))==raw_region
    (out/'main_region_lossless.txt').write_text(decode(raw_region),encoding='utf-8')
    (out/'english_partial.tbl').write_text('\n'.join(f'{k:02X}={v}' for k,v in sorted(MAP.items()))+'\n',encoding='utf-8')
    # Authoritative directory path identified in the original lookup routines.
    from pointers import analyze
    audit=analyze(b)
    (out/'pointer_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    blocks=[v for v in audit['blocks'] if v['main_text_pool']]
    tables=[{'table_offset':v['offset'],'entries':v['groups'],'relative_offsets':v['relative_offsets'],'target_offsets':v['group_targets'],'block_ids':v['block_ids'],'status':'directory_referenced_group_table'} for v in blocks if v['groups']>1]
    singles=[v['offset'] for v in blocks if v['groups']==1]
    headers=[(int(t['table_offset'],16),2*t['entries']) for t in tables]
    singles=[h for h in singles if not any(a<=int(h,16)<a+n for a,n in headers)]
    (out/'pointer_candidates.json').write_text(json.dumps({'multi_entry':tables,'single_entry_candidates':singles},indent=2),encoding='utf-8')
    headers=sorted(headers+[(int(h,16),2) for h in singles])
    mask=bytearray(END-START)
    for a,n in headers:mask[a-START:a-START+n]=bytes([1])*n
    (out/'structure_inventory.json').write_text(json.dumps([{'offset':hex(a),'length':n,'raw_hex':b[a:a+n].hex(' '),'status':'directory_referenced_group_table'} for a,n in headers],indent=2),encoding='utf-8')
    rows=[];rejected=[];pos=START;all_fragments=0
    ranges=[];p=START
    for a,n in headers:
        if p<a:ranges.append((p,a))
        p=max(p,a+n)
    if p<END:ranges.append((p,END))
    for region_start,region_end in ranges:
        pos=region_start
        for raw in b[region_start:region_end].split(b'\x00'):
            all_fragments+=1
            if quality(raw):
                assert encode(decode(raw))==raw
                rows.append({'id':f'T{pos:06X}','offset':f'0x{pos:06X}','length':len(raw),'raw_hex':raw.hex(' '),'english_tokens':decode(raw),'english_preview':decode(raw,True),'french':'','status':'fragment_non_valide'})
            elif raw:
                rejected.append({'offset':f'0x{pos:06X}','raw_hex':raw.hex(' '),'tokens':decode(raw),'status':'non_selectionne_par_heuristique'})
            pos+=len(raw)+1
    (out/'unselected_fragments.json').write_text(json.dumps(rejected,ensure_ascii=False,indent=2),encoding='utf-8')
    with (out/'english_fragments.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (out/'english_fragments.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    with (out/'english_readable.txt').open('w',encoding='utf-8') as f:
        f.write('PREMIERE EXTRACTION — fragments, ponctuation inferée, codes non résolus entre <XX>\n\n')
        for r in rows:f.write(f"[{r['id']} | {r['offset']} | {r['length']} octets]\n{r['english_preview']}\n\n")
    group_inventory=[]
    for block in blocks:
        targets=[int(v,16) for v in block['group_targets']]
        for i,a in enumerate(targets):
            end=targets[i+1] if i+1<len(targets) else int(block['end_exclusive'],16)
            group_inventory.append({'block_ids':block['block_ids'],'group_id':i+1,'first_string_id':16*i+1,'start':hex(a),'end_exclusive':hex(end),'status':'engine_group_anchor_confirmed'})
    (out/'group_inventory.json').write_text(json.dumps(group_inventory,indent=2),encoding='utf-8')
    # Whole-ROM scan outside the main region. Require common English words;
    # graphics/encoded art can still create false positives.
    secondary=[]
    common=re.compile(r'\b(?:the|you|your|and|have|with|this|that|will|of|to|on|in|press|enter|based|planning)\b',re.I)
    for m in re.finditer(rb'[\x30-\x49\x50-\x69\x20\x01\x10\x16\x1b\x1c\x1d\x2e]{16,}',b):
        if START<=m.start()<END:continue
        t=decode(m[0],True)
        if len(common.findall(t))>=2:
            secondary.append({'offset':f'0x{m.start():06X}','length':len(m[0]),'raw_hex':m[0].hex(' '),'english_tokens':decode(m[0]),'english_preview':t,'status':'candidate_hors_zone'})
    # ASCII credits are a separate known encoding in the ROM footer.
    credits=[{'offset':f'0x{m.start():06X}','text':m[0].decode('ascii')} for m in re.finditer(rb'[\x20-\x7e]{8,}',b) if m.start()>=0x6fff00]
    (out/'secondary_candidates.json').write_text(json.dumps(secondary,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'ascii_credits.json').write_text(json.dumps(credits,indent=2),encoding='utf-8')
    stats={'sha256':sha,'rom_size':len(b),'main_start':hex(START),'main_end_exclusive':hex(END),'main_bytes':len(raw_region),'null_delimited_fragments_total':all_fragments,'text_candidates':len(rows),'multi_entry_pointer_tables_candidates':len(tables),'single_entry_candidates':len(singles),'secondary_candidates':len(secondary),'ascii_footer_strings':len(credits),'letter_space_bytes':sum(x in MAP for x in raw_region),'unknown_byte_counts':{f'{x:02X}':n for x,n in sorted(Counter(x for x in raw_region if x not in MAP and x not in (0,1)).items())},'table_bytes_excluded_from_fragments':sum(n for a,n in headers),'lossless_roundtrip':'PASS: main region and all CSV fragments','coverage':'Master directory and group tables confirmed by targeted CPU probe; CSV remains null-delimited, command and graphics coverage incomplete'}
    (out/'manifest.json').write_text(json.dumps(stats,indent=2),encoding='utf-8');print(json.dumps(stats,indent=2))
if __name__=='__main__':main()
