#!/usr/bin/env python3
"""Regression check for long native grouped-string scans in the English source."""
import argparse,hashlib,json
from pathlib import Path
from cpu65816_probe import CPU,ProbeError
from pointers import analyze
from relocate import position
p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
rom=a.rom.read_bytes();assert hashlib.sha256(rom).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
b=next(b for b in analyze(rom)['blocks'] if 221 in b['block_ids']);raw=rom[int(b['offset'],16):int(b['end_exclusive'],16)];rr=[int(x,16) for x in b['relative_offsets']]
c=CPU(rom);c.load_block(221)
try:c.select(11,limit=100000)
except ProbeError as e:assert str(e)=='Instruction budget exceeded'
else:raise AssertionError('Expected the old budget to reject this known long source scan')
checks=[]
for idx in [11,12,13,14,15,55]:
 c=CPU(rom);c.load_block(221);n=len(c.trace);cursor=c.select(idx);steps=len(c.trace)-n;s,e=position(raw,rr,idx)
 assert c.string()==raw[s:e]
 checks.append({'entry':f'B221-S{idx:03}','selection_instructions':steps,'exact_source_bytes_read':True,'cursor':hex(cursor)})
a.out.write_text(json.dumps({'selection_instruction_budget':500000,'old_100000_budget_rejection_confirmed':True,'passed':len(checks),'checks':checks,'scope':'Restricted native reader probe only; no game-engine changes.'},indent=2)+'\n');print('Six original-source selection cases PASS')
