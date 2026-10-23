"""Credits-only partial-glyph flush before line-base snapshot; clear27 columns."""
def patch_credits_line_start(rom,allocation_end):
 start=(int(allocation_end,0)+15)&~15;assert rom[0x176e2:0x176e6]==bytes.fromhex('20 e6 76 6b');assert rom[0x37028:0x3702c]==bytes.fromhex('22 5d 77 c1');assert rom[0x3712d:0x3712f]==bytes.fromhex('e0 0f')
 payload=bytes.fromhex('22 e2 76 c1 c2 20 ad 8f 1c 8d 91 1c e2 20 22 5d 77 c1 6b');end=start+len(payload);assert 0x6c0000<=start<end<0x6d0000 and not any(rom[start:end])
 out=bytearray(rom);out[start:end]=payload;out[0x37028:0x3702c]=bytes([0x22])+(start-0x200000).to_bytes(3,'little');out[0x3712e]=27
 return bytes(out),{'spans':[(start,end),(0x37028,0x3702c),(0x3712e,0x3712f)],'cleared_columns':27,'old_cleared_columns':15,'wrapper_cpu':hex(start-0x200000),'allocation_start':hex(start),'allocation_end':hex(end),'wrapper_hex':payload.hex(),'old_call_hex':'225d77c1','scope':'Credits cleanup only; native reader/font/DMA preserved.'}
