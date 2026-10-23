#!/usr/bin/env python3
"""Opt-in merchant-entry fixture, recovered after local workspace loss.
No environment => no CPU, RAM or ROM changes. Private core not distributed.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();f=a.source/'cpuexec.cpp';original=f.read_bytes();lib=a.source/'libretro/snes9x_libretro.so';normal=lib.read_bytes();objects={p:p.read_bytes()for p in a.source.rglob('*.o')}
assert hashlib.sha256(original).hexdigest()=='37b2f4ece0ff797b616fbeee6084c42a6198d477a08eb1837b5445abacd2c56b'
code=r'''
            static bool feoeShopDone=false,feoeShopText=false;
            if(getenv("FEOE_LOT50_SHOP_ENTRY") && !feoeShopDone && Registers.PB==0xc3 && Registers.PCw==0x29b6 && Registers.AL==48 && Memory.RAM[0xa8]==0x39 && Memory.RAM[0xa9]==0x63 && Memory.RAM[0xaa]==0xc7) {
                int matches=0;
                for(int thread=0;thread<52;thread++) {
                    uint32 cursor=Memory.RAM[0x796 + thread]|(Memory.RAM[0x7ca + thread]<<8)|(Memory.RAM[0x7fe + thread]<<16);
                    if(cursor==0xc7633a) {Memory.RAM[0x796 + thread]=0xea;Memory.RAM[0x7ca + thread]=0xde;Memory.RAM[0x7fe + thread]=0xc5;matches++;}
                }
                fprintf(stderr,"FEOE50_SHOP redirected_thread_count=%d\n",matches);if(matches!=1)abort();Registers.AL=37;Memory.RAM[0xa5]=0xea;Memory.RAM[0xa6]=0xde;Memory.RAM[0xa7]=0xc5;feoeShopDone=true;feoeShopText=true;
            }
            if(feoeShopText && Registers.PB==0xc3 && Registers.PCw==0x29da) {Registers.AL=52;feoeShopText=false;}
            if(getenv("FEOE_LOT50_OBSERVE") && Registers.PB==0xc3) {
                if(Registers.PCw==0x29b6)fprintf(stderr,"FEOE50_LOOKUP load=%u script=%02x%02x%02x\n",Registers.AL,Memory.RAM[0xaa],Memory.RAM[0xa9],Memory.RAM[0xa8]);
                if(Registers.PCw==0x29da)fprintf(stderr,"FEOE50_SELECT base=%02x%02x%02x index=%u\n",Memory.RAM[0x10c7],Memory.RAM[0x10c6],Memory.RAM[0x10c5],Registers.AL);
            }
'''
try:
 s=original.decode();token='\t\t\tuint8\t\t\t\tOp;';assert s.count(token)==1;f.write_text('#include <cstdlib>\n#include <cstdio>\n'+s.replace(token,code+'\n'+token));subprocess.run(['make','-C',str(a.source/'libretro'),'-j4'],check=True);a.out.parent.mkdir(exist_ok=True,parents=True);a.out.write_bytes(lib.read_bytes())
finally:
 f.write_bytes(original);lib.write_bytes(normal)
 for p,data in objects.items():p.write_bytes(data)
assert f.read_bytes()==original and lib.read_bytes()==normal
print(json.dumps(dict(core_sha256=hashlib.sha256(a.out.read_bytes()).hexdigest(),standard_sha256=hashlib.sha256(normal).hexdigest(),source_objects_core_restored=True,scope='Merchant-entry fixture only;prior item/glyph observer features not recovered in this version')))
