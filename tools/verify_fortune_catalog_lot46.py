#!/usr/bin/env python3
"""Prove the finite fortune text-slot catalog with native copier execution.
Static bytecode references are checked separately from restricted CPU execution.
No claim of naturally reaching the fortune-telling event or of PPU rendering.
"""
import argparse,hashlib,json
from pathlib import Path
from text65816_probe import TextCPU
from cpu65816_probe import CPU
from french_font import encode_fr,visible_width,patch_font
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--candidate',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[1];source=a.source.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(source)=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
lot=json.loads((root/'traduction/lot46_fr.json').read_text());font=patch_font(source)[0];cases=[]
for idx in range(108,120):
 offset=0x616c6+6*(idx-108);code=source[offset:offset+6]
 assert code[:5]==bytes([0x89,40,idx,1,4]);assert offset+6+code[5]==0x6170e
 assert source[0x6170e:0x61710]==bytes([1,120])
 assert int.from_bytes(source[0x3048f+2*(0x89-1):0x30491+2*(0x89-1)],'little')==0x1dbb
 assert source[0x31003+0x89-1]==3
 text=lot['40'][str(idx)];fr=encode_fr(text);assert 0<len(fr)<32 and all(0x10<=v<0xe0 for v in fr)
 entry={'id':f'B040-S{idx:03}','french':text,'encoded_bytes':len(fr),'pixels':visible_width(text,font),'event_offset':hex(offset),'bytecode':code.hex(),'branch_destination':'0x6170e','target':'B040-S120','slot':1}
 for name,rom in [('source',source)]+([('candidate',a.candidate.read_bytes())] if a.candidate else []):
  read=CPU(rom);read.load_block(40);read.select(idx);expected=read.string()+b'\0'
  if name=='candidate':assert expected==fr+b'\0'
  c=TextCPU(rom);c.load_block(40);c.write(9,idx,1);c.X=17;c.Y=29;c.ram[0x32aa:0x332a]=b'\x55'*128
  c.run(0xc32aa4,1,limit=500000);start=0x32ca
  assert c.ram[start:start+len(expected)]==expected
  assert c.ram[0x32aa:start]==b'\x55'*32 and c.ram[start+len(expected):0x332a]==b'\x55'*(0x332a-start-len(expected))
  assert c.X==17 and c.Y==29
  entry[name+'_copier_passed']=True
 cases.append(entry)
report={'source_sha256':sha(source),'candidate_sha256':sha(a.candidate.read_bytes()) if a.candidate else None,'catalog_size':12,'target':'B040-S120','command':'05','slot':1,'native_producer':'C3:2AA4 with block/string lookup and C0:2C6E raw reader','reservation_pixels':max(e['pixels'] for e in cases),'cases':cases,'limits':['Static references and restricted copier execution, not a natural event or PPU proof.','SNES multiplication result modeled without timing.','Only these twelve fortune labels; no general name/item slot bound.']}
a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS twelve fortune references/copiers; width',report['reservation_pixels'])
