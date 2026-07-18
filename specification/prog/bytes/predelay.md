[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Pre Delay

_Generated 2026-07-18. Source folder: `sysex/prog/parameters/predelay/`._

## SysEx summary

- **Offsets:** 104-105
- **Encoding:** `nibble_hilo`
- **Confidence:** medium
- **Range:** Range 0 ... 500 ms (capture extremes)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Sets the amount of time which elapses between the input signal and the onset of reverberation.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| `nibble_hilo` | Offset 104 | Offset 105 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | 0 ms | dump, provided, [1](../presets/ambience/bass-xxl.md), [2](../presets/ambience/percussion-air.md), [3](../presets/ambience/small-and-bright.md), [4](../presets/ambience/small-and-dark.md), [5](../presets/chambers/amb-chamber-a.md), +51 more |
| 1 | `00` | `01` | 2 ms | dump, provided, [1](../presets/ambience/medium-and-dark.md), [2](../presets/rooms/center-room.md) |
| 2 | `00` | `02` | 4 ms | dump, provided, [1](../presets/chambers/medium-chamber.md), [2](../presets/rooms/back-room.md), [3](../presets/rooms/djangos-room.md), [4](../presets/rooms/studio-a.md), [5](../presets/spaces/cinema-room.md) |
| 3 | `00` | `03` | 6 ms | provided, [1](../presets/ambience/clear-ambience.md), [2](../presets/spaces/bath-house.md) |
| 4 | `00` | `04` | 8 ms | provided |
| 5 | `00` | `05` | 10 ms | provided, [1](../presets/ambience/large-and-bright.md), [2](../presets/ambience/large-and-dark.md), [3](../presets/ambience/large-ambience.md), [4](../presets/ambience/long-ambience.md), [5](../presets/chambers/large-and-bright.md), +8 more |
| 6 | `00` | `06` | 12 ms | provided |
| 7 | `00` | `07` | 14 ms | provided |
| 8 | `00` | `08` | 16 ms | provided |
| 9 | `00` | `09` | 18 ms | provided, [1](../presets/halls/concert-hall.md), [2](../presets/plates/crystal-plate.md) |
| 10 | `00` | `0A` | 20 ms | provided, [1](../presets/ambience/deep-ambience.md), [2](../presets/chambers/a-and-m-chamber.md), [3](../presets/chambers/cd-chamber.md), [4](../presets/halls/brass-hall.md), [5](../presets/halls/medium-and-deep.md), +4 more |
| 11 | `00` | `0B` | 22 ms | provided |
| 12 | `00` | `0C` | 24 ms | provided, [1](../presets/halls/medium-and-near.md), [2](../presets/halls/medium-hall.md) |
| 13 | `00` | `0D` | 26 ms | provided |
| 14 | `00` | `0E` | 28 ms | provided |
| 15 | `00` | `0F` | 30 ms | provided, [1](../presets/halls/gold-hall.md) |
| 16 | `01` | `00` | 32 ms | provided |
| 17 | `01` | `01` | 34 ms | provided |
| 18 | `01` | `02` | 36 ms | provided |
| 19 | `01` | `03` | 38 ms | provided |
| 20 | `01` | `04` | 40 ms | provided, [1](../presets/halls/large-and-deep.md) |
| 21 | `01` | `05` | 44 ms | provided |
| 22 | `01` | `06` | 48 ms | provided, [1](../presets/spaces/car-park.md) |
| 23 | `01` | `07` | 52 ms | provided |
| 24 | `01` | `08` | 56 ms | provided |
| 25 | `01` | `09` | 60 ms | provided, [1](../presets/plates/echo-plate.md), [2](../presets/rooms/drum-and-chamber.md) |
| 26 | `01` | `0A` | 64 ms | provided |
| 27 | `01` | `0B` | 68 ms | provided |
| 28 | `01` | `0C` | 72 ms | provided |
| 29 | `01` | `0D` | 76 ms | provided |
| 30 | `01` | `0E` | 80 ms | provided, [1](../presets/spaces/arena.md) |
| 31 | `01` | `0F` | 84 ms | provided |
| 32 | `02` | `00` | 88 ms | provided |
| 33 | `02` | `01` | 92 ms | provided |
| 34 | `02` | `02` | 96 ms | provided |
| 35 | `02` | `03` | 100 ms | dump, provided |
| 36 | `02` | `04` | 108 ms | provided |
| 37 | `02` | `05` | 116 ms | provided |
| 38 | `02` | `06` | 124 ms | provided |
| 39 | `02` | `07` | 132 ms | provided |
| 40 | `02` | `08` | 140 ms | provided |
| 41 | `02` | `09` | 148 ms | provided |
| 42 | `02` | `0A` | 156 ms | provided |
| 43 | `02` | `0B` | 164 ms | provided |
| 44 | `02` | `0C` | 172 ms | provided |
| 45 | `02` | `0D` | 180 ms | provided |
| 46 | `02` | `0E` | 188 ms | provided |
| 47 | `02` | `0F` | 196 ms | provided |
| 48 | `03` | `00` | 204 ms | dump, provided |
| 49 | `03` | `01` | 212 ms | provided |
| 50 | `03` | `02` | 220 ms | provided, [1](../presets/spaces/redwood-valley.md) |
| 51 | `03` | `03` | 228 ms | provided |
| 52 | `03` | `04` | 236 ms | provided |
| 53 | `03` | `05` | 244 ms | provided |
| 54 | `03` | `06` | 252 ms | provided |
| 55 | `03` | `07` | 260 ms | provided |
| 56 | `03` | `08` | 268 ms | provided |
| 57 | `03` | `09` | 276 ms | provided |
| 58 | `03` | `0A` | 284 ms | provided |
| 59 | `03` | `0B` | 292 ms | provided |
| 60 | `03` | `0C` | 300 ms | provided |
| 61 | `03` | `0D` | 308 ms | provided |
| 62 | `03` | `0E` | 316 ms | provided |
| 63 | `03` | `0F` | 324 ms | provided |
| 64 | `04` | `00` | 332 ms | provided |
| 65 | `04` | `01` | 340 ms | provided |
| 66 | `04` | `02` | 348 ms | provided |
| 67 | `04` | `03` | 356 ms | provided |
| 68 | `04` | `04` | 364 ms | provided |
| 69 | `04` | `05` | 372 ms | provided |
| 70 | `04` | `06` | 380 ms | provided |
| 71 | `04` | `07` | 388 ms | provided |
| 72 | `04` | `08` | 396 ms | provided |
| 73 | `04` | `09` | 404 ms | provided |
| 74 | `04` | `0A` | 412 ms | provided |
| 75 | `04` | `0B` | 420 ms | provided |
| 76 | `04` | `0C` | 428 ms | provided |
| 77 | `04` | `0D` | 436 ms | provided |
| 78 | `04` | `0E` | 444 ms | provided |
| 79 | `04` | `0F` | 452 ms | provided |
| 80 | `05` | `00` | 460 ms | provided |
| 81 | `05` | `01` | 468 ms | provided |
| 82 | `05` | `02` | 476 ms | provided |
| 83 | `05` | `03` | 484 ms | provided |
| 84 | `05` | `04` | 492 ms | provided |
| 85 | `05` | `05` | 500 ms | dump, provided |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **0:** **Ambience:** [Bass  XXL](../presets/ambience/bass-xxl.md), [Percussion Air](../presets/ambience/percussion-air.md), [Small & Bright](../presets/ambience/small-and-bright.md), [Small & Dark](../presets/ambience/small-and-dark.md); **Chambers:** [Amb Chamber A](../presets/chambers/amb-chamber-a.md), [Amb Chamber B](../presets/chambers/amb-chamber-b.md), [Deep Chamber](../presets/chambers/deep-chamber.md), [Kick Chamber](../presets/chambers/kick-chamber.md), [Old Chamber](../presets/chambers/old-chamber.md), [Small Chamber](../presets/chambers/small-chamber.md); **Halls:** [Amsterdam Hall](../presets/halls/amsterdam-hall.md), [Berliner Hall](../presets/halls/berliner-hall.md), [Boston Hall A](../presets/halls/boston-hall-a.md), [Boston Hall B](../presets/halls/boston-hall-b.md), [Chicago Hall](../presets/halls/chicago-hall.md), [Clear Hall](../presets/halls/clear-hall.md), [Large & Dark](../presets/halls/large-and-dark.md), [Small & Near](../presets/halls/small-and-near.md), [Small Hall](../presets/halls/small-hall.md), [The ArchDuke](../presets/halls/the-archduke.md), [Vienna Hall](../presets/halls/vienna-hall.md), [Worcester Hall](../presets/halls/worcester-hall.md); **Plates:** [Bright Plate](../presets/plates/bright-plate.md), [CD Plate A](../presets/plates/cd-plate-a.md), [CD Plate B](../presets/plates/cd-plate-b.md), [Dark Plate](../presets/plates/dark-plate.md), [Dense Plate](../presets/plates/dense-plate.md), [Fat Plate](../presets/plates/fat-plate.md), [Gold Plate](../presets/plates/gold-plate.md), [Large Plate](../presets/plates/large-plate.md), [London Plate](../presets/plates/london-plate.md), [Percussion](../presets/plates/percussion.md), [Small Plate](../presets/plates/small-plate.md), [Snare Plate A](../presets/plates/snare-plate-a.md); **Rooms:** [Front Room](../presets/rooms/front-room.md), [Glass Room](../presets/rooms/glass-room.md), [Heavy Room](../presets/rooms/heavy-room.md), [Large Q Room](../presets/rooms/large-q-room.md), [Large Room](../presets/rooms/large-room.md), [Large Tiled](../presets/rooms/large-tiled.md), [Large Wooden](../presets/rooms/large-wooden.md), [Music Room](../presets/rooms/music-room.md), [Small Room](../presets/rooms/small-room.md), [Small Tiled](../presets/rooms/small-tiled.md), [Small Vox Room](../presets/rooms/small-vox-room.md), [Small Wooden](../presets/rooms/small-wooden.md), [Studio B Far](../presets/rooms/studio-b-far.md), [Studio C](../presets/rooms/studio-c.md), [Studio D](../presets/rooms/studio-d.md), [Studio E](../presets/rooms/studio-e.md); **Spaces:** [East Church](../presets/spaces/east-church.md), [North Church](../presets/spaces/north-church.md), [Scoring Stage](../presets/spaces/scoring-stage.md), [South Church](../presets/spaces/south-church.md), [Stone Quarry](../presets/spaces/stone-quarry.md), [West Church](../presets/spaces/west-church.md)
- **5:** **Ambience:** [Large & Bright](../presets/ambience/large-and-bright.md), [Large & Dark](../presets/ambience/large-and-dark.md), [Large Ambience](../presets/ambience/large-ambience.md), [Long Ambience](../presets/ambience/long-ambience.md); **Chambers:** [Large & Bright](../presets/chambers/large-and-bright.md), [Large Chamber](../presets/chambers/large-chamber.md), [Snare Chamber](../presets/chambers/snare-chamber.md); **Halls:** [Dense Hall](../presets/halls/dense-hall.md), [Large & Near](../presets/halls/large-and-near.md), [Large Hall](../presets/halls/large-hall.md); **Plates:** [Silver Plate](../presets/plates/silver-plate.md); **Rooms:** [Marble Foyer](../presets/rooms/marble-foyer.md), [Small Q Room](../presets/rooms/small-q-room.md)
- **10:** **Ambience:** [Deep Ambience](../presets/ambience/deep-ambience.md); **Chambers:** [A&M Chamber](../presets/chambers/a-and-m-chamber.md), [CD Chamber](../presets/chambers/cd-chamber.md); **Halls:** [Brass Hall](../presets/halls/brass-hall.md), [Medium & Deep](../presets/halls/medium-and-deep.md), [Sandors Hall](../presets/halls/sandors-hall.md); **Plates:** [Snare Plate B](../presets/plates/snare-plate-b.md); **Rooms:** [Deep Stone](../presets/rooms/deep-stone.md); **Spaces:** [Tanglewood](../presets/spaces/tanglewood.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 104 | Offset 105 | `nibble_hilo` | Display lo 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 0 ms | `00` | `00` | 0 | `02` | `0C` `02` `0F` `05` | dump |
| 2 ms | `00` | `01` | 1 | `03` | `0A` `0E` `0A` `05` | dump |
| 4 ms | `00` | `02` | 2 | `04` | `0D` `0A` `0A` `04` | dump |
| 100 ms | `02` | `03` | 35 | `06` | `02` `0C` `06` `09` | dump |
| 204 ms | `03` | `00` | 48 | `06` | `07` `05` `0B` `00` | dump |
| 500 ms | `05` | `05` | 85 | `07` | `0C` `07` `03` `0A` | dump |

## Interpretation

- **Primary field:** offsets **104-105**, encoding `nibble_hilo` (table/index candidate (monotonic 100%)).
- **Confidence:** medium (0/6 dumps matched, 100%).
- **Catalog hint (Bricasti):** Pre Delay - printed 0 ... 500 ms [match] - hint only; dumps win.
- **Catalog notes:** Sparse capture series uses a non-linear table @ 104-105.
- **Range:** Range 0 ... 500 ms (capture extremes).
- **Sampling:** extremes, adjacents, 2 sample mid(s) (not every step).
- **Edge slopes:** Low and high extreme->adjacent slopes disagree - prefer a table/index interpretation over a partial closed-form scale.
- **How to set:**
  1. Use the per-dump mapping table in encoding_hypotheses until a closed-form scale is confirmed
  2. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 147 (display low nibble) (edit/UI state, not the parameter word).
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
- [HF RT Crossover](hf-rt-crossover.md)
- [HF RT Multiply](hf-rt-multiply.md)
- [LF RT Crossover](lf-rt-crossover.md)
- [LF RT Multiply](lf-rt-multiply.md)
- [Modulation](modulation.md)
- **Pre Delay** (this page)
- [Reverb Time](reverb-time.md)
- [Rolloff](rolloff.md)
- [Size](size.md)
- [VLF Cut](vlf-cut.md)
