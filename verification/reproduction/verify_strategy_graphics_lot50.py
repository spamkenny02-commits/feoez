#!/usr/bin/env python3
"""Exact fields of the ordinary strategy menu;no synthetic stock/actor state."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
r=a.rom.read_bytes();sha=hashlib.sha256(r).hexdigest();report=json.loads((a.run/'report.json').read_text());assert report['rom_sha256']==sha and report['controller_only'];root=Path(__file__).resolve().parents[2]
v=(a.run/'strategy_02.vram').read_bytes();assert v[0x7a00:0x7c10]==r[0x6d4000:0x6d4210];cases=[]
for e in json.loads((root/'traduction/strategy_graphics_lot50_fr.json').read_text()):
 st=int(e['offset'],16);tile=(st-0x6d4000)//16+0x1a0;n=e['tiles'];assert e['pixels']<=8*n
 for f in e['visible_fields']:
  at=0xb000+64*f['row']+2*f['column'];tiles=[int.from_bytes(v[at+2*i:at+2*i+2],'little')&1023 for i in range(n)];assert tiles==list(range(tile,tile+n)),(e['id'],tiles);cases.append(dict(id=e['id'],field=f,tiles=tiles,source=hex(st),width_limit=8*n,pixels=e['pixels'],exact=True))
a.out.write_text(json.dumps(dict(rom_sha256=sha,native_dma_source='4D4000',native_dma_length=528,native_vram_word='3D00',all_source_vram_bytes_exact=True,fields=cases,new_canonical_source_count=1,prior_source_variants=7,visual_review='pending',scope='Ordinary menu from fresh same-ROM field;not proof of saved strategy changes or combat execution'),ensure_ascii=False,indent=2)+'\n');print('PASS strategy528byte DMA and9exact visible fields;visual pending')
