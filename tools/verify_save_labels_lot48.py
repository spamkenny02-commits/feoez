#!/usr/bin/env python3
"""Execute the original27tile save-slot label reader and padding leaf.
This proves the exact selected bytes/copier/canaries and padding width, not PPU
rendering, natural availability, combat actions, or the complete game menus.
"""
import argparse,json,hashlib
from pathlib import Path
from numeric65816_probe import NumericCPU
from cpu65816_probe import CPU
from french_font import encode_fr,visible_width,WIDTHS
class MenuCPU(NumericCPU):
 allowed_ranges=((0xc329b6,0xc32aa4),(0xc02c5e,0xc02d00),(0xc029a1,0xc029bb),
                 (0xc07880,0xc078fc),(0x4d3900,0x4d393f),(0x4d3b80,0x4d3be9),(0x4f1d30,0x4f1d46))
 def mapped(self,address):
  if 0xdf0000<=address<0xe00000:return address-0xb00000
  return super().mapped(address)
 load_block=CPU.load_block
 select=CPU.select
 string=CPU.string
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--candidate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();source=a.source.read_bytes();rom=a.candidate.read_bytes();root=Path(__file__).resolve().parents[1]
assert hashlib.sha256(source).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
assert bytes.fromhex('8a a2 1b 20 6f 78 60') in source[0x992d:0x9970]
assert source[0x7880:0x788a]==bytes.fromhex('8e 2f 1d 20 a1 78 22 00 39 4d')
assert rom[WIDTHS+0xdf]==8,'Native padding glyph must span one8px tile'
rows=json.loads((root/'traduction/traduction_v54.json').read_text());cases=[]
for row in rows:
 if row['lot']!='48' or row['block_id'] !=16:continue
 raw=encode_fr(row['french_in_game']);assert b'\1' not in raw and 0<len(raw)<=45
 px=visible_width(row['french_in_game'],rom);assert px<=216
 c=MenuCPU(rom);c.ram[0x1d2e:0x1d65]=b'\x55'*55;c.load_block(row['block_id']);c.X=27;c.Y=37
 result=c.run(0xc07880,row['string_id'],limit=500000)
 padded=bytes(c.ram[0x1d30:0x1d65]).split(b'\0')[0]
 assert padded[:len(raw)]==raw and padded[len(raw):]==b'\xdf'*(len(padded)-len(raw)),row['id']
 assert len(padded)<=45 and c.ram[0x1d2e]==0x55 and c.ram[0x1d2f]==27 and c.ram[0x1d5e:0x1d65]==b'\x55'*7,row['id']
 assert c.read(9,2)==0x1d30 and c.ram[0xb]==0 and result==27,row['id']
 assert len(padded)==min(45,len(raw)+max(0,27-(px+7)//8)),(row['id'],px,len(padded))
 cases.append({'id':row['id'],'bytes':len(raw),'pixels':px,'padded_bytes':len(padded),'native_reader_passed':True})
report={'source_sha256':hashlib.sha256(source).hexdigest(),'candidate_sha256':hashlib.sha256(rom).hexdigest(),'native_executions':len(cases),'consumer':'C0993D catalog16 with save location7E2505 (or corrupt entry1),X27; C07880/C078A1 then4D3900','width_pixels':216,'maximum_bytes':45,'cases':cases,'scope':'Exact fixed-line help copy and padding leaf; no natural save error, final location or load-slot UI traversal claim.'};a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS',len(cases),'native save-label reads/padding executions')
