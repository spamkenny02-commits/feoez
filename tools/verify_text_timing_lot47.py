#!/usr/bin/env python3
"""Original text-speed and delay leafs. No audio/frame synchronization claim."""
import argparse,json,hashlib
from pathlib import Path
from numeric65816_probe import NumericCPU
class TimingCPU(NumericCPU):
 allowed_ranges=((0xc32e99,0xc32ebf),)
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.source.read_bytes();assert hashlib.sha256(r).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e';results=[]
for command,address,step in [(0x0b,0xc32e99,1),(0x0c,0xc32e9d,-1)]:
 assert int.from_bytes(r[0x32e01+2*command:0x32e03+2*command],'little')|0xc30000==address
 for thread in [0,3,17]:
  for speed in range(11):
   c=TimingCPU(r);c.write(0x62,thread,2);c.ram[0x762+thread]=speed;before=c.ram[:];c.run(address);assert c.ram[0x762+thread]==min(10,max(0,speed+step));changes=[i for i,(a0,b0) in enumerate(zip(before,c.ram)) if a0!=b0];assert set(changes)<={0,0x762+thread};results.append({'command':f'{command:02X}','thread':thread,'input_speed':speed,'output_speed':c.ram[0x762+thread]})
for thread in [0,3,17]:
 c=TimingCPU(r);c.write(0x62,thread,2);c.Y=17;c.run(0xc32eb3);assert c.ram[0x65e+thread]==16 and c.Y==0
out={'source_sha256':hashlib.sha256(r).hexdigest(),'speed_handler_executions':66,'delay_handler_executions':3,'commands':{'0B':'speed index +1, saturating at10','0C':'speed index -1, saturating at0','0D':'write16 to per-thread delay counter and setY0'},'speed_case_results':results,'scope':'Native handler register/RAM effects only. Delay-counter writes do not establish audio tempo, synchronization, natural karaoke triggers or full frame timing. No horizontal cursor writes in0B/0C.'};a.out.write_text(json.dumps(out,indent=2)+'\n');print('PASS 66 speed-handler executions and3 delay-handler executions')
