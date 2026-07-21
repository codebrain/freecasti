[Program dumps](../../prog/README.md) | **System overview** | [Bytes](../bytes/README.md) | [Byte map](../byte-map-overview.md)


# Output Level

_Generated 2026-07-21. Source folder: `sysex/system/output level/`._

## SysEx summary

- **Offsets:** 17
- **Encoding:** `raw_u8`
- **Confidence:** high
- **Range:** Range 8 ... 24 (capture extremes)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Sets the analog output level trim in three steps (−8 dB, −16 dB, and −24 dB) to match the input sensitivity of your mixer return or the next device in the chain. Return to factory defaults after level-matching tests — high settings can distort on hot signals.

_Source: [Bricasti M7 Owner's Manual — System Menu](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| Encoded | Offset 17 | Label | Source |
| --- | --- | --- | --- |
| 0 | `00` | -8 dB | dump, provided |
| 1 | `01` | -16 dB | dump, provided |
| 2 | `02` | -24 dB | dump, provided |

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 17 | Encoded | Checksum 72-75 | Source |
| --- | --- | --- | --- | --- |
| 8 | `00` | 0 | `0C` `0C` `08` `05` | dump |
| 16 | `01` | 1 | `07` `07` `02` `0E` | dump |
| 24 | `02` | 2 | `0F` `0B` `0D` `00` | dump |

## Interpretation

- **Primary field:** offsets **17**, encoding `raw_u8` (encoded * 8 + (8)).
- **Confidence:** high (3/3 dumps matched, 100%).
- **Range:** Range 8 ... 24 (capture extremes).
- **Sampling:** extremes.
- **How to set:**
  1. encoded = round((desired_label - (8)) / 8.0)
  2. byte[offset0] = encoded & 0x0F  # M7 payload nibbles are 0x00-0x0F
  3. recompute trailing checksum: CRC-16/ARC over bytes[8:72], pack as four high-nibble-first SysEx bytes at offsets 72-75
- **Checksum nibbles:** 72-75 (CRC-16/ARC over offsets 8-71, packed high-nibble-first).

## Other system series

- [Audio Format](audio-format.md)
- [Audio Routing](audio-routing.md)
- [Display Level](display-level.md)
- [Dry Gain](dry-gain.md)
- [MIDI Bank](midi-bank.md)
- [MIDI Channel](midi-channel.md)
- **Output Level** (this page)
- [Wet Gain](wet-gain.md)
