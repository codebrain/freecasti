[Program dumps](../../prog/README.md) | **System overview** | [Bytes](../bytes/README.md) | [Byte map](../byte-map-overview.md)


# Wet Gain

_Generated 2026-07-18. Source folder: `sysex/system/wet gain/`._

## SysEx summary

- **Offsets:** 8-9
- **Encoding:** `nibble_hilo`
- **Confidence:** high
- **Range:** off encoded=0; range -60 ... -0.5 dB
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Part of the M7’s internal mixing: sets the level of the processed (reverb) signal. Off, then −60 dB to 0 dB (Full) in 0.5 dB steps. Normally 0 dB (Full) with Dry Gain Off for a full-wet sidechain setup. Set Off to bypass processing for I/O test and measurement. Allow headroom when balancing with Dry Gain — the mix can add gain and the reverb process itself can add up to about 10 dB.

_Source: [Bricasti M7 Owner's Manual — System Menu](https://www.bricasti.com/images/M7.pdf)._

> **Capture note:** No hardware UI walk in `docs/reference/provided_labels.json` yet for this system setting — encoding map is built from sparse labeled dumps.

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| `nibble_hilo` | Offset 8 | Offset 9 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | off | dump, inferred |
| 1 | `00` | `01` | -60 dB | dump |
| 2 | `00` | `02` | -59.5 dB | dump |
| 3 | `00` | `03` | -59 dB | inferred |
| 4 | `00` | `04` | -58.5 dB | inferred |
| 5 | `00` | `05` | -58 dB | inferred |
| 6 | `00` | `06` | -57.5 dB | inferred |
| 7 | `00` | `07` | -57 dB | inferred |
| 8 | `00` | `08` | -56.5 dB | inferred |
| 9 | `00` | `09` | -56 dB | inferred |
| 10 | `00` | `0A` | -55.5 dB | inferred |
| 11 | `00` | `0B` | -55 dB | inferred |
| 12 | `00` | `0C` | -54.5 dB | inferred |
| 13 | `00` | `0D` | -54 dB | inferred |
| 14 | `00` | `0E` | -53.5 dB | inferred |
| 15 | `00` | `0F` | -53 dB | dump |
| 16 | `01` | `00` | -52.5 dB | inferred |
| 17 | `01` | `01` | -52 dB | inferred |
| 18 | `01` | `02` | -51.5 dB | inferred |
| 19 | `01` | `03` | -51 dB | inferred |
| 20 | `01` | `04` | -50.5 dB | inferred |
| 21 | `01` | `05` | -50 dB | inferred |
| 22 | `01` | `06` | -49.5 dB | inferred |
| 23 | `01` | `07` | -49 dB | inferred |
| 24 | `01` | `08` | -48.5 dB | inferred |
| 25 | `01` | `09` | -48 dB | inferred |
| 26 | `01` | `0A` | -47.5 dB | inferred |
| 27 | `01` | `0B` | -47 dB | inferred |
| 28 | `01` | `0C` | -46.5 dB | inferred |
| 29 | `01` | `0D` | -46 dB | inferred |
| 30 | `01` | `0E` | -45.5 dB | inferred |
| 31 | `01` | `0F` | -45 dB | inferred |
| 32 | `02` | `00` | -44.5 dB | inferred |
| 33 | `02` | `01` | -44 dB | inferred |
| 34 | `02` | `02` | -43.5 dB | inferred |
| 35 | `02` | `03` | -43 dB | inferred |
| 36 | `02` | `04` | -42.5 dB | inferred |
| 37 | `02` | `05` | -42 dB | inferred |
| 38 | `02` | `06` | -41.5 dB | dump |
| 39 | `02` | `07` | -41 dB | inferred |
| 40 | `02` | `08` | -40.5 dB | inferred |
| 41 | `02` | `09` | -40 dB | inferred |
| 42 | `02` | `0A` | -39.5 dB | inferred |
| 43 | `02` | `0B` | -39 dB | inferred |
| 44 | `02` | `0C` | -38.5 dB | inferred |
| 45 | `02` | `0D` | -38 dB | inferred |
| 46 | `02` | `0E` | -37.5 dB | inferred |
| 47 | `02` | `0F` | -37 dB | inferred |
| 48 | `03` | `00` | -36.5 dB | inferred |
| 49 | `03` | `01` | -36 dB | inferred |
| 50 | `03` | `02` | -35.5 dB | inferred |
| 51 | `03` | `03` | -35 dB | inferred |
| 52 | `03` | `04` | -34.5 dB | inferred |
| 53 | `03` | `05` | -34 dB | inferred |
| 54 | `03` | `06` | -33.5 dB | inferred |
| 55 | `03` | `07` | -33 dB | inferred |
| 56 | `03` | `08` | -32.5 dB | inferred |
| 57 | `03` | `09` | -32 dB | inferred |
| 58 | `03` | `0A` | -31.5 dB | inferred |
| 59 | `03` | `0B` | -31 dB | inferred |
| 60 | `03` | `0C` | -30.5 dB | inferred |
| 61 | `03` | `0D` | -30 dB | inferred |
| 62 | `03` | `0E` | -29.5 dB | inferred |
| 63 | `03` | `0F` | -29 dB | inferred |
| 64 | `04` | `00` | -28.5 dB | inferred |
| 65 | `04` | `01` | -28 dB | inferred |
| 66 | `04` | `02` | -27.5 dB | inferred |
| 67 | `04` | `03` | -27 dB | inferred |
| 68 | `04` | `04` | -26.5 dB | inferred |
| 69 | `04` | `05` | -26 dB | inferred |
| 70 | `04` | `06` | -25.5 dB | inferred |
| 71 | `04` | `07` | -25 dB | inferred |
| 72 | `04` | `08` | -24.5 dB | inferred |
| 73 | `04` | `09` | -24 dB | inferred |
| 74 | `04` | `0A` | -23.5 dB | inferred |
| 75 | `04` | `0B` | -23 dB | inferred |
| 76 | `04` | `0C` | -22.5 dB | inferred |
| 77 | `04` | `0D` | -22 dB | inferred |
| 78 | `04` | `0E` | -21.5 dB | inferred |
| 79 | `04` | `0F` | -21 dB | inferred |
| 80 | `05` | `00` | -20.5 dB | inferred |
| 81 | `05` | `01` | -20 dB | inferred |
| 82 | `05` | `02` | -19.5 dB | inferred |
| 83 | `05` | `03` | -19 dB | inferred |
| 84 | `05` | `04` | -18.5 dB | inferred |
| 85 | `05` | `05` | -18 dB | inferred |
| 86 | `05` | `06` | -17.5 dB | inferred |
| 87 | `05` | `07` | -17 dB | inferred |
| 88 | `05` | `08` | -16.5 dB | inferred |
| 89 | `05` | `09` | -16 dB | inferred |
| 90 | `05` | `0A` | -15.5 dB | inferred |
| 91 | `05` | `0B` | -15 dB | inferred |
| 92 | `05` | `0C` | -14.5 dB | inferred |
| 93 | `05` | `0D` | -14 dB | inferred |
| 94 | `05` | `0E` | -13.5 dB | inferred |
| 95 | `05` | `0F` | -13 dB | inferred |
| 96 | `06` | `00` | -12.5 dB | inferred |
| 97 | `06` | `01` | -12 dB | inferred |
| 98 | `06` | `02` | -11.5 dB | inferred |
| 99 | `06` | `03` | -11 dB | inferred |
| 100 | `06` | `04` | -10.5 dB | inferred |
| 101 | `06` | `05` | -10 dB | inferred |
| 102 | `06` | `06` | -9.5 dB | inferred |
| 103 | `06` | `07` | -9 dB | inferred |
| 104 | `06` | `08` | -8.5 dB | inferred |
| 105 | `06` | `09` | -8 dB | inferred |
| 106 | `06` | `0A` | -7.5 dB | inferred |
| 107 | `06` | `0B` | -7 dB | inferred |
| 108 | `06` | `0C` | -6.5 dB | inferred |
| 109 | `06` | `0D` | -6 dB | inferred |
| 110 | `06` | `0E` | -5.5 dB | inferred |
| 111 | `06` | `0F` | -5 dB | inferred |
| 112 | `07` | `00` | -4.5 dB | inferred |
| 113 | `07` | `01` | -4 dB | inferred |
| 114 | `07` | `02` | -3.5 dB | inferred |
| 115 | `07` | `03` | -3 dB | inferred |
| 116 | `07` | `04` | -2.5 dB | inferred |
| 117 | `07` | `05` | -2 dB | inferred |
| 118 | `07` | `06` | -1.5 dB | inferred |
| 119 | `07` | `07` | -1 dB | dump |
| 120 | `07` | `08` | -0.5 dB | dump |
| 121 | `07` | `09` | full | dump, inferred |

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 8 | Offset 9 | `nibble_hilo` | Checksum 72-75 | Source |
| --- | --- | --- | --- | --- | --- |
| off | `00` | `00` | 0 | `0F` `09` `00` `0E` | dump |
| -60 dB | `00` | `01` | 1 | `03` `09` `04` `0E` | dump |
| -59.5 dB | `00` | `02` | 2 | `03` `09` `08` `0D` | dump |
| -53 dB | `00` | `0F` | 15 | `0F` `0A` `0C` `01` | dump |
| -41.5 dB | `02` | `06` | 38 | `05` `09` `00` `09` | dump |
| -1 dB | `07` | `07` | 119 | `06` `0A` `08` `09` | dump |
| -0.5 dB | `07` | `08` | 120 | `06` `09` `04` `06` | dump |
| full | `07` | `09` | 121 | `0A` `09` `00` `06` | dump |

## Interpretation

- **Primary field:** offsets **8-9**, encoding `nibble_hilo` (encoded * 0.5 + (-60.5)).
- **Confidence:** high (6/6 dumps matched, 100%).
- **Range:** off encoded=0; range -60 ... -0.5 dB.
- **OFF endpoint:** `off.syx` -> encoded 0 - discrete off (not converted through the mid-value scale).
- **HIGH/FULL endpoint:** `full.syx` -> encoded 121 (label 0 dB).
- **Sampling:** extremes, adjacents, 3 sample mid(s) (not every step).
- **How to set:**
  1. encoded = round((desired_label - (-60.5)) / 0.5)
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
- [MIDI Channel](midi-channel.md)
- [Output Level](output-level.md)
- **Wet Gain** (this page)
