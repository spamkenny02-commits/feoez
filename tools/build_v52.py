#!/usr/bin/env python3
"""Rebuild the complete 400-distinct-text lot 46; runtime evidence remains separate."""
import json,shutil
from pathlib import Path
from build_lot46_checkpoint import main
if __name__=='__main__':
 main()
 root=Path(__file__).resolve().parents[1]
 report=json.loads((root/'verification/build_report_lot46_checkpoint.json').read_text())
 assert report['new_distinct_texts_total']==400 and report['new_entries']==394
 shutil.copyfile(root/'Tengai_Makyou_Zero_FR_LOT46_CHECKPOINT.ips',root/'Tengai_Makyou_Zero_FR_V52.ips')
 report.update(version='V52',release_status='complete_lot_build_requires_separate_runtime_report',runtime_validation='see verification/emulation_report_v52.json')
 (root/'verification/build_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
