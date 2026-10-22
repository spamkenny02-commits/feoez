#!/usr/bin/env python3
"""Build a private observation-only core logging actual text lookups.
The hook reads registers/WRAM and logs them; no CPU/ROM/WRAM writes or fixture
redirection. Source and built normal library are restored in a finally block.
"""
import argparse,hashlib,json,shutil,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();f=a.source/'cpuexec.cpp';lib=a.source/'libretro/snes9x_libretro.so';original=f.read_bytes();normal=lib.read_bytes()
hook=r'''
            static unsigned long feoeTextCalls = 0;
            if (getenv("FEOE_TRACE_LOOKUPS") && feoeTextCalls < 100000) {
                if (Registers.PB == 0xc3 && Registers.PCw == 0x29b6) {
                    fprintf(stderr, "FEOE_OBSERVE load=%u pc=c329b6\n", Registers.AL); feoeTextCalls++;
                } else if (Registers.PB == 0xc3 && Registers.PCw == 0x29da) {
                    uint32 base=Memory.RAM[0x10c5]|(Memory.RAM[0x10c6]<<8)|(Memory.RAM[0x10c7]<<16);
                    fprintf(stderr, "FEOE_OBSERVE base=%06x select=%u pc=c329da\n", base,Registers.AL); feoeTextCalls++;
                }
            }
'''
try:
 s=original.decode().replace('#include "snes9x.h"','#include "snes9x.h"\n#include <cstdlib>\n#include <cstdio>')
 token='\t\t\tuint8\t\t\t\tOp;';assert s.count(token)==1;f.write_text(s.replace(token,hook+'\n'+token));subprocess.run(['make','-C',str(a.source/'libretro'),'-j4'],check=True);shutil.copyfile(lib,a.out)
finally:f.write_bytes(original);lib.write_bytes(normal)
assert f.read_bytes()==original and lib.read_bytes()==normal
print(json.dumps({'trace_core_sha256':hashlib.sha256(a.out.read_bytes()).hexdigest(),'source_cpp_sha256':hashlib.sha256(original).hexdigest(),'normal_library_sha256':hashlib.sha256(normal).hexdigest(),'observer_only':True,'source_and_library_restored':True}))
