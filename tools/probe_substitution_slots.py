#!/usr/bin/env python3
"""Execute only the native command 04..07 leaf handlers on the pinned source.
This is not a render/width/producer-bounds validation or a SNES emulator.
"""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
rom=a.source.read_bytes();sha=hashlib.sha256(rom).hexdigest()
assert sha=='eb07eed483f8f79ab64309c50ad0ef19560946b8e28fbd695470552ba68e356e'
# JSR ($2E01,X) is used after ASL/TAX for low commands (8-bit accumulator).
signature=bytes.fromhex('eb c9 10 b0 10 da 0a aa fc 01 2e fa')
assert rom[0x32dd0:0x32e01].count(signature)==1
results=[]
for command in range(4,8):
    entry=int.from_bytes(rom[0x32e01+2*command:0x32e03+2*command],'little')
    pc=0x30000+entry;memory={0x1c95:0x12};trace=[]
    for _ in range(16):
        trace.append(hex(0xc00000+pc));op=rom[pc];pc+=1
        if op==0xa9:acc=rom[pc];pc+=1
        elif op==0x80:
            d=rom[pc];pc+=1;pc+=d if d<128 else d-256
        elif op in (0x8d,0x9c,0xad):
            addr=int.from_bytes(rom[pc:pc+2],'little');pc+=2
            if op==0xad:acc=memory[addr]
            else:memory[addr]=0 if op==0x9c else acc
        elif op==0x8f:
            addr=int.from_bytes(rom[pc:pc+3],'little');pc+=3;memory[addr]=acc
        elif op==0x60:break
        else:raise AssertionError(('Unsupported instruction',hex(pc-1),hex(op)))
    else:raise AssertionError('Leaf instruction budget exceeded')
    assert memory[0x10c8]==command-4 and memory[0x10c9]==0 and memory[0x7e336a]==0x12
    results.append({'command':f'{command:02X}','handler':hex(0xc30000+entry),'slot':memory[0x10c8], 'cursor_initial':memory[0x10c9], 'trace':trace})
# Native reader multiplies slot by 32, ORs cursor, then reads WRAM through 4F:1D30.
assert rom[0x32a6f:0x32a84]==bytes.fromhex('ad c8 10 85 1e a9 20 85 20 22 a1 29 c0 da a5 22 0d c9 10 aa ee')
assert rom[0x6f1d30:0x6f1d47]==bytes.fromhex('bf aa 32 7e c9 21 90 0e c9 2b b0 0a da 38 e9 21 aa bf d0 1f 4f fa 6b')
assert rom[0x32b01:0x32b0e]==bytes.fromhex('85 1e a9 20 85 20 22 a1 29 c0 a6 22 60')
report={'source_sha256':sha,'scope':'Restricted execution of command leaf handlers; static reader-stride assertions. No runtime display or width validation.', 'handlers':results,'slot_stride_bytes':32,'reader_value_remap':{'input_range':'21..2A','output_hex':rom[0x6f1fd0:0x6f1fda].hex(),'table_cpu':'4F:1FD0'},'reader_address_expression':'7E:32AA + ((slot * 32) OR cursor)', 'limitations':['32-byte spacing is not a proven maximum producer length.','String copy producers at C3:2AA4 and C3:2ABC copy until zero without a local length check.','Actual event producers, values, glyph widths and 05–07 fixtures still require validation.','No 96-pixel width reservation is inferred from command 04.']}
a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS: four native leaf handlers; reader stride. Width bounds remain unresolved.')
