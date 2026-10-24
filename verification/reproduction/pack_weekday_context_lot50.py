#!/usr/bin/env python3
"""Exact ordinary weekday VRAM/tilemap/PPU contracts plus complete windows.
Only the original22/12/1995 clock state is opened;not other date branches.
"""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.rom.read_bytes();report=json.loads((a.run/'report.json').read_text());assert report['rom_sha256']==hashlib.sha256(r).hexdigest()and report['controller_only']and not a.out.exists();a.out.mkdir(parents=True);main=(a.run/'main.vram').read_bytes();cal=(a.run/'almanac.vram').read_bytes();assert main[0x7c00:0x7c70]==r[0x6f0900:0x6f0970]and cal[0x7c00:0x7c70]==r[0x6f1600:0x6f1670]
assert int.from_bytes(main[0xb000+15*64+2*2:0xb000+15*64+2*2+2],'little')&1023==0x1c5
at=0xb000+14*64+10*2;assert [int.from_bytes(cal[at+2*k:at+2*k+2],'little')&1023 for k in range(21)]==list(range(0x1c0,0x1c7))*3
palette=[(0,0,57),(0,0,0),(255,255,255)]
def tile_pixels(data):
 out=Image.new('RGB',(len(data)//16*8,8))
 for y in range(8):
  for x in range(out.width):
   pos=x//8*16+2*y;bit=128>>(x%8);v=int(bool(data[pos]&bit))+2*int(bool(data[pos+1]&bit));out.putpixel((x,y),palette[v])
 return out
im=Image.open(a.run/'almanac.png').convert('RGB');chart=tile_pixels(r[0x6f1600:0x6f1670]*3);assert im.crop((80,111,248,119)).tobytes()==chart.tobytes();menu=Image.open(a.run/'main.png').convert('RGB');assert menu.crop((16,119,24,127)).tobytes()==tile_pixels(r[0x6f0950:0x6f0960]).tobytes()
files=sorted(a.run.glob('*.png'));assert len(files)==6;sheet=Image.new('RGB',(810,2*258),'#ddd');d=ImageDraw.Draw(sheet);cases=[]
for j,f in enumerate(files):
 im=Image.open(f).convert('RGB');assert im.size==(256,224);x=j%3*270;y=j//3*258;sheet.paste(im,(x,y+25));assert sheet.crop((x,y+25,x+256,y+249)).tobytes()==im.tobytes();d.text((x,y),f.stem,fill='black');cases.append(dict(id=f.stem,pixels_sha256=hashlib.sha256(im.tobytes()).hexdigest(),all_pixels_preserved=True))
sheet.save(a.out/'weekday_views.png');(a.out/'report.json').write_text(json.dumps(dict(rom_sha256=report['rom_sha256'],date_context='22/12/1995 Friday index5',both_weekday_banks_vram_exact=True,friday_menu_tile='1C5 at(2,15)',chart_21_tiles_exact=True,chart_21_tile_pixels_exact=True,menu_friday_pixels_exact=True,ppu_chart_rectangle=[80,111,248,119],ppu_menu_weekday_rectangle=[16,119,24,127],date_header='Dynamic2byte string table checked separately by native header probe;complete V header needs actual visual reading',cases=cases,visual_review='pending',scope=__doc__),indent=2)+'\n');print('PASS2native VRAM banks,22weekday tile instances and exact pixels;6complete views;header visual pending')
