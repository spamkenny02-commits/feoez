#!/usr/bin/env python3
"""Execute the four original inline formatters; no event/PPU/timing claim."""
from numeric65816_probe import NumericCPU
class CalendarCPU(NumericCPU):
    allowed_ranges=((0x4d3c00,0x4d3d80),)
