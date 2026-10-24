"""French display variants of existing B002/B003 names;zero new sources.

The native64px item strip has variable-width native glyphs and two-pixel word
spacing.46 original suffix pictograms remain pixel-identical at their original
columns. Full names and articles stay in the bounded French catalogs.
"""
import json,hashlib
from pathlib import Path
from menu_graphics_lot49 import glyph
ROOT=Path(__file__).resolve().parents[1]
def pixels(raw):
 return [[((raw[x//8*16+2*y]>>(7-x%8))&1)+2*((raw[x//8*16+2*y+1]>>(7-x%8))&1)for x in range(64)]for y in range(8)]
def pack(p):
 out=bytearray(128)
 for y in range(8):
  for x in range(64):
   v=p[y][x];i=x//8*16+y*2;bit=128>>(x%8)
   if v&1:out[i]|=bit
   if v&2:out[i+1]|=bit
 return bytes(out)
def raster_item(rom,text):
 text=text.replace('’',"'").replace('œ','oe').replace('Œ','OE');gs=[[[0]for _ in range(8)]if c==' 'else glyph(rom,c)for c in text];width=sum(len(g[0])+1 for g in gs);body=[[0]*max(64,width)for _ in range(8)];x=0
 for g in gs:
  for y in range(8):body[y][x:x+len(g[y])]=g[y]
  x+=len(g[0])+1
 result=[[2 if body[y][x]else 1 if x and body[y][x-1]else 0 for x in range(max(64,width))]for y in range(8)]
 return result,width
def patch_items(rom):
 rows=json.loads((ROOT/'traduction/item_graphics_lot50_fr.json').read_text());assert len(rows)==303;out=bytearray(rom);icons=0
 for i,e in enumerate(rows):
  assert e['index']==i and e['new_distinct_source']is False;st=0x6f6000+128*i;raw=rom[st:st+128];assert hashlib.sha256(raw).hexdigest()==e['source_bitmap_sha256'];p,w=raster_item(rom,e['french_short']);assert w==e['pixels'] and w<=e['limit'],e['id'];p=[line[:64]for line in p]
  if e['icon']is not None:
   original=pixels(raw);start=e['icon']['start'];assert w<start
   for y in range(8):p[y][start:]=original[y][start:]
   icons+=1
  out[st:st+128]=pack(p)
 assert icons==46
 return bytes(out),dict(spans=[(0x6f6000,0x6ff780)],rows=rows,prior_bitmap_variants=303,new_distinct_sources=0,original_pictograms_preserved=46,scope='Reconstructed short forms;fresh native/PPU validation required;does not recreate the lostP8b binary')
