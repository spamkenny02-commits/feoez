#!/usr/bin/env python3
"""Replay only recorded controller commands from a fresh same-ROM field state.
No ROM, CPU, WRAM or state modifications. Private artifacts remain in --out.
"""
import argparse,hashlib,json,subprocess,sys,os
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--core',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);p.add_argument('--full-run',type=Path,required=True);p.add_argument('--commands',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--observe-lookups',action='store_true',help='For the separate read-only lookup trace core; never enables redirection');a=p.parse_args();assert not a.out.exists();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();ready=[]
for line in (a.full_run/'core_console.log').read_text().splitlines():
 try:r=json.loads(line)
 except ValueError:continue
 if r.get('ready'):ready.append(r)
assert ready and ready[0]['source_sha256']==sha(a.rom)
commands=json.loads(a.commands.read_text());assert commands and commands[0].get('load')=='@FULL_RUN_DIR@/field_verified.state'
for cmd in commands:
 if 'load' in cmd:cmd['load']=cmd['load'].replace('@FULL_RUN_DIR@',str(a.full_run.resolve()))
 assert set(cmd)<={'load','frames','buttons','screenshot','save','quit','frame','ram','dump_vram'},cmd
assert not any('FEOE_TEST_' in k for k in os.environ),'Synthetic text redirection must be disabled'
a.out.mkdir(parents=True);env=dict(os.environ)
if a.observe_lookups:env['FEOE_TRACE_LOOKUPS']='1'
with (a.out/'console.log').open('w') as f:subprocess.run([sys.executable,str(Path(__file__).parent/'libretro_runner.py'),'--core',str(a.core.resolve()),'--rom',str(a.rom.resolve()),'--out',str(a.out.resolve())],input=''.join(json.dumps(c)+'\n' for c in commands),text=True,stdout=f,stderr=subprocess.STDOUT,env=env,check=True)
(a.out/'report.json').write_text(json.dumps({'rom_sha256':sha(a.rom),'core_sha256':sha(a.core),'commands_sha256':sha(a.commands),'source_field_state_sha256':sha(a.full_run/'field_verified.state'),'controller_only':True,'observe_only_core':a.observe_lookups,'visual_review':'pending'},indent=2)+'\n');print('PASS controller replay; visual review pending')
