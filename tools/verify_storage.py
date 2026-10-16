#!/usr/bin/env python3
"""Exercise storage safety using the pinned ROM and real directory aliases."""
import argparse,copy,hashlib,json
from pathlib import Path
from block_storage import store_blocks
from pointers import analyze,FREE_START,file_to_cpu
p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('--version',choices=['V14','V15','V16','V17','V18','V19','V20','V21','V22','V23','V24','V25','V26','V27','V28','V29'],default='V14');p.add_argument('--built-rom',type=Path);p.add_argument('--build-report',type=Path);a=p.parse_args()
if bool(a.built_rom)!=bool(a.build_report):p.error('Provide both --built-rom and --build-report')
rom=a.rom.read_bytes();before=hashlib.sha256(rom).hexdigest();audit=analyze(rom);checks=[]
def item(bid,payload):
    b=next(b for b in audit['blocks'] if bid in b['block_ids']);assert b['groups']==1
    s=int(b['offset'],16)
    return {'block':copy.deepcopy(b),'source':s,'old':rom[s:int(b['end_exclusive'],16)],'payload':bytearray(payload),'relative':[2]}
def rejects(name,items,source=rom):
    try:store_blocks(source,items)
    except ValueError:checks.append(name)
    else:raise AssertionError(name)
small=item(98,b'\x02\0Okay\0');grow=item(81,b'\x02\0'+b'A'*120+b'\0')
out,r=store_blocks(rom,[small,grow]);assert small['destination']==small['source'];assert grow['destination']==FREE_START
assert out[small['source']:small['source']+len(small['payload'])]==small['payload'];checks.append('Fitting block uses its own audited span')
for s in grow['block']['directory_slots']:
    slot=int(s,16);assert out[slot:slot+3]==file_to_cpu(FREE_START).to_bytes(3,'little')
checks.append('Both aliases 81/82 move together')
assert out[grow['source']:grow['source']+len(grow['old'])]==grow['old'];checks.append('Relocated block keeps its English source bytes')
assert len(out)==len(rom) and r['in_place_blocks']==1 and r['relocated_blocks']==1;checks.append('ROM length and allocation counts are correct')
rejects('Overlapping source blocks rejected',[item(81,b'\x02\0A\0'),item(81,b'\x02\0B\0')])
rejects('Pool exhaustion rejected before output',[item(b,b'\x02\0'+b'A'*59997+b'\0') for b in (81,98,103)])
bad=item(81,b'\x02\0A\0');bad['relative']=[4];rejects('Invalid group target rejected',[bad])
bad=item(81,b'\x02\0A\0');bad['block']['directory_slots']=['0x100000'];rejects('Unrelated directory write rejected',[bad])
bad=item(81,b'\x02\0A\0');bad['old']=bytes(len(bad['old']));rejects('Unverified source bytes rejected',[bad])
bad=item(81,b'\x02\0A\0');bad['block']['directory_slots']=bad['block']['directory_slots'][:1];rejects('Missing alias rejected',[bad])
bad=item(81,b'\x02\0A\0');bad['block']['length']+=1;rejects('Unverified span length rejected',[bad])
busy=bytearray(rom);busy[FREE_START]=1;rejects('Occupied free pool rejected',[item(81,b'\x02\0A\0')],bytes(busy))
assert before==hashlib.sha256(a.rom.read_bytes()).hexdigest();checks.append('Input ROM on disk unchanged after successes and rejections')
if a.built_rom:
    from french_font import patch_font
    from build_v14 import checksum
    build=json.loads(a.build_report.read_text());actual=a.built_rom.read_bytes()
    assert hashlib.sha256(actual).hexdigest()==build['output_sha256']
    items=[]
    for entry in build['blocks']:
        block=next(b for b in audit['blocks'] if b['block_ids']==entry['block_ids'])
        source=int(block['offset'],16);destination=int(entry['destination'],16)
        items.append({'block':block,'source':source,'old':rom[source:int(block['end_exclusive'],16)],
                      'payload':bytearray(actual[destination:destination+entry['new_size']]),
                      'relative':entry['new_relative_offsets']})
    rebuilt,allocation=store_blocks(rom,items)
    assert checksum(patch_font(rebuilt)[0])==actual
    assert all(allocation[k]==build[k] for k in allocation)
    checks.append('All actual rebuilt blocks reproduce the tested ROM byte for byte with current allocator')
report={'source_sha256':before,'passed':len(checks),'checks':checks,'scope':'Allocation safety; actual rebuilt strings are exercised separately by native 65816 routines.'}
(Path(__file__).resolve().parent.parent/f'verification/storage_checks_{a.version.lower()}.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
