#!/usr/bin/env python3
"""Run after run_scenario.py, using states made by that same ROM/core."""
import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--core',required=True);p.add_argument('--rom',required=True)
p.add_argument('--full-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
p.add_argument('--mode',choices=['dialogues','navigation'],default='dialogues');a=p.parse_args()
out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
if a.mode=='dialogues':
    commands=[{'load':str((a.full_run/'story_122.state').resolve()),'frame':50721,'frames':120}]
    for i in range(80):commands.extend([{'frames':1,'buttons':['A']},{'frames':240,'screenshot':f'dialogue_{i:02}','ram':{'offset':'0x10C5','length':3}}])
else:
    commands=[{'load':str((a.full_run/'field_verified.state').resolve()),'frame':64342,'frames':5},
              {'frames':1,'buttons':['X']},{'frames':180,'screenshot':'main_menu'},
              {'frames':1,'buttons':['Right']},{'frames':10},{'frames':1,'buttons':['Down']},{'frames':10},
              {'frames':1,'buttons':['A']},{'frames':180,'screenshot':'settings'},
              {'frames':1,'buttons':['B']},{'frames':30},{'frames':1,'buttons':['B']},{'frames':60},
              {'frames':1,'buttons':['Select']},{'frames':240,'screenshot':'region_map'},
              {'frames':1,'buttons':['A']},{'frames':180,'screenshot':'village_return'}]
commands.append({'quit':True})
with (out/'console.log').open('w') as log:
    subprocess.run([sys.executable,str(Path(__file__).with_name('libretro_runner.py')),
                    '--core',a.core,'--rom',a.rom,'--out',str(out)],
                   input=''.join(json.dumps(c)+'\n' for c in commands),text=True,
                   stdout=log,stderr=subprocess.STDOUT,check=True)
print(out/'history.json')
