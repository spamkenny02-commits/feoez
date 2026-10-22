#!/usr/bin/env python3
"""Native leaf probes; valid calendar domains, without event/clock/PPU claims."""
import argparse,json,hashlib
from pathlib import Path
from calendar65816_probe import CalendarCPU
from calendar_formats_lot47 import patch_calendar_formats,MONTHS
from french_font import encode_fr,visible_width
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();source=a.source.read_bytes();assert hashlib.sha256(source).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e';rom,patch=patch_calendar_formats(source)
def probe(data,address,slot,value):
 c=CalendarCPU(data);c.X=17;c.Y=29;c.DBR=0x42;before=(c.X,c.Y,c.DBR,c.P,c.S);offset=32*slot;at=0x32aa+offset;c.ram[0x32aa:0x332a]=b'\x55'*128;raw=bytes(0x21+int(n) for n in str(value))+b'\0';c.ram[at:at+len(raw)]=raw;c.write(0x8f,0x100,3);c.ram[0x100]=4+slot;c.run(address,offset);assert (c.X,c.Y,c.DBR,c.P,c.S)==before;assert c.read(0x8f,3)==0x101
 got=bytes(c.ram[at:at+32]).split(b'\0')[0];assert c.ram[0x32aa:at]==b'\x55'*(at-0x32aa);assert c.ram[at+32:0x332a]==b'\x55'*(0x332a-at-32);return got
rows=[];total=0
for slot in range(4):
 for mode,address,values in [('month',0x4d3c00,range(1,13)),('ordinal',0x4d3d00,range(1,32)),('hour12',0x4d3c60,range(24)),('minute',0x4d3cb0,range(60))]:
  for value in values:
   old=probe(source,address,slot,value);new=probe(rom,address,slot,value);numeric=bytes(0x21+int(d) for d in str(value))
   if mode=='month':expected=encode_fr(patch['months'][value-1]['french'])
   elif mode=='ordinal':expected=numeric+encode_fr('er' if value==1 else 'e ')
   elif mode=='hour12':expected=bytes(0x21+int(d) for d in str(value or 12));assert old==new
   else:expected=bytes(0x21+int(d) for d in f'{value:02}');assert old==new
   assert new==expected,(slot,mode,value,new,expected);total+=2
   if slot==0:rows.append({'mode':mode,'value':value,'source_hex':old.hex(),'localized_hex':new.hex()})
changed=[i for i,(x,y) in enumerate(zip(source,rom)) if x!=y];spans=[(int(s,16),int(e,16)) for s,e in patch['changed_spans']];assert all(any(s<=i<e for s,e in spans) for i in changed)
report={'source_sha256':hashlib.sha256(source).hexdigest(),'formatter_only_candidate_sha256':hashlib.sha256(rom).hexdigest(),'native_executions':total,'slots':4,'domains':{'month':'1..12 decimal glyphs','ordinal':'1..31','hour12':'0..23; zero maps to12,13..23 unchanged','minute':'0..59'},'registers_stack_flags_dbr_preserved':True,'slot_canaries_preserved':True,'read_pointer_advanced_one':True,'changed_bytes':len(changed),'patch':patch,'cases':rows,'scope':'Restricted native formatter leafs, not full SNES timing, PPU, event producer paths or natural dates.','maximum_month_pixels':max(visible_width(e['french'],source) for e in patch['months'])};a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS',total,'native executions; finite month/ordinal/hour/minute domains')
