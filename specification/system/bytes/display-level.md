[Program dumps](../../prog/README.md) | **System overview** | [Bytes](../bytes/README.md) | [Byte map](../byte-map-overview.md)


# Display Level

_Generated 2026-07-19. Source folder: `sysex/system/display level/`._

## SysEx summary

- **Offsets:** 21
- **Encoding:** `raw_u8`
- **Confidence:** high
- **Range:** Range 1 ... 3 (capture extremes)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Sets the brightness of the front-panel display in five steps: Dim, 1, 2, 3, and Bright.

_Source: [Bricasti M7 Owner's Manual — System Menu](https://www.bricasti.com/images/M7.pdf)._

> **Capture note:** No hardware UI walk in `docs/reference/provided_labels.json` yet for this system setting — encoding map is built from sparse labeled dumps.

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| Encoded | Offset 21 | Label | Source |
| --- | --- | --- | --- |
| 0 | `00` | dim | dump |
| 1 | `01` | 1 | dump |
| 2 | `02` | 2 | dump |
| 3 | `03` | 3 | dump |
| 4 | `04` | bright | dump |

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 21 | Encoded | Offset 25 | Checksum 72-75 | Source |
| --- | --- | --- | --- | --- | --- |
| dim | `00` | 0 | `0C` | `0A` `00` `06` `0B` | dump |
| 1 | `01` | 1 | `0C` | `02` `0D` `0B` `07` | dump |
| 2 | `02` | 2 | `0C` | `0F` `0B` `0D` `00` | dump |
| 3 | `03` | 3 | `0C` | `07` `06` `00` `0C` | dump |
| bright | `04` | 4 | `00` | `04` `05` `0C` `0B` | dump |

## Interpretation

- **Primary field:** offsets **21**, encoding `raw_u8` (identity).
- **Confidence:** high (3/3 dumps matched, 100%).
- **Range:** Range 1 ... 3 (capture extremes).
- **Sampling:** extremes, 2 sample mid(s) (not every step).
- **How to set:**
  1. encoded = desired_label
  2. byte[offset0] = encoded & 0x0F  # M7 payload nibbles are 0x00-0x0F
  3. recompute trailing checksum: CRC-16/ARC over bytes[8:72], pack as four high-nibble-first SysEx bytes at offsets 72-75
- **Secondary offsets:** 25 (edit/UI state, not the parameter word).
- **Checksum nibbles:** 72-75 (CRC-16/ARC over offsets 8-71, packed high-nibble-first).

## Other system series

- [Audio Format](audio-format.md)
- [Audio Routing](audio-routing.md)
- **Display Level** (this page)
- [Dry Gain](dry-gain.md)
- [MIDI Bank](midi-bank.md)
- [MIDI Channel](midi-channel.md)
- [Output Level](output-level.md)
- [Wet Gain](wet-gain.md)
