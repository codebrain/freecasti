[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# VLF Cut

_Generated 2026-07-22. Source folder: `sysex/prog/parameters/vlf cut/`._

## SysEx summary

- **Offsets:** 122-123
- **Encoding:** `nibble_hilo`
- **Confidence:** high
- **Range:** Range -20 ... 0 dB (capture extremes)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

> **Capture note:** No hardware UI walk in `docs/reference/provided_labels.json` yet for this program parameter — encoding map is built from sparse labeled dumps — mid-steps may be **inferred** from the confirmed affine scale between sparse dumps and factory preset anchors.

## Description

Cuts the very low frequency content of the initial part of both the early and late reverberant fields.

_Source: [Bricasti M7 Owner's Manual — Reverb Parameters](https://www.bricasti.com/images/M7.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| `nibble_hilo` | Offset 122 | Offset 123 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | -20 dB | dump, [1](../presets/ambience/clear-ambience.md), [2](../presets/plates/crystal-plate.md), [3](../presets/spaces/bath-house.md) |
| 1 | `00` | `01` | -19 dB | dump, [1](../presets/chambers/snare-chamber.md) |
| 2 | `00` | `02` | -18 dB | dump, [1](../presets/halls/pepes-hall-a.md), [2](../presets/halls/pepes-hall-b.md), [3](../presets/rooms-2/sm-wood-room.md), [4](../presets/spaces-2/brick-chamber.md) |
| 3 | `00` | `03` | -17 dB | dump, [1](../presets/chambers/a-and-m-chamber-b.md), [2](../presets/halls-2/small-church.md), [3](../presets/plates-2/rich-plate-a.md), [4](../presets/plates-2/rich-plate-b.md), [5](../presets/rooms/sf-perf-room.md), +1 more |
| 4 | `00` | `04` | -16 dB | [1](../presets/rooms-2/music-club.md) |
| 5 | `00` | `05` | -15 dB | [1](../presets/ambience/large-and-bright.md), [2](../presets/ambience/long-ambience.md), [3](../presets/chambers/large-chamber.md), [4](../presets/plates/bright-plate.md), [5](../presets/plates/dark-plate.md), +6 more |
| 6 | `00` | `06` | -14 dB | [1](../presets/chambers/a-and-m-chamber.md), [2](../presets/halls/sandors-hall.md) |
| 7 | `00` | `07` | -13 dB | [1](../presets/halls/the-archduke.md), [2](../presets/rooms/glass-room.md) |
| 8 | `00` | `08` | -12 dB | [1](../presets/chambers/large-and-bright.md), [2](../presets/chambers/medium-chamber.md), [3](../presets/chambers/small-chamber.md), [4](../presets/halls/large-hall.md), [5](../presets/rooms/center-room.md), +5 more |
| 9 | `00` | `09` | -11 dB | [1](../presets/ambience/small-and-bright.md), [2](../presets/chambers/amb-chamber-a.md), [3](../presets/halls/brass-hall.md), [4](../presets/halls/large-and-near.md), [5](../presets/halls/worcester-hall.md), +1 more |
| 10 | `00` | `0A` | -10 dB | dump, [1](../presets/ambience/deep-ambience.md), [2](../presets/ambience/large-and-dark.md), [3](../presets/ambience/large-ambience.md), [4](../presets/ambience/medium-and-dark.md), [5](../presets/ambience/small-and-dark.md), +18 more |
| 11 | `00` | `0B` | -9 dB | [1](../presets/chambers/old-chamber.md), [2](../presets/halls/boston-hall-b.md), [3](../presets/halls/vienna-hall.md), [4](../presets/plates/snare-plate-a.md), [5](../presets/rooms/large-q-room.md), +3 more |
| 12 | `00` | `0C` | -8 dB | dump, [1](../presets/chambers/amb-chamber-b.md), [2](../presets/rooms/deep-stone.md) |
| 13 | `00` | `0D` | -7 dB | [1](../presets/halls/small-and-near.md), [2](../presets/rooms/small-wooden.md) |
| 14 | `00` | `0E` | -6 dB | [1](../presets/ambience/percussion-air.md), [2](../presets/chambers/kick-chamber.md), [3](../presets/halls/amsterdam-hall.md), [4](../presets/halls/berliner-hall.md), [5](../presets/plates/cd-plate-b.md), +4 more |
| 15 | `00` | `0F` | -5 dB | [1](../presets/halls/large-and-dark.md), [2](../presets/halls/medium-and-deep.md), [3](../presets/spaces/scoring-stage.md) |
| 16 | `01` | `00` | -4 dB | dump, [1](../presets/halls/clear-hall.md), [2](../presets/spaces/cinema-room.md), [3](../presets/spaces/south-church.md) |
| 17 | `01` | `01` | -3 dB | [1](../presets/halls/dense-hall.md), [2](../presets/rooms/studio-a.md), [3](../presets/rooms/studio-b-far.md) |
| 18 | `01` | `02` | -2 dB | [1](../presets/halls/boston-hall-a.md), [2](../presets/plates/fat-plate.md), [3](../presets/rooms/studio-c.md) |
| 19 | `01` | `03` | -1 dB | dump, [1](../presets/rooms/studio-e.md) |
| 20 | `01` | `04` | 0 dB | dump, [1](../presets/ambience/bass-xxl.md), [2](../presets/halls/chicago-hall.md), [3](../presets/halls/gold-hall.md), [4](../presets/rooms/heavy-room.md), [5](../presets/rooms/studio-d.md), +1 more |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **3:** **Chambers:** [A&M Chamber B](../presets/chambers/a-and-m-chamber-b.md); **Halls 2:** [Small Church](../presets/halls-2/small-church.md); **Plates 2:** [Rich Plate A](../presets/plates-2/rich-plate-a.md), [Rich Plate B](../presets/plates-2/rich-plate-b.md); **Rooms:** [SF Perf Room](../presets/rooms/sf-perf-room.md); **Rooms 2:** [Vocal Chamber](../presets/rooms-2/vocal-chamber.md)
- **5:** **Ambience:** [Large & Bright](../presets/ambience/large-and-bright.md), [Long Ambience](../presets/ambience/long-ambience.md); **Chambers:** [Large Chamber](../presets/chambers/large-chamber.md); **Plates:** [Bright Plate](../presets/plates/bright-plate.md), [Dark Plate](../presets/plates/dark-plate.md), [Dense Plate](../presets/plates/dense-plate.md), [Echo Plate](../presets/plates/echo-plate.md), [Silver Plate](../presets/plates/silver-plate.md); **Rooms:** [Front Room](../presets/rooms/front-room.md), [Marble Foyer](../presets/rooms/marble-foyer.md); **Spaces:** [East Church](../presets/spaces/east-church.md)
- **8:** **Chambers:** [Large & Bright](../presets/chambers/large-and-bright.md), [Medium Chamber](../presets/chambers/medium-chamber.md), [Small Chamber](../presets/chambers/small-chamber.md); **Halls:** [Large Hall](../presets/halls/large-hall.md); **Rooms:** [Center Room](../presets/rooms/center-room.md), [Large Room](../presets/rooms/large-room.md), [Small Room](../presets/rooms/small-room.md), [Small Tiled](../presets/rooms/small-tiled.md), [Small Vox Room](../presets/rooms/small-vox-room.md); **Spaces:** [Car Park](../presets/spaces/car-park.md)
- **9:** **Ambience:** [Small & Bright](../presets/ambience/small-and-bright.md); **Chambers:** [Amb Chamber A](../presets/chambers/amb-chamber-a.md); **Halls:** [Brass Hall](../presets/halls/brass-hall.md), [Large & Near](../presets/halls/large-and-near.md), [Worcester Hall](../presets/halls/worcester-hall.md); **Plates:** [CD Plate A](../presets/plates/cd-plate-a.md)
- **10:** **Ambience:** [Deep Ambience](../presets/ambience/deep-ambience.md), [Large & Dark](../presets/ambience/large-and-dark.md), [Large Ambience](../presets/ambience/large-ambience.md), [Medium & Dark](../presets/ambience/medium-and-dark.md), [Small & Dark](../presets/ambience/small-and-dark.md); **Chambers:** [CD Chamber](../presets/chambers/cd-chamber.md), [Deep Chamber](../presets/chambers/deep-chamber.md); **Halls:** [Concert Hall](../presets/halls/concert-hall.md), [Large & Deep](../presets/halls/large-and-deep.md), [Medium & Near](../presets/halls/medium-and-near.md), [Medium Hall](../presets/halls/medium-hall.md), [Small Hall](../presets/halls/small-hall.md); **Plates:** [Gold Plate](../presets/plates/gold-plate.md), [Large Plate](../presets/plates/large-plate.md), [London Plate](../presets/plates/london-plate.md), [Percussion](../presets/plates/percussion.md), [Small Plate](../presets/plates/small-plate.md), [Snare Plate B](../presets/plates/snare-plate-b.md); **Rooms:** [Back Room](../presets/rooms/back-room.md), [Djangos Room](../presets/rooms/djangos-room.md), [Large Tiled](../presets/rooms/large-tiled.md); **Spaces:** [Arena](../presets/spaces/arena.md), [Redwood Valley](../presets/spaces/redwood-valley.md)
- **11:** **Chambers:** [Old Chamber](../presets/chambers/old-chamber.md); **Halls:** [Boston Hall B](../presets/halls/boston-hall-b.md), [Vienna Hall](../presets/halls/vienna-hall.md); **Plates:** [Snare Plate A](../presets/plates/snare-plate-a.md); **Rooms:** [Large Q Room](../presets/rooms/large-q-room.md), [Large Wooden](../presets/rooms/large-wooden.md), [Music Room](../presets/rooms/music-room.md); **Spaces:** [West Church](../presets/spaces/west-church.md)
- **14:** **Ambience:** [Percussion Air](../presets/ambience/percussion-air.md); **Chambers:** [Kick Chamber](../presets/chambers/kick-chamber.md); **Halls:** [Amsterdam Hall](../presets/halls/amsterdam-hall.md), [Berliner Hall](../presets/halls/berliner-hall.md); **Plates:** [CD Plate B](../presets/plates/cd-plate-b.md); **Rooms:** [Drum & Chamber](../presets/rooms/drum-and-chamber.md), [Small Q Room](../presets/rooms/small-q-room.md); **Spaces:** [North Church](../presets/spaces/north-church.md), [Tanglewood](../presets/spaces/tanglewood.md)
- **20:** **Ambience:** [Bass  XXL](../presets/ambience/bass-xxl.md); **Halls:** [Chicago Hall](../presets/halls/chicago-hall.md), [Gold Hall](../presets/halls/gold-hall.md); **Rooms:** [Heavy Room](../presets/rooms/heavy-room.md), [Studio D](../presets/rooms/studio-d.md); **Spaces:** [Stone Quarry](../presets/spaces/stone-quarry.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 122 | Offset 123 | `nibble_hilo` | Display 146–147 | display `nibble_hilo` | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -20 dB | `00` | `00` | 0 | `07 08` | 120 | `0A` `0F` `0E` `09` | dump |
| -19 dB | `00` | `01` | 1 | `07 09` | 121 | `06` `0E` `01` `04` | dump |
| -18 dB | `00` | `02` | 2 | `07 0A` | 122 | `06` `0C` `01` `00` | dump |
| -17 dB | `00` | `03` | 3 | `07 0B` | 123 | `0A` `0D` `0E` `0D` | dump |
| -10 dB | `00` | `0A` | 10 | `07 0C` | 124 | `06` `02` `09` `08` | dump |
| -8 dB | `00` | `0C` | 12 | `07 0D` | 125 | `0A` `06` `02` `05` | dump |
| -4 dB | `01` | `00` | 16 | `07 0E` | 126 | `0F` `0F` `06` `00` | dump |
| -1 dB | `01` | `03` | 19 | `07 0F` | 127 | `03` `0D` `01` `0D` | dump |
| 0 dB | `01` | `04` | 20 | `08 00` | 128 | `0C` `06` `00` `09` | dump |

## Interpretation

- **Primary field:** offsets **122-123**, encoding `nibble_hilo` (encoded + (-20)).
- **Confidence:** high (9/9 dumps matched, 100%).
- **Catalog hint (Bricasti):** VLF Cut - printed -18 ... 0 db [differs_from_hint] - hint only; dumps win.
- **Catalog notes:** Printed 0 to -18 dB. Some units/UI paths may show -20; record hardware truth, do not force the printed floor.
- **Catalog note:** Observed min -20 is below printed manual -18 (unit/firmware variance; dump is authoritative)
- **Range:** Range -20 ... 0 dB (capture extremes).
- **Sampling:** extremes, adjacents, 5 sample mid(s) (not every step).
- **Edge slopes:** Low and high extreme->adjacent slopes agree - strong evidence for a global linear/affine map.
- **How to set:**
  1. encoded = desired_label - (-20)
  2. byte[offset0] = (encoded >> 4) & 0x0F
  3. byte[offset1] = encoded & 0x0F
  4. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 146–147 (`nibble_hilo` display) (edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Unseen values

Documented in the spec (encoding map / manual) but not yet witnessed in a committed dump. "Possible" spans every encoded step in this field's range; missing steps are listed as ranges when there are many.

- **Encoding range:** encoded 0–20 (21 steps documented).
- **Never captured on the wire (12):**
  - encoded **4** → -16 dB (preset)
  - encoded **5** → -15 dB (preset)
  - encoded **6** → -14 dB (preset)
  - encoded **7** → -13 dB (preset)
  - encoded **8** → -12 dB (preset)
  - encoded **9** → -11 dB (preset)
  - encoded **11** → -9 dB (preset)
  - encoded **13** → -7 dB (preset)
  - encoded **14** → -6 dB (preset)
  - encoded **15** → -5 dB (preset)
  - encoded **17** → -3 dB (preset)
  - encoded **18** → -2 dB (preset)
- **Documented gaps (no row at all):** none between documented min/max.
- **Wire nibbles never observed (`0`–`F`):** offset 122 (high): `2` `3` `4` `5` `6` `7` `8` `9` `A` `B` `C` `D` `E` `F`; offset 123 (low): none

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
- [Size](size.md)
- **VLF Cut** (this page)
