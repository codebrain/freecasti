[Overview](../README.md) | [Parameters](../parameters/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Delay Modulation

_Generated 2026-07-18. Source folder: `sysex/prog/parameters/delay modulation/`._

## SysEx summary

- **Offsets:** 139
- **Encoding:** `raw_u8`
- **Confidence:** high
- **Range:** off encoded=0; range 0 ... 10
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

> **Capture note:** No hardware UI walk in `docs/reference/provided_labels.json` yet for this program parameter — encoding map is built from sparse labeled dumps — mid-steps may be **inferred** from the confirmed affine scale between sparse dumps and factory preset anchors.

## Description

Modulates the delay voices only (not the reverb), similar in character to reverb Modulation: low settings are slower and more shallow; higher settings are more random and deeper.

_Source: [Bricasti M7 V2 Manual Addendum](https://www.bricasti.com/images/M7_V2_Manual_Addendum_Upgrade.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| Encoded | Offset 139 | Label | Source |
| --- | --- | --- | --- |
| 0 | `00` | off | dump, inferred |
| 1 | `01` | 0 | dump, [1](../presets/halls/reflect-hall-b.md), [2](../presets/plates/repro-plate.md), [3](../presets/plates-2/vocal-plate-b.md), [4](../presets/spaces-2/cathedral.md) |
| 2 | `02` | 1 | dump, [1](../presets/chambers/tiled-chamber.md), [2](../presets/rooms-2/wide-room.md), [3](../presets/spaces/reflect-chapel.md) |
| 3 | `03` | 2 | dump, [1](../presets/chambers/stone-chamber.md), [2](../presets/halls/pepes-hall-b.md) |
| 4 | `04` | 3 | [1](../presets/plates-2/fat-plate.md), [2](../presets/spaces-2/dark-warm-room.md), [3](../presets/spaces-2/oak-ballroom.md), [4](../presets/spaces-2/shimmering-sky.md) |
| 5 | `05` | 4 | [1](../presets/chambers/fat-chamber.md), [2](../presets/rooms-2/guitar-room.md), [3](../presets/spaces-2/ice-house.md) |
| 6 | `06` | 5 | [1](../presets/plates-2/vocal-shimmer.md) |
| 7 | `07` | 6 | [1](../presets/rooms-2/lush-room.md), [2](../presets/spaces/reflect-church.md) |
| 8 | `08` | 7 | dump, [1](../presets/halls-2/live-hall.md), [2](../presets/spaces-2/live-room.md) |
| 9 | `09` | 8 | [1](../presets/rooms-2/vocal-chamber.md) |
| 10 | `0A` | 9 | dump |
| 11 | `0B` | 10 | dump |

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 139 | Encoded | Offset 146 | Offset 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| off (-1) | `00` | 0 | `0B` | `0A` | `06` `00` `0E` `05` | dump |
| low (0) | `01` | 1 | `0B` | `0B` | `02` `01` `0D` `0A` | dump |
| 1 | `02` | 2 | `0B` | `0D` | `0E` `02` `05` `07` | dump |
| 2 | `03` | 3 | `0B` | `0E` | `06` `03` `01` `01` | dump |
| 7 | `08` | 8 | `0B` | `0E` | `0E` `08` `00` `0B` | dump |
| 9 | `0A` | 10 | `0B` | `0F` | `06` `0A` `03` `01` | dump |
| high (10) | `0B` | 11 | `0C` | `00` | `05` `0D` `06` `06` | dump |

## Interpretation

- **Primary field:** offsets **139**, encoding `raw_u8` (encoded + (-1)).
- **Confidence:** high (4/4 dumps matched, 100%).
- **Catalog hint (Bricasti):** Delay Modulation - printed 1 ... 9 [differs_from_hint] - hint only; dumps win.
- **Catalog notes:** Off, Low 1 - 9 High (same shape as reverb Modulation). V2 addendum parameter.
- **Catalog note:** Observed min 0 is below printed manual 1 (unit/firmware variance; dump is authoritative)
- **Catalog note:** Observed max 10 is above printed manual 9 (unit/firmware variance; dump is authoritative)
- **Range:** off encoded=0; range 0 ... 10.
- **OFF endpoint:** `off.syx` -> encoded 0 - discrete off (not converted through the mid-value scale).
- **LOW endpoint:** `low.syx` -> encoded 1 (label 0).
- **HIGH/FULL endpoint:** `high.syx` -> encoded 11 (label 10).
- **Sampling:** extremes, adjacents, 2 sample mid(s) (not every step).
- **How to set:**
  1. encoded = desired_label - (-1)
  2. byte[offset0] = encoded & 0x0F  # M7 payload nibbles are 0x00-0x0F
  3. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 146-147 (likely edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Other parameters

- [Delay Level](delay-level.md)
- **Delay Modulation** (this page)
- [Delay Time](delay-time.md)
- [Density](density.md)
- [Diffusion](diffusion.md)
- [Early Rolloff](early-rolloff.md)
- [Early Select](early-select.md)
- [Early/Reverb Mix](early-to-reverb-mix.md)
- [HF RT Crossover](hf-rt-crossover.md)
- [HF RT Multiply](hf-rt-multiply.md)
- [LF RT Crossover](lf-rt-crossover.md)
- [LF RT Multiply](lf-rt-multiply.md)
- [Modulation](modulation.md)
- [Pre Delay](predelay.md)
- [Reverb Time](reverb-time.md)
- [Rolloff](rolloff.md)
- [Size](size.md)
- [VLF Cut](vlf-cut.md)
