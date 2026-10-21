#!/usr/bin/env python3
"""Native Tengai Makyou Zero English font, exact pinned ROM layout.
16x16 monochrome glyphs, 32 bytes each; two horizontally adjacent bytes/row.
Font CPU DF5200 and advances DF7200, normal SPC7110 D-window maps file 2F....
French glyphs already present; only Y/y with diaeresis replace A/a macron.
"""
import json,re,unicodedata
from pathlib import Path
from extract import MAP,GUESSES

FONT=0x2F5200
WIDTHS=0x2F7200
ACCENTS={
 'À':0x72,'Â':0x73,'Ä':0x70,'É':0x99,'È':0x9A,'Ê':0x9B,'Ë':0x98,
 'Î':0xB3,'Ï':0xB0,'Ô':0x7B,'Ö':0x78,'Ù':0x92,'Û':0x93,'Ü':0x90,
 'Ç':0xC3,'Ÿ':0x75,
 'à':0x82,'â':0x83,'ä':0x80,'é':0xA9,'è':0xAA,'ê':0xAB,'ë':0xA8,
 'î':0xBB,'ï':0xB8,'ô':0x8B,'ö':0x88,'ù':0xA2,'û':0xA3,'ü':0xA0,
 'ç':0xC4,'ÿ':0x85,
 'Œ':0x9F,'œ':0xAF,'Æ':0x7F,'æ':0x8F,
}
CHAR_TO_BYTE={**{v:k for k,v in MAP.items()},**{v:k for k,v in GUESSES.items()},
              **ACCENTS,':':0x29,';':0x2A,'"':0x11}
ALIASES={'’':"'",'‘':"'",'«':'"','»':'"','–':'-','—':'-','…':'...'}

def patch_font(source):
    out=bytearray(source);report=[]
    for char,code,base,dots,row in [('Ÿ',0x75,0x48,0x48,1),('ÿ',0x85,0x68,0x90,4)]:
        glyph=bytearray(source[FONT+base*32:FONT+(base+1)*32])
        assert glyph[row*2:row*2+2]==b'\0\0'
        glyph[row*2]=dots
        start=FONT+code*32;old=source[start:start+32]
        out[start:start+32]=glyph;out[WIDTHS+code]=source[WIDTHS+base]
        report.append({'character':char,'code':f'{code:02X}','replaces':'Ā' if char=='Ÿ' else 'ā',
                       'base_character':'Y' if char=='Ÿ' else 'y','offset':hex(start),
                       'old_hex':old.hex(),'new_hex':glyph.hex(),
                       'advance':source[WIDTHS+base],'body_preserved':True})
    return bytes(out),report

def encode_fr(text):
    text=unicodedata.normalize('NFC',text)
    for old,new in ALIASES.items():text=text.replace(old,new)
    out=bytearray();i=0
    while i<len(text):
        if text[i]=='<':
            token=text[i:i+4]
            if not re.fullmatch(r'<[0-9A-F]{2}>',token):raise ValueError('Malformed command')
            out.append(int(token[1:3],16));i+=4
        elif text[i]=='\n':out.append(1);i+=1
        else:
            if text[i] not in CHAR_TO_BYTE:raise ValueError(f'Unsupported character: {text[i]!r}')
            out.append(CHAR_TO_BYTE[text[i]]);i+=1
    return bytes(out)

def decode_fr(raw):
    inv={v:k for k,v in CHAR_TO_BYTE.items()}
    return ''.join('\n' if b==1 else inv.get(b,f'<{b:02X}>') for b in raw)

def visible_width(text,rom,dynamic_widths=None):
    # 0A shares the 08/09 mode-flag handler: only flag bits change,
    # no cursor writes (verification/text_modes_lot46.json). Glyphs remain
    # measured individually; no claim of music synchronization is made.
    # The native 09..08 marker pair surrounding a heart is preserved and
    # assigned zero horizontal advance; effects are not interpreted here.
    # 0E is retained verbatim as a nonprinting flow command; its timing is
    # not reinterpreted by the inserter. 0C/0D are scene/pause markers. 04 is a dynamic name: reserve a conservative
    # 96 pixels rather than counting it as an invisible character. Explicit
    # per-entry contracts can override 04 or admit 05..07; no implicit bound
    # is assigned to these other substitution slots.
    dynamic_widths={} if dynamic_widths is None else dynamic_widths
    if any(k not in (4,5,6,7) or not isinstance(v,int) or v<0 for k,v in dynamic_widths.items()):raise ValueError('Invalid dynamic width contract')
    raw=encode_fr(text)
    zero={1,8,9,0x0A,0x0B,0x0C,0x0D,0x0E}
    if any(b<0x10 and b not in zero|{4}|set(dynamic_widths) for b in raw):raise ValueError('Unresolved layout command')
    return sum(dynamic_widths[b] if b in dynamic_widths else 96 if b==4 else rom[WIDTHS+b] for b in raw if b not in zero)

def layout_fr(text,rom,limit=216,dynamic_widths=None):
    # French punctuation stays with its preceding word. NBSP exists only
    # during layout, then becomes the native space glyph in encoded output.
    text=re.sub(r' +([!?;:])',lambda m:'\u00a0'+m[1],text)
    lines=[]
    for paragraph in text.split('\n'):
        line=''
        for word in paragraph.split(' '):
            candidate=(line+' '+word if line else word)
            measured=candidate.replace('\u00a0',' ')
            if visible_width(measured,rom,dynamic_widths)>limit and line:
                lines.append(line.replace('\u00a0',' '));line=word
            else:line=candidate
            if visible_width(line.replace('\u00a0',' '),rom,dynamic_widths)>limit:raise ValueError('Unbreakable word too wide')
        lines.append(line.replace('\u00a0',' '))
    result='\n'.join(lines)
    assert all(visible_width(s,rom,dynamic_widths)<=limit for s in result.split('\n'))
    return result

def atlas(rom,path):
    from PIL import Image,ImageDraw
    pairs=['Aa','Àà','Ââ','Ää','Ee','Éé','Èè','Êê','Ëë','Ii','Îî','Ïï',
           'Oo','Ôô','Öö','Uu','Ùù','Ûû','Üü','Cc','Çç','Yy','Ÿÿ','Œœ','Ææ']
    scale=4;cellw=128;cellh=96
    image=Image.new('RGB',(cellw*5,cellh*5),'#141c27');draw=ImageDraw.Draw(image)
    for n,pair in enumerate(pairs):
        x=n%5*cellw;y=n//5*cellh
        # ASCII labels make the diagram font-independent; native glyphs below.
        codes=[CHAR_TO_BYTE[c] for c in pair]
        draw.text((x+5,y+4),' / '.join(f'{v:02X}' for v in codes),fill='#94a5b9')
        for j,code in enumerate(codes):
            raw=rom[FONT+code*32:FONT+(code+1)*32]
            for row in range(16):
                for col in range(16):
                    if raw[row*2+col//8]>>(7-col%8)&1:
                        xx=x+5+j*60+col*scale;yy=y+20+row*scale
                        draw.rectangle((xx,yy,xx+scale-1,yy+scale-1),fill='#ffffff')
        if pair=='Ÿÿ':draw.rectangle((x,y,x+cellw-1,y+cellh-1),outline='#63d8b1',width=2)
    image.save(path)
