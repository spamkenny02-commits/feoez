"""Select the last text-bearing native dialogue frame before automatic closure.

The pinned game's dialogue window has a (0,0,57) background and white glyphs.
No screenshot is changed; the source capture is retained byte for byte.
"""
from pathlib import Path
from PIL import Image

def text_frame(path):
    with Image.open(path) as image:
        image=image.convert('RGB')
        background=image.crop((8,152,248,214)).getcolors(15840) or []
        navy=sum(n for n,color in background if color==(0,0,57))
        interior=image.crop((16,160,240,208)).getcolors(10752) or []
        glyphs=sum(n for n,color in interior if color==(255,255,255))
        return navy>=5000 and glyphs>0

def selected_pages(paths):
    groups={}
    for name in paths:
        groups.setdefault(Path(name).stem.split('_')[1],[]).append(name)
    result={}
    for page,files in groups.items():
        selected=next((name for name in reversed(files) if text_frame(name)),None)
        if selected is not None:result[page]=selected
    if not result:raise ValueError('No native dialogue text captured')
    return result
