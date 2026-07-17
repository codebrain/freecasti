[Overview](../README.md) | [Parameters](../parameters/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Early Select

_Generated 2026-07-18. Source folder: `sysex/prog/parameters/early select/`._

## SysEx summary

- **Offsets:** 128-129
- **Encoding:** `nibble_hilo`
- **Confidence:** high
- **Range:** Range 0 ... 31 (capture extremes)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Controls the build up and decay characteristics of the early part of the reverberant field. The V2 addendum expands the selection beyond the printed 0–20 to 0–31 with larger, more spread-out early variants for a slower early reverb build-up (available on both V1 and V2 algorithm presets).

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf); [Bricasti M7 V2 Manual Addendum](https://www.bricasti.com/images/M7_V2_Manual_Addendum_Upgrade.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| Encoded | Offset 128 | Offset 129 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | 0 | dump, provided, [1](../presets/plates/cd-plate-a.md) |
| 1 | `00` | `01` | 1 | dump, provided, [1](../presets/ambience/small-and-dark.md), [2](../presets/rooms/small-vox-room.md) |
| 2 | `00` | `02` | 2 | dump, provided, [1](../presets/plates/cd-plate-b.md), [2](../presets/plates/fat-plate.md), [3](../presets/plates/gold-plate.md), [4](../presets/plates/london-plate.md), [5](../presets/rooms/studio-d.md) |
| 3 | `00` | `03` | 3 | provided, [1](../presets/ambience/small-and-bright.md), [2](../presets/chambers/kick-chamber.md), [3](../presets/plates/percussion.md), [4](../presets/plates/snare-plate-b.md), [5](../presets/rooms/front-room.md) |
| 4 | `00` | `04` | 4 | provided, [1](../presets/plates/crystal-plate.md), [2](../presets/plates/dense-plate.md), [3](../presets/plates/small-plate.md), [4](../presets/rooms/studio-a.md), [5](../presets/rooms/studio-c.md), +2 more |
| 5 | `00` | `05` | 5 | provided, [1](../presets/ambience/medium-and-dark.md), [2](../presets/chambers/amb-chamber-a.md), [3](../presets/chambers/medium-chamber.md), [4](../presets/chambers/small-chamber.md), [5](../presets/chambers/snare-chamber.md), +3 more |
| 6 | `00` | `06` | 6 | provided, [1](../presets/ambience/percussion-air.md), [2](../presets/chambers/cd-chamber.md), [3](../presets/chambers/large-and-bright.md), [4](../presets/chambers/large-chamber.md), [5](../presets/halls/large-and-dark.md), +4 more |
| 7 | `00` | `07` | 7 | provided, [1](../presets/chambers/a-and-m-chamber.md), [2](../presets/halls/small-and-near.md), [3](../presets/plates/large-plate.md), [4](../presets/rooms/back-room.md), [5](../presets/rooms/large-room.md) |
| 8 | `00` | `08` | 8 | dump, provided, [1](../presets/chambers/amb-chamber-b.md), [2](../presets/halls/chicago-hall.md), [3](../presets/plates/dark-plate.md) |
| 9 | `00` | `09` | 9 | provided, [1](../presets/ambience/clear-ambience.md), [2](../presets/ambience/large-and-dark.md), [3](../presets/chambers/deep-chamber.md), [4](../presets/chambers/old-chamber.md), [5](../presets/halls/boston-hall-b.md), +8 more |
| 10 | `00` | `0A` | 10 | provided, [1](../presets/halls/berliner-hall.md) |
| 11 | `00` | `0B` | 11 | provided, [1](../presets/plates-2/snare-plate.md), [2](../presets/rooms-2/fat-chamber.md), [3](../presets/rooms-2/studio-1.md), [4](../presets/spaces-2/dark-warm-room.md) |
| 12 | `00` | `0C` | 12 | provided, [1](../presets/ambience/large-and-bright.md), [2](../presets/ambience/large-ambience.md), [3](../presets/halls/boston-hall-a.md), [4](../presets/rooms/studio-b-far.md) |
| 13 | `00` | `0D` | 13 | provided, [1](../presets/halls/large-hall.md) |
| 14 | `00` | `0E` | 14 | dump, provided, [1](../presets/halls/large-and-near.md) |
| 15 | `00` | `0F` | 15 | provided, [1](../presets/halls/amsterdam-hall.md), [2](../presets/plates/bright-plate.md), [3](../presets/rooms/small-q-room.md), [4](../presets/spaces/north-church.md) |
| 16 | `01` | `00` | 16 | provided, [1](../presets/halls/vienna-hall.md), [2](../presets/spaces/west-church.md) |
| 17 | `01` | `01` | 17 | provided, [1](../presets/halls/large-and-deep.md), [2](../presets/halls/medium-and-deep.md), [3](../presets/halls/medium-and-near.md), [4](../presets/rooms/music-room.md) |
| 18 | `01` | `02` | 18 | provided, [1](../presets/halls/dense-hall.md), [2](../presets/rooms/large-tiled.md), [3](../presets/spaces/tanglewood.md) |
| 19 | `01` | `03` | 19 | provided, [1](../presets/ambience/bass-xxl.md), [2](../presets/ambience/deep-ambience.md), [3](../presets/ambience/long-ambience.md), [4](../presets/halls/brass-hall.md), [5](../presets/halls/concert-hall.md), +13 more |
| 20 | `01` | `04` | 20 | provided, [1](../presets/halls-2/jazz-hall.md), [2](../presets/halls-2/small-church.md), [3](../presets/nonlin/nonlin-c.md), [4](../presets/plates-2/rich-plate-b.md), [5](../presets/rooms-2/music-club.md), +3 more |
| 21 | `01` | `05` | 21 | provided, [1](../presets/halls/reflect-hall-a.md), [2](../presets/halls-2/large-hall.md), [3](../presets/rooms-2/lg-wood-room.md) |
| 22 | `01` | `06` | 22 | provided, [1](../presets/halls/pepes-hall-a.md), [2](../presets/halls/pepes-hall-b.md), [3](../presets/rooms-2/marble-room.md), [4](../presets/spaces-2/live-room.md), [5](../presets/spaces-2/shimmering-sky.md) |
| 23 | `01` | `07` | 23 | provided, [1](../presets/halls-2/live-hall.md), [2](../presets/halls-2/med-and-stage.md), [3](../presets/halls-2/small-and-stage.md), [4](../presets/nonlin/nonlin-d.md) |
| 24 | `01` | `08` | 24 | provided, [1](../presets/halls-2/large-church.md), [2](../presets/spaces-2/concert-wave.md), [3](../presets/spaces-2/lush-church.md), [4](../presets/spaces-2/open-space.md) |
| 25 | `01` | `09` | 25 | dump, provided, [1](../presets/halls-2/concert-a.md), [2](../presets/rooms-2/guitar-room.md) |
| 26 | `01` | `0A` | 26 | provided |
| 27 | `01` | `0B` | 27 | provided, [1](../presets/spaces-2/oak-ballroom.md) |
| 28 | `01` | `0C` | 28 | provided, [1](../presets/halls-2/large-and-stage.md) |
| 29 | `01` | `0D` | 29 | provided, [1](../presets/spaces-2/brick-chamber.md) |
| 30 | `01` | `0E` | 30 | dump, provided |
| 31 | `01` | `0F` | 31 | dump, provided, [1](../presets/spaces-2/long-vox-space.md), [2](../presets/spaces-2/music-forest.md), [3](../presets/spaces-2/waving-bloom.md) |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **4:** **Plates:** [Crystal Plate](../presets/plates/crystal-plate.md), [Dense Plate](../presets/plates/dense-plate.md), [Small Plate](../presets/plates/small-plate.md); **Rooms:** [Studio A](../presets/rooms/studio-a.md), [Studio C](../presets/rooms/studio-c.md), [Studio E](../presets/rooms/studio-e.md); **Spaces:** [Car Park](../presets/spaces/car-park.md)
- **5:** **Ambience:** [Medium & Dark](../presets/ambience/medium-and-dark.md); **Chambers:** [Amb Chamber A](../presets/chambers/amb-chamber-a.md), [Medium Chamber](../presets/chambers/medium-chamber.md), [Small Chamber](../presets/chambers/small-chamber.md), [Snare Chamber](../presets/chambers/snare-chamber.md); **Plates:** [Silver Plate](../presets/plates/silver-plate.md), [Snare Plate A](../presets/plates/snare-plate-a.md); **Rooms:** [Center Room](../presets/rooms/center-room.md)
- **6:** **Ambience:** [Percussion Air](../presets/ambience/percussion-air.md); **Chambers:** [CD Chamber](../presets/chambers/cd-chamber.md), [Large & Bright](../presets/chambers/large-and-bright.md), [Large Chamber](../presets/chambers/large-chamber.md); **Halls:** [Large & Dark](../presets/halls/large-and-dark.md), [Small Hall](../presets/halls/small-hall.md), [The ArchDuke](../presets/halls/the-archduke.md); **Rooms:** [Djangos Room](../presets/rooms/djangos-room.md), [Small Room](../presets/rooms/small-room.md)
- **9:** **Ambience:** [Clear Ambience](../presets/ambience/clear-ambience.md), [Large & Dark](../presets/ambience/large-and-dark.md); **Chambers:** [Deep Chamber](../presets/chambers/deep-chamber.md), [Old Chamber](../presets/chambers/old-chamber.md); **Halls:** [Boston Hall B](../presets/halls/boston-hall-b.md), [Clear Hall](../presets/halls/clear-hall.md); **Rooms:** [Deep Stone](../presets/rooms/deep-stone.md), [Drum & Chamber](../presets/rooms/drum-and-chamber.md), [Heavy Room](../presets/rooms/heavy-room.md), [Large Wooden](../presets/rooms/large-wooden.md), [Small Tiled](../presets/rooms/small-tiled.md), [Small Wooden](../presets/rooms/small-wooden.md); **Spaces:** [Cinema Room](../presets/spaces/cinema-room.md)
- **19:** **Ambience:** [Bass  XXL](../presets/ambience/bass-xxl.md), [Deep Ambience](../presets/ambience/deep-ambience.md), [Long Ambience](../presets/ambience/long-ambience.md); **Halls:** [Brass Hall](../presets/halls/brass-hall.md), [Concert Hall](../presets/halls/concert-hall.md), [Gold Hall](../presets/halls/gold-hall.md), [Sandors Hall](../presets/halls/sandors-hall.md), [Worcester Hall](../presets/halls/worcester-hall.md); **Plates:** [Echo Plate](../presets/plates/echo-plate.md); **Rooms:** [Glass Room](../presets/rooms/glass-room.md), [Large Q Room](../presets/rooms/large-q-room.md), [Marble Foyer](../presets/rooms/marble-foyer.md); **Spaces:** [Arena](../presets/spaces/arena.md), [East Church](../presets/spaces/east-church.md), [Redwood Valley](../presets/spaces/redwood-valley.md), [Scoring Stage](../presets/spaces/scoring-stage.md), [South Church](../presets/spaces/south-church.md), [Stone Quarry](../presets/spaces/stone-quarry.md)
- **20:** **Halls 2:** [Jazz Hall](../presets/halls-2/jazz-hall.md), [Small Church](../presets/halls-2/small-church.md); **NonLin:** [NonLin C](../presets/nonlin/nonlin-c.md); **Plates 2:** [Rich Plate B](../presets/plates-2/rich-plate-b.md); **Rooms 2:** [Music Club](../presets/rooms-2/music-club.md); **Spaces:** [Reflect Chapel](../presets/spaces/reflect-chapel.md), [Reflect Church](../presets/spaces/reflect-church.md); **Spaces 2:** [Ice House](../presets/spaces-2/ice-house.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 128 | Offset 129 | `nibble_hilo` | Offset 146 | Offset 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | `00` | `00` | 0 | `09` | `0B` | `05` `09` `02` `00` | dump |
| 1 | `00` | `01` | 1 | `09` | `0C` | `00` `05` `05` `08` | dump |
| 2 | `00` | `02` | 2 | `09` | `0D` | `02` `00` `03` `01` | dump |
| 8 | `00` | `08` | 8 | `09` | `0E` | `0F` `0F` `08` `0B` | dump |
| 14 | `00` | `0E` | 14 | `0A` | `00` | `08` `07` `04` `09` | dump |
| 25 | `01` | `09` | 25 | `0A` | `01` | `0C` `04` `04` `0F` | dump |
| 30 | `01` | `0E` | 30 | `0A` | `02` | `0D` `02` `06` `0D` | dump |
| 31 | `01` | `0F` | 31 | `0A` | `03` | `08` `0E` `09` `0D` | dump |

## Interpretation

- **Primary field:** offsets **128-129**, encoding `nibble_hilo` (identity).
- **Confidence:** high (8/8 dumps matched, 100%).
- **Catalog hint (Bricasti):** Early Select - printed 0 ... 20 [differs_from_hint] - hint only; dumps win.
- **Catalog notes:** Manual prints 0 - 20; this project's M7 reaches 0 - 31. Treat the printed range as a hint only.
- **Catalog note:** Observed max 31 is above printed manual 20 (unit/firmware variance; dump is authoritative)
- **Range:** Range 0 ... 31 (capture extremes).
- **Sampling:** extremes, adjacents, 4 sample mid(s) (not every step).
- **Edge slopes:** Low and high extreme->adjacent slopes agree - strong evidence for a global linear/affine map.
- **How to set:**
  1. encoded = desired_label
  2. byte[offset0] = (encoded >> 4) & 0x0F
  3. byte[offset1] = encoded & 0x0F
  4. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 146-147 (likely edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Other parameters

- [Delay Level](delay-level.md)
- [Delay Modulation](delay-modulation.md)
- [Delay Time](delay-time.md)
- [Density](density.md)
- [Diffusion](diffusion.md)
- [Early Rolloff](early-rolloff.md)
- **Early Select** (this page)
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
