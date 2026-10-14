#!/usr/bin/env python3
"""Controller-driven intro replay from a same-ROM state; observe raw cursor."""
import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--core',required=True);p.add_argument('--rom',required=True)
p.add_argument('--full-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
commands=[{'load':str((a.full_run/'story_12.state').resolve()),'frame':32945,'frames':5}]
for i in range(100):commands.extend([{'frames':1,'buttons':['A']},
                                  {'frames':240,'screenshot':f'intro_{i:02}','ram':{'offset':'0x8F','length':3}},
                                  {'frames':0,'ram':{'offset':'0x10C5','length':3}}])
commands.append({'quit':True})
with (out/'console.log').open('w') as log:
    subprocess.run([sys.executable,str(Path(__file__).with_name('libretro_runner.py')),
                    '--core',a.core,'--rom',a.rom,'--out',str(out)],
                   input=''.join(json.dumps(c)+'\n' for c in commands),text=True,
                   stdout=log,stderr=subprocess.STDOUT,check=True)
print(out/'history.json')
