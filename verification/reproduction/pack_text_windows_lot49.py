#!/usr/bin/env python3
"""Pack complete80px native text windows without redrawing or losing pixels."""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
p=argparse.ArgumentParser();p.add_argument('--images',type=Path,required=True);a=p.parse_args();dest=a.images;d=json.loads((dest/'render_report.json').read_text());assert not d.get('packing');system={'check_a.png','check_b.png','main_menu.png','settings.png','region_map.png'};items=[(n,c) for n,c in d['images'].items() if n not in system];sheets=[];tiles={}
for start in range(0,len(items),16):
 im=Image.new('RGB',(1024,1488),'#ddd');draw=ImageDraw.Draw(im);manifest=[]
 for j,(name,c) in enumerate(items[start:start+16]):
  assert hashlib.sha256((dest/name).read_bytes()).hexdigest()==c['sha256'];crop=Image.open(dest/name).convert('RGB').crop((0,144,256,224)).resize((512,160),Image.Resampling.NEAREST);x=j%2*512;y=j//2*186;draw.text((x+5,y+3),name,fill='black');im.paste(crop,(x,y+22));assert ImageChops.difference(im.crop((x,y+22,x+512,y+182)),crop).getbbox() is None;tiles[name]={'sheet':f'field_{start//16:03}.png','tile':j,'source_sha256':c['sha256']};manifest.append({'source':name,**tiles[name]})
 fn=f'field_{start//16:03}.png';im.save(dest/fn);sheets.append({'file':fn,'sha256':hashlib.sha256((dest/fn).read_bytes()).hexdigest(),'captures':manifest,'reviewed':False})
for g in d['groups'].values():
 for c in g['cases']:c['review_tiles']=[tiles[n] for n in c['review_images']];c['review_images']=list(dict.fromkeys(t['sheet'] for t in c['review_tiles']))
d['source_captures']={n:v for n,v in items};d['sheets']=sheets;d['images']={n:c for n,c in d['images'].items() if n not in tiles}|{s['file']:{'sha256':s['sha256']} for s in sheets};d['packing']={'native_crop':[0,144,256,224],'scale':2,'all_crop_pixels_verified':True};(dest/'render_report.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for n,_ in items:(dest/n).unlink()
print(len(items),'captures packed; actual review pending')
