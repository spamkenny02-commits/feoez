#!/usr/bin/env python3
"""Execute FD8B's original X0 copier and native 4D2C00 width calculator.
PPU fixtures and natural combat progression are separate reports.
"""
import argparse,hashlib,json
from pathlib import Path
from numeric65816_probe import NumericCPU
from cpu65816_probe import CPU
from french_font import encode_fr,WIDTHS
class BannerCPU(NumericCPU):
 allowed_ranges=((0xc329b6,0xc32aa4),(0xc02c5e,0xc02d00),(0xc029a1,0xc029bb),(0xc07880,0xc078fc),(0x4d3900,0x4d393f),(0x4d3b80,0x4d3be9),(0x4f1d30,0x4f1d46),(0x4d2c00,0x4d2c34))
 def mapped(self,address):
  if 0xdf0000<=address<0xe00000:return address-0xb00000
  return super().mapped(address)
 load_block=CPU.load_block
 select=CPU.select
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--candidate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();source=a.source.read_bytes();rom=a.candidate.read_bytes();root=Path(__file__).resolve().parents[1]
assert hashlib.sha256(source).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
assert rom[0x77af:0x77b7]==source[0x77af:0x77b7]==bytes.fromhex('da a2 00 20 80 78 64 00')
assert bytes.fromhex('a2 1c 20 af 77') in source[0x7750:0x7780]
producer=bytes.fromhex('0e 13 12 bb 43 09 fd 8b 1b 02');assert source[0x653c1:0x653cb]==rom[0x653c1:0x653cb]==producer
rows=[x for x in json.loads((root/'traduction/traduction_v54.json').read_text()) if x['lot']=='48' and x['block_id']==19];cases=[]
for row in rows:
 raw=encode_fr(row['french_in_game']);assert 0<len(raw)<=45 and b'\1' not in raw
 c=BannerCPU(rom);c.ram[0x1d2e:0x1d65]=b'\x55'*55;c.load_block(19);c.X=0
 c.run(0xc07880,row['string_id'],limit=500000);actual=bytes(c.ram[0x1d30:0x1d65]).split(b'\0')[0];assert actual==raw,row['id'];assert c.ram[0x1d2e]==0x55 and c.ram[0x1d5e:0x1d65]==b'\x55'*7
 pixels=sum(rom[WIDTHS+b] for b in actual);c.write(0,0,1);tiles=c.run(0x4d2c00,limit=50000);assert tiles==(pixels+7)//8 and tiles<=28,(row['id'],pixels,tiles)
 cases.append({'id':row['id'],'native_bytes':len(actual),'native_width_pixels':pixels,'native_width_tiles':tiles,'field_dialogue_rules_used':False})
a.out.write_text(json.dumps({'rom_sha256':hashlib.sha256(rom).hexdigest(),'native_executions':len(cases),'consumer':'FD8B C07722; C077AF X0; C07880/C078A1;4D2C00 width;28tile banner','ordinary_action_script_offset':'0x653c1','selector':'RAM43BB','canaries_preserved':True,'cases':cases,'scope':'Exact native copied bytes and dynamic font width only. See staged battle PPU fixture and separate natural controller replay; not every attack branch traversed.'},ensure_ascii=False,indent=2)+'\n');print('PASS',len(cases),'native battle copier and width executions')
