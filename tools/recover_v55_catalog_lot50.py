#!/usr/bin/env python3
"""Recover generated bilingual V55 rows from pinned bytes and frozen ID sets.
IDs=all9038 bounded entries minus frozenV52 remainder plus approved47/48/49.
The candidate then executes the native raw reader for every one of6769 rows.
No guessed French text or incomplete generated catalog is accepted.
"""
import argparse,hashlib,json
from pathlib import Path
from pointers import analyze
from relocate import position
from extract import decode
from french_font import decode_fr,encode_fr
from cpu65816_probe import CPU
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--candidate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();source=a.source.read_bytes();base=a.baseline.read_bytes();rom=a.candidate.read_bytes();assert sha(source)=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'and sha(base)=='2631d90bd0f2b0ed927055143117525517d06f15f29511439d6e76acdc371e4c';allrows={}
 for b in analyze(source)['blocks']:
  if not b['main_text_pool']:continue
  st=int(b['offset'],16);old=source[st:int(b['end_exclusive'],16)];rel=[int(x,16)for x in b['relative_offsets']];bid=b['block_ids'][0]
  for i in range(1,256):
   try:s,e=position(old,rel,i)
   except ValueError:break
   key=f'B{bid:03}-S{i:03}';allrows[key]=dict(id=key,block_id=bid,string_id=i,source_hex=old[s:e].hex(),source_offset=hex(st+s),english=decode(old[s:e],True))
 assert len(allrows)==9038;remaining=json.loads((ROOT/'verification/remaining_bounded_strings_v52.json').read_text());ids=set(allrows)-{e['id']for e in remaining['entries']};assert len(ids)==5381;lots={k:'recovered_pre47'for k in ids};excluded=[]
 for n in [47,48,49]:
  data=json.loads((ROOT/f'traduction/lot{n}_fr.json').read_text());contracts=json.loads((ROOT/f'verification/layout_contracts_lot{n}.json').read_text())['entries']
  for b,rows in data.items():
   for i in rows:
    key=f'B{int(b):03}-S{int(i):03}'
    if n==47 and b not in ['3','4','5','6','7','12']and key not in contracts:excluded.append(key);continue
    assert key not in ids;ids.add(key);lots[key]=str(n)
 assert len(ids)==6769 and excluded==['B040-S036'];rows=[];read_hash=hashlib.sha256()
 for k in sorted(ids):
  row=allrows[k];b=CPU(base);b.load_block(row['block_id']);b.select(row['string_id']);start=b.mapped(b.read(0x8f,3));end=base.find(b'\0',start);assert 0<=end-start<4096;raw=base[start:end];fr=decode_fr(raw);assert encode_fr(fr)==raw,k
  c=CPU(rom);c.load_block(row['block_id']);c.select(row['string_id']);actual=c.string();assert actual==raw,k;read_hash.update(k.encode()+b'\0'+actual+b'\0');rows.append(dict(row,french=fr,french_in_game=fr,lot=lots[k],status='recovered_from_pinned_V55_and_native_candidate_read'))
 (ROOT/'traduction/traduction_v55.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');a.out.write_text(json.dumps(dict(source_sha256=sha(source),baseline_sha256=sha(base),rom_sha256=sha(rom),source_bounded_entries=9038,recovered_bilingual_rows=len(rows),native_candidate_full_string_reads=len(rows),excluded_unapproved_draft=excluded,ordered_read_sha256=read_hash.hexdigest(),scope='Exact native raw reads of6769 stored prior French rows;not game/branch/PPU coverage'),indent=2)+'\n');print('PASS recovered6769 exact bilingual rows and fresh native candidate readers')
if __name__=='__main__':main()
