#!/usr/bin/env python3
"""Load the same natural in-game question and test both controller choices."""
import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--core',required=True);p.add_argument('--rom',required=True)
p.add_argument('--walk-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);commands=[]
for name in ['oui','non']:
    commands.append({'load':str((a.walk_run/'choice_ready.state').resolve()),'frame':65960,'frames':5})
    if name=='non':commands.extend([{'frames':1,'buttons':['Right']},{'frames':10}])
    commands.extend([{'frames':1,'buttons':['A']},{'frames':360,'screenshot':'answer_'+name,'ram':{'offset':'0x10C5','length':3}}])
commands.append({'quit':True})
with (out/'console.log').open('w') as log:
    subprocess.run([sys.executable,str(Path(__file__).with_name('libretro_runner.py')),
                    '--core',a.core,'--rom',a.rom,'--out',str(out)],
                   input=''.join(json.dumps(c)+'\n' for c in commands),text=True,
                   stdout=log,stderr=subprocess.STDOUT,check=True)
print(out/'history.json')
