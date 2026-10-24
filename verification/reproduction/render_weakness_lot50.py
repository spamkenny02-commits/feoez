#!/usr/bin/env python3
"""Targeted FD8B battle-banner fixtures with explicit synthetic four slots.
Not naturally selected View/All actions;no real weakness/event selection proof.
"""
import argparse,concurrent.futures,hashlib,itertools,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'));from french_font import encode_fr
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--core',type=Path,required=True);p.add_argument('--entry-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--workers',type=int,default=4);a=p.parse_args();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not a.out.exists();a.out.mkdir(parents=True);entry=json.loads((a.entry_run/'report.json').read_text());assert entry['rom_sha256']==sha(a.rom) and entry['controller_only'];state=a.entry_run/'caption_entry.state';assert state.is_file();elements=['Physique','Feu','Eau','Vent','Foudre'];slots=[]
for n in range(5):
 for vals in itertools.combinations(elements,n):slots.append(list(vals)+['']*(4-n))
slots += [['','Feu','',''],['','','','Foudre'],['Physique','Foudre','Vent','Eau']];assert len(slots)==34
cases=[]
for s in slots:
 for idx in [8,9]:cases.append(dict(id=f'w{len(cases):02}',block=44,string=idx,slots=s))
for b,i in [(44,1),(44,7),(43,7)]:cases.append(dict(id=f'w{len(cases):02}',block=b,string=i,slots=['']*4))
def one(row):
 out=a.out/row['id'];out.mkdir();env=os.environ.copy()
 for k in list(env):
  if k.startswith(('FEOE_TEST_','FEOE_LOT50_')):env.pop(k)
 env.update(FEOE_TEST_BLOCK=str(row['block']),FEOE_TEST_STRING=str(row['string']))
 for i,s in enumerate(row['slots']):env[f'FEOE_TEST_SLOT{i}_HEX']=encode_fr(s).hex()
 c=[{'load':str(state.resolve()),'frames':0},{'buttons':['Up'],'frames':1},{'frames':30},{'buttons':['A'],'frames':1},{'frames':60,'screenshot':'caption','dump_vram':'caption'},{'quit':True}]
 with(out/'console.log').open('w')as f:subprocess.run([sys.executable,str(Path(__file__).parent/'libretro_runner.py'),'--core',str(a.core.resolve()),'--rom',str(a.rom.resolve()),'--out',str(out.resolve())],input=''.join(json.dumps(x)+'\n'for x in c),text=True,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 log=(out/'console.log').read_text();assert f"FEOE_DIAGNOSTIC block={row['block']}\n"in log and f"FEOE_DIAGNOSTIC string={row['string']}\n"in log and'FEOE_DIAGNOSTIC terminator='in log
 for i,s in enumerate(row['slots']):assert f'synthetic_slot={i} hex={encode_fr(s).hex()}\n'in log
 return dict(row,image=str((out/'caption.png').resolve()),pixels_review='pending')
with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers)as ex:results=list(ex.map(one,cases))
(a.out/'report.json').write_text(json.dumps(dict(rom_sha256=sha(a.rom),core_sha256=sha(a.core),entry_state_sha256=sha(state),cases=results,case_count=len(results),visual_review='pending',scope=__doc__),ensure_ascii=False,indent=2)+'\n');print('PASS71 fresh native banner fixtures;visual review pending')
