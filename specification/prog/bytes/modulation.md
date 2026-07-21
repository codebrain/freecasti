[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Modulation

_Generated 2026-07-21. Source folder: `sysex/prog/parameters/modulation/`._

## SysEx summary

- **Offsets:** 111
- **Encoding:** `raw_u8`
- **Confidence:** high
- **Range:** off encoded=0; range 0 ... 10
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

> **Capture note:** No hardware UI walk in `docs/reference/provided_labels.json` yet for this program parameter — encoding map is built from sparse labeled dumps — mid-steps may be **inferred** from the confirmed affine scale between sparse dumps and factory preset anchors.

## Description

Controls the amount of modulation and pitch variation in the later part of the reverberant field.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| Encoded | Offset 111 | Label | Source |
| --- | --- | --- | --- |
| 0 | `00` | off | dump, inferred |
| 1 | `01` | 0 | dump, [1](../presets/halls/amsterdam-hall.md), [2](../presets/halls/berliner-hall.md), [3](../presets/halls/vienna-hall.md), [4](../presets/rooms/large-q-room.md), [5](../presets/rooms/large-wooden.md), +11 more |
| 2 | `02` | 1 | dump, [1](../presets/chambers/a-and-m-chamber.md), [2](../presets/chambers/large-and-bright.md), [3](../presets/chambers/large-chamber.md), [4](../presets/chambers/medium-chamber.md), [5](../presets/halls/large-and-deep.md), +3 more |
| 3 | `03` | 2 | dump, [1](../presets/chambers/amb-chamber-b.md), [2](../presets/chambers/snare-chamber.md), [3](../presets/halls/brass-hall.md), [4](../presets/halls/small-and-near.md), [5](../presets/halls/small-hall.md), +8 more |
| 4 | `04` | 3 | dump, [1](../presets/chambers/amb-chamber-a.md), [2](../presets/chambers/old-chamber.md), [3](../presets/plates/percussion.md), [4](../presets/plates/snare-plate-a.md), [5](../presets/rooms/djangos-room.md) |
| 5 | `05` | 4 | [1](../presets/halls/gold-hall.md), [2](../presets/halls/large-and-near.md), [3](../presets/halls/large-hall.md), [4](../presets/halls/medium-and-near.md), [5](../presets/halls/medium-hall.md), +1 more |
| 6 | `06` | 5 | [1](../presets/chambers/cd-chamber.md), [2](../presets/halls/sandors-hall.md), [3](../presets/plates/cd-plate-b.md), [4](../presets/rooms/center-room.md) |
| 7 | `07` | 6 | [1](../presets/halls/concert-hall.md) |
| 8 | `08` | 7 | [1](../presets/chambers/kick-chamber.md), [2](../presets/plates/dense-plate.md), [3](../presets/rooms/back-room.md) |
| 9 | `09` | 8 | [1](../presets/plates-2/fat-plate.md), [2](../presets/rooms-2/fat-chamber.md), [3](../presets/spaces/gated-space.md) |
| 10 | `0A` | 9 | dump, [1](../presets/halls/dense-hall.md), [2](../presets/plates/fat-plate.md), [3](../presets/rooms/front-room.md) |
| 11 | `0B` | 10 | dump, [1](../presets/plates/cd-plate-a.md), [2](../presets/rooms/drum-and-chamber.md), [3](../presets/spaces/europa.md) |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **1:** **Halls:** [Amsterdam Hall](../presets/halls/amsterdam-hall.md), [Berliner Hall](../presets/halls/berliner-hall.md), [Vienna Hall](../presets/halls/vienna-hall.md); **Rooms:** [Large Q Room](../presets/rooms/large-q-room.md), [Large Wooden](../presets/rooms/large-wooden.md), [Studio A](../presets/rooms/studio-a.md); **Spaces:** [Arena](../presets/spaces/arena.md), [Bath House](../presets/spaces/bath-house.md), [East Church](../presets/spaces/east-church.md), [North Church](../presets/spaces/north-church.md), [Redwood Valley](../presets/spaces/redwood-valley.md), [Scoring Stage](../presets/spaces/scoring-stage.md), [South Church](../presets/spaces/south-church.md), [Stone Quarry](../presets/spaces/stone-quarry.md), [Tanglewood](../presets/spaces/tanglewood.md), [West Church](../presets/spaces/west-church.md)
- **2:** **Chambers:** [A&M Chamber](../presets/chambers/a-and-m-chamber.md), [Large & Bright](../presets/chambers/large-and-bright.md), [Large Chamber](../presets/chambers/large-chamber.md), [Medium Chamber](../presets/chambers/medium-chamber.md); **Halls:** [Large & Deep](../presets/halls/large-and-deep.md), [Medium & Deep](../presets/halls/medium-and-deep.md); **Plates:** [Snare Plate B](../presets/plates/snare-plate-b.md); **Rooms:** [Deep Stone](../presets/rooms/deep-stone.md)
- **3:** **Chambers:** [Amb Chamber B](../presets/chambers/amb-chamber-b.md), [Snare Chamber](../presets/chambers/snare-chamber.md); **Halls:** [Brass Hall](../presets/halls/brass-hall.md), [Small & Near](../presets/halls/small-and-near.md), [Small Hall](../presets/halls/small-hall.md); **Plates:** [Bright Plate](../presets/plates/bright-plate.md), [Dark Plate](../presets/plates/dark-plate.md), [Echo Plate](../presets/plates/echo-plate.md), [Silver Plate](../presets/plates/silver-plate.md); **Rooms:** [Large Room](../presets/rooms/large-room.md), [Music Room](../presets/rooms/music-room.md), [Small Room](../presets/rooms/small-room.md), [Small Vox Room](../presets/rooms/small-vox-room.md)
- **5:** **Halls:** [Gold Hall](../presets/halls/gold-hall.md), [Large & Near](../presets/halls/large-and-near.md), [Large Hall](../presets/halls/large-hall.md), [Medium & Near](../presets/halls/medium-and-near.md), [Medium Hall](../presets/halls/medium-hall.md); **Plates:** [Crystal Plate](../presets/plates/crystal-plate.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 111 | Encoded | Display lo 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- |
| off (-1) | `00` | 0 | `05` | `07` `09` `0C` `05` | dump |
| low (0) | `01` | 1 | `06` | `0C` `04` `08` `06` | dump |
| 1 | `02` | 2 | `07` | `08` `03` `0B` `01` | dump |
| 2 | `03` | 3 | `08` | `03` `0F` `0E` `02` | dump |
| 3 | `04` | 4 | `09` | `00` `0C` `0C` `0F` | dump |
| 9 | `0A` | 10 | `0A` | `0A` `0A` `0A` `08` | dump |
| high (10) | `0B` | 11 | `0B` | `0D` `07` `09` `02` | dump |

## Interpretation

- **Primary field:** offsets **111**, encoding `raw_u8` (encoded + (-1)).
- **Confidence:** high (4/4 dumps matched, 100%).
- **Catalog hint (Bricasti):** Modulation - printed 1 ... 9 [differs_from_hint] - hint only; dumps win.
- **Catalog notes:** Manual UI: Off, Low 1 - 9 High. Captures may use encoded off + 0...10.
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
- **Secondary offsets:** 147 (display low nibble) (edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Unseen values

Documented in the spec (encoding map / manual) but not yet witnessed in a committed dump. "Possible" spans every encoded step in this field's range; missing steps are listed as ranges when there are many.

- **Encoding range:** encoded 0–11 (12 steps documented).
- **Never captured on the wire (5):**
  - encoded **5** → 4 (preset)
  - encoded **6** → 5 (preset)
  - encoded **7** → 6 (preset)
  - encoded **8** → 7 (preset)
  - encoded **9** → 8 (preset)
- **Documented gaps (no row at all):** none between documented min/max.
- **Wire nibbles never observed (`0`–`F`):** offset 111: `C` `D` `E` `F`

## Other parameters

- [Delay Level](delay-level.md)
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
- **Modulation** (this page)
- [Pre Delay](predelay.md)
- [Reverb Time](reverb-time.md)
- [Rolloff](rolloff.md)
- [Size](size.md)
- [VLF Cut](vlf-cut.md)
