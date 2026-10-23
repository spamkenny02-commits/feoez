#!/usr/bin/env python3
"""Execute cleanup/wrapper up to native font entry for24 font-pool edge cases."""
import argparse,json,hashlib
from pathlib import Path
from numeric65816_probe import NumericCPU
class AtFont(Exception):pass
class FixCPU(NumericCPU):
 allowed_ranges=((0x4c0000,0x4d0000),(0xc176e2,0xc17706),(0xc1775d,0xc1775e),(0xc17959,0xc17979))
 def fetch(self,n=1):
  if self.PC==0xc1775d:raise AtFont()
  return super().fetch(n)
p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();rom=a.rom.read_bytes();entry=int.from_bytes(rom[0x37029:0x3702c],'little');assert rom[0x3712e]==27;cases=[]
for base in (0x4000,0x4810,0x4ff0):
 for pending in range(8):
  c=FixCPU(rom);c.write(0x1c8f,base,2);c.write(0x1c8d,0x4000,2);c.write(0x1c9a,pending,1);c.write(0xd9,0x1d30,3);c.X=19
  try:c.run(entry)
  except AtFont:pass
  else:raise AssertionError('Font entry not reached')
  expected=base if not pending else base+16 if base+16<0x5000 else 0x4000
  assert c.read(0x1c91,2)==c.read(0x1c8f,2)==expected and c.read(0x1c9a,1)==0 and c.X==19 and c.read(0xd9,3)==0x1d30
  cases.append({'base':hex(base),'pending_pixels':pending,'snapshot':hex(expected)})
a.out.write_text(json.dumps({'rom_sha256':hashlib.sha256(rom).hexdigest(),'passed':len(cases),'clear_columns':27,'scope':'Actual cleanup/wrapper execution until font entry; no DMA/PPU emulation. Runtime credits proof separate.','cases':cases},indent=2)+'\n');print('PASS24 credits line-base cases')
