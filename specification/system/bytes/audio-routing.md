[Program dumps](../../prog/README.md) | **System overview** | [Bytes](../bytes/README.md) | [Byte map](../byte-map-overview.md)


# Audio Routing

_Generated 2026-07-21. Source folder: `sysex/system/audio routing/`._

## SysEx summary

- **Offsets:** 13
- **Encoding:** `raw_u8`
- **Confidence:** high
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Sets the routing of the processed (wet) audio. Useful for mono-in, stereo-out reverb work where a single input feeds both processing channels. This affects the wet path only — the dry path stays stereo (use a Y cable for mono internal dry mixing). Choices are Mono L, Mono R, or Stereo.

_Source: [Bricasti M7 Owner's Manual — System Menu](https://www.bricasti.com/images/M7.pdf)._

> **Capture note:** No hardware UI walk in `docs/reference/provided_labels.json` yet for this system setting — encoding map is built from sparse labeled dumps.

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| Encoded | Offset 13 | Label | Source |
| --- | --- | --- | --- |
| 0 | `00` | stereo | dump |
| 1 | `01` | mono l | dump |
| 2 | `02` | mono r | dump |

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 13 | Encoded | Checksum 73-74 | Source |
| --- | --- | --- | --- | --- |
| Stereo | `00` | 0 | `09` `01` | dump |
| Mono L | `01` | 1 | `08` `04` | dump |
| Mono R | `02` | 2 | `0B` `0B` | dump |

## Interpretation

- **Primary field:** offsets **13**, encoding `raw_u8` (enum table: 3 distinct labels each map to a unique encoded value).
- **Confidence:** high (3/3 dumps matched, 100%).
- **Sampling:** 3 sample mid(s) (not every step).
- **How to set:**
  1. encoded = lookup desired label in the capture encoding map (enum table)
  2. byte[offset0] = encoded & 0x0F  # M7 payload nibbles are 0x00-0x0F
  3. recompute trailing checksum: CRC-16/ARC over bytes[8:72], pack as four high-nibble-first SysEx bytes at offsets 72-75
- **Checksum nibbles:** 73-74 (CRC-16/ARC over offsets 8-71, packed high-nibble-first).

## Other system series

- [Audio Format](audio-format.md)
- **Audio Routing** (this page)
- [Display Level](display-level.md)
- [Dry Gain](dry-gain.md)
- [MIDI Bank](midi-bank.md)
- [MIDI Channel](midi-channel.md)
- [Output Level](output-level.md)
- [Wet Gain](wet-gain.md)
