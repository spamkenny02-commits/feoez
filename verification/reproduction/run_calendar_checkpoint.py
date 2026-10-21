#!/usr/bin/env python3
"""Open the Almanac by controller input from a fresh same-ROM field replay."""
import argparse,json,hashlib,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--core',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);p.add_argument('--full-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();repo=Path(__file__).resolve().parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not a.out.exists(),a.out
ready=None
for line in (a.full_run/'core_console.log').read_text().splitlines():
 try:r=json.loads(line)
 except ValueError:continue
 if r.get('ready'):ready=r;break
assert ready and ready['source_sha256']==sha(a.rom),'Field replay belongs to another ROM'
state=a.full_run/'field_verified.state';assert state.is_file()
commands=json.loads((repo/'verification/calendar_lot46_checkpoint/commands.json').read_text());commands[0]['load']=str(state.resolve());a.out.mkdir(parents=True)
with (a.out/'console.log').open('w') as log:
 subprocess.run([sys.executable,str(Path(__file__).parent/'libretro_runner.py'),'--core',str(a.core.resolve()),'--rom',str(a.rom.resolve()),'--out',str(a.out.resolve())],input=''.join(json.dumps(c)+'\n' for c in commands),text=True,cwd=repo,stdout=log,stderr=subprocess.STDOUT,check=True)
(a.out/'report.json').write_text(json.dumps({'rom_sha256':sha(a.rom),'core_sha256':sha(a.core),'field_state_sha256':sha(state),'scope':'Controller navigation to the real Almanac from a fresh same-ROM replay; no synthetic text-slot fixture.','visual_review':'pending','expected_replay_date':'1995-12-22','image':'almanac_open.png'},indent=2)+'\n');print('PASS controller sequence; visual review pending')
