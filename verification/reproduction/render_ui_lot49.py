#!/usr/bin/env python3
"""Fresh controller-only menu views plus opt-in learned-scroll grid fixture."""
import argparse,subprocess,os,json,hashlib,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--core',type=Path,required=True);p.add_argument('--grid-core',type=Path,required=True);p.add_argument('--state',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();a.out.mkdir(parents=True);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();cases={'main':[],'scrolls':['A','A'],'settings':['Right','Down','A'],'inventory':['Down','A'],'inventory_actions':['Down','A','A'],'status':['Down','Down','Down','A','A'],'equip':['Down','Down','A','A'],'clock':['Right','Down','Down','Down','A'],'strategy':['Right','A'],'actor':['Right','A','A'],'guard_tactic':['Right','A','A','A','A','Down','Down','Right','A'],'attack_tactic':['Right','A','A','A','A','A']};reports=[]
for name,buttons in list(cases.items())+[(f'grid_{i}',['A','A']+['Down']*i) for i in (0,3,6)]:
 out=a.out/name;out.mkdir();grid=name.startswith('grid');core=a.grid_core if grid else a.core;env=dict(os.environ)
 if grid:env['FEOE_LOT49_SCROLL_GRID']='1'
 cmds=[{'load':str(a.state.resolve()),'frames':60},{'buttons':['X'],'frames':12},{'frames':80}]
 for key in buttons:cmds +=[{'buttons':[key],'frames':12},{'frames':60}]
 cmds +=[{'screenshot':'view'},{'quit':True}]
 with (out/'console.log').open('w') as f:subprocess.run([sys.executable,str(Path(__file__).parent/'libretro_runner.py'),'--core',str(core.resolve()),'--rom',str(a.rom.resolve()),'--out',str(out.resolve())],input=''.join(json.dumps(x)+'\n' for x in cmds),text=True,stdout=f,stderr=subprocess.STDOUT,env=env,check=True)
 if grid:assert 'synthetic_learned_ids=36' in (out/'console.log').read_text()
 reports.append({'name':name,'image':str(out/'view.png'),'capture_sha256':sha(out/'view.png'),'core_sha256':sha(core),'fixture':grid})
(a.out/'report.json').write_text(json.dumps({'rom_sha256':sha(a.rom),'state_sha256':sha(a.state),'cases':reports,'visual_review':'pending','scope':'12 controller menu paths;3 learned-scroll synthetic fixtures. No all-branch proof.'},indent=2)+'\n');print('PASS15 UI captures; review pending')
