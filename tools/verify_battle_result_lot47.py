#!/usr/bin/env python3
"""Bound FD8B result messages; native lookup plus finite producer domains.
No battle progression, PPU drawing or UI pagination claim.
"""
import argparse,hashlib,json,re
from pathlib import Path
from cpu65816_probe import CPU
from pointers import analyze
from relocate import position
from french_font import decode_fr,visible_width
p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();rom=a.rom.read_bytes()
def native(b,i):
 c=CPU(rom);c.load_block(b);c.select(i);return c.string()
root=Path(__file__).resolve().parents[1]
inventory=json.loads((root/"verification/build_report_lot47_checkpoint.json").read_text())
assert inventory["output_sha256"]==hashlib.sha256(rom).hexdigest()
def catalog(b):
 out=[]
 block=next(x for x in inventory["blocks"] if b in x["block_ids"])
 start=int(block["destination"],16);payload=rom[start:start+block["new_size"]];relative=block["new_relative_offsets"]
 for i in range(1,256):
  try:position(payload,relative,i)
  except ValueError:break
  raw=native(b,i)
  if len(raw)<=31 and all(v>=16 for v in raw):out.append(raw)
 return out
actors=[native(12,i) for i in range(1,5)];skills=catalog(5);items=sum([catalog(b) for b in [1,2,3]],[])
number=lambda n:bytes(0x21+int(d) for d in str(n))
domains={1:[{4:number(n)} for n in [0,1,0xffffff]],2:[{4:number(n)} for n in [0,1,0xffffff]],3:[{4:name,5:number(rank)} for name in actors for rank in [1,99,255]],4:[{4:name,5:skill} for name in actors for skill in skills],5:[{4:item} for item in items],6:[{4:native(3,49)}]}
results=[]
for i,domain in domains.items():
 raw=native(43,i);assert 1 not in raw and 3 not in raw
 for slots in domain:
  expanded=b''.join(slots.get(v,bytes([v])) for v in raw);assert not any(v<16 for v in expanded)
  text=decode_fr(expanded);width=visible_width(text,rom);assert len(expanded)<=45 and width<=216,(i,text,len(expanded),width)
  results.append({'id':f'B043-S{i:03}','expanded':text,'bytes':len(expanded),'pixels':width})
report={'rom_sha256':hashlib.sha256(rom).hexdigest(),'native_lookup_expansions':len(results),'maximum_bytes':max(x['bytes'] for x in results),'maximum_pixels':max(x['pixels'] for x in results),'scope':__doc__,'cases':results};a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS',len(results),'finite result-message expansions')
