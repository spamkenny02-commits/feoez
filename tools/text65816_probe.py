#!/usr/bin/env python3
"""Restricted native text-slot copier. No event interpreter, PPU or IO timing.
Only raw, uncompressed catalog strings are admitted by the caller.
The shared CPU models multiplication results, not hardware cycles.
"""
from numeric65816_probe import NumericCPU
from cpu65816_probe import CPU
class TextCPU(NumericCPU):
    allowed_ranges=((0xc329b6,0xc32a23),(0xc32aa4,0xc32b0e),
                    (0xc02c5e,0xc02d00),(0xc029a1,0xc029bb))
    load_block=CPU.load_block
    select=CPU.select
    string=CPU.string
