#!/usr/bin/env python3
"""Exact native VRAM and complete64x8 PPU strip checks;16 cases per sheet.
All pixels outside that strip must stay identical in this controlled fixture.
"""
import argparse,json,hashlib,sys
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'));from item_graphics_lot50 import pixels
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.rom.read_bytes();report=json.loads((a.run/'report.json').read_text());assert report['rom_sha256']==hashlib.sha256(r).hexdigest();assert not a.out.exists();a.out.mkdir(parents=True);rows=json.loads((ROOT/'traduction/item_graphics_lot50_fr.json').read_text());cases=[];palette={};outside=None;fullref=None
for n in range(0,303,16):
 sheet=Image.new('RGB',(1120,4*94),'#ddd');draw=ImageDraw.Draw(sheet)
 for j,case in enumerate(report['fixtures'][n:n+16]):
  i=case['index'];e=rows[i];st=0x6f6000+128*i;raw=r[st:st+128];v=Path(case['vram']).read_bytes();assert v[0x8b80:0x8c00]==raw,e['id'];at=0xb000+64*11+2*8;tiles=[int.from_bytes(v[at+2*k:at+2*k+2],'little')&1023 for k in range(8)];assert tiles==list(range(0x2b8,0x2c0)),(i,tiles)
  im=Image.open(case['screenshot']).convert('RGB');crop=im.crop((64,79,128,87));pp=pixels(raw)
  for y in range(8):
   for x in range(64):
    c=pp[y][x];rgb=crop.getpixel((x,y))
    if c in palette:assert palette[c]==rgb,(i,x,y,c,rgb,palette[c])
    else:assert rgb not in palette.values();palette[c]=rgb
  masked=im.copy();masked.paste((0,0,0),(64,79,128,87));h=hashlib.sha256(masked.tobytes()).hexdigest()
  if outside is None:outside=h;fullref=im.copy()
  assert outside==h,(i,'outside-strip pixels changed')
  x=j%4*280;y=j//4*94;draw.text((x,y),f"{i:03} {e['id']} {e['french_short']}",fill='black');tile=crop.resize((256,32),Image.Resampling.NEAREST);sheet.paste(tile,(x,y+20));assert sheet.crop((x,y+20,x+256,y+52)).tobytes()==tile.tobytes();draw.text((x,y+56),e['french_full'][:45],fill='black');draw.text((x,y+72),f"{e['pixels']}/{e['limit']}px;icon="+str(e['icon']is not None),fill='black');cases.append(dict(index=i,id=e['id'],sheet=f'items_{n//16+1:02}.png',full_strip_pixels_sha256=hashlib.sha256(crop.tobytes()).hexdigest(),vram_bytes_exact=True,pixels_exact=True,icon_preserved=e['icon']is not None))
 sheet.save(a.out/f'items_{n//16+1:02}.png')
fullref.save(a.out/'full_context.png');(a.out/'manifest.json').write_text(json.dumps(dict(rom_sha256=report['rom_sha256'],cases=cases,cases_count=len(cases),sheets=19,palette={str(k):v for k,v in palette.items()},outside_strip_sha256=outside,all_outside_strip_pixels_identical=True,native_vram_bytes_exact=True,full64x8_pixels_exact=True,visual_review='pending',scope=report['scope']),ensure_ascii=False,indent=2)+'\n');print('PASS303 exact VRAM/PPU strips;19 sheets;review pending')
