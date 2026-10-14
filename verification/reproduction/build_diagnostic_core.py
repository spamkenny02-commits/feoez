#!/usr/bin/env python3
"""Build a separate diagnostic Snes9x core; standard core/source are restored.
At one dialogue lookup (source block 49), only the CPU arguments are redirected.
ROM bytes, native lookup/selection/reader, font and renderer remain unchanged.
Use FEOE_TEST_BLOCK and FEOE_TEST_STRING; never use this core for progression claims.
"""
import argparse,subprocess,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
f=a.source/'cpuexec.cpp';lib=a.source/'libretro/snes9x_libretro.so';original=f.read_bytes();normal=lib.read_bytes()
hook=r'''
            static const int feoeBlock = getenv("FEOE_TEST_BLOCK") ? atoi(getenv("FEOE_TEST_BLOCK")) : 0;
            static const int feoeString = getenv("FEOE_TEST_STRING") ? atoi(getenv("FEOE_TEST_STRING")) : 0;
            static int feoePhase = 0;
            if (feoeBlock && feoeString) {
                if (feoePhase == 0 && Registers.PB == 0xc3 && Registers.PCw == 0x29b6 && Registers.AL == 49) {
                    Registers.AL = feoeBlock; feoePhase = 1;
                    fprintf(stderr, "FEOE_DIAGNOSTIC block=%d\n", feoeBlock);
                } else if (feoePhase == 1 && Registers.PB == 0xc3 && Registers.PCw == 0x29da) {
                    Registers.AL = feoeString; feoePhase = 2;
                    fprintf(stderr, "FEOE_DIAGNOSTIC string=%d\n", feoeString);
                } else if (feoePhase == 2 && Registers.PB == 0xc3 && Registers.PCw == 0x2a22) {
                    feoePhase = 3;
                } else if (feoePhase == 3 && Registers.PB == 0xc0 && Registers.PCw == 0x2c6e) {
                    uint32 cursor = Memory.RAM[0x8f] | (Memory.RAM[0x90]<<8) | (Memory.RAM[0x91]<<16);
                    if (S9xGetByte(cursor) == 0) {
                        fprintf(stderr, "FEOE_DIAGNOSTIC terminator=%06x\n", cursor);
                        feoePhase = 4;
                    }
                }
            }
'''
try:
 s=original.decode().replace('#include "snes9x.h"','#include "snes9x.h"\n#include <cstdlib>\n#include <cstdio>')
 token='\t\t\tuint8\t\t\t\tOp;';assert s.count(token)==1
 f.write_text(s.replace(token,hook+'\n'+token))
 subprocess.run(['make','-C',str(a.source/'libretro'),'-j4'],check=True)
 a.out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(lib,a.out)
finally:
 f.write_bytes(original);lib.write_bytes(normal)
