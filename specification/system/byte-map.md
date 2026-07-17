[Program dumps](../prog/README.md) | [System overview](README.md) | [Parameters](parameters/README.md)

# System byte map

Every offset in the 77-byte system-dump layout.

Codegen layout: [m7_system_dump.ksy](m7_system_dump.ksy) · [m7_system_dump.spec.json](m7_system_dump.spec.json).

Each sysex/system/<series>/ folder is an independent capture stream. Reserved/meta roles come from a corpus scan of all system dumps.

Coverage: **77** known/frame/checksum, **0** secondary, **0** unknown (of 77).

### Regions

| Offsets | Len | Example hex | Status | Meaning |
|---------|-----|-------------|--------|---------|
| 0 | 1 | `F0` | frame | SysEx start (F0) |
| 1-3 | 3 | `00 62 63` | frame | Manufacturer ID (00 62 63) |
| 4-7 | 4 | `70 08 02 00` | frame | System-dump header (70 08 02 00) |
| 8-9 | 2 | `00 00` | known | Parameter `wet gain` (from sysex/system/wet gain/) (nibble_hilo) |
| 10-11 | 2 | `00 00` | known | Parameter `dry gain` (from sysex/system/dry gain/) (nibble_hilo) |
| 12 | 1 | `00` | known | Fixed header/prefix block (constant in this corpus) |
| 13 | 1 | `01` | known | Parameter `audio routing` (from sysex/system/audio routing/) (raw_u8) |
| 14 | 1 | `00` | known | Fixed header/prefix block (constant in this corpus) |
| 15 | 1 | `00` | known | Parameter `audio format` (from sysex/system/audio format/) (raw_u8) |
| 16 | 1 | `00` | known | Fixed header/prefix block (constant in this corpus) |
| 17 | 1 | `01` | known | Parameter `output level` (from sysex/system/output level/) (raw_u8) |
| 18 | 1 | `00` | known | Reserved (always 0 in this corpus) |
| 19-20 | 2 | `02 00` | known | Fixed field (always `02 00` in this corpus) |
| 21 | 1 | `01` | known | Parameter `display level` (from sysex/system/display level/) (raw_u8) |
| 22-23 | 2 | `00 00` | known | Parameter `midi channel` (from sysex/system/midi channel/) (nibble_hilo) |
| 24 | 1 | `00` | known | Reserved / padding (constant in this corpus) |
| 25 | 1 | `04` | known | Parameter `midi bank` (from sysex/system/midi bank/) (raw_u8) (also secondary in: `display level`) |
| 26-71 | 46 | `00 00 00 00 00 00 00 00 ...` | known | Reserved / padding (constant in this corpus) |
| 72-75 | 4 | - | checksum | Checksum: CRC-16/ARC over offsets 8-71, packed as four high-nibble-first SysEx bytes |
| 76 | 1 | `F7` | frame | SysEx end (F7) |


_Last exported: 2026-07-18_
