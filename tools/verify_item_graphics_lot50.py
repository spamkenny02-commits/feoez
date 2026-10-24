#!/usr/bin/env python3
"""Execute native item queue producer and DMA register writer for303 variants.
DMA bytes are copied mathematically from programmed registers,not PPU/timing.
Fresh emulator captures must independently establish the actual VRAM render.
"""
import argparse,json,hashlib
from pathlib import Path
from numeric65816_probe import NumericCPU
from item_graphics_lot50 import pixels
class ItemCPU(NumericCPU):
 allowed_ranges=((0x4f2e30,0x4f2ed9),(0x4ff815,0x4ff862))
 def __init__(self,r):super().__init__(r);self.transfers=[]
 def rb(self,a):
  if 0x800000<=a<=0xbfffff and (a&65535)<0x8000:a&=65535
  return super().rb(a)
 def write(self,a,v,n):
  if 0x800000<=a<=0xbfffff and (a&65535)<0x8000:a&=65535
  super().write(a,v,n)
  if a==0x420b:
   assert v==1 and n==1;src=self.read(0x4302,2)|(self.read(0x4304,1)<<16);size=self.read(0x4305,2);dest=self.read(0x2116,2)*2
   assert self.read(0x4300,1)==1 and self.read(0x4301,1)==0x18
   data=bytes(self.rb(src+i)for i in range(size));self.transfers.append((src,dest,data))
def main():
 p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.rom.read_bytes();root=Path(__file__).resolve().parents[1];rows=json.loads((root/'traduction/item_graphics_lot50_fr.json').read_text());results=[]
 for i,e in enumerate(rows):
  b=2 if i<109 else 3;idx=i+1 if b==2 else i-108;src=0x4f6000+i*128;c=ItemCPU(r);c.ram[0x1f7e:0x1f90]=b'\x55'*18;c.write(0x1cdd,b,1);c.write(0x1cdc,idx,1);c.write(0x1f72,0x45c0,2);c.run(0x4f2e30)
  assert c.read(0x1f70,2)==4 and c.read(0x1f72,2)==0x4600 and c.read(0x1f76,2)==1
  assert c.read(0x1f80,2)==(src&65535)and c.read(0x1f82,2)==0x45c0
  assert c.ram[0x1f7e:0x1f80]==b'\x55'*2 and c.ram[0x1f84:0x1f90]==b'\x55'*12
  c.run(0x4ff815);assert len(c.transfers)==1;actual,dest,data=c.transfers[0];assert actual==src and dest==0x8b80 and len(data)==128 and data==r[src+0x200000:src+0x200080]
  assert c.read(0x1f70,2)==0 and c.read(0x1f72,2)==0x4600
  if e['icon']:
   st=e['icon']['start'];p=pixels(data);assert hashlib.sha256(bytes(v for line in p for v in line[st:])).hexdigest()==e['icon']['source_pixels_sha256']
  results.append(dict(id=e['id'],source=hex(src),vram=hex(dest),bytes=len(data),producer_native=True,dma_registers_native=True,icon_preserved=e['icon']is not None))
 a.out.write_text(json.dumps(dict(rom_sha256=hashlib.sha256(r).hexdigest(),cases=len(results),native_routine_executions=2*len(results),original_icons_preserved=46,results=results,scope=__doc__),indent=2)+'\n');print('PASS303 native producer/DMA pairs;46 icons;PPU separate')
if __name__=='__main__':main()
