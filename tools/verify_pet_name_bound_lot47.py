#!/usr/bin/env python3
"""Native bounded pet-name loader and direct slot-copy probes.
Storage bound, not proof of keyboard entry, pet selection or natural event paths.
"""
import argparse,hashlib,json
from pathlib import Path
from numeric65816_probe import NumericCPU
from text65816_probe import TextCPU
from french_font import WIDTHS
class PetNameCPU(NumericCPU):
 allowed_ranges=((0xc1730c,0xc17330),)
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.source.read_bytes();assert hashlib.sha256(r).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
assert r[0x1730c:0x17330]==bytes.fromhex('18 69 07 5a da 0a 85 00 0a 0a 18 65 00 aa a0 00 bd 3c 04 e8 99 30 1d c8 c0 0a d0 f4 a9 00 99 30 1d fa 7a 60')
assert int.from_bytes(r[0x3092a+3*(0xae-1):0x3092d+3*(0xae-1)],'little')==0xc172d7
assert r[0x62fcc:0x62fd0]==bytes.fromhex('8a 01 30 1d')
patterns=[b'\0'*10,bytes([0x66])*10,bytes([0x9f])*10,bytes([0xce])*10]+[bytes([0x50])*n+b'\0'+b'\x55'*(9-n) for n in range(10)]
count=copies=0
for pet in range(7):
 for name in patterns:
  c=PetNameCPU(r);c.X=17;c.Y=29;at=0x43c+10*(pet+7);c.ram[at:at+10]=name;c.ram[0x1d2f:0x1d3c]=b'\x55'*13;c.run(0xc1730c,pet);assert c.X==17 and c.Y==29 and c.ram[0x1d30:0x1d3a]==name and c.ram[0x1d3a]==0 and c.ram[0x1d2f]==0x55 and c.ram[0x1d3b]==0x55;count+=1;expected=name.split(b'\0')[0]
  for slot in range(4):
   t=TextCPU(r);t.ram[0x1d30:0x1d3b]=name+b'\0';t.ram[0x32aa:0x332a]=b'\x55'*128;t.write(9,0x7e1d30,3);t.X=17;t.Y=29;t.run(0xc32abd,slot);start=0x32aa+32*slot;assert t.ram[start:start+len(expected)+1]==expected+b'\0';assert t.ram[0x32aa:start]==b'\x55'*(start-0x32aa) and t.ram[start+len(expected)+1:0x332a]==b'\x55'*(0x332a-start-len(expected)-1);assert t.X==17 and t.Y==29;copies+=1
history_loads=0
assert r[0x174c0:0x174dc].find(bytes.fromhex('8a 20 0f 73'))>=0
for record in range(7):
 for name in patterns:
  c=PetNameCPU(r);c.X=17;c.Y=29;at=0x43c+10*record;c.ram[at:at+10]=name;c.ram[0x1d2f:0x1d3c]=b'\x55'*13;c.run(0xc1730f,record);assert c.ram[0x1d30:0x1d3a]==name and c.ram[0x1d3a]==0 and c.ram[0x1d2f]==0x55 and c.ram[0x1d3b]==0x55 and (c.X,c.Y)==(17,29);history_loads+=1
maxglyph=max(r[WIDTHS+0x10:WIDTHS+0xe0]);out={'source_sha256':hashlib.sha256(r).hexdigest(),'native_name_loader':'C1:730C..732F','finite_storage_records_tested':7,'loader_executions':count,'history_record_loader_executions':history_loads,'slot_copy_executions':copies,'maximum_storage_bytes':10,'terminator_appended_at':'7E:1D3A','consumer_fragment':'C6:2FCC 8A 01 30 1D before B041-S025','maximum_native_glyph_advance':maxglyph,'conservative_pet_name_pixels':10*maxglyph,'scope':'Native fixed10-byte record load, explicit NUL and all four text slots. Does not validate keyboard alphabet, current pet selection, full events or natural nursery navigation.'};a.out.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS',count,'name loads,',copies,'slot copies; conservative',10*maxglyph,'px')
