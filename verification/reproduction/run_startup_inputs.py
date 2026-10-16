#!/usr/bin/env python3
"""Natural controller-only startup replay and birthday/RTC editing branches.
Builds all states with the exact ROM under test; never changes RAM or ROM.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--core',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False);root=Path(__file__).parent
commands=[];keep={'boot','after_reset_a','check_a','check_b','date_setup','date_confirmed','clock_start','birthday_question','birth_step1','birth_step2','birth_step3'}
for original in json.loads((root/'scenario.json').read_text()):
 c=dict(original)
 if 'load' in c:c['load']=c['load'].replace('@RUN_DIR@',str(a.out.resolve()))
 name=c.get('screenshot')
 if name not in keep:c.pop('screenshot',None)
 if name in ['birthday_question','date_setup','birth_step3']:c['save']=name
 commands.append(c)
 if name=='birth_step3':break
def capture(name):commands.append({'frames':120,'screenshot':name})
def press(key,name=None):
 commands.append({'frames':12,'buttons':[key]})
 if name:capture(name)
 else:commands.append({'frames':120})
commands.append({'load':str((a.out/'birth_step3.state').resolve()),'frames':120});capture('birth_confirmation_initial')
press('Left','birth_oui_initial');press('Right','birth_non_initial');press('A','birth_refused')
press('Up','birth_month_up');press('A','birth_day_selected');press('Down','birth_day_down');press('A','birth_year_selected');press('Up','birth_year_up');press('A','birth_confirmation');press('Left','birth_oui');press('A');commands.append({'frames':600,'screenshot':'birth_future_rejected'})
press('A');press('A');press('Down');press('Down','birth_year_valid');press('A','birth_valid_confirmation');press('Left','birth_valid_oui');press('A');commands.append({'frames':600,'screenshot':'birth_accepted'})
commands.append({'load':str((a.out/'date_setup.state').resolve()),'frames':120});capture('rtc_initial');press('Up','rtc_month_up')
for field in ['day','year','hour','minute']:
 press('A','rtc_'+field+'_selected');press('Up','rtc_'+field+'_up')
press('A','rtc_confirmation');press('Left','rtc_oui_initial');press('Right','rtc_non');press('A','rtc_refused')
for key in ['A']*5:press(key)
press('Left','rtc_oui');press('A');commands.append({'frames':600,'screenshot':'rtc_accepted'});commands.append({'quit':True})
(a.out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
with (a.out/'console.log').open('w') as log:
 subprocess.run([sys.executable,str(root/'libretro_runner.py'),'--core',str(a.core.resolve()),'--rom',str(a.rom.resolve()),'--out',str(a.out.resolve())],input=''.join(json.dumps(x)+'\n' for x in commands),text=True,stdout=log,stderr=subprocess.STDOUT,check=True)
report={'rom_sha256':hashlib.sha256(a.rom.read_bytes()).hexdigest(),'core_sha256':hashlib.sha256(a.core.read_bytes()).hexdigest(),'controller_only':True,'same_rom_fresh_states':True,'images':[f.name for f in sorted(a.out.glob('*.png'))],'visual_review':'pending','scope':'Input branches require visual verification; no error condition or real-hardware test is implied.'};(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
