[Overview](../README.md) | [Parameters](../parameters/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# HF RT Crossover

_Generated 2026-07-18. Source folder: `sysex/prog/parameters/hf rt crossover/`._

## SysEx summary

- **Offsets:** 116-117
- **Encoding:** `nibble_hilo`
- **Confidence:** medium
- **Range:** Range 200 ... 16000 Hz (capture extremes)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Sets the crossover frequency used by HF RT Multiply.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| Encoded | Offset 116 | Offset 117 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | 200 Hz | dump, provided |
| 1 | `00` | `01` | 240 Hz | dump, provided |
| 2 | `00` | `02` | 280 Hz | provided |
| 3 | `00` | `03` | 320 Hz | provided, [1](../presets/ambience/bass-xxl.md) |
| 4 | `00` | `04` | 360 Hz | provided |
| 5 | `00` | `05` | 400 Hz | provided |
| 6 | `00` | `06` | 480 Hz | dump, provided |
| 7 | `00` | `07` | 560 Hz | provided |
| 8 | `00` | `08` | 640 Hz | provided |
| 9 | `00` | `09` | 720 Hz | provided |
| 10 | `00` | `0A` | 800 Hz | provided, [1](../presets/spaces/stone-quarry.md) |
| 11 | `00` | `0B` | 1000 Hz | provided, [1](../presets/rooms/large-q-room.md), [2](../presets/spaces/bath-house.md), [3](../presets/spaces/west-church.md) |
| 12 | `00` | `0C` | 1200 Hz | dump, provided, [1](../presets/spaces/south-church.md) |
| 13 | `00` | `0D` | 1400 Hz | provided |
| 14 | `00` | `0E` | 1600 Hz | provided, [1](../presets/spaces/car-park.md) |
| 15 | `00` | `0F` | 1800 Hz | provided, [1](../presets/halls/worcester-hall.md), [2](../presets/rooms/small-vox-room.md) |
| 16 | `01` | `00` | 2000 Hz | provided, [1](../presets/rooms/small-room.md), [2](../presets/rooms/studio-b-far.md), [3](../presets/spaces/tanglewood.md) |
| 17 | `01` | `01` | 2400 Hz | provided, [1](../presets/ambience/percussion-air.md), [2](../presets/ambience/small-and-dark.md), [3](../presets/rooms/large-room.md), [4](../presets/spaces/cinema-room.md), [5](../presets/spaces/north-church.md), +1 more |
| 18 | `01` | `02` | 2800 Hz | provided, [1](../presets/ambience/large-and-dark.md), [2](../presets/ambience/medium-and-dark.md), [3](../presets/halls/boston-hall-b.md), [4](../presets/halls/dense-hall.md), [5](../presets/halls/large-and-dark.md), +6 more |
| 19 | `01` | `03` | 3200 Hz | provided, [1](../presets/chambers/cd-chamber.md), [2](../presets/chambers/old-chamber.md), [3](../presets/halls/berliner-hall.md), [4](../presets/halls/chicago-hall.md), [5](../presets/halls/concert-hall.md), +9 more |
| 20 | `01` | `04` | 3600 Hz | dump, provided, [1](../presets/ambience/large-ambience.md), [2](../presets/ambience/long-ambience.md), [3](../presets/halls/amsterdam-hall.md), [4](../presets/halls/boston-hall-a.md), [5](../presets/halls/sandors-hall.md), +9 more |
| 21 | `01` | `05` | 4000 Hz | provided, [1](../presets/ambience/deep-ambience.md), [2](../presets/chambers/deep-chamber.md), [3](../presets/chambers/large-chamber.md), [4](../presets/halls/large-and-deep.md), [5](../presets/halls/medium-and-deep.md), +4 more |
| 22 | `01` | `06` | 4800 Hz | provided, [1](../presets/ambience/clear-ambience.md), [2](../presets/chambers/amb-chamber-b.md), [3](../presets/chambers/kick-chamber.md), [4](../presets/chambers/large-and-bright.md), [5](../presets/chambers/medium-chamber.md), +9 more |
| 23 | `01` | `07` | 5600 Hz | provided, [1](../presets/ambience/large-and-bright.md), [2](../presets/ambience/small-and-bright.md), [3](../presets/chambers/a-and-m-chamber.md), [4](../presets/chambers/amb-chamber-a.md), [5](../presets/plates/bright-plate.md), +5 more |
| 24 | `01` | `08` | 6400 Hz | dump, provided, [1](../presets/halls/gold-hall.md), [2](../presets/rooms/large-tiled.md), [3](../presets/rooms/small-tiled.md), [4](../presets/rooms/studio-a.md) |
| 25 | `01` | `09` | 7200 Hz | provided, [1](../presets/rooms/heavy-room.md), [2](../presets/rooms/small-wooden.md) |
| 26 | `01` | `0A` | 8000 Hz | provided |
| 27 | `01` | `0B` | 8800 Hz | provided |
| 28 | `01` | `0C` | 9600 Hz | dump, provided |
| 29 | `01` | `0D` | 10400 Hz | provided |
| 30 | `01` | `0E` | 11200 Hz | dump, provided |
| 31 | `01` | `0F` | 12000 Hz | provided |
| 32 | `02` | `00` | 12800 Hz | provided |
| 33 | `02` | `01` | 13600 Hz | dump, provided |
| 34 | `02` | `02` | 14400 Hz | provided |
| 35 | `02` | `03` | 15200 Hz | provided |
| 36 | `02` | `04` | 16000 Hz | dump, provided |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **17:** **Ambience:** [Percussion Air](../presets/ambience/percussion-air.md), [Small & Dark](../presets/ambience/small-and-dark.md); **Rooms:** [Large Room](../presets/rooms/large-room.md); **Spaces:** [Cinema Room](../presets/spaces/cinema-room.md), [North Church](../presets/spaces/north-church.md), [Scoring Stage](../presets/spaces/scoring-stage.md)
- **18:** **Ambience:** [Large & Dark](../presets/ambience/large-and-dark.md), [Medium & Dark](../presets/ambience/medium-and-dark.md); **Halls:** [Boston Hall B](../presets/halls/boston-hall-b.md), [Dense Hall](../presets/halls/dense-hall.md), [Large & Dark](../presets/halls/large-and-dark.md), [Vienna Hall](../presets/halls/vienna-hall.md); **Plates:** [CD Plate B](../presets/plates/cd-plate-b.md), [Crystal Plate](../presets/plates/crystal-plate.md); **Rooms:** [Small Q Room](../presets/rooms/small-q-room.md); **Spaces:** [Arena](../presets/spaces/arena.md), [East Church](../presets/spaces/east-church.md)
- **19:** **Chambers:** [CD Chamber](../presets/chambers/cd-chamber.md), [Old Chamber](../presets/chambers/old-chamber.md); **Halls:** [Berliner Hall](../presets/halls/berliner-hall.md), [Chicago Hall](../presets/halls/chicago-hall.md), [Concert Hall](../presets/halls/concert-hall.md), [Large & Near](../presets/halls/large-and-near.md), [Large Hall](../presets/halls/large-hall.md), [The ArchDuke](../presets/halls/the-archduke.md); **Plates:** [Large Plate](../presets/plates/large-plate.md), [London Plate](../presets/plates/london-plate.md), [Snare Plate A](../presets/plates/snare-plate-a.md); **Rooms:** [Djangos Room](../presets/rooms/djangos-room.md), [Studio E](../presets/rooms/studio-e.md); **Spaces:** [Redwood Valley](../presets/spaces/redwood-valley.md)
- **20:** **Ambience:** [Large Ambience](../presets/ambience/large-ambience.md), [Long Ambience](../presets/ambience/long-ambience.md); **Halls:** [Amsterdam Hall](../presets/halls/amsterdam-hall.md), [Boston Hall A](../presets/halls/boston-hall-a.md), [Sandors Hall](../presets/halls/sandors-hall.md), [Small & Near](../presets/halls/small-and-near.md), [Small Hall](../presets/halls/small-hall.md); **Plates:** [Fat Plate](../presets/plates/fat-plate.md), [Gold Plate](../presets/plates/gold-plate.md), [Snare Plate B](../presets/plates/snare-plate-b.md); **Rooms:** [Back Room](../presets/rooms/back-room.md), [Center Room](../presets/rooms/center-room.md), [Drum & Chamber](../presets/rooms/drum-and-chamber.md), [Studio C](../presets/rooms/studio-c.md)
- **21:** **Ambience:** [Deep Ambience](../presets/ambience/deep-ambience.md); **Chambers:** [Deep Chamber](../presets/chambers/deep-chamber.md), [Large Chamber](../presets/chambers/large-chamber.md); **Halls:** [Large & Deep](../presets/halls/large-and-deep.md), [Medium & Deep](../presets/halls/medium-and-deep.md); **Plates:** [Dark Plate](../presets/plates/dark-plate.md); **Rooms:** [Front Room](../presets/rooms/front-room.md), [Marble Foyer](../presets/rooms/marble-foyer.md), [Studio D](../presets/rooms/studio-d.md)
- **22:** **Ambience:** [Clear Ambience](../presets/ambience/clear-ambience.md); **Chambers:** [Amb Chamber B](../presets/chambers/amb-chamber-b.md), [Kick Chamber](../presets/chambers/kick-chamber.md), [Large & Bright](../presets/chambers/large-and-bright.md), [Medium Chamber](../presets/chambers/medium-chamber.md), [Small Chamber](../presets/chambers/small-chamber.md), [Snare Chamber](../presets/chambers/snare-chamber.md); **Halls:** [Brass Hall](../presets/halls/brass-hall.md), [Clear Hall](../presets/halls/clear-hall.md); **Plates:** [Dense Plate](../presets/plates/dense-plate.md), [Echo Plate](../presets/plates/echo-plate.md), [Silver Plate](../presets/plates/silver-plate.md), [Small Plate](../presets/plates/small-plate.md); **Rooms:** [Large Wooden](../presets/rooms/large-wooden.md)
- **23:** **Ambience:** [Large & Bright](../presets/ambience/large-and-bright.md), [Small & Bright](../presets/ambience/small-and-bright.md); **Chambers:** [A&M Chamber](../presets/chambers/a-and-m-chamber.md), [Amb Chamber A](../presets/chambers/amb-chamber-a.md); **Plates:** [Bright Plate](../presets/plates/bright-plate.md), [CD Plate A](../presets/plates/cd-plate-a.md), [Percussion](../presets/plates/percussion.md); **Rooms:** [Deep Stone](../presets/rooms/deep-stone.md), [Glass Room](../presets/rooms/glass-room.md), [Music Room](../presets/rooms/music-room.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 116 | Offset 117 | `nibble_hilo` | Offset 146 | Offset 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 200 Hz | `00` | `00` | 0 | `06` | `08` | `0C` `0C` `0A` `03` | dump |
| 240 Hz | `00` | `01` | 1 | `06` | `0A` | `0C` `0C` `0F` `06` | dump |
| 480 Hz | `00` | `06` | 6 | `06` | `0B` | `0C` `0C` `00` `09` | dump |
| 1200 Hz | `00` | `0C` | 12 | `06` | `0C` | `00` `0D` `08` `0E` | dump |
| 3600 Hz | `01` | `04` | 20 | `06` | `0E` | `0D` `01` `05` `0F` | dump |
| 6400 Hz | `01` | `08` | 24 | `06` | `0F` | `01` `00` `0B` `0E` | dump |
| 9600 Hz | `01` | `0C` | 28 | `07` | `02` | `0C` `00` `02` `07` | dump |
| 11200 Hz | `01` | `0E` | 30 | `07` | `03` | `0C` `00` `04` `01` | dump |
| 13600 Hz | `02` | `01` | 33 | `07` | `04` | `02` `07` `01` `0F` | dump |
| 16000 Hz | `02` | `04` | 36 | `07` | `05` | `0E` `07` `0B` `0B` | dump |

## Interpretation

- **Primary field:** offsets **116-117**, encoding `nibble_hilo` (table/index candidate (monotonic 100%)).
- **Confidence:** medium (0/10 dumps matched, 100%).
- **Catalog hint (Bricasti):** HF RT Crossover - printed 200 ... 16000 hz [match] - hint only; dumps win.
- **Catalog notes:** Non-linear Hz table @ 116-117.
- **Range:** Range 200 ... 16000 Hz (capture extremes).
- **Sampling:** extremes, adjacents, 6 sample mid(s) (not every step).
- **Edge slopes:** Low and high extreme->adjacent slopes disagree - prefer a table/index interpretation over a partial closed-form scale.
- **How to set:**
  1. Use the per-dump mapping table in encoding_hypotheses until a closed-form scale is confirmed
  2. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 146-147 (likely edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Other parameters

- [Delay Level](delay-level.md)
- [Delay Modulation](delay-modulation.md)
- [Delay Time](delay-time.md)
- [Density](density.md)
- [Diffusion](diffusion.md)
- [Early Rolloff](early-rolloff.md)
- [Early Select](early-select.md)
- [Early/Reverb Mix](early-to-reverb-mix.md)
- **HF RT Crossover** (this page)
- [HF RT Multiply](hf-rt-multiply.md)
- [LF RT Crossover](lf-rt-crossover.md)
- [LF RT Multiply](lf-rt-multiply.md)
- [Modulation](modulation.md)
- [Pre Delay](predelay.md)
- [Reverb Time](reverb-time.md)
- [Rolloff](rolloff.md)
- [Size](size.md)
- [VLF Cut](vlf-cut.md)
