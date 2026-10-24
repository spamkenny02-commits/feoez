#!/usr/bin/env python3
"""Execute FE-F4's native weakness-byte getter for13 actors and5 attributes.
Finite address/value test only;does not execute full View event/PPU branches.
"""
import argparse,json,hashlib
from pathlib import Path
from numeric65816_probe import NumericCPU
class GetterCPU(NumericCPU):allowed_ranges=((0xc4166f,0xc4167f),(0xc428b3,0xc428cc))
p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.rom.read_bytes();at=0x3092a+3*(0xf4-1);assert int.from_bytes(r[at:at+3],'little')==0xc4166f;assert r[0x66079:0x6607c]==bytes.fromhex('09 fe f4');cases=[]
for actor in range(13):
 for attr in range(5):
  c=GetterCPU(r);c.X=117;c.Y=29;c.write(0xa8,0x100,3);c.write(0x100,attr,1);c.write(0x193f,actor,1)
  for i in range(91):c.ram[0x1777+i]=(37+19*i)&255
  expected=c.ram[0x1777+7*actor+attr];c.run(0xc4166f);assert c.ram[0x1098]==expected and c.ram[0x1099]==0 and c.X==117 and c.Y==29 and c.S==0x1ff
  cases.append(dict(actor=actor,attribute=attr,address=hex(0x1777+7*actor+attr),value=expected))
a.out.write_text(json.dumps(dict(rom_sha256=hashlib.sha256(r).hexdigest(),getter_executions=65,cases=cases,scope=__doc__),indent=2)+'\n');print('PASS65 FE-F4 native getter calls')
