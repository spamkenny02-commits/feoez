"""Native8px alphabet -> bounded2bpp menu strips; palette body/shadow retained."""
import json,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def glyph(rom,ch):
 if ch==' ':return [[0]*3 for _ in range(8)]
 plain=unicodedata.normalize('NFD',ch);base=plain[0];punct={'.':74,'!':75,'?':76,',':77,"'":78,'"':79,':':80,';':80,'-':81,'/':82,'(':84,')':85,'+':98}
 tile=ord(base)-65+12 if 'A'<=base<='Z' else ord(base)-97+38 if 'a'<=base<='z' else ord(base)-48+2 if base.isdigit() else punct.get(base)
 if tile is None:raise ValueError(ch)
 raw=rom[0x6f0000+tile*16:0x6f0000+(tile+1)*16];a=[[int(bool(raw[y*2]&(128>>x))) for x in range(8)] for y in range(8)]
 if len(plain)>1:
  accent=plain[1];cols=[x for x in range(8) if any(a[y][x] for y in range(8))];mid=(min(cols)+max(cols))//2
  if base.isupper():a=[[0]*8]+a[:7]
  if accent=='\u0301':a[0][min(7,mid+1)]=1;a[1][mid]=1
  elif accent=='\u0300':a[0][max(0,mid-1)]=1;a[1][mid]=1
  elif accent=='\u0302':a[0][mid]=1;a[1][max(0,mid-1)]=1;a[1][min(7,mid+1)]=1
  elif accent=='\u0327':a[7][mid]=1
  elif accent=='\u0308':a[0][max(0,mid-1)]=1;a[0][min(7,mid+1)]=1
  else:raise ValueError(ch)
 cols=[x for x in range(8) if any(a[y][x] for y in range(8))];return [line[min(cols):max(cols)+1] for line in a]
def raster(rom,text,tiles):
 text=text.replace('’',"'").replace('œ','oe').replace('Œ','OE');gs=[glyph(rom,c) for c in text];width=sum(len(g[0])+1 for g in gs)-1;assert width+1<=tiles*8,(text,width+1,tiles*8)
 body=[[0]*(tiles*8) for _ in range(8)];x=0
 for g in gs:
  for y in range(8):body[y][x:x+len(g[y])]=g[y]
  x+=len(g[0])+1
 out=bytearray(tiles*16)
 for x in range(tiles*8):
  for y in range(8):
   value=2 if body[y][x] else 1 if x and body[y][x-1] else 0;p=(x//8)*16+y*2;bit=128>>(x%8)
   if value&1:out[p]|=bit
   if value&2:out[p+1]|=bit
 return bytes(out),width+1
def patch_menu_graphics(rom):
 entries=json.loads((ROOT/'traduction/menu_graphics_lot49_fr.json').read_text());out=bytearray(rom);spans=[];report=[]
 for e in entries:
  start=int(e['offset'],16);n=e['tiles']*16;assert rom[start:start+n].hex()==e['source_hex'];assert not any(start<z and start+n>a for a,z in spans);spans.append((start,start+n));new,px=raster(rom,e['french'],e['tiles']);out[start:start+n]=new;report.append({'id':e['id'],'offset':e['offset'],'tiles':e['tiles'],'pixels':px,'width_pixels':e['tiles']*8,'english':e['english'],'french':e['french']})
 return bytes(out),{'entries':report,'spans':spans,'scope':'Native alphabet/palette/bounds; live UI and visual review separate.'}
