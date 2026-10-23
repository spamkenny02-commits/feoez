#!/usr/bin/env python3
"""One NPC continuation redirected to real medicine FD15/FD80. Not natural visit."""
import argparse,json,hashlib,os,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--core',type=Path,required=True);p.add_argument('--full-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not a.out.exists();a.out.mkdir(parents=True)
ready=[json.loads(s)for s in(a.full_run/'core_console.log').read_text().splitlines()if s.startswith('{"ready"')];assert ready[0]['source_sha256']==sha(a.rom)
c=[{'load':str((a.full_run/'field_verified.state').resolve()),'frames':0}]
for b,n in [('Up',16),('Down',1),('Right',16),('A',1)]:c.append({'buttons':[b],'frames':n})
c.append({'frames':120,'screenshot':'greeting'})
for b,label in [('A','choice'),('A','main'),('A','buy'),('B','back'),('Down','sell_choice'),('A','sell'),('B','cancel_sell'),('B','leave')]:c.extend([{'buttons':[b],'frames':1},{'frames':120,'screenshot':label,'dump_vram':label}])
c.append({'quit':True});env=os.environ.copy()
for k in list(env):
 if k.startswith(('FEOE_TEST_','FEOE_LOT50_')):env.pop(k)
env.update(FEOE_LOT50_OBSERVE='1',FEOE_LOT50_SHOP_ENTRY='1')
with(a.out/'console.log').open('w')as f:subprocess.run([sys.executable,str(Path(__file__).parent/'libretro_runner.py'),'--core',str(a.core.resolve()),'--rom',str(a.rom.resolve()),'--out',str(a.out.resolve())],input=''.join(json.dumps(x)+'\n'for x in c),text=True,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
assert 'redirected_thread_count=1' in(a.out/'console.log').read_text();(a.out/'commands.json').write_text(json.dumps(c,indent=2)+'\n');(a.out/'report.json').write_text(json.dumps(dict(rom_sha256=sha(a.rom),core_sha256=sha(a.core),state_sha256=sha(a.full_run/'field_verified.state'),fixture=True,scope='Not natural shop visit or successful transaction proof',visual_review='pending',vram_validation='pending'),indent=2)+'\n');print('Shop fixture complete;review pending')
