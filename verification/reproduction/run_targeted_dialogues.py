#!/usr/bin/env python3
"""Screen tests using the unchanged ROM and a diagnostic core, not normal progression.
Requires same-ROM dialogue_entry.state from a fresh standard-core replay.
Redirects a single existing dialogue call through native block lookup/selection.
Checks that the native reader reaches the exact target terminator; captures every page step.
"""
import argparse,json,subprocess,sys,os,hashlib,re,concurrent.futures
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--cases',type=Path);p.add_argument('--core',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);p.add_argument('--state',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--workers',type=int,choices=range(1,5),default=1);p.add_argument('--compact',action='store_true',help='Retain only the last screenshot of each page after a case passes');a=p.parse_args()
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'tools'))
from cpu65816_probe import CPU
rom=a.rom.read_bytes();cases=[(136,10,'pierre_grue'),(138,7,'lettre_puits'),(139,37,'remise_20'),(141,1,'omine_poche'),(141,12,'omine_sauvetage'),(140,3,'sara_accueil'),(140,8,'sara_nom'),(140,17,'tenjin_rejoint'),(140,35,'parchemins'),(140,42,'tenjin_presentation'),(143,1,'statue_sara'),(146,1,'statue_alias')]
if a.cases:cases=json.loads(a.cases.read_text())
assert all(1<=b<=253 and 1<=i<=255 and re.fullmatch(r'[a-z0-9_]+',n) for b,i,n in cases)
a.out.mkdir(parents=True,exist_ok=True);results=[]
def run_case(case):
 bid,idx,name=case
 cpu=CPU(rom);cpu.load_block(bid);start=cpu.select(idx);raw=cpu.string();expected_end=start+len(raw)
 out=a.out/name;out.mkdir(exist_ok=True);env=dict(os.environ,FEOE_TEST_BLOCK=str(bid),FEOE_TEST_STRING=str(idx));proc=subprocess.Popen([sys.executable,str(Path(__file__).parent/'libretro_runner.py'),'--core',str(a.core.resolve()),'--rom',str(a.rom.resolve()),'--out',str(out.resolve()),'--history-every','50'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,env=env,bufsize=1)
 log=[];terminators=[]
 def send(cmd):
  proc.stdin.write(json.dumps(cmd)+'\n');proc.stdin.flush()
  while True:
   line=proc.stdout.readline()
   if not line:raise RuntimeError('Runner stopped: '+''.join(log[-5:]))
   log.append(line)
   for m in re.finditer(r'FEOE_DIAGNOSTIC terminator=([0-9a-f]+)',line):terminators.append(int(m[1],16))
   try:r=json.loads(line)
   except ValueError:continue
   if 'frame' in r:return r
 send({'load':str(a.state.resolve()),'frames':1})
 send({'frames':1,'buttons':['A']})
 frames=[]
 cursor=start
 for n in range(32):
  elapsed=0;tick=0
  while elapsed<1200:
   step=1 if expected_end-100<=cursor<=expected_end else 30
   response=send({'frames':step,'screenshot':f'page_{n:02}_{tick:04}','ram':{'offset':'0x8f','length':3}})
   frames.append(response);cursor=int.from_bytes(bytes.fromhex(response['ram_hex']),'little');elapsed+=step;tick+=1
   if terminators:break
  if terminators:break
  send({'frames':1,'buttons':['A']})
 send({'quit':True});proc.stdin.close();proc.wait(timeout=10);(out/'console.log').write_text(''.join(log))
 passed=terminators==[expected_end];result={'entry':f'B{bid:03}-S{idx:03}','case':name,'expected_terminator':hex(expected_end),'observed_terminators':[hex(x) for x in terminators],'native_read_complete':passed,'captures':len(frames),'visual_review':'pending','images':[r['image']['path'] for r in frames]}
 if not passed:raise AssertionError(result)
 if a.compact:
  # Exactly the same per-page selection used by collect_evidence.py.
  last={}
  for filename in result['images']:last[Path(filename).stem.split('_')[1]]=filename
  keep=set(last.values())
  for filename in result['images']:
   if filename not in keep:Path(filename).unlink()
  result['images']=list(last.values());result['intermediate_frames_removed']=len(frames)-len(keep)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
 for result in pool.map(run_case,cases):
  results.append(result)
  (a.out/'results.json').write_text(json.dumps({'workers':a.workers,'rom_sha256':hashlib.sha256(rom).hexdigest(),'diagnostic_core_sha256':hashlib.sha256(a.core.read_bytes()).hexdigest(),'state_sha256':hashlib.sha256(a.state.read_bytes()).hexdigest(),'scope':'Staged native rendering, pagination and complete read; not event progression, NPC placement or rewards.','cases':results},ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['entry','native_read_complete','captures']}),flush=True)
