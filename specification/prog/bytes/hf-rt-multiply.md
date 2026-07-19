[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# HF RT Multiply

_Generated 2026-07-19. Source folder: `sysex/prog/parameters/hf rt multiply/`._

## SysEx summary

- **Offsets:** 114-115
- **Encoding:** `nibble_hilo`
- **Confidence:** high
- **Range:** Range 0.2 ... 1 (capture extremes)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

> **Capture note:** No hardware UI walk in `docs/reference/provided_labels.json` yet for this program parameter — encoding map is built from sparse labeled dumps — mid-steps may be **inferred** from the confirmed affine scale between sparse dumps and factory preset anchors.

## Description

Sets the high-frequency reverb time above the crossover frequency set by HF RT Crossover. Displayed and controlled as a scaling of Reverb Time.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| `nibble_hilo` | Offset 114 | Offset 115 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | 0.2 | dump, [1](../presets/nonlin/nonlin-a.md), [2](../presets/nonlin/nonlin-b.md), [3](../presets/nonlin/nonlin-c.md), [4](../presets/nonlin/nonlin-d.md), [5](../presets/spaces/europa.md), +3 more |
| 1 | `00` | `01` | 0.25 | dump |
| 2 | `00` | `02` | 0.3 | dump |
| 3 | `00` | `03` | 0.35 | dump, [1](../presets/spaces/hillside.md) |
| 4 | `00` | `04` | 0.4 | dump, [1](../presets/rooms/studio-k.md) |
| 5 | `00` | `05` | 0.45 | dump, [1](../presets/spaces/academy-yard.md) |
| 6 | `00` | `06` | 0.5 | dump, [1](../presets/ambience/bass-xxl.md), [2](../presets/spaces/car-park.md), [3](../presets/spaces/north-church.md) |
| 7 | `00` | `07` | 0.55 | dump, [1](../presets/halls/vienna-hall.md), [2](../presets/rooms/small-room.md), [3](../presets/rooms/small-vox-room.md), [4](../presets/spaces/east-church.md) |
| 8 | `00` | `08` | 0.6 | [1](../presets/halls/berliner-hall.md), [2](../presets/halls/clear-hall.md), [3](../presets/spaces/arena.md), [4](../presets/spaces/cinema-room.md), [5](../presets/spaces/redwood-valley.md), +1 more |
| 9 | `00` | `09` | 0.65 | [1](../presets/halls/amsterdam-hall.md), [2](../presets/rooms/back-room.md), [3](../presets/rooms/large-room.md), [4](../presets/spaces/stone-quarry.md), [5](../presets/spaces/tanglewood.md) |
| 10 | `00` | `0A` | 0.7 | [1](../presets/chambers/deep-chamber.md), [2](../presets/chambers/old-chamber.md), [3](../presets/halls/boston-hall-a.md), [4](../presets/halls/boston-hall-b.md), [5](../presets/halls/brass-hall.md), +8 more |
| 11 | `00` | `0B` | 0.75 | [1](../presets/chambers/amb-chamber-a.md), [2](../presets/chambers/amb-chamber-b.md), [3](../presets/halls/concert-hall.md), [4](../presets/halls/dense-hall.md), [5](../presets/halls/large-and-dark.md), +15 more |
| 12 | `00` | `0C` | 0.8 | [1](../presets/ambience/clear-ambience.md), [2](../presets/ambience/deep-ambience.md), [3](../presets/ambience/large-and-bright.md), [4](../presets/ambience/large-and-dark.md), [5](../presets/ambience/long-ambience.md), +25 more |
| 13 | `00` | `0D` | 0.85 | [1](../presets/ambience/large-ambience.md), [2](../presets/chambers/large-and-bright.md), [3](../presets/halls/large-and-deep.md), [4](../presets/plates/snare-plate-b.md), [5](../presets/rooms/djangos-room.md), +3 more |
| 14 | `00` | `0E` | 0.9 | [1](../presets/chambers/kick-chamber.md), [2](../presets/chambers/snare-chamber.md), [3](../presets/plates/cd-plate-b.md), [4](../presets/plates/snare-plate-a.md), [5](../presets/rooms/deep-stone.md), +2 more |
| 15 | `00` | `0F` | 0.95 | dump, [1](../presets/plates/london-plate.md) |
| 16 | `01` | `00` | 1 | dump, [1](../presets/chambers/sunset-chamber.md), [2](../presets/plates/rich-plate.md), [3](../presets/plates-2/dark-plate.md), [4](../presets/plates-2/snare-plate.md), [5](../presets/spaces-2/ice-beads.md), +1 more |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **0:** **NonLin:** [NonLin A](../presets/nonlin/nonlin-a.md), [NonLin B](../presets/nonlin/nonlin-b.md), [NonLin C](../presets/nonlin/nonlin-c.md), [NonLin D](../presets/nonlin/nonlin-d.md); **Spaces:** [Europa](../presets/spaces/europa.md), [Gated Space](../presets/spaces/gated-space.md); **Spaces 2:** [Brick Chamber](../presets/spaces-2/brick-chamber.md), [Waving Bloom](../presets/spaces-2/waving-bloom.md)
- **8:** **Halls:** [Berliner Hall](../presets/halls/berliner-hall.md), [Clear Hall](../presets/halls/clear-hall.md); **Spaces:** [Arena](../presets/spaces/arena.md), [Cinema Room](../presets/spaces/cinema-room.md), [Redwood Valley](../presets/spaces/redwood-valley.md), [South Church](../presets/spaces/south-church.md)
- **10:** **Chambers:** [Deep Chamber](../presets/chambers/deep-chamber.md), [Old Chamber](../presets/chambers/old-chamber.md); **Halls:** [Boston Hall A](../presets/halls/boston-hall-a.md), [Boston Hall B](../presets/halls/boston-hall-b.md), [Brass Hall](../presets/halls/brass-hall.md), [Gold Hall](../presets/halls/gold-hall.md), [Sandors Hall](../presets/halls/sandors-hall.md), [Worcester Hall](../presets/halls/worcester-hall.md); **Rooms:** [Drum & Chamber](../presets/rooms/drum-and-chamber.md), [Large Q Room](../presets/rooms/large-q-room.md), [Large Tiled](../presets/rooms/large-tiled.md), [Small Q Room](../presets/rooms/small-q-room.md); **Spaces:** [West Church](../presets/spaces/west-church.md)
- **11:** **Chambers:** [Amb Chamber A](../presets/chambers/amb-chamber-a.md), [Amb Chamber B](../presets/chambers/amb-chamber-b.md); **Halls:** [Concert Hall](../presets/halls/concert-hall.md), [Dense Hall](../presets/halls/dense-hall.md), [Large & Dark](../presets/halls/large-and-dark.md), [Large & Near](../presets/halls/large-and-near.md), [Large Hall](../presets/halls/large-hall.md), [Medium & Deep](../presets/halls/medium-and-deep.md), [Medium & Near](../presets/halls/medium-and-near.md), [Medium Hall](../presets/halls/medium-hall.md), [Small & Near](../presets/halls/small-and-near.md), [Small Hall](../presets/halls/small-hall.md), [The ArchDuke](../presets/halls/the-archduke.md); **Plates:** [CD Plate A](../presets/plates/cd-plate-a.md); **Rooms:** [Center Room](../presets/rooms/center-room.md), [Front Room](../presets/rooms/front-room.md), [Heavy Room](../presets/rooms/heavy-room.md), [Large Wooden](../presets/rooms/large-wooden.md), [Small Wooden](../presets/rooms/small-wooden.md); **Spaces:** [Scoring Stage](../presets/spaces/scoring-stage.md)
- **12:** **Ambience:** [Clear Ambience](../presets/ambience/clear-ambience.md), [Deep Ambience](../presets/ambience/deep-ambience.md), [Large & Bright](../presets/ambience/large-and-bright.md), [Large & Dark](../presets/ambience/large-and-dark.md), [Long Ambience](../presets/ambience/long-ambience.md), [Medium & Dark](../presets/ambience/medium-and-dark.md), [Percussion Air](../presets/ambience/percussion-air.md), [Small & Bright](../presets/ambience/small-and-bright.md), [Small & Dark](../presets/ambience/small-and-dark.md); **Chambers:** [A&M Chamber](../presets/chambers/a-and-m-chamber.md), [CD Chamber](../presets/chambers/cd-chamber.md), [Large Chamber](../presets/chambers/large-chamber.md), [Small Chamber](../presets/chambers/small-chamber.md); **Halls:** [Chicago Hall](../presets/halls/chicago-hall.md); **Plates:** [Bright Plate](../presets/plates/bright-plate.md), [Crystal Plate](../presets/plates/crystal-plate.md), [Dark Plate](../presets/plates/dark-plate.md), [Dense Plate](../presets/plates/dense-plate.md), [Echo Plate](../presets/plates/echo-plate.md), [Fat Plate](../presets/plates/fat-plate.md), [Gold Plate](../presets/plates/gold-plate.md), [Large Plate](../presets/plates/large-plate.md), [Percussion](../presets/plates/percussion.md), [Silver Plate](../presets/plates/silver-plate.md), [Small Plate](../presets/plates/small-plate.md); **Rooms:** [Marble Foyer](../presets/rooms/marble-foyer.md), [Small Tiled](../presets/rooms/small-tiled.md), [Studio B Far](../presets/rooms/studio-b-far.md), [Studio D](../presets/rooms/studio-d.md), [Studio E](../presets/rooms/studio-e.md)
- **13:** **Ambience:** [Large Ambience](../presets/ambience/large-ambience.md); **Chambers:** [Large & Bright](../presets/chambers/large-and-bright.md); **Halls:** [Large & Deep](../presets/halls/large-and-deep.md); **Plates:** [Snare Plate B](../presets/plates/snare-plate-b.md); **Rooms:** [Djangos Room](../presets/rooms/djangos-room.md), [Glass Room](../presets/rooms/glass-room.md), [Studio A](../presets/rooms/studio-a.md); **Spaces:** [Bath House](../presets/spaces/bath-house.md)
- **14:** **Chambers:** [Kick Chamber](../presets/chambers/kick-chamber.md), [Snare Chamber](../presets/chambers/snare-chamber.md); **Plates:** [CD Plate B](../presets/plates/cd-plate-b.md), [Snare Plate A](../presets/plates/snare-plate-a.md); **Rooms:** [Deep Stone](../presets/rooms/deep-stone.md), [Music Room](../presets/rooms/music-room.md), [Studio C](../presets/rooms/studio-c.md)
- **16:** **Chambers:** [Sunset Chamber](../presets/chambers/sunset-chamber.md); **Plates:** [Rich Plate](../presets/plates/rich-plate.md); **Plates 2:** [Dark Plate](../presets/plates-2/dark-plate.md), [Snare Plate](../presets/plates-2/snare-plate.md); **Spaces 2:** [Ice Beads](../presets/spaces-2/ice-beads.md), [Ice House](../presets/spaces-2/ice-house.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 114 | Offset 115 | `nibble_hilo` | Display 146–147 | display `nibble_hilo` | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.2 | `00` | `00` | 0 | `05 0C` | 92 | `0A` `0A` `0F` `08` | dump |
| 0.25 | `00` | `01` | 1 | `05 0D` | 93 | `0F` `0A` `0D` `09` | dump |
| 0.3 | `00` | `02` | 2 | `05 0E` | 94 | `00` `0A` `0B` `0A` | dump |
| 0.35 | `00` | `03` | 3 | `06 00` | 96 | `06` `08` `0C` `0F` | dump |
| 0.4 | `00` | `04` | 4 | `06 01` | 97 | `09` `08` `0A` `03` | dump |
| 0.45 | `00` | `05` | 5 | `06 02` | 98 | `00` `08` `0F` `0B` | dump |
| 0.5 | `00` | `06` | 6 | `06 03` | 99 | `03` `08` `0E` `01` | dump |
| 0.55 | `00` | `07` | 7 | `06 04` | 100 | `06` `08` `04` `08` | dump |
| 0.95 | `00` | `0F` | 15 | `06 04` | 100 | `0A` `08` `0A` `07` | dump |
| 1 | `01` | `00` | 16 | `06 05` | 101 | `05` `01` `0B` `05` | dump |

## Interpretation

- **Primary field:** offsets **114-115**, encoding `nibble_hilo` (encoded * 0.05 + (0.2)).
- **Confidence:** high (10/10 dumps matched, 100%).
- **Catalog hint (Bricasti):** HF RT Multiply - printed 0.2 ... 1.0 [match] - hint only; dumps win.
- **Catalog notes:** Closed-form scale @ 114-115: label = 0.05×encoded + 0.2.
- **Range:** Range 0.2 ... 1 (capture extremes).
- **Sampling:** extremes, adjacents, 6 sample mid(s) (not every step).
- **Edge slopes:** Low and high extreme->adjacent slopes agree - strong evidence for a global linear/affine map.
- **How to set:**
  1. encoded = round((desired_label - (0.2)) / 0.05)
  2. byte[offset0] = (encoded >> 4) & 0x0F
  3. byte[offset1] = encoded & 0x0F
  4. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 146–147 (`nibble_hilo` display) (edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Unseen values

Documented in the spec (encoding map / manual) but not yet witnessed in a committed dump. "Possible" spans every encoded step in this field's range; missing steps are listed as ranges when there are many.

- **Encoding range:** encoded 0–16 (17 steps documented).
- **Never captured on the wire (7):**
  - encoded **8** → 0.6 (preset)
  - encoded **9** → 0.65 (preset)
  - encoded **10** → 0.7 (preset)
  - encoded **11** → 0.75 (preset)
  - encoded **12** → 0.8 (preset)
  - encoded **13** → 0.85 (preset)
  - encoded **14** → 0.9 (preset)
- **Documented gaps (no row at all):** none between documented min/max.
- **Wire nibbles never observed (`0`–`F`):** offset 114 (high): `2` `3` `4` `5` `6` `7` `8` `9` `A` `B` `C` `D` `E` `F`; offset 115 (low): none

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
- **HF RT Multiply** (this page)
- [LF RT Crossover](lf-rt-crossover.md)
- [LF RT Multiply](lf-rt-multiply.md)
- [Modulation](modulation.md)
- [Pre Delay](predelay.md)
- [Reverb Time](reverb-time.md)
- [Rolloff](rolloff.md)
- [Size](size.md)
- [VLF Cut](vlf-cut.md)
