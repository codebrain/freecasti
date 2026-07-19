[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Density

_Generated 2026-07-19. Source folder: `sysex/prog/parameters/density/`._

## SysEx summary

- **Offsets:** 109
- **Encoding:** `raw_u8`
- **Confidence:** high
- **Range:** Observed range 0 ... 10
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Sets how the echo density builds up over time.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| Encoded | Offset 109 | Label | Source |
| --- | --- | --- | --- |
| 0 | `00` | Low | dump, provided, [1](../presets/ambience/clear-ambience.md), [2](../presets/rooms/glass-room.md), [3](../presets/rooms/small-tiled.md), [4](../presets/rooms/studio-c.md), [5](../presets/rooms/studio-e.md), +2 more |
| 1 | `01` | 1 | dump, provided, [1](../presets/ambience/deep-ambience.md), [2](../presets/ambience/large-and-bright.md), [3](../presets/ambience/long-ambience.md), [4](../presets/ambience/small-and-bright.md), [5](../presets/halls/clear-hall.md), +6 more |
| 2 | `02` | 2 | dump, provided, [1](../presets/halls/large-and-near.md), [2](../presets/halls/large-hall.md), [3](../presets/halls/sandors-hall.md), [4](../presets/rooms/heavy-room.md), [5](../presets/rooms/large-tiled.md), +2 more |
| 3 | `03` | 3 | dump, provided, [1](../presets/ambience/large-and-dark.md), [2](../presets/ambience/large-ambience.md), [3](../presets/ambience/medium-and-dark.md), [4](../presets/ambience/small-and-dark.md), [5](../presets/chambers/large-chamber.md), +13 more |
| 4 | `04` | 4 | dump, provided, [1](../presets/ambience/bass-xxl.md), [2](../presets/chambers/a-and-m-chamber.md), [3](../presets/chambers/amb-chamber-a.md), [4](../presets/chambers/amb-chamber-b.md), [5](../presets/chambers/deep-chamber.md), +14 more |
| 5 | `05` | 5 | provided, [1](../presets/halls/brass-hall.md), [2](../presets/halls/large-and-dark.md), [3](../presets/halls/large-and-deep.md), [4](../presets/halls/small-and-near.md), [5](../presets/halls/small-hall.md), +4 more |
| 6 | `06` | 6 | provided, [1](../presets/halls/boston-hall-b.md), [2](../presets/halls/dense-hall.md), [3](../presets/halls/vienna-hall.md), [4](../presets/rooms/deep-stone.md), [5](../presets/rooms/small-vox-room.md), +1 more |
| 7 | `07` | 7 | provided, [1](../presets/ambience/percussion-air.md), [2](../presets/chambers/cd-chamber.md), [3](../presets/chambers/snare-chamber.md), [4](../presets/plates/bright-plate.md), [5](../presets/plates/dark-plate.md), +2 more |
| 8 | `08` | 8 | provided, [1](../presets/plates/cd-plate-a.md), [2](../presets/plates/echo-plate.md), [3](../presets/plates/fat-plate.md), [4](../presets/plates/gold-plate.md), [5](../presets/plates/silver-plate.md), +1 more |
| 9 | `09` | 9 | dump, provided, [1](../presets/plates/large-plate.md), [2](../presets/plates/small-plate.md), [3](../presets/plates/snare-plate-a.md), [4](../presets/plates/snare-plate-b.md) |
| 10 | `0A` | High | dump, provided, [1](../presets/chambers/kick-chamber.md), [2](../presets/plates/cd-plate-b.md), [3](../presets/plates/dense-plate.md), [4](../presets/plates/london-plate.md) |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **0:** **Ambience:** [Clear Ambience](../presets/ambience/clear-ambience.md); **Rooms:** [Glass Room](../presets/rooms/glass-room.md), [Small Tiled](../presets/rooms/small-tiled.md), [Studio C](../presets/rooms/studio-c.md), [Studio E](../presets/rooms/studio-e.md); **Spaces:** [Car Park](../presets/spaces/car-park.md), [Stone Quarry](../presets/spaces/stone-quarry.md)
- **1:** **Ambience:** [Deep Ambience](../presets/ambience/deep-ambience.md), [Large & Bright](../presets/ambience/large-and-bright.md), [Long Ambience](../presets/ambience/long-ambience.md), [Small & Bright](../presets/ambience/small-and-bright.md); **Halls:** [Clear Hall](../presets/halls/clear-hall.md), [Concert Hall](../presets/halls/concert-hall.md), [Gold Hall](../presets/halls/gold-hall.md); **Rooms:** [Large Q Room](../presets/rooms/large-q-room.md), [Marble Foyer](../presets/rooms/marble-foyer.md); **Spaces:** [Arena](../presets/spaces/arena.md), [West Church](../presets/spaces/west-church.md)
- **2:** **Halls:** [Large & Near](../presets/halls/large-and-near.md), [Large Hall](../presets/halls/large-hall.md), [Sandors Hall](../presets/halls/sandors-hall.md); **Rooms:** [Heavy Room](../presets/rooms/heavy-room.md), [Large Tiled](../presets/rooms/large-tiled.md), [Small Q Room](../presets/rooms/small-q-room.md); **Spaces:** [Scoring Stage](../presets/spaces/scoring-stage.md)
- **3:** **Ambience:** [Large & Dark](../presets/ambience/large-and-dark.md), [Large Ambience](../presets/ambience/large-ambience.md), [Medium & Dark](../presets/ambience/medium-and-dark.md), [Small & Dark](../presets/ambience/small-and-dark.md); **Chambers:** [Large Chamber](../presets/chambers/large-chamber.md), [Medium Chamber](../presets/chambers/medium-chamber.md), [Small Chamber](../presets/chambers/small-chamber.md); **Halls:** [Berliner Hall](../presets/halls/berliner-hall.md), [Medium & Near](../presets/halls/medium-and-near.md), [Medium Hall](../presets/halls/medium-hall.md); **Rooms:** [Center Room](../presets/rooms/center-room.md), [Djangos Room](../presets/rooms/djangos-room.md), [Front Room](../presets/rooms/front-room.md), [Large Wooden](../presets/rooms/large-wooden.md), [Small Wooden](../presets/rooms/small-wooden.md), [Studio D](../presets/rooms/studio-d.md); **Spaces:** [North Church](../presets/spaces/north-church.md), [Tanglewood](../presets/spaces/tanglewood.md)
- **4:** **Ambience:** [Bass  XXL](../presets/ambience/bass-xxl.md); **Chambers:** [A&M Chamber](../presets/chambers/a-and-m-chamber.md), [Amb Chamber A](../presets/chambers/amb-chamber-a.md), [Amb Chamber B](../presets/chambers/amb-chamber-b.md), [Deep Chamber](../presets/chambers/deep-chamber.md), [Large & Bright](../presets/chambers/large-and-bright.md), [Old Chamber](../presets/chambers/old-chamber.md); **Halls:** [Amsterdam Hall](../presets/halls/amsterdam-hall.md), [Boston Hall A](../presets/halls/boston-hall-a.md), [Chicago Hall](../presets/halls/chicago-hall.md), [Medium & Deep](../presets/halls/medium-and-deep.md), [Worcester Hall](../presets/halls/worcester-hall.md); **Plates:** [Crystal Plate](../presets/plates/crystal-plate.md); **Rooms:** [Drum & Chamber](../presets/rooms/drum-and-chamber.md), [Large Room](../presets/rooms/large-room.md), [Music Room](../presets/rooms/music-room.md); **Spaces:** [Cinema Room](../presets/spaces/cinema-room.md), [Redwood Valley](../presets/spaces/redwood-valley.md), [South Church](../presets/spaces/south-church.md)
- **5:** **Halls:** [Brass Hall](../presets/halls/brass-hall.md), [Large & Dark](../presets/halls/large-and-dark.md), [Large & Deep](../presets/halls/large-and-deep.md), [Small & Near](../presets/halls/small-and-near.md), [Small Hall](../presets/halls/small-hall.md), [The ArchDuke](../presets/halls/the-archduke.md); **Rooms:** [Back Room](../presets/rooms/back-room.md), [Small Room](../presets/rooms/small-room.md); **Spaces:** [East Church](../presets/spaces/east-church.md)
- **6:** **Halls:** [Boston Hall B](../presets/halls/boston-hall-b.md), [Dense Hall](../presets/halls/dense-hall.md), [Vienna Hall](../presets/halls/vienna-hall.md); **Rooms:** [Deep Stone](../presets/rooms/deep-stone.md), [Small Vox Room](../presets/rooms/small-vox-room.md); **Spaces:** [Bath House](../presets/spaces/bath-house.md)
- **7:** **Ambience:** [Percussion Air](../presets/ambience/percussion-air.md); **Chambers:** [CD Chamber](../presets/chambers/cd-chamber.md), [Snare Chamber](../presets/chambers/snare-chamber.md); **Plates:** [Bright Plate](../presets/plates/bright-plate.md), [Dark Plate](../presets/plates/dark-plate.md), [Percussion](../presets/plates/percussion.md); **Rooms:** [Studio B Far](../presets/rooms/studio-b-far.md)
- **8:** **Plates:** [CD Plate A](../presets/plates/cd-plate-a.md), [Echo Plate](../presets/plates/echo-plate.md), [Fat Plate](../presets/plates/fat-plate.md), [Gold Plate](../presets/plates/gold-plate.md), [Silver Plate](../presets/plates/silver-plate.md); **Rooms:** [Studio A](../presets/rooms/studio-a.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 109 | Encoded | Display lo 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- |
| low (0) | `00` | 0 | `07` | `05` `08` `03` `05` | dump |
| 1 | `01` | 1 | `08` | `01` `08` `0A` `03` | dump |
| 2 | `02` | 2 | `09` | `01` `0A` `0D` `08` | dump |
| 3 | `03` | 3 | `0A` | `05` `0B` `05` `0E` | dump |
| 4 | `04` | 4 | `0C` | `0D` `0E` `09` `0B` | dump |
| 9 | `09` | 9 | `0D` | `09` `06` `07` `09` | dump |
| high (10) | `0A` | 10 | `0D` | `05` `04` `03` `0F` | dump |

## Interpretation

- **Primary field:** offsets **109**, encoding `raw_u8` (identity).
- **Confidence:** high (5/5 dumps matched, 100%).
- **Catalog hint (Bricasti):** Density - printed 1 ... 9 [differs_from_hint] - hint only; dumps win.
- **Catalog notes:** Manual UI: Low 1 - 9 High. Captured hardware series also show 0...10.
- **Catalog note:** Observed min 0 is below printed manual 1 (unit/firmware variance; dump is authoritative)
- **Catalog note:** Observed max 10 is above printed manual 9 (unit/firmware variance; dump is authoritative)
- **Range:** Observed range 0 ... 10.
- **LOW endpoint:** `low.syx` -> encoded 0 (label 0).
- **HIGH/FULL endpoint:** `high.syx` -> encoded 10 (label 10).
- **Sampling:** extremes, adjacents, 3 sample mid(s) (not every step).
- **How to set:**
  1. encoded = desired_label
  2. byte[offset0] = encoded & 0x0F  # M7 payload nibbles are 0x00-0x0F
  3. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 147 (display low nibble) (edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Unseen values

Documented in the spec (encoding map / manual) but not yet witnessed in a committed dump. "Possible" spans every encoded step in this field's range; missing steps are listed as ranges when there are many.

- **Encoding range:** encoded 0–10 (11 steps documented).
- **Never captured on the wire (4):**
  - encoded **5** → 5 (provided, preset)
  - encoded **6** → 6 (provided, preset)
  - encoded **7** → 7 (provided, preset)
  - encoded **8** → 8 (provided, preset)
- **Documented gaps (no row at all):** none between documented min/max.
- **Wire nibbles never observed (`0`–`F`):** offset 109: `B` `C` `D` `E` `F`

## Other parameters

- [Delay Level](delay-level.md)
- [Delay Modulation](delay-modulation.md)
- [Delay Time](delay-time.md)
- **Density** (this page)
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
- [Rolloff](rolloff.md)
- [Size](size.md)
- [VLF Cut](vlf-cut.md)
