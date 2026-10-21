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
assert len(old)==4987 and set(current)-set(old)==new and len(new)==sum(map(len,lot.values()))
for key,before in old.items():
 for field in ('english','source_hex','source_offset','french','french_in_game'):
  assert before[field]==current[key][field],(key,field)
aliases=json.loads((root/'verification/aliases_lot46.json').read_text())
canonical=new-set(aliases)
for alias,link in aliases.items():
 for field in ('english','source_hex','french'):
  assert current[alias][field]==current[link['canonical']][field],(alias,field)
assert len({current[k]['french'] for k in canonical})==len(canonical)
assert len({current[k]['english'] for k in canonical})==len(canonical)
contracts=json.loads((root/'verification/numeric_contracts_lot46.json').read_text())
checks=[]
for key in sorted(new):
 r=current[key];t=r['french'];en=r['english'];raw=bytes.fromhex(r['source_hex'])
 assert t!=en and en.strip()
 if r['block_id'] in (17,18):
  assert t==r['french_in_game'] and t.count('\n')==en.count('\n')==1
  assert [bool(x.strip()) for x in t.split('\n')]==[bool(x.strip()) for x in en.split('\n')]
 assert re.findall(r'<[0-9A-F]{2}>',t)==re.findall(r'<[0-9A-F]{2}>',en)
 contract=contracts.get(key,{})
 dynamic_widths={int(c,16):contract['reservation_pixels_per_numeric_slot'] for c in contract.get('commands',[])}
 text_contract=json.loads((root/'verification/text_contracts_lot46.json').read_text()).get(key,{})
 dynamic_widths.update({int(c,16):width for c,width in text_contract.get('widths',{}).items()})
 widths=[visible_width(s,rom,dynamic_widths) for s in r['french_in_game'].split('\n')];assert max(widths)<=216
 for data,expected in ((source,raw),(rom,encode_fr(r['french_in_game']))):
  cpu=CPU(data);cpu.load_block(r['block_id']);cpu.select(r['string_id']);assert cpu.string()==expected
 checks.append({'id':key,'widths':widths,'calendar_two_rows_and_empty_rows_preserved':True if r['block_id'] in (17,18) else 'not_calendar','numeric_contract':contract or None,'source_and_output_native_read':True})
build=json.loads((root/'verification/build_report_lot46_checkpoint.json').read_text());assert build['output_sha256']==sha(rom) and build['new_entries']==len(new)
from calendar_ui_lot46 import patch_calendar_ui,START,END
expected_ui,ui_report=patch_calendar_ui(source)
assert rom[START:END]==expected_ui[START:END]
report={'additional_native_ui_entries':len(ui_report['entries']),'new_distinct_texts_total':len(canonical)+len(ui_report['entries']),'new_bounded_occurrences':len(new),'aliases_not_counted':aliases,'lot':46,'target':400,'new_distinct_texts':len(canonical),'corrections':0,'previous_entries_preserved':len(old),'integrated_entries_checkpoint':len(rows),'source_sha256':sha(source),'rom_sha256':sha(rom),'checks':checks,'runtime_visual_validation':'Separate staged results; not asserted by this script.','remaining_phase1':'Variables 05–07, effects, songs and special formats; natural calendar dates still need validation.'}
(root/'verification/lot46_checkpoint_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(f'PASS: {len(canonical)+len(ui_report["entries"])} distinct texts, {len(new)} bounded occurrences, 4987 baseline entries unchanged, {2*len(new)} native source/output reads.')
