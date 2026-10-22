#!/usr/bin/env python3
"""Pack native text-window crops without changing their pixels.
Use a reviewed manifest of source image hashes, grouped into sheets.
Full source captures remain private; all text-window pixels are preserved.
"""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
p=argparse.ArgumentParser();p.add_argument('--images',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);a=p.parse_args();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();report=json.loads((a.images/'render_report.json').read_text());manifest=json.loads(a.manifest.read_text());assert manifest['rom_sha256']==report['rom_sha256'];original=report.get('source_captures',report['images']);bysha={x['sha256']:name for name,x in original.items()};tiles={};sheets={}
for sheet in manifest['sheets']:
 canvas=Image.new('RGB',(1024,1488),'#e5e5e5');draw=ImageDraw.Draw(canvas)
 for j,item in enumerate(sheet['captures']):
  source=a.images/bysha[item['sha256']];assert sha(source)==item['sha256'];crop=Image.open(source).convert('RGB').crop((0,144,256,224)).resize((512,160),Image.Resampling.NEAREST);x=j%2*512;y=j//2*186;draw.text((x+6,y+3),item['group']+' '+item['case'],fill='black');canvas.paste(crop,(x,y+22));tiles[bysha[item['sha256']]]={'sheet':sheet['file'],'tile':j,'bbox':[x,y+22,x+512,y+182],'sha256':item['sha256']}
  assert ImageChops.difference(canvas.crop((x,y+22,x+512,y+182)),crop).getbbox() is None
 target=a.images/sheet['file'];canvas.save(target);assert sha(target)==sheet['sha256'],'Reviewed sheet pixels/labels differ';sheets[sheet['file']]={'sha256':sha(target),'native_text_crops':len(sheet['captures'])}
assert len(tiles)==report['unique_text_captures']==619
system={k:v for k,v in report['images'].items() if k not in tiles};assert set(system)=={'check_a.png','check_b.png','main_menu.png','settings.png','region_map.png'}
for group in report['groups'].values():
 for case in group['cases']:
  case['review_tiles']=[tiles[n] for n in case['review_images']];case['review_images']=list(dict.fromkeys(t['sheet'] for t in case['review_tiles']))
report['source_captures']={k:v for k,v in original.items() if k in tiles};report['images']=system|sheets;report['packing']={'native_crop':[0,144,256,224],'scale':2,'interpolation':'nearest','sheets':len(sheets),'source_captures':len(tiles),'all_crop_pixels_verified':True};(a.images/'render_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
for name in tiles:(a.images/name).unlink()
print('PASS',len(tiles),'native crops packed into',len(sheets),'reviewed sheets')
