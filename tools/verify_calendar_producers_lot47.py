#!/usr/bin/env python3
"""Bind static date-call fragments to original 8-bit numeric producer leafs.
This executes the actual event producer handler, not the full event/RTC code.
"""
import argparse,json,hashlib
from pathlib import Path
from numeric65816_probe import NumericCPU
from calendar65816_probe import CalendarCPU
from calendar_formats_lot47 import patch_calendar_formats
from french_font import encode_fr
class EventNumericCPU(NumericCPU):
 allowed_ranges=NumericCPU.allowed_ranges+((0xc31de0,0xc31df3),(0xc21036,0xc21043))
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();source=a.source.read_bytes();assert hashlib.sha256(source).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e';rom,patch=patch_calendar_formats(source)
assert source[0x8962c:0x8965b]==bytes.fromhex('fe 71 12 7f 7e 02 fe 76 12 7f 7e 20 25 05 fe 75 12 7f 7e 20 26 05 fe 74 12 7f 7e 20 27 05 fe 73 12 7f 7e 20 29 05 8b 00 25 05 8b 01 26 05 00')
assert source[0x5978a:0x59792]==bytes.fromhex('8b 00 26 05 8b 01 25 05')
# VM dispatch table and operand-length tables independently bind opcode8B.
handler=int.from_bytes(source[0x3048f+2*(0x8b-1):0x30491+2*(0x8b-1)],'little')|0xc30000
assert handler==0xc31de0 and source[0x31003+0x8b-1]==3,(hex(handler),'dispatch')
cases=[]
for label,address in [('miho_month',0x0525),('birthday_month',0x0526)]:
 for value in range(1,13):
  c=EventNumericCPU(source);c.Y=1;c.write(0xa8,0x100,3);c.ram[0x100:0x103]=bytes([0,address&255,address>>8]);c.write(address,value,1);c.run(handler);numeric=bytes(c.ram[0x32aa:0x32ca]).split(b'\0')[0];assert numeric==bytes(0x21+int(d) for d in str(value))
  outputs={}
  for name,data in [('source',source),('localized',rom)]:
   f=CalendarCPU(data);f.ram[0x32aa:0x32ab+len(numeric)]=numeric+b'\0';f.write(0x8f,0x100,3);f.ram[0x100]=4;f.run(0x4d3c00,0);out=bytes(f.ram[0x32aa:0x32ca]).split(b'\0')[0];outputs[name]=out.hex()
   if name=='localized':assert out==encode_fr(patch['months'][value-1]['french'])
  cases.append({'path':label,'ram':hex(address),'month':value,'numeric_slot_hex':numeric.hex(),**outputs})
report={'source_sha256':hashlib.sha256(source).hexdigest(),'event_opcode':'8B','handler':hex(handler),'operand_bytes':3,'static_fragments':['C8:962C..965A month/day producer subroutine','C5:978A..9791 birthday month/day producer pair'],'native_month_producer_executions':24,'native_formatter_executions':48,'cases':cases,'scope':'Static instruction fragments plus exact native numeric producer/formatter leafs. The FE clock/birthday extraction, full VM branches, RTC progression and natural event triggers were not executed.','natural_validation':'pending'};a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS 24 actual native event-producer calls and48 formatter calls')
