"""Verify the400 frozen canonical source identities recovered from checkpoint.
The manifest preserves counting across interruption. It is not runtime evidence.
"""
import json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def identity(s):
 s=s.replace('’',"'").replace('‘',"'");s=re.sub(r'x[1-5]|<[0-9A-F]{2}>',' ',s);s=' '.join(s.casefold().split());return s

def audit():
 manifest=json.loads((ROOT/'verification/lot49_sources_manifest.json').read_text());assert len(manifest['sources'])==400
 lot=json.loads((ROOT/'traduction/lot49_fr.json').read_text());allrows={f'B{int(b):03}-S{int(i):03}':{'french':fr} for b,es in lot.items() for i,fr in es.items()}
 for f in ['credits_lot49_fr.json','menu_graphics_lot49_fr.json','menu_native_lot49_fr.json']:
  allrows.update({e['id']:e for e in json.loads((ROOT/'traduction'/f).read_text())})
 seen={};ids=set()
 for e in manifest['sources']:
  assert e['id'] not in ids;ids.add(e['id']);assert allrows[e['id']]['french']==e['french'],e['id']
  if 'english' in allrows[e['id']]:assert allrows[e['id']]['english']==e['english'],e['id']
  key=identity(e['english']);key='weapon' if key=='weapons' else key
  assert key not in seen,(e['id'],seen.get(key));assert key and identity(e['french'])!=key,e['id'];seen[key]=e['id']
 assert {e['kind'] for e in manifest['sources']}=={'bounded','credits','graphics','native_ui'}
 return manifest
if __name__=='__main__':
 from collections import Counter
 r=audit();print('canonical prepared',len(r['sources']),Counter(e['kind'] for e in r['sources']))
