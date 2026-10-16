#!/usr/bin/env python3
"""Capture early-game dialogues after holding without input.
Animated cutscenes may continue and remain at different phases.
Loads only states from a fresh scenario run of the exact same ROM/core.
No diagnostic hook, RAM writes, or cross-ROM state reuse.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--core',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);p.add_argument('--full-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
sha=hashlib.sha256(a.rom.read_bytes()).hexdigest();ready=None
for line in (a.full_run/'core_console.log').read_text().splitlines():
 try:r=json.loads(line)
 except ValueError:continue
 if r.get('ready'):ready=r;break
assert ready and ready['source_sha256']==sha,'Scenario must have used this exact ROM'
a.out.mkdir(parents=True,exist_ok=False);commands=[];states=[]
for name in ['story_122','story_167','field_command_b']:
 state=(a.full_run/(name+'.state')).resolve();states.append({'state':name,'sha256':hashlib.sha256(state.read_bytes()).hexdigest()});commands.append({'load':str(state),'frames':1200,'screenshot':name})
commands.append({'quit':True})
with (a.out/'console.log').open('w') as log:
 subprocess.run([sys.executable,str(Path(__file__).with_name('libretro_runner.py')),'--core',str(a.core.resolve()),'--rom',str(a.rom.resolve()),'--out',str(a.out.resolve())],input=''.join(json.dumps(x)+'\n' for x in commands),text=True,stdout=log,stderr=subprocess.STDOUT,check=True)
(a.out/'report.json').write_text(json.dumps({'rom_sha256':sha,'core_sha256':hashlib.sha256(a.core.read_bytes()).hexdigest(),'states':states,'hold_frames':1200,'scope':'No-input holds; animated cutscenes may remain phased. Not a natural playthrough.'},indent=2)+'\n')
print('Three no-input dialogue captures complete')
