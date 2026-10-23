#!/usr/bin/env python3
"""Staged B019 renders through the real FD8B battle banner, not field windows.
The opt-in core redirects a B020 target-name lookup; this is NOT a natural
special attack or a proof that every enemy/event branch has been traversed.
ROMs, cores, states and WRAM stay in private --out. Only reports/crops ship.
"""
import argparse,concurrent.futures,hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from cpu65816_probe import CPU
from french_font import encode_fr
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--standard-core',type=Path,required=True);p.add_argument('--diagnostic-core',type=Path,required=True);p.add_argument('--full-run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--resume-entry',action='store_true',help='Reuse only a verified same-ROM entry state after an interrupted fixture run');p.add_argument('--workers',type=int,default=4);a=p.parse_args();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert a.resume_entry or not a.out.exists();a.out.mkdir(parents=True,exist_ok=a.resume_entry)
assert a.diagnostic_core.is_file()
assert a.standard_core.is_file()
source_commands=ROOT/'verification/reproduction/commands_lot48_natural_combat.json';commands=[]
for row in json.loads(source_commands.read_text()):
 commands.append(row)
 if row.get('screenshot')=='floor2_end_walk79':break
assert commands[-1]['screenshot']=='floor2_end_walk79';commands +=[{'save':'caption_entry'},{'quit':True}]
manifest=a.out/'entry_commands.json';manifest.write_text(json.dumps(commands,indent=2)+'\n');entry=a.out/'entry'
if a.resume_entry:
 assert json.loads((entry/'report.json').read_text())['rom_sha256']==sha(a.rom)
 assert json.loads((entry/'report.json').read_text())['commands_sha256']==sha(manifest)
else:subprocess.run([sys.executable,str(Path(__file__).parent/'run_controller_replay.py'),'--core',str(a.standard_core.resolve()),'--rom',str(a.rom.resolve()),'--full-run',str(a.full_run.resolve()),'--commands',str(manifest.resolve()),'--out',str(entry.resolve())],check=True)
state=entry/'caption_entry.state';rom=a.rom.read_bytes();rows=[x for x in json.loads((ROOT/'traduction/traduction_v55.json').read_text()) if x['lot']=='49' and x['block_id'] in (19,20)];assert len(rows)==235
# FD8B is the ordinary battle banner. The live script emits catalog19 from
# RAM43BB (action label) and catalog20 from the same index slot (target name).
pattern=bytes.fromhex('0e 13 12 bb 43 09 fd 8b 1b 02');offset=rom.find(pattern);assert offset==0x653c1
assert rom[0x30c1e+138*3:0x30c1e+138*3+3]==bytes.fromhex('22 77 c0')
assert rom[0x77af:0x77b7]==bytes.fromhex('da a2 00 20 80 78 64 00')
def render(row):
 out=a.out/row['id'].lower();out.mkdir();c=CPU(rom);c.load_block(row["block_id"]);c.select(row['string_id']);start=c.read(0x8f,3);raw=encode_fr(row['french_in_game']);end=start+len(raw)
 cmds=[{'load':str(state.resolve()),'frames':0},{'buttons':['Up'],'frames':1},{'frames':30},{'buttons':['A'],'frames':1},{'frames':60,'screenshot':'caption'},{'quit':True}]
 env=dict(os.environ,FEOE_TEST_BLOCK=str(row['block_id']),FEOE_TEST_STRING=str(row['string_id']))
 with (out/'console.log').open('w') as log:subprocess.run([sys.executable,str(Path(__file__).parent/'libretro_runner.py'),'--core',str(a.diagnostic_core.resolve()),'--rom',str(a.rom.resolve()),'--out',str(out.resolve())],input=''.join(json.dumps(x)+'\n' for x in cmds),text=True,stdout=log,stderr=subprocess.STDOUT,env=env,check=True)
 log=(out/'console.log').read_text();assert f'FEOE_DIAGNOSTIC block={row["block_id"]}' in log and f'FEOE_DIAGNOSTIC string={row["string_id"]}\n' in log,row['id'];assert f'FEOE_DIAGNOSTIC terminator={end:06x}' in log,(row['id'],hex(end));assert 'reader=c02c6e' in log,row['id']
 return {'id':row['id'],'string_id':row['string_id'],'text':row['french_in_game'],'bytes':len(raw),'native_reader':'C0:2C6E','terminator':f'{end:06x}','capture_sha256':sha(out/'caption.png'),'log_sha256':sha(out/'console.log'),'image':str(out/'caption.png')}
with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:cases=list(pool.map(render,rows))
report={'rom_sha256':sha(a.rom),'standard_core_sha256':sha(a.standard_core),'diagnostic_core_sha256':sha(a.diagnostic_core),'entry_state_sha256':sha(state),'natural_commands_sha256':sha(source_commands),'fixture':'B020 target-name lookup redirected to B019; native FD8B reader, formatting, centering and PPU unchanged.','ordinary_action_producer':{'script_offset':hex(offset),'bytes':pattern.hex(),'selector':'RAM43BB','consumer':'FD8B -> C07722 -> C077AF (X0 copy) -> C07880/C078A1 ->4D2C00 width and C17702 drawing','maximum_banner_tiles':28},'cases':cases,'case_count':len(cases),'visual_review':'pending','all_natural_attack_branches_validated':False};(a.out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS',len(cases),'native battle banner fixtures; visual review pending')
