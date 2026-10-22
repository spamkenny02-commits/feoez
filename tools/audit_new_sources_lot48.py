#!/usr/bin/env python3
"""Check new canonical source identities against the complete V53 base."""
import collections,json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1];old=json.loads((root/'traduction/traduction_v53.json').read_text());new=json.loads((root/'verification/lot48_counting.json').read_text())['canonical_sources']
def identity(s):
 s=re.sub(r'x[1-5]','',s);s=re.sub(r'<0[4-7]>',' VAR ',s);s=re.sub(r'<[0-9A-Fa-f]{2}>','',s);return ' '.join(s.split()).casefold()
seen=collections.defaultdict(list)
for row in new:seen[identity(row['english'])].append(row['id'])
prior={identity(row['english']) for row in old};cross=[row['id'] for row in new if identity(row['english']) in prior];assert len(new)==400 and not cross and all(len(v)==1 for v in seen.values())
r={'lot':48,'canonical_new_sources':400,'normalized_sources_unique':True,'normalized_sources_absent_from_v53':True,'normalization':'Collapse whitespace,casefold,remove styles/timing/x1..5 and normalize04..07 variables; semantic aliases additionally excluded.','source_ids':[x['id'] for x in new],'cross_collisions':cross};(root/'verification/shared_sources_strict_lot48.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS400 distinct canonical sources, no normalized V53 collision')
