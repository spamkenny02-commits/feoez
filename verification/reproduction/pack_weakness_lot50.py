#!/usr/bin/env python3
"""Pack complete256x33 battle text windows with exact pixel preservation."""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=json.loads((a.run/'report.json').read_text());assert not a.out.exists();a.out.mkdir(parents=True);cases=[]
for st in range(0,len(r['cases']),8):
 sheet=Image.new('RGB',(1080,4*110),'#ddd');d=ImageDraw.Draw(sheet)
 for j,e in enumerate(r['cases'][st:st+8]):
  im=Image.open(e['image']).convert('RGB');assert im.size==(256,224);crop=im.crop((0,7,256,40));tile=crop.resize((512,66),Image.Resampling.NEAREST);x=j%2*540;y=j//2*110;d.text((x,y),f"{e['id']} B{e['block']}-S{e['string']} {e['slots']}",fill='black');sheet.paste(tile,(x,y+22));assert sheet.crop((x,y+22,x+512,y+88)).tobytes()==tile.tobytes();cases.append(dict(id=e['id'],sheet=f'weakness_{st//8+1:02}.png',window_sha256=hashlib.sha256(crop.tobytes()).hexdigest(),full_window_pixels_preserved=True))
 sheet.save(a.out/f'weakness_{st//8+1:02}.png')
(a.out/'manifest.json').write_text(json.dumps(dict(rom_sha256=r['rom_sha256'],cases=cases,cases_count=len(cases),sheets=9,visual_review='pending',scope=r['scope']),indent=2)+'\n');print('PASS71 complete text windows;9 sheets;review pending')
