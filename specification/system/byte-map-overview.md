[Program dumps](../prog/README.md) | [System overview](README.md) | [Bytes](bytes/README.md) | **Byte map**

# Byte map overview

**77**-byte system dump. Known/frame/checksum **77** · secondary **0** · unknown **0**.

Full regions table: [byte-map.md](byte-map.md).

Codegen layout: [m7_system_dump.ksy](m7_system_dump.ksy) ([Kaitai Struct](https://kaitai.io/)) · [m7_system_dump.spec.json](m7_system_dump.spec.json).

Reserved/meta roles (fixed prefix, padding) come from a corpus scan of all system `.syx` dumps — medium confidence.

### Layout

| Offsets | Len | Status | Field |
|---------|----:|--------|-------|
| 0 | 1 | frame | SysEx start (F0) |
| 1-3 | 3 | frame | manufacturer ID |
| 4-7 | 4 | frame | system-dump header |
| 8-9 | 2 | known | [wet gain](bytes/wet-gain.md) (`nibble_hilo`) |
| 10-11 | 2 | known | [dry gain](bytes/dry-gain.md) (`nibble_hilo`) |
| 12 | 1 | known | fixed prefix |
| 13 | 1 | known | [audio routing](bytes/audio-routing.md) (`raw_u8`) |
| 14 | 1 | known | fixed prefix |
| 15 | 1 | known | [audio format](bytes/audio-format.md) (`raw_u8`) |
| 16 | 1 | known | fixed prefix |
| 17 | 1 | known | [output level](bytes/output-level.md) (`raw_u8`) |
| 18 | 1 | known | reserved (always 0) |
| 19-20 | 2 | known | fixed (always 02 00) |
| 21 | 1 | known | [display level](bytes/display-level.md) (`raw_u8`) |
| 22-23 | 2 | known | [midi channel](bytes/midi-channel.md) (`nibble_hilo`) |
| 24 | 1 | known | reserved padding |
| 25 | 1 | known | [midi bank](bytes/midi-bank.md) (`raw_u8`) |
| 26-71 | 46 | known | reserved padding |
| 72-75 | 4 | checksum | checksum (CRC-16/ARC) |
| 76 | 1 | frame | SysEx end (F7) |

### Settings (by offset)

| Offsets | Setting | Encoding | Source |
|---------|---------|----------|--------|
| 8-9 | [wet gain](bytes/wet-gain.md) | `nibble_hilo` | series |
| 10-11 | [dry gain](bytes/dry-gain.md) | `nibble_hilo` | series |
| 13 | [audio routing](bytes/audio-routing.md) | `raw_u8` | series |
| 15 | [audio format](bytes/audio-format.md) | `raw_u8` | series |
| 17 | [output level](bytes/output-level.md) | `raw_u8` | series |
| 21 | [display level](bytes/display-level.md) | `raw_u8` | series |
| 22-23 | [midi channel](bytes/midi-channel.md) | `nibble_hilo` | series |
| 25 | [midi bank](bytes/midi-bank.md) | `raw_u8` | series |

### Coupled offsets

- Offset **25** ([midi bank](bytes/midi-bank.md)) also moves when capturing [display level](bytes/display-level.md).


_Last exported: 2026-07-21_
