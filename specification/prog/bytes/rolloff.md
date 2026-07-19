[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Rolloff

_Generated 2026-07-19. Source folder: `sysex/prog/parameters/rolloff/`._

## SysEx summary

- **Offsets:** 112-113
- **Encoding:** `nibble_hilo`
- **Confidence:** medium
- **Range:** Observed range 80 ... 22000 Hz
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Low pass filter applied to the overall output of the reverb.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| `nibble_hilo` | Offset 112 | Offset 113 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | 80 Hz | dump, provided |
| 1 | `00` | `01` | 120 Hz | dump, provided |
| 2 | `00` | `02` | 160 Hz | dump, provided |
| 3 | `00` | `03` | 200 Hz | dump, provided, [1](../presets/ambience/bass-xxl.md) |
| 4 | `00` | `04` | 240 Hz | provided |
| 5 | `00` | `05` | 280 Hz | provided |
| 6 | `00` | `06` | 320 Hz | provided |
| 7 | `00` | `07` | 360 Hz | provided |
| 8 | `00` | `08` | 400 Hz | provided |
| 9 | `00` | `09` | 480 Hz | provided |
| 10 | `00` | `0A` | 560 Hz | provided |
| 11 | `00` | `0B` | 640 Hz | provided |
| 12 | `00` | `0C` | 720 Hz | provided |
| 13 | `00` | `0D` | 800 Hz | dump, provided |
| 14 | `00` | `0E` | 1000 Hz | provided |
| 15 | `00` | `0F` | 1200 Hz | provided |
| 16 | `01` | `00` | 1400 Hz | provided |
| 17 | `01` | `01` | 1600 Hz | provided |
| 18 | `01` | `02` | 1800 Hz | provided |
| 19 | `01` | `03` | 2000 Hz | dump, provided, [1](../presets/spaces/car-park.md) |
| 20 | `01` | `04` | 2400 Hz | provided |
| 21 | `01` | `05` | 2800 Hz | provided, [1](../presets/ambience/small-and-dark.md) |
| 22 | `01` | `06` | 3200 Hz | dump, provided, [1](../presets/ambience/large-and-dark.md), [2](../presets/ambience/medium-and-dark.md), [3](../presets/spaces/redwood-valley.md) |
| 23 | `01` | `07` | 3600 Hz | provided, [1](../presets/spaces/stone-quarry.md) |
| 24 | `01` | `08` | 4000 Hz | provided |
| 25 | `01` | `09` | 4400 Hz | provided, [1](../presets/plates/london-plate.md) |
| 26 | `01` | `0A` | 4800 Hz | provided, [1](../presets/halls/boston-hall-b.md), [2](../presets/halls/large-and-dark.md), [3](../presets/plates/dark-plate.md), [4](../presets/plates/large-plate.md), [5](../presets/rooms/large-q-room.md), +4 more |
| 27 | `01` | `0B` | 5200 Hz | dump, provided, [1](../presets/halls/concert-hall.md), [2](../presets/halls/large-and-deep.md), [3](../presets/halls/large-hall.md), [4](../presets/halls/the-archduke.md), [5](../presets/plates/gold-plate.md), +3 more |
| 28 | `01` | `0C` | 5600 Hz | provided, [1](../presets/ambience/deep-ambience.md), [2](../presets/ambience/long-ambience.md), [3](../presets/chambers/snare-chamber.md), [4](../presets/halls/chicago-hall.md), [5](../presets/halls/dense-hall.md), +15 more |
| 29 | `01` | `0D` | 6000 Hz | provided, [1](../presets/ambience/large-ambience.md), [2](../presets/chambers/amb-chamber-b.md), [3](../presets/chambers/cd-chamber.md), [4](../presets/halls/boston-hall-a.md), [5](../presets/halls/gold-hall.md), +4 more |
| 30 | `01` | `0E` | 6400 Hz | provided, [1](../presets/ambience/clear-ambience.md), [2](../presets/chambers/a-and-m-chamber.md), [3](../presets/chambers/deep-chamber.md), [4](../presets/chambers/large-chamber.md), [5](../presets/chambers/medium-chamber.md), +7 more |
| 31 | `01` | `0F` | 6800 Hz | dump, provided, [1](../presets/halls/amsterdam-hall.md), [2](../presets/halls/clear-hall.md), [3](../presets/plates/snare-plate-a.md), [4](../presets/rooms/small-room.md) |
| 32 | `02` | `00` | 7200 Hz | provided, [1](../presets/plates/snare-plate-b.md), [2](../presets/rooms/small-vox-room.md), [3](../presets/rooms/studio-c.md), [4](../presets/rooms/studio-d.md) |
| 33 | `02` | `01` | 7600 Hz | provided, [1](../presets/chambers/amb-chamber-a.md), [2](../presets/halls/worcester-hall.md), [3](../presets/rooms/music-room.md), [4](../presets/spaces/scoring-stage.md) |
| 34 | `02` | `02` | 8000 Hz | provided, [1](../presets/ambience/large-and-bright.md), [2](../presets/ambience/percussion-air.md), [3](../presets/ambience/small-and-bright.md), [4](../presets/chambers/large-and-bright.md), [5](../presets/rooms/large-wooden.md), +1 more |
| 35 | `02` | `03` | 8400 Hz | provided, [1](../presets/halls/brass-hall.md), [2](../presets/rooms/studio-a.md) |
| 36 | `02` | `04` | 8800 Hz | provided, [1](../presets/plates/silver-plate.md), [2](../presets/spaces/bath-house.md) |
| 37 | `02` | `05` | 9200 Hz | provided, [1](../presets/rooms/studio-b-far.md) |
| 38 | `02` | `06` | 9600 Hz | provided, [1](../presets/rooms/heavy-room.md), [2](../presets/rooms/large-tiled.md), [3](../presets/rooms/small-tiled.md), [4](../presets/rooms/small-wooden.md) |
| 39 | `02` | `07` | 10000 Hz | provided |
| 40 | `02` | `08` | 10400 Hz | provided |
| 41 | `02` | `09` | 10800 Hz | provided |
| 42 | `02` | `0A` | 11200 Hz | provided |
| 43 | `02` | `0B` | 11600 Hz | provided |
| 44 | `02` | `0C` | 12000 Hz | provided, [1](../presets/plates/crystal-plate.md) |
| 45 | `02` | `0D` | 12400 Hz | provided |
| 46 | `02` | `0E` | 12800 Hz | provided |
| 47 | `02` | `0F` | 13200 Hz | provided |
| 48 | `03` | `00` | 13600 Hz | provided |
| 49 | `03` | `01` | 14000 Hz | provided |
| 50 | `03` | `02` | 14400 Hz | provided |
| 51 | `03` | `03` | 14800 Hz | provided |
| 52 | `03` | `04` | 15200 Hz | provided |
| 53 | `03` | `05` | 15600 Hz | provided |
| 54 | `03` | `06` | 16000 Hz | provided |
| 55 | `03` | `07` | 16400 Hz | provided |
| 56 | `03` | `08` | 16800 Hz | provided |
| 57 | `03` | `09` | 17200 Hz | provided |
| 58 | `03` | `0A` | 17600 Hz | provided |
| 59 | `03` | `0B` | 18000 Hz | provided |
| 60 | `03` | `0C` | 18400 Hz | provided |
| 61 | `03` | `0D` | 18800 Hz | provided |
| 62 | `03` | `0E` | 19200 Hz | provided |
| 63 | `03` | `0F` | 19600 Hz | provided |
| 64 | `04` | `00` | 20000 Hz | dump, provided |
| 65 | `04` | `01` | 20400 Hz | provided |
| 66 | `04` | `02` | 20800 Hz | provided |
| 67 | `04` | `03` | 21200 Hz | provided |
| 68 | `04` | `04` | 21600 Hz | provided |
| 69 | `04` | `05` | 22000 Hz | dump, provided |
| 70 | `04` | `06` | Full | dump, provided |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **26:** **Halls:** [Boston Hall B](../presets/halls/boston-hall-b.md), [Large & Dark](../presets/halls/large-and-dark.md); **Plates:** [Dark Plate](../presets/plates/dark-plate.md), [Large Plate](../presets/plates/large-plate.md); **Rooms:** [Large Q Room](../presets/rooms/large-q-room.md), [Studio E](../presets/rooms/studio-e.md); **Spaces:** [Cinema Room](../presets/spaces/cinema-room.md), [Tanglewood](../presets/spaces/tanglewood.md), [West Church](../presets/spaces/west-church.md)
- **27:** **Halls:** [Concert Hall](../presets/halls/concert-hall.md), [Large & Deep](../presets/halls/large-and-deep.md), [Large Hall](../presets/halls/large-hall.md), [The ArchDuke](../presets/halls/the-archduke.md); **Plates:** [Gold Plate](../presets/plates/gold-plate.md), [Percussion](../presets/plates/percussion.md); **Rooms:** [Djangos Room](../presets/rooms/djangos-room.md); **Spaces:** [South Church](../presets/spaces/south-church.md)
- **28:** **Ambience:** [Deep Ambience](../presets/ambience/deep-ambience.md), [Long Ambience](../presets/ambience/long-ambience.md); **Chambers:** [Snare Chamber](../presets/chambers/snare-chamber.md); **Halls:** [Chicago Hall](../presets/halls/chicago-hall.md), [Dense Hall](../presets/halls/dense-hall.md), [Medium & Deep](../presets/halls/medium-and-deep.md), [Sandors Hall](../presets/halls/sandors-hall.md), [Small & Near](../presets/halls/small-and-near.md), [Small Hall](../presets/halls/small-hall.md), [Vienna Hall](../presets/halls/vienna-hall.md); **Plates:** [CD Plate B](../presets/plates/cd-plate-b.md), [Dense Plate](../presets/plates/dense-plate.md), [Echo Plate](../presets/plates/echo-plate.md), [Small Plate](../presets/plates/small-plate.md); **Rooms:** [Back Room](../presets/rooms/back-room.md), [Center Room](../presets/rooms/center-room.md), [Deep Stone](../presets/rooms/deep-stone.md), [Small Q Room](../presets/rooms/small-q-room.md); **Spaces:** [Arena](../presets/spaces/arena.md), [North Church](../presets/spaces/north-church.md)
- **29:** **Ambience:** [Large Ambience](../presets/ambience/large-ambience.md); **Chambers:** [Amb Chamber B](../presets/chambers/amb-chamber-b.md), [CD Chamber](../presets/chambers/cd-chamber.md); **Halls:** [Boston Hall A](../presets/halls/boston-hall-a.md), [Gold Hall](../presets/halls/gold-hall.md), [Large & Near](../presets/halls/large-and-near.md); **Plates:** [Fat Plate](../presets/plates/fat-plate.md); **Rooms:** [Front Room](../presets/rooms/front-room.md), [Large Room](../presets/rooms/large-room.md)
- **30:** **Ambience:** [Clear Ambience](../presets/ambience/clear-ambience.md); **Chambers:** [A&M Chamber](../presets/chambers/a-and-m-chamber.md), [Deep Chamber](../presets/chambers/deep-chamber.md), [Large Chamber](../presets/chambers/large-chamber.md), [Medium Chamber](../presets/chambers/medium-chamber.md), [Old Chamber](../presets/chambers/old-chamber.md), [Small Chamber](../presets/chambers/small-chamber.md); **Halls:** [Berliner Hall](../presets/halls/berliner-hall.md); **Plates:** [CD Plate A](../presets/plates/cd-plate-a.md); **Rooms:** [Drum & Chamber](../presets/rooms/drum-and-chamber.md), [Glass Room](../presets/rooms/glass-room.md), [Marble Foyer](../presets/rooms/marble-foyer.md)
- **34:** **Ambience:** [Large & Bright](../presets/ambience/large-and-bright.md), [Percussion Air](../presets/ambience/percussion-air.md), [Small & Bright](../presets/ambience/small-and-bright.md); **Chambers:** [Large & Bright](../presets/chambers/large-and-bright.md); **Rooms:** [Large Wooden](../presets/rooms/large-wooden.md); **Spaces:** [East Church](../presets/spaces/east-church.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 112 | Offset 113 | `nibble_hilo` | Display 146–147 | display `nibble_hilo` | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 80 Hz | `00` | `00` | 0 | `04 0D` | 77 | `04` `0C` `00` `0C` | dump |
| 120 Hz | `00` | `01` | 1 | `04 0E` | 78 | `0E` `00` `04` `00` | dump |
| 160 Hz | `00` | `02` | 2 | `05 00` | 80 | `04` `04` `03` `03` | dump |
| 200 Hz | `00` | `03` | 3 | `05 01` | 81 | `02` `08` `00` `06` | dump |
| 800 Hz | `00` | `0D` | 13 | `05 03` | 83 | `0A` `00` `00` `06` | dump |
| 2000 Hz | `01` | `03` | 19 | `05 04` | 84 | `0E` `0E` `06` `07` | dump |
| 3200 Hz | `01` | `06` | 22 | `05 04` | 84 | `07` `02` `04` `09` | dump |
| 5200 Hz | `01` | `0B` | 27 | `05 05` | 85 | `04` `0E` `01` `06` | dump |
| 6800 Hz | `01` | `0F` | 31 | `05 06` | 86 | `07` `0E` `07` `04` | dump |
| 20000 Hz | `04` | `00` | 64 | `05 08` | 88 | `04` `07` `07` `00` | dump |
| 22000 Hz | `04` | `05` | 69 | `05 09` | 89 | `01` `0B` `06` `03` | dump |
| full | `04` | `06` | 70 | `05 0A` | 90 | `0A` `0F` `03` `0C` | dump |

## Interpretation

- **Primary field:** offsets **112-113**, encoding `nibble_hilo` (table/index candidate (monotonic 100%)).
- **Confidence:** medium (0/11 dumps matched, 100%).
- **Catalog hint (Bricasti):** Rolloff - printed 80 ... 28000 hz [match] - hint only; dumps win.
- **Catalog notes:** Manual max 28 kHz; FULL may sit above the last numbered Hz. Filter order (dB/octave) analysis: [rolloff-slopes.md](../../../docs/rolloff-slopes.md).
- **Range:** Observed range 80 ... 22000 Hz.
- **HIGH/FULL endpoint:** `full.syx` -> encoded 70 - encoded 70 is 1 step(s) above 22000 Hz (encoded 69); absolute unit value unknown (likely a non-linear table / 'full' max)..
- **Sampling:** extremes, adjacents, 8 sample mid(s) (not every step).
- **How to set:**
  1. Use the per-dump mapping table in encoding_hypotheses until a closed-form scale is confirmed
  2. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 146–147 (`nibble_hilo` display) (edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Unseen values

Documented in the spec (encoding map / manual) but not yet witnessed in a committed dump. "Possible" spans every encoded step in this field's range; missing steps are listed as ranges when there are many.

- **Encoding range:** encoded 0–70 (71 steps documented).
- **Manual range not fully captured:** manual ceiling 28000 above captured max 22000.
- **Never captured on the wire (59):** encoded 4–12, 14–18, 20–21, 23–26, 28–30, 32–63, 65–68 — see the [encoding map](#encoding-map) above for each label.
- **Documented gaps (no row at all):** none between documented min/max.
- **Wire nibbles never observed (`0`–`F`):** offset 112 (high): `5` `6` `7` `8` `9` `A` `B` `C` `D` `E` `F`; offset 113 (low): none

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
- [Modulation](modulation.md)
- [Pre Delay](predelay.md)
- [Reverb Time](reverb-time.md)
- **Rolloff** (this page)
- [Size](size.md)
- [VLF Cut](vlf-cut.md)
