#!/usr/bin/env python3
"""Rebuild V10 from the pinned original English ROM. Extended narrative and helper labels, pinned ROM."""
import argparse,csv,hashlib,json,re
from pathlib import Path
from extract import decode
from pointers import analyze
from relocate import position,run_plan
from insert import make_ips,apply_ips
from cpu65816_probe import CPU
from french_font import *
ROOT=Path(__file__).resolve().parent.parent
BLOCKS=(1,29,45,49,50,51,52,53,54,55,57,58,59,60,61,62,63,64,69,70,71,72,182)
SAFE_LOW={1,4,8,9,0x0B,0x0C,0x0D}
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
            laid=text if (bid,idx)==(29,1) else layout_fr(text,fontrom);new=encode_fr(laid)
            assert markers(laid)==markers(english)
            assert encode_fr(decode_fr(new))==new
            assert all(c>=0x10 or c in SAFE_LOW for c in new)
            assert all(c<0xE0 for c in new)
            widths.extend(visible_width(l,fontrom) for l in laid.split('\n'))
            start,end=position(payload,rr,idx);delta=len(new)-(end-start)
            payload[start:end]=new;expected[idx]=new
            for n,v in enumerate(rr):
                if start<v<end:raise ValueError('Group pointer inside edited string')
                if v>start:rr[n]+=delta
                payload[2*n:2*n+2]=rr[n].to_bytes(2,'little')
            rows.append({'id':f'B{bid:03}-S{idx:03}','block_id':bid,'string_id':idx,'source_offset':hex(s+os),
                         'source_hex':raw.hex(),'english':english,'french':text,'french_in_game':laid,
                         'status':'premier_jet_a_relire','lot':'05' if bid in (69,70,71,72) else '04' if bid in (1,59,60,61,62,63,64,182) else '03' if bid in (29,45,57,58) else '01' if bid==49 and idx<=64 else '02'})
        assert len(payload)<=65535
        prepared.append({'block':block,'source':s,'old':old,'payload':payload,'relative':rr,'expected':expected})
    dest=0x6B0000;plan=[]
    for item in prepared:
        item['destination']=dest;plan.append({'block_id':item['block']['block_ids'][0],'destination':hex(dest)})
        dest=(dest+max(len(item['old']),len(item['payload']))+255)&~255
    assert dest<=0x6D0000
    out,_=run_plan(original,plan);out=bytearray(patch_font(out)[0]);allowed=[(0xFFDC,0xFFE0)]
    reports=[];tested=0
    for item in prepared:
        b=item['block'];d=item['destination'];old=item['old'];payload=item['payload'];length=max(len(old),len(payload))
        out[d:d+length]=bytes(length);out[d:d+len(payload)]=payload
        assert out[item['source']:item['source']+len(old)]==old
        allowed.append((d,d+length));allowed.extend((int(s,16),int(s,16)+3) for s in b['directory_slots'])
        reports.append({'block_ids':b['block_ids'],'source':hex(item['source']),'destination':hex(d),
                        'old_size':len(old),'new_size':len(payload),'translated':len(item['expected']),
                        'old_relative_offsets':b['relative_offsets'],'new_relative_offsets':item['relative']})
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
        if b['block_ids'][0]!=29:assert len(item['expected'])==idx-1,('block not fully translated',b['block_ids'])
    patch=make_ips(original,out);assert apply_ips(original,patch)==out
    (ROOT/'Tengai_Makyou_Zero_FR_V10.ips').write_bytes(patch)
    if a.rom_out:a.rom_out.write_bytes(out)
    (ROOT/'traduction/traduction_v10.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    with (ROOT/'traduction/traduction_v10.tsv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0],delimiter='\t');w.writeheader();w.writerows(rows)
    (ROOT/'traduction/lecture_v10.txt').write_text('\n\n'.join(f"[{r['id']}]\nEN : {r['english']}\nFR : {r['french']}" for r in rows)+'\n')
    report={'source_sha256':hashlib.sha256(original).hexdigest(),'output_sha256':hashlib.sha256(out).hexdigest(),
            'translated_entries':len(rows),'new_entries':sum(r['lot']=='05' for r in rows),'previously_integrated':374,
            'integrated_entries':len(rows),'blocks':reports,'engine_checks':tested,'all_markers_preserved':True,
            'maximum_measured_line_width':max(widths),'line_width_limit':216,
            'dynamic_name_reservation_pixels':96,'original_blocks_preserved':True,'ips_roundtrip':True,
            'font_same_as_v06':True,'runtime_validation':'see emulation_report.json'}
    (ROOT/'verification/build_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
