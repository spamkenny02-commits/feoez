#!/usr/bin/env python3
import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--core',required=True);p.add_argument('--rom',required=True);p.add_argument('--out',required=True);a=p.parse_args()
root=Path(__file__).parent;out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
commands=json.loads((root/'scenario.json').read_text())
for c in commands:
 if 'load' in c:c['load']=c['load'].replace('@RUN_DIR@',str(out))
payload=''.join(json.dumps(c)+'\n' for c in commands)
with (out/'core_console.log').open('w') as log:
 subprocess.run([sys.executable,str(root/'libretro_runner.py'),'--core',a.core,'--rom',a.rom,'--out',str(out)],input=payload,text=True,stdout=log,stderr=subprocess.STDOUT,check=True)
print(out/'history.json')
