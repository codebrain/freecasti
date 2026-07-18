[Program dumps](../../prog/README.md) | **System overview** | [Bytes](../bytes/README.md) | [Byte map](../byte-map-overview.md)


# MIDI Channel

_Generated 2026-07-18. Source folder: `sysex/system/midi channel/`._

## SysEx summary

- **Offsets:** 22-23
- **Encoding:** `nibble_hilo`
- **Confidence:** high
- **Range:** Range 1 ... 16 (capture extremes)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Selects the MIDI channel the M7 listens on for program change and other control messages (channels 1–16, or Omni for all channels). SysEx dumps are channel-less and are not filtered by this setting.

_Source: [Bricasti M7 MIDI Application Notes](https://www.bricasti.com/images/Midi_app_note.pdf)._

> **Capture note:** No hardware UI walk in `docs/reference/provided_labels.json` yet for this system setting — encoding map is built from sparse labeled dumps.

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| `nibble_hilo` | Offset 22 | Offset 23 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | 1 | dump |
| 1 | `00` | `01` | 2 | dump |
| 2 | `00` | `02` | 3 | dump |
| 3 | `00` | `03` | 4 | dump |
| 4 | `00` | `04` | 5 | dump |
| 5 | `00` | `05` | 6 | dump |
| 6 | `00` | `06` | 7 | dump |
| 7 | `00` | `07` | 8 | dump |
| 8 | `00` | `08` | 9 | dump |
| 9 | `00` | `09` | 10 | dump |
| 10 | `00` | `0A` | 11 | dump |
| 11 | `00` | `0B` | 12 | dump |
| 12 | `00` | `0C` | 13 | dump |
| 13 | `00` | `0D` | 14 | dump |
| 14 | `00` | `0E` | 15 | dump |
| 15 | `00` | `0F` | 16 | dump |
| 16 | `01` | `00` | omni | dump |

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 22 | Offset 23 | `nibble_hilo` | Checksum 72-75 | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | `00` | `00` | 0 | `0C` `0A` `0F` `01` | dump |
| 2 | `00` | `01` | 1 | `02` `07` `0D` `0D` | dump |
| 3 | `00` | `02` | 2 | `05` `00` `0A` `0A` | dump |
| 4 | `00` | `03` | 3 | `0B` `0D` `08` `06` | dump |
| 5 | `00` | `04` | 4 | `0B` `0E` `04` `04` | dump |
| 6 | `00` | `05` | 5 | `05` `03` `06` `08` | dump |
| 7 | `00` | `06` | 6 | `02` `04` `01` `0F` | dump |
| 8 | `00` | `07` | 7 | `0C` `09` `03` `03` | dump |
| 9 | `00` | `08` | 8 | `02` `03` `09` `0B` | dump |
| 10 | `00` | `09` | 9 | `0C` `0E` `0B` `07` | dump |
| 11 | `00` | `0A` | 10 | `0B` `09` `0C` `00` | dump |
| 12 | `00` | `0B` | 11 | `05` `04` `0E` `0C` | dump |
| 13 | `00` | `0C` | 12 | `05` `07` `02` `0E` | dump |
| 14 | `00` | `0D` | 13 | `0B` `0A` `00` `02` | dump |
| 15 | `00` | `0E` | 14 | `0C` `0D` `07` `05` | dump |
| 16 | `00` | `0F` | 15 | `02` `00` `05` `09` | dump |
| omni | `01` | `00` | 16 | `01` `07` `01` `0D` | dump |

## Interpretation

- **Primary field:** offsets **22-23**, encoding `nibble_hilo` (encoded + (1)).
- **Confidence:** high (16/16 dumps matched, 100%).
- **Range:** Range 1 ... 16 (capture extremes).
- **Sampling:** extremes, adjacents, 13 sample mid(s) (not every step).
- **Edge slopes:** Low and high extreme->adjacent slopes agree - strong evidence for a global linear/affine map.
- **How to set:**
  1. encoded = desired_label - (1)
  2. byte[offset0] = (encoded >> 4) & 0x0F
  3. byte[offset1] = encoded & 0x0F
  4. recompute trailing checksum: CRC-16/ARC over bytes[8:72], pack as four high-nibble-first SysEx bytes at offsets 72-75
- **Checksum nibbles:** 72-75 (CRC-16/ARC over offsets 8-71, packed high-nibble-first).

## Other system series

- [Audio Format](audio-format.md)
- [Audio Routing](audio-routing.md)
- [Display Level](display-level.md)
- [Dry Gain](dry-gain.md)
- [MIDI Bank](midi-bank.md)
- **MIDI Channel** (this page)
- [Output Level](output-level.md)
- [Wet Gain](wet-gain.md)
