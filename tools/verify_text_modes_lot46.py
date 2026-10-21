#!/usr/bin/env python3
"""Execute shared native low-command mode handlers; no PPU claims."""
import argparse,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.source.read_bytes()
assert hashlib.sha256(r).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
results=[]
for cmd,mode in [(8,0),(9,4),(10,8)]:
 addr=int.from_bytes(r[0x32e01+2*cmd:0x32e03+2*cmd],'little')+0x30000
 for original in range(256):
  mem={0x1c94:original};pc=addr;A=0;trace=[];writes=[]
  for _ in range(16):
   trace.append(pc+0xc00000);op=r[pc];pc+=1
   if op==0xa9:A=r[pc];pc+=1
   elif op==0x80:d=r[pc];pc+=1;pc+=d if d<128 else d-256
   elif op==0x0a:A=(A*2)&255
   elif op==0x85:mem[r[pc]]=A;writes.append(r[pc]);pc+=1
   elif op==0xad:A=mem[int.from_bytes(r[pc:pc+2],'little')];pc+=2
   elif op==0x29:A&=r[pc];pc+=1
   elif op==0x05:A|=mem[r[pc]];pc+=1
   elif op==0x8d:at=int.from_bytes(r[pc:pc+2],'little');pc+=2;mem[at]=A;writes.append(at)
   elif op==0x60:break
   else:raise AssertionError((hex(pc-1),hex(op)))
  else:raise AssertionError('budget')
  assert mem[0x1c94]==((original&0xf3)|mode) and writes==[0,0x1c94]
 results.append({'command':f'{cmd:02X}','handler':hex(addr+0xc00000),'mode_bits':mode,'original_values_tested':256,'writes':['000000','001c94'],'cursor_or_slot_writes':False})
a.out.write_text(json.dumps({'source_sha256':hashlib.sha256(r).hexdigest(),'handlers':results,'scope':'Native mode flag writes only; no horizontal cursor writes. Does not prove music sync, natural events, palette or graphic meaning.','rendering_required':True},indent=2)+'\n');print('PASS 768 native mode-handler executions')
