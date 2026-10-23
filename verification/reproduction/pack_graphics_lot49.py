#!/usr/bin/env python3
"""Decode actual patched2bpp strips; source-raster review is separate from PPU."""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();root=Path(__file__).resolve().parents[2];rom=a.rom.read_bytes();entries=json.loads((root/'traduction/menu_graphics_lot49_fr.json').read_text());a.out.mkdir(parents=True,exist_ok=True);sheets=[]
for start in range(0,len(entries),32):
 im=Image.new('RGB',(1024,960),'#ddd');d=ImageDraw.Draw(im);items=[]
 for j,e in enumerate(entries[start:start+32]):
  raw=rom[int(e['offset'],16):int(e['offset'],16)+e['tiles']*16];strip=Image.new('RGB',(e['tiles']*8,8),'#000044');pixels=strip.load()
  for y in range(8):
   for x in range(e['tiles']*8):
    off=x//8*16+y*2;v=((raw[off]>>(7-x%8))&1)|(((raw[off+1]>>(7-x%8))&1)<<1);pixels[x,y]=[(0,0,68),(119,119,119),(255,255,255),(255,255,255)][v]
  x=j%2*512;y=j//2*60;d.text((x+3,y+2),e['id']+' '+e['french'],fill='black');im.paste(strip.resize((strip.width*2,16),Image.Resampling.NEAREST),(x+3,y+24));items.append({'id':e['id'],'offset':e['offset'],'tiles':e['tiles'],'french':e['french'],'span_sha256':hashlib.sha256(raw).hexdigest()})
 fn=f'graphics_{start//32:03}.png';im.save(a.out/fn);sheets.append({'file':fn,'sha256':hashlib.sha256((a.out/fn).read_bytes()).hexdigest(),'strips':items,'reviewed':False})
(a.out/'report.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(rom).hexdigest(),'native_2bpp_strips':len(entries),'sheets':sheets,'scope':'Decoded native bitmap strips, not actual context/tilemap/availability proof. Live menu paths in UI report.'},ensure_ascii=False,indent=2)+'\n')
