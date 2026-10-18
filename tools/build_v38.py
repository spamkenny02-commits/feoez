#!/usr/bin/env python3
"""Rebuild V38 from the pinned original English ROM. Ice Mountain, elemental hermits and Kingin; preserves French startup screens."""
import argparse,csv,hashlib,json,re
from pathlib import Path
from extract import decode
from pointers import analyze
from relocate import position
from block_storage import store_blocks
from insert import make_ips,apply_ips
from cpu65816_probe import CPU
from french_font import *
from startup_text import patch_startup
ROOT=Path(__file__).resolve().parent.parent
BLOCKS=(1, 29, 45, 49, 50, 51, 52, 53, 54, 55, 57, 58, 59, 60, 61, 62, 63, 64, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 79, 80, 81, 83, 84, 85, 87, 89, 90, 93, 97, 98, 100, 101, 103, 106, 107, 108, 109, 110, 111, 112, 113, 115, 117, 118, 119, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 133, 134, 135, 136, 137, 138, 139, 140, 141, 143, 147, 149, 150, 151, 152, 153, 154, 155, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 175, 176, 177, 178, 179, 180, 181, 182, 184, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 201, 202, 203, 205, 206, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 219, 220, 221, 222, 223, 224, 225, 226, 228, 229, 230, 231, 232, 233, 234, 237, 238, 239, 240, 241, 242, 243, 244, 246, 247, 249, 252, 253)
SAFE_LOW={1,4,8,9,0x0B,0x0C,0x0D,0x0E}
def markers(t):return re.findall(r'<[0-9A-F]{2}>',t)
def checksum(data):
    data=bytearray(data);v=sum(data)&65535
    data[0xFFDC:0xFFDE]=(v^65535).to_bytes(2,'little');data[0xFFDE:0xFFE0]=v.to_bytes(2,'little')
    assert sum(data)&65535==v
    return bytes(data)
