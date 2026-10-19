"""Compare startup spans and inventory untouched blocks on the exact V46 ROM."""
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
assert sha(before)=='1fcb5d6ddab647de9a72550b6720af7c9a48dee2db2439de9d85a5e8c5819425'
build=json.loads((root/'verification/build_report.json').read_text())
assert build['output_sha256']==sha(built)
def save(name,data):
 (root/'verification'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
_,edits=patch_startup(source);assert len(edits)==32
spans=[]
for edit in edits:
 s=int(edit['offset'],16);e=s+edit['length']
 assert built[s:e]==before[s:e]==bytes.fromhex(edit['modified_hex'])
 spans.append({'offset':hex(s),'length':e-s,'bytes_identical_to_v45':True})
marker=b'SPC7110 CHECK OK'
for s in (0x2F25,0xFF0E7):assert built[s:s+len(marker)]==before[s:s+len(marker)]==source[s:s+len(marker)]==marker
save('startup_regression_v46.json',{'rom_sha256':sha(built),'baseline_v45_sha256':sha(before),'all_32_edits_preserved':True,'protocol_markers_preserved':True,'spans':spans})
inventory=json.loads((root/'verification/unprocessed_inventory_v45.json').read_text())
inventory['version']='V46';inventory['blocks']=[x for x in inventory['blocks'] if 56 not in x['block_ids']]
for b in inventory['blocks']:
 s=int(b['offset'],16);assert built[s:s+b['length']]==source[s:s+b['length']]
inventory['canonical_blocks']=len(inventory['blocks'])
save('unprocessed_inventory_v46.json',inventory)
save('deferred_reasons_v46.json',{'version':'V46','source_bytes_preserved':True,'entries':[{'block':56,'strings':[12],'reason':'Literal x5 and special blank-line layout; original bytes retained pending dedicated analysis and rendering.'}],'previous_deferred':'All previous entries retained; see deferred_texts_v46.json and deferred_reasons_v45.json.'})
audit=analyze(source);translated={(r['block_id'],r['string_id']) for r in json.loads((root/'traduction/traduction_v46.json').read_text())}
remaining=[]
for b in audit['blocks']:
 if not b['main_text_pool']:continue
 bid=b['block_ids'][0];s=int(b['offset'],16);raw=source[s:int(b['end_exclusive'],16)];rr=[int(x,16) for x in b['relative_offsets']]
 for idx in range(1,256):
  try:u,v=position(raw,rr,idx)
  except ValueError:break
  if (bid,idx) not in translated:
   remaining.append({'id':f'B{bid:03}-S{idx:03}','block_ids':b['block_ids'],'source_offset':hex(s+u),'source_length':v-u,'english':decode(raw[u:v],True),'empty':not raw[u:v].strip(b' \x01')})
save('remaining_bounded_strings_v46.json',{'version':'V46','scope':'Canonical bounded main-text blocks only; includes menus, special formats, empty strings and debug prompts. Not a count of dialogue alone. Other graphics and unbounded block 42 remain outside this list.','remaining_entries':len(remaining),'nonempty_entries':sum(not x['empty'] for x in remaining),'entries':remaining})
print(json.dumps({'startup_edits':32,'untouched_blocks':len(inventory['blocks']),'remaining_bounded_entries':len(remaining)}))
