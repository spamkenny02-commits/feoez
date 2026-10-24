#!/usr/bin/env python3
"""Execute actual compact-cache wrapper/select/reader, then compare full catalog."""
import argparse,json,hashlib
from pathlib import Path
from numeric65816_probe import NumericCPU
from cpu65816_probe import CPU
from french_font import encode_fr
class CacheCPU(NumericCPU):
 allowed_ranges=((0x4c0000,0x4d0000),(0xc329b6,0xc32aa4),(0xc02c5e,0xc02d00))
 select=CPU.select
 string=CPU.string
p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();rom=a.rom.read_bytes();root=Path(__file__).resolve().parents[1];build=json.loads((root/'verification/build_report_lot49_checkpoint.json').read_text());rows=json.loads((root/'traduction/scroll_menu_short_lot49_fr.json').read_text());full={r['id']:r for r in json.loads((root/'traduction/traduction_v55.json').read_text())} if (root/'traduction/traduction_v55.json').exists() else {r['id']:{'french_in_game':r['french_full']}for r in rows};cases=[]
for row in rows:
 c=CacheCPU(rom);c.X=117;c.run(int(build['scroll_menu']['wrapper_cpu'],16),4);assert c.X==117 and c.S==0x1ff;c.select(int(row['id'][-3:]));assert c.string()==encode_fr(row['french_short'])
 d=CPU(rom);d.load_block(4);d.select(int(row['id'][-3:]));assert d.string()==encode_fr(full[f"B004-S{int(row['id'][-3:]):03}"]['french_in_game'])
 cases.append(int(row['id'][-3:]))
a.out.write_text(json.dumps({'rom_sha256':hashlib.sha256(rom).hexdigest(),'passed_compact_and_full_pairs':len(cases),'cases':cases,'scope':'Native wrapper/select/reader and full-text preservation; learned-ID menu fixture and PPU separate.'},indent=2)+'\n');print('PASS36 compact/full native pairs')
