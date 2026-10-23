#!/usr/bin/env python3
"""Execute unchanged C37071 copier over all629 sequential credits records."""
import argparse,json,hashlib
from pathlib import Path
from numeric65816_probe import NumericCPU
class CreditCPU(NumericCPU):
 allowed_ranges=((0xc37071,0xc370a6),)
p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();rom=a.rom.read_bytes();c=CreditCPU(rom);c.write(0xe6,0x4d5000,3);records=[]
while c.read(0xe6,3)<0x4d668c:
 start=c.read(0xe6,3);file=start+0x200000;end=rom.index(0,file);raw=rom[file:end];assert len(raw)<=45
 c.ram[0x1d2e:0x1d65]=b'\x55'*55;c.run(0xc37071,limit=50000)
 assert bytes(c.ram[0x1d30:0x1d30+len(raw)+1])==raw+b'\0'
 assert c.ram[0x1d2e:0x1d30]==b'\x55'*2 and c.ram[0x1d30+len(raw)+1:0x1d65]==b'\x55'*(0x1d65-0x1d30-len(raw)-1)
 assert c.read(0xe6,3)==start+len(raw)+1 and c.read(0xd9,3)==0x1d30
 records.append({'cursor':hex(start),'bytes':len(raw)})
assert len(records)==629 and rom[0x6d668c]==255
a.out.write_text(json.dumps({'rom_sha256':hashlib.sha256(rom).hexdigest(),'passed':len(records),'final_cursor':hex(c.read(0xe6,3)),'canaries_preserved':True,'scope':'Sequential native copy only; PPU/timing/ending separate.','records':records},indent=2)+'\n');print('PASS629 native credits copies')
