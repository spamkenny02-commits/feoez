"""Localized inline month/ordinal tables and exact two-digit month reader repair.
No natural event/clock claim: valid input domains are checked separately.
"""
import json
from pathlib import Path
from french_font import encode_fr
ROOT=Path(__file__).resolve().parents[1]
MONTHS=0x6f1f00
ORDINALS=0x6f1e70
MONTH_TWO_DIGIT_LOAD=0x6d3c15
ORIGINAL_MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December']
def patch_calendar_formats(source):
 out=bytearray(source);entries=json.loads((ROOT/'traduction/calendar_months_lot47_fr.json').read_text());assert [e['english'] for e in entries]==ORIGINAL_MONTHS
 spans=[]
 for i,e in enumerate(entries):
  at=MONTHS+16*i;old=encode_fr(e['english'])+b'\0';assert source[at:at+len(old)]==old and source[at+len(old):at+16]==b'\0'*(16-len(old));new=encode_fr(e['french'])+b'\0';assert len(new)<=16;out[at:at+16]=new.ljust(16,b'\0');spans.append((at,at+16))
 # Only the two-digit arm changes. Its second decimal digit selects Oct–Dec.
 assert source[MONTH_TWO_DIGIT_LOAD:MONTH_TWO_DIGIT_LOAD+6]==bytes.fromhex('b9 aa 32 38 e9 18')
 out[MONTH_TWO_DIGIT_LOAD+1]=0xab;spans.append((MONTH_TWO_DIGIT_LOAD+1,MONTH_TWO_DIGIT_LOAD+2))
 suffixes=[]
 for value in range(1,32):
  english='th' if 10<=value%100<=20 else {1:'st',2:'nd',3:'rd'}.get(value%10,'th');at=ORDINALS+2*(value-1);assert source[at:at+2]==encode_fr(english)
  french='er' if value==1 else 'e ';out[at:at+2]=encode_fr(french);suffixes.append({'value':value,'english':english,'french':french})
 spans.append((ORDINALS,ORDINALS+62))
 return bytes(out),{'months':entries,'ordinal_forms':suffixes,'counting':'12 month source strings; ordinal-format variants and the code repair are not counted as new texts.','changed_spans':[[hex(s),hex(e)] for s,e in spans],'month_bug':'Original decimal10/11/12 all read November; two-digit arm now reads its second digit.','scope':'Leaf formatting under valid calendar domains only. Producer binding, actual dates and event timing require separate validation.'}
