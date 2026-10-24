#!/usr/bin/env python3
"""Finite four-slot weakness expansions through the native FD8B copier.
No event selection,PPU or naturally triggered View action is established.
"""
import argparse,hashlib,itertools,json
from pathlib import Path
from numeric65816_probe import NumericCPU
from cpu65816_probe import CPU
from french_font import encode_fr,WIDTHS
class WeakCPU(NumericCPU):
 allowed_ranges=((0xc329b6,0xc32aa4),(0xc02c5e,0xc02d00),(0xc029a1,0xc029bb),(0xc07880,0xc0793d),(0x4d3900,0x4d393f),(0x4d3b80,0x4d3be9),(0x4f1d30,0x4f1d48),(0x4d2c00,0x4d2c34))
 def mapped(self,a):
  if 0xdf0000<=a<0xe00000:return a-0xb00000
  return super().mapped(a)
 load_block=CPU.load_block
 select=CPU.select
 string=CPU.string
p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.rom.read_bytes();elements=['Physique','Feu','Eau','Vent','Foudre'];results=[]
for used in range(5):
 for positions in itertools.combinations(range(4),used):
  for values in itertools.permutations(elements,used):
   slots=['']*4
   for pos,text in zip(positions,values):slots[pos]=text
   for idx,suffix in [(8,' : faib. extrême'),(9,' : faiblesse')]:
    c=WeakCPU(r);c.ram[0x1d2e:0x1d65]=b'\x55'*55;c.ram[0x32a9]=0x55;c.ram[0x332a]=0x55
    for i,s in enumerate(slots):
     raw=encode_fr(s);st=0x32aa+32*i;c.ram[st:st+32]=raw+b'\0'+bytes(31-len(raw))
    c.load_block(44);c.X=0;c.run(0xc07880,idx,limit=500000);actual=bytes(c.ram[0x1d30:0x1d65]).split(b'\0')[0];expected=b'\x1c'.join(encode_fr(s)+b'\x03'for s in slots)+encode_fr(suffix);assert actual==expected,(idx,slots,actual.hex(),expected.hex());assert len(actual)<=45
    assert c.ram[0x1d2e]==0x55 and c.ram[0x1d5e:0x1d65]==b'\x55'*7 and c.ram[0x32a9]==0x55 and c.ram[0x332a]==0x55
    px=sum(r[WIDTHS+b]for b in actual);c.write(0,0,1);tiles=c.run(0x4d2c00);assert tiles==(px+7)//8 and tiles<=28
    results.append(dict(source=idx,slots=slots,bytes=len(actual),pixels=px,tiles=tiles))
assert len(results)==1002
a.out.write_text(json.dumps(dict(rom_sha256=hashlib.sha256(r).hexdigest(),expansions=len(results),maximum_bytes=max(x['bytes']for x in results),maximum_pixels=max(x['pixels']for x in results),four_inserted_03_markers=True,canaries_preserved=True,cases=results,scope=__doc__),ensure_ascii=False,indent=2)+'\n');print('PASS1002 native expansions',max(x['bytes']for x in results),'bytes',max(x['pixels']for x in results),'px')
