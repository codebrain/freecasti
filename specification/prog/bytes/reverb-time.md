[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Reverb Time

_Generated 2026-07-19. Source folder: `sysex/prog/parameters/reverb time/`._

## SysEx summary

- **Offsets:** 100-101
- **Encoding:** `nibble_hilo`
- **Confidence:** medium
- **Range:** Range 0.2 ... 30 s (capture extremes)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Mid-frequency reverb time. Sets the reverb time of the mid frequencies when the signal stops.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| `nibble_hilo` | Offset 100 | Offset 101 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | 0.2 | dump, provided |
| 1 | `00` | `01` | 0.25 | dump, provided |
| 2 | `00` | `02` | 0.3 | dump, provided |
| 3 | `00` | `03` | 0.35 | provided |
| 4 | `00` | `04` | 0.4 | provided, [1](../presets/ambience/small-and-bright.md), [2](../presets/rooms/front-room.md) |
| 5 | `00` | `05` | 0.45 | provided, [1](../presets/rooms/studio-d.md), [2](../presets/spaces/cinema-room.md) |
| 6 | `00` | `06` | 0.5 | provided, [1](../presets/ambience/percussion-air.md), [2](../presets/ambience/small-and-dark.md), [3](../presets/rooms/center-room.md) |
| 7 | `00` | `07` | 0.55 | provided, [1](../presets/rooms/back-room.md), [2](../presets/rooms/studio-c.md) |
| 8 | `00` | `08` | 0.6 | provided, [1](../presets/rooms/heavy-room.md), [2](../presets/rooms/small-room.md), [3](../presets/rooms/small-wooden.md) |
| 9 | `00` | `09` | 0.65 | provided, [1](../presets/rooms/studio-b-far.md) |
| 10 | `00` | `0A` | 0.7 | provided, [1](../presets/ambience/clear-ambience.md), [2](../presets/chambers/kick-chamber.md), [3](../presets/rooms/small-tiled.md), [4](../presets/rooms/studio-a.md) |
| 11 | `00` | `0B` | 0.75 | provided |
| 12 | `00` | `0C` | 0.8 | dump, provided, [1](../presets/ambience/large-ambience.md), [2](../presets/rooms/djangos-room.md), [3](../presets/rooms/glass-room.md) |
| 13 | `00` | `0D` | 0.85 | provided |
| 14 | `00` | `0E` | 0.9 | provided, [1](../presets/ambience/medium-and-dark.md), [2](../presets/plates/small-plate.md) |
| 15 | `00` | `0F` | 0.95 | provided, [1](../presets/ambience/large-and-bright.md), [2](../presets/plates/fat-plate.md), [3](../presets/rooms/small-vox-room.md) |
| 16 | `01` | `00` | 1 | provided, [1](../presets/ambience/deep-ambience.md), [2](../presets/ambience/large-and-dark.md), [3](../presets/chambers/small-chamber.md), [4](../presets/plates/snare-plate-b.md), [5](../presets/rooms/music-room.md), +1 more |
| 17 | `01` | `01` | 1.05 | provided |
| 18 | `01` | `02` | 1.1 | provided, [1](../presets/plates/percussion.md), [2](../presets/rooms/large-room.md) |
| 19 | `01` | `03` | 1.15 | provided, [1](../presets/ambience/long-ambience.md) |
| 20 | `01` | `04` | 1.2 | provided, [1](../presets/chambers/snare-chamber.md), [2](../presets/plates/snare-plate-a.md), [3](../presets/rooms/deep-stone.md), [4](../presets/rooms/drum-and-chamber.md), [5](../presets/rooms/large-tiled.md), +2 more |
| 21 | `01` | `05` | 1.25 | provided, [1](../presets/ambience/bass-xxl.md), [2](../presets/chambers/medium-chamber.md), [3](../presets/rooms/marble-foyer.md) |
| 22 | `01` | `06` | 1.3 | dump, provided |
| 23 | `01` | `07` | 1.35 | provided, [1](../presets/plates/crystal-plate.md) |
| 24 | `01` | `08` | 1.4 | provided, [1](../presets/chambers/large-chamber.md), [2](../presets/halls/small-and-near.md), [3](../presets/halls/small-hall.md) |
| 25 | `01` | `09` | 1.45 | provided |
| 26 | `01` | `0A` | 1.5 | provided, [1](../presets/chambers/amb-chamber-b.md), [2](../presets/plates/dark-plate.md) |
| 27 | `01` | `0B` | 1.55 | provided |
| 28 | `01` | `0C` | 1.6 | provided, [1](../presets/chambers/large-and-bright.md), [2](../presets/plates/cd-plate-b.md) |
| 29 | `01` | `0D` | 1.65 | provided, [1](../presets/chambers/amb-chamber-a.md) |
| 30 | `01` | `0E` | 1.7 | provided, [1](../presets/plates/cd-plate-a.md), [2](../presets/plates/dense-plate.md), [3](../presets/plates/echo-plate.md) |
| 31 | `01` | `0F` | 1.75 | provided |
| 32 | `02` | `00` | 1.8 | provided, [1](../presets/halls/boston-hall-b.md), [2](../presets/halls/gold-hall.md), [3](../presets/halls/medium-and-deep.md), [4](../presets/halls/medium-and-near.md), [5](../presets/halls/medium-hall.md), +3 more |
| 33 | `02` | `01` | 1.85 | provided |
| 34 | `02` | `02` | 1.9 | provided, [1](../presets/chambers/cd-chamber.md), [2](../presets/chambers/deep-chamber.md), [3](../presets/spaces/redwood-valley.md) |
| 35 | `02` | `03` | 1.95 | provided |
| 36 | `02` | `04` | 2 | provided, [1](../presets/halls/brass-hall.md), [2](../presets/halls/dense-hall.md), [3](../presets/plates/bright-plate.md), [4](../presets/plates/silver-plate.md) |
| 37 | `02` | `05` | 2.05 | provided |
| 38 | `02` | `06` | 2.1 | provided, [1](../presets/halls/boston-hall-a.md) |
| 39 | `02` | `07` | 2.15 | provided, [1](../presets/halls/large-and-dark.md), [2](../presets/halls/large-and-deep.md) |
| 40 | `02` | `08` | 2.2 | dump, provided, [1](../presets/chambers/a-and-m-chamber.md), [2](../presets/halls/clear-hall.md), [3](../presets/halls/concert-hall.md), [4](../presets/halls/large-and-near.md), [5](../presets/halls/large-hall.md), +2 more |
| 41 | `02` | `09` | 2.25 | provided, [1](../presets/halls/worcester-hall.md) |
| 42 | `02` | `0A` | 2.3 | provided, [1](../presets/halls/amsterdam-hall.md), [2](../presets/halls/vienna-hall.md), [3](../presets/spaces/arena.md) |
| 43 | `02` | `0B` | 2.35 | provided |
| 44 | `02` | `0C` | 2.4 | provided, [1](../presets/chambers/old-chamber.md) |
| 45 | `02` | `0D` | 2.45 | provided |
| 46 | `02` | `0E` | 2.5 | provided, [1](../presets/halls/berliner-hall.md) |
| 47 | `02` | `0F` | 2.55 | provided |
| 48 | `03` | `00` | 2.6 | provided, [1](../presets/halls/sandors-hall.md), [2](../presets/rooms/large-q-room.md) |
| 49 | `03` | `01` | 2.65 | provided |
| 50 | `03` | `02` | 2.7 | provided |
| 51 | `03` | `03` | 2.75 | provided |
| 52 | `03` | `04` | 2.8 | provided |
| 53 | `03` | `05` | 2.85 | provided |
| 54 | `03` | `06` | 2.9 | provided |
| 55 | `03` | `07` | 2.95 | provided |
| 56 | `03` | `08` | 3 | provided, [1](../presets/spaces/tanglewood.md) |
| 57 | `03` | `09` | 3.1 | provided |
| 58 | `03` | `0A` | 3.2 | provided, [1](../presets/spaces/north-church.md) |
| 59 | `03` | `0B` | 3.3 | provided, [1](../presets/spaces/east-church.md) |
| 60 | `03` | `0C` | 3.4 | provided |
| 61 | `03` | `0D` | 3.5 | dump, provided, [1](../presets/spaces/car-park.md) |
| 62 | `03` | `0E` | 3.6 | provided |
| 63 | `03` | `0F` | 3.7 | provided |
| 64 | `04` | `00` | 3.8 | provided |
| 65 | `04` | `01` | 3.9 | provided, [1](../presets/spaces/bath-house.md), [2](../presets/spaces/south-church.md) |
| 66 | `04` | `02` | 4.0 | provided |
| 67 | `04` | `03` | 4.1 | provided |
| 68 | `04` | `04` | 4.2 | provided |
| 69 | `04` | `05` | 4.3 | provided |
| 70 | `04` | `06` | 4.4 | provided |
| 71 | `04` | `07` | 4.5 | provided |
| 72 | `04` | `08` | 4.6 | provided |
| 73 | `04` | `09` | 4.7 | provided |
| 74 | `04` | `0A` | 4.8 | provided |
| 75 | `04` | `0B` | 4.9 | provided |
| 76 | `04` | `0C` | 5 | provided |
| 77 | `04` | `0D` | 5.1 | provided, [1](../presets/spaces/stone-quarry.md) |
| 78 | `04` | `0E` | 5.2 | provided |
| 79 | `04` | `0F` | 5.3 | provided |
| 80 | `05` | `00` | 5.4 | provided, [1](../presets/spaces/west-church.md) |
| 81 | `05` | `01` | 5.5 | provided |
| 82 | `05` | `02` | 5.6 | provided |
| 83 | `05` | `03` | 5.7 | provided |
| 84 | `05` | `04` | 5.8 | provided |
| 85 | `05` | `05` | 5.9 | provided |
| 86 | `05` | `06` | 6 | provided |
| 87 | `05` | `07` | 6.2 | provided |
| 88 | `05` | `08` | 6.4 | provided |
| 89 | `05` | `09` | 6.6 | provided |
| 90 | `05` | `0A` | 6.8 | dump, provided |
| 91 | `05` | `0B` | 7 | provided |
| 92 | `05` | `0C` | 7.2 | provided |
| 93 | `05` | `0D` | 7.4 | provided |
| 94 | `05` | `0E` | 7.6 | provided |
| 95 | `05` | `0F` | 7.8 | provided |
| 96 | `06` | `00` | 8 | provided |
| 97 | `06` | `01` | 8.2 | provided |
| 98 | `06` | `02` | 8.4 | provided |
| 99 | `06` | `03` | 8.6 | provided |
| 100 | `06` | `04` | 8.8 | provided |
| 101 | `06` | `05` | 9 | provided |
| 102 | `06` | `06` | 9.2 | provided |
| 103 | `06` | `07` | 9.4 | provided |
| 104 | `06` | `08` | 9.6 | provided |
| 105 | `06` | `09` | 9.8 | provided |
| 106 | `06` | `0A` | 10 | dump, provided |
| 107 | `06` | `0B` | 10.5 | provided |
| 108 | `06` | `0C` | 11 | provided |
| 109 | `06` | `0D` | 11.5 | provided |
| 110 | `06` | `0E` | 12 | provided |
| 111 | `06` | `0F` | 12.5 | provided |
| 112 | `07` | `00` | 13 | provided |
| 113 | `07` | `01` | 13.5 | provided |
| 114 | `07` | `02` | 14 | provided |
| 115 | `07` | `03` | 14.5 | provided |
| 116 | `07` | `04` | 15 | provided |
| 117 | `07` | `05` | 15.5 | provided |
| 118 | `07` | `06` | 16 | provided |
| 119 | `07` | `07` | 16.5 | dump, provided |
| 120 | `07` | `08` | 17 | provided |
| 121 | `07` | `09` | 17.5 | provided |
| 122 | `07` | `0A` | 18 | provided |
| 123 | `07` | `0B` | 18.5 | provided |
| 124 | `07` | `0C` | 19 | provided |
| 125 | `07` | `0D` | 19.5 | provided |
| 126 | `07` | `0E` | 20 | provided |
| 127 | `07` | `0F` | 21 | provided |
| 128 | `08` | `00` | 22 | provided |
| 129 | `08` | `01` | 23 | dump, provided |
| 130 | `08` | `02` | 24 | provided |
| 131 | `08` | `03` | 25 | provided |
| 132 | `08` | `04` | 26 | provided |
| 133 | `08` | `05` | 27 | provided |
| 134 | `08` | `06` | 28 | provided |
| 135 | `08` | `07` | 29 | dump, provided |
| 136 | `08` | `08` | 30 | dump, provided |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **16:** **Ambience:** [Deep Ambience](../presets/ambience/deep-ambience.md), [Large & Dark](../presets/ambience/large-and-dark.md); **Chambers:** [Small Chamber](../presets/chambers/small-chamber.md); **Plates:** [Snare Plate B](../presets/plates/snare-plate-b.md); **Rooms:** [Music Room](../presets/rooms/music-room.md), [Studio E](../presets/rooms/studio-e.md)
- **20:** **Chambers:** [Snare Chamber](../presets/chambers/snare-chamber.md); **Plates:** [Snare Plate A](../presets/plates/snare-plate-a.md); **Rooms:** [Deep Stone](../presets/rooms/deep-stone.md), [Drum & Chamber](../presets/rooms/drum-and-chamber.md), [Large Tiled](../presets/rooms/large-tiled.md), [Large Wooden](../presets/rooms/large-wooden.md), [Small Q Room](../presets/rooms/small-q-room.md)
- **32:** **Halls:** [Boston Hall B](../presets/halls/boston-hall-b.md), [Gold Hall](../presets/halls/gold-hall.md), [Medium & Deep](../presets/halls/medium-and-deep.md), [Medium & Near](../presets/halls/medium-and-near.md), [Medium Hall](../presets/halls/medium-hall.md), [The ArchDuke](../presets/halls/the-archduke.md); **Plates:** [Gold Plate](../presets/plates/gold-plate.md), [London Plate](../presets/plates/london-plate.md)
- **40:** **Chambers:** [A&M Chamber](../presets/chambers/a-and-m-chamber.md); **Halls:** [Clear Hall](../presets/halls/clear-hall.md), [Concert Hall](../presets/halls/concert-hall.md), [Large & Near](../presets/halls/large-and-near.md), [Large Hall](../presets/halls/large-hall.md); **Plates:** [Large Plate](../presets/plates/large-plate.md); **Spaces:** [Scoring Stage](../presets/spaces/scoring-stage.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 100 | Offset 101 | `nibble_hilo` | Display lo 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 0.2 s | `00` | `00` | 0 | `02` | `0A` `02` `07` `02` | dump |
| 0.25 s | `00` | `01` | 1 | `04` | `02` `0F` `02` `06` | dump |
| 0.3 s | `00` | `02` | 2 | `05` | `03` `09` `07` `0C` | dump |
| 0.8 s | `00` | `0C` | 12 | `06` | `0F` `0B` `01` `0A` | dump |
| 1.3 s | `01` | `06` | 22 | `07` | `0D` `07` `0F` `0F` | dump |
| 2.2 s | `02` | `08` | 40 | `08` | `0F` `0E` `01` `0E` | dump |
| 3.5 s | `03` | `0D` | 61 | `0A` | `09` `0D` `04` `01` | dump |
| 6.8 s | `05` | `0A` | 90 | `0A` | `06` `09` `07` `0D` | dump |
| 10 s | `06` | `0A` | 106 | `0B` | `04` `03` `0D` `07` | dump |
| 16.5 s | `07` | `07` | 119 | `0D` | `0C` `0E` `09` `06` | dump |
| 23 s | `08` | `01` | 129 | `0D` | `0A` `02` `09` `05` | dump |
| 29 s | `08` | `07` | 135 | `0E` | `04` `0E` `01` `0C` | dump |
| 30 s | `08` | `08` | 136 | `0F` | `0C` `01` `0D` `0F` | dump |

## Interpretation

- **Primary field:** offsets **100-101**, encoding `nibble_hilo` (table/index candidate (monotonic 100%)).
- **Confidence:** medium (0/13 dumps matched, 100%).
- **Catalog hint (Bricasti):** Reverb Time - printed 0.1 ... 30.0 s [match] - hint only; dumps win.
- **Catalog notes:** This unit: non-linear table @ 100-101; captured 0.2...30 s (printed floor 0.1 s not yet dumped).
- **Range:** Range 0.2 ... 30 s (capture extremes).
- **Sampling:** extremes, adjacents, 9 sample mid(s) (not every step).
- **Edge slopes:** Low and high extreme->adjacent slopes disagree - prefer a table/index interpretation over a partial closed-form scale.
- **How to set:**
  1. Use the per-dump mapping table in encoding_hypotheses until a closed-form scale is confirmed
  2. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 147 (display low nibble) (edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Unseen values

Documented in the spec (encoding map / manual) but not yet witnessed in a committed dump. "Possible" spans every encoded step in this field's range; missing steps are listed as ranges when there are many.

- **Encoding range:** encoded 0–136 (137 steps documented).
- **Manual range not fully captured:** manual floor 0.1 below captured min 0.2.
- **Never captured on the wire (124):** encoded 3–11, 13–21, 23–39, 41–60, 62–89, 91–105, 107–118, 120–128, 130–134 — see the [encoding map](#encoding-map) above for each label.
- **Documented gaps (no row at all):** none between documented min/max.
- **Wire nibbles never observed (`0`–`F`):** offset 100 (high): `9` `A` `B` `C` `D` `E` `F`; offset 101 (low): none

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
- **Reverb Time** (this page)
- [Rolloff](rolloff.md)
- [Size](size.md)
- [VLF Cut](vlf-cut.md)
