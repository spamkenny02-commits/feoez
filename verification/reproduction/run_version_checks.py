#!/usr/bin/env python3
"""Run storage, boot, navigation, A/B and staged rendering on a single fresh ROM.
Requires locally built standard/diagnostic cores; neither is distributed here.
Refuses existing run directories so evidence cannot mix different ROMs.
"""
import argparse,concurrent.futures,json,re,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--version',required=True);p.add_argument('--tag',default='final');p.add_argument('--source',type=Path,required=True);p.add_argument('--emulator-root',type=Path,required=True);p.add_argument('--render-workers',type=int,choices=range(1,5),default=1);p.add_argument('--compact-render',action='store_true',help='Remove unselected intermediate screenshots after each completed case');p.add_argument('--diagnostic-core',type=Path);p.add_argument('--auto-close-captures',action='store_true');p.add_argument('--build-report',type=Path,help='Explicit report for a checkpoint ROM');a=p.parse_args()
assert re.fullmatch(r'v[0-9]+',a.version) and re.fullmatch(r'[a-z0-9_]+',a.tag)
v=a.version;tag=a.tag;root=Path(__file__).resolve().parent;repo=root.parents[1];em=a.emulator_root.resolve();rom=em/f'fr_{v}.sfc';runs=em/'runs';core=em/'snes9x_libretro_standard.so';diag=a.diagnostic_core.resolve() if a.diagnostic_core else em/'snes9x_libretro_diagnostic.so'
for f in [a.source,rom,core,diag,root/f'cases_{v}.json',root/f'scenario_checks_{v}.json']:assert f.is_file(),f
for name in [f'fr_{v}_{tag}',f'{v}_navigation_{tag}',f'{v}_dialogue_{tag}',f'{v}_scenes_{tag}',f'{v}_check_ab_{tag}']:
 if (runs/name).exists():p.error(f'Run directory already exists: {runs/name}; use a fresh tag')
def run(label,script,*args,stdin=None):
 with (em/f'{v}_{label}_{tag}.log').open('w') as log:
  subprocess.run([sys.executable,str(script),*map(str,args)],cwd=repo,input=stdin,text=True,stdout=log,stderr=subprocess.STDOUT,check=True)
 print(label,'PASS',flush=True)
def scenario():
 run('scenario',root/'run_scenario.py','--core',core,'--rom',rom,'--out',runs/f'fr_{v}_{tag}')
 run('navigation',root/'run_navigation.py','--core',core,'--rom',rom,'--full-run',runs/f'fr_{v}_{tag}','--out',runs/f'{v}_navigation_{tag}')
def dialogue():
 run('state',root/'prepare_dialogue_state.py','--core',core,'--rom',rom,'--out',runs/f'{v}_dialogue_{tag}')
 run('scenes',root/'run_targeted_dialogues.py','--core',diag,'--rom',rom,'--state',runs/f'{v}_dialogue_{tag}/dialogue_entry.state','--out',runs/f'{v}_scenes_{tag}','--cases',root/f'cases_{v}.json','--workers',a.render_workers,*(['--compact'] if a.compact_render else []),*(['--auto-close-captures'] if a.auto_close_captures else []))
def ab():
 commands=json.loads((root/f'scenario_checks_{v}.json').read_text());run('ab',root/'libretro_runner.py','--core',core,'--rom',rom,'--out',runs/f'{v}_check_ab_{tag}',stdin=''.join(json.dumps(x)+'\n' for x in commands))
run('storage',repo/'tools/verify_storage.py',a.source.resolve(),'--version',v.upper(),'--built-rom',rom,'--build-report',a.build_report.resolve() if a.build_report else repo/'verification/build_report.json')
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 futures=[pool.submit(fn) for fn in [scenario,dialogue,ab]]
 for f in concurrent.futures.as_completed(futures):f.result()
