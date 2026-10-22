#!/usr/bin/env python3
"""Original location-banner centering leaf, pinned native VWF advances.
Static native consumer references and direct leaf executions, not map/menu UI.
"""
import argparse,json,hashlib
from pathlib import Path
from numeric65816_probe import NumericCPU
from french_font import encode_fr,visible_width,patch_font
class LocationCPU(NumericCPU):
 allowed_ranges=((0x4d3e00,0x4d3e2e),)
 def mapped(self,address):
  if 0xdf0000<=address<0xe00000:return address-0xb00000
  return super().mapped(address)
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();source=a.source.read_bytes();assert hashlib.sha256(source).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e';r,_=patch_font(source);root=Path(__file__).resolve().parents[1];lot=json.loads((root/'traduction/lot47_fr.json').read_text());rows=[]
for b in [14,15]:
 at=0x34b53 if b==14 else 0x34afd;fragment=bytes([0xa9,b])+bytes.fromhex('22 b6 29 c3 bd ca 07 22 da 29 c3 20 e2 4d 22 00 3e 4d');assert r[at:at+len(fragment)]==fragment
 for i,text in lot[str(b)].items():
  raw=encode_fr(text);assert len(raw)<=31 and b'\x01' not in raw and all(v>=0x10 for v in raw)
  c=LocationCPU(r);c.X=17;c.Y=29;c.DBR=0x42;c.ram[0x48ab:0x48cd]=b'\x55'*34;c.ram[0x48ac:0x48ad+len(raw)]=raw+b'\0';before=bytes(c.ram[0x48ab:0x48cd]);got=c.run(0x4d3e00)
  width=visible_width(text,r);expected=(32-width//8)//2;assert got==expected and c.read(0,1)==width//8,(text,got,width)
  assert (c.X,c.Y,c.DBR,c.S)==(17,29,0x42,0x1ff) and bytes(c.ram[0x48ab:0x48cd])==before
  assert 0<=got*8 and got*8+width<=256
  rows.append({'id':f'B{b:03}-S{int(i):03}','bytes':len(raw),'pixels':width,'left_tile':got,'right_pixel':got*8+width})
report={'source_sha256':hashlib.sha256(source).hexdigest(),'native_executions':len(rows),'routine':'4D:3E00..3E2D','consumer_fragments':['C3:4AFD B015 lookup/selection then4D3E00','C3:4B53 B014 lookup/selection then4D3E00','C0:98AF B014 save-location consumer, not executed here'],'maximum_label_bytes':max(x['bytes'] for x in rows),'maximum_pixels':max(x['pixels'] for x in rows),'cases':rows,'scope':'Exact native centering leaf on newly translated finite labels, no map header draw, save-menu navigation, selector or natural location traversal claim.'};a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS',len(rows),'native banner centering executions')
