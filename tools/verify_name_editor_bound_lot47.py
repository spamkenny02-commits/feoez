#!/usr/bin/env python3
"""Original editor insertion guard and writer, before UI continuation.
Proves a byte-storage bound for initially empty FF names, not input alphabet or
natural keyboard navigation. Every instruction is read from the pinned ROM.
"""
import argparse,json,hashlib
from pathlib import Path
from numeric65816_probe import NumericCPU
class AtContinuation(Exception):pass
class EditorCPU(NumericCPU):
 allowed_ranges=((0xc093b6,0xc093c5),(0xc09423,0xc09439))
 def fetch(self,n=1):
  if self.PC==0xc093c4:raise AtContinuation
  return super().fetch(n)
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.source.read_bytes();sha=hashlib.sha256(r).hexdigest();assert sha=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
assert r[0x93b6:0x93c4]==bytes.fromhex('ae 8f 1d e0 0a 90 02 a2 08 20 23 94 e8 e8')
assert r[0x9423:0x9439]==bytes.fromhex('48 bd 30 1d 85 00 68 9d 30 1d eb 9d 31 1d a5 00 d0 03 9d 32 1d 60')
# Source FF editor entry is empty; pet and wish scripts both use FF.
assert r[0x92e8:0x92eb]==bytes.fromhex('9c 30 1d')
for p0,fragment in [(0x62fc2,'fd 7a ff 05'),(0x618fc,'fd 7a ff 02')]:
 assert bytes.fromhex(fragment) in r[p0-8:p0+10],(hex(p0),fragment)
count=0
for length in range(0,11,2):
 for cursor in range(0,length+1,2):
  for pair in [0x5050,0x209f,0xcece,0x9910]:
   c=EditorCPU(r);c.ram[0x1d2f:0x1d3d]=b'\x55'*14;c.ram[0x1d30:0x1d31+length]=b'\x50'*length+b'\0';c.ram[0x1d8f]=cursor;c.A=pair
   try:c.run(0xc093b6)
   except AtContinuation:pass
   else:raise AssertionError('Did not reach pinned continuation')
   raw=bytes(c.ram[0x1d30:0x1d3b]);assert 0 in raw and raw.index(0)<=10
   assert c.ram[0x1d2f]==0x55 and c.ram[0x1d3b:0x1d3d]==b'\x55'*2
   assert c.X==min(cursor,8)+2 and c.S==0x1ff;count+=1
report={'source_sha256':sha,'native_insertions':count,'guard':'C0:93B6..93C3; cursor>=10 clamps to8 before two-byte write','writer':'C0:9423..9438','initial_empty_entry':'C0:92E8 STZ1D30, FF argument bypasses initial-name copy','static_calls':['C6:2FC2 vicinity FD7AFF05 pet name','C6:18FC vicinity FD7AFF02 Star Festival wish'],'bound_bytes':10,'conservative_pixels':110,'scope':'Inductive insertion invariant from empty FF entry, all valid even cursors and four nonzero glyph pairs. No full keyboard alphabet, deletion, preset entries, event trigger or normal UI navigation claim.'};a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS',count,'original guarded editor insertions')
