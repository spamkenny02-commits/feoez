#!/usr/bin/env python3
"""Rebuild the complete lot49 IPS from the pinned original English ROM.
Runtime evidence is separate. Neither source nor output ROM is distributed.
"""
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--rom-out',type=Path,required=True);a=p.parse_args()
 if a.source.resolve()==a.rom_out.resolve():p.error('Cannot overwrite source ROM')
 assert hashlib.sha256(a.source.read_bytes()).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
 if not (ROOT/'traduction/traduction_v54.json').exists():
  with tempfile.TemporaryDirectory(prefix='feoe-v54-baseline-') as directory:
   subprocess.run([sys.executable,str(ROOT/'tools/build_v54.py'),str(a.source.resolve()),'--rom-out',str(Path(directory)/'baseline.sfc')],cwd=ROOT,check=True)
 sys.argv=[str(ROOT/'tools/build_lot49_checkpoint.py'),str(a.source.resolve()),'--rom-out',str(a.rom_out.resolve()),'--require-complete-lot']
 from build_lot49_checkpoint import main as build
 build()
 report=json.loads((ROOT/'verification/build_report_lot49_checkpoint.json').read_text());assert report['new_distinct_texts_total_prepared']==400
 shutil.copyfile(ROOT/'Tengai_Makyou_Zero_FR_LOT49_CHECKPOINT.ips',ROOT/'Tengai_Makyou_Zero_FR_V55.ips')
 report.update(version='V55',release_status='complete_lot_build_requires_separate_runtime_report',runtime_validation='see verification/emulation_report_v55.json; verify exact ROM hash')
 (ROOT/'verification/build_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
