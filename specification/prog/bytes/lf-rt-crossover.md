[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# LF RT Crossover

_Generated 2026-07-22. Source folder: `sysex/prog/parameters/lf rt crossover/`._

## SysEx summary

- **Offsets:** 120-121
- **Encoding:** `nibble_hilo`
- **Confidence:** medium
- **Range:** Range 80 ... 4800 Hz (capture extremes)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Sets the crossover frequency used by LF RT Multiply.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| `nibble_hilo` | Offset 120 | Offset 121 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | 80 Hz | dump, provided |
| 1 | `00` | `01` | 120 Hz | dump, provided, [1](../presets/spaces/car-park.md) |
| 2 | `00` | `02` | 160 Hz | dump, provided, [1](../presets/halls/dense-hall.md) |
| 3 | `00` | `03` | 200 Hz | provided, [1](../presets/spaces/stone-quarry.md) |
| 4 | `00` | `04` | 240 Hz | provided, [1](../presets/plates/fat-plate.md), [2](../presets/spaces/redwood-valley.md) |
| 5 | `00` | `05` | 280 Hz | provided, [1](../presets/halls/boston-hall-a.md), [2](../presets/rooms/back-room.md) |
| 6 | `00` | `06` | 320 Hz | provided, [1](../presets/halls/berliner-hall.md), [2](../presets/rooms/studio-d.md) |
| 7 | `00` | `07` | 360 Hz | provided, [1](../presets/halls/worcester-hall.md) |
| 8 | `00` | `08` | 400 Hz | dump, provided, [1](../presets/halls/clear-hall.md), [2](../presets/plates/cd-plate-b.md), [3](../presets/plates/small-plate.md) |
| 9 | `00` | `09` | 480 Hz | provided, [1](../presets/plates/gold-plate.md), [2](../presets/rooms/center-room.md), [3](../presets/rooms/front-room.md), [4](../presets/rooms/studio-b-far.md), [5](../presets/spaces/tanglewood.md) |
| 10 | `00` | `0A` | 560 Hz | provided, [1](../presets/ambience/large-and-dark.md), [2](../presets/ambience/medium-and-dark.md), [3](../presets/ambience/small-and-dark.md), [4](../presets/chambers/old-chamber.md), [5](../presets/halls/concert-hall.md), +3 more |
| 11 | `00` | `0B` | 640 Hz | provided, [1](../presets/chambers/kick-chamber.md), [2](../presets/halls/amsterdam-hall.md), [3](../presets/rooms/small-q-room.md), [4](../presets/spaces/arena.md), [5](../presets/spaces/bath-house.md), +2 more |
| 12 | `00` | `0C` | 720 Hz | dump, provided, [1](../presets/chambers/large-chamber.md), [2](../presets/chambers/small-chamber.md), [3](../presets/halls/boston-hall-b.md), [4](../presets/halls/large-and-deep.md), [5](../presets/halls/large-and-near.md), +3 more |
| 13 | `00` | `0D` | 800 Hz | provided, [1](../presets/ambience/deep-ambience.md), [2](../presets/ambience/large-and-bright.md), [3](../presets/ambience/large-ambience.md), [4](../presets/ambience/long-ambience.md), [5](../presets/ambience/small-and-bright.md), +21 more |
| 14 | `00` | `0E` | 1000 Hz | provided, [1](../presets/ambience/bass-xxl.md), [2](../presets/ambience/clear-ambience.md), [3](../presets/chambers/amb-chamber-a.md), [4](../presets/chambers/amb-chamber-b.md), [5](../presets/chambers/deep-chamber.md), +12 more |
| 15 | `00` | `0F` | 1200 Hz | provided, [1](../presets/plates/bright-plate.md), [2](../presets/plates/percussion.md), [3](../presets/rooms/studio-a.md) |
| 16 | `01` | `00` | 1400 Hz | provided, [1](../presets/rooms/large-tiled.md), [2](../presets/rooms/small-tiled.md) |
| 17 | `01` | `01` | 1600 Hz | provided, [1](../presets/rooms/glass-room.md), [2](../presets/rooms/marble-foyer.md) |
| 18 | `01` | `02` | 1800 Hz | provided |
| 19 | `01` | `03` | 2000 Hz | provided, [1](../presets/rooms/small-vox-room.md) |
| 20 | `01` | `04` | 2400 Hz | provided, [1](../presets/ambience/percussion-air.md) |
| 21 | `01` | `05` | 2800 Hz | provided |
| 22 | `01` | `06` | 3200 Hz | provided |
| 23 | `01` | `07` | 3600 Hz | provided |
| 24 | `01` | `08` | 4000 Hz | dump, provided, [1](../presets/plates/crystal-plate.md) |
| 25 | `01` | `09` | 4400 Hz | dump, provided |
| 26 | `01` | `0A` | 4800 Hz | dump, provided |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **10:** **Ambience:** [Large & Dark](../presets/ambience/large-and-dark.md), [Medium & Dark](../presets/ambience/medium-and-dark.md), [Small & Dark](../presets/ambience/small-and-dark.md); **Chambers:** [Old Chamber](../presets/chambers/old-chamber.md); **Halls:** [Concert Hall](../presets/halls/concert-hall.md); **Rooms:** [Heavy Room](../presets/rooms/heavy-room.md), [Studio C](../presets/rooms/studio-c.md), [Studio E](../presets/rooms/studio-e.md)
- **11:** **Chambers:** [Kick Chamber](../presets/chambers/kick-chamber.md); **Halls:** [Amsterdam Hall](../presets/halls/amsterdam-hall.md); **Rooms:** [Small Q Room](../presets/rooms/small-q-room.md); **Spaces:** [Arena](../presets/spaces/arena.md), [Bath House](../presets/spaces/bath-house.md), [East Church](../presets/spaces/east-church.md), [North Church](../presets/spaces/north-church.md)
- **12:** **Chambers:** [Large Chamber](../presets/chambers/large-chamber.md), [Small Chamber](../presets/chambers/small-chamber.md); **Halls:** [Boston Hall B](../presets/halls/boston-hall-b.md), [Large & Deep](../presets/halls/large-and-deep.md), [Large & Near](../presets/halls/large-and-near.md), [The ArchDuke](../presets/halls/the-archduke.md), [Vienna Hall](../presets/halls/vienna-hall.md); **Spaces:** [Scoring Stage](../presets/spaces/scoring-stage.md)
- **13:** **Ambience:** [Deep Ambience](../presets/ambience/deep-ambience.md), [Large & Bright](../presets/ambience/large-and-bright.md), [Large Ambience](../presets/ambience/large-ambience.md), [Long Ambience](../presets/ambience/long-ambience.md), [Small & Bright](../presets/ambience/small-and-bright.md); **Chambers:** [A&M Chamber](../presets/chambers/a-and-m-chamber.md), [CD Chamber](../presets/chambers/cd-chamber.md), [Large & Bright](../presets/chambers/large-and-bright.md), [Medium Chamber](../presets/chambers/medium-chamber.md), [Snare Chamber](../presets/chambers/snare-chamber.md); **Halls:** [Brass Hall](../presets/halls/brass-hall.md), [Chicago Hall](../presets/halls/chicago-hall.md), [Large Hall](../presets/halls/large-hall.md), [Medium & Deep](../presets/halls/medium-and-deep.md), [Medium & Near](../presets/halls/medium-and-near.md), [Medium Hall](../presets/halls/medium-hall.md), [Small & Near](../presets/halls/small-and-near.md), [Small Hall](../presets/halls/small-hall.md); **Plates:** [Dark Plate](../presets/plates/dark-plate.md), [Large Plate](../presets/plates/large-plate.md), [London Plate](../presets/plates/london-plate.md), [Snare Plate B](../presets/plates/snare-plate-b.md); **Rooms:** [Large Q Room](../presets/rooms/large-q-room.md), [Large Room](../presets/rooms/large-room.md), [Music Room](../presets/rooms/music-room.md); **Spaces:** [West Church](../presets/spaces/west-church.md)
- **14:** **Ambience:** [Bass  XXL](../presets/ambience/bass-xxl.md), [Clear Ambience](../presets/ambience/clear-ambience.md); **Chambers:** [Amb Chamber A](../presets/chambers/amb-chamber-a.md), [Amb Chamber B](../presets/chambers/amb-chamber-b.md), [Deep Chamber](../presets/chambers/deep-chamber.md); **Halls:** [Sandors Hall](../presets/halls/sandors-hall.md); **Plates:** [CD Plate A](../presets/plates/cd-plate-a.md), [Dense Plate](../presets/plates/dense-plate.md), [Echo Plate](../presets/plates/echo-plate.md), [Silver Plate](../presets/plates/silver-plate.md), [Snare Plate A](../presets/plates/snare-plate-a.md); **Rooms:** [Deep Stone](../presets/rooms/deep-stone.md), [Drum & Chamber](../presets/rooms/drum-and-chamber.md), [Large Wooden](../presets/rooms/large-wooden.md), [Small Room](../presets/rooms/small-room.md), [Small Wooden](../presets/rooms/small-wooden.md); **Spaces:** [Cinema Room](../presets/spaces/cinema-room.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 120 | Offset 121 | `nibble_hilo` | Display lo 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 80 Hz | `00` | `00` | 0 | `07` | `01` `0B` `0F` `08` | dump |
| 120 Hz | `00` | `01` | 1 | `07` | `0D` `0B` `06` `09` | dump |
| 160 Hz | `00` | `02` | 2 | `08` | `0D` `0B` `08` `0D` | dump |
| 400 Hz | `00` | `08` | 8 | `09` | `01` `0E` `01` `00` | dump |
| 720 Hz | `00` | `0C` | 12 | `0A` | `0D` `0C` `01` `05` | dump |
| 4000 Hz | `01` | `08` | 24 | `0B` | `07` `02` `06` `08` | dump |
| 4400 Hz | `01` | `09` | 25 | `0C` | `07` `02` `04` `0C` | dump |
| 4800 Hz | `01` | `0A` | 26 | `0D` | `0B` `03` `0C` `01` | dump |

## Interpretation

- **Primary field:** offsets **120-121**, encoding `nibble_hilo` (table/index candidate (monotonic 100%)).
- **Confidence:** medium (0/8 dumps matched, 100%).
- **Catalog hint (Bricasti):** LF RT Crossover - printed 80 ... 4800 hz [match] - hint only; dumps win.
- **Catalog notes:** Own Hz table @ 120-121 (not HF's).
- **Range:** Range 80 ... 4800 Hz (capture extremes).
- **Sampling:** extremes, adjacents, 4 sample mid(s) (not every step).
- **Edge slopes:** Low and high extreme->adjacent slopes disagree - prefer a table/index interpretation over a partial closed-form scale.
- **How to set:**
  1. Use the per-dump mapping table in encoding_hypotheses until a closed-form scale is confirmed
  2. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 147 (display low nibble) (edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Unseen values

Documented in the spec (encoding map / manual) but not yet witnessed in a committed dump. "Possible" spans every encoded step in this field's range; missing steps are listed as ranges when there are many.

- **Encoding range:** encoded 0–26 (27 steps documented).
- **Never captured on the wire (19):** encoded 3–7, 9–11, 13–23 — see the [encoding map](#encoding-map) above for each label.
- **Documented gaps (no row at all):** none between documented min/max.
- **Wire nibbles never observed (`0`–`F`):** offset 120 (high): `2` `3` `4` `5` `6` `7` `8` `9` `A` `B` `C` `D` `E` `F`; offset 121 (low): none

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
- **LF RT Crossover** (this page)
- [LF RT Multiply](lf-rt-multiply.md)
- [Modulation](modulation.md)
- [Pre Delay](predelay.md)
- [Reverb Time](reverb-time.md)
- [Rolloff](rolloff.md)
- [Size](size.md)
- [VLF Cut](vlf-cut.md)
