"""Source-checked fixed native menu text spans, preserving lengths/terminators."""
import json
from pathlib import Path
from french_font import encode_fr,visible_width
ROOT=Path(__file__).resolve().parents[1]
def patch_native_menu(rom):
 entries=json.loads((ROOT/'traduction/menu_native_lot49_fr.json').read_text());out=bytearray(rom);spans=[]
 for e in entries:
  for l in e['lines']:
   p=int(l['offset'],16);old=encode_fr(l['english']);new=encode_fr(l['french']);assert rom[p:p+len(old)]==old and rom[p+len(old)]==0
   assert len(new)<=len(old) and visible_width(l['french'],rom)<=l['width_pixels'];out[p:p+len(old)]=new+b' '*(len(old)-len(new));spans.append((p,p+len(old)))
 return bytes(out),{'spans':spans,'entries':entries,'scope':'Fixed native strings only; live context validation separate.'}
