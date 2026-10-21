#!/usr/bin/env python3
"""Collect a named suite without asserting visual review or natural event coverage."""
import argparse,hashlib,json,shutil
from pathlib import Path
from PIL import Image,ImageChops
p=argparse.ArgumentParser();p.add_argument('--runs',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);p.add_argument('--tag',required=True);p.add_argument('--suite',type=Path,required=True);a=p.parse_args();a.runs=a.runs.resolve();repo=Path(__file__).resolve().parents[2];dest=repo/'verification/scenes_v52';dest.mkdir(exist_ok=True);h=hashlib.sha256(a.rom.read_bytes()).hexdigest();build=json.loads((repo/'verification/build_report_lot46_checkpoint.json').read_text());assert h==build['output_sha256'];suite=json.loads(a.suite.read_text());report={'rom_sha256':h,'tag':a.tag,'visual_review':'pending','event_progression_validated':False,'groups':{},'images':{},'case_count':0};known={}
for group in suite['groups']:
 name=group['name'];r=json.loads((a.runs/f'v52_{name}_{a.tag}/results.json').read_text());assert r['rom_sha256']==h;assert all(c['native_read_complete'] for c in r['cases']);report['case_count']+=len(r['cases'])
 for case in r['cases']:
  copied=[]
  for filename in case.pop('images'):
   f=Path(filename);data=f.read_bytes();sha=hashlib.sha256(data).hexdigest()
   if sha not in known:
    target=f'{name}_{case["case"]}_{f.stem}.png';shutil.copyfile(f,dest/target);known[sha]=target;report['images'][target]={'sha256':sha,'source':str(f.relative_to(a.runs))}
   copied.append(known[sha])
  case['review_images']=copied;case['event_progression_validated']=False
 report['groups'][name]=r
assert report['case_count']==488
for source,name in [(a.runs/f'v52_check_ab_{a.tag}/check_a.png','check_a.png'),(a.runs/f'v52_check_ab_{a.tag}/check_b_20.png','check_b.png')]+[(a.runs/f'v52_navigation_{a.tag}'/n,n) for n in ['main_menu.png','settings.png','region_map.png']]:
 shutil.copyfile(source,dest/name);report['images'][name]={'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source':str(source.relative_to(a.runs))}

for stale in dest.glob('*.png'):
 if stale.name not in report['images']:stale.unlink()
report['unique_text_captures']=len(known);(dest/'render_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
for label,new,old in [('startup',f'fr_v52_{a.tag}','fr_v51_final51'),('navigation',f'v52_navigation_{a.tag}','v51_navigation_final51')]:
 rows=[]
 for f in sorted((a.runs/old).glob('*.png')):
  g=a.runs/new/f.name;assert g.exists(),g;box=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(g).convert('RGB')).getbbox();rows.append({'file':f.name,'identical':box is None,'bbox':box})
 assert rows
 (repo/f'verification/{label}_regression_v52.json').write_text(json.dumps({'rom_sha256':h,'reference_rom_sha256':'ddfce7b8f4ad9425e37a636478b0774495f809efa23b42c2ddbe981f55e61c31','comparisons':rows,'all_identical':all(r['identical'] for r in rows)},indent=2)+'\n')
print(json.dumps({'rom_sha256':h,'cases':report['case_count'],'unique_text_images':len(known),'visual_review':'pending'}))
