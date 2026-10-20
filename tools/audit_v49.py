"""Compare startup spans and inventory untouched blocks on the exact V49 ROM."""
import argparse,hashlib,json
from pathlib import Path
from pointers import analyze
from relocate import position
from extract import decode
from startup_text import patch_startup

p=argparse.ArgumentParser()
p.add_argument('source',type=Path);p.add_argument('previous',type=Path);p.add_argument('built',type=Path)
a=p.parse_args();root=Path(__file__).resolve().parents[1]
source=a.source.read_bytes();before=a.previous.read_bytes();built=a.built.read_bytes()
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(source)=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
assert sha(before)=='a8451782359c523bd0d37a29dd2e30006b2e9f6e9c79768e7b31c5a86148491a'
build=json.loads((root/'verification/build_report.json').read_text())
assert build['output_sha256']==sha(built)
def save(name,data):
 (root/'verification'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
_,edits=patch_startup(source);assert len(edits)==32
spans=[]
for edit in edits:
 s=int(edit['offset'],16);e=s+edit['length']
 assert built[s:e]==before[s:e]==bytes.fromhex(edit['modified_hex'])
 spans.append({'offset':hex(s),'length':e-s,'bytes_identical_to_v48':True})
marker=b'SPC7110 CHECK OK'
for s in (0x2F25,0xFF0E7):assert built[s:s+len(marker)]==before[s:s+len(marker)]==source[s:s+len(marker)]==marker
save('startup_regression_v49.json',{'rom_sha256':sha(built),'baseline_v48_sha256':sha(before),'all_32_edits_preserved':True,'protocol_markers_preserved':True,'spans':spans})
inventory=json.loads((root/'verification/unprocessed_inventory_v48.json').read_text())
inventory['version']='V49';inventory['blocks']=[x for x in inventory['blocks'] if not set(x['block_ids']) & {40, 39, 37, 31}]
for b in inventory['blocks']:
 s=int(b['offset'],16);assert built[s:s+b['length']]==source[s:s+b['length']]
inventory['canonical_blocks']=len(inventory['blocks'])
save('unprocessed_inventory_v49.json',inventory)
save('deferred_reasons_v49.json',{'version': 'V49', 'source_bytes_preserved': True, 'entries': [{'block': 31, 'strings': [14, 15, 16, 17, 18], 'reason': 'Deferred selectors, special controls, untranslated labels, diagnostics or remaining dialogue. All original bytes retained pending dedicated layout/interaction work.'}, {'block': 37, 'strings': [2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 20, 21, 22, 23, 24, 26, 27, 29, 30, 36, 49, 51, 93, 100, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118], 'reason': 'Deferred selectors, special controls, untranslated labels, diagnostics or remaining dialogue. All original bytes retained pending dedicated layout/interaction work.'}, {'block': 39, 'strings': [12, 13, 22, 24, 25, 29, 30, 34, 35, 39, 40, 43, 44, 45, 46, 48, 49, 51, 53, 56], 'reason': 'Deferred selectors, special controls, untranslated labels, diagnostics or remaining dialogue. All original bytes retained pending dedicated layout/interaction work.'}, {'block': 40, 'strings': [25, 26, 29, 36, 54, 95, 102, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 136, 138, 140, 147, 154, 165, 167, 168, 169, 170, 186, 187, 191, 192, 193, 194, 195, 196, 197, 200, 207, 208, 212, 214, 215, 223], 'reason': 'Deferred selectors, special controls, untranslated labels, diagnostics or remaining dialogue. All original bytes retained pending dedicated layout/interaction work.'}], 'previous_deferred': 'All previous entries retained; see deferred_texts_v49.json and deferred_reasons_v48.json.'})
audit=analyze(source);translated={(r['block_id'],r['string_id']) for r in json.loads((root/'traduction/traduction_v49.json').read_text())}
remaining=[]
for b in audit['blocks']:
 if not b['main_text_pool']:continue
 bid=b['block_ids'][0];s=int(b['offset'],16);raw=source[s:int(b['end_exclusive'],16)];rr=[int(x,16) for x in b['relative_offsets']]
 for idx in range(1,256):
  try:u,v=position(raw,rr,idx)
  except ValueError:break
  if (bid,idx) not in translated:
   remaining.append({'id':f'B{bid:03}-S{idx:03}','block_ids':b['block_ids'],'source_offset':hex(s+u),'source_length':v-u,'english':decode(raw[u:v],True),'empty':not raw[u:v].strip(b' \x01')})
save('remaining_bounded_strings_v49.json',{'version':'V49','scope':'Canonical bounded main-text blocks only; includes menus, special formats, empty strings and debug prompts. Not a count of dialogue alone. Other graphics and unbounded block 42 remain outside this list.','remaining_entries':len(remaining),'nonempty_entries':sum(not x['empty'] for x in remaining),'entries':remaining})
print(json.dumps({'startup_edits':32,'untouched_blocks':len(inventory['blocks']),'remaining_bounded_entries':len(remaining)}))
