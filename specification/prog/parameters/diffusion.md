[Overview](../README.md) | [Parameters](../parameters/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Diffusion

_Generated 2026-07-18. Source folder: `sysex/prog/parameters/diffusion/`._

## SysEx summary

- **Offsets:** 107
- **Encoding:** `raw_u8`
- **Confidence:** high
- **Range:** Observed range 0 ... 10
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Sets initial diffusion of the reverb. Displayed and controlled as a percentage change from the initial value defined by the preset.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| Encoded | Offset 107 | Label | Source |
| --- | --- | --- | --- |
| 0 | `00` | Low | dump, provided, [1](../presets/ambience/heavy-ambience.md), [2](../presets/nonlin/nonlin-a.md), [3](../presets/nonlin/nonlin-b.md), [4](../presets/nonlin/nonlin-c.md), [5](../presets/nonlin/nonlin-d.md), +4 more |
| 1 | `01` | 1 | dump, provided, [1](../presets/plates/large-plate.md), [2](../presets/plates/london-plate.md) |
| 2 | `02` | 2 | dump, provided, [1](../presets/ambience/clear-ambience.md), [2](../presets/ambience/large-and-dark.md), [3](../presets/ambience/long-ambience.md), [4](../presets/ambience/medium-and-dark.md), [5](../presets/ambience/small-and-dark.md), +6 more |
| 3 | `03` | 3 | dump, provided, [1](../presets/ambience/bass-xxl.md), [2](../presets/ambience/deep-ambience.md), [3](../presets/ambience/large-and-bright.md), [4](../presets/ambience/large-ambience.md), [5](../presets/ambience/small-and-bright.md), +23 more |
| 4 | `04` | 4 | dump, provided, [1](../presets/chambers/snare-chamber.md), [2](../presets/plates/echo-plate.md), [3](../presets/rooms/center-room.md), [4](../presets/rooms/deep-stone.md), [5](../presets/rooms/glass-room.md), +5 more |
| 5 | `05` | 5 | dump, provided, [1](../presets/chambers/a-and-m-chamber.md), [2](../presets/chambers/cd-chamber.md), [3](../presets/chambers/kick-chamber.md), [4](../presets/chambers/large-chamber.md), [5](../presets/chambers/medium-chamber.md), +17 more |
| 6 | `06` | 6 | dump, provided, [1](../presets/chambers/large-and-bright.md), [2](../presets/halls/berliner-hall.md), [3](../presets/halls/boston-hall-a.md), [4](../presets/halls/large-and-dark.md), [5](../presets/halls/medium-and-near.md), +5 more |
| 7 | `07` | 7 | provided, [1](../presets/chambers/amb-chamber-a.md), [2](../presets/chambers/amb-chamber-b.md), [3](../presets/chambers/deep-chamber.md), [4](../presets/halls/amsterdam-hall.md), [5](../presets/halls/chicago-hall.md), +5 more |
| 8 | `08` | 8 | provided, [1](../presets/halls/vienna-hall.md), [2](../presets/spaces/cinema-room.md) |
| 9 | `09` | 9 | dump, provided, [1](../presets/spaces/bath-house.md) |
| 10 | `0A` | High | dump, provided, [1](../presets/ambience/percussion-air.md) |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **0:** **Ambience:** [Heavy Ambience](../presets/ambience/heavy-ambience.md); **NonLin:** [NonLin A](../presets/nonlin/nonlin-a.md), [NonLin B](../presets/nonlin/nonlin-b.md), [NonLin C](../presets/nonlin/nonlin-c.md), [NonLin D](../presets/nonlin/nonlin-d.md); **Spaces 2:** [Med Space](../presets/spaces-2/med-space.md), [Music Forest](../presets/spaces-2/music-forest.md), [Small Space](../presets/spaces-2/small-space.md), [Waving Bloom](../presets/spaces-2/waving-bloom.md)
- **2:** **Ambience:** [Clear Ambience](../presets/ambience/clear-ambience.md), [Large & Dark](../presets/ambience/large-and-dark.md), [Long Ambience](../presets/ambience/long-ambience.md), [Medium & Dark](../presets/ambience/medium-and-dark.md), [Small & Dark](../presets/ambience/small-and-dark.md); **Plates:** [CD Plate B](../presets/plates/cd-plate-b.md), [Gold Plate](../presets/plates/gold-plate.md), [Snare Plate A](../presets/plates/snare-plate-a.md); **Rooms:** [Studio A](../presets/rooms/studio-a.md); **Spaces:** [Arena](../presets/spaces/arena.md), [East Church](../presets/spaces/east-church.md)
- **3:** **Ambience:** [Bass  XXL](../presets/ambience/bass-xxl.md), [Deep Ambience](../presets/ambience/deep-ambience.md), [Large & Bright](../presets/ambience/large-and-bright.md), [Large Ambience](../presets/ambience/large-ambience.md), [Small & Bright](../presets/ambience/small-and-bright.md); **Halls:** [Boston Hall B](../presets/halls/boston-hall-b.md), [Gold Hall](../presets/halls/gold-hall.md), [Sandors Hall](../presets/halls/sandors-hall.md); **Plates:** [Bright Plate](../presets/plates/bright-plate.md), [CD Plate A](../presets/plates/cd-plate-a.md), [Crystal Plate](../presets/plates/crystal-plate.md), [Dark Plate](../presets/plates/dark-plate.md), [Dense Plate](../presets/plates/dense-plate.md), [Fat Plate](../presets/plates/fat-plate.md), [Percussion](../presets/plates/percussion.md), [Silver Plate](../presets/plates/silver-plate.md), [Small Plate](../presets/plates/small-plate.md), [Snare Plate B](../presets/plates/snare-plate-b.md); **Rooms:** [Back Room](../presets/rooms/back-room.md), [Front Room](../presets/rooms/front-room.md), [Large Tiled](../presets/rooms/large-tiled.md), [Large Wooden](../presets/rooms/large-wooden.md), [Marble Foyer](../presets/rooms/marble-foyer.md), [Studio B Far](../presets/rooms/studio-b-far.md), [Studio C](../presets/rooms/studio-c.md), [Studio E](../presets/rooms/studio-e.md); **Spaces:** [Car Park](../presets/spaces/car-park.md), [Tanglewood](../presets/spaces/tanglewood.md)
- **4:** **Chambers:** [Snare Chamber](../presets/chambers/snare-chamber.md); **Plates:** [Echo Plate](../presets/plates/echo-plate.md); **Rooms:** [Center Room](../presets/rooms/center-room.md), [Deep Stone](../presets/rooms/deep-stone.md), [Glass Room](../presets/rooms/glass-room.md), [Large Room](../presets/rooms/large-room.md), [Small Room](../presets/rooms/small-room.md), [Small Tiled](../presets/rooms/small-tiled.md), [Small Vox Room](../presets/rooms/small-vox-room.md); **Spaces:** [Redwood Valley](../presets/spaces/redwood-valley.md)
- **5:** **Chambers:** [A&M Chamber](../presets/chambers/a-and-m-chamber.md), [CD Chamber](../presets/chambers/cd-chamber.md), [Kick Chamber](../presets/chambers/kick-chamber.md), [Large Chamber](../presets/chambers/large-chamber.md), [Medium Chamber](../presets/chambers/medium-chamber.md), [Old Chamber](../presets/chambers/old-chamber.md), [Small Chamber](../presets/chambers/small-chamber.md); **Halls:** [Brass Hall](../presets/halls/brass-hall.md), [Clear Hall](../presets/halls/clear-hall.md), [Concert Hall](../presets/halls/concert-hall.md), [Dense Hall](../presets/halls/dense-hall.md), [Small & Near](../presets/halls/small-and-near.md), [Small Hall](../presets/halls/small-hall.md), [The ArchDuke](../presets/halls/the-archduke.md); **Rooms:** [Djangos Room](../presets/rooms/djangos-room.md), [Drum & Chamber](../presets/rooms/drum-and-chamber.md), [Heavy Room](../presets/rooms/heavy-room.md), [Music Room](../presets/rooms/music-room.md), [Small Wooden](../presets/rooms/small-wooden.md), [Studio D](../presets/rooms/studio-d.md); **Spaces:** [North Church](../presets/spaces/north-church.md), [South Church](../presets/spaces/south-church.md)
- **6:** **Chambers:** [Large & Bright](../presets/chambers/large-and-bright.md); **Halls:** [Berliner Hall](../presets/halls/berliner-hall.md), [Boston Hall A](../presets/halls/boston-hall-a.md), [Large & Dark](../presets/halls/large-and-dark.md), [Medium & Near](../presets/halls/medium-and-near.md), [Medium Hall](../presets/halls/medium-hall.md), [Worcester Hall](../presets/halls/worcester-hall.md); **Rooms:** [Large Q Room](../presets/rooms/large-q-room.md), [Small Q Room](../presets/rooms/small-q-room.md); **Spaces:** [West Church](../presets/spaces/west-church.md)
- **7:** **Chambers:** [Amb Chamber A](../presets/chambers/amb-chamber-a.md), [Amb Chamber B](../presets/chambers/amb-chamber-b.md), [Deep Chamber](../presets/chambers/deep-chamber.md); **Halls:** [Amsterdam Hall](../presets/halls/amsterdam-hall.md), [Chicago Hall](../presets/halls/chicago-hall.md), [Large & Deep](../presets/halls/large-and-deep.md), [Large & Near](../presets/halls/large-and-near.md), [Large Hall](../presets/halls/large-hall.md), [Medium & Deep](../presets/halls/medium-and-deep.md); **Spaces:** [Scoring Stage](../presets/spaces/scoring-stage.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 107 | Encoded | Offset 146 | Offset 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| low (0) | `00` | 0 | `02` | `09` | `0F` `06` `05` `09` | dump |
| 1 | `01` | 1 | `02` | `0A` | `0A` `06` `08` `0C` | dump |
| 2 | `02` | 2 | `02` | `0B` | `09` `07` `00` `02` | dump |
| 3 | `03` | 3 | `02` | `0C` | `00` `07` `02` `06` | dump |
| 4 | `04` | 4 | `02` | `0D` | `03` `04` `0E` `0F` | dump |
| 5 | `05` | 5 | `02` | `0F` | `0A` `04` `00` `07` | dump |
| 6 | `06` | 6 | `03` | `00` | `08` `05` `0E` `01` | dump |
| 9 | `09` | 9 | `03` | `01` | `0B` `02` `0A` `06` | dump |
| high (10) | `0A` | 10 | `03` | `02` | `04` `03` `05` `01` | dump |

## Interpretation

- **Primary field:** offsets **107**, encoding `raw_u8` (identity).
- **Confidence:** high (7/7 dumps matched, 100%).
- **Catalog hint (Bricasti):** Diffusion - printed 1 ... 9 [differs_from_hint] - hint only; dumps win.
- **Catalog notes:** Manual UI: Low 1 - 9 High. Captured hardware series also show 0...10. SysEx stores an absolute encoded value @ 107.
- **Catalog note:** Observed min 0 is below printed manual 1 (unit/firmware variance; dump is authoritative)
- **Catalog note:** Observed max 10 is above printed manual 9 (unit/firmware variance; dump is authoritative)
- **Range:** Observed range 0 ... 10.
- **LOW endpoint:** `low.syx` -> encoded 0 (label 0).
- **HIGH/FULL endpoint:** `high.syx` -> encoded 10 (label 10).
- **Sampling:** extremes, adjacents, 5 sample mid(s) (not every step).
- **How to set:**
  1. encoded = desired_label
  2. byte[offset0] = encoded & 0x0F  # M7 payload nibbles are 0x00-0x0F
  3. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 146-147 (likely edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Other parameters

- [Delay Level](delay-level.md)
- [Delay Modulation](delay-modulation.md)
- [Delay Time](delay-time.md)
- [Density](density.md)
- **Diffusion** (this page)
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
