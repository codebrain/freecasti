[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Early/Reverb Mix

_Generated 2026-07-18. Source folder: `sysex/prog/parameters/early to reverb mix/`._

## SysEx summary

- **Offsets:** 124-125
- **Encoding:** `nibble_hilo`
- **Confidence:** high
- **Range:** Balance path 0/20 ... 20/20 ... 20/0 (positions 0 ... 40; filenames use A.B for '/')
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Sets the balance between the early and later parts of the reverberant fields.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| `nibble_hilo` | Offset 124 | Offset 125 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | 0/20 | dump, provided, [1](../presets/nonlin/nonlin-a.md), [2](../presets/spaces-2/ice-beads.md), [3](../presets/spaces-2/long-vox-space.md) |
| 1 | `00` | `01` | 1/20 | dump, provided |
| 2 | `00` | `02` | 2/20 | dump, provided |
| 3 | `00` | `03` | 3/20 | dump, provided |
| 4 | `00` | `04` | 4/20 | provided |
| 5 | `00` | `05` | 5/20 | provided, [1](../presets/halls/large-and-deep.md) |
| 6 | `00` | `06` | 6/20 | provided, [1](../presets/halls/medium-and-deep.md) |
| 7 | `00` | `07` | 7/20 | provided, [1](../presets/halls/large-hall.md) |
| 8 | `00` | `08` | 8/20 | provided, [1](../presets/halls-2/jazz-hall.md), [2](../presets/halls-2/large-hall.md), [3](../presets/halls-2/medium-hall.md), [4](../presets/spaces/europa.md) |
| 9 | `00` | `09` | 9/20 | provided, [1](../presets/rooms-2/music-club.md), [2](../presets/spaces-2/big-bottom.md) |
| 10 | `00` | `0A` | 10/20 | provided, [1](../presets/chambers/old-chamber.md), [2](../presets/halls/medium-hall.md) |
| 11 | `00` | `0B` | 11/20 | provided, [1](../presets/rooms-2/sm-wood-room.md) |
| 12 | `00` | `0C` | 12/20 | provided, [1](../presets/halls-2/small-and-stage.md) |
| 13 | `00` | `0D` | 13/20 | provided, [1](../presets/rooms/music-room.md), [2](../presets/spaces/stone-quarry.md) |
| 14 | `00` | `0E` | 14/20 | provided, [1](../presets/chambers/amb-chamber-a.md), [2](../presets/halls/large-and-dark.md), [3](../presets/spaces/arena.md) |
| 15 | `00` | `0F` | 15/20 | provided, [1](../presets/chambers/a-and-m-chamber.md), [2](../presets/halls/chicago-hall.md), [3](../presets/plates/gold-plate.md) |
| 16 | `01` | `00` | 16/20 | provided, [1](../presets/chambers/amb-chamber-b.md), [2](../presets/chambers/deep-chamber.md), [3](../presets/halls/small-hall.md), [4](../presets/halls/the-archduke.md), [5](../presets/halls/worcester-hall.md), +2 more |
| 17 | `01` | `01` | 17/20 | provided, [1](../presets/rooms/deep-stone.md), [2](../presets/spaces/north-church.md) |
| 18 | `01` | `02` | 18/20 | provided, [1](../presets/chambers/cd-chamber.md), [2](../presets/halls/amsterdam-hall.md), [3](../presets/halls/boston-hall-a.md), [4](../presets/halls/boston-hall-b.md), [5](../presets/halls/medium-and-near.md), +6 more |
| 19 | `01` | `03` | 19/20 | dump, provided, [1](../presets/halls/sandors-hall.md), [2](../presets/plates/snare-plate-b.md), [3](../presets/rooms/large-q-room.md), [4](../presets/spaces/scoring-stage.md), [5](../presets/spaces/south-church.md), +1 more |
| 20 | `01` | `04` | 20/20 | dump, provided, [1](../presets/ambience/bass-xxl.md), [2](../presets/chambers/kick-chamber.md), [3](../presets/chambers/large-and-bright.md), [4](../presets/chambers/large-chamber.md), [5](../presets/chambers/medium-chamber.md), +19 more |
| 21 | `01` | `05` | 20/19 | dump, provided, [1](../presets/halls/vienna-hall.md), [2](../presets/rooms/heavy-room.md), [3](../presets/rooms/large-wooden.md), [4](../presets/rooms/studio-b-far.md), [5](../presets/rooms/studio-e.md) |
| 22 | `01` | `06` | 20/18 | dump, provided, [1](../presets/halls/berliner-hall.md), [2](../presets/halls/brass-hall.md), [3](../presets/plates/cd-plate-a.md), [4](../presets/plates/percussion.md), [5](../presets/plates/small-plate.md), +3 more |
| 23 | `01` | `07` | 20/17 | provided, [1](../presets/rooms/glass-room.md), [2](../presets/rooms/marble-foyer.md), [3](../presets/rooms/studio-c.md) |
| 24 | `01` | `08` | 20/16 | provided, [1](../presets/halls/small-and-near.md), [2](../presets/rooms/front-room.md), [3](../presets/rooms/large-room.md), [4](../presets/rooms/small-tiled.md), [5](../presets/spaces/tanglewood.md) |
| 25 | `01` | `09` | 20/15 | provided, [1](../presets/ambience/deep-ambience.md), [2](../presets/rooms/studio-a.md) |
| 26 | `01` | `0A` | 20/14 | provided, [1](../presets/rooms/studio-k.md), [2](../presets/spaces-2/med-space.md) |
| 27 | `01` | `0B` | 20/13 | provided, [1](../presets/ambience/clear-ambience.md), [2](../presets/ambience/large-and-dark.md), [3](../presets/ambience/medium-and-dark.md), [4](../presets/ambience/small-and-bright.md), [5](../presets/ambience/small-and-dark.md) |
| 28 | `01` | `0C` | 20/12 | dump, provided, [1](../presets/ambience/large-and-bright.md) |
| 29 | `01` | `0D` | 20/11 | provided, [1](../presets/rooms/blue-room.md), [2](../presets/rooms/sf-perf-room.md) |
| 30 | `01` | `0E` | 20/10 | provided, [1](../presets/ambience/large-ambience.md), [2](../presets/ambience/long-ambience.md), [3](../presets/plates/crystal-plate.md), [4](../presets/rooms/small-room.md) |
| 31 | `01` | `0F` | 20/9 | provided, [1](../presets/ambience/percussion-air.md) |
| 32 | `02` | `00` | 20/8 | provided, [1](../presets/rooms/small-vox-room.md) |
| 33 | `02` | `01` | 20/7 | provided |
| 34 | `02` | `02` | 20/6 | dump, provided |
| 35 | `02` | `03` | 20/5 | provided |
| 36 | `02` | `04` | 20/4 | provided |
| 37 | `02` | `05` | 20/3 | provided |
| 38 | `02` | `06` | 20/2 | provided |
| 39 | `02` | `07` | 20/1 | dump, provided |
| 40 | `02` | `08` | 20/0 | dump, provided |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **16:** **Chambers:** [Amb Chamber B](../presets/chambers/amb-chamber-b.md), [Deep Chamber](../presets/chambers/deep-chamber.md); **Halls:** [Small Hall](../presets/halls/small-hall.md), [The ArchDuke](../presets/halls/the-archduke.md), [Worcester Hall](../presets/halls/worcester-hall.md); **Rooms:** [Back Room](../presets/rooms/back-room.md); **Spaces:** [Bath House](../presets/spaces/bath-house.md)
- **18:** **Chambers:** [CD Chamber](../presets/chambers/cd-chamber.md); **Halls:** [Amsterdam Hall](../presets/halls/amsterdam-hall.md), [Boston Hall A](../presets/halls/boston-hall-a.md), [Boston Hall B](../presets/halls/boston-hall-b.md), [Medium & Near](../presets/halls/medium-and-near.md); **Plates:** [Echo Plate](../presets/plates/echo-plate.md), [Silver Plate](../presets/plates/silver-plate.md); **Rooms:** [Drum & Chamber](../presets/rooms/drum-and-chamber.md), [Small Q Room](../presets/rooms/small-q-room.md), [Studio D](../presets/rooms/studio-d.md); **Spaces:** [Car Park](../presets/spaces/car-park.md)
- **19:** **Halls:** [Sandors Hall](../presets/halls/sandors-hall.md); **Plates:** [Snare Plate B](../presets/plates/snare-plate-b.md); **Rooms:** [Large Q Room](../presets/rooms/large-q-room.md); **Spaces:** [Scoring Stage](../presets/spaces/scoring-stage.md), [South Church](../presets/spaces/south-church.md), [West Church](../presets/spaces/west-church.md)
- **20:** **Ambience:** [Bass  XXL](../presets/ambience/bass-xxl.md); **Chambers:** [Kick Chamber](../presets/chambers/kick-chamber.md), [Large & Bright](../presets/chambers/large-and-bright.md), [Large Chamber](../presets/chambers/large-chamber.md), [Medium Chamber](../presets/chambers/medium-chamber.md), [Small Chamber](../presets/chambers/small-chamber.md), [Snare Chamber](../presets/chambers/snare-chamber.md); **Halls:** [Clear Hall](../presets/halls/clear-hall.md), [Concert Hall](../presets/halls/concert-hall.md), [Dense Hall](../presets/halls/dense-hall.md), [Gold Hall](../presets/halls/gold-hall.md), [Large & Near](../presets/halls/large-and-near.md); **Plates:** [Bright Plate](../presets/plates/bright-plate.md), [CD Plate B](../presets/plates/cd-plate-b.md), [Dark Plate](../presets/plates/dark-plate.md), [Dense Plate](../presets/plates/dense-plate.md), [Fat Plate](../presets/plates/fat-plate.md), [Large Plate](../presets/plates/large-plate.md), [London Plate](../presets/plates/london-plate.md), [Snare Plate A](../presets/plates/snare-plate-a.md); **Rooms:** [Center Room](../presets/rooms/center-room.md), [Small Wooden](../presets/rooms/small-wooden.md); **Spaces:** [Cinema Room](../presets/spaces/cinema-room.md), [Redwood Valley](../presets/spaces/redwood-valley.md)
- **22:** **Halls:** [Berliner Hall](../presets/halls/berliner-hall.md), [Brass Hall](../presets/halls/brass-hall.md); **Plates:** [CD Plate A](../presets/plates/cd-plate-a.md), [Percussion](../presets/plates/percussion.md), [Small Plate](../presets/plates/small-plate.md); **Rooms:** [Djangos Room](../presets/rooms/djangos-room.md), [Large Tiled](../presets/rooms/large-tiled.md); **Spaces:** [East Church](../presets/spaces/east-church.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 124 | Offset 125 | `nibble_hilo` | Display lo 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 0/20 | `00` | `00` | 0 | `03` | `0B` `00` `08` `01` | dump |
| 1/20 | `00` | `01` | 1 | `04` | `0F` `02` `0C` `0A` | dump |
| 2/20 | `00` | `02` | 2 | `05` | `0F` `05` `0F` `06` | dump |
| 3/20 | `00` | `03` | 3 | `05` | `07` `07` `00` `08` | dump |
| 19/20 | `01` | `03` | 19 | `06` | `0F` `07` `04` `0F` | dump |
| 20/20 | `01` | `04` | 20 | `07` | `07` `0B` `08` `0D` | dump |
| 20/19 | `01` | `05` | 21 | `08` | `0F` `08` `02` `07` | dump |
| 20/18 | `01` | `06` | 22 | `09` | `0F` `0F` `01` `0B` | dump |
| 20/12 | `01` | `0C` | 28 | `0A` | `0E` `0D` `05` `0F` | dump |
| 20/6 | `02` | `02` | 34 | `0A` | `0B` `04` `0A` `07` | dump |
| 20/1 | `02` | `07` | 39 | `0B` | `07` `0D` `09` `0A` | dump |
| 20/0 | `02` | `08` | 40 | `0C` | `0A` `06` `02` `0F` | dump |

## Interpretation

- **Primary field:** offsets **124-125**, encoding `nibble_hilo` (identity).
- **Confidence:** high (12/12 dumps matched, 100%).
- **Catalog hint (Bricasti):** Early/Reverb Mix - printed 0 ... 40 [match] - hint only; dumps win.
- **Catalog notes:** Official 0/20 ... 20/20 ... 20/0 balance path (positions 0...40 at 124-125). Capture filenames use A.B (0.20, 20.6, 20.0) because '/' is illegal in filenames — same values as UI/sheet A/B.
- **Range:** Balance path 0/20 ... 20/20 ... 20/0 (positions 0 ... 40; filenames use A.B for '/').
- **Display:** A/B mix with side max 20: 0/20 -> 20/20 -> 20/0 (filenames use A.B because '/' is illegal); fitted value is path position 0..40.
- **Sampling:** extremes, adjacents, 8 sample mid(s) (not every step).
- **Edge slopes:** Low and high extreme->adjacent slopes agree - strong evidence for a global linear/affine map.
- **How to set:**
  1. encoded = desired_label
  2. byte[offset0] = (encoded >> 4) & 0x0F
  3. byte[offset1] = encoded & 0x0F
  4. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
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
- **Early/Reverb Mix** (this page)
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
