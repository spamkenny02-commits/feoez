#!/usr/bin/env python3
"""Native8x8 weekday graphics,exact duplicate banks and unchanged alphabets.
No date calculation or weekday-order change;runtime PPU validation is separate.
"""
import argparse,json,hashlib
from pathlib import Path
from menu_graphics_lot49 import raster
from french_font import encode_fr,visible_width
from numeric65816_probe import NumericCPU
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.rom.read_bytes();b=a.baseline.read_bytes();assert hashlib.sha256(b).hexdigest()=='2631d90bd0f2b0ed927055143117525517d06f15f29511439d6e76acdc371e4c';rows=json.loads((ROOT/'traduction/weekday_graphics_lot50_fr.json').read_text());assert len(rows)==7;assert r[0x6f0000:0x6f0900]==b[0x6f0000:0x6f0900];checks=[]
for i,e in enumerate(rows):
 assert e['weekday_sunday_zero']==i;data,px=raster(b,e['french_in_game'],1);pad=(8-px+1)//2;assert px+pad<=8;data=bytes(v>>pad for v in data)
 for strip in e['strips']:
  st=int(strip['offset'],16);assert strip['tiles']==1 and b[st:st+16].hex()==strip['source_hex'] and r[st:st+16]==data
 checks.append(dict(id=e['id'],english=e['english'],expanded_english=e['english_expanded'],french=e['french'],display=e['french_in_game'],pixels=px,left_pad=pad,width_contract=8,bitmap_sha256=hashlib.sha256(data).hexdigest(),native_palette_values=[0,1,2]))
assert r[0x6f0920:0x6f0930]==r[0x6f0930:0x6f0940]==b[0x6f0910:0x6f0920],'French Mardi/Mercredi use the exact original native M glyph'
class WeekdayHeaderCPU(NumericCPU):
 allowed_ranges=((0x4f1750,0x4f17a2),)
assert r[0x6f1750:0x6f17a2]==b[0x6f1750:0x6f17a2] and r[0xb739:0xb742]==bytes.fromhex('c2 20 29 ff 00 22 50 17 4f')
header_checks=[];widths=[]
for i,e in enumerate(rows):
 slot=e['native_string_slots'][0];st=int(slot['offset'],16);assert st==0x6f1740+2*i and slot['bytes']==2 and b[st:st+2].hex()==slot['source_hex'];assert r[st:st+2]==encode_fr(e['french_in_game'])+b'\0';widths.append(visible_width(e['french_in_game'],r))
 for cursor in [10,11,13,16,24]:
  for which,data in [('baseline',b),('candidate',r)]:
   c=WeekdayHeaderCPU(data);c.P=0x10;c.Y=0x2a;c.ram[0x1d2f:0x1d60]=b'\x5a'*49;c.ram[0x1d30:0x1d50]=b'\xaa'*32;seed=bytes.fromhex('d1 d9 d9 d5 1c d1 d2 1c d2 d2');c.ram[0x1d30:0x1d3a]=seed;c.write(0x1e15,cursor,1);c.write(0x1e16,0x5a,1);c.run(0x4f1750,a=i)
   txt=data[st:st+2].rstrip(b'\0');tail=txt+bytes.fromhex('18 df df df df');assert c.ram[0x1d30+cursor:0x1d30+cursor+len(tail)]==tail
   assert c.ram[0x1d30:0x1d3a]==seed[5:7]+b'\x1c'+seed[8:10]+b'\x1c'+seed[:4]
   assert c.read(0x1e15,1)==cursor+len(tail)and c.X==cursor+len(tail)and c.read(0x1e16,1)==0x5a and c.Y==0x2a
   assert c.ram[0x1d2f]==0x5a and c.ram[0x1d50:0x1d60]==b'\x5a'*16 and c.P&0x30==0x30
  header_checks.append(dict(day=i,input_cursor=cursor,candidate_result_cursor=cursor+6,canaries=True,date_prefix_native_reordered=True))
original_max=max(visible_width(e['english'],b)for e in rows);assert max(widths)<=original_max==13 and max(widths)==8
a.out.write_text(json.dumps(dict(rom_sha256=hashlib.sha256(r).hexdigest(),canonical_new_sources=7,physical_tile_copies=14,tile_bytes=16,max_pixels=max(e['pixels']for e in checks),native_alphabet_unchanged=True,weekday_order='Sunday-first,unchanged',French_calendar_initials='D L M M J V S',checks=checks,native_header_cases=header_checks,native_header_executions=70,header_source_slot_bytes=2,header_tested_canary_window_bytes=32,maximum_header_weekday_pixels=max(widths),old_maximum_header_weekday_pixels=original_max,header_code_unchanged=True,header_abi='A16/X8/D=DBR0;observed Friday A5,cursor13->19 on ordinary Almanac',header_scope='Synthetic copy/append/date-byte reorder cases;only22/12/1995 is naturally opened,not other date branches',scope=__doc__),ensure_ascii=False,indent=2)+'\n');print('PASS7weekday sources/14tiles+7fixed2byte slots;70native header executions;canaries/date prefix;code unchanged')
