#!/usr/bin/env python3
"""Ordinary held-equipment fiche and naturally won consumable target/cancel.
Loads only fresh same-ROM controller states;no diagnostic environment.
No healing effect,cost deduction or unvisited category is claimed.
"""
import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--core',type=Path,required=True);p.add_argument('--full-run',type=Path,required=True);p.add_argument('--natural-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rh=sha(a.rom);ready=[json.loads(s)for s in(a.full_run/'core_console.log').read_text().splitlines()if s.startswith('{"ready"')];assert ready[0]['source_sha256']==rh;nr=json.loads((a.natural_run/'report.json').read_text());assert nr['rom_sha256']==rh and nr['controller_only'];assert not a.out.exists();a.out.mkdir(parents=True);commands=[]
def load(path):assert path.is_file();commands.append(dict(load=str(path.resolve()),frames=0))
def key(b,label):commands.extend([dict(buttons=[b],frames=12),dict(frames=90,screenshot=label,dump_vram=label)])
load(a.full_run/'field_verified.state')
for b,label in [('X','main'),('Down','objects'),('A','inventory'),('A','equipment_selected'),('A','equipment_fiche'),('A','equipment_close')]:key(b,label)
load(a.natural_run/'natural_replay_final.state')
for b,label in [('X','party_main'),('Down','party_objects'),('A','party_inventory'),('A','party_bookmark'),('Down','sandals'),('Right','kusa_selected'),('A','target'),('B','cancel')]:key(b,label)
commands.append(dict(quit=True));env=dict(os.environ)
for k in list(env):
 if k.startswith(('FEOE_TEST_','FEOE_LOT50_')):env.pop(k)
with(a.out/'console.log').open('w')as f:subprocess.run([sys.executable,str(Path(__file__).parent/'libretro_runner.py'),'--core',str(a.core.resolve()),'--rom',str(a.rom.resolve()),'--out',str(a.out.resolve())],input=''.join(json.dumps(c)+'\n'for c in commands),text=True,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
rom=a.rom.read_bytes();checks=[]
contracts=[('equipment_fiche',0x6d2890,4,2,13),('equipment_fiche',0x6d28e0,7,2,3),('equipment_fiche',0x6d2a20,6,2,7),('target',0x6d2800,9,2,3),('target',0x6d2890,4,2,13),('target',0x6d29b0,3,2,7)]
for view,st,n,x,y in contracts:
 v=(a.out/(view+'.vram')).read_bytes();va=0x6f00+st-0x6d2300;assert v[va:va+16*n]==rom[st:st+16*n];t=0xf0+(st-0x6d2300)//16;at=0xb000+y*64+x*2;got=[int.from_bytes(v[at+2*k:at+2*k+2],'little')&1023 for k in range(n)];assert got==list(range(t,t+n));checks.append(dict(view=view,source=hex(st),vram=hex(va),tiles=got,column=x,row=y,exact=True))
(a.out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');(a.out/'report.json').write_text(json.dumps(dict(rom_sha256=rh,core_sha256=sha(a.core),boot_field_state_sha256=sha(a.full_run/'field_verified.state'),natural_field_state_sha256=sha(a.natural_run/'natural_replay_final.state'),controller_only=True,diagnostic_environment_disabled=True,native_vram_tilemap_checks=checks,visual_review='pending',scope=__doc__),indent=2)+'\n');print('PASS ordinary equipment fiche and consumable selector/cancel;6 exact VRAM/tilemap contracts;visual pending')
