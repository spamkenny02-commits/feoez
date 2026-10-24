#!/usr/bin/env python3
"""Native pending-name dispatch and DMA registers for32 allocated shop headers.
Real stock descriptors and source FD80 operands establish static consumers.
DMA transfer copies from programmed registers;actual PPU and natural visits separate.
"""
import argparse,hashlib,json
from pathlib import Path
from verify_item_graphics_lot50 import ItemCPU
ROOT=Path(__file__).resolve().parents[1]
class ShopNameCPU(ItemCPU):
 allowed_ranges=((0x4ff800,0x4ff815),(0x4ff8c0,0x4ff8fe))
def main():
 p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.rom.read_bytes();rows=json.loads((ROOT/'traduction/shop_names_lot50_fr.json').read_text());checks=[]
 assert len(rows)==29 and sum(x['new_distinct_source']for x in rows)==28
 assert int.from_bytes(r[0x2e6e16:0x2e6e18],'little')==0x6d3e and 0x6800+122*11==0x6d3e
 for e in rows:
  for use in e['ordinary_stock_consumers']:
   at=int(use['script_offset'],16);stock=use['stock'];desc=0x2e6800+11*(stock-1);assert r[at:at+3]==bytes([0xfd,0x80,stock]) and r[desc]==e['name_index'] and desc==int(use['descriptor_offset'],16)
 for i in range(32):
  c=ShopNameCPU(r);c.write(0x1f70,0,2);c.write(0x1f7b,0x55,1);c.write(0x1f7c,i+1,1);c.write(0x1f7d,0xaa,1);c.run(0x4ff800);assert len(c.transfers)==1
  src,dest,data=c.transfers[0];assert src==0x4d0000+256*i and dest==0x7d00 and len(data)==160 and data==r[0x6d0000+256*i:0x6d00a0+256*i]
  assert c.read(0x1f7c,1)==0 and c.read(0x1f7b,1)==0x55 and c.read(0x1f7d,1)==0xaa
  checks.append(dict(name_index=i,source=hex(src),bytes=160,vram=hex(dest),pending_native_dispatch=True,dma_registers_native=True))
 a.out.write_text(json.dumps(dict(rom_sha256=hashlib.sha256(r).hexdigest(),allocated_titles=32,translated_fields=29,new_distinct_sources=28,semantic_aliases_excluded=1,real_stock_descriptors=122,results=checks,scope=__doc__),indent=2)+'\n');print('PASS32 native pending-name/DMA cases;29 translated fields,28 new sources')
if __name__=='__main__':main()
