[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Delay Time

_Generated 2026-07-19. Source folder: `sysex/prog/parameters/delay time/`._

## SysEx summary

- **Offsets:** 134-135
- **Encoding:** `nibble_hilo`
- **Confidence:** high
- **Range:** Range 100 ... 996 ms (capture extremes)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Delay time for a diffused set of eight voices spread in time (controlled as a single delay). Adds coloration and a late swell to the late reverb.

_Source: [Bricasti M7 V2 Manual Addendum](https://www.bricasti.com/images/M7_V2_Manual_Addendum_Upgrade.pdf)._

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| `nibble_hilo` | Offset 134 | Offset 135 | Label | Source |
| --- | --- | --- | --- | --- |
| 0 | `00` | `00` | 100 mSec | dump, provided, [1](../presets/ambience/bass-xxl.md), [2](../presets/ambience/clear-ambience.md), [3](../presets/ambience/deep-ambience.md), [4](../presets/ambience/heavy-ambience.md), [5](../presets/ambience/large-and-bright.md), +180 more |
| 1 | `00` | `01` | 108 mSec | dump, provided |
| 2 | `00` | `02` | 116 mSec | dump, provided |
| 3 | `00` | `03` | 124 mSec | provided |
| 4 | `00` | `04` | 132 mSec | provided |
| 5 | `00` | `05` | 140 mSec | provided, [1](../presets/chambers/fat-chamber.md) |
| 6 | `00` | `06` | 148 mSec | provided |
| 7 | `00` | `07` | 156 mSec | provided |
| 8 | `00` | `08` | 164 mSec | dump, provided |
| 9 | `00` | `09` | 172 mSec | provided |
| 10 | `00` | `0A` | 180 mSec | provided, [1](../presets/rooms-2/marble-room.md), [2](../presets/rooms-2/wide-room.md) |
| 11 | `00` | `0B` | 188 mSec | provided |
| 12 | `00` | `0C` | 196 mSec | provided, [1](../presets/plates-2/drum-plate.md) |
| 13 | `00` | `0D` | 204 mSec | provided, [1](../presets/plates-2/fat-plate.md), [2](../presets/rooms-2/lush-room.md), [3](../presets/spaces-2/dark-warm-room.md) |
| 14 | `00` | `0E` | 212 mSec | provided |
| 15 | `00` | `0F` | 220 mSec | provided |
| 16 | `01` | `00` | 228 mSec | provided |
| 17 | `01` | `01` | 236 mSec | provided, [1](../presets/chambers/stone-chamber.md), [2](../presets/halls-2/koncert-piano.md), [3](../presets/plates-2/vocal-shimmer.md), [4](../presets/rooms/long-wood-room.md) |
| 18 | `01` | `02` | 244 mSec | provided, [1](../presets/spaces-2/live-room.md) |
| 19 | `01` | `03` | 252 mSec | provided, [1](../presets/spaces-2/vox-ambience.md) |
| 20 | `01` | `04` | 260 mSec | provided, [1](../presets/chambers/tiled-chamber.md), [2](../presets/plates/vocal-plate-b.md) |
| 21 | `01` | `05` | 268 mSec | provided |
| 22 | `01` | `06` | 276 mSec | provided, [1](../presets/plates/repro-plate.md), [2](../presets/plates-2/vocal-plate-b.md) |
| 23 | `01` | `07` | 284 mSec | dump, provided, [1](../presets/rooms-2/dark-chamber.md) |
| 24 | `01` | `08` | 292 mSec | provided |
| 25 | `01` | `09` | 300 mSec | provided, [1](../presets/halls/pepes-hall-b.md), [2](../presets/halls/reflect-hall-b.md), [3](../presets/halls-2/live-hall.md), [4](../presets/rooms-2/guitar-room.md) |
| 26 | `01` | `0A` | 308 mSec | provided |
| 27 | `01` | `0B` | 316 mSec | provided |
| 28 | `01` | `0C` | 324 mSec | provided |
| 29 | `01` | `0D` | 332 mSec | provided |
| 30 | `01` | `0E` | 340 mSec | provided, [1](../presets/chambers/a-and-m-chamber-b.md), [2](../presets/rooms-2/vocal-chamber.md), [3](../presets/spaces/reflect-chapel.md) |
| 31 | `01` | `0F` | 348 mSec | provided, [1](../presets/chambers/echo-chamber.md) |
| 32 | `02` | `00` | 356 mSec | provided |
| 33 | `02` | `01` | 364 mSec | provided, [1](../presets/rooms-2/deep-chamber.md) |
| 34 | `02` | `02` | 372 mSec | dump, provided |
| 35 | `02` | `03` | 380 mSec | provided |
| 36 | `02` | `04` | 388 mSec | provided |
| 37 | `02` | `05` | 396 mSec | provided |
| 38 | `02` | `06` | 404 mSec | provided |
| 39 | `02` | `07` | 412 mSec | provided |
| 40 | `02` | `08` | 420 mSec | provided |
| 41 | `02` | `09` | 428 mSec | provided, [1](../presets/halls/mechanics-hall.md) |
| 42 | `02` | `0A` | 436 mSec | provided |
| 43 | `02` | `0B` | 444 mSec | provided, [1](../presets/halls/reflect-hall-a.md) |
| 44 | `02` | `0C` | 452 mSec | provided |
| 45 | `02` | `0D` | 460 mSec | provided |
| 46 | `02` | `0E` | 468 mSec | provided |
| 47 | `02` | `0F` | 476 mSec | provided |
| 48 | `03` | `00` | 484 mSec | provided |
| 49 | `03` | `01` | 492 mSec | dump, provided |
| 50 | `03` | `02` | 500 mSec | provided, [1](../presets/spaces/reflect-church.md), [2](../presets/spaces-2/cathedral.md), [3](../presets/spaces-2/open-space.md) |
| 51 | `03` | `03` | 508 mSec | provided |
| 52 | `03` | `04` | 516 mSec | provided |
| 53 | `03` | `05` | 524 mSec | provided |
| 54 | `03` | `06` | 532 mSec | provided |
| 55 | `03` | `07` | 540 mSec | provided |
| 56 | `03` | `08` | 548 mSec | provided |
| 57 | `03` | `09` | 556 mSec | provided |
| 58 | `03` | `0A` | 564 mSec | provided |
| 59 | `03` | `0B` | 572 mSec | provided |
| 60 | `03` | `0C` | 580 mSec | provided |
| 61 | `03` | `0D` | 588 mSec | provided |
| 62 | `03` | `0E` | 596 mSec | provided |
| 63 | `03` | `0F` | 604 mSec | provided |
| 64 | `04` | `00` | 612 mSec | provided |
| 65 | `04` | `01` | 620 mSec | provided |
| 66 | `04` | `02` | 628 mSec | provided |
| 67 | `04` | `03` | 636 mSec | provided |
| 68 | `04` | `04` | 644 mSec | provided |
| 69 | `04` | `05` | 652 mSec | provided |
| 70 | `04` | `06` | 660 mSec | provided, [1](../presets/spaces-2/ice-house.md), [2](../presets/spaces-2/shimmering-sky.md) |
| 71 | `04` | `07` | 668 mSec | provided |
| 72 | `04` | `08` | 676 mSec | provided, [1](../presets/spaces-2/oak-ballroom.md) |
| 73 | `04` | `09` | 684 mSec | provided |
| 74 | `04` | `0A` | 692 mSec | provided, [1](../presets/spaces-2/concert-wave.md) |
| 75 | `04` | `0B` | 700 mSec | provided |
| 76 | `04` | `0C` | 708 mSec | provided |
| 77 | `04` | `0D` | 716 mSec | provided |
| 78 | `04` | `0E` | 724 mSec | dump, provided |
| 79 | `04` | `0F` | 732 mSec | provided |
| 80 | `05` | `00` | 740 mSec | provided |
| 81 | `05` | `01` | 748 mSec | provided |
| 82 | `05` | `02` | 756 mSec | provided |
| 83 | `05` | `03` | 764 mSec | provided |
| 84 | `05` | `04` | 772 mSec | provided |
| 85 | `05` | `05` | 780 mSec | provided, [1](../presets/spaces-2/waving-bloom.md) |
| 86 | `05` | `06` | 788 mSec | provided |
| 87 | `05` | `07` | 796 mSec | provided |
| 88 | `05` | `08` | 804 mSec | provided |
| 89 | `05` | `09` | 812 mSec | provided |
| 90 | `05` | `0A` | 820 mSec | provided |
| 91 | `05` | `0B` | 828 mSec | provided |
| 92 | `05` | `0C` | 836 mSec | provided |
| 93 | `05` | `0D` | 844 mSec | provided |
| 94 | `05` | `0E` | 852 mSec | provided |
| 95 | `05` | `0F` | 860 mSec | provided |
| 96 | `06` | `00` | 868 mSec | provided |
| 97 | `06` | `01` | 876 mSec | provided |
| 98 | `06` | `02` | 884 mSec | provided |
| 99 | `06` | `03` | 892 mSec | provided |
| 100 | `06` | `04` | 900 mSec | provided |
| 101 | `06` | `05` | 908 mSec | provided |
| 102 | `06` | `06` | 916 mSec | provided |
| 103 | `06` | `07` | 924 mSec | provided |
| 104 | `06` | `08` | 932 mSec | provided |
| 105 | `06` | `09` | 940 mSec | provided |
| 106 | `06` | `0A` | 948 mSec | provided |
| 107 | `06` | `0B` | 956 mSec | provided |
| 108 | `06` | `0C` | 964 mSec | provided |
| 109 | `06` | `0D` | 972 mSec | provided |
| 110 | `06` | `0E` | 980 mSec | provided |
| 111 | `06` | `0F` | 988 mSec | dump, provided |
| 112 | `07` | `00` | 996 mSec | dump, provided |

### Preset witnesses

Factory presets that witness encoded steps with more than 5 matches (collapsed in the table above):

- **0:** **Ambience:** [Bass  XXL](../presets/ambience/bass-xxl.md), [Clear Ambience](../presets/ambience/clear-ambience.md), [Deep Ambience](../presets/ambience/deep-ambience.md), [Heavy Ambience](../presets/ambience/heavy-ambience.md), [Large & Bright](../presets/ambience/large-and-bright.md), [Large & Dark](../presets/ambience/large-and-dark.md), [Large Ambience](../presets/ambience/large-ambience.md), [Long Ambience](../presets/ambience/long-ambience.md), [Med & Bright](../presets/ambience/med-and-bright.md), [Med Ambience](../presets/ambience/med-ambience.md), [Medium & Dark](../presets/ambience/medium-and-dark.md), [Percussion Air](../presets/ambience/percussion-air.md), [Small & Bright](../presets/ambience/small-and-bright.md), [Small & Dark](../presets/ambience/small-and-dark.md), [Small Ambience](../presets/ambience/small-ambience.md); **Chambers:** [A&M Chamber](../presets/chambers/a-and-m-chamber.md), [Amb Chamber A](../presets/chambers/amb-chamber-a.md), [Amb Chamber B](../presets/chambers/amb-chamber-b.md), [CD Chamber](../presets/chambers/cd-chamber.md), [Deep Chamber](../presets/chambers/deep-chamber.md), [Kick Chamber](../presets/chambers/kick-chamber.md), [Large & Bright](../presets/chambers/large-and-bright.md), [Large & Dark](../presets/chambers/large-and-dark.md), [Large Chamber](../presets/chambers/large-chamber.md), [Medium Chamber](../presets/chambers/medium-chamber.md), [Old Chamber](../presets/chambers/old-chamber.md), [Small & Bright](../presets/chambers/small-and-bright.md), [Small & Dark](../presets/chambers/small-and-dark.md), [Small Chamber](../presets/chambers/small-chamber.md), [Snare Chamber](../presets/chambers/snare-chamber.md), [Sunset Chamber](../presets/chambers/sunset-chamber.md), [Vocal Chamber](../presets/chambers/vocal-chamber.md); **Halls:** [Amsterdam Hall](../presets/halls/amsterdam-hall.md), [Berliner Hall](../presets/halls/berliner-hall.md), [Boston Hall A](../presets/halls/boston-hall-a.md), [Boston Hall B](../presets/halls/boston-hall-b.md), [Brass Hall](../presets/halls/brass-hall.md), [Chicago Hall](../presets/halls/chicago-hall.md), [Clear Hall](../presets/halls/clear-hall.md), [Concert Hall](../presets/halls/concert-hall.md), [Dense Hall](../presets/halls/dense-hall.md), [Gold Hall](../presets/halls/gold-hall.md), [Large & Dark](../presets/halls/large-and-dark.md), [Large & Deep](../presets/halls/large-and-deep.md), [Large & Near](../presets/halls/large-and-near.md), [Large Hall](../presets/halls/large-hall.md), [Medium & Deep](../presets/halls/medium-and-deep.md), [Medium & Near](../presets/halls/medium-and-near.md), [Medium Hall](../presets/halls/medium-hall.md), [Pepes Hall A](../presets/halls/pepes-hall-a.md), [Piano Hall](../presets/halls/piano-hall.md), [Saint Gerold](../presets/halls/saint-gerold.md), [Saint Sylvain](../presets/halls/saint-sylvain.md), [Sandors Hall](../presets/halls/sandors-hall.md), [Small & Near](../presets/halls/small-and-near.md), [Small Hall](../presets/halls/small-hall.md), [The ArchDuke](../presets/halls/the-archduke.md), [Troy Hall](../presets/halls/troy-hall.md), [Vienna Hall](../presets/halls/vienna-hall.md), [Worcester Hall](../presets/halls/worcester-hall.md); **Halls 2:** [Concert A](../presets/halls-2/concert-a.md), [Concert B](../presets/halls-2/concert-b.md), [Jazz Hall](../presets/halls-2/jazz-hall.md), [Large & Stage](../presets/halls-2/large-and-stage.md), [Large Church](../presets/halls-2/large-church.md), [Large Hall](../presets/halls-2/large-hall.md), [Med & Stage](../presets/halls-2/med-and-stage.md), [Medium Hall](../presets/halls-2/medium-hall.md), [Small & Stage](../presets/halls-2/small-and-stage.md), [Small Church](../presets/halls-2/small-church.md), [Small Hall](../presets/halls-2/small-hall.md), [West Hall](../presets/halls-2/west-hall.md); **NonLin:** [NonLin A](../presets/nonlin/nonlin-a.md), [NonLin B](../presets/nonlin/nonlin-b.md), [NonLin C](../presets/nonlin/nonlin-c.md), [NonLin D](../presets/nonlin/nonlin-d.md); **Plates:** [Bright Plate](../presets/plates/bright-plate.md), [CD Plate A](../presets/plates/cd-plate-a.md), [CD Plate B](../presets/plates/cd-plate-b.md), [Crystal Plate](../presets/plates/crystal-plate.md), [Dark Plate](../presets/plates/dark-plate.md), [Dense Plate](../presets/plates/dense-plate.md), [Echo Plate](../presets/plates/echo-plate.md), [Fat Plate](../presets/plates/fat-plate.md), [Gold Plate](../presets/plates/gold-plate.md), [Large Plate](../presets/plates/large-plate.md), [London Plate](../presets/plates/london-plate.md), [Old Plate](../presets/plates/old-plate.md), [Percussion](../presets/plates/percussion.md), [Rich Plate](../presets/plates/rich-plate.md), [Silver Plate](../presets/plates/silver-plate.md), [Small Plate](../presets/plates/small-plate.md), [Snare Plate A](../presets/plates/snare-plate-a.md), [Snare Plate B](../presets/plates/snare-plate-b.md), [Sun Plate A](../presets/plates/sun-plate-a.md), [Sun Plate B](../presets/plates/sun-plate-b.md), [Sun Plate C](../presets/plates/sun-plate-c.md), [Vocal Plate](../presets/plates/vocal-plate.md); **Plates 2:** [Alpha Plate](../presets/plates-2/alpha-plate.md), [Dark Plate](../presets/plates-2/dark-plate.md), [Large Plate](../presets/plates-2/large-plate.md), [Plate A](../presets/plates-2/plate-a.md), [Rich Plate A](../presets/plates-2/rich-plate-a.md), [Rich Plate B](../presets/plates-2/rich-plate-b.md), [Small Plate](../presets/plates-2/small-plate.md), [Snare Plate](../presets/plates-2/snare-plate.md), [Thin Plate](../presets/plates-2/thin-plate.md), [Vocal Plate A](../presets/plates-2/vocal-plate-a.md); **Rooms:** [Back Room](../presets/rooms/back-room.md), [Blue Room](../presets/rooms/blue-room.md), [Center Room](../presets/rooms/center-room.md), [Corn Room](../presets/rooms/corn-room.md), [Deep Stone](../presets/rooms/deep-stone.md), [Djangos Room](../presets/rooms/djangos-room.md), [Drum & Chamber](../presets/rooms/drum-and-chamber.md), [Front Room](../presets/rooms/front-room.md), [Glass Room](../presets/rooms/glass-room.md), [Heavy Room](../presets/rooms/heavy-room.md), [Large Q Room](../presets/rooms/large-q-room.md), [Large Red Room](../presets/rooms/large-red-room.md), [Large Room](../presets/rooms/large-room.md), [Large Tiled](../presets/rooms/large-tiled.md), [Large Wooden](../presets/rooms/large-wooden.md), [Marble Foyer](../presets/rooms/marble-foyer.md), [Medium Tiled](../presets/rooms/medium-tiled.md), [Music Room](../presets/rooms/music-room.md), [Oakland Room](../presets/rooms/oakland-room.md), [Percussion](../presets/rooms/percussion.md), [Red Room](../presets/rooms/red-room.md), [SF Perf Room](../presets/rooms/sf-perf-room.md), [Small Q Room](../presets/rooms/small-q-room.md), [Small Room](../presets/rooms/small-room.md), [Small Tiled](../presets/rooms/small-tiled.md), [Small Vox Room](../presets/rooms/small-vox-room.md), [Small Wooden](../presets/rooms/small-wooden.md), [Studio A](../presets/rooms/studio-a.md), [Studio B Close](../presets/rooms/studio-b-close.md), [Studio B Far](../presets/rooms/studio-b-far.md), [Studio C](../presets/rooms/studio-c.md), [Studio D](../presets/rooms/studio-d.md), [Studio E](../presets/rooms/studio-e.md), [Studio K](../presets/rooms/studio-k.md), [Waits Room](../presets/rooms/waits-room.md); **Rooms 2:** [Bright Chamber](../presets/rooms-2/bright-chamber.md), [Fat Chamber](../presets/rooms-2/fat-chamber.md), [Large Chamber](../presets/rooms-2/large-chamber.md), [Large Room](../presets/rooms-2/large-room.md), [Lg Wood Room](../presets/rooms-2/lg-wood-room.md), [Med Room](../presets/rooms-2/med-room.md), [Music Club](../presets/rooms-2/music-club.md), [Sm Wood Room](../presets/rooms-2/sm-wood-room.md), [Small Chamber](../presets/rooms-2/small-chamber.md), [Small Room](../presets/rooms-2/small-room.md), [Studio 1](../presets/rooms-2/studio-1.md), [Studio 2](../presets/rooms-2/studio-2.md), [Studio 3](../presets/rooms-2/studio-3.md), [Studio 4](../presets/rooms-2/studio-4.md), [Tiled Room](../presets/rooms-2/tiled-room.md); **Spaces:** [Academy Yard](../presets/spaces/academy-yard.md), [Arena](../presets/spaces/arena.md), [Bath House](../presets/spaces/bath-house.md), [Car Park](../presets/spaces/car-park.md), [Cavern](../presets/spaces/cavern.md), [Cinema Room](../presets/spaces/cinema-room.md), [East Church](../presets/spaces/east-church.md), [Europa](../presets/spaces/europa.md), [Gated Space](../presets/spaces/gated-space.md), [Hillside](../presets/spaces/hillside.md), [North Church](../presets/spaces/north-church.md), [Redwood Valley](../presets/spaces/redwood-valley.md), [Scoring Stage](../presets/spaces/scoring-stage.md), [South Church](../presets/spaces/south-church.md), [Stone Quarry](../presets/spaces/stone-quarry.md), [Tanglewood](../presets/spaces/tanglewood.md), [West Church](../presets/spaces/west-church.md); **Spaces 2:** [Big Bottom](../presets/spaces-2/big-bottom.md), [Brick Chamber](../presets/spaces-2/brick-chamber.md), [Grand Church](../presets/spaces-2/grand-church.md), [Grand Stage](../presets/spaces-2/grand-stage.md), [Ice Beads](../presets/spaces-2/ice-beads.md), [Long Vox Space](../presets/spaces-2/long-vox-space.md), [Lush Church](../presets/spaces-2/lush-church.md), [Med Space](../presets/spaces-2/med-space.md), [Music Forest](../presets/spaces-2/music-forest.md), [Small Space](../presets/spaces-2/small-space.md)

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 134 | Offset 135 | `nibble_hilo` | Display lo 147 | Checksum 152-155 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 100 ms | `00` | `00` | 0 | `00` | `0C` `04` `0E` `05` | dump |
| 108 ms | `00` | `01` | 1 | `01` | `09` `04` `08` `09` | dump |
| 116 ms | `00` | `02` | 2 | `02` | `06` `04` `03` `0D` | dump |
| 164 ms | `00` | `08` | 8 | `03` | `00` `06` `02` `06` | dump |
| 284 ms | `01` | `07` | 23 | `04` | `0C` `09` `0F` `07` | dump |
| 372 ms | `02` | `02` | 34 | `05` | `01` `0C` `02` `09` | dump |
| 492 ms | `03` | `01` | 49 | `06` | `01` `00` `0C` `0C` | dump |
| 724 ms | `04` | `0E` | 78 | `06` | `09` `06` `04` `08` | dump |
| 988 ms | `06` | `0F` | 111 | `06` | `0B` `0E` `0B` `08` | dump |
| 996 ms | `07` | `00` | 112 | `07` | `07` `01` `0E` `01` | dump |

## Interpretation

- **Primary field:** offsets **134-135**, encoding `nibble_hilo` (encoded * 8 + (100)).
- **Confidence:** high (10/10 dumps matched, 100%).
- **Catalog hint (Bricasti):** Delay Time - printed 100 ... 1000 ms [match] - hint only; dumps win.
- **Catalog notes:** Printed 100 ms ... 1 s. This unit: label = 8*encoded + 100; captured high 996 ms (8 ms grid; 1000 would not land on a step).
- **Range:** Range 100 ... 996 ms (capture extremes).
- **Sampling:** extremes, adjacents, 6 sample mid(s) (not every step).
- **Edge slopes:** Low and high extreme->adjacent slopes agree - strong evidence for a global linear/affine map.
- **How to set:**
  1. encoded = round((desired_label - (100)) / 8.0)
  2. byte[offset0] = (encoded >> 4) & 0x0F
  3. byte[offset1] = encoded & 0x0F
  4. recompute trailing checksum: CRC-16/ARC over bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155
- **Secondary offsets:** 147 (display low nibble) (edit/UI state, not the parameter word).
- **Checksum nibbles:** 152-155 (CRC-16/ARC over offsets 8-151, packed high-nibble-first).


## Unseen values

Documented in the spec (encoding map / manual) but not yet witnessed in a committed dump. "Possible" spans every encoded step in this field's range; missing steps are listed as ranges when there are many.

- **Encoding range:** encoded 0–112 (113 steps documented).
- **Manual range not fully captured:** manual ceiling 1000 above captured max 996.
- **Never captured on the wire (103):** encoded 3–7, 9–22, 24–33, 35–48, 50–77, 79–110 — see the [encoding map](#encoding-map) above for each label.
- **Documented gaps (no row at all):** none between documented min/max.
- **Wire nibbles never observed (`0`–`F`):** offset 134 (high): `8` `9` `A` `B` `C` `D` `E` `F`; offset 135 (low): none

## Other parameters

- [Delay Level](delay-level.md)
- [Delay Modulation](delay-modulation.md)
- **Delay Time** (this page)
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
- [VLF Cut](vlf-cut.md)
