#!/usr/bin/env python3
"""Recover known lot50 sources after workspace loss;not a release.

The303 former item display variants are pending recovery and are not silently
counted, replaced or claimed validated. Published V55 is the pinned baseline.
"""
import argparse,hashlib,json
from pathlib import Path
from cpu65816_probe import CPU
from french_font import encode_fr
from insert import apply_ips,make_ips
from menu_graphics_lot49 import raster
from build_lot46_checkpoint import checksum
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--rom-out',type=Path,required=True);p.add_argument('--ips-out',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args();source=a.source.read_bytes();assert sha(source)=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e';baseline=apply_ips(source,(ROOT/'Tengai_Makyou_Zero_FR_V55.ips').read_bytes());assert sha(baseline)=='2631d90bd0f2b0ed927055143117525517d06f15f29511439d6e76acdc371e4c';out=bytearray(baseline);spans=[];checks=[]
 def put(st,data):
  end=st+len(data);assert not any(st<z and end>s for s,z in spans),(hex(st),spans);out[st:end]=data;spans.append((st,end))
 weak=json.loads((ROOT/'traduction/weakness_lot50_fr.json').read_text());payload=b'\x02\x00'+b''.join(encode_fr(e['french'])+b'\0' for e in weak);assert len(payload)==93;assert baseline[0x6c9510:0x6c9580]==bytes(112);put(0x6c9510,payload);put(0xc9881,(0x4c9510).to_bytes(3,'little'))
 c=CPU(baseline);c.load_block(43);prior=[]
 for i in range(1,8):c.select(i);prior.append(c.string())
 assert prior[-1]==encode_fr('All');payload=b'\x02\x00'+b''.join(s+b'\0'for s in prior[:6])+encode_fr('Tous')+b'\0';assert len(payload)==88;assert baseline[0x6c9590:0x6c9600]==bytes(112);put(0x6c9590,payload);put(0xc987e,(0x4c9590).to_bytes(3,'little'))
 for file in ['block42_graphics_lot50_fr.json','native_prior_variants_lot50_fr.json','shop_graphics_lot50_fr.json']:
  for e in json.loads((ROOT/'traduction'/file).read_text()):
   for part in e.get('strips',[e]):
    st=int(part['offset'],16);n=part['tiles']*16;assert baseline[st:st+n].hex()==part['source_hex'],e['id'];data,px=raster(baseline,part['french'],part['tiles']);assert px<=part['tiles']*8;put(st,data);checks.append(dict(id=e['id'],offset=hex(st),tiles=part['tiles'],pixels=px))
 out=checksum(out);spans.append((0xffdc,0xffe0));assert len(out)==len(baseline);assert all(any(s<=i<z for s,z in spans)for i,(x,y)in enumerate(zip(out,baseline))if x!=y)
 for e in weak:
  c=CPU(out);c.load_block(44);c.select(int(e['id'][-3:]));assert c.string()==encode_fr(e['french'])
 for i in range(1,8):
  c=CPU(out);c.load_block(43);c.select(i);assert c.string()==(prior[i-1]if i<7 else encode_fr('Tous'))
 for i in range(1,8):
  c=CPU(out);c.load_block(42);c.select(i);d=CPU(baseline);d.load_block(42);d.select(i);assert c.string()==d.string()
 storage=json.loads((ROOT/'verification/build_report_lot49_checkpoint.json').read_text())['blocks'];preserved=0
 for b in storage:
  st=int(b['destination'],16);n=b['new_size'];assert out[st:st+n]==baseline[st:st+n],b['block_ids'];preserved+=b['translated']
 assert preserved==6769,preserved
 patch=make_ips(source,out);assert apply_ips(source,patch)==out;a.rom_out.write_bytes(out);a.ips_out.write_bytes(patch)
 report=dict(status='Recovery research candidate;not a completed lot or validated release',source_sha256=sha(source),baseline_sha256=sha(baseline),output_sha256=sha(out),ips_sha256=sha(patch),prior_stored_bounded_occurrences_byte_preserved=preserved,prior_block43_native_reads=6,new_bounded_native_reads=9,prior_element_variant_native_reads=4,block42_glyph_lists_native_preserved=7,graphics_bounds=checks,authorized_spans=spans,ips_roundtrip=True,new_distinct_sources_prepared=14,former303_item_variants='Pending recovery;not included in this candidate',runtime_validation='pending',visual_review='pending')
 a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('Recovery candidate built;fresh runtime pending',sha(out))
if __name__=='__main__':main()
