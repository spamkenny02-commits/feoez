#!/usr/bin/env python3
"""Match every translated credit occurrence against full native glyph pixels.
Compact sheets keep full256px captured lines, nearest scaling, no text redraw.
"""
import argparse,json,hashlib,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from french_font import FONT,WIDTHS
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--images',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);rom=a.rom.read_bytes();source=a.source.read_bytes();assert hashlib.sha256(source).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e';entries=json.loads((ROOT/'traduction/credits_lot49_fr.json').read_text());targets={int(e['offset'],16):e for e in entries};p0=p1=0x6d5000;expected={}
def trim(mask):
 yy,xx=np.where(mask)
 if not len(yy):return None
 return mask[yy.min():yy.max()+1,xx.min():xx.max()+1]
def key(mask):return (mask.shape,hashlib.sha256(mask.tobytes()).hexdigest())
for index in range(629):
 e0=source.index(0,p0);e1=rom.index(0,p1)
 if p0 in targets:
  raw=rom[p1:e1];bits=np.zeros((16,256),dtype=bool);x=0
  for code in raw:
   for y in range(16):
    word=int.from_bytes(rom[FONT+code*32+y*2:FONT+code*32+y*2+2],'big')
    for z in range(16):
     if word&(1<<(15-z)):bits[y,x+z]=True
   x+=rom[WIDTHS+code]
  mask=trim(bits);expected[targets[p0]['id']]={'index':index,'mask':mask,'key':key(mask),'text':targets[p0]['french']}
 p0=e0+1;p1=e1+1
assert p0==p1==0x6d668c and len(expected)==122
bykey={}
for ident,e in expected.items():bykey.setdefault(e['key'],[]).append(ident)
found={}
for path in sorted(a.images.glob('credits_*.png')):
 im=Image.open(path).convert('RGB');mask=np.array(im).max(axis=2)>100;ys=np.where(mask.any(axis=1))[0];groups=[]
 for y in ys:
  if not groups or y-groups[-1][-1]>3:groups.append([y])
  else:groups[-1].append(y)
 for group in groups:
  y0,y1=int(group[0]),int(group[-1])+1
  if y0<3 or y1>221:continue
  cropped=trim(mask[y0:y1]);k=key(cropped)
  for ident in bykey.get(k,[]):
   if ident not in found:found[ident]={'image':path.name,'capture_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'y0':max(0,y0-3),'y1':min(224,y1+3)}
print('matched',len(found),'of122; missing',[i for i in expected if i not in found])
sheets=[];ids=[i for i in expected if i in found]
for start in range(0,len(ids),16):
 canvas=Image.new('RGB',(1024,640),'#ddd');d=ImageDraw.Draw(canvas);items=[]
 for j,ident in enumerate(ids[start:start+16]):
  f=found[ident];im=Image.open(a.images/f['image']).convert('RGB');crop=im.crop((0,f['y0'],256,f['y1'])).resize((512,2*(f['y1']-f['y0'])),Image.Resampling.NEAREST);x=j%2*512;y=j//2*80;d.text((x+5,y+2),ident,fill='black');canvas.paste(crop,(x,y+18));assert ImageChops.difference(canvas.crop((x,y+18,x+512,y+18+crop.height)),crop).getbbox() is None;items.append({'id':ident,'text':expected[ident]['text'],**f,'bbox':[x,y+18,x+512,y+18+crop.height]})
 path=a.out/f'credits_{start//16:03}.png';canvas.save(path);sheets.append({'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'occurrences':items,'reviewed':False})
report={'rom_sha256':hashlib.sha256(rom).hexdigest(),'matched_native_pixel_occurrences':len(found),'total_translated_occurrences':122,'missing':[i for i in expected if i not in found],'sheets':sheets,'pixel_comparison':'Complete trimmed native-font ink masks match captured PPU lines exactly; full-width captures packed at2x nearest.','visual_review':'pending','scope':'Staged full sequential native credits flow, not natural ending.'};(a.out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
assert len(found)==122
