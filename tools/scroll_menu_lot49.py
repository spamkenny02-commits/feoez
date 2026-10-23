"""Separate24px36-name scroll cache; full B004/B006 French remains intact."""
import json
from pathlib import Path
from french_font import encode_fr,visible_width
ROOT=Path(__file__).resolve().parents[1]
def patch_scroll_menu(rom,allocation_end):
 rows=json.loads((ROOT/'traduction/scroll_menu_short_lot49_fr.json').read_text());assert len(rows)==36
 start=(int(allocation_end,0)+15)&~15;assert 0x6c0000<=start<0x6d0000;payload=bytearray(6)
 for i,row in enumerate(rows):
  if not i%16:payload[(i//16)*2:(i//16)*2+2]=len(payload).to_bytes(2,'little')
  assert visible_width(row['french_short'],rom)<=24;payload.extend(encode_fr(row['french_short'])+b'\0')
 addr=start-0x200000;entry=(start+len(payload)+15)&~15
 wrapper=bytes.fromhex('22 b6 29 c3 08 c2 20 a9')+(addr&65535).to_bytes(2,'little')+bytes.fromhex('8d c5 10 e2 20 a9')+bytes([addr>>16])+bytes.fromhex('8d c7 10 28 6b');end=entry+len(wrapper)
 assert end<=0x6d0000 and not any(rom[start:end]);assert rom[0x6f56:0x6f5c]==bytes.fromhex('a9 04 22 b6 29 c3')
 out=bytearray(rom);out[start:start+len(payload)]=payload;out[entry:end]=wrapper;out[0x6f58:0x6f5c]=bytes([0x22])+(entry-0x200000).to_bytes(3,'little')
 return bytes(out),{'spans':[(start,end),(0x6f58,0x6f5c)],'catalog_cpu':hex(addr),'wrapper_cpu':hex(entry-0x200000),'allocation_start':hex(start),'allocation_end':hex(end),'entries':rows,'menu_width_pixels':24,'full_B004_B006_unchanged':True,'display_corrections_not_new':sum(r['correction_not_new'] for r in rows)}
