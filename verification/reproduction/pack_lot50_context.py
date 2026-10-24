#!/usr/bin/env python3
"""Pack selected complete256x224 context screens without changing any pixel."""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('--input-list',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--rom-sha256',required=True);a=p.parse_args();paths=json.loads(a.input_list.read_text());assert not a.out.exists();a.out.mkdir(parents=True);cases=[]
for start in range(0,len(paths),12):
 sheet=Image.new('RGB',(810,4*258),'#ddd');d=ImageDraw.Draw(sheet)
 for j,path in enumerate(paths[start:start+12]):
  f=Path(path);im=Image.open(f).convert('RGB');assert im.size==(256,224);x=j%3*270;y=j//3*258;sheet.paste(im,(x,y+25));assert sheet.crop((x,y+25,x+256,y+249)).tobytes()==im.tobytes();label=f.parent.name.replace('lot50_recovery42a_','')+'/'+f.stem;d.text((x,y),label,fill='black');cases.append(dict(id=label,sheet=f'context_{start//12+1:02}.png',pixels_sha256=hashlib.sha256(im.tobytes()).hexdigest(),full_pixels_preserved=True))
 sheet.save(a.out/f'context_{start//12+1:02}.png')
(a.out/'manifest.json').write_text(json.dumps(dict(rom_sha256=a.rom_sha256,captures=cases,sheets=(len(paths)+11)//12,visual_review='pending',scope='Complete selected context captures;not all branches,dynamic values,dates or events'),indent=2)+'\n');print('Packed',len(paths),'complete context images')
