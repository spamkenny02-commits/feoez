#!/usr/bin/env python3
"""Pack the entire real battle banner, preserving every pixel of its40px strip."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);r=json.loads(a.report.read_text());unique={};cases=[]
for case in r['cases']:
 path=Path(case['image']);assert hashlib.sha256(path.read_bytes()).hexdigest()==case['capture_sha256'];im=Image.open(path).convert('RGB');crop=im.crop((0,0,256,40));h=hashlib.sha256(crop.tobytes()).hexdigest();unique.setdefault(h,{'id':case['id'],'crop':crop,'source_capture_sha256':case['capture_sha256']});cases.append({k:v for k,v in case.items() if k!='image'}|{'crop_sha256':h})
sheets=[];tiles={};items=list(unique.items())
for start in range(0,len(items),16):
 canvas=Image.new('RGB',(1024,864),'#e5e5e5');draw=ImageDraw.Draw(canvas);manifest=[]
 for n,(h,item) in enumerate(items[start:start+16]):
  x=n%2*512;y=n//2*108;crop=item['crop'].resize((512,80),Image.Resampling.NEAREST);draw.text((x+6,y+3),item['id'],fill='black');canvas.paste(crop,(x,y+24));assert ImageChops.difference(canvas.crop((x,y+24,x+512,y+104)),crop).getbbox() is None;tiles[h]={'sheet':f'banner_{start//16:03}.png','tile':n};manifest.append({'id':item['id'],'crop_sha256':h,'source_capture_sha256':item['source_capture_sha256'],'bbox':[x,y+24,x+512,y+104]})
 p=a.out/f'banner_{start//16:03}.png';canvas.save(p);sheets.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'captures':manifest,'reviewed':False})
for case in cases:case.update(tiles[case['crop_sha256']])
r={k:v for k,v in r.items() if k not in ('cases','entry_state_sha256')};r.update(cases=cases,unique_banner_captures=len(items),sheets=sheets,packing={'crop':[0,0,256,40],'scale':2,'interpolation':'nearest','all_crop_pixels_verified':True},visual_review='pending');(a.out/'report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(len(cases),'cases',len(items),'unique banner crops',len(sheets),'sheets')
