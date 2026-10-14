#!/usr/bin/env python3
"""Directory and grouped-text tables identified from actual lookup routines."""
import hashlib,json,argparse
from pathlib import Path
from extract import EXPECTED
MASTER=0x0c9800
COUNT=253
MAIN_START=0x600000
MAIN_END=0x6ad527
FREE_START=0x6b0000
FREE_END=0x6d0000

def cpu_to_file(p):
    if not 0x400000<=p<0x500000:raise ValueError('Not in mapped expansion banks')
    return p+0x200000

def file_to_cpu(p):
    if not 0x600000<=p<0x700000:raise ValueError('Not in expansion ROM')
    return p-0x200000

def analyze(rom):
    if hashlib.sha256(rom).hexdigest()!=EXPECTED:raise ValueError('Unsupported source SHA-256')
    refs=[int.from_bytes(rom[MASTER+3*i:MASTER+3*i+3],'little') for i in range(COUNT)]
    bases=[cpu_to_file(p) for p in refs];unique=sorted(set(bases));blocks=[]
    for a in unique:
        main=MAIN_START<=a<MAIN_END
        end=min(MAIN_END,next((v for v in unique if v>a),MAIN_END)) if main else None
        table_bytes=int.from_bytes(rom[a:a+2],'little')
        if not table_bytes or table_bytes%2 or table_bytes>32:raise ValueError('Invalid grouped table header')
        rel=[int.from_bytes(rom[a+i:a+i+2],'little') for i in range(0,table_bytes,2)]
        if rel[0]!=table_bytes or any(y<x for x,y in zip(rel,rel[1:])):raise ValueError('Invalid table ordering')
        if main and any(a+v>=end for v in rel):raise ValueError('Group pointer outside block')
        slots=[i for i,b in enumerate(bases) if b==a]
        blocks.append({'offset':f'0x{a:06X}','cpu_address':f'0x{file_to_cpu(a):06X}','end_exclusive':f'0x{end:06X}' if end else None,'length':end-a if end else None,'main_text_pool':main,'table_bytes':table_bytes,'groups':len(rel),'relative_offsets':[f'0x{v:04X}' for v in rel],'group_targets':[f'0x{a+v:06X}' for v in rel],'block_ids':[i+1 for i in slots],'directory_slots':[f'0x{MASTER+3*i:06X}' for i in slots],'status':'referenced_by_executed_lookup_routines'})
    return {'master_offset':hex(MASTER),'master_cpu_address':'0xCC9800','master_end_exclusive':hex(MASTER+COUNT*3),'directory_entries':COUNT,'unique_blocks':len(unique),'main_blocks':sum(b['main_text_pool'] for b in blocks),'mapping':'CPU 0x400000..0x4FFFFF -> file +0x200000','group_formula':'group=(string_id-1)//16; position=(string_id-1)%16; start=block_base+u16le(block_base+2*group)','routine_addresses':{'lookup':'0xC329B6','select':'0xC329DA','cursor':'0xC02C5E','reader':'0xC02C6E'},'blocks':blocks,'routine_sha256':{hex(a):hashlib.sha256(rom[a:z]).hexdigest() for a,z in [(0x329b6,0x329da),(0x329da,0x32a23),(0x2c5e,0x2d00)]}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('rom',type=Path);ap.add_argument('--out',type=Path,default=Path('output/pointer_audit.json'));a=ap.parse_args();report=analyze(a.rom.read_bytes());a.out.write_text(json.dumps(report,indent=2));print({k:v for k,v in report.items() if k not in ('blocks','routine_sha256')})
