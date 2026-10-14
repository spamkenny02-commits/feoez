#!/usr/bin/env python3
"""Fresh standard-core replay to the known dialogue-entry state, same ROM only."""
import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--core',required=True);p.add_argument('--rom',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
root=Path(__file__).parent;commands=json.loads((root/'scenario.json').read_text())[:431]
for c in commands:
 if 'load' in c:c['load']=c['load'].replace('@RUN_DIR@',str(a.out.resolve()))
commands.append({'save':'dialogue_entry','screenshot':'dialogue_entry'})
with (a.out/'console.log').open('w') as log:
 subprocess.run([sys.executable,str(root/'libretro_runner.py'),'--core',a.core,'--rom',a.rom,'--out',str(a.out)],input=''.join(json.dumps(c)+'\n' for c in commands),text=True,stdout=log,stderr=subprocess.STDOUT,check=True)
print(a.out/'dialogue_entry.state')
