#!/usr/bin/env python3
"""Keep complete shop-name window pixels and exact native VRAM/tilemap bounds."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.rom.read_bytes();report=json.loads((a.run/'report.json').read_text());assert report['rom_sha256']==hashlib.sha256(r).hexdigest()and not a.out.exists();a.out.mkdir(parents=True);cases=[]
for start in range(0,32,8):
 sheet=Image.new('RGB',(1080,4*132),'#ddd');d=ImageDraw.Draw(sheet)
 for j,c in enumerate(report['cases'][start:start+8]):
  i=c['name_index'];v=Path(c['vram']).read_bytes();st=0x6d0000+i*256;assert v[0x7d00:0x7da0]==r[st:st+160];at=0xb000+3*64+2;tiles=[int.from_bytes(v[at+2*k:at+2*k+2],'little')&1023 for k in range(10)];assert tiles==list(range(0x1d0,0x1da))
  im=Image.open(c['image']).convert('RGB');assert im.size==(256,224);window=im.crop((0,7,256,48));tile=window.resize((512,82),Image.Resampling.NEAREST);x=j%2*540;y=j//2*132;sheet.paste(tile,(x,y+24));d.text((x,y),f'Native shop name {i:02};10 tiles/80px',fill='black');assert sheet.crop((x,y+24,x+512,y+106)).tobytes()==tile.tobytes();cases.append(dict(name_index=i,sheet=f'names_{start//8+1:02}.png',source_offset=hex(st),vram='0x7d00',bytes=160,tiles=tiles,window_sha256=hashlib.sha256(window.tobytes()).hexdigest(),full_window_pixels_preserved=True))
 sheet.save(a.out/f'names_{start//8+1:02}.png')
Image.open(report['cases'][0]['image']).save(a.out/'full_context.png');(a.out/'manifest.json').write_text(json.dumps(dict(rom_sha256=report['rom_sha256'],native_vram_and_tiles_exact=True,cases=cases,visual_review='pending',scope=report['scope']),indent=2)+'\n');print('PASS32 VRAM/name tile sequences;4 complete-window sheets;visual review pending')
