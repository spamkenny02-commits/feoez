#!/usr/bin/env python3
"""Prepare finite, explicitly synthetic native-render fixtures for lot47.
Every provider is read back through original native lookup/selection. No fixture
proves real event values, availability, clock progression or player navigation.
"""
import argparse,hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from cpu65816_probe import CPU
from calendar65816_probe import CalendarCPU
from french_font import visible_width,encode_fr
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--build-report',type=Path,required=True);p.add_argument('--diagnostic-core',type=Path,required=True);a=p.parse_args();rom=a.rom.read_bytes();build=json.loads(a.build_report.read_text());assert hashlib.sha256(rom).hexdigest()==build['output_sha256'];assert build['new_distinct_texts_total_prepared']==400
rows=json.loads((ROOT/'traduction/traduction_v53.json').read_text());new=[r for r in rows if r['lot']=='47'];assert len(new)==build['new_bounded_occurrences'];byid={r['id']:r for r in rows};contracts=json.loads((ROOT/'verification/layout_contracts_lot47.json').read_text())['entries'];groups={};fixtures={};providers={}
def native(b,i):
 c=CPU(rom);c.load_block(b);c.select(i);return c.string().hex()
def num(n):return bytes(0x21+int(d) for d in str(n)).hex()
def longest(blocks):
 eligible=[r for r in rows if r['block_id'] in blocks and len(encode_fr(r['french_in_game']))<=31 and '\n' not in r['french_in_game']]
 return max(eligible,key=lambda r:visible_width(r['french_in_game'],rom))
item=longest([1,2,3]);skill=longest([5,7]);scroll=longest([4,6]);fusion=longest([6]);species=max([byid[f'B041-S{i:03}'] for i in range(59,63)],key=lambda r:visible_width(r['french_in_game'],rom))
def provider(row):return native(row['block_id'],row['string_id'])
def formatted(mode,raw,slot):
 c=CalendarCPU(rom);data=bytes.fromhex(raw);at=0x32aa+32*slot;c.ram[at:at+len(data)+1]=data+b'\0';c.write(0x8f,0x100,3);c.ram[0x100]=4+slot;c.run({1:0x4d3c00,2:0x4d3c60,3:0x4d3cb0,4:0x4d3d00}[mode],32*slot);return bytes(c.ram[at:at+32]).split(b'\0')[0].hex()
def add(group,b,i,name,slots=None,source_ids=None,stress=False):
 groups.setdefault(group,[]).append([b,i,name]);f={'slots':slots or {},'providers':source_ids or [f'B{b:03}-S{i:03}'],'scope':'Synthetic native text fixture, not a natural event or selector.','layout_stress':stress};fr=byid[f'B{b:03}-S{i:03}']['french_in_game'];expected={};state=dict(slots or {})
 for mode,token in re.findall(r'x([1-4])<([0-9A-F]{2})>',fr):
  slot=str(int(token,16)-4);state[slot]=formatted(int(mode),state[slot],int(slot));expected.setdefault(slot,[]).append(state[slot])
 if expected:f['expected_consumed_slots']={s:sorted(set(v)) for s,v in expected.items()}
 fixtures.setdefault(group,{})[name]=f
for r in new:
 b,i=r['block_id'],r['string_id'];key=r['id'];name=f'b{b:03}s{i:03}'
 if b==12 and i==25:add('labels',b,i,name);continue
 if b==43:
  slots={1:{'0':num(0xffffff)},2:{'0':num(0xffffff)},3:{'0':native(12,2),'1':num(255)},4:{'0':native(12,2),'1':provider(skill)},5:{'0':provider(item)},6:{'0':native(3,49)}}[i]
  add('messages',b,i,name,slots);continue
 if b in [3,4,5,6,7,12]:
  src=[key];actor=native(12,1)
  if b==3:add('catalogs',37,9,name,{'0':actor,'1':native(b,i)},src)
  elif b in [4,6]:add('catalogs',29,6,name,{'0':actor,'3':native(b,i)},src)
  elif b in [5,7]:add('catalogs',29,7,name,{'0':actor,'3':native(b,i)},src)
  elif i==8:add('catalogs',29,6,name,{'0':native(b,i),'3':native(4,1)},src)
  else:add('catalogs',29,21,name,{'2':native(b,i)},src)
  continue
 if b in [13,14,15,16]:add('labels',b,i,name);continue
 slots={};dw=contracts[key]['widths'];actual=set(re.findall(r'<(0[4-7])>',r['french_in_game']));fr=r['french_in_game']
 for token in sorted(actual):
  s=str(int(token,16)-4);width=dw[token]
  if width==0:value='08'
  elif width in [14,28,56]:value=num(1)
  elif width==26:value=native(95,54)
  elif width==32:value=native(41,69)
  elif width==44:value=native(99,14)
  elif width==48:value=native(12,18)
  elif width==65:value=provider(species)
  elif width==76:value=native(2,78)
  elif width==80:value=native(12,6)
  elif width==100:value=native(2,90)
  elif width==110:value=encode_fr('ABCDEFGHIJ').hex()
  elif width==119:value=provider(fusion if b==29 and i==9 else scroll if b==29 and i==6 else skill)
  elif width==144:value=provider(item)
  else:raise ValueError((key,token,width))
  if b==29 and token=='07' and i in [6,7,9]:
   value=provider(scroll if i==6 else skill if i==7 else fusion)
  inline=re.search(r'x([1-4])'+re.escape('<'+token+'>'),fr)
  if inline:value=num({1:10,2:11 if b in [95,99] else 23,3:59,4:1}[int(inline[1])])
  slots[s]=value
 add('messages',b,i,name,slots)
