#!/usr/bin/env python3
"""Rebuild a selected, contract-backed lot48 checkpoint from pinned source.
Baseline strings use their exact V53 bytes/layout. Runtime validation is separate.
Generate traduction_v53.json first with build_v53.py; no ROM is distributed.
"""
import argparse,hashlib,json,re
from pathlib import Path
from pointers import analyze
from relocate import position
from extract import decode
from block_storage import store_blocks
from french_font import encode_fr,decode_fr,layout_fr,visible_width,patch_font,FONT,WIDTHS

from startup_text import patch_startup
from calendar_ui_lot46 import patch_calendar_ui
from calendar_formats_lot47 import patch_calendar_formats
from build_lot46_checkpoint import checksum
from insert import make_ips,apply_ips
from cpu65816_probe import CPU
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--rom-out',type=Path,required=True);p.add_argument('--require-complete-lot',action='store_true');p.add_argument('--prepare-only',action='store_true',help='Write a candidate with native lookup checks explicitly pending; never a validated release');a=p.parse_args();assert a.source.resolve()!=a.rom_out.resolve();source=a.source.read_bytes();assert len(source)==7340032 and hashlib.sha256(source).hexdigest()=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
 baseline=apply_ips(source,(ROOT/'Tengai_Makyou_Zero_FR_V53.ips').read_bytes());assert hashlib.sha256(baseline).hexdigest()=='ba2b468c2ba2f05ba542d421213c1564861fed7e35018704b88038608dcc2f7c'
 rows=json.loads((ROOT/'traduction/traduction_v53.json').read_text());assert len(rows)==5961;base={r['id']:r for r in rows};lot=json.loads((ROOT/'traduction/lot48_fr.json').read_text());contracts=json.loads((ROOT/'verification/layout_contracts_lot48.json').read_text());approved=contracts['entries'];catalogs={}
 input_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'traduction/lot48_fr.json',ROOT/'verification/aliases_lot48.json',ROOT/'verification/layout_contracts_lot48.json',Path(__file__)]}
 new={}
 for b,entries in lot.items():
  for idx,text in entries.items():
   key=f'B{int(b):03}-S{int(idx):03}'
   if int(idx) not in catalogs.get(int(b),[]) and key not in approved:continue
   assert key not in base;new[key]={'id':key,'block_id':int(b),'string_id':int(idx),'french':text,'lot':'48','status':'checkpoint_runtime_review_pending'}
 audit=analyze(source);order=[b['block_ids'][0] for b in json.loads((ROOT/'verification/build_report_lot47_checkpoint.json').read_text())['blocks']];order+=sorted({r['block_id'] for r in new.values()}-set(order));prepared=[];font,fontedits=patch_font(source);allrows=base|new;widths=[]
 for bid in order:
  block=next(b for b in audit['blocks'] if bid in b['block_ids']);start=int(block['offset'],16);old=source[start:int(block['end_exclusive'],16)];rel=[int(v,16) for v in block['relative_offsets']];payload=bytearray(old);rr=rel[:];expected={};original_indexes=[]
  for row in sorted([r for r in allrows.values() if r['block_id']==bid],key=lambda r:r['string_id']):
   idx=row['string_id'];s,e=position(old,rel,idx);raw=old[s:e];en=decode(raw,True);key=row['id'];text=row['french']
   if key in base:
    assert en==row['english'] and raw.hex()==row['source_hex'];laid=row['french_in_game']
   else:
    assert re.findall(r'<[0-9A-F]{2}>',en)==re.findall(r'<[0-9A-F]{2}>',text),(key,'markers');assert re.findall(r'x[1-5]',en)==re.findall(r'x[1-5]',text),(key,'inline');dw={int(k,16):v for k,v in approved.get(key,{}).get('widths',{}).items()};laid=text;assert '\n' not in laid and len(encode_fr(laid))<=45 and visible_width(laid,font)<=192,(key,'fixed one-line menu/action contract')
    if idx in catalogs.get(bid,[]):assert len(encode_fr(laid))<=31 and not any(v<0x10 or 0x21<=v<=0x2a for v in encode_fr(laid)),key
    ww=[visible_width(l,font,dynamic_widths=dw) for l in laid.split('\n')];assert max(ww)<=216,(key,ww);widths+=ww;row.update(english=en,source_hex=raw.hex(),source_offset=hex(start+s),french_in_game=laid)
   encoded=encode_fr(laid);assert encode_fr(decode_fr(encoded))==encoded;os,oe=position(payload,rr,idx);delta=len(encoded)-(oe-os);payload[os:oe]=encoded;expected[idx]=encoded
   for n,v in enumerate(rr):
    assert not os<v<oe
    if v>os:rr[n]+=delta
    payload[2*n:2*n+2]=rr[n].to_bytes(2,'little')
  prepared.append({'block':block,'source':start,'old':old,'payload':payload,'relative':rr,'expected':expected})
 out,storage=store_blocks(source,prepared);out=patch_font(out)[0];allowed=[(0xffdc,0xffe0)];reports=[]
 for item in prepared:
  b=item['block'];d=item['destination'];allowed.append((d,d+item['storage_length']));allowed.extend((int(s,16),int(s,16)+3) for s in b['directory_slots']);reports.append({'block_ids':b['block_ids'],'source':hex(item['source']),'destination':hex(d),'storage':item['allocation_kind'],'old_size':len(item['old']),'new_size':len(item['payload']),'old_relative_offsets':b['relative_offsets'],'new_relative_offsets':item['relative'],'translated':len(item['expected'])})
 out,startup=patch_startup(out);allowed.extend((int(e['offset'],16),int(e['offset'],16)+e['length']) for e in startup);out,ui=patch_calendar_ui(out);allowed.append((int(ui['offset'],16),int(ui['offset'],16)+ui['length']));out,calendar=patch_calendar_formats(out);allowed.extend((int(s,16),int(e,16)) for s,e in calendar['changed_spans']);out=checksum(out)
 for edit in fontedits:
  c=int(edit['code'],16);allowed.extend([(FONT+c*32,FONT+(c+1)*32),(WIDTHS+c,WIDTHS+c+1)])
 assert all(any(s<=i<e for s,e in allowed) for i,(x,y) in enumerate(zip(source,out)) if x!=y),'out of scope write'
 # Compare to the exact published V53 outside old/new text storage and
 # explicitly authorized font/startup/calendar/checksum spans.
 preservation_spans=list(allowed)
 preservation_spans.extend((item['source'],item['source']+len(item['old'])) for item in prepared)
 prior_blocks=json.loads((ROOT/'verification/build_report_lot47_checkpoint.json').read_text())['blocks']
 preservation_spans.extend((int(b['destination'],16),int(b['destination'],16)+b['new_size']) for b in prior_blocks)
 assert all(any(s<=i<e for s,e in preservation_spans) for i,(x,y) in enumerate(zip(baseline,out)) if x!=y),'V53 out-of-scope bytes changed'
 aliases=json.loads((ROOT/'verification/aliases_lot48.json').read_text());canonical={k:r for k,r in new.items() if k not in aliases and r['english']!=r['french'] and r['english'] not in {v['english'] for v in base.values()}};assert len({r['english'] for r in canonical.values()})==len(canonical),'add a shared-source alias before counting';
 def identity(text):
  text=re.sub(r'x[1-5]','',text);text=re.sub(r'<0[4-7]>',' VAR ',text);text=re.sub(r'<[0-9A-F]{2}>','',text);return ' '.join(text.split())
 identities={}
 for key,row in canonical.items():
  ident=identity(row['english']);assert ident not in identities,('shared formatted source requires alias',key,identities.get(ident));identities[ident]=key
 if a.require_complete_lot:assert len(canonical)==400,('incomplete canonical lot',len(canonical))
 tested=0;deferred=[]
 for item in ([] if a.prepare_only else prepared):
  for idx in range(1,256):
   try:s,e=position(item['old'],[int(v,16) for v in item['block']['relative_offsets']],idx)
   except ValueError:break
   expected=item['expected'].get(idx,item['old'][s:e])
   for alias in item['block']['block_ids']:
    cpu=CPU(out);assert cpu.load_block(alias)==item['destination']-0x200000;cpu.select(idx);assert cpu.string()==expected,(alias,idx);tested+=1
   if idx not in item['expected']:deferred.append(f'B{item["block"]["block_ids"][0]:03}-S{idx:03}')
 patch=make_ips(source,out);assert apply_ips(source,patch)==out;(ROOT/'Tengai_Makyou_Zero_FR_LOT48_CHECKPOINT.ips').write_bytes(patch);a.rom_out.write_bytes(out);(ROOT/'traduction/traduction_v54.json').write_text(json.dumps(list(allrows.values()),ensure_ascii=False,indent=2)+'\n')
 report={'version':'V54_CHECKPOINT','release_status':'incomplete_lot48_not_published','input_files_sha256':input_hashes,'source_sha256':hashlib.sha256(source).hexdigest(),'output_sha256':hashlib.sha256(out).hexdigest(),'baseline_v53_sha256':hashlib.sha256(baseline).hexdigest(),'baseline_rows_preserved':len(base),'v53_outside_authorized_spans_preserved':True,'new_bounded_occurrences':len(new),'new_distinct_bounded_sources':len(canonical),'native_month_sources':0,'new_distinct_texts_total_prepared':len(canonical),'runtime_validation':'pending','engine_checks':tested,'native_lookup_validation':'pending' if a.prepare_only else 'passed','ips_roundtrip':True,'ips_sha256':hashlib.sha256(patch).hexdigest(),'calendar_formats':calendar,'calendar_ui':ui,'startup_edits':startup,'blocks':reports,'deferred_source_entries':deferred,**storage};(ROOT/'verification/build_report_lot48_checkpoint.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['blocks','deferred_source_entries','calendar_formats','calendar_ui','startup_edits']},indent=2))
if __name__=='__main__':main()
