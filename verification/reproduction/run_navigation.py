#!/usr/bin/env python3
"""Menu/map replay with 12-frame inputs, using a same-ROM field state."""
import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--core',required=True);p.add_argument('--rom',required=True)
p.add_argument('--full-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
root=Path(__file__).parent;out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
commands=json.loads((root/'scenario_navigation.json').read_text())
for c in commands:
    if 'load' in c:c['load']=c['load'].replace('@FULL_RUN_DIR@',str(a.full_run.resolve()))
with (out/'console.log').open('w') as log:
    subprocess.run([sys.executable,str(root/'libretro_runner.py'),'--core',a.core,'--rom',a.rom,'--out',str(out)],
                   input=''.join(json.dumps(c)+'\n' for c in commands),text=True,stdout=log,stderr=subprocess.STDOUT,check=True)
print(out/'history.json')
