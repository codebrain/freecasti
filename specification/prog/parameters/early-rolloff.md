[Overview](../README.md) | [Parameters](../parameters/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Early Rolloff

_Generated 2026-07-18. Source folder: `sysex/prog/parameters/early rolloff/`._

## SysEx summary

- **Offsets:** 126-127
- **Encoding:** `nibble_hilo`
- **Confidence:** medium
- **Range:** Observed range 80 ... 22000 Hz
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Sets the rolloff frequency point of the low pass filter for the early part of the reverberant field.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| Encoded | Offset 126 | Offset 127 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | 80 Hz | dump, provided |
| 1 | `00` | `01` | 120 Hz | dump, provided |
| 2 | `00` | `02` | 160 Hz | provided |
| 3 | `00` | `03` | 200 Hz | provided, [1](../presets/ambience/bass-xxl.md) |
| 4 | `00` | `04` | 240 Hz | provided |
| 5 | `00` | `05` | 280 Hz | dump, provided |
| 6 | `00` | `06` | 320 Hz | provided |
| 7 | `00` | `07` | 360 Hz | provided |
| 8 | `00` | `08` | 400 Hz | provided |
| 9 | `00` | `09` | 480 Hz | dump, provided |
| 10 | `00` | `0A` | 560 Hz | provided |
| 11 | `00` | `0B` | 640 Hz | provided |
| 12 | `00` | `0C` | 720 Hz | provided |
| 13 | `00` | `0D` | 800 Hz | provided |
| 14 | `00` | `0E` | 1000 Hz | provided |
| 15 | `00` | `0F` | 1200 Hz | provided, [1](../presets/spaces/arena.md) |
| 16 | `01` | `00` | 1400 Hz | provided |
| 17 | `01` | `01` | 1600 Hz | provided |
| 18 | `01` | `02` | 1800 Hz | provided |
| 19 | `01` | `03` | 2000 Hz | provided |
| 20 | `01` | `04` | 2400 Hz | provided |
| 21 | `01` | `05` | 2800 Hz | provided |
| 22 | `01` | `06` | 3200 Hz | provided |
| 23 | `01` | `07` | 3600 Hz | provided, [1](../presets/ambience/medium-and-dark.md), [2](../presets/ambience/small-and-dark.md) |
| 24 | `01` | `08` | 4000 Hz | provided |
| 25 | `01` | `09` | 4400 Hz | provided |
| 26 | `01` | `0A` | 4800 Hz | provided, [1](../presets/spaces/car-park.md) |
| 27 | `01` | `0B` | 5200 Hz | provided, [1](../presets/halls/large-and-dark.md) |
| 28 | `01` | `0C` | 5600 Hz | provided, [1](../presets/ambience/large-and-dark.md), [2](../presets/spaces/cinema-room.md) |
| 29 | `01` | `0D` | 6000 Hz | provided |
| 30 | `01` | `0E` | 6400 Hz | provided, [1](../presets/halls/chicago-hall.md), [2](../presets/plates/dense-plate.md), [3](../presets/plates/percussion.md), [4](../presets/rooms/heavy-room.md) |
| 31 | `01` | `0F` | 6800 Hz | provided, [1](../presets/plates/dark-plate.md) |
| 32 | `02` | `00` | 7200 Hz | provided, [1](../presets/halls/large-and-deep.md), [2](../presets/plates/echo-plate.md), [3](../presets/plates/london-plate.md), [4](../presets/rooms/large-room.md), [5](../presets/rooms/small-room.md), +1 more |
| 33 | `02` | `01` | 7600 Hz | provided |
| 34 | `02` | `02` | 8000 Hz | provided, [1](../presets/chambers/old-chamber.md), [2](../presets/halls/small-hall.md), [3](../presets/rooms/studio-c.md) |
| 35 | `02` | `03` | 8400 Hz | provided |
| 36 | `02` | `04` | 8800 Hz | provided, [1](../presets/halls/medium-hall.md), [2](../presets/rooms/music-room.md) |
| 37 | `02` | `05` | 9200 Hz | provided, [1](../presets/rooms/back-room.md) |
| 38 | `02` | `06` | 9600 Hz | provided, [1](../presets/chambers/snare-chamber.md), [2](../presets/halls/medium-and-deep.md), [3](../presets/halls/small-and-near.md), [4](../presets/plates/cd-plate-a.md), [5](../presets/plates/cd-plate-b.md), +4 more |
| 39 | `02` | `07` | 10000 Hz | provided, [1](../presets/chambers/large-chamber.md), [2](../presets/chambers/medium-chamber.md), [3](../presets/chambers/small-chamber.md), [4](../presets/halls/the-archduke.md), [5](../presets/plates/small-plate.md), +2 more |
| 40 | `02` | `08` | 10400 Hz | provided, [1](../presets/ambience/deep-ambience.md), [2](../presets/ambience/large-ambience.md), [3](../presets/ambience/long-ambience.md), [4](../presets/chambers/amb-chamber-b.md), [5](../presets/chambers/cd-chamber.md), +8 more |
| 41 | `02` | `09` | 10800 Hz | provided, [1](../presets/halls/large-hall.md) |
| 42 | `02` | `0A` | 11200 Hz | provided, [1](../presets/ambience/clear-ambience.md), [2](../presets/halls/clear-hall.md), [3](../presets/rooms/drum-and-chamber.md) |
| 43 | `02` | `0B` | 11600 Hz | provided, [1](../presets/rooms/studio-a.md) |
| 44 | `02` | `0C` | 12000 Hz | provided, [1](../presets/chambers/a-and-m-chamber.md), [2](../presets/chambers/amb-chamber-a.md), [3](../presets/plates/snare-plate-a.md), [4](../presets/rooms/front-room.md), [5](../presets/rooms/studio-e.md), +2 more |
| 45 | `02` | `0D` | 12400 Hz | provided, [1](../presets/halls/dense-hall.md) |
| 46 | `02` | `0E` | 12800 Hz | provided, [1](../presets/rooms/djangos-room.md) |
| 47 | `02` | `0F` | 13200 Hz | provided |
| 48 | `03` | `00` | 13600 Hz | dump, provided, [1](../presets/halls/brass-hall.md) |
| 49 | `03` | `01` | 14000 Hz | provided, [1](../presets/chambers/kick-chamber.md), [2](../presets/halls/amsterdam-hall.md) |
| 50 | `03` | `02` | 14400 Hz | provided, [1](../presets/chambers/large-and-bright.md), [2](../presets/spaces/south-church.md) |
| 51 | `03` | `03` | 14800 Hz | provided |
| 52 | `03` | `04` | 15200 Hz | provided, [1](../presets/ambience/large-and-bright.md), [2](../presets/ambience/small-and-bright.md), [3](../presets/halls/gold-hall.md), [4](../presets/plates/crystal-plate.md) |
| 53 | `03` | `05` | 15600 Hz | provided, [1](../presets/halls/boston-hall-a.md), [2](../presets/halls/medium-and-near.md), [3](../presets/halls/worcester-hall.md), [4](../presets/rooms/small-q-room.md), [5](../presets/spaces/tanglewood.md) |
| 54 | `03` | `06` | 16000 Hz | provided, [1](../presets/rooms/deep-stone.md) |
| 55 | `03` | `07` | 16400 Hz | provided, [1](../presets/rooms/marble-foyer.md) |
| 56 | `03` | `08` | 16800 Hz | provided, [1](../presets/rooms/large-q-room.md), [2](../presets/rooms/small-tiled.md), [3](../presets/spaces/west-church.md) |
| 57 | `03` | `09` | 17200 Hz | provided, [1](../presets/halls/concert-hall.md) |
| 58 | `03` | `0A` | 17600 Hz | provided |
| 59 | `03` | `0B` | 18000 Hz | provided, [1](../presets/halls/berliner-hall.md) |
| 60 | `03` | `0C` | 18400 Hz | provided, [1](../presets/rooms/glass-room.md) |
| 61 | `03` | `0D` | 18800 Hz | provided |
| 62 | `03` | `0E` | 19200 Hz | provided |
| 63 | `03` | `0F` | 19600 Hz | provided |
| 64 | `04` | `00` | 20000 Hz | provided |
| 65 | `04` | `01` | 20400 Hz | provided |
| 66 | `04` | `02` | 20800 Hz | provided |
| 67 | `04` | `03` | 21200 Hz | provided |
| 68 | `04` | `04` | 21600 Hz | provided |
| 69 | `04` | `05` | 22000 Hz | dump, provided |
| 70 | `04` | `06` | Full | dump, provided |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **32:** **Halls:** [Large & Deep](../presets/halls/large-and-deep.md); **Plates:** [Echo Plate](../presets/plates/echo-plate.md), [London Plate](../presets/plates/london-plate.md); **Rooms:** [Large Room](../presets/rooms/large-room.md), [Small Room](../presets/rooms/small-room.md), [Small Vox Room](../presets/rooms/small-vox-room.md)
- **38:** **Chambers:** [Snare Chamber](../presets/chambers/snare-chamber.md); **Halls:** [Medium & Deep](../presets/halls/medium-and-deep.md), [Small & Near](../presets/halls/small-and-near.md); **Plates:** [CD Plate A](../presets/plates/cd-plate-a.md), [CD Plate B](../presets/plates/cd-plate-b.md), [Fat Plate](../presets/plates/fat-plate.md), [Gold Plate](../presets/plates/gold-plate.md), [Large Plate](../presets/plates/large-plate.md); **Spaces:** [Scoring Stage](../presets/spaces/scoring-stage.md)
- **39:** **Chambers:** [Large Chamber](../presets/chambers/large-chamber.md), [Medium Chamber](../presets/chambers/medium-chamber.md), [Small Chamber](../presets/chambers/small-chamber.md); **Halls:** [The ArchDuke](../presets/halls/the-archduke.md); **Plates:** [Small Plate](../presets/plates/small-plate.md); **Rooms:** [Center Room](../presets/rooms/center-room.md), [Studio B Far](../presets/rooms/studio-b-far.md)
- **40:** **Ambience:** [Deep Ambience](../presets/ambience/deep-ambience.md), [Large Ambience](../presets/ambience/large-ambience.md), [Long Ambience](../presets/ambience/long-ambience.md); **Chambers:** [Amb Chamber B](../presets/chambers/amb-chamber-b.md), [CD Chamber](../presets/chambers/cd-chamber.md), [Deep Chamber](../presets/chambers/deep-chamber.md); **Halls:** [Boston Hall B](../presets/halls/boston-hall-b.md), [Large & Near](../presets/halls/large-and-near.md); **Plates:** [Bright Plate](../presets/plates/bright-plate.md), [Silver Plate](../presets/plates/silver-plate.md), [Snare Plate B](../presets/plates/snare-plate-b.md); **Rooms:** [Large Wooden](../presets/rooms/large-wooden.md), [Small Wooden](../presets/rooms/small-wooden.md)
- **44:** **Chambers:** [A&M Chamber](../presets/chambers/a-and-m-chamber.md), [Amb Chamber A](../presets/chambers/amb-chamber-a.md); **Plates:** [Snare Plate A](../presets/plates/snare-plate-a.md); **Rooms:** [Front Room](../presets/rooms/front-room.md), [Studio E](../presets/rooms/studio-e.md); **Spaces:** [North Church](../presets/spaces/north-church.md), [Stone Quarry](../presets/spaces/stone-quarry.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 126 | Offset 127 | `nibble_hilo` | Offset 92 | Offset 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 80 Hz | `00` | `00` | 0 | `02` | `01` | `01` `05` `03` `00` | dump |
| 120 Hz | `00` | `01` | 1 | `00` | `02` | `09` `04` `02` `02` | dump |
| 280 Hz | `00` | `05` | 5 | `02` | `04` | `0C` `09` `0F` `0D` | dump |
| 480 Hz | `00` | `09` | 9 | `00` | `05` | `01` `0E` `03` `0D` | dump |
| 13600 Hz | `03` | `00` | 48 | `00` | `07` | `02` `0D` `0B` `01` | dump |
| 22000 Hz | `04` | `05` | 69 | `00` | `08` | `08` `0F` `00` `0A` | dump |
| full | `04` | `06` | 70 | `00` | `09` | `00` `04` `0C` `08` | dump |

## Interpretation

- **Primary field:** offsets **126-127**, encoding `nibble_hilo` (table/index candidate (monotonic 100%)).
- **Confidence:** medium (0/6 dumps matched, 100%).
- **Catalog hint (Bricasti):** Early Rolloff - printed 80 ... 20000 hz [differs_from_hint] - hint only; dumps win.
- **Catalog notes:** Non-linear Hz table @ 126-127.
- **Catalog note:** Observed max 22000 is above catalog hint ceiling 20000 hz (hardware wins)
- **Range:** Observed range 80 ... 22000 Hz.
- **HIGH/FULL endpoint:** `full.syx` -> encoded 70 - encoded 70 is 1 step(s) above 22000 Hz (encoded 69); absolute unit value unknown (likely a non-linear table / 'full' max)..
- **Sampling:** extremes, adjacents, 3 sample mid(s) (not every step).
- **How to set:**
  1. Use the per-dump mapping table in encoding_hypotheses until a closed-form scale is confirmed
  2. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 92, 147 (likely edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Other parameters

- [Delay Level](delay-level.md)
- [Delay Modulation](delay-modulation.md)
- [Delay Time](delay-time.md)
- [Density](density.md)
- [Diffusion](diffusion.md)
- **Early Rolloff** (this page)
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
