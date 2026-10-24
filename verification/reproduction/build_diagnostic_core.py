#!/usr/bin/env python3
"""Build a separate diagnostic Snes9x core; standard core/source are restored.
At one dialogue lookup (source block 49), only the CPU arguments are redirected.
ROM bytes, native lookup/selection/reader, font and renderer remain unchanged.
Use FEOE_TEST_BLOCK and FEOE_TEST_STRING; never use this core for progression claims.
"""
import argparse,subprocess,shutil,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--trigger-block',type=int,default=49,choices=range(1,256),metavar='1..255',help='Opt-in source lookup to redirect for staged rendering; default49.20 is a battle target-name fixture, never normal progression');p.add_argument('--enable-slot-fixtures',action='store_true',help='Opt-in synthetic WRAM text slots for staged rendering only');p.add_argument('--enable-style-slot-fixtures',action='store_true',help='Permit only native08/0A in addition to printable synthetic slot bytes; requires --enable-slot-fixtures');a=p.parse_args()
if a.enable_style_slot_fixtures and not a.enable_slot_fixtures:p.error('Style fixtures require --enable-slot-fixtures')
f=a.source/'cpuexec.cpp';lib=a.source/'libretro/snes9x_libretro.so';original=f.read_bytes();normal=lib.read_bytes();objects={p:p.read_bytes() for p in a.source.rglob('*.o')}
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
                } else if (feoePhase == 3 && ((Registers.PB == 0xc0 && Registers.PCw == 0x2c6e) ||
                           (Registers.PB == 0x4d && Registers.PCw == 0x3d8d))) {
                    // The pinned English patch's x5 handler reads an inline byte
                    // at 4D:3D8D after closing the window, outside C0:2C6E.
                    // Observe the same zero fetch without modifying CPU or ROM.
                    uint32 cursor = Memory.RAM[0x8f] | (Memory.RAM[0x90]<<8) | (Memory.RAM[0x91]<<16);
                    if (S9xGetByte(cursor) == 0) {
                        fprintf(stderr, "FEOE_DIAGNOSTIC reader=%02x%04x\n", Registers.PB, Registers.PCw);
                        fprintf(stderr, "FEOE_DIAGNOSTIC terminator=%06x\n", cursor);
                        feoePhase = 4;
                    }
                }
            }
'''
hook=hook.replace('Registers.AL == 49',f'Registers.AL == {a.trigger_block}')
if a.enable_slot_fixtures:
 fixture_hook=r'''
                    // Explicit synthetic fixture; never a natural-event proof.
                    for (int slot=0; slot<4; slot++) {
                        char key[40]; snprintf(key, sizeof(key), "FEOE_TEST_SLOT%d_HEX", slot);
                        const char *hex = getenv(key);
                        if (!hex) continue;
                        size_t len = strlen(hex);
                        if (len > 62 || len % 2) abort();
                        memset(Memory.RAM + 0x32aa + 32*slot, 0, 32);
                        for (size_t n=0; n<len; n+=2) {
                            if (!isxdigit((unsigned char)hex[n]) || !isxdigit((unsigned char)hex[n+1])) abort();
                            char pair[3] = {hex[n],hex[n+1],0};
                            unsigned long value = strtoul(pair, NULL, 16);
                            if (value < 0x10 || value >= 0xe0) abort();
                            Memory.RAM[0x32aa + 32*slot + n/2] = (uint8)value;
                        }
                        fprintf(stderr, "FEOE_DIAGNOSTIC synthetic_slot=%d hex=%s\n", slot, hex);
                    }
'''
 if a.enable_style_slot_fixtures:fixture_hook=fixture_hook.replace('value < 0x10 || value >= 0xe0','(value < 0x10 && value != 0x08 && value != 0x0a) || value >= 0xe0')
 hook=hook.replace('feoePhase = 3;', 'feoePhase = 3;'+fixture_hook)
 consumed_hook=r'''
                } else if (feoePhase == 3 && Registers.PB == 0xc3 &&
                           (Registers.PCw == 0x2e60 || Registers.PCw == 0x2e64 || Registers.PCw == 0x2e68 || Registers.PCw == 0x2e6c)) {
                    int slot=(Registers.PCw-0x2e60)/4;
                    fprintf(stderr, "FEOE_DIAGNOSTIC consumed_slot=%d hex=", slot);
                    for (int n=0; n<32 && Memory.RAM[0x32aa+32*slot+n]; n++)
                        fprintf(stderr, "%02x", Memory.RAM[0x32aa+32*slot+n]);
                    fprintf(stderr, "\n");
'''
 hook=hook.replace('                } else if (feoePhase == 3 &&', consumed_hook+'                } else if (feoePhase == 3 &&',1)
try:
 s=original.decode().replace('#include "snes9x.h"','#include "snes9x.h"\n#include <cstdlib>\n#include <cstdio>\n#include <cstring>\n#include <cctype>')
 token='\t\t\tuint8\t\t\t\tOp;';assert s.count(token)==1
 f.write_text(s.replace(token,hook+'\n'+token))
 subprocess.run(['make','-C',str(a.source/'libretro'),'-j4'],check=True)
 a.out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(lib,a.out)
finally:
 f.write_bytes(original);lib.write_bytes(normal)
 for p,b in objects.items():p.write_bytes(b)

assert f.read_bytes()==original and lib.read_bytes()==normal
print(json.dumps({'diagnostic_core_sha256':hashlib.sha256(a.out.read_bytes()).hexdigest(),'source_cpp_sha256':hashlib.sha256(original).hexdigest(),'source_library_sha256':hashlib.sha256(normal).hexdigest(),'source_and_library_restored':True,'synthetic_style_slots_enabled':a.enable_style_slot_fixtures,'trigger_block':a.trigger_block}))
