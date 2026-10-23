#!/usr/bin/env python3
"""Match fresh shop VRAM strips and observed tile sequences to exact-ROM bytes."""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True);r=a.rom.read_bytes();report=json.loads((a.run/'report.json').read_text());assert report['rom_sha256']==hashlib.sha256(r).hexdigest();rows=json.loads((ROOT/'traduction/shop_graphics_lot50_fr.json').read_text());checks=[]
contracts={'SHOP-BUY':('main',0x7200,0x6f4700,3,15,0x120,2),'SHOP-SELL':('main',0x7220,0x6f4720,5,15,0x122,2),'SHOP-GREETING':('main',0x7240,0x6f4740,3,20,0x124,5),'SHOP-OWNED':('buy',0x7830,0x6f4d30,24,22,0x183,4),'SHOP-SELL-QUESTION':('sell',0x7290,0x6d3090,5,20,0x129,10),'SHOP-PHARMACIST':('main',0x7d00,0x6d1300,3,1,0x1d0,10)}
for e in rows:
 view,va,st,y,x,t,n=contracts[e['id']];v=(a.run/(view+'.vram')).read_bytes();part=next(s for s in e['strips']if int(s['offset'],16)==st);size=part['tiles']*16;assert v[va:va+size]==r[st:st+size],(e['id'],'VRAM');at=0xb000+64*y+2*x;actual=[int.from_bytes(v[at+2*i:at+2*i+2],'little')&1023 for i in range(n)];assert actual==list(range(t,t+n)),(e['id'],'tilemap',actual);checks.append(dict(id=e['id'],view=view,vram=hex(va),source=hex(st),bytes=size,tiles=actual,exact=True))
v=(a.run/'main.vram').read_bytes();assert v[0x7290:0x7340]==r[0x6f4790:0x6f4840];v=(a.run/'sell.vram').read_bytes();assert v[0x7440:0x74b0]==r[0x6d3240:0x6d32b0]
files=sorted(a.run.glob('*.png'));cases=[];sheet=Image.new('RGB',(810,774),'#ddd');d=ImageDraw.Draw(sheet)
for i,p in enumerate(files):
 im=Image.open(p).convert('RGB');assert im.size==(256,224);x=i%3*270;y=i//3*258;sheet.paste(im,(x,y+25));assert sheet.crop((x,y+25,x+256,y+249)).tobytes()==im.tobytes();d.text((x,y),p.stem,fill='black');cases.append(dict(id=p.stem,pixels_sha256=hashlib.sha256(im.tobytes()).hexdigest()))
sheet.save(a.out/'shop_views.png');(a.out/'report.json').write_text(json.dumps(dict(rom_sha256=report['rom_sha256'],native_vram_checks=checks,help_line_exact=True,sell_cash_variant_exact=True,full_captures=cases,all_capture_pixels_preserved=True,visual_review='pending',scope=report['scope']),indent=2)+'\n');print('PASS shop VRAM and tilemaps;visual review pending')
