#!/usr/bin/env python3
"""Finite one-byte mode catalogs, native copies and static grid bindings.
No natural inventory-selection, gift availability or cursor progression claims.
"""
import argparse,json,hashlib
from pathlib import Path
from cpu65816_probe import CPU
from text65816_probe import TextCPU
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.source.read_bytes();assert hashlib.sha256(r).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e';cases=[];count=0
for block,indexes in [(41,[126,127,128,129,131,132,133,134,136,137,138]),(66,[32,33])]:
 for idx in indexes:
  c=CPU(r);c.load_block(block);c.select(idx);raw=c.string();assert raw in [b'\x08',b'\x0a']
  for slot in range(4):
   t=TextCPU(r);t.load_block(block);t.write(9,idx,1);t.ram[0x32aa:0x332a]=b'\x55'*128;t.run(0xc32aa4,slot);start=0x32aa+32*slot;assert t.ram[start:start+2]==raw+b'\0' and t.ram[0x32aa:start]==b'\x55'*(start-0x32aa) and t.ram[start+2:0x332a]==b'\x55'*(0x332a-start-2);count+=1
  cases.append({'source':f'B{block:03}-S{idx:03}','slot_payload':raw.hex(),'pixel_advance':0,'proof':'Native08/0A mode flags, see text_modes_lot46.json'})
patterns=[bytes.fromhex('88 7e 01 04 03 88 7f 01'),bytes.fromhex('88 80 02 04 03 88 81 02 01 82')];hits=[]
for pat in patterns:
 at=r.find(pat,0x62a51,0x64601);assert at>=0;hits.append({'offset':hex(at),'bytes':pat.hex(),'scope':'Same block41 event region; feeds style slots05/06 before text130'})
# Block66 root bounds select the actual gift-menu event region.
root=int.from_bytes(r[0x57184+3*65:0x57187+3*65],'little')-0xc00000;end=int.from_bytes(r[0x57184+3*66:0x57187+3*66],'little')-0xc00000
# The gift grid uses stacked arguments: common routines 01/02 push a
# style-source index, then the previous value of counter052B, incrementing it.
# Opcode09 selects stacked operands for the following88; the literal1B02
# is skipped by operand setup (C3:03B0), rather than being the chosen text.
assert r[0x7cd91:0x7cd95]==bytes.fromhex('5f 91 cb c7')
table=r[0x7cb91:0x7cbd6]
for idx,ident,offset in [(32,1,0x7cd6f),(33,2,0x7cd7a)]:
 pat=bytes([ident])+int(offset+0xc00000).to_bytes(3,'little');assert pat in table
 routine=bytes([0x0e,idx])+bytes.fromhex('3c 2b 05 0a 09 88 1b 02 00');assert r[offset:offset+len(routine)]==routine
 hits.append({'source':f'B066-S{idx:03}','common_lookup':hex(0xc7cb91),'common_id':ident,'routine':hex(offset+0xc00000),'bytes':routine.hex(),'binding':'Push style text index, post-increment052B, push old counter as slot;09 enables stack operands for88.'})
assert r[0x7cd95:0x7cd9a]==bytes.fromhex('1c 00 20 2b 05')
assert r[0x31446:0x31451]==bytes.fromhex('20 cd 16 a7 2a 85 1e 1a 87 2a 60')
assert r[0x31496:0x3149f]==bytes.fromhex('a5 1e 8d 98 10 9c 99 10 60')
assert r[0x311cc:0x311d2]==bytes.fromhex('a9 81 9d ce 08 60')
for text in [35,36,37]:
 at=r.find(bytes([1,text]),0x7cdb0,0x7ce35);assert at>=0
 hits.append({'visible_grid':f'B066-S{text:03}','text_call':hex(at),'preceding_common_calls':r[at-16:at].hex(),'proof':'Static same-event paths call01 or02 per inventory condition before this grid. Actual availability and selector branches remain untested.'})
a.out.write_text(json.dumps({'source_sha256':hashlib.sha256(r).hexdigest(),'native_copier_executions':count,'mode_catalogs':cases,'static_grid_bindings':hits,'contract':'Slots carry zero-advance native08/0A commands, not quantities or names.','scope':'Finite native leaf copies and static event fragments, not full event interpretation or natural selectors.'},indent=2)+'\n');print('PASS',count,'native style-slot copies andstatic bindings')
