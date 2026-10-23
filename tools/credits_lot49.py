"""Native629-record credit stream, preserving blank rows/contributors/sentinel."""
import json
from pathlib import Path
from french_font import encode_fr,decode_fr,WIDTHS
ROOT=Path(__file__).resolve().parents[1];START,END=0x6d5000,0x6d668c
def patch_credits(rom):
 entries=json.loads((ROOT/'traduction/credits_lot49_fr.json').read_text());byoff={int(e['offset'],16):e for e in entries};lines=[];p=START;changed=[]
 assert rom[END]==255 and rom[0x36fd4:0x36fdf]==bytes.fromhex('a9 00 50 85 e6 e2 20 a9 4d 85 e8')
 while p<END:
  q=rom.index(0,p);raw=rom[p:q]
  if p in byoff:
   e=byoff[p];assert raw.hex()==e['source_hex'];t=encode_fr(e['french']);assert 0<len(t)<=45
   assert [b for b in raw if b in [0x17,0x18,0x1e]]==[b for b in t if b in [0x17,0x18,0x1e]]
   width=sum(rom[WIDTHS+b] for b in t);assert width<=216
   lead=min(len(raw)-len(raw.lstrip(b'\xdf')),max(0,(216-width)//8));new=b'\xdf'*lead+t;changed.append(e['id'])
  else:new=raw
  lines.append(bytearray(new));p=q+1
 assert p==END
 slack=(END-START)-sum(len(x)+1 for x in lines)
 if slack<0:
  for i in sorted(range(len(lines)),key=lambda i:sum(rom[WIDTHS+b] for b in lines[i]),reverse=True):
   if slack>=0:break
   if lines[i] and lines[i][0]==0xdf and decode_fr(bytes(lines[i])).replace('<DF>','').strip() in {e['french'].replace('’',"'") for e in entries}:lines[i].pop(0);slack+=1
 assert slack>=0
 for line in lines:
  if not slack:break
  if not line:continue
  px=sum(rom[WIDTHS+b] for b in line);n=min(slack,45-len(line),max(0,(216-px)//rom[WIDTHS+0x20]));line.extend(b' '*n);slack-=n
 assert not slack
 payload=b''.join(bytes(x)+b'\0' for x in lines);assert len(payload)==END-START and len(lines)==629
 assert all(len(x)<=45 and sum(rom[WIDTHS+b] for b in x)<=216 for x in lines)
 out=bytearray(rom);out[START:END]=payload
 return bytes(out),{'offset':hex(START),'end':hex(END),'lines':629,'unchanged_empty_line_positions':[i for i,x in enumerate(lines) if not x],'changed_occurrences':len(entries),'changed_ids':changed,'sentinel_preserved':True,'maximum_bytes':max(map(len,lines)),'maximum_width_pixels':max(sum(rom[WIDTHS+b] for b in x) for x in lines),'runtime_review':'pending','scope':'Native credits only; no natural ending proof.'}
