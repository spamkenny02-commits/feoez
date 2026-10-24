#!/usr/bin/env python3
"""Native shop-name DMA fixtures in complete shop windows;not natural visits.
Uses an ordinary NPC continuation redirected to the existing pharmacist shop,
then explicitly selects one allocated name index at4FF8C0. Stock/ownership stay
those of the original fixture shop. No transactions are performed.
"""
import argparse,concurrent.futures,hashlib,json,os,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--core',type=Path,required=True);p.add_argument('--full-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest();assert not a.out.exists();a.out.mkdir(parents=True);ready=[json.loads(s)for s in(a.full_run/'core_console.log').read_text().splitlines()if s.startswith('{"ready"')];assert ready[0]['source_sha256']==sha(a.rom)
commands=[dict(load=str((a.full_run/'field_verified.state').resolve()),frames=0)]
for b,n in [('Up',16),('Down',1),('Right',16),('A',1)]:commands.append(dict(buttons=[b],frames=n))
commands.append(dict(frames=120))
for b in ['A','A']:commands.extend([dict(buttons=[b],frames=1),dict(frames=120)])
commands.extend([dict(frames=0,screenshot='main',dump_vram='main'),dict(quit=True)])
def one(i):
 out=a.out/f'name_{i:02}';out.mkdir();env=dict(os.environ)
 for k in list(env):
  if k.startswith(('FEOE_TEST_','FEOE_LOT50_')):env.pop(k)
 env.update(FEOE_LOT50_SHOP_ENTRY='1',FEOE_LOT50_SHOP_NAME_INDEX=str(i))
 with(out/'console.log').open('w')as f:subprocess.run([sys.executable,str(Path(__file__).parent/'libretro_runner.py'),'--core',str(a.core.resolve()),'--rom',str(a.rom.resolve()),'--out',str(out.resolve())],input=''.join(json.dumps(c)+'\n'for c in commands),text=True,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 log=(out/'console.log').read_text();assert 'redirected_thread_count=1' in log and f'target={i}\n'in log
 return dict(name_index=i,image=str((out/'main.png').resolve()),vram=str((out/'main.vram').resolve()),fixture=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:cases=list(pool.map(one,range(32)))
(a.out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');(a.out/'report.json').write_text(json.dumps(dict(rom_sha256=sha(a.rom),core_sha256=sha(a.core),field_state_sha256=sha(a.full_run/'field_verified.state'),cases=cases,visual_review='pending',scope=__doc__),indent=2)+'\n');print('PASS32 fresh shop-name fixtures;visual/VRAM review pending')
