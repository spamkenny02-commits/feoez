"""Bounded native Almanac label stream, FE headers preserved byte for byte.
Seven sequential NUL-terminated strings, followed by another menu descriptor.
The 00 at ED53 is the first byte of that next descriptor, NOT a list terminator.
The stream fits its original span; no following data or code is moved.
"""
import json
from pathlib import Path
from french_font import encode_fr,visible_width,WIDTHS
START,END=0xecdb,0xed53
ENGLISH=['Biorhythm',' What day is it today?',' On this day in history:','Body','Wisdom','Feelings','Notable Days']
HEADERS=[bytes.fromhex(v) for v in ['fe020506','fe04120d','fe04170d','fe010803','fe010a04','fe010c05','fe020f08']]
ROOT=Path(__file__).resolve().parents[1]
def patch_calendar_ui(rom):
    original=b''.join(h+encode_fr(t)+b'\0' for h,t in zip(HEADERS,ENGLISH))
    assert len(original)==END-START and rom[START:END]==original
    entries=json.loads((ROOT/'traduction/calendar_ui_lot46_fr.json').read_text())
    assert [e['english'] for e in entries]==ENGLISH
    texts=[encode_fr(e['french']) for e in entries]
    used=sum(4+len(t)+1 for t in texts)
    assert used<=len(original)
    padding=len(original)-used
    # FE printing returns its source cursor to the menu interpreter. Pad a
    # string with spaces so the next descriptor remains aligned. Zero-filled
    # slack after the list would instead execute a spurious descriptor.
    padded=[e['french'] for e in entries]
    remaining=padding
    for index in (1,0,6,5,4,3,2):
        width=visible_width(padded[index],rom)
        limit=HEADERS[index][-1]*8
        assert width<=limit,(entries[index]['id'],width,limit)
        extra=min(remaining,(limit-width)//rom[WIDTHS+0x20])
        padded[index]+=' '*extra;remaining-=extra
    assert remaining==0,'No safe pixel space to preserve descriptor alignment'
    texts=[encode_fr(t) for t in padded]
    payload=b''.join(h+t+b'\0' for h,t in zip(HEADERS,texts))
    assert len(payload)==len(original)
    out=bytearray(rom);out[START:END]=payload
    assert out[:START]==rom[:START] and out[END:]==rom[END:]
    return bytes(out),{'offset':hex(START),'length':END-START,'used_bytes':len(payload),'slack_bytes':0,'padding_bytes_in_strings':padding,'rendered_labels':padded,'field_widths_pixels':[h[-1]*8 for h in HEADERS],'next_descriptor_offset':hex(END),'entries':entries,'headers_preserved':[h.hex() for h in HEADERS],'scope':'Sequential native label stream; display and placement require same-ROM Almanac test.'}
