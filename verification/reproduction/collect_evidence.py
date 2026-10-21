#!/usr/bin/env python3
"""Collect native-render reports and compact pages; visual review stays pending.
Run after the scenario, navigation, A/B and targeted dialogue scripts complete.
Never interprets staged rendering as normal quest progression.
"""
import argparse,collections,hashlib,json,shutil,sys
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
p=argparse.ArgumentParser();p.add_argument('--version',required=True);p.add_argument('--previous',required=True);p.add_argument('--runs',type=Path,required=True);p.add_argument('--tag',default='final');p.add_argument('--previous-tag',default='corrected');p.add_argument('--cases',type=int,required=True);p.add_argument('--preview',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);p.add_argument('--build-report',type=Path,help='Explicit report for a checkpoint ROM');a=p.parse_args()
repo=Path(__file__).resolve().parents[2];v=a.version.lower();prev=a.previous.lower();runs=a.runs.resolve();dest=repo/f'verification/scenes_{v}';dest.mkdir(exist_ok=True);a.preview.mkdir(parents=True,exist_ok=True)
r=json.loads((runs/f'{v}_scenes_{a.tag}/results.json').read_text());rom=a.rom.read_bytes();build=json.loads((a.build_report.resolve() if a.build_report else repo/'verification/build_report.json').read_text());assert hashlib.sha256(rom).hexdigest()==r['rom_sha256']==build['output_sha256'];assert len(r['cases'])==a.cases and all(c['native_read_complete'] for c in r['cases'])
for stale in dest.glob('*.png'):stale.unlink()
tiles=[]
for c in r['cases']:
 groups=collections.defaultdict(list)
 for path in c.pop('images'):
  f=Path(path);groups[f.stem.split('_')[1]].append(f)
 c['review_images']=[];c['event_progression_validated']=False
 for page,files in groups.items():
  name=f"{c['case']}_{page}.png";shutil.copyfile(files[-1],dest/name);c['review_images'].append(name);tiles.append((name,dest/name))
r['selected_captures']=len(tiles);(dest/'render_report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
for n,start in enumerate(range(0,len(tiles),36)):
 batch=tiles[start:start+36];out=Image.new('RGB',(768,88*((len(batch)+2)//3)),'#222');draw=ImageDraw.Draw(out)
 for i,(name,f) in enumerate(batch):
  x=i%3*256;y=i//3*88;draw.text((x,y),name,fill='white');out.paste(Image.open(f).crop((0,160,256,224)),(x,y+20))
 out.save(a.preview/f'sheet_{n}.png')
for filename,newname in [('check_a.png','check_a.png'),('check_b_20.png','check_b.png')]:shutil.copyfile(runs/f'{v}_check_ab_{a.tag}'/filename,dest/newname)
for name in ['main_menu.png','settings.png','region_map.png']:shutil.copyfile(runs/f'{v}_navigation_{a.tag}'/name,dest/name)
old={x['id']:x for x in json.loads((repo/f'traduction/traduction_{prev}.json').read_text())};new={x['id']:x for x in json.loads((repo/f'traduction/traduction_{v}.json').read_text())};fields=['french','french_in_game','source_hex'];assert all(all(x[k]==new[i][k] for k in fields) for i,x in old.items())
reg={'baseline_entries':len(old),'all_preserved':True,'compared_fields':fields,'new_entries':len(new)-len(old),'new_changed_entries':build['new_changed_entries'],'passthrough_entries':[i for i,x in new.items() if i not in old and x['french']==x['english']]};(repo/f'verification/regression_{prev}_{v}.json').write_text(json.dumps(reg,indent=2)+'\n')
comparison={'identical':[],'different':[]}
for f in sorted((runs/f'fr_{prev}_{a.previous_tag}').glob('*.png')):
 g=runs/f'fr_{v}_{a.tag}'/f.name
 if not g.exists():continue
 box=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(g).convert('RGB')).getbbox();comparison['different' if box else 'identical'].append({'file':f.name,'bbox':box})
(repo/f'verification/comparison_{prev}_{v}.json').write_text(json.dumps(comparison,indent=2)+'\n')
nav=[]
for name in ['main_menu.png','settings.png','region_map.png']:
 before=Image.open(runs/f'{prev}_navigation_{a.previous_tag}'/name).convert('RGB');after=Image.open(runs/f'{v}_navigation_{a.tag}'/name).convert('RGB');box=ImageChops.difference(before,after).getbbox();before.paste(after.crop((65,110,125,135)),(65,110));nav.append({'file':name,'bbox':box,'identical':box is None,'identical_outside_clock':ImageChops.difference(before,after).getbbox() is None})
(repo/f'verification/navigation_comparison_{prev}_{v}.json').write_text(json.dumps(nav,indent=2)+'\n')
sys.path.insert(0,str(repo/'tools'))
from cpu65816_probe import CPU
from pointers import analyze
original=a.source.read_bytes();audit=analyze(original);deferred={int(k):ids for k,ids in build['deferred_entries'].items()};deferred[97]=build['deferred_block97_entries'];entries=[]
for bid,ids in deferred.items():
 aliases=next(b['block_ids'] for b in audit['blocks'] if bid in b['block_ids'])
 for alias in aliases:
  for idx in ids:
   x=CPU(original);x.load_block(alias);x.select(idx);y=CPU(rom);y.load_block(alias);y.select(idx);assert x.string()==y.string();entries.append({'entry':f'B{alias:03}-S{idx:03}','source_bytes_preserved':True})
d={'native_reads':len(entries),'unique_messages':sum(map(len,deferred.values())),'entries':entries}
for bid in [132,183]:
 if any(x['block_id']==bid for x in new.values()):continue
 block=next(b for b in audit['blocks'] if bid in b['block_ids']);s=int(block['offset'],16);e=int(block['end_exclusive'],16);assert rom[s:e]==original[s:e];d[f'block{bid}_source_bytes_preserved']=True
(repo/f'verification/deferred_texts_{v}.json').write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps({'sheets':(len(tiles)+35)//36,'images':len(tiles),'boot_identical':len(comparison['identical']),'boot_different':comparison['different'],'navigation':nav,'deferred_native_reads':len(entries)},ensure_ascii=False))
