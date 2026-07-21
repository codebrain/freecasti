[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Size

_Generated 2026-07-21. Source folder: `sysex/prog/parameters/size/`._

## SysEx summary

- **Offsets:** 102-103
- **Encoding:** `nibble_hilo`
- **Confidence:** high
- **Range:** Observed range 0 ... 30
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Adjusts the apparent size of the late reverberant field.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| `nibble_hilo` | Offset 102 | Offset 103 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | Small | dump, provided, [1](../presets/rooms/red-room.md), [2](../presets/rooms/small-room.md), [3](../presets/rooms/small-tiled.md), [4](../presets/rooms/small-vox-room.md), [5](../presets/rooms-2/small-room.md), +2 more |
| 1 | `00` | `01` | 1 | dump, provided, [1](../presets/rooms/studio-e.md) |
| 2 | `00` | `02` | 2 | dump, provided, [1](../presets/chambers/small-chamber.md), [2](../presets/plates/percussion.md), [3](../presets/rooms/djangos-room.md), [4](../presets/rooms/front-room.md), [5](../presets/rooms/studio-a.md), +1 more |
| 3 | `00` | `03` | 3 | provided, [1](../presets/ambience/percussion-air.md), [2](../presets/ambience/small-and-dark.md), [3](../presets/chambers/medium-chamber.md), [4](../presets/chambers/snare-chamber.md), [5](../presets/plates/dense-plate.md), +3 more |
| 4 | `00` | `04` | 4 | provided, [1](../presets/ambience/small-and-bright.md), [2](../presets/plates/bright-plate.md), [3](../presets/plates/dark-plate.md), [4](../presets/plates/london-plate.md), [5](../presets/rooms/back-room.md) |
| 5 | `00` | `05` | 5 | provided, [1](../presets/chambers/large-and-bright.md), [2](../presets/chambers/large-chamber.md), [3](../presets/chambers/old-chamber.md), [4](../presets/plates/fat-plate.md), [5](../presets/plates/small-plate.md), +6 more |
| 6 | `00` | `06` | 6 | provided, [1](../presets/halls/small-and-near.md), [2](../presets/halls/small-hall.md), [3](../presets/rooms/large-wooden.md) |
| 7 | `00` | `07` | 7 | dump, provided, [1](../presets/halls/berliner-hall.md), [2](../presets/halls/the-archduke.md), [3](../presets/halls/vienna-hall.md), [4](../presets/plates/cd-plate-b.md) |
| 8 | `00` | `08` | 8 | provided, [1](../presets/ambience/medium-and-dark.md), [2](../presets/chambers/deep-chamber.md), [3](../presets/halls/worcester-hall.md), [4](../presets/plates/cd-plate-a.md), [5](../presets/plates/silver-plate.md), +1 more |
| 9 | `00` | `09` | 9 | provided, [1](../presets/chambers/cd-chamber.md) |
| 10 | `00` | `0A` | 10 | provided, [1](../presets/chambers/kick-chamber.md), [2](../presets/halls/boston-hall-a.md), [3](../presets/halls/clear-hall.md), [4](../presets/plates/gold-plate.md), [5](../presets/plates/large-plate.md), +5 more |
| 11 | `00` | `0B` | 11 | provided, [1](../presets/spaces/north-church.md) |
| 12 | `00` | `0C` | 12 | provided, [1](../presets/halls/amsterdam-hall.md), [2](../presets/halls/boston-hall-b.md), [3](../presets/spaces/south-church.md) |
| 13 | `00` | `0D` | 13 | provided, [1](../presets/spaces-2/cathedral.md) |
| 14 | `00` | `0E` | 14 | provided, [1](../presets/spaces-2/concert-wave.md) |
| 15 | `00` | `0F` | 15 | dump, provided, [1](../presets/ambience/clear-ambience.md), [2](../presets/ambience/large-and-bright.md), [3](../presets/ambience/large-and-dark.md), [4](../presets/ambience/large-ambience.md), [5](../presets/chambers/a-and-m-chamber.md), +6 more |
| 16 | `01` | `00` | 16 | provided, [1](../presets/halls/piano-hall.md), [2](../presets/rooms-2/vocal-chamber.md) |
| 17 | `01` | `01` | 17 | provided, [1](../presets/plates/crystal-plate.md) |
| 18 | `01` | `02` | 18 | provided, [1](../presets/halls/dense-hall.md), [2](../presets/spaces/scoring-stage.md) |
| 19 | `01` | `03` | 19 | provided |
| 20 | `01` | `04` | 20 | provided, [1](../presets/chambers/amb-chamber-a.md), [2](../presets/halls/chicago-hall.md), [3](../presets/halls/concert-hall.md), [4](../presets/halls/large-and-dark.md), [5](../presets/halls/large-and-near.md), +5 more |
| 21 | `01` | `05` | 21 | provided, [1](../presets/spaces-2/brick-chamber.md) |
| 22 | `01` | `06` | 22 | provided, [1](../presets/halls/reflect-hall-b.md), [2](../presets/halls-2/med-and-stage.md), [3](../presets/spaces/reflect-chapel.md) |
| 23 | `01` | `07` | 23 | provided, [1](../presets/halls/gold-hall.md), [2](../presets/halls/medium-hall.md) |
| 24 | `01` | `08` | 24 | provided, [1](../presets/ambience/deep-ambience.md) |
| 25 | `01` | `09` | 25 | provided, [1](../presets/ambience/long-ambience.md), [2](../presets/halls/large-and-deep.md) |
| 26 | `01` | `0A` | 26 | provided |
| 27 | `01` | `0B` | 27 | provided, [1](../presets/halls-2/large-and-stage.md), [2](../presets/spaces-2/open-space.md) |
| 28 | `01` | `0C` | 28 | dump, provided, [1](../presets/halls/large-hall.md), [2](../presets/spaces/arena.md) |
| 29 | `01` | `0D` | 29 | dump, provided |
| 30 | `01` | `0E` | Large | dump, provided, [1](../presets/ambience/bass-xxl.md), [2](../presets/spaces/academy-yard.md), [3](../presets/spaces/car-park.md), [4](../presets/spaces/europa.md), [5](../presets/spaces/hillside.md), +5 more |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **0:** **Rooms:** [Red Room](../presets/rooms/red-room.md), [Small Room](../presets/rooms/small-room.md), [Small Tiled](../presets/rooms/small-tiled.md), [Small Vox Room](../presets/rooms/small-vox-room.md); **Rooms 2:** [Small Room](../presets/rooms-2/small-room.md), [Studio 1](../presets/rooms-2/studio-1.md); **Spaces:** [Cinema Room](../presets/spaces/cinema-room.md)
- **2:** **Chambers:** [Small Chamber](../presets/chambers/small-chamber.md); **Plates:** [Percussion](../presets/plates/percussion.md); **Rooms:** [Djangos Room](../presets/rooms/djangos-room.md), [Front Room](../presets/rooms/front-room.md), [Studio A](../presets/rooms/studio-a.md), [Studio C](../presets/rooms/studio-c.md)
- **3:** **Ambience:** [Percussion Air](../presets/ambience/percussion-air.md), [Small & Dark](../presets/ambience/small-and-dark.md); **Chambers:** [Medium Chamber](../presets/chambers/medium-chamber.md), [Snare Chamber](../presets/chambers/snare-chamber.md); **Plates:** [Dense Plate](../presets/plates/dense-plate.md), [Echo Plate](../presets/plates/echo-plate.md); **Rooms:** [Center Room](../presets/rooms/center-room.md), [Glass Room](../presets/rooms/glass-room.md)
- **5:** **Chambers:** [Large & Bright](../presets/chambers/large-and-bright.md), [Large Chamber](../presets/chambers/large-chamber.md), [Old Chamber](../presets/chambers/old-chamber.md); **Plates:** [Fat Plate](../presets/plates/fat-plate.md), [Small Plate](../presets/plates/small-plate.md); **Rooms:** [Deep Stone](../presets/rooms/deep-stone.md), [Heavy Room](../presets/rooms/heavy-room.md), [Large Room](../presets/rooms/large-room.md), [Small Wooden](../presets/rooms/small-wooden.md), [Studio B Far](../presets/rooms/studio-b-far.md), [Studio D](../presets/rooms/studio-d.md)
- **8:** **Ambience:** [Medium & Dark](../presets/ambience/medium-and-dark.md); **Chambers:** [Deep Chamber](../presets/chambers/deep-chamber.md); **Halls:** [Worcester Hall](../presets/halls/worcester-hall.md); **Plates:** [CD Plate A](../presets/plates/cd-plate-a.md), [Silver Plate](../presets/plates/silver-plate.md); **Rooms:** [Marble Foyer](../presets/rooms/marble-foyer.md)
- **10:** **Chambers:** [Kick Chamber](../presets/chambers/kick-chamber.md); **Halls:** [Boston Hall A](../presets/halls/boston-hall-a.md), [Clear Hall](../presets/halls/clear-hall.md); **Plates:** [Gold Plate](../presets/plates/gold-plate.md), [Large Plate](../presets/plates/large-plate.md), [Snare Plate A](../presets/plates/snare-plate-a.md), [Snare Plate B](../presets/plates/snare-plate-b.md); **Rooms:** [Drum & Chamber](../presets/rooms/drum-and-chamber.md), [Large Tiled](../presets/rooms/large-tiled.md), [Small Q Room](../presets/rooms/small-q-room.md)
- **15:** **Ambience:** [Clear Ambience](../presets/ambience/clear-ambience.md), [Large & Bright](../presets/ambience/large-and-bright.md), [Large & Dark](../presets/ambience/large-and-dark.md), [Large Ambience](../presets/ambience/large-ambience.md); **Chambers:** [A&M Chamber](../presets/chambers/a-and-m-chamber.md), [Amb Chamber B](../presets/chambers/amb-chamber-b.md); **Halls:** [Brass Hall](../presets/halls/brass-hall.md), [Medium & Deep](../presets/halls/medium-and-deep.md); **Spaces:** [Bath House](../presets/spaces/bath-house.md), [East Church](../presets/spaces/east-church.md), [Stone Quarry](../presets/spaces/stone-quarry.md)
- **20:** **Chambers:** [Amb Chamber A](../presets/chambers/amb-chamber-a.md); **Halls:** [Chicago Hall](../presets/halls/chicago-hall.md), [Concert Hall](../presets/halls/concert-hall.md), [Large & Dark](../presets/halls/large-and-dark.md), [Large & Near](../presets/halls/large-and-near.md), [Medium & Near](../presets/halls/medium-and-near.md), [Sandors Hall](../presets/halls/sandors-hall.md); **Rooms:** [Large Q Room](../presets/rooms/large-q-room.md), [Music Room](../presets/rooms/music-room.md); **Spaces:** [West Church](../presets/spaces/west-church.md)
- **30:** **Ambience:** [Bass  XXL](../presets/ambience/bass-xxl.md); **Spaces:** [Academy Yard](../presets/spaces/academy-yard.md), [Car Park](../presets/spaces/car-park.md), [Europa](../presets/spaces/europa.md), [Hillside](../presets/spaces/hillside.md), [Redwood Valley](../presets/spaces/redwood-valley.md), [Tanglewood](../presets/spaces/tanglewood.md); **Spaces 2:** [Music Forest](../presets/spaces-2/music-forest.md), [Oak Ballroom](../presets/spaces-2/oak-ballroom.md), [Waving Bloom](../presets/spaces-2/waving-bloom.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 102 | Offset 103 | `nibble_hilo` | Display lo 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| small (0) | `00` | `00` | 0 | `01` | `0D` `0D` `07` `06` | dump |
| 1 | `00` | `01` | 1 | `02` | `03` `00` `01` `0E` | dump |
| 2 | `00` | `02` | 2 | `03` | `08` `07` `05` `04` | dump |
| 7 | `00` | `07` | 7 | `04` | `0D` `0E` `07` `08` | dump |
| 15 | `00` | `0F` | 15 | `05` | `0F` `07` `02` `0F` | dump |
| 28 | `01` | `0C` | 28 | `05` | `05` `0D` `0B` `04` | dump |
| 29 | `01` | `0D` | 29 | `06` | `0B` `00` `0D` `0C` | dump |
| large (30) | `01` | `0E` | 30 | `07` | `00` `07` `09` `06` | dump |

## Interpretation

- **Primary field:** offsets **102-103**, encoding `nibble_hilo` (identity).
- **Confidence:** high (6/6 dumps matched, 100%).
- **Catalog hint (Bricasti):** Size - printed 1 ... 24 [differs_from_hint] - hint only; dumps win.
- **Catalog notes:** Manual UI: Small 1 - 24 Large. This unit uses Small / numbered / Large endpoints (may exceed 24).
- **Catalog note:** Observed min 0 is below printed manual 1 (unit/firmware variance; dump is authoritative)
- **Catalog note:** Observed max 30 is above printed manual 24 (unit/firmware variance; dump is authoritative)
- **Range:** Observed range 0 ... 30.
- **LOW endpoint:** `small.syx` -> encoded 0 (label 0).
- **HIGH/FULL endpoint:** `large.syx` -> encoded 30 (label 30).
- **Sampling:** extremes, adjacents, 4 sample mid(s) (not every step).
- **How to set:**
  1. encoded = desired_label
  2. byte[offset0] = (encoded >> 4) & 0x0F
  3. byte[offset1] = encoded & 0x0F
  4. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 147 (display low nibble) (edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Unseen values

Documented in the spec (encoding map / manual) but not yet witnessed in a committed dump. "Possible" spans every encoded step in this field's range; missing steps are listed as ranges when there are many.

- **Encoding range:** encoded 0–30 (31 steps documented).
- **Never captured on the wire (23):** encoded 3–6, 8–14, 16–27 — see the [encoding map](#encoding-map) above for each label.
- **Documented gaps (no row at all):** none between documented min/max.
- **Wire nibbles never observed (`0`–`F`):** offset 102 (high): `2` `3` `4` `5` `6` `7` `8` `9` `A` `B` `C` `D` `E` `F`; offset 103 (low): none

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
- [Rolloff](rolloff.md)
- **Size** (this page)
- [VLF Cut](vlf-cut.md)
