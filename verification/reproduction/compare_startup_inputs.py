#!/usr/bin/env python3
"""Compare rendered date/time values in two natural controller replays.
Ignore translated captions and the blue cursor, but retain every white numeric pixel.
"""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops
p=argparse.ArgumentParser();p.add_argument('--before',type=Path,required=True);p.add_argument('--after',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
before=json.loads((a.before/'report.json').read_text());after=json.loads((a.after/'report.json').read_text());assert before['images']==after['images'];rows=[]
for name in after['images']:
 if name in ['boot.png','after_reset_a.png','check_a.png','check_b.png','birth_accepted.png']:continue
 boxes=[(64,87,192,105)]
 if name.startswith('rtc_') or name in ['date_setup.png','date_confirmed.png','clock_start.png']:boxes.append((96,111,200,129))
 def numeric(path,box):return Image.open(path).convert('L').crop(box).point(lambda x:255 if x>200 else 0)
 matches=[ImageChops.difference(numeric(a.before/name,b),numeric(a.after/name,b)).getbbox() is None for b in boxes]
 assert all(matches),name
 rows.append({'image':name,'numeric_regions':boxes,'identical_numeric_glyphs':True,'baseline_image_sha256':hashlib.sha256((a.before/name).read_bytes()).hexdigest(),'modified_image_sha256':hashlib.sha256((a.after/name).read_bytes()).hexdigest()})
result={'baseline_rom_sha256':before['rom_sha256'],'modified_rom_sha256':after['rom_sha256'],'compared_captures':len(rows),'method':'White numeric glyphs, luminance >200; blue cursor fill excluded. Same controller sequence, own-ROM fresh states.','scope':'Rendered values in these cases; not all calendar boundaries, persistent host saves or real hardware.','comparisons':rows};a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'compared_captures':len(rows),'all_identical':True}))
