[Program dumps](../../prog/README.md) | **System overview** | [Parameters](../parameters/README.md)


# MIDI Bank

_Generated 2026-07-18. Source folder: `sysex/system/midi bank/`._

## SysEx summary

- **Offsets:** 25
- **Encoding:** `raw_u8`
- **Confidence:** high
- **Layout:** [system byte map](../byte-map.md)

## Description

Selects which program bank the M7 uses when receiving MIDI program changes — factory banks (Halls, Plates, Rooms, and so on), the V2 “2” banks, NonLin, and user register/favorite banks.

_Source: [Bricasti M7 MIDI Application Notes](https://www.bricasti.com/images/Midi_app_note.pdf)._

> **Capture note:** No hardware UI walk in `docs/reference/provided_labels.json` yet for this system setting — encoding map is built from sparse labeled dumps.

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| Encoded | Offset 25 | Label | Source |
| --- | --- | --- | --- |
| 0 | `00` | halls | dump |
| 1 | `01` | plates | dump |
| 2 | `02` | rooms | dump |
| 3 | `03` | chambers | dump |
| 4 | `04` | ambience | dump |
| 5 | `05` | spaces | dump |
| 6 | `06` | halls 2 | dump |
| 7 | `07` | plates 2 | dump |
| 8 | `08` | rooms 2 | dump |
| 9 | `09` | spaces 2 | dump |
| 10 | `0A` | nonlin | dump |
| 11 | `0B` | edit | dump |
| 12 | `0C` | regs | dump |
| 13 | `0D` | favs | dump |

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 25 | Encoded | Checksum 72-75 | Source |
| --- | --- | --- | --- | --- |
| Ambience | `04` | 4 | `09` `08` `0B` `04` | dump |
| Chambers | `03` | 3 | `01` `0D` `0B` `02` | dump |
| Edit | `0B` | 11 | `07` `0E` `0D` `06` | dump |
| Favs | `0D` | 13 | `05` `07` `0B` `0D` | dump |
| Halls | `00` | 0 | `0A` `09` `00` `06` | dump |
| Halls 2 | `06` | 6 | `08` `00` `06` `0D` | dump |
| NonLin | `0A` | 10 | `0D` `02` `0B` `0B` | dump |
| Plates | `01` | 1 | `00` `05` `06` `0B` | dump |
| Plates 2 | `07` | 7 | `02` `0C` `00` `00` | dump |
| Regs | `0C` | 12 | `0F` `0B` `0D` `00` | dump |
| Rooms | `02` | 2 | `0B` `01` `0D` `0F` | dump |
| Rooms 2 | `08` | 8 | `0C` `0A` `06` `02` | dump |
| Spaces | `05` | 5 | `03` `04` `0D` `09` | dump |
| Spaces 2 | `09` | 9 | `06` `06` `00` `0F` | dump |

## Interpretation

- **Primary field:** offsets **25**, encoding `raw_u8` (enum table: 14 distinct labels each map to a unique encoded value).
- **Confidence:** high (14/14 dumps matched, 100%).
- **Sampling:** 14 sample mid(s) (not every step).
- **How to set:**
  1. encoded = lookup desired label in the capture encoding map (enum table)
  2. byte[offset0] = encoded & 0x0F  # M7 payload nibbles are 0x00-0x0F
  3. recompute trailing checksum: CRC-16/ARC over bytes[8:72], pack as four high-nibble-first SysEx bytes at offsets 72-75
- **Checksum nibbles:** 72-75 (CRC-16/ARC over offsets 8-71, packed high-nibble-first).

## Other system series

- [Audio Format](audio-format.md)
- [Audio Routing](audio-routing.md)
- [Display Level](display-level.md)
- [Dry Gain](dry-gain.md)
- **MIDI Bank** (this page)
- [MIDI Channel](midi-channel.md)
- [Output Level](output-level.md)
- [Wet Gain](wet-gain.md)
