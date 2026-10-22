#!/usr/bin/env python3
"""Build a read-only text data access observer. No CPU/ROM/WRAM redirection.
All original source and the source-tree core are restored after the build.
The resulting core stays private. FEOE_OBSERVE_TEXT_READS enables logging.
"""
import argparse,hashlib,json,shutil,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
f=a.source/'getset.h';lib=a.source/'libretro/snes9x_libretro.so';original=f.read_bytes();normal=lib.read_bytes();objects={p:p.read_bytes() for p in a.source.rglob('*.o')}
hook=r'''
inline void feoeObserveTextRead (uint32 Address, int width)
{
 static const bool enabled = getenv("FEOE_OBSERVE_TEXT_READS") != NULL;
 if (!enabled) return;
 const uint32 addr = Address & 0xffffff;
 const bool directory = addr >= 0xcc9800 && addr < 0xcc9b00;
 const bool action = addr >= 0x4c7660 && addr < 0x4c85a7;
 const bool enemy = addr >= 0x4096e3 && addr < 0x40b200;
 if (!(directory || action || enemy)) return;
 static unsigned int count = 0;
 static uint32 previousPC = 0;
 static int previousKind = -1;
 const uint32 pc = (Registers.PB << 16) | Registers.PCw;
 const int kind = directory ? 0 : action ? 1 : 2;
 if (pc == previousPC && kind == previousKind && !directory) return;
 previousPC = pc; previousKind = kind;
 if (directory && addr >= 0xcc9836 && addr <= 0xcc983b) {
  fprintf(stderr,"FEOE_SCRIPT cursor=%02x%02x%02x stack=",Memory.RAM[0xaa],Memory.RAM[0xa9],Memory.RAM[0xa8]);
  for (int n = 1; n <= 14; n++) fprintf(stderr,"%02x",Memory.RAM[(Registers.S.W+n)&65535]);
  fprintf(stderr,"\n");
 }
 if (count++ < 12000)
  fprintf(stderr,"FEOE_TEXT_READ addr=%06x width=%d pc=%06x a=%04x x=%04x y=%04x s=%04x\n",addr,width,pc,Registers.A.W,Registers.X.W,Registers.Y.W,Registers.S.W);
}
'''
try:
 s=original.decode();token='inline uint8 S9xGetByte (uint32 Address)\n{';assert s.count(token)==1;s=s.replace(token,hook+'\n'+token+'\n\tfeoeObserveTextRead(Address, 1);')
 token='inline uint16 S9xGetWord (uint32 Address, enum s9xwrap_t w = WRAP_NONE)\n{';assert s.count(token)==1;s=s.replace(token,token+'\n\tfeoeObserveTextRead(Address, 2);');f.write_text(s)
 subprocess.run(['make','-C',str(a.source/'libretro'),'-B','-j4'],check=True);a.out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(lib,a.out)
finally:
 f.write_bytes(original);lib.write_bytes(normal)
 for p,b in objects.items():p.write_bytes(b)
assert f.read_bytes()==original and lib.read_bytes()==normal
print(json.dumps({'observer_sha256':hashlib.sha256(a.out.read_bytes()).hexdigest(),'original_header_sha256':hashlib.sha256(original).hexdigest(),'source_and_library_restored':True,'scope':'Logging only, no CPU/ROM/WRAM modification'}))