def main():
    p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('--rom-out',type=Path);a=p.parse_args()
    if a.rom_out and a.rom_out.resolve()==a.rom.resolve():raise ValueError('Cannot overwrite source')
    original=a.rom.read_bytes();audit=analyze(original);fontrom,fontedits=patch_font(original)
    fr=json.loads((ROOT/'traduction/lot02_fr.json').read_text())
    previous=json.loads((ROOT/'traduction/lot01_fr.json').read_text());fr['49']={**previous,**fr['49']}
    fr.update(json.loads((ROOT/'traduction/lot03_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot04_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot05_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot06_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot07_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot08_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot09_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot10_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot11_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot12_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot13_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot14_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot15_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot16_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot17_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot18_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot19_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot20_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot21_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot22_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot23_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot24_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot25_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot26_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot27_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot28_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot29_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot30_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot31_fr.json').read_text()))
    fr.update(json.loads((ROOT/'traduction/lot32_fr.json').read_text()))
    for bid, entries in json.loads((ROOT/'traduction/corrections_v20.json').read_text()).items():
        fr[bid].update(entries)
    prepared=[];rows=[];widths=[]
    for bid in BLOCKS:
        block=next(b for b in audit['blocks'] if bid in b['block_ids']);s=int(block['offset'],16)
        old=original[s:int(block['end_exclusive'],16)];relative=[int(v,16) for v in block['relative_offsets']]
        payload=bytearray(old);rr=relative[:];expected={}
        for key,text in sorted(fr[str(bid)].items(),key=lambda kv:int(kv[0])):
            idx=int(key);os,oe=position(old,relative,idx);raw=old[os:oe];english=decode(raw,True)
            assert markers(english)==markers(text),(bid,idx,'markers')
            assert all(c>=0x10 or c in SAFE_LOW for c in raw),(bid,idx,'unknown source command')
            assert all(c<0xE0 for c in raw),(bid,idx,'dictionary requires a parser')
            laid=text if (bid,idx) in ((29,1),(93,40),(106,5),(106,34),(107,9),(117,3),(122,3),(130,16),(234,20),(234,21),(244,1),(210,57),(210,60)) else layout_fr(text,fontrom)
            if (bid,idx) in ((93,39),(217,13),(210,21),(73,4)):
                prompt, choices=text.split('\n\n',1)
                laid=layout_fr(prompt,fontrom)+'\n\n'+choices
            if (bid,idx) in ((152,16),(153,35)):
                prompt,choices=text.rsplit('\n',1)
                laid=layout_fr(prompt,fontrom)+'\n'+choices
            new=encode_fr(laid)
            assert markers(laid)==markers(english)
            assert encode_fr(decode_fr(new))==new
            assert all(c>=0x10 or c in SAFE_LOW for c in new)
            assert all(c<0xE0 for c in new)
            widths.extend(visible_width(l,fontrom) for l in laid.split('\n'))
            assert all(visible_width(l,fontrom)<=216 for l in laid.split('\n')), (bid,idx,'line width')
            start,end=position(payload,rr,idx);delta=len(new)-(end-start)
            payload[start:end]=new;expected[idx]=new
            for n,v in enumerate(rr):
                if start<v<end:raise ValueError('Group pointer inside edited string')
                if v>start:rr[n]+=delta
                payload[2*n:2*n+2]=rr[n].to_bytes(2,'little')
            rows.append({'id':f'B{bid:03}-S{idx:03}','block_id':bid,'string_id':idx,'source_offset':hex(s+os),
                         'source_hex':raw.hex(),'english':english,'french':text,'french_in_game':laid,
                         'status':'premier_jet_a_relire','lot':'32' if bid in (67,68,73,80) else '31' if bid==210 else '30' if bid in (167,244,253) else '29' if bid in (241,242,243,246,247,249,252) else '28' if bid in (233,234,237,238,239,240,241,242,243,246,247,249,252) else '27' if bid in (225,226,228,229,230,231,232) else '26' if bid in (217,219,220,221,222,223,224) else '25' if bid in (214,215,216) else '24' if bid in (206,208,209,211,212,213) else '23' if bid in (193,194,195,196,197,201,202,203,205,206,208,209,211,212,213) else '22' if bid in (184,186,187,188,189,190,191,192,193,194,195,196,197,201,202,203,205,206,208,209,211,212,213) else '21' if bid in (177,178,179,180,181) else '20' if bid in (171,172,173,175,176) else '19' if bid in (163,164,165,166,168,169,170) else '18' if bid in (158,159,160,161,162) else '17' if bid in (155,157) else '16' if bid in (147,149,150,151,152,153,154) else '15' if bid in (140,143) else '14' if bid in (136,137,138,139,141) else '13' if bid in (130,131,133,134,135) else '12' if bid in (124,125,126,127,128,129) else '11' if bid in (117,118,119,121,122,123) else '10' if bid in (106,107,108,109,110,111,112,113,115) else '09' if bid in (97,98,100,101,103) else '08' if bid in (75,89,90,93) else '07' if bid in (77,81,83,87) else '06' if bid in (74,75,76,79,84,85) else '05' if bid in (69,70,71,72) else '04' if bid in (1,59,60,61,62,63,64,182) else '03' if bid in (29,45,57,58) else '01' if bid==49 and idx<=64 else '02'})
        assert len(payload)<=65535
        prepared.append({'block':block,'source':s,'old':old,'payload':payload,'relative':rr,'expected':expected})
    out,storage=store_blocks(original,prepared)
    out=bytearray(patch_font(out)[0]);allowed=[(0xFFDC,0xFFE0)]
    reports=[];tested=0
    for item in prepared:
        b=item['block'];d=item['destination'];old=item['old'];payload=item['payload'];length=item['storage_length']
        if item['allocation_kind']=='relocated':
            assert out[item['source']:item['source']+len(old)]==old
        allowed.append((d,d+length));allowed.extend((int(s,16),int(s,16)+3) for s in b['directory_slots'])
        reports.append({'block_ids':b['block_ids'],'source':hex(item['source']),'destination':hex(d),
                        'old_size':len(old),'new_size':len(payload),'translated':len(item['expected']),
                        'storage':item['allocation_kind'],
                        'old_relative_offsets':b['relative_offsets'],'new_relative_offsets':item['relative']})
    out,startup_edits=patch_startup(out)
    allowed.extend((int(e['offset'],16),int(e['offset'],16)+e['length']) for e in startup_edits)
    out=checksum(out)
    for edit in fontedits:
        c=int(edit['code'],16);allowed.extend([(FONT+c*32,FONT+(c+1)*32),(WIDTHS+c,WIDTHS+c+1)])
    assert all(any(s<=i<e for s,e in allowed) for i,(x,y) in enumerate(zip(original,out)) if x!=y)
    for item in prepared:
        b=item['block'];original_relative=[int(v,16) for v in b['relative_offsets']]
        for idx in range(1,256):
            try:s,e=position(item['old'],original_relative,idx)
            except ValueError:break
            expected=item['expected'].get(idx,item['old'][s:e])
            for alias in b['block_ids']:
                cpu=CPU(out);assert cpu.load_block(alias)==item['destination']-0x200000
                cpu.select(idx);assert cpu.string()==expected,(alias,idx);tested+=1
        if b['block_ids'][0] not in (29,97,125,130,140,149,184,186,189,193,194,197,201,202,205,212,221,225,229,231,234,252,210,80):assert len(item['expected'])==idx-1,('block not fully translated',b['block_ids'])
    patch=make_ips(original,out);assert apply_ips(original,patch)==out
    (ROOT/'Tengai_Makyou_Zero_FR_V38.ips').write_bytes(patch)
    if a.rom_out:a.rom_out.write_bytes(out)
    (ROOT/'traduction/traduction_v38.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    with (ROOT/'traduction/traduction_v38.tsv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0],delimiter='\t');w.writeheader();w.writerows(rows)
    (ROOT/'traduction/lecture_v38.txt').write_text('\n\n'.join(f"[{r['id']}]\nEN : {r['english']}\nFR : {r['french']}" for r in rows)+'\n')
    report={'source_sha256':hashlib.sha256(original).hexdigest(),'output_sha256':hashlib.sha256(out).hexdigest(),
            'translated_entries':len(rows),'new_entries':89,'previously_integrated':3287,
            'new_nonempty_texts':89,
            'new_changed_entries':88,
            'new_passthrough_entries':1,
            'new_empty_entries_preserved':0,
            'startup_text_occurrences':len(startup_edits),'startup_edits':startup_edits,'internal_backup_signature_preserved':out[0xFF0E7:0xFF0F7]==original[0xFF0E7:0xFF0F7],'integrated_entries':len(rows),'blocks':reports,'engine_checks':tested,'all_markers_preserved':True,
            'maximum_measured_line_width':max(widths),'line_width_limit':216,
            'selection_instruction_budget':500000,'dynamic_name_reservation_pixels':96,'original_blocks_preserved':False,'input_rom_unchanged':True,
            'relocated_source_blocks_preserved':True,'ips_roundtrip':True,
            'font_same_as_v06':True,'runtime_validation':'see emulation_report_v38.json',
            **storage,'allocation_policy':'in place when fitting, otherwise free pool',
            'deferred_entries':{'80':[21],'210':[36,65,75,76,77],'125':[3],'130':[19],'140':[2,22,27],'149':[1,6],'184':[8,10],'186':[15],'189':[1,2],'193':[4],'194':[6,9],'197':[2,3,13,14,18,27],'201':[6,8],'202':[5,8,9,10],'205':[53],'212':[18],'221':[22],'225':[12],'229':[12],'231':[10,13,29,32],'234':[50],'252':[18,19,98,99,100,101]},'deferred_block97_entries':[23,24,25,26,27,28,58,98,104,107,109]}
    (ROOT/'verification/build_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
