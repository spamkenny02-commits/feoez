#!/usr/bin/env python3
"""Collect a named suite without asserting visual review or natural event coverage."""
import argparse,hashlib,json,shutil,re
from pathlib import Path
from PIL import Image,ImageChops
p=argparse.ArgumentParser();p.add_argument('--runs',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);p.add_argument('--tag',required=True);p.add_argument('--suite',type=Path,required=True);p.add_argument('--version',default='v52');p.add_argument('--build-report',type=Path);p.add_argument('--reference-version');p.add_argument('--reference-tag');p.add_argument('--reference-rom-sha256');a=p.parse_args();assert re.fullmatch(r'v[0-9]+',a.version);v=a.version;reference=a.reference_version or ('v51' if v=='v52' else 'v52');reference_tag=a.reference_tag or ('final51' if v=='v52' else 'lot46p400b');reference_sha=a.reference_rom_sha256 or ('ddfce7b8f4ad9425e37a636478b0774495f809efa23b42c2ddbe981f55e61c31' if reference=='v51' else 'd74ba2aaff5e9f01dacde9c630e6e8c34495b7aba5a6a5f5256f6e72d6a4f862');a.runs=a.runs.resolve();repo=Path(__file__).resolve().parents[2];dest=repo/f'verification/scenes_{v}';dest.mkdir(exist_ok=True);h=hashlib.sha256(a.rom.read_bytes()).hexdigest();build=json.loads((a.build_report or repo/'verification/build_report_lot46_checkpoint.json').read_text());assert h==build['output_sha256'];suite=json.loads(a.suite.read_text());report={'rom_sha256':h,'tag':a.tag,'visual_review':'pending','event_progression_validated':False,'groups':{},'images':{},'case_count':0};known={}
for group in suite['groups']:
 name=group['name'];r=json.loads((a.runs/f'{v}_{name}_{a.tag}/results.json').read_text());assert r['rom_sha256']==h;assert all(c['native_read_complete'] for c in r['cases']);report['case_count']+=len(r['cases'])
 for case in r['cases']:
  copied=[]
  for filename in case.pop('images'):
   f=Path(filename);data=f.read_bytes();sha=hashlib.sha256(data).hexdigest()
   if sha not in known:
    target=f'{name}_{case["case"]}_{f.stem}.png';shutil.copyfile(f,dest/target);known[sha]=target;report['images'][target]={'sha256':sha,'source':str(f.relative_to(a.runs))}
   copied.append(known[sha])
  case['review_images']=copied;case['event_progression_validated']=False
 report['groups'][name]=r
assert report['case_count']==suite.get('case_count',488)
if suite.get('lot')==47:
 required={x['id'] for x in json.loads((repo/'verification/lot47_counting.json').read_text())['canonical_sources']}
 required|={f'CALMONTH-{i:02}' for i in range(1,13)}
 covered={p for g in report['groups'].values() for c in g['cases'] for p in c.get('synthetic_slot_fixture',{}).get('providers',[c['entry']])}
 assert required<=covered,sorted(required-covered)
 report['canonical_provider_ids_exercised']=sorted(required)
 report['canonical_new_texts_exercised']=len(required)
for source,name in [(a.runs/f'{v}_check_ab_{a.tag}/check_a.png','check_a.png'),(a.runs/f'{v}_check_ab_{a.tag}/check_b_20.png','check_b.png')]+[(a.runs/f'{v}_navigation_{a.tag}'/n,n) for n in ['main_menu.png','settings.png','region_map.png']]:
 shutil.copyfile(source,dest/name);report['images'][name]={'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source':str(source.relative_to(a.runs))}

for stale in dest.glob('*.png'):
 if stale.name not in report['images']:stale.unlink()
report['unique_text_captures']=len(known);(dest/'render_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
for label,new,old in [('startup',f'fr_{v}_{a.tag}',f'fr_{reference}_{reference_tag}'),('navigation',f'{v}_navigation_{a.tag}',f'{reference}_navigation_{reference_tag}')]:
 rows=[]
 reference_log=a.runs/old/('core_console.log' if label=='startup' else 'console.log')
 ready=[]
 for line in reference_log.read_text().splitlines():
  try:value=json.loads(line)
  except ValueError:continue
  if value.get('ready'):ready.append(value)
 assert ready and ready[0]['source_sha256']==reference_sha,'Reference screenshots belong to another ROM'
 for f in sorted((a.runs/old).glob('*.png')):
  g=a.runs/new/f.name;assert g.exists(),g;box=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(g).convert('RGB')).getbbox();rows.append({'file':f.name,'identical':box is None,'bbox':box})
 assert rows
 (repo/f'verification/{label}_regression_{v}.json').write_text(json.dumps({'rom_sha256':h,'reference_rom_sha256':reference_sha,'comparisons':rows,'all_identical':all(r['identical'] for r in rows)},indent=2)+'\n')
print(json.dumps({'rom_sha256':h,'cases':report['case_count'],'unique_text_images':len(known),'visual_review':'pending'}))
