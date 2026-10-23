#!/usr/bin/env python3
"""Explicitly reject prior translated English sources in the frozen400 manifest."""
import json,hashlib
from pathlib import Path
from audit_new_sources_lot49 import audit,identity
r=Path(__file__).resolve().parents[1];manifest=audit();baseline=json.loads((r/'traduction/traduction_v54.json').read_text());old={identity(e['english']) for e in baseline}
assert len(baseline)==6534
for e in manifest['sources']:assert identity(e['english']) not in old,('already translated source',e['id'])
report={'new_canonical_sources_checked':400,'prior_bounded_rows_checked':6534,'overlap':0,'scope':'Normalized source identities, not visual game coverage.'}
(r/'verification/prior_sources_audit_lot49.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS400 source identities absent from6534 prior translations')
