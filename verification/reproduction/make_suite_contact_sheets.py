#!/usr/bin/env python3
"""Create reproducible native text crops for subsequent human visual review.
The pending manifest records original image hashes. Packing is a separate step.
"""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('--images',type=Path,required=True);a=p.parse_args();r=json.loads((a.images/'render_report.json').read_text());assert 'source_captures' not in r,'Use fresh collected full frames, not an already packed report';system={'check_a.png','check_b.png','main_menu.png','settings.png','region_map.png'};ims=[(n,x) for n,x in r['images'].items() if n not in system];cases={}
for group,rs in r['groups'].items():
 for case in rs['cases']:
  for name in case['review_images']:cases.setdefault(name,(group,case['case']))
assert len(ims)==r['unique_text_captures'];manifest={'rom_sha256':r['rom_sha256'],'review_status':'pending','sheets':[]}
for k in range(0,len(ims),16):
 canvas=Image.new('RGB',(1024,1488),'#e5e5e5');draw=ImageDraw.Draw(canvas);items=[]
 for j,(name,meta) in enumerate(ims[k:k+16]):
  path=a.images/name;assert hashlib.sha256(path.read_bytes()).hexdigest()==meta['sha256'];group,case=cases[name];x=j%2*512;y=j//2*186;draw.text((x+6,y+3),group+' '+case,fill='black');crop=Image.open(path).convert('RGB').crop((0,144,256,224)).resize((512,160),Image.Resampling.NEAREST);canvas.paste(crop,(x,y+22));items.append({'sha256':meta['sha256'],'group':group,'case':case,'source':name})
 name=f'contact_{k//16:03}.png';canvas.save(a.images/name);manifest['sheets'].append({'file':name,'sha256':hashlib.sha256((a.images/name).read_bytes()).hexdigest(),'captures':items})
(a.images/'contact_sheets.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Created',len(ims),'native crops in',len(manifest['sheets']),'sheets; visual review pending.')
