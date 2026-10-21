#!/usr/bin/env python3
"""Validate partial lot46 against V51, without changing release reports."""
import argparse,hashlib,json,re
from pathlib import Path
from french_font import encode_fr,visible_width
from cpu65816_probe import CPU
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('built',type=Path);a=p.parse_args();root=Path(__file__).resolve().parents[1]
source=a.source.read_bytes();rom=a.built.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(source)=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
previous=json.loads((root/'traduction/traduction_v51.json').read_text());rows=json.loads((root/'traduction/traduction_v52.json').read_text())
old={r['id']:r for r in previous};current={r['id']:r for r in rows};lot=json.loads((root/'traduction/lot46_fr.json').read_text());new={f'B{int(b):03}-S{int(i):03}' for b,v in lot.items() for i in v}
assert len(old)==4987 and set(current)-set(old)==new and len(new)==52
for key,before in old.items():
 for field in ('english','source_hex','source_offset','french','french_in_game'):
  assert before[field]==current[key][field],(key,field)
assert len({current[k]['french'] for k in new})==52
checks=[]
for key in sorted(new):
 r=current[key];t=r['french'];en=r['english'];raw=bytes.fromhex(r['source_hex'])
 assert t==r['french_in_game'] and t!=en and en.strip() and t.count('\n')==en.count('\n')==1
 assert re.findall(r'<[0-9A-F]{2}>',t)==re.findall(r'<[0-9A-F]{2}>',en)
 assert [bool(x.strip()) for x in t.split('\n')]==[bool(x.strip()) for x in en.split('\n')]
 widths=[visible_width(s,rom) for s in t.split('\n')];assert max(widths)<=216
 for data,expected in ((source,raw),(rom,encode_fr(t))):
  cpu=CPU(data);cpu.load_block(r['block_id']);cpu.select(r['string_id']);assert cpu.string()==expected
 checks.append({'id':key,'widths':widths,'two_rows_and_empty_rows_preserved':True,'source_and_output_native_read':True})
build=json.loads((root/'verification/build_report_lot46_checkpoint.json').read_text());assert build['output_sha256']==sha(rom) and build['new_entries']==52
report={'lot':46,'target':400,'new_distinct_texts':52,'corrections':0,'previous_entries_preserved':len(old),'integrated_entries_checkpoint':len(rows),'source_sha256':sha(source),'rom_sha256':sha(rom),'checks':checks,'runtime_visual_validation':'Separate staged results; not asserted by this script.','remaining_phase1':'Variables 05–07, effects, songs and special formats; natural calendar dates still need validation.'}
(root/'verification/lot46_checkpoint_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS: 52 distinct additions, 4987 baseline entries unchanged, 104 native source/output reads.')
