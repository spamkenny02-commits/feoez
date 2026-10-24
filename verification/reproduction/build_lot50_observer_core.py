#!/usr/bin/env python3
"""Opt-in merchant-entry fixture, recovered after local workspace loss.
No environment => no CPU, RAM or ROM changes. Private core not distributed.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();f=a.source/'cpuexec.cpp';original=f.read_bytes();df=a.source/'dma.cpp';dma_original=df.read_bytes();lib=a.source/'libretro/snes9x_libretro.so';normal=lib.read_bytes();objects={p:p.read_bytes()for p in a.source.rglob('*.o')}
assert hashlib.sha256(original).hexdigest()=='37b2f4ece0ff797b616fbeee6084c42a6198d477a08eb1837b5445abacd2c56b'
code=r'''
            if(getenv("FEOE_LOT50_GRAPHICS_TRACE") && Registers.PB==0xc0 && (Registers.PCw==0x1605 || Registers.PCw==0x166b || Registers.PCw==0x2d00 || Registers.PCw==0x617a)) {
                unsigned d=Registers.D.W;
                fprintf(stderr,"FEOE50_GRAPHICS pc=%02x%04x A=%04x X=%04x Y=%04x D=%04x field=%02x%02x table=%02x%02x%02x desc=%02x%02x%02x skip=%02x%02x dest=%02x%02x len=%02x%02x name=%02x%02x\n",Registers.PB,Registers.PCw,Registers.A.W,Registers.X.W,Registers.Y.W,d,Memory.RAM[0xfee],Memory.RAM[0xfed],Memory.RAM[d+8],Memory.RAM[d+7],Memory.RAM[d+6],Memory.RAM[d+0x2c],Memory.RAM[d+0x2b],Memory.RAM[d+0x2a],Memory.RAM[0x2ec2],Memory.RAM[0x2ec1],Memory.RAM[d+0x10],Memory.RAM[d+0xf],Memory.RAM[d+0xd],Memory.RAM[d+0xc],Memory.RAM[0x518],Memory.RAM[0x519]);
            }
            if(getenv("FEOE_LOT50_GRAPHICS_TRACE") && ((Registers.PB==0xc0 && (Registers.PCw==0xaf35 || Registers.PCw==0xafa7 || Registers.PCw==0xafa9)) || (Registers.PB==0x4f && Registers.PCw==0xf8c0))) {
                fprintf(stderr,"FEOE50_SHOP_DATA pc=%02x%04x A=%04x cursor=%02x%02x%02x stockptr=%02x%02x%02x name=%02x pending=%02x\n",Registers.PB,Registers.PCw,Registers.A.W,Memory.RAM[0xaa],Memory.RAM[0xa9],Memory.RAM[0xa8],Memory.RAM[0xde],Memory.RAM[0xdd],Memory.RAM[0xdc],Memory.RAM[0x1dcf],Memory.RAM[0x1f7c]);
            }
            if(getenv("FEOE_LOT50_SHOP_NAME_INDEX") && Registers.PB==0x4f && Registers.PCw==0xf8c0) {
                int index=atoi(getenv("FEOE_LOT50_SHOP_NAME_INDEX"));if(index<0||index>=32)abort();
                fprintf(stderr,"FEOE50_SHOP_NAME fixture original=%u target=%u\n",Registers.AL-1,index);Registers.AL=index+1;
            }
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
dma_code=r'''
    static bool feoeItemDone=false;
    const char *feoeItem=getenv("FEOE_LOT50_ITEM_INDEX");
    if(feoeItem && !feoeItemDone && d->ABank==0x4f && d->AAddress>=0x6000 && d->TransferBytes==128 && !d->ReverseTransfer) {
        int index=atoi(feoeItem);if(index<0||index>=303)abort();
        fprintf(stderr,"FEOE50_ITEM fixture original=%04x target=%04x bytes=128\n",d->AAddress,0x6000+128*index);
        d->AAddress=0x6000+128*index;feoeItemDone=true;
    }
'''
try:
 ds=dma_original.decode();dt='SDMA\t*d = &DMA[Channel];';assert ds.count(dt)==1;df.write_text('#include <cstdlib>\n#include <cstdio>\n'+ds.replace(dt,dt+'\n'+dma_code))
 s=original.decode();token='\t\t\tuint8\t\t\t\tOp;';assert s.count(token)==1;f.write_text('#include <cstdlib>\n#include <cstdio>\n'+s.replace(token,code+'\n'+token));subprocess.run(['make','-C',str(a.source/'libretro'),'-j4'],check=True);a.out.parent.mkdir(exist_ok=True,parents=True);a.out.write_bytes(lib.read_bytes())
finally:
 f.write_bytes(original);df.write_bytes(dma_original);lib.write_bytes(normal)
 for p,data in objects.items():p.write_bytes(data)
assert f.read_bytes()==original and df.read_bytes()==dma_original and lib.read_bytes()==normal
print(json.dumps(dict(core_sha256=hashlib.sha256(a.out.read_bytes()).hexdigest(),standard_sha256=hashlib.sha256(normal).hexdigest(),source_objects_core_restored=True,scope='Independent merchant-entry and first item DMA fixtures;glyph-header fixture not recovered;no natural ownership claim')))
