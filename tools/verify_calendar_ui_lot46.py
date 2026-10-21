#!/usr/bin/env python3
"""Check literal FE menu streams and their continuation cursor independently.
The seven labels do not end the menu program. The next descriptor at ED53
must be reached exactly; zero-filling a shortened stream changes execution.
"""
import argparse,hashlib,json,sys
from pathlib import Path
from french_font import encode_fr,visible_width
from calendar_ui_lot46 import START,END,HEADERS
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('candidate',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();source=a.source.read_bytes();rom=a.candidate.read_bytes();root=Path(__file__).resolve().parents[1]
assert hashlib.sha256(source).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
entries=json.loads((root/'traduction/calendar_ui_lot46_fr.json').read_text());cursor=START;checks=[]
for head,entry in zip(HEADERS,entries):
 assert rom[cursor:cursor+4]==head,(entry['id'],'changed FE descriptor')
 cursor+=4;end=rom.index(0,cursor,END);raw=rom[cursor:end]
 assert raw.rstrip(b' ')==encode_fr(entry['french']).rstrip(b' '),entry['id']
 pixels=visible_width(entry['french']+' '*(len(raw)-len(encode_fr(entry['french']))),rom)
 assert pixels<=head[-1]*8,(entry['id'],pixels,head[-1]*8)
 cursor=end+1;checks.append({'id':entry['id'],'pixels_with_padding':pixels,'field_limit_pixels':head[-1]*8,'next_cursor':hex(cursor)})
assert cursor==END,('misaligned continuation descriptor',hex(cursor),hex(END))
assert rom[END:END+24]==source[END:END+24]
# Native FE handler calls C1:7702 then restores DP09 from the resulting D9 cursor.
assert source[0x5e1a:0x5e2e]==bytes.fromhex('22 02 77 c1 c2 20 a5 d9 85 09 e2 20 a5 db 85 0b c2 20 ad f3')
a.out.write_text(json.dumps({'rom_sha256':hashlib.sha256(rom).hexdigest(),'source_sha256':hashlib.sha256(source).hexdigest(),'labels':checks,'continuation_descriptor':hex(cursor),'scope':'Parser alignment, literal labels and pixel field bounds. Natural display remains a separate test.'},ensure_ascii=False,indent=2)+'\n');print('PASS seven labels, field widths and exact menu continuation')
