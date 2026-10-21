#!/usr/bin/env python3
"""Resume an interrupted staged-render batch using the exact same ROM/core/state.
Completed cases are retained; unfinished cases run in a fresh isolated directory.
The original manifest is replaced only after all remaining cases pass; its prior
contents and the remaining-case list are kept in the new run directory.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser()
for key in ('existing-results','cases','core','rom','state','out'):p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--workers',type=int,choices=range(1,5),default=4);p.add_argument('--compact',action='store_true');a=p.parse_args()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=a.existing_results.read_text();old=json.loads(original);cases=json.loads(a.cases.read_text())
assert old['rom_sha256']==sha(a.rom) and old['diagnostic_core_sha256']==sha(a.core) and old['state_sha256']==sha(a.state)
assert not a.out.exists(),'Use a fresh output directory'
expected={name:f'B{bid:03}-S{idx:03}' for bid,idx,name in cases};done={}
for c in old['cases']:
 assert c['case'] in expected and c['entry']==expected[c['case']] and c['case'] not in done
 assert c['native_read_complete'] and c['observed_terminators']==[c['expected_terminator']]
 assert c['images'] and all(Path(x).is_file() for x in c['images'])
 done[c['case']]=c
remaining=[c for c in cases if c[2] not in done];assert remaining,'No unfinished cases'
casefile=a.out.with_suffix('.remaining_cases.json');assert not casefile.exists();casefile.write_text(json.dumps(remaining,indent=2)+'\n')
print(json.dumps({'retained_cases':len(done),'remaining_cases':len(remaining)}),flush=True)
subprocess.run([sys.executable,str(Path(__file__).with_name('run_targeted_dialogues.py')),'--cases',str(casefile.resolve()),'--core',str(a.core.resolve()),'--rom',str(a.rom.resolve()),'--state',str(a.state.resolve()),'--out',str(a.out.resolve()),'--workers',str(a.workers),*(['--compact'] if a.compact else [])],check=True)
new=json.loads((a.out/'results.json').read_text())
for k in ('rom_sha256','diagnostic_core_sha256','state_sha256'):assert new[k]==old[k]
for c in new['cases']:
 assert c['native_read_complete'] and c['case'] not in done and c['entry']==expected[c['case']]
 done[c['case']]=c
assert len(done)==len(cases)
merged={**old,'cases':[done[name] for _,_,name in cases],'resumptions':old.get('resumptions',[])+[{'retained_cases':len(old['cases']),'new_cases':len(new['cases']),'directory':str(a.out.resolve()),'workers':a.workers,'same_rom_core_state':True}]}
(a.out/'previous_results.json').write_text(original)
a.existing_results.write_text(json.dumps(merged,ensure_ascii=False,indent=2)+'\n')
print('All staged rendering cases PASS; original manifest merged',flush=True)
