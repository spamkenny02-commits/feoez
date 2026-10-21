"""Compare startup spans and inventory untouched blocks on the exact V51 ROM."""
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
assert sha(before)=='e94f7f4dab0ac39e01de7c640d676f674a0d8a81e8e2ed5bc6d3f926950c9603'
build=json.loads((root/'verification/build_report.json').read_text())
assert build['output_sha256']==sha(built)
def save(name,data):
 (root/'verification'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
_,edits=patch_startup(source);assert len(edits)==32
spans=[]
for edit in edits:
 s=int(edit['offset'],16);e=s+edit['length']
 assert built[s:e]==before[s:e]==bytes.fromhex(edit['modified_hex'])
 spans.append({'offset':hex(s),'length':e-s,'bytes_identical_to_v50':True})
marker=b'SPC7110 CHECK OK'
for s in (0x2F25,0xFF0E7):assert built[s:s+len(marker)]==before[s:s+len(marker)]==source[s:s+len(marker)]==marker
save('startup_regression_v51.json',{'rom_sha256':sha(built),'baseline_v50_sha256':sha(before),'all_32_edits_preserved':True,'protocol_markers_preserved':True,'spans':spans})
inventory=json.loads((root/'verification/unprocessed_inventory_v50.json').read_text())
inventory['version']='V51';inventory['blocks']=[x for x in inventory['blocks'] if not set(x['block_ids']) & {17,18}]
for b in inventory['blocks']:
 s=int(b['offset'],16);assert built[s:s+b['length']]==source[s:s+b['length']]
inventory['canonical_blocks']=len(inventory['blocks'])
save('unprocessed_inventory_v51.json',inventory)
save('deferred_reasons_v51.json',{'version': 'V51', 'source_bytes_preserved': True, 'entries': [{'block': 29, 'strings': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 21, 84, 87, 88, 90, 91, 96, 97, 105, 106, 107, 114, 115, 116], 'reason': 'Remaining untranslated entries, including empty dates and notices; original bytes retained. See English inventory for exact content.'}, {'block': 33, 'strings': [1, 2, 13, 26], 'reason': 'Remaining untranslated entries, including empty dates and notices; original bytes retained. See English inventory for exact content.'}, {'block': 91, 'strings': [1, 2, 35], 'reason': 'Remaining untranslated entries, including empty dates and notices; original bytes retained. See English inventory for exact content.'}, {'block': 95, 'strings': [11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 26, 27, 31, 32, 38, 39, 44, 45, 50, 51, 54, 55, 184], 'reason': 'Remaining untranslated entries, including empty dates and notices; original bytes retained. See English inventory for exact content.'}, {'block': 202, 'strings': [5, 8], 'reason': 'Remaining untranslated entries, including empty dates and notices; original bytes retained. See English inventory for exact content.'}, {'block': 17, 'strings': [5, 18, 32, 49, 57, 62, 63, 64, 70, 94, 96, 127, 128, 160, 164, 173, 175, 187, 189, 191, 192], 'reason': 'Remaining untranslated entries, including empty dates and notices; original bytes retained. See English inventory for exact content.'}, {'block': 18, 'strings': [5, 9, 23, 24, 27, 32, 45, 48, 50, 54, 55, 61, 64, 71, 72, 75, 76, 83, 85, 89, 95, 96, 98, 101, 107, 115, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192], 'reason': 'Remaining untranslated entries, including empty dates and notices; original bytes retained. See English inventory for exact content.'}], 'previous_deferred': 'Remaining special variables, effects, labels and debug preserved; see deferred_reasons_v50.json.'})
audit=analyze(source);translated={(r['block_id'],r['string_id']) for r in json.loads((root/'traduction/traduction_v51.json').read_text())}
remaining=[]
for b in audit['blocks']:
 if not b['main_text_pool']:continue
 bid=b['block_ids'][0];s=int(b['offset'],16);raw=source[s:int(b['end_exclusive'],16)];rr=[int(x,16) for x in b['relative_offsets']]
 for idx in range(1,256):
  try:u,v=position(raw,rr,idx)
  except ValueError:break
  if (bid,idx) not in translated:
   remaining.append({'id':f'B{bid:03}-S{idx:03}','block_ids':b['block_ids'],'source_offset':hex(s+u),'source_length':v-u,'english':decode(raw[u:v],True),'empty':not raw[u:v].strip(b' \x01')})
save('remaining_bounded_strings_v51.json',{'version':'V51','scope':'Canonical bounded main-text blocks only; includes menus, special formats, empty strings and debug prompts. Not a count of dialogue alone. Other graphics and unbounded block 42 remain outside this list.','remaining_entries':len(remaining),'nonempty_entries':sum(not x['empty'] for x in remaining),'entries':remaining})
print(json.dumps({'startup_edits':32,'untouched_blocks':len(inventory['blocks']),'remaining_bounded_entries':len(remaining)}))
