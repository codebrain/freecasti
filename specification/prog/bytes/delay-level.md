[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Delay Level

_Generated 2026-07-21. Source folder: `sysex/prog/parameters/delay level/`._

## SysEx summary

- **Offsets:** 132-133
- **Encoding:** `nibble_hilo`
- **Confidence:** high
- **Range:** off encoded=0; range -20 ... -6 dB
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Level of the delayed input injected into the start of the late reverb (not the early reverb). The delayed sound is the original input signal, delayed, diffused, and band-limited by Rolloff.

_Source: [Bricasti M7 V2 Manual Addendum](https://www.bricasti.com/images/M7_V2_Manual_Addendum_Upgrade.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| `nibble_hilo` | Offset 132 | Offset 133 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | off | dump, provided |
| 1 | `00` | `01` | -20 dB | dump, provided, [1](../presets/halls/mechanics-hall.md), [2](../presets/halls-2/koncert-piano.md), [3](../presets/spaces-2/cathedral.md) |
| 2 | `00` | `02` | -19 dB | dump, provided |
| 3 | `00` | `03` | -18 dB | provided, [1](../presets/halls/reflect-hall-a.md), [2](../presets/halls/reflect-hall-b.md), [3](../presets/plates-2/drum-plate.md), [4](../presets/rooms-2/wide-room.md), [5](../presets/spaces/reflect-church.md), +1 more |
| 4 | `00` | `04` | -17 dB | provided, [1](../presets/rooms-2/dark-chamber.md), [2](../presets/rooms-2/deep-chamber.md), [3](../presets/rooms-2/vocal-chamber.md), [4](../presets/spaces-2/vox-ambience.md) |
| 5 | `00` | `05` | -16 dB | provided, [1](../presets/rooms/long-wood-room.md), [2](../presets/rooms-2/marble-room.md) |
| 6 | `00` | `06` | -15 dB | provided, [1](../presets/chambers/a-and-m-chamber-b.md), [2](../presets/chambers/tiled-chamber.md), [3](../presets/halls-2/live-hall.md), [4](../presets/plates-2/fat-plate.md), [5](../presets/spaces-2/concert-wave.md) |
| 7 | `00` | `07` | -14 dB | provided, [1](../presets/rooms-2/guitar-room.md), [2](../presets/spaces-2/music-forest.md), [3](../presets/spaces-2/open-space.md) |
| 8 | `00` | `08` | -13 dB | dump, provided, [1](../presets/spaces/reflect-chapel.md), [2](../presets/spaces-2/live-room.md) |
| 9 | `00` | `09` | -12 dB | provided, [1](../presets/chambers/fat-chamber.md), [2](../presets/halls/pepes-hall-b.md), [3](../presets/plates/vocal-plate-b.md), [4](../presets/spaces-2/ice-house.md), [5](../presets/spaces-2/oak-ballroom.md), +1 more |
| 10 | `00` | `0A` | -11 dB | provided, [1](../presets/rooms-2/lush-room.md) |
| 11 | `00` | `0B` | -10 dB | provided, [1](../presets/chambers/stone-chamber.md), [2](../presets/plates/repro-plate.md), [3](../presets/plates-2/vocal-plate-b.md), [4](../presets/plates-2/vocal-shimmer.md) |
| 12 | `00` | `0C` | -9 dB | provided |
| 13 | `00` | `0D` | -8 dB | provided, [1](../presets/chambers/echo-chamber.md) |
| 14 | `00` | `0E` | -7 dB | dump, provided |
| 15 | `00` | `0F` | -6 dB | dump, provided, [1](../presets/spaces-2/waving-bloom.md) |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **3:** **Halls:** [Reflect Hall A](../presets/halls/reflect-hall-a.md), [Reflect Hall B](../presets/halls/reflect-hall-b.md); **Plates 2:** [Drum Plate](../presets/plates-2/drum-plate.md); **Rooms 2:** [Wide Room](../presets/rooms-2/wide-room.md); **Spaces:** [Reflect Church](../presets/spaces/reflect-church.md); **Spaces 2:** [Dark Warm Room](../presets/spaces-2/dark-warm-room.md)
- **9:** **Chambers:** [Fat Chamber](../presets/chambers/fat-chamber.md); **Halls:** [Pepes Hall B](../presets/halls/pepes-hall-b.md); **Plates:** [Vocal Plate B](../presets/plates/vocal-plate-b.md); **Spaces 2:** [Ice House](../presets/spaces-2/ice-house.md), [Oak Ballroom](../presets/spaces-2/oak-ballroom.md), [Shimmering Sky](../presets/spaces-2/shimmering-sky.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 132 | Offset 133 | `nibble_hilo` | Display lo 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| off (-21 dB) | `??` | `00` | 0 | `05` | `02` `0B` `08` `0D` | dump |
| -20 dB | `??` | `01` | 1 | `06` | `0D` `07` `0F` `04` | dump |
| -19 dB | `??` | `02` | 2 | `07` | `05` `03` `08` `0D` | dump |
| -13 dB | `??` | `08` | 8 | `09` | `04` `0B` `07` `0F` | dump |
| -7 dB | `??` | `0E` | 14 | `0B` | `00` `03` `08` `0E` | dump |
| -6 dB | `??` | `0F` | 15 | `0A` | `03` `0F` `08` `0E` | dump |

## Interpretation

- **Primary field:** offsets **132-133**, encoding `nibble_hilo` (encoded + (-21)).
- **Confidence:** high (5/5 dumps matched, 100%).
- **Catalog hint (Bricasti):** Delay Level - printed -20 ... -6 db [match] - hint only; dumps win.
- **Catalog notes:** This M7: discrete Off, or -20 dB ... -6 dB. V2 addendum parameter; not in older printed tables.
- **Range:** off encoded=0; range -20 ... -6 dB.
- **OFF endpoint:** `off.syx` -> encoded 0 - discrete off (not converted through the mid-value scale).
- **Sampling:** extremes, adjacents, 1 sample mid(s) (not every step).
- **Edge slopes:** Low and high extreme->adjacent slopes agree - strong evidence for a global linear/affine map.
- **How to set:**
  1. encoded = desired_label - (-21)
  2. byte[offset0] = (encoded >> 4) & 0x0F
  3. byte[offset1] = encoded & 0x0F
  4. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 147 (display low nibble) (edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Unseen values

Documented in the spec (encoding map / manual) but not yet witnessed in a committed dump. "Possible" spans every encoded step in this field's range; missing steps are listed as ranges when there are many.

- **Encoding range:** encoded 0–15 (16 steps documented).
- **Never captured on the wire (10):**
  - encoded **3** → -18 dB (provided, preset)
  - encoded **4** → -17 dB (provided, preset)
  - encoded **5** → -16 dB (provided, preset)
  - encoded **6** → -15 dB (provided, preset)
  - encoded **7** → -14 dB (provided, preset)
  - encoded **9** → -12 dB (provided, preset)
  - encoded **10** → -11 dB (provided, preset)
  - encoded **11** → -10 dB (provided, preset)
  - encoded **12** → -9 dB (provided)
  - encoded **13** → -8 dB (provided, preset)
- **Documented gaps (no row at all):** none between documented min/max.
- **Wire nibbles never observed (`0`–`F`):** offset 132 (high): `1` `2` `3` `4` `5` `6` `7` `8` `9` `A` `B` `C` `D` `E` `F`; offset 133 (low): `C`

## Other parameters

- **Delay Level** (this page)
- [Delay Modulation](delay-modulation.md)
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
