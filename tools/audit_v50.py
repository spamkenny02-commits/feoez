"""Compare startup spans and inventory untouched blocks on the exact V50 ROM."""
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
assert sha(before)=='e13a8bcdee8cac7d53e33fb9092de5ec5d84d5613ef83ff5836cd70b6c2af396'
build=json.loads((root/'verification/build_report.json').read_text())
assert build['output_sha256']==sha(built)
def save(name,data):
 (root/'verification'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
_,edits=patch_startup(source);assert len(edits)==32
spans=[]
for edit in edits:
 s=int(edit['offset'],16);e=s+edit['length']
 assert built[s:e]==before[s:e]==bytes.fromhex(edit['modified_hex'])
 spans.append({'offset':hex(s),'length':e-s,'bytes_identical_to_v49':True})
marker=b'SPC7110 CHECK OK'
for s in (0x2F25,0xFF0E7):assert built[s:s+len(marker)]==before[s:s+len(marker)]==source[s:s+len(marker)]==marker
save('startup_regression_v50.json',{'rom_sha256':sha(built),'baseline_v49_sha256':sha(before),'all_32_edits_preserved':True,'protocol_markers_preserved':True,'spans':spans})
inventory=json.loads((root/'verification/unprocessed_inventory_v49.json').read_text())
inventory['version']='V50';inventory['blocks']=[x for x in inventory['blocks'] if not set(x['block_ids']) & {33, 35, 38, 41, 30}]
for b in inventory['blocks']:
 s=int(b['offset'],16);assert built[s:s+b['length']]==source[s:s+b['length']]
inventory['canonical_blocks']=len(inventory['blocks'])
save('unprocessed_inventory_v50.json',inventory)
save('deferred_reasons_v50.json',{'version': 'V50', 'source_bytes_preserved': True, 'entries': [{'block': 29, 'strings': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 21, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 84, 87, 88, 90, 91, 96, 97, 105, 106, 107, 114, 115, 116], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 30, 'strings': [6, 7, 8], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 31, 'strings': [16], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 33, 'strings': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 24, 25, 26, 27], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 37, 'strings': [9, 10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 36, 51], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 38, 'strings': [3, 13], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 39, 'strings': [49], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 40, 'strings': [25, 26, 29, 36, 54, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 147, 154, 165, 167, 168, 169, 186, 187, 200, 207, 208, 212], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 41, 'strings': [15, 25, 30, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 58, 63, 69, 70, 71, 72, 73, 74, 78, 79, 80, 82, 84, 86, 95, 96, 97, 98, 103, 107, 110, 115, 116, 117, 121, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 144], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 66, 'strings': [10, 32, 33, 35, 36, 37, 67], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 95, 'strings': [11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 26, 27, 31, 32, 38, 39, 44, 45, 46, 50, 51, 54, 55, 184], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 96, 'strings': [23, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 132, 'strings': [59, 99, 122], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 231, 'strings': [32], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}, {'block': 252, 'strings': [98, 99, 100, 101], 'reason': 'Remaining dynamic substitutions, selectors, musical/effect controls, labels or diagnostics; original bytes retained pending dedicated work.'}], 'previous_deferred': 'All remaining deferred entries retained; see deferred_texts_v50.json and deferred_reasons_v49.json.'})
audit=analyze(source);translated={(r['block_id'],r['string_id']) for r in json.loads((root/'traduction/traduction_v50.json').read_text())}
remaining=[]
for b in audit['blocks']:
 if not b['main_text_pool']:continue
 bid=b['block_ids'][0];s=int(b['offset'],16);raw=source[s:int(b['end_exclusive'],16)];rr=[int(x,16) for x in b['relative_offsets']]
 for idx in range(1,256):
  try:u,v=position(raw,rr,idx)
  except ValueError:break
  if (bid,idx) not in translated:
   remaining.append({'id':f'B{bid:03}-S{idx:03}','block_ids':b['block_ids'],'source_offset':hex(s+u),'source_length':v-u,'english':decode(raw[u:v],True),'empty':not raw[u:v].strip(b' \x01')})
save('remaining_bounded_strings_v50.json',{'version':'V50','scope':'Canonical bounded main-text blocks only; includes menus, special formats, empty strings and debug prompts. Not a count of dialogue alone. Other graphics and unbounded block 42 remain outside this list.','remaining_entries':len(remaining),'nonempty_entries':sum(not x['empty'] for x in remaining),'entries':remaining})
print(json.dumps({'startup_edits':32,'untouched_blocks':len(inventory['blocks']),'remaining_bounded_entries':len(remaining)}))
