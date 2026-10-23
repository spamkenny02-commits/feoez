#!/usr/bin/env python3
"""Opt-in credits screen context / learned-scroll ID fixtures, never progression.
Credits FD-A2 dispatch, line copy, font, tilemap, DMA, scroll timing remain native.
Standard source/core/object files are restored even on a failed build.
"""
import argparse,subprocess,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();f=a.source/'cpuexec.cpp';lib=a.source/'libretro/snes9x_libretro.so';original=f.read_bytes();normal=lib.read_bytes();objects={q:q.read_bytes() for q in a.source.rglob('*.o')}
assert hashlib.sha256(original).hexdigest()=='37b2f4ece0ff797b616fbeee6084c42a6198d477a08eb1837b5445abacd2c56b'
hook=r'''
            static bool creditStarted=false, creditContext=false, gridStarted=false;
            if (getenv("FEOE_LOT49_CREDITS")) {
                if (!creditStarted && Registers.PB==0xc3 && Registers.PCw==0x0448) {
                    Registers.AL=0xa1;creditStarted=true;
                    fprintf(stderr,"FEOE_LOT49 credits_fixture_dispatch\n");
                }
                if (creditStarted && Registers.PB==0xc3 && Registers.PCw==0x7071) {
                    Memory.RAM[0x020f]=4;Memory.RAM[0x021b]=0x5a;Memory.RAM[0x0236]=3;
                    S9xSetPPU(0x5a,0x2109);S9xSetPPU(3,0x210c);S9xSetPPU(4,0x212c);S9xSetPPU(15,0x2100);
                    Memory.RAM[0x0211]=Memory.RAM[0x0212]=Memory.RAM[0x0213]=Memory.RAM[0x0214]=0;
                    S9xSetPPU(0,0x212e);S9xSetPPU(0,0x212f);S9xSetPPU(0,0x2130);S9xSetPPU(0,0x2131);
                    Memory.RAM[0x0554]=0;S9xSetCPU(0,0x420c);
                    if (!creditContext) {
                        uint8 old=Memory.FillRAM[0x2115];uint16 addr=PPU.VMA.Address;
                        S9xSetPPU(0x80,0x2115);S9xSetPPU(0,0x2116);S9xSetPPU(0x30,0x2117);
                        for(int n=0;n<4096;n++){S9xSetPPU(0,0x2118);S9xSetPPU(0,0x2119);}
                        S9xSetPPU(old,0x2115);S9xSetPPU(addr&255,0x2116);S9xSetPPU(addr>>8,0x2117);creditContext=true;
                    }
                    fprintf(stderr,"FEOE_LOT49 credits_copy cursor=%02x%02x%02x\n",Memory.RAM[0xe8],Memory.RAM[0xe7],Memory.RAM[0xe6]);
                }
                if (creditStarted && Registers.PB==0xc3 && Registers.PCw==0x70c6) {
                    fprintf(stderr,"FEOE_LOT49 credits_line snapshot=%02x%02x next=%02x%02x text=",Memory.RAM[0x1c92],Memory.RAM[0x1c91],Memory.RAM[0xe7],Memory.RAM[0xe6]);
                    for(int n=0;n<46&&Memory.RAM[0x1d30+n];n++)fprintf(stderr,"%02x",Memory.RAM[0x1d30+n]);fprintf(stderr,"\n");
                }
            }
            if (getenv("FEOE_LOT49_SCROLL_GRID") && !gridStarted && Registers.PB==0xc3 && Registers.PCw==0x29b6 && Registers.AL==4) {
                for(int n=0;n<36;n++)Memory.RAM[0x6863+n]=n+1;
                gridStarted=true;fprintf(stderr,"FEOE_LOT49 synthetic_learned_ids=36\n");
            }
'''
try:
 s=original.decode().replace('#include "snes9x.h"','#include "snes9x.h"\n#include <cstdlib>\n#include <cstdio>');token='\t\t\tuint8\t\t\t\tOp;';assert s.count(token)==1;f.write_text(s.replace(token,hook+'\n'+token));subprocess.run(['make','-C',str(a.source/'libretro'),'-j4'],check=True);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(lib.read_bytes())
finally:
 f.write_bytes(original);lib.write_bytes(normal)
 for q,b in objects.items():q.write_bytes(b)
assert f.read_bytes()==original and lib.read_bytes()==normal
print(json.dumps({'source_commit':'1bcc369e89f08243e0a462882fb1f3e42e51de3a','source_cpp_sha256':hashlib.sha256(original).hexdigest(),'standard_core_sha256':hashlib.sha256(normal).hexdigest(),'diagnostic_core_sha256':hashlib.sha256(a.out.read_bytes()).hexdigest(),'source_and_library_restored':True}))