# Every month provider is consumed in its actual native x1 formatter.
for month in range(1,13):
 day=28 if month==2 else 30 if month in [4,6,9,11] else 31
 add('formats',31,16,f'birthday_month{month:02}',{'0':num(month),'1':num(day),'2':num(1)},['B031-S016',f'CALMONTH-{month:02}'])
add('formats',31,16,'birthday_leapday',{'0':num(2),'1':num(29),'2':num(255)},['B031-S016','CALMONTH-02'])
# Ordinal domains are finite; these are formatter stress cases, not lunar dates.
for day in range(1,32):add('formats',40,165,f'lunar_ordinal_{day:02}',{'1':num(day)},stress=True)
for b,i,maximum in [(41,95,5),(41,96,5),(40,208,5),(40,212,5),(97,98,15)]:
 for ordinal in range(2,maximum+1):add('formats',b,i,f'ordinal_{b}_{i}_{ordinal:02}',{'1':num(ordinal)})
for n in range(1,5):add('formats',41,98,f'feed_next_{n}',{'1':num(n),'2':num(n+1)})
for b,i in [(210,36),(210,75),(210,76),(210,77),(212,18)]:
 for hour,minute in [(0,0),(1,1),(11,59),(12,30),(23,59)]:
  slot={'0':num(hour)}
  if i in [36,18]:slot['1']=num(minute)
  add('formats',b,i,f'time_{b}_{i}_{hour:02}_{minute:02}',slot)
# Worst storage name glyph is11px. This exceeds the known keyboard alphabet,
# intentionally testing the proven byte-storage bound, not a reachable name.
for i in list(range(36,52))+[25,52,53,54,55,56,58,63,71]:
 base=fixtures['messages'][f'b041s{i:03}'];slot=dict(base['slots']);slot['1']='9f'*10
 add('stress',41,i,f'pet_name_bound_{i}',slot,stress=True)
# All style branches are explicitly synthetic; Quit remains enabled in normal flow.
for b,i in [(41,130),(41,135),(41,139),(66,35),(66,36),(66,37)]:
 base=fixtures['messages'][f'b{b:03}s{i:03}'];slot={k:'0a' if int(k)%2==0 else '08' for k in base['slots']}
 add('stress',b,i,f'mixed_modes_{b}_{i}',slot,stress=True)
# Maximum24-bit numeric fields test the conservative width contract separately.
for b,i in [(29,84),(29,105),(40,26),(41,107),(91,1),(91,2),(94,4),(193,4)]:
 base=fixtures['messages'][f'b{b:03}s{i:03}'];slot={s:(num(0xffffff) if contracts[f'B{b:03}-S{i:03}']['widths'][f'{int(s)+4:02X}']==56 else v) for s,v in base['slots'].items()}
 add('stress',b,i,f'numeric_bound_{b}_{i}',slot,stress=True)
covered={k for group in fixtures.values() for f in group.values() for k in f['providers']};required={r['id'] for r in new}|{f'CALMONTH-{i:02}' for i in range(1,13)};assert required<=covered,sorted(required-covered)
core=a.diagnostic_core.name;core_sha=hashlib.sha256(a.diagnostic_core.read_bytes()).hexdigest();suite={'lot':47,'rom_sha256':build['output_sha256'],'native_month_sources':12,'new_bounded_occurrences':len(new),'case_count':sum(map(len,groups.values())),'scope':'Synthetic native text consumption/rendering; actual map/save UI, event branches, clock, selectors and music require separate evidence.','groups':[]}
for name,cases in groups.items():
 filename=f'cases_lot47_400_{name}.json';fixfile=f'fixtures_lot47_400_{name}.json';(ROOT/'verification/reproduction'/filename).write_text(json.dumps(cases,indent=2)+'\n');(ROOT/'verification/reproduction'/fixfile).write_text(json.dumps(fixtures[name],ensure_ascii=False,indent=2)+'\n');suite['groups'].append({'name':name,'cases':filename,'slot_fixtures':fixfile,'core_filename':core,'core_sha256':core_sha})
(ROOT/'verification/reproduction/suite_lot47_400.json').write_text(json.dumps(suite,indent=2)+'\n');(ROOT/'verification/reproduction/cases_v53.json').write_text(json.dumps(groups['messages'],indent=2)+'\n');print(json.dumps({'rom_sha256':build['output_sha256'],'cases':suite['case_count'],'groups':{k:len(v) for k,v in groups.items()}},indent=2))
