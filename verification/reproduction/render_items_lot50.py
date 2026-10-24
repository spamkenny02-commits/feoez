#!/usr/bin/env python3
"""303 independent first-item-DMA fixtures from a fresh same-ROM field state.
Does not claim natural ownership;the actual equipment and full-name fields
remain the ordinary held Katana. Private states/dumps/core are not published.
"""
import argparse,concurrent.futures,hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--core',type=Path,required=True);p.add_argument('--full-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--workers',type=int,default=4);a=p.parse_args();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not a.out.exists();a.out.mkdir(parents=True);rows=json.loads((ROOT/'traduction/item_graphics_lot50_fr.json').read_text());ready=[json.loads(s)for s in(a.full_run/'core_console.log').read_text().splitlines()if s.startswith('{"ready"')];assert ready[0]['source_sha256']==sha(a.rom)
def one(e):
 out=a.out/f"item_{e['index']:03}";out.mkdir();c=[{'load':str((a.full_run/'field_verified.state').resolve()),'frames':60}]
 for b in ['X','Down','A']:c.extend([{'buttons':[b],'frames':12},{'frames':60}])
 c.extend([{'frames':0,'screenshot':'view','dump_vram':'view'},{'quit':True}]);env=os.environ.copy()
 for k in list(env):
  if k.startswith(('FEOE_TEST_','FEOE_LOT50_')):env.pop(k)
 env['FEOE_LOT50_ITEM_INDEX']=str(e['index'])
 with(out/'console.log').open('w')as f:subprocess.run([sys.executable,str(Path(__file__).parent/'libretro_runner.py'),'--core',str(a.core.resolve()),'--rom',str(a.rom.resolve()),'--out',str(out.resolve())],input=''.join(json.dumps(x)+'\n'for x in c),text=True,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 log=(out/'console.log').read_text();assert log.count('FEOE50_ITEM fixture')==1;return dict(index=e['index'],id=e['id'],screenshot=str((out/'view.png').resolve()),vram=str((out/'view.vram').resolve()))
with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers)as ex:results=list(ex.map(one,rows))
(a.out/'report.json').write_text(json.dumps(dict(rom_sha256=sha(a.rom),core_sha256=sha(a.core),source_state_sha256=sha(a.full_run/'field_verified.state'),fixtures=results,cases=len(results),scope=__doc__,visual_review='pending',native_vram_and_pixels='pending'),indent=2)+'\n');print('303 fresh item fixtures complete;VRAM/pixels and review pending')
