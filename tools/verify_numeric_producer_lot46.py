#!/usr/bin/env python3
"""Execute the pinned 24-bit numeric formatter and slot copier on boundary values.
Restricted CPU, modeled multiplication result; no event binding/timing proof.
"""
import argparse,hashlib,json,random
from pathlib import Path
from numeric65816_probe import NumericCPU
from french_font import encode_fr,visible_width
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();rom=a.source.read_bytes()
sha=hashlib.sha256(rom).hexdigest();assert sha=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
values=set(range(256))|{256,257,65534,65535,65536,65537,0xfffffe,0xffffff}
for n in range(1,8):values|={10**n-1,10**n,10**n+1}
rng=random.Random(46);values|={rng.randrange(0x1000000) for _ in range(256)}
remap=rom[0x6f1fd0:0x6f1fda];total=0;length_max=width_max=0
for slot in range(4):
 for value in sorted(values):
  c=NumericCPU(rom);c.X=17;c.Y=29;c.write(9,value,3);c.ram[0x32aa:0x332a]=b'\x55'*128
  c.run(0xc32ad3,slot)
  start=0x32aa+32*slot;expected=bytes(0x21+int(d) for d in str(value))+b'\0'
  assert c.ram[start:start+len(expected)]==expected,(slot,value)
  assert c.ram[0x32aa:start]==b'\x55'*(start-0x32aa)
  assert c.ram[start+len(expected):0x332a]==b'\x55'*(0x332a-start-len(expected))
  assert c.X==17 and c.Y==29 and c.P&0x30==0x30
  native_glyphs=bytes(remap[b-0x21] for b in expected[:-1]);assert native_glyphs==encode_fr(str(value))
  length_max=max(length_max,len(expected)-1);width_max=max(width_max,visible_width(str(value),rom));total+=1
widest=max(range(10),key=lambda d:visible_width(str(d),rom));reserve=8*visible_width(str(widest),rom)
report={'source_sha256':sha,'routine':'C3:2AD3 including C1:0450 decimal conversion and C0:29A1 multiply','tested_values_per_slot':len(values),'slots':4,'executions_passed':total,'input_range_supported':'unsigned 24-bit; tests cover all 8-bit values, decimal/binary boundaries and deterministic samples, not all 24-bit inputs','maximum_observed_digits':length_max,'maximum_observed_pixels':width_max,'eight_widest_digits_reservation_pixels':reserve,'widest_digit':str(widest),'scope':'Numeric producer and slot write behavior only. IO multiplication is modeled without cycle timing. No actual event producer binding or natural gameplay claim.','cases_for_fixtures':{'zero':0,'one':1,'max24':0xffffff},'limitations':['A numeric width contract applies only to the selected entries whose source text calls for a number.','Actual event call paths must still be traced before a final validated release.','No numeric bound is applied to item names, character names, dates/ordinals, choices or other special formats.']}
a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(f'PASS {total} numeric producer executions, reserve {reserve}px')
