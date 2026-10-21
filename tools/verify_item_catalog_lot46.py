#!/usr/bin/env python3
"""Check finite item/equipment name catalogs through the native slot copier.
All four slots, exact NUL termination and neighbor canaries. The restricted
CPU does not prove natural acquisition, event branches or IO timing.
"""
import argparse,hashlib,json
from pathlib import Path
from cpu65816_probe import CPU
from text65816_probe import TextCPU
from french_font import encode_fr,visible_width
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--candidate',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();root=Path(__file__).resolve().parents[1];source=a.source.read_bytes();assert hashlib.sha256(source).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
lot=json.loads((root/'traduction/lot46_fr.json').read_text());cases=[];executions=0
for b in (2,3):
 for i,t in lot[str(b)].items():
  idx=int(i);fr=encode_fr(t);assert 0<len(fr)<=31,(b,i,len(fr))
  assert all(0x10<=v<0xe0 and not 0x21<=v<=0x2a for v in fr),(b,i,'control or remapped digit in translated label')
  entry={'id':f'B{b:03}-S{idx:03}','encoded_bytes':len(fr),'french':t,'pixels':visible_width(t,source)}
  for kind,rom in [('source',source)]+([('candidate',a.candidate.read_bytes())] if a.candidate else []):
   reader=CPU(rom);reader.load_block(b);reader.select(idx);raw=reader.string();assert len(raw)<=31
   if kind=='candidate':assert raw==fr
   for slot in range(4):
    c=TextCPU(rom);c.load_block(b);c.write(9,idx,1);c.X=17;c.Y=29;c.ram[0x32aa:0x332a]=b'\x55'*128;c.run(0xc32aa4,slot,limit=500000);start=0x32aa+32*slot
    assert c.ram[start:start+len(raw)+1]==raw+b'\0'
    assert c.ram[0x32aa:start]==b'\x55'*(start-0x32aa) and c.ram[start+len(raw)+1:0x332a]==b'\x55'*(0x332a-start-len(raw)-1)
    assert (c.X,c.Y)==(17,29);executions+=1
   entry[kind+'_four_slots_passed']=True
  cases.append(entry)
report={'source_sha256':hashlib.sha256(source).hexdigest(),'candidate_sha256':hashlib.sha256(a.candidate.read_bytes()).hexdigest() if a.candidate else None,'catalog_occurrences':len(cases),'distinct_new_catalog_sources':len(cases)-1,'aliases':{'B002-S074':'B002-S073'},'maximum_encoded_bytes':max(c['encoded_bytes'] for c in cases),'maximum_pixels':max(c['pixels'] for c in cases),'copier_executions':executions,'cases':cases,'scope':'Finite catalog slot-copy bounds and encoding only. No claim of natural item acquisition, menu layout, all-item coverage or event binding. No numeric 56px bound reused for names.'}
a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS',executions,'slot copies,',len(cases),'occurrences,',len(cases)-1,'distinct labels')
