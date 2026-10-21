"""Preserve original option-column anchors for V50 service prompts only.
Widths use the pinned native font; no selector code or previous entry is changed.
"""
import re
from french_font import layout_fr,visible_width,encode_fr,WIDTHS
# Number of fixed final option rows. Other lines keep normal 216px wrapping.
CHOICE_ROWS={(29,12):1,(29,17):2,(29,85):1,(29,98):1,(38,12):1,
 (40,102):1,(40,191):3,(40,214):1,(40,215):3,(41,6):1,(41,12):1,
 (66,6):2,(66,7):1,(66,9):1,(66,40):1,(66,119):1,(95,56):1,(95,180):3,
 (96,20):3,(102,1):1,(102,3):3,(132,95):1,(132,96):3,(132,126):3,(235,8):1}
def align_row(source,translation,font):
    parts=[];position=0
    for segment in re.split(r'( {2,})',source):
        if segment.strip():parts.append((visible_width(source[:position+len(segment)-len(segment.lstrip())],font),segment.strip()))
        position+=len(segment)
    labels=re.split(r' {2,}',translation.strip())
    if len(parts)!=len(labels):raise ValueError(('Option count changed',source,translation))
    out='';space=font[WIDTHS+32];anchors=[]
    for (target,_),label in zip(parts,labels):
        current=visible_width(out,font)
        if out and target<current+space:raise ValueError(('Option overlap',target,current,label))
        if target<current:raise ValueError(('Negative option anchor',target,current,label))
        out+=' '*int((target-current+space//2)//space)
        actual=visible_width(out,font);assert abs(actual-target)<=space//2
        anchors.append({'source_x':target,'french_x':actual})
        out+=label
    if visible_width(out,font)>216:raise ValueError(('Option row too wide',visible_width(out,font),out))
    return out,anchors

def service_layout(key,english,french,font):
    if key not in CHOICE_ROWS:return layout_fr(french,font),[]
    n=CHOICE_ROWS[key];en=english.rstrip('\n').split('\n');fr=french.rstrip('\n').split('\n')
    assert len(en)>=n and len(fr)>=n
    rows=[];anchors=[]
    for a,b in zip(en[-n:],fr[-n:]):
        row,positions=align_row(a,b,font);rows.append(row);anchors.append(positions)
    prompt='\n'.join(fr[:-n]);laid_prompt=layout_fr(prompt,font) if prompt else ''
    source_lines=len(en)-n
    french_lines=len(laid_prompt.split('\n')) if prompt else 0
    if french_lines>source_lines:raise ValueError(('Choice prompt exceeds original row count',key,source_lines,french_lines))
    # Retain the source option rows, including the page on which they begin.
    laid=(laid_prompt+'\n' if prompt else '')+'\n'*(source_lines-french_lines)+'\n'.join(rows)
    return laid,anchors
