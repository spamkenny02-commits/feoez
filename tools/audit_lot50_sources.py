#!/usr/bin/env python3
"""Audit current new-source counter,previous-source overlap and explicit aliases.
Does not establish game coverage or completion of a phase/lot.
"""
import json
from pathlib import Path
from audit_new_sources_lot49 import identity
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'verification/lot50_sources_manifest.json').read_text());new=m['new'];assert len(new)==sum(e['count']for e in new)==m['new_distinct_sources_prepared']==42
old=json.loads((ROOT/'traduction/traduction_v55.json').read_text());assert len(old)==6769
for f in ['credits_lot49_fr.json','menu_graphics_lot49_fr.json','menu_native_lot49_fr.json']:old+=json.loads((ROOT/'traduction'/f).read_text())
prior={identity(e.get('english',''))for e in old};seen={}
for e in new:
 k=identity(e['english']);assert k and k not in seen,(e['id'],seen.get(k));assert k not in prior,('prior source',e['id']);seen[k]=e['id'];assert identity(e['french'])!=k
names=json.loads((ROOT/'traduction/shop_names_lot50_fr.json').read_text());assert sum(e['new_distinct_source']for e in names)==28 and len(names)==29
alias=next(e for e in names if not e['new_distinct_source']);assert alias['id']=='SHOPNAME-10' and alias['canonical_alias']=='SHOPNAME-01'
assert not {'SHOPNAME-03','SHOPNAME-13','SHOPNAME-19','SHOPNAME-10'}&{e['id']for e in new}
r=dict(lot=50,target=400,current_prepared_distinct_sources=42,prior_bounded_rows_checked=6769,normalized_prior_overlap=0,normalized_new_duplicates=0,shop_name_fields=29,shop_name_new_sources=28,shop_name_semantic_aliases_excluded=1,prior_item_display_variants_excluded=303,prior_bitmap_copies_excluded=20,scope=__doc__)
(ROOT/'verification/lot50_source_audit_recovery42a.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS42 distinct new sources;28new shop names;aliases/prior variants excluded;lot incomplete')
