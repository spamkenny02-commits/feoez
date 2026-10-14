#!/usr/bin/env python3
"""Binary/font invariants and meaningful encoder/layout regression checks."""
import argparse,json,unicodedata
from pathlib import Path
from pointers import analyze
from french_font import *
p=argparse.ArgumentParser();p.add_argument('rom',type=Path);a=p.parse_args()
original=a.rom.read_bytes();analyze(original);rom,edits=patch_font(original);checks=[]
def check(name,passed):
    if not passed:raise AssertionError(name)
    checks.append(name)
alphabet='àâäéèêëîïôöùûüÿçÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇœŒæÆ'
check('All 32 French accented letters and four ligatures round-trip',decode_fr(encode_fr(alphabet))==alphabet)
check('Combining Unicode input normalized to composed accents',encode_fr(unicodedata.normalize('NFD',alphabet))==encode_fr(alphabet))
check('No accented code collides with commands or dictionary',all(0x20<=c<0xE0 for c in ACCENTS.values()))
check('Each accented letter has its own byte',len(set(ACCENTS.values()))==len(ACCENTS))
for e in edits:
    c=int(e['code'],16);base=0x48 if c==0x75 else 0x68;row=1 if c==0x75 else 4
    new=bytearray(rom[FONT+c*32:FONT+(c+1)*32]);new[row*2:row*2+2]=b'\0\0'
    check(e['character']+' preserves every Y/y body pixel',bytes(new)==original[FONT+base*32:FONT+(base+1)*32])
    check(e['character']+' has exactly two new dots',rom[FONT+c*32+row*2].bit_count()==2)
    check(e['character']+' uses the base advance',rom[WIDTHS+c]==original[WIDTHS+base])
for c in range(256):
    if c not in (0x75,0x85):
        assert rom[FONT+c*32:FONT+(c+1)*32]==original[FONT+c*32:FONT+(c+1)*32]
        assert rom[WIDTHS+c]==original[WIDTHS+c]
check('All 254 other glyphs and advances unchanged',True)
allowed=[(FONT+0x75*32,FONT+0x76*32),(FONT+0x85*32,FONT+0x86*32),
         (WIDTHS+0x75,WIDTHS+0x76),(WIDTHS+0x85,WIDTHS+0x86)]
check('No data outside two glyphs/advances changed by font builder',
      all(any(s<=i<e for s,e in allowed) for i,(x,y) in enumerate(zip(original,rom)) if x!=y))
sentence='<0C>Été à Noël : cœur, naïf, français !<0D> Où est Ÿ ?'
laid=layout_fr(sentence,rom,limit=100)
check('Layout preserves accents, punctuation and pause order',laid.replace('\n',' ')==sentence)
check('Layout uses the real advances, including wide Œ',all(visible_width(s,rom)<=100 for s in laid.split('\n')))
check('French exclamation/question cannot become an orphan line',all(s.strip() not in ('!','?') for s in laid.split('\n')))
try:encode_fr('😀')
except ValueError:check('Unsupported character fails instead of disappearing',True)
else:raise AssertionError('Unsupported character silently accepted')
report={'passed':len(checks),'checks':checks,'glyphs_unchanged':254,'french_accented_letters':32,'ligatures':4,
        'scope':'Font binary, encoding and pixel layout. Emulator evidence is separate.'}
(Path(__file__).resolve().parent.parent/'verification/font_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
