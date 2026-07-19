[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# LF RT Multiply

_Generated 2026-07-19. Source folder: `sysex/prog/parameters/lf rt multiply/`._

## SysEx summary

- **Offsets:** 118-119
- **Encoding:** `nibble_hilo`
- **Confidence:** medium
- **Range:** Range 0.2 ... 4 (capture extremes)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Sets the low-frequency reverb time below the crossover frequency set by LF RT Crossover. Displayed and controlled as a scaling of Reverb Time.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| `nibble_hilo` | Offset 118 | Offset 119 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | 0.2 | dump, provided |
| 1 | `00` | `01` | 0.25 | dump, provided |
| 2 | `00` | `02` | 0.3 | dump, provided |
| 3 | `00` | `03` | 0.35 | provided, [1](../presets/spaces/bath-house.md) |
| 4 | `00` | `04` | 0.4 | provided |
| 5 | `00` | `05` | 0.45 | provided, [1](../presets/rooms/small-tiled.md) |
| 6 | `00` | `06` | 0.5 | provided, [1](../presets/spaces/east-church.md) |
| 7 | `00` | `07` | 0.55 | provided |
| 8 | `00` | `08` | 0.6 | provided, [1](../presets/rooms/glass-room.md) |
| 9 | `00` | `09` | 0.65 | provided, [1](../presets/rooms/marble-foyer.md) |
| 10 | `00` | `0A` | 0.7 | provided, [1](../presets/plates/bright-plate.md), [2](../presets/rooms/large-tiled.md), [3](../presets/rooms/studio-a.md) |
| 11 | `00` | `0B` | 0.75 | dump, provided, [1](../presets/plates/crystal-plate.md) |
| 12 | `00` | `0C` | 0.8 | provided, [1](../presets/plates/cd-plate-a.md), [2](../presets/plates/percussion.md), [3](../presets/rooms/deep-stone.md), [4](../presets/spaces/cinema-room.md) |
| 13 | `00` | `0D` | 0.85 | provided, [1](../presets/ambience/large-and-bright.md), [2](../presets/ambience/small-and-bright.md), [3](../presets/rooms/large-wooden.md) |
| 14 | `00` | `0E` | 0.9 | provided, [1](../presets/ambience/clear-ambience.md), [2](../presets/ambience/large-ambience.md), [3](../presets/chambers/amb-chamber-a.md), [4](../presets/chambers/amb-chamber-b.md), [5](../presets/chambers/large-and-bright.md), +8 more |
| 15 | `00` | `0F` | 0.95 | provided, [1](../presets/ambience/deep-ambience.md), [2](../presets/ambience/percussion-air.md), [3](../presets/chambers/large-chamber.md), [4](../presets/chambers/small-chamber.md), [5](../presets/plates/silver-plate.md), +4 more |
| 16 | `01` | `00` | 1 | provided, [1](../presets/ambience/bass-xxl.md), [2](../presets/chambers/cd-chamber.md), [3](../presets/chambers/deep-chamber.md), [4](../presets/chambers/kick-chamber.md), [5](../presets/halls/brass-hall.md), +10 more |
| 17 | `01` | `01` | 1.05 | provided, [1](../presets/ambience/large-and-dark.md), [2](../presets/ambience/long-ambience.md), [3](../presets/ambience/medium-and-dark.md), [4](../presets/ambience/small-and-dark.md), [5](../presets/chambers/a-and-m-chamber.md), +9 more |
| 18 | `01` | `02` | 1.1 | provided, [1](../presets/halls/amsterdam-hall.md), [2](../presets/halls/large-and-near.md), [3](../presets/halls/medium-and-near.md), [4](../presets/plates/large-plate.md), [5](../presets/rooms/small-q-room.md), +1 more |
| 19 | `01` | `03` | 1.15 | provided, [1](../presets/halls/large-and-dark.md), [2](../presets/rooms/studio-b-far.md), [3](../presets/rooms/studio-c.md) |
| 20 | `01` | `04` | 1.2 | provided, [1](../presets/halls/berliner-hall.md), [2](../presets/halls/concert-hall.md), [3](../presets/halls/large-hall.md), [4](../presets/halls/medium-hall.md), [5](../presets/halls/sandors-hall.md), +2 more |
| 21 | `01` | `05` | 1.25 | provided, [1](../presets/chambers/old-chamber.md), [2](../presets/halls/gold-hall.md), [3](../presets/spaces/redwood-valley.md) |
| 22 | `01` | `06` | 1.3 | provided, [1](../presets/halls/dense-hall.md), [2](../presets/plates/cd-plate-b.md), [3](../presets/spaces/north-church.md) |
| 23 | `01` | `07` | 1.35 | provided, [1](../presets/rooms/heavy-room.md), [2](../presets/spaces/arena.md) |
| 24 | `01` | `08` | 1.4 | provided, [1](../presets/halls/worcester-hall.md), [2](../presets/rooms/large-q-room.md), [3](../presets/spaces/tanglewood.md) |
| 25 | `01` | `09` | 1.45 | provided |
| 26 | `01` | `0A` | 1.5 | provided, [1](../presets/rooms/studio-d.md), [2](../presets/spaces/car-park.md) |
| 27 | `01` | `0B` | 1.55 | provided |
| 28 | `01` | `0C` | 1.6 | provided |
| 29 | `01` | `0D` | 1.65 | provided |
| 30 | `01` | `0E` | 1.7 | provided |
| 31 | `01` | `0F` | 1.75 | provided, [1](../presets/rooms/small-vox-room.md) |
| 32 | `02` | `00` | 1.8 | provided |
| 33 | `02` | `01` | 1.85 | provided |
| 34 | `02` | `02` | 1.9 | provided |
| 35 | `02` | `03` | 1.95 | provided |
| 36 | `02` | `04` | 2 | provided |
| 37 | `02` | `05` | 2.1 | provided |
| 38 | `02` | `06` | 2.2 | provided |
| 39 | `02` | `07` | 2.3 | provided |
| 40 | `02` | `08` | 2.4 | provided |
| 41 | `02` | `09` | 2.5 | provided |
| 42 | `02` | `0A` | 2.6 | dump, provided |
| 43 | `02` | `0B` | 2.7 | provided |
| 44 | `02` | `0C` | 2.8 | provided |
| 45 | `02` | `0D` | 2.9 | provided |
| 46 | `02` | `0E` | 3.0 | provided |
| 47 | `02` | `0F` | 3.1 | provided |
| 48 | `03` | `00` | 3.2 | dump, provided |
| 49 | `03` | `01` | 3.3 | provided |
| 50 | `03` | `02` | 3.4 | provided |
| 51 | `03` | `03` | 3.5 | provided |
| 52 | `03` | `04` | 3.6 | provided |
| 53 | `03` | `05` | 3.7 | provided |
| 54 | `03` | `06` | 3.8 | provided |
| 55 | `03` | `07` | 3.9 | dump, provided |
| 56 | `03` | `08` | 4 | dump, provided, [1](../presets/spaces/stone-quarry.md) |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **14:** **Ambience:** [Clear Ambience](../presets/ambience/clear-ambience.md), [Large Ambience](../presets/ambience/large-ambience.md); **Chambers:** [Amb Chamber A](../presets/chambers/amb-chamber-a.md), [Amb Chamber B](../presets/chambers/amb-chamber-b.md), [Large & Bright](../presets/chambers/large-and-bright.md), [Medium Chamber](../presets/chambers/medium-chamber.md), [Snare Chamber](../presets/chambers/snare-chamber.md); **Plates:** [Dark Plate](../presets/plates/dark-plate.md), [Dense Plate](../presets/plates/dense-plate.md), [Echo Plate](../presets/plates/echo-plate.md); **Rooms:** [Drum & Chamber](../presets/rooms/drum-and-chamber.md), [Small Wooden](../presets/rooms/small-wooden.md); **Spaces:** [Scoring Stage](../presets/spaces/scoring-stage.md)
- **15:** **Ambience:** [Deep Ambience](../presets/ambience/deep-ambience.md), [Percussion Air](../presets/ambience/percussion-air.md); **Chambers:** [Large Chamber](../presets/chambers/large-chamber.md), [Small Chamber](../presets/chambers/small-chamber.md); **Plates:** [Silver Plate](../presets/plates/silver-plate.md), [Small Plate](../presets/plates/small-plate.md), [Snare Plate B](../presets/plates/snare-plate-b.md); **Rooms:** [Front Room](../presets/rooms/front-room.md), [Large Room](../presets/rooms/large-room.md)
- **16:** **Ambience:** [Bass  XXL](../presets/ambience/bass-xxl.md); **Chambers:** [CD Chamber](../presets/chambers/cd-chamber.md), [Deep Chamber](../presets/chambers/deep-chamber.md), [Kick Chamber](../presets/chambers/kick-chamber.md); **Halls:** [Brass Hall](../presets/halls/brass-hall.md), [Clear Hall](../presets/halls/clear-hall.md), [The ArchDuke](../presets/halls/the-archduke.md), [Vienna Hall](../presets/halls/vienna-hall.md); **Plates:** [London Plate](../presets/plates/london-plate.md), [Snare Plate A](../presets/plates/snare-plate-a.md); **Rooms:** [Center Room](../presets/rooms/center-room.md), [Djangos Room](../presets/rooms/djangos-room.md), [Music Room](../presets/rooms/music-room.md), [Studio E](../presets/rooms/studio-e.md); **Spaces:** [West Church](../presets/spaces/west-church.md)
- **17:** **Ambience:** [Large & Dark](../presets/ambience/large-and-dark.md), [Long Ambience](../presets/ambience/long-ambience.md), [Medium & Dark](../presets/ambience/medium-and-dark.md), [Small & Dark](../presets/ambience/small-and-dark.md); **Chambers:** [A&M Chamber](../presets/chambers/a-and-m-chamber.md); **Halls:** [Boston Hall A](../presets/halls/boston-hall-a.md), [Boston Hall B](../presets/halls/boston-hall-b.md), [Chicago Hall](../presets/halls/chicago-hall.md), [Large & Deep](../presets/halls/large-and-deep.md), [Medium & Deep](../presets/halls/medium-and-deep.md), [Small & Near](../presets/halls/small-and-near.md), [Small Hall](../presets/halls/small-hall.md); **Rooms:** [Back Room](../presets/rooms/back-room.md), [Small Room](../presets/rooms/small-room.md)
- **18:** **Halls:** [Amsterdam Hall](../presets/halls/amsterdam-hall.md), [Large & Near](../presets/halls/large-and-near.md), [Medium & Near](../presets/halls/medium-and-near.md); **Plates:** [Large Plate](../presets/plates/large-plate.md); **Rooms:** [Small Q Room](../presets/rooms/small-q-room.md); **Spaces:** [South Church](../presets/spaces/south-church.md)
- **20:** **Halls:** [Berliner Hall](../presets/halls/berliner-hall.md), [Concert Hall](../presets/halls/concert-hall.md), [Large Hall](../presets/halls/large-hall.md), [Medium Hall](../presets/halls/medium-hall.md), [Sandors Hall](../presets/halls/sandors-hall.md); **Plates:** [Fat Plate](../presets/plates/fat-plate.md), [Gold Plate](../presets/plates/gold-plate.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 118 | Offset 119 | `nibble_hilo` | Display 146–147 | display `nibble_hilo` | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.2 | `00` | `00` | 0 | `0B 0F` | 191 | `00` `05` `0E` `02` | dump |
| 0.25 | `00` | `01` | 1 | `0C 00` | 192 | `07` `03` `0D` `0A` | dump |
| 0.3 | `00` | `02` | 2 | `0C 01` | 193 | `0B` `03` `05` `03` | dump |
| 0.75 | `00` | `0B` | 11 | `0C 02` | 194 | `0B` `00` `01` `0B` | dump |
| 2.6 | `02` | `0A` | 42 | `0C 02` | 194 | `0E` `0A` `07` `07` | dump |
| 3.2 | `03` | `00` | 48 | `0C 03` | 195 | `0C` `04` `0F` `03` | dump |
| 3.9 | `03` | `07` | 55 | `0C 04` | 196 | `0C` `05` `04` `03` | dump |
| 4 | `03` | `08` | 56 | `0C 05` | 197 | `00` `07` `01` `0A` | dump |

## Interpretation

- **Primary field:** offsets **118-119**, encoding `nibble_hilo` (table/index candidate (monotonic 100%)).
- **Confidence:** medium (0/8 dumps matched, 100%).
- **Catalog hint (Bricasti):** LF RT Multiply - printed 0.2 ... 4.0 [match] - hint only; dumps win.
- **Catalog notes:** Captured @ 118-119: 0.05 steps up to 2.0×, then 0.1 steps to 4.0× (non-uniform table, unlike HF).
- **Range:** Range 0.2 ... 4 (capture extremes).
- **Sampling:** extremes, adjacents, 4 sample mid(s) (not every step).
- **Edge slopes:** Low and high extreme->adjacent slopes disagree - prefer a table/index interpretation over a partial closed-form scale.
- **How to set:**
  1. Use the per-dump mapping table in encoding_hypotheses until a closed-form scale is confirmed
  2. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 146–147 (`nibble_hilo` display) (edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Unseen values

Documented in the spec (encoding map / manual) but not yet witnessed in a committed dump. "Possible" spans every encoded step in this field's range; missing steps are listed as ranges when there are many.

- **Encoding range:** encoded 0–56 (57 steps documented).
- **Never captured on the wire (49):** encoded 3–10, 12–41, 43–47, 49–54 — see the [encoding map](#encoding-map) above for each label.
- **Documented gaps (no row at all):** none between documented min/max.
- **Wire nibbles never observed (`0`–`F`):** offset 118 (high): `4` `5` `6` `7` `8` `9` `A` `B` `C` `D` `E` `F`; offset 119 (low): none

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
- **LF RT Multiply** (this page)
- [Modulation](modulation.md)
- [Pre Delay](predelay.md)
- [Reverb Time](reverb-time.md)
- [Rolloff](rolloff.md)
- [Size](size.md)
- [VLF Cut](vlf-cut.md)
