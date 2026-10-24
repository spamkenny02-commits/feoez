#!/usr/bin/env python3
"""Compare fresh exact-ROM controller runs;does not mark visual review."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops
p=argparse.ArgumentParser();p.add_argument('--candidate',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--runs',type=Path,required=True);p.add_argument('--candidate-prefix',required=True);p.add_argument('--baseline-prefix',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rh=sha(a.candidate);bh=sha(a.baseline);groups={}
for name in ['boot','ab','navigation','natural']:
 new=a.runs/f'{a.candidate_prefix}_{name}';old=a.runs/f'{a.baseline_prefix}_{name}';log='core_console.log'if name=='boot'else'console.log'
 for root,h in [(new,rh),(old,bh)]:
  ready=[json.loads(s)for s in(root/log).read_text().splitlines()if s.startswith('{"ready"')];assert ready[0]['source_sha256']==h
 ns={f.name for f in new.glob('*.png')};bs={f.name for f in old.glob('*.png')};assert ns==bs and ns,(name,ns^bs);rows=[]
 for fn in sorted(ns):
  n=Image.open(new/fn).convert('RGB');b=Image.open(old/fn).convert('RGB');assert n.size==b.size==(256,224);box=ImageChops.difference(n,b).getbbox();rows.append(dict(file=fn,identical=box is None,difference_bbox=box,candidate_pixels_sha256=hashlib.sha256(n.tobytes()).hexdigest(),baseline_pixels_sha256=hashlib.sha256(b.tobytes()).hexdigest()))
 groups[name]=dict(captures=len(rows),identical=sum(x['identical']for x in rows),comparisons=rows)
a.out.write_text(json.dumps(dict(rom_sha256=rh,baseline_sha256=bh,groups=groups,visual_review='pending',scope=__doc__),indent=2)+'\n');print({k:(v['captures'],v['identical'])for k,v in groups.items()})
