[Overview](README.md) | [Bytes](bytes/README.md) | **Program identity** | [Preset inventory](preset-inventory.md) | [Preset sheet](preset-sheet.md) | [Byte map](byte-map-overview.md) | [Cross-series](cross.md) | [System dumps](../system/README.md)


# Program identity

_Generated 2026-07-21. Source folder: `sysex/prog/presets/` (222 dumps named `<bank name>.<preset name>.syx`)._

**Confidence:** high

Program name at offsets 8-21 (14-char editable; pad 22-23; factory dumps also space-pad through 87) match filename preset in 222/222 dumps. Bank index at 88-89 (nibble_hilo); mirrored at 137. Program slot within bank at 90-91 (nibble_hilo).

Decoded parameters: **[presets/](presets/)** (bank pages + [presets.json](presets/presets.json)).

Published-sheet comparison: **[preset-sheet.md](preset-sheet.md)** (8 hard / 3 soft-only discrepancies).

## Fields

- **Program name** offsets **8-21** (`ascii_space_padded`). Filename check: 222/222 dumps match (mismatch count 0). ASCII program name: 14-character editable label (manual) at offsets 8–21; trailing pad at 22–23 completes the 16-byte wire window. Bank name is not stored here. Factory preset dumps space-pad the remainder through offset 87; Reg-backed hold-EDIT dumps put a register basis blob at 24–87 instead. Factory validation still checks bytes[8:88] against the filename preset half, space-padded to 80 bytes.
- **Bank index** offsets **88-89** (`nibble_hilo`). Factory/user bank select. Low nibble at offset 89 carries the index in this corpus (offset 88 stayed 00). Offset 137 always equals offset 89.
- **Program slot** offsets **90-91** (`nibble_hilo`). Slot within the current bank (not a global program number). Halls samples: Large Hall=0, Medium Hall=1, Small Hall=2, Large & Near=3 (factory list order). Rooms uses contiguous slots 0–35 (Long Wood Room at 35).

## Bank index map

| Bank | Encoded | Bytes 88-89 | Mirror 137 | Presets |
|------|--------:|-------------|------------|---------|
| [Halls](presets/halls/) | 0 | `00` `00` | `00` | 32 |
| [Plates](presets/plates/) | 1 | `00` `01` | `01` | 24 |
| [Rooms](presets/rooms/) | 2 | `00` `02` | `02` | 36 |
| [Chambers](presets/chambers/) | 3 | `00` `03` | `03` | 22 |
| [Ambience](presets/ambience/) | 4 | `00` `04` | `04` | 15 |
| [Spaces](presets/spaces/) | 5 | `00` `05` | `05` | 19 |
| [Halls 2](presets/halls-2/) | 6 | `00` `06` | `06` | 14 |
| [Plates 2](presets/plates-2/) | 7 | `00` `07` | `07` | 14 |
| [Rooms 2](presets/rooms-2/) | 8 | `00` `08` | `08` | 22 |
| [Spaces 2](presets/spaces-2/) | 9 | `00` `09` | `09` | 20 |
| [NonLin](presets/nonlin/) | 10 | `00` `0A` | `0A` | 4 |

## Captured presets

| Bank | Preset | Slot | Name bytes | Docs |
|------|--------|-----:|------------|------|
| [Halls](presets/halls/) | [Large Hall](presets/halls/large-hall.md) | 0 | ok | [open](presets/halls/large-hall.md) |
| [Halls](presets/halls/) | [Medium Hall](presets/halls/medium-hall.md) | 1 | ok | [open](presets/halls/medium-hall.md) |
| [Halls](presets/halls/) | [Small Hall](presets/halls/small-hall.md) | 2 | ok | [open](presets/halls/small-hall.md) |
| [Halls](presets/halls/) | [Large & Near](presets/halls/large-and-near.md) | 3 | ok | [open](presets/halls/large-and-near.md) |
| [Halls](presets/halls/) | [Medium & Near](presets/halls/medium-and-near.md) | 4 | ok | [open](presets/halls/medium-and-near.md) |
| [Halls](presets/halls/) | [Small & Near](presets/halls/small-and-near.md) | 5 | ok | [open](presets/halls/small-and-near.md) |
| [Halls](presets/halls/) | [Large & Dark](presets/halls/large-and-dark.md) | 6 | ok | [open](presets/halls/large-and-dark.md) |
| [Halls](presets/halls/) | [Large & Deep](presets/halls/large-and-deep.md) | 7 | ok | [open](presets/halls/large-and-deep.md) |
| [Halls](presets/halls/) | [Medium & Deep](presets/halls/medium-and-deep.md) | 8 | ok | [open](presets/halls/medium-and-deep.md) |
| [Halls](presets/halls/) | [Concert Hall](presets/halls/concert-hall.md) | 9 | ok | [open](presets/halls/concert-hall.md) |
| [Halls](presets/halls/) | [Gold Hall](presets/halls/gold-hall.md) | 10 | ok | [open](presets/halls/gold-hall.md) |
| [Halls](presets/halls/) | [Sandors Hall](presets/halls/sandors-hall.md) | 11 | ok | [open](presets/halls/sandors-hall.md) |
| [Halls](presets/halls/) | [Dense Hall](presets/halls/dense-hall.md) | 12 | ok | [open](presets/halls/dense-hall.md) |
| [Halls](presets/halls/) | [Clear Hall](presets/halls/clear-hall.md) | 13 | ok | [open](presets/halls/clear-hall.md) |
| [Halls](presets/halls/) | [Brass Hall](presets/halls/brass-hall.md) | 14 | ok | [open](presets/halls/brass-hall.md) |
| [Halls](presets/halls/) | [Amsterdam Hall](presets/halls/amsterdam-hall.md) | 15 | ok | [open](presets/halls/amsterdam-hall.md) |
| [Halls](presets/halls/) | [Berliner Hall](presets/halls/berliner-hall.md) | 16 | ok | [open](presets/halls/berliner-hall.md) |
| [Halls](presets/halls/) | [Boston Hall A](presets/halls/boston-hall-a.md) | 17 | ok | [open](presets/halls/boston-hall-a.md) |
| [Halls](presets/halls/) | [Boston Hall B](presets/halls/boston-hall-b.md) | 18 | ok | [open](presets/halls/boston-hall-b.md) |
| [Halls](presets/halls/) | [Chicago Hall](presets/halls/chicago-hall.md) | 19 | ok | [open](presets/halls/chicago-hall.md) |
| [Halls](presets/halls/) | [Vienna Hall](presets/halls/vienna-hall.md) | 20 | ok | [open](presets/halls/vienna-hall.md) |
| [Halls](presets/halls/) | [Worcester Hall](presets/halls/worcester-hall.md) | 21 | ok | [open](presets/halls/worcester-hall.md) |
| [Halls](presets/halls/) | [The ArchDuke](presets/halls/the-archduke.md) | 22 | ok | [open](presets/halls/the-archduke.md) |
| [Halls](presets/halls/) | [Troy Hall](presets/halls/troy-hall.md) | 23 | ok | [open](presets/halls/troy-hall.md) |
| [Halls](presets/halls/) | [Saint Sylvain](presets/halls/saint-sylvain.md) | 24 | ok | [open](presets/halls/saint-sylvain.md) |
| [Halls](presets/halls/) | [Mechanics Hall](presets/halls/mechanics-hall.md) | 25 | ok | [open](presets/halls/mechanics-hall.md) |
| [Halls](presets/halls/) | [Saint Gerold](presets/halls/saint-gerold.md) | 26 | ok | [open](presets/halls/saint-gerold.md) |
| [Halls](presets/halls/) | [Pepes Hall A](presets/halls/pepes-hall-a.md) | 27 | ok | [open](presets/halls/pepes-hall-a.md) |
| [Halls](presets/halls/) | [Pepes Hall B](presets/halls/pepes-hall-b.md) | 28 | ok | [open](presets/halls/pepes-hall-b.md) |
| [Halls](presets/halls/) | [Reflect Hall A](presets/halls/reflect-hall-a.md) | 29 | ok | [open](presets/halls/reflect-hall-a.md) |
| [Halls](presets/halls/) | [Reflect Hall B](presets/halls/reflect-hall-b.md) | 30 | ok | [open](presets/halls/reflect-hall-b.md) |
| [Halls](presets/halls/) | [Piano Hall](presets/halls/piano-hall.md) | 31 | ok | [open](presets/halls/piano-hall.md) |
| [Plates](presets/plates/) | [Bright Plate](presets/plates/bright-plate.md) | 0 | ok | [open](presets/plates/bright-plate.md) |
| [Plates](presets/plates/) | [Dark Plate](presets/plates/dark-plate.md) | 1 | ok | [open](presets/plates/dark-plate.md) |
| [Plates](presets/plates/) | [London Plate](presets/plates/london-plate.md) | 2 | ok | [open](presets/plates/london-plate.md) |
| [Plates](presets/plates/) | [Snare Plate A](presets/plates/snare-plate-a.md) | 3 | ok | [open](presets/plates/snare-plate-a.md) |
| [Plates](presets/plates/) | [Snare Plate B](presets/plates/snare-plate-b.md) | 4 | ok | [open](presets/plates/snare-plate-b.md) |
| [Plates](presets/plates/) | [Vocal Plate](presets/plates/vocal-plate.md) | 5 | ok | [open](presets/plates/vocal-plate.md) |
| [Plates](presets/plates/) | [Old Plate](presets/plates/old-plate.md) | 6 | ok | [open](presets/plates/old-plate.md) |
| [Plates](presets/plates/) | [Rich Plate](presets/plates/rich-plate.md) | 7 | ok | [open](presets/plates/rich-plate.md) |
| [Plates](presets/plates/) | [Gold Plate](presets/plates/gold-plate.md) | 8 | ok | [open](presets/plates/gold-plate.md) |
| [Plates](presets/plates/) | [Dense Plate](presets/plates/dense-plate.md) | 9 | ok | [open](presets/plates/dense-plate.md) |
| [Plates](presets/plates/) | [Silver Plate](presets/plates/silver-plate.md) | 10 | ok | [open](presets/plates/silver-plate.md) |
| [Plates](presets/plates/) | [Percussion](presets/plates/percussion.md) | 11 | ok | [open](presets/plates/percussion.md) |
| [Plates](presets/plates/) | [Echo Plate](presets/plates/echo-plate.md) | 12 | ok | [open](presets/plates/echo-plate.md) |
| [Plates](presets/plates/) | [CD Plate A](presets/plates/cd-plate-a.md) | 13 | ok | [open](presets/plates/cd-plate-a.md) |
| [Plates](presets/plates/) | [CD Plate B](presets/plates/cd-plate-b.md) | 14 | ok | [open](presets/plates/cd-plate-b.md) |
| [Plates](presets/plates/) | [Large Plate](presets/plates/large-plate.md) | 15 | ok | [open](presets/plates/large-plate.md) |
| [Plates](presets/plates/) | [Small Plate](presets/plates/small-plate.md) | 16 | ok | [open](presets/plates/small-plate.md) |
| [Plates](presets/plates/) | [Fat Plate](presets/plates/fat-plate.md) | 17 | ok | [open](presets/plates/fat-plate.md) |
| [Plates](presets/plates/) | [Crystal Plate](presets/plates/crystal-plate.md) | 18 | ok | [open](presets/plates/crystal-plate.md) |
| [Plates](presets/plates/) | [Sun Plate A](presets/plates/sun-plate-a.md) | 19 | ok | [open](presets/plates/sun-plate-a.md) |
| [Plates](presets/plates/) | [Sun Plate B](presets/plates/sun-plate-b.md) | 20 | ok | [open](presets/plates/sun-plate-b.md) |
| [Plates](presets/plates/) | [Sun Plate C](presets/plates/sun-plate-c.md) | 21 | ok | [open](presets/plates/sun-plate-c.md) |
| [Plates](presets/plates/) | [Vocal Plate B](presets/plates/vocal-plate-b.md) | 22 | ok | [open](presets/plates/vocal-plate-b.md) |
| [Plates](presets/plates/) | [Repro Plate](presets/plates/repro-plate.md) | 23 | ok | [open](presets/plates/repro-plate.md) |
| [Rooms](presets/rooms/) | [Studio A](presets/rooms/studio-a.md) | 0 | ok | [open](presets/rooms/studio-a.md) |
| [Rooms](presets/rooms/) | [Studio B Close](presets/rooms/studio-b-close.md) | 1 | ok | [open](presets/rooms/studio-b-close.md) |
| [Rooms](presets/rooms/) | [Studio B Far](presets/rooms/studio-b-far.md) | 2 | ok | [open](presets/rooms/studio-b-far.md) |
| [Rooms](presets/rooms/) | [Studio C](presets/rooms/studio-c.md) | 3 | ok | [open](presets/rooms/studio-c.md) |
| [Rooms](presets/rooms/) | [Studio D](presets/rooms/studio-d.md) | 4 | ok | [open](presets/rooms/studio-d.md) |
| [Rooms](presets/rooms/) | [Studio E](presets/rooms/studio-e.md) | 5 | ok | [open](presets/rooms/studio-e.md) |
| [Rooms](presets/rooms/) | [Deep Stone](presets/rooms/deep-stone.md) | 6 | ok | [open](presets/rooms/deep-stone.md) |
| [Rooms](presets/rooms/) | [Music Room](presets/rooms/music-room.md) | 7 | ok | [open](presets/rooms/music-room.md) |
| [Rooms](presets/rooms/) | [Heavy Room](presets/rooms/heavy-room.md) | 8 | ok | [open](presets/rooms/heavy-room.md) |
| [Rooms](presets/rooms/) | [Large Wooden](presets/rooms/large-wooden.md) | 9 | ok | [open](presets/rooms/large-wooden.md) |
| [Rooms](presets/rooms/) | [Small Wooden](presets/rooms/small-wooden.md) | 10 | ok | [open](presets/rooms/small-wooden.md) |
| [Rooms](presets/rooms/) | [Large Tiled](presets/rooms/large-tiled.md) | 11 | ok | [open](presets/rooms/large-tiled.md) |
| [Rooms](presets/rooms/) | [Medium Tiled](presets/rooms/medium-tiled.md) | 12 | ok | [open](presets/rooms/medium-tiled.md) |
| [Rooms](presets/rooms/) | [Small Tiled](presets/rooms/small-tiled.md) | 13 | ok | [open](presets/rooms/small-tiled.md) |
| [Rooms](presets/rooms/) | [Drum & Chamber](presets/rooms/drum-and-chamber.md) | 14 | ok | [open](presets/rooms/drum-and-chamber.md) |
| [Rooms](presets/rooms/) | [Djangos Room](presets/rooms/djangos-room.md) | 15 | ok | [open](presets/rooms/djangos-room.md) |
| [Rooms](presets/rooms/) | [Small Vox Room](presets/rooms/small-vox-room.md) | 16 | ok | [open](presets/rooms/small-vox-room.md) |
| [Rooms](presets/rooms/) | [Glass Room](presets/rooms/glass-room.md) | 17 | ok | [open](presets/rooms/glass-room.md) |
| [Rooms](presets/rooms/) | [Percussion](presets/rooms/percussion.md) | 18 | ok | [open](presets/rooms/percussion.md) |
| [Rooms](presets/rooms/) | [Marble Foyer](presets/rooms/marble-foyer.md) | 19 | ok | [open](presets/rooms/marble-foyer.md) |
| [Rooms](presets/rooms/) | [Large Q Room](presets/rooms/large-q-room.md) | 20 | ok | [open](presets/rooms/large-q-room.md) |
| [Rooms](presets/rooms/) | [Small Q Room](presets/rooms/small-q-room.md) | 21 | ok | [open](presets/rooms/small-q-room.md) |
| [Rooms](presets/rooms/) | [Large Red Room](presets/rooms/large-red-room.md) | 22 | ok | [open](presets/rooms/large-red-room.md) |
| [Rooms](presets/rooms/) | [Red Room](presets/rooms/red-room.md) | 23 | ok | [open](presets/rooms/red-room.md) |
| [Rooms](presets/rooms/) | [Blue Room](presets/rooms/blue-room.md) | 24 | ok | [open](presets/rooms/blue-room.md) |
| [Rooms](presets/rooms/) | [Large Room](presets/rooms/large-room.md) | 25 | ok | [open](presets/rooms/large-room.md) |
| [Rooms](presets/rooms/) | [Small Room](presets/rooms/small-room.md) | 26 | ok | [open](presets/rooms/small-room.md) |
| [Rooms](presets/rooms/) | [Front Room](presets/rooms/front-room.md) | 27 | ok | [open](presets/rooms/front-room.md) |
| [Rooms](presets/rooms/) | [Center Room](presets/rooms/center-room.md) | 28 | ok | [open](presets/rooms/center-room.md) |
| [Rooms](presets/rooms/) | [Back Room](presets/rooms/back-room.md) | 29 | ok | [open](presets/rooms/back-room.md) |
| [Rooms](presets/rooms/) | [Studio K](presets/rooms/studio-k.md) | 30 | ok | [open](presets/rooms/studio-k.md) |
| [Rooms](presets/rooms/) | [Waits Room](presets/rooms/waits-room.md) | 31 | ok | [open](presets/rooms/waits-room.md) |
| [Rooms](presets/rooms/) | [Corn Room](presets/rooms/corn-room.md) | 32 | ok | [open](presets/rooms/corn-room.md) |
| [Rooms](presets/rooms/) | [Oakland Room](presets/rooms/oakland-room.md) | 33 | ok | [open](presets/rooms/oakland-room.md) |
| [Rooms](presets/rooms/) | [SF Perf Room](presets/rooms/sf-perf-room.md) | 34 | ok | [open](presets/rooms/sf-perf-room.md) |
| [Rooms](presets/rooms/) | [Long Wood Room](presets/rooms/long-wood-room.md) | 35 | ok | [open](presets/rooms/long-wood-room.md) |
| [Chambers](presets/chambers/) | [Large Chamber](presets/chambers/large-chamber.md) | 0 | ok | [open](presets/chambers/large-chamber.md) |
| [Chambers](presets/chambers/) | [Medium Chamber](presets/chambers/medium-chamber.md) | 1 | ok | [open](presets/chambers/medium-chamber.md) |
| [Chambers](presets/chambers/) | [Small Chamber](presets/chambers/small-chamber.md) | 2 | ok | [open](presets/chambers/small-chamber.md) |
| [Chambers](presets/chambers/) | [Large & Dark](presets/chambers/large-and-dark.md) | 3 | ok | [open](presets/chambers/large-and-dark.md) |
| [Chambers](presets/chambers/) | [Small & Dark](presets/chambers/small-and-dark.md) | 4 | ok | [open](presets/chambers/small-and-dark.md) |
| [Chambers](presets/chambers/) | [Large & Bright](presets/chambers/large-and-bright.md) | 5 | ok | [open](presets/chambers/large-and-bright.md) |
| [Chambers](presets/chambers/) | [Small & Bright](presets/chambers/small-and-bright.md) | 6 | ok | [open](presets/chambers/small-and-bright.md) |
| [Chambers](presets/chambers/) | [Kick Chamber](presets/chambers/kick-chamber.md) | 7 | ok | [open](presets/chambers/kick-chamber.md) |
| [Chambers](presets/chambers/) | [Snare Chamber](presets/chambers/snare-chamber.md) | 8 | ok | [open](presets/chambers/snare-chamber.md) |
| [Chambers](presets/chambers/) | [Vocal Chamber](presets/chambers/vocal-chamber.md) | 9 | ok | [open](presets/chambers/vocal-chamber.md) |
| [Chambers](presets/chambers/) | [A&M Chamber](presets/chambers/a-and-m-chamber.md) | 10 | ok | [open](presets/chambers/a-and-m-chamber.md) |
| [Chambers](presets/chambers/) | [CD Chamber](presets/chambers/cd-chamber.md) | 11 | ok | [open](presets/chambers/cd-chamber.md) |
| [Chambers](presets/chambers/) | [Old Chamber](presets/chambers/old-chamber.md) | 12 | ok | [open](presets/chambers/old-chamber.md) |
| [Chambers](presets/chambers/) | [Deep Chamber](presets/chambers/deep-chamber.md) | 13 | ok | [open](presets/chambers/deep-chamber.md) |
| [Chambers](presets/chambers/) | [Amb Chamber A](presets/chambers/amb-chamber-a.md) | 14 | ok | [open](presets/chambers/amb-chamber-a.md) |
| [Chambers](presets/chambers/) | [Amb Chamber B](presets/chambers/amb-chamber-b.md) | 15 | ok | [open](presets/chambers/amb-chamber-b.md) |
| [Chambers](presets/chambers/) | [Sunset Chamber](presets/chambers/sunset-chamber.md) | 16 | ok | [open](presets/chambers/sunset-chamber.md) |
| [Chambers](presets/chambers/) | [A&M Chamber B](presets/chambers/a-and-m-chamber-b.md) | 17 | ok | [open](presets/chambers/a-and-m-chamber-b.md) |
| [Chambers](presets/chambers/) | [Stone Chamber](presets/chambers/stone-chamber.md) | 18 | ok | [open](presets/chambers/stone-chamber.md) |
| [Chambers](presets/chambers/) | [Tiled Chamber](presets/chambers/tiled-chamber.md) | 19 | ok | [open](presets/chambers/tiled-chamber.md) |
| [Chambers](presets/chambers/) | [Fat Chamber](presets/chambers/fat-chamber.md) | 20 | ok | [open](presets/chambers/fat-chamber.md) |
| [Chambers](presets/chambers/) | [Echo Chamber](presets/chambers/echo-chamber.md) | 21 | ok | [open](presets/chambers/echo-chamber.md) |
| [Ambience](presets/ambience/) | [Large Ambience](presets/ambience/large-ambience.md) | 0 | ok | [open](presets/ambience/large-ambience.md) |
| [Ambience](presets/ambience/) | [Med Ambience](presets/ambience/med-ambience.md) | 1 | ok | [open](presets/ambience/med-ambience.md) |
| [Ambience](presets/ambience/) | [Small Ambience](presets/ambience/small-ambience.md) | 2 | ok | [open](presets/ambience/small-ambience.md) |
| [Ambience](presets/ambience/) | [Large & Dark](presets/ambience/large-and-dark.md) | 3 | ok | [open](presets/ambience/large-and-dark.md) |
| [Ambience](presets/ambience/) | [Medium & Dark](presets/ambience/medium-and-dark.md) | 4 | ok | [open](presets/ambience/medium-and-dark.md) |
| [Ambience](presets/ambience/) | [Small & Dark](presets/ambience/small-and-dark.md) | 5 | ok | [open](presets/ambience/small-and-dark.md) |
| [Ambience](presets/ambience/) | [Large & Bright](presets/ambience/large-and-bright.md) | 6 | ok | [open](presets/ambience/large-and-bright.md) |
| [Ambience](presets/ambience/) | [Med & Bright](presets/ambience/med-and-bright.md) | 7 | ok | [open](presets/ambience/med-and-bright.md) |
| [Ambience](presets/ambience/) | [Small & Bright](presets/ambience/small-and-bright.md) | 8 | ok | [open](presets/ambience/small-and-bright.md) |
| [Ambience](presets/ambience/) | [Deep Ambience](presets/ambience/deep-ambience.md) | 9 | ok | [open](presets/ambience/deep-ambience.md) |
| [Ambience](presets/ambience/) | [Long Ambience](presets/ambience/long-ambience.md) | 10 | ok | [open](presets/ambience/long-ambience.md) |
| [Ambience](presets/ambience/) | [Clear Ambience](presets/ambience/clear-ambience.md) | 11 | ok | [open](presets/ambience/clear-ambience.md) |
| [Ambience](presets/ambience/) | [Heavy Ambience](presets/ambience/heavy-ambience.md) | 12 | ok | [open](presets/ambience/heavy-ambience.md) |
| [Ambience](presets/ambience/) | [Bass  XXL](presets/ambience/bass-xxl.md) | 13 | ok | [open](presets/ambience/bass-xxl.md) |
| [Ambience](presets/ambience/) | [Percussion Air](presets/ambience/percussion-air.md) | 14 | ok | [open](presets/ambience/percussion-air.md) |
| [Spaces](presets/spaces/) | [North Church](presets/spaces/north-church.md) | 0 | ok | [open](presets/spaces/north-church.md) |
| [Spaces](presets/spaces/) | [East Church](presets/spaces/east-church.md) | 1 | ok | [open](presets/spaces/east-church.md) |
| [Spaces](presets/spaces/) | [South Church](presets/spaces/south-church.md) | 2 | ok | [open](presets/spaces/south-church.md) |
| [Spaces](presets/spaces/) | [West Church](presets/spaces/west-church.md) | 3 | ok | [open](presets/spaces/west-church.md) |
| [Spaces](presets/spaces/) | [Cinema Room](presets/spaces/cinema-room.md) | 4 | ok | [open](presets/spaces/cinema-room.md) |
| [Spaces](presets/spaces/) | [Scoring Stage](presets/spaces/scoring-stage.md) | 5 | ok | [open](presets/spaces/scoring-stage.md) |
| [Spaces](presets/spaces/) | [Bath House](presets/spaces/bath-house.md) | 6 | ok | [open](presets/spaces/bath-house.md) |
| [Spaces](presets/spaces/) | [Car Park](presets/spaces/car-park.md) | 7 | ok | [open](presets/spaces/car-park.md) |
| [Spaces](presets/spaces/) | [Arena](presets/spaces/arena.md) | 8 | ok | [open](presets/spaces/arena.md) |
| [Spaces](presets/spaces/) | [Redwood Valley](presets/spaces/redwood-valley.md) | 9 | ok | [open](presets/spaces/redwood-valley.md) |
| [Spaces](presets/spaces/) | [Tanglewood](presets/spaces/tanglewood.md) | 10 | ok | [open](presets/spaces/tanglewood.md) |
| [Spaces](presets/spaces/) | [Academy Yard](presets/spaces/academy-yard.md) | 11 | ok | [open](presets/spaces/academy-yard.md) |
| [Spaces](presets/spaces/) | [Hillside](presets/spaces/hillside.md) | 12 | ok | [open](presets/spaces/hillside.md) |
| [Spaces](presets/spaces/) | [Cavern](presets/spaces/cavern.md) | 13 | ok | [open](presets/spaces/cavern.md) |
| [Spaces](presets/spaces/) | [Stone Quarry](presets/spaces/stone-quarry.md) | 14 | ok | [open](presets/spaces/stone-quarry.md) |
| [Spaces](presets/spaces/) | [Europa](presets/spaces/europa.md) | 15 | ok | [open](presets/spaces/europa.md) |
| [Spaces](presets/spaces/) | [Gated Space](presets/spaces/gated-space.md) | 16 | ok | [open](presets/spaces/gated-space.md) |
| [Spaces](presets/spaces/) | [Reflect Chapel](presets/spaces/reflect-chapel.md) | 17 | ok | [open](presets/spaces/reflect-chapel.md) |
| [Spaces](presets/spaces/) | [Reflect Church](presets/spaces/reflect-church.md) | 18 | ok | [open](presets/spaces/reflect-church.md) |
| [Halls 2](presets/halls-2/) | [Large Hall](presets/halls-2/large-hall.md) | 0 | ok | [open](presets/halls-2/large-hall.md) |
| [Halls 2](presets/halls-2/) | [Large & Stage](presets/halls-2/large-and-stage.md) | 1 | ok | [open](presets/halls-2/large-and-stage.md) |
| [Halls 2](presets/halls-2/) | [Medium Hall](presets/halls-2/medium-hall.md) | 2 | ok | [open](presets/halls-2/medium-hall.md) |
| [Halls 2](presets/halls-2/) | [Med & Stage](presets/halls-2/med-and-stage.md) | 3 | ok | [open](presets/halls-2/med-and-stage.md) |
| [Halls 2](presets/halls-2/) | [Small Hall](presets/halls-2/small-hall.md) | 4 | ok | [open](presets/halls-2/small-hall.md) |
| [Halls 2](presets/halls-2/) | [Small & Stage](presets/halls-2/small-and-stage.md) | 5 | ok | [open](presets/halls-2/small-and-stage.md) |
| [Halls 2](presets/halls-2/) | [Large Church](presets/halls-2/large-church.md) | 6 | ok | [open](presets/halls-2/large-church.md) |
| [Halls 2](presets/halls-2/) | [Small Church](presets/halls-2/small-church.md) | 7 | ok | [open](presets/halls-2/small-church.md) |
| [Halls 2](presets/halls-2/) | [Jazz Hall](presets/halls-2/jazz-hall.md) | 8 | ok | [open](presets/halls-2/jazz-hall.md) |
| [Halls 2](presets/halls-2/) | [West Hall](presets/halls-2/west-hall.md) | 9 | ok | [open](presets/halls-2/west-hall.md) |
| [Halls 2](presets/halls-2/) | [Concert A](presets/halls-2/concert-a.md) | 10 | ok | [open](presets/halls-2/concert-a.md) |
| [Halls 2](presets/halls-2/) | [Concert B](presets/halls-2/concert-b.md) | 11 | ok | [open](presets/halls-2/concert-b.md) |
| [Halls 2](presets/halls-2/) | [Live Hall](presets/halls-2/live-hall.md) | 12 | ok | [open](presets/halls-2/live-hall.md) |
| [Halls 2](presets/halls-2/) | [Koncert Piano](presets/halls-2/koncert-piano.md) | 13 | ok | [open](presets/halls-2/koncert-piano.md) |
| [Plates 2](presets/plates-2/) | [Plate A](presets/plates-2/plate-a.md) | 0 | ok | [open](presets/plates-2/plate-a.md) |
| [Plates 2](presets/plates-2/) | [Small Plate](presets/plates-2/small-plate.md) | 1 | ok | [open](presets/plates-2/small-plate.md) |
| [Plates 2](presets/plates-2/) | [Snare Plate](presets/plates-2/snare-plate.md) | 2 | ok | [open](presets/plates-2/snare-plate.md) |
| [Plates 2](presets/plates-2/) | [Dark Plate](presets/plates-2/dark-plate.md) | 3 | ok | [open](presets/plates-2/dark-plate.md) |
| [Plates 2](presets/plates-2/) | [Rich Plate A](presets/plates-2/rich-plate-a.md) | 4 | ok | [open](presets/plates-2/rich-plate-a.md) |
| [Plates 2](presets/plates-2/) | [Rich Plate B](presets/plates-2/rich-plate-b.md) | 5 | ok | [open](presets/plates-2/rich-plate-b.md) |
| [Plates 2](presets/plates-2/) | [Thin Plate](presets/plates-2/thin-plate.md) | 6 | ok | [open](presets/plates-2/thin-plate.md) |
| [Plates 2](presets/plates-2/) | [Vocal Plate A](presets/plates-2/vocal-plate-a.md) | 7 | ok | [open](presets/plates-2/vocal-plate-a.md) |
| [Plates 2](presets/plates-2/) | [Vocal Plate B](presets/plates-2/vocal-plate-b.md) | 8 | ok | [open](presets/plates-2/vocal-plate-b.md) |
| [Plates 2](presets/plates-2/) | [Drum Plate](presets/plates-2/drum-plate.md) | 9 | ok | [open](presets/plates-2/drum-plate.md) |
| [Plates 2](presets/plates-2/) | [Large Plate](presets/plates-2/large-plate.md) | 10 | ok | [open](presets/plates-2/large-plate.md) |
| [Plates 2](presets/plates-2/) | [Fat Plate](presets/plates-2/fat-plate.md) | 11 | ok | [open](presets/plates-2/fat-plate.md) |
| [Plates 2](presets/plates-2/) | [Alpha Plate](presets/plates-2/alpha-plate.md) | 12 | ok | [open](presets/plates-2/alpha-plate.md) |
| [Plates 2](presets/plates-2/) | [Vocal Shimmer](presets/plates-2/vocal-shimmer.md) | 13 | ok | [open](presets/plates-2/vocal-shimmer.md) |
| [Rooms 2](presets/rooms-2/) | [Music Club](presets/rooms-2/music-club.md) | 0 | ok | [open](presets/rooms-2/music-club.md) |
| [Rooms 2](presets/rooms-2/) | [Large Room](presets/rooms-2/large-room.md) | 1 | ok | [open](presets/rooms-2/large-room.md) |
| [Rooms 2](presets/rooms-2/) | [Med Room](presets/rooms-2/med-room.md) | 2 | ok | [open](presets/rooms-2/med-room.md) |
| [Rooms 2](presets/rooms-2/) | [Small Room](presets/rooms-2/small-room.md) | 3 | ok | [open](presets/rooms-2/small-room.md) |
| [Rooms 2](presets/rooms-2/) | [Lg Wood Room](presets/rooms-2/lg-wood-room.md) | 4 | ok | [open](presets/rooms-2/lg-wood-room.md) |
| [Rooms 2](presets/rooms-2/) | [Sm Wood Room](presets/rooms-2/sm-wood-room.md) | 5 | ok | [open](presets/rooms-2/sm-wood-room.md) |
| [Rooms 2](presets/rooms-2/) | [Large Chamber](presets/rooms-2/large-chamber.md) | 6 | ok | [open](presets/rooms-2/large-chamber.md) |
| [Rooms 2](presets/rooms-2/) | [Small Chamber](presets/rooms-2/small-chamber.md) | 7 | ok | [open](presets/rooms-2/small-chamber.md) |
| [Rooms 2](presets/rooms-2/) | [Bright Chamber](presets/rooms-2/bright-chamber.md) | 8 | ok | [open](presets/rooms-2/bright-chamber.md) |
| [Rooms 2](presets/rooms-2/) | [Tiled Room](presets/rooms-2/tiled-room.md) | 9 | ok | [open](presets/rooms-2/tiled-room.md) |
| [Rooms 2](presets/rooms-2/) | [Fat Chamber](presets/rooms-2/fat-chamber.md) | 10 | ok | [open](presets/rooms-2/fat-chamber.md) |
| [Rooms 2](presets/rooms-2/) | [Studio 1](presets/rooms-2/studio-1.md) | 11 | ok | [open](presets/rooms-2/studio-1.md) |
| [Rooms 2](presets/rooms-2/) | [Studio 2](presets/rooms-2/studio-2.md) | 12 | ok | [open](presets/rooms-2/studio-2.md) |
| [Rooms 2](presets/rooms-2/) | [Studio 3](presets/rooms-2/studio-3.md) | 13 | ok | [open](presets/rooms-2/studio-3.md) |
| [Rooms 2](presets/rooms-2/) | [Studio 4](presets/rooms-2/studio-4.md) | 14 | ok | [open](presets/rooms-2/studio-4.md) |
| [Rooms 2](presets/rooms-2/) | [Guitar Room](presets/rooms-2/guitar-room.md) | 15 | ok | [open](presets/rooms-2/guitar-room.md) |
| [Rooms 2](presets/rooms-2/) | [Marble Room](presets/rooms-2/marble-room.md) | 16 | ok | [open](presets/rooms-2/marble-room.md) |
| [Rooms 2](presets/rooms-2/) | [Deep Chamber](presets/rooms-2/deep-chamber.md) | 17 | ok | [open](presets/rooms-2/deep-chamber.md) |
| [Rooms 2](presets/rooms-2/) | [Dark Chamber](presets/rooms-2/dark-chamber.md) | 18 | ok | [open](presets/rooms-2/dark-chamber.md) |
| [Rooms 2](presets/rooms-2/) | [Vocal Chamber](presets/rooms-2/vocal-chamber.md) | 19 | ok | [open](presets/rooms-2/vocal-chamber.md) |
| [Rooms 2](presets/rooms-2/) | [Wide Room](presets/rooms-2/wide-room.md) | 20 | ok | [open](presets/rooms-2/wide-room.md) |
| [Rooms 2](presets/rooms-2/) | [Lush Room](presets/rooms-2/lush-room.md) | 21 | ok | [open](presets/rooms-2/lush-room.md) |
| [Spaces 2](presets/spaces-2/) | [Open Space](presets/spaces-2/open-space.md) | 0 | ok | [open](presets/spaces-2/open-space.md) |
| [Spaces 2](presets/spaces-2/) | [Med Space](presets/spaces-2/med-space.md) | 1 | ok | [open](presets/spaces-2/med-space.md) |
| [Spaces 2](presets/spaces-2/) | [Small Space](presets/spaces-2/small-space.md) | 2 | ok | [open](presets/spaces-2/small-space.md) |
| [Spaces 2](presets/spaces-2/) | [Vox Ambience](presets/spaces-2/vox-ambience.md) | 3 | ok | [open](presets/spaces-2/vox-ambience.md) |
| [Spaces 2](presets/spaces-2/) | [Big Bottom](presets/spaces-2/big-bottom.md) | 4 | ok | [open](presets/spaces-2/big-bottom.md) |
| [Spaces 2](presets/spaces-2/) | [Cathedral](presets/spaces-2/cathedral.md) | 5 | ok | [open](presets/spaces-2/cathedral.md) |
| [Spaces 2](presets/spaces-2/) | [Grand Stage](presets/spaces-2/grand-stage.md) | 6 | ok | [open](presets/spaces-2/grand-stage.md) |
| [Spaces 2](presets/spaces-2/) | [Lush Church](presets/spaces-2/lush-church.md) | 7 | ok | [open](presets/spaces-2/lush-church.md) |
| [Spaces 2](presets/spaces-2/) | [Grand Church](presets/spaces-2/grand-church.md) | 8 | ok | [open](presets/spaces-2/grand-church.md) |
| [Spaces 2](presets/spaces-2/) | [Concert Wave](presets/spaces-2/concert-wave.md) | 9 | ok | [open](presets/spaces-2/concert-wave.md) |
| [Spaces 2](presets/spaces-2/) | [Long Vox Space](presets/spaces-2/long-vox-space.md) | 10 | ok | [open](presets/spaces-2/long-vox-space.md) |
| [Spaces 2](presets/spaces-2/) | [Dark Warm Room](presets/spaces-2/dark-warm-room.md) | 11 | ok | [open](presets/spaces-2/dark-warm-room.md) |
| [Spaces 2](presets/spaces-2/) | [Live Room](presets/spaces-2/live-room.md) | 12 | ok | [open](presets/spaces-2/live-room.md) |
| [Spaces 2](presets/spaces-2/) | [Shimmering Sky](presets/spaces-2/shimmering-sky.md) | 13 | ok | [open](presets/spaces-2/shimmering-sky.md) |
| [Spaces 2](presets/spaces-2/) | [Oak Ballroom](presets/spaces-2/oak-ballroom.md) | 14 | ok | [open](presets/spaces-2/oak-ballroom.md) |
| [Spaces 2](presets/spaces-2/) | [Ice House](presets/spaces-2/ice-house.md) | 15 | ok | [open](presets/spaces-2/ice-house.md) |
| [Spaces 2](presets/spaces-2/) | [Ice Beads](presets/spaces-2/ice-beads.md) | 16 | ok | [open](presets/spaces-2/ice-beads.md) |
| [Spaces 2](presets/spaces-2/) | [Music Forest](presets/spaces-2/music-forest.md) | 17 | ok | [open](presets/spaces-2/music-forest.md) |
| [Spaces 2](presets/spaces-2/) | [Waving Bloom](presets/spaces-2/waving-bloom.md) | 18 | ok | [open](presets/spaces-2/waving-bloom.md) |
| [Spaces 2](presets/spaces-2/) | [Brick Chamber](presets/spaces-2/brick-chamber.md) | 19 | ok | [open](presets/spaces-2/brick-chamber.md) |
| [NonLin](presets/nonlin/) | [NonLin A](presets/nonlin/nonlin-a.md) | 0 | ok | [open](presets/nonlin/nonlin-a.md) |
| [NonLin](presets/nonlin/) | [NonLin B](presets/nonlin/nonlin-b.md) | 1 | ok | [open](presets/nonlin/nonlin-b.md) |
| [NonLin](presets/nonlin/) | [NonLin C](presets/nonlin/nonlin-c.md) | 2 | ok | [open](presets/nonlin/nonlin-c.md) |
| [NonLin](presets/nonlin/) | [NonLin D](presets/nonlin/nonlin-d.md) | 3 | ok | [open](presets/nonlin/nonlin-d.md) |

## Program slots by bank

### [Ambience](presets/ambience/)

| Slot | Preset |
|-----:|--------|
| 0 | [Large Ambience](presets/ambience/large-ambience.md) |
| 1 | [Med Ambience](presets/ambience/med-ambience.md) |
| 2 | [Small Ambience](presets/ambience/small-ambience.md) |
| 3 | [Large & Dark](presets/ambience/large-and-dark.md) |
| 4 | [Medium & Dark](presets/ambience/medium-and-dark.md) |
| 5 | [Small & Dark](presets/ambience/small-and-dark.md) |
| 6 | [Large & Bright](presets/ambience/large-and-bright.md) |
| 7 | [Med & Bright](presets/ambience/med-and-bright.md) |
| 8 | [Small & Bright](presets/ambience/small-and-bright.md) |
| 9 | [Deep Ambience](presets/ambience/deep-ambience.md) |
| 10 | [Long Ambience](presets/ambience/long-ambience.md) |
| 11 | [Clear Ambience](presets/ambience/clear-ambience.md) |
| 12 | [Heavy Ambience](presets/ambience/heavy-ambience.md) |
| 13 | [Bass  XXL](presets/ambience/bass-xxl.md) |
| 14 | [Percussion Air](presets/ambience/percussion-air.md) |

### [Chambers](presets/chambers/)

| Slot | Preset |
|-----:|--------|
| 0 | [Large Chamber](presets/chambers/large-chamber.md) |
| 1 | [Medium Chamber](presets/chambers/medium-chamber.md) |
| 2 | [Small Chamber](presets/chambers/small-chamber.md) |
| 3 | [Large & Dark](presets/chambers/large-and-dark.md) |
| 4 | [Small & Dark](presets/chambers/small-and-dark.md) |
| 5 | [Large & Bright](presets/chambers/large-and-bright.md) |
| 6 | [Small & Bright](presets/chambers/small-and-bright.md) |
| 7 | [Kick Chamber](presets/chambers/kick-chamber.md) |
| 8 | [Snare Chamber](presets/chambers/snare-chamber.md) |
| 9 | [Vocal Chamber](presets/chambers/vocal-chamber.md) |
| 10 | [A&M Chamber](presets/chambers/a-and-m-chamber.md) |
| 11 | [CD Chamber](presets/chambers/cd-chamber.md) |
| 12 | [Old Chamber](presets/chambers/old-chamber.md) |
| 13 | [Deep Chamber](presets/chambers/deep-chamber.md) |
| 14 | [Amb Chamber A](presets/chambers/amb-chamber-a.md) |
| 15 | [Amb Chamber B](presets/chambers/amb-chamber-b.md) |
| 16 | [Sunset Chamber](presets/chambers/sunset-chamber.md) |
| 17 | [A&M Chamber B](presets/chambers/a-and-m-chamber-b.md) |
| 18 | [Stone Chamber](presets/chambers/stone-chamber.md) |
| 19 | [Tiled Chamber](presets/chambers/tiled-chamber.md) |
| 20 | [Fat Chamber](presets/chambers/fat-chamber.md) |
| 21 | [Echo Chamber](presets/chambers/echo-chamber.md) |

### [Halls](presets/halls/)

| Slot | Preset |
|-----:|--------|
| 0 | [Large Hall](presets/halls/large-hall.md) |
| 1 | [Medium Hall](presets/halls/medium-hall.md) |
| 2 | [Small Hall](presets/halls/small-hall.md) |
| 3 | [Large & Near](presets/halls/large-and-near.md) |
| 4 | [Medium & Near](presets/halls/medium-and-near.md) |
| 5 | [Small & Near](presets/halls/small-and-near.md) |
| 6 | [Large & Dark](presets/halls/large-and-dark.md) |
| 7 | [Large & Deep](presets/halls/large-and-deep.md) |
| 8 | [Medium & Deep](presets/halls/medium-and-deep.md) |
| 9 | [Concert Hall](presets/halls/concert-hall.md) |
| 10 | [Gold Hall](presets/halls/gold-hall.md) |
| 11 | [Sandors Hall](presets/halls/sandors-hall.md) |
| 12 | [Dense Hall](presets/halls/dense-hall.md) |
| 13 | [Clear Hall](presets/halls/clear-hall.md) |
| 14 | [Brass Hall](presets/halls/brass-hall.md) |
| 15 | [Amsterdam Hall](presets/halls/amsterdam-hall.md) |
| 16 | [Berliner Hall](presets/halls/berliner-hall.md) |
| 17 | [Boston Hall A](presets/halls/boston-hall-a.md) |
| 18 | [Boston Hall B](presets/halls/boston-hall-b.md) |
| 19 | [Chicago Hall](presets/halls/chicago-hall.md) |
| 20 | [Vienna Hall](presets/halls/vienna-hall.md) |
| 21 | [Worcester Hall](presets/halls/worcester-hall.md) |
| 22 | [The ArchDuke](presets/halls/the-archduke.md) |
| 23 | [Troy Hall](presets/halls/troy-hall.md) |
| 24 | [Saint Sylvain](presets/halls/saint-sylvain.md) |
| 25 | [Mechanics Hall](presets/halls/mechanics-hall.md) |
| 26 | [Saint Gerold](presets/halls/saint-gerold.md) |
| 27 | [Pepes Hall A](presets/halls/pepes-hall-a.md) |
| 28 | [Pepes Hall B](presets/halls/pepes-hall-b.md) |
| 29 | [Reflect Hall A](presets/halls/reflect-hall-a.md) |
| 30 | [Reflect Hall B](presets/halls/reflect-hall-b.md) |
| 31 | [Piano Hall](presets/halls/piano-hall.md) |

### [Halls 2](presets/halls-2/)

| Slot | Preset |
|-----:|--------|
| 0 | [Large Hall](presets/halls-2/large-hall.md) |
| 1 | [Large & Stage](presets/halls-2/large-and-stage.md) |
| 2 | [Medium Hall](presets/halls-2/medium-hall.md) |
| 3 | [Med & Stage](presets/halls-2/med-and-stage.md) |
| 4 | [Small Hall](presets/halls-2/small-hall.md) |
| 5 | [Small & Stage](presets/halls-2/small-and-stage.md) |
| 6 | [Large Church](presets/halls-2/large-church.md) |
| 7 | [Small Church](presets/halls-2/small-church.md) |
| 8 | [Jazz Hall](presets/halls-2/jazz-hall.md) |
| 9 | [West Hall](presets/halls-2/west-hall.md) |
| 10 | [Concert A](presets/halls-2/concert-a.md) |
| 11 | [Concert B](presets/halls-2/concert-b.md) |
| 12 | [Live Hall](presets/halls-2/live-hall.md) |
| 13 | [Koncert Piano](presets/halls-2/koncert-piano.md) |

### [NonLin](presets/nonlin/)

| Slot | Preset |
|-----:|--------|
| 0 | [NonLin A](presets/nonlin/nonlin-a.md) |
| 1 | [NonLin B](presets/nonlin/nonlin-b.md) |
| 2 | [NonLin C](presets/nonlin/nonlin-c.md) |
| 3 | [NonLin D](presets/nonlin/nonlin-d.md) |

### [Plates](presets/plates/)

| Slot | Preset |
|-----:|--------|
| 0 | [Bright Plate](presets/plates/bright-plate.md) |
| 1 | [Dark Plate](presets/plates/dark-plate.md) |
| 2 | [London Plate](presets/plates/london-plate.md) |
| 3 | [Snare Plate A](presets/plates/snare-plate-a.md) |
| 4 | [Snare Plate B](presets/plates/snare-plate-b.md) |
| 5 | [Vocal Plate](presets/plates/vocal-plate.md) |
| 6 | [Old Plate](presets/plates/old-plate.md) |
| 7 | [Rich Plate](presets/plates/rich-plate.md) |
| 8 | [Gold Plate](presets/plates/gold-plate.md) |
| 9 | [Dense Plate](presets/plates/dense-plate.md) |
| 10 | [Silver Plate](presets/plates/silver-plate.md) |
| 11 | [Percussion](presets/plates/percussion.md) |
| 12 | [Echo Plate](presets/plates/echo-plate.md) |
| 13 | [CD Plate A](presets/plates/cd-plate-a.md) |
| 14 | [CD Plate B](presets/plates/cd-plate-b.md) |
| 15 | [Large Plate](presets/plates/large-plate.md) |
| 16 | [Small Plate](presets/plates/small-plate.md) |
| 17 | [Fat Plate](presets/plates/fat-plate.md) |
| 18 | [Crystal Plate](presets/plates/crystal-plate.md) |
| 19 | [Sun Plate A](presets/plates/sun-plate-a.md) |
| 20 | [Sun Plate B](presets/plates/sun-plate-b.md) |
| 21 | [Sun Plate C](presets/plates/sun-plate-c.md) |
| 22 | [Vocal Plate B](presets/plates/vocal-plate-b.md) |
| 23 | [Repro Plate](presets/plates/repro-plate.md) |

### [Plates 2](presets/plates-2/)

| Slot | Preset |
|-----:|--------|
| 0 | [Plate A](presets/plates-2/plate-a.md) |
| 1 | [Small Plate](presets/plates-2/small-plate.md) |
| 2 | [Snare Plate](presets/plates-2/snare-plate.md) |
| 3 | [Dark Plate](presets/plates-2/dark-plate.md) |
| 4 | [Rich Plate A](presets/plates-2/rich-plate-a.md) |
| 5 | [Rich Plate B](presets/plates-2/rich-plate-b.md) |
| 6 | [Thin Plate](presets/plates-2/thin-plate.md) |
| 7 | [Vocal Plate A](presets/plates-2/vocal-plate-a.md) |
| 8 | [Vocal Plate B](presets/plates-2/vocal-plate-b.md) |
| 9 | [Drum Plate](presets/plates-2/drum-plate.md) |
| 10 | [Large Plate](presets/plates-2/large-plate.md) |
| 11 | [Fat Plate](presets/plates-2/fat-plate.md) |
| 12 | [Alpha Plate](presets/plates-2/alpha-plate.md) |
| 13 | [Vocal Shimmer](presets/plates-2/vocal-shimmer.md) |

### [Rooms](presets/rooms/)

| Slot | Preset |
|-----:|--------|
| 0 | [Studio A](presets/rooms/studio-a.md) |
| 1 | [Studio B Close](presets/rooms/studio-b-close.md) |
| 2 | [Studio B Far](presets/rooms/studio-b-far.md) |
| 3 | [Studio C](presets/rooms/studio-c.md) |
| 4 | [Studio D](presets/rooms/studio-d.md) |
| 5 | [Studio E](presets/rooms/studio-e.md) |
| 6 | [Deep Stone](presets/rooms/deep-stone.md) |
| 7 | [Music Room](presets/rooms/music-room.md) |
| 8 | [Heavy Room](presets/rooms/heavy-room.md) |
| 9 | [Large Wooden](presets/rooms/large-wooden.md) |
| 10 | [Small Wooden](presets/rooms/small-wooden.md) |
| 11 | [Large Tiled](presets/rooms/large-tiled.md) |
| 12 | [Medium Tiled](presets/rooms/medium-tiled.md) |
| 13 | [Small Tiled](presets/rooms/small-tiled.md) |
| 14 | [Drum & Chamber](presets/rooms/drum-and-chamber.md) |
| 15 | [Djangos Room](presets/rooms/djangos-room.md) |
| 16 | [Small Vox Room](presets/rooms/small-vox-room.md) |
| 17 | [Glass Room](presets/rooms/glass-room.md) |
| 18 | [Percussion](presets/rooms/percussion.md) |
| 19 | [Marble Foyer](presets/rooms/marble-foyer.md) |
| 20 | [Large Q Room](presets/rooms/large-q-room.md) |
| 21 | [Small Q Room](presets/rooms/small-q-room.md) |
| 22 | [Large Red Room](presets/rooms/large-red-room.md) |
| 23 | [Red Room](presets/rooms/red-room.md) |
| 24 | [Blue Room](presets/rooms/blue-room.md) |
| 25 | [Large Room](presets/rooms/large-room.md) |
| 26 | [Small Room](presets/rooms/small-room.md) |
| 27 | [Front Room](presets/rooms/front-room.md) |
| 28 | [Center Room](presets/rooms/center-room.md) |
| 29 | [Back Room](presets/rooms/back-room.md) |
| 30 | [Studio K](presets/rooms/studio-k.md) |
| 31 | [Waits Room](presets/rooms/waits-room.md) |
| 32 | [Corn Room](presets/rooms/corn-room.md) |
| 33 | [Oakland Room](presets/rooms/oakland-room.md) |
| 34 | [SF Perf Room](presets/rooms/sf-perf-room.md) |
| 35 | [Long Wood Room](presets/rooms/long-wood-room.md) |

### [Rooms 2](presets/rooms-2/)

| Slot | Preset |
|-----:|--------|
| 0 | [Music Club](presets/rooms-2/music-club.md) |
| 1 | [Large Room](presets/rooms-2/large-room.md) |
| 2 | [Med Room](presets/rooms-2/med-room.md) |
| 3 | [Small Room](presets/rooms-2/small-room.md) |
| 4 | [Lg Wood Room](presets/rooms-2/lg-wood-room.md) |
| 5 | [Sm Wood Room](presets/rooms-2/sm-wood-room.md) |
| 6 | [Large Chamber](presets/rooms-2/large-chamber.md) |
| 7 | [Small Chamber](presets/rooms-2/small-chamber.md) |
| 8 | [Bright Chamber](presets/rooms-2/bright-chamber.md) |
| 9 | [Tiled Room](presets/rooms-2/tiled-room.md) |
| 10 | [Fat Chamber](presets/rooms-2/fat-chamber.md) |
| 11 | [Studio 1](presets/rooms-2/studio-1.md) |
| 12 | [Studio 2](presets/rooms-2/studio-2.md) |
| 13 | [Studio 3](presets/rooms-2/studio-3.md) |
| 14 | [Studio 4](presets/rooms-2/studio-4.md) |
| 15 | [Guitar Room](presets/rooms-2/guitar-room.md) |
| 16 | [Marble Room](presets/rooms-2/marble-room.md) |
| 17 | [Deep Chamber](presets/rooms-2/deep-chamber.md) |
| 18 | [Dark Chamber](presets/rooms-2/dark-chamber.md) |
| 19 | [Vocal Chamber](presets/rooms-2/vocal-chamber.md) |
| 20 | [Wide Room](presets/rooms-2/wide-room.md) |
| 21 | [Lush Room](presets/rooms-2/lush-room.md) |

### [Spaces](presets/spaces/)

| Slot | Preset |
|-----:|--------|
| 0 | [North Church](presets/spaces/north-church.md) |
| 1 | [East Church](presets/spaces/east-church.md) |
| 2 | [South Church](presets/spaces/south-church.md) |
| 3 | [West Church](presets/spaces/west-church.md) |
| 4 | [Cinema Room](presets/spaces/cinema-room.md) |
| 5 | [Scoring Stage](presets/spaces/scoring-stage.md) |
| 6 | [Bath House](presets/spaces/bath-house.md) |
| 7 | [Car Park](presets/spaces/car-park.md) |
| 8 | [Arena](presets/spaces/arena.md) |
| 9 | [Redwood Valley](presets/spaces/redwood-valley.md) |
| 10 | [Tanglewood](presets/spaces/tanglewood.md) |
| 11 | [Academy Yard](presets/spaces/academy-yard.md) |
| 12 | [Hillside](presets/spaces/hillside.md) |
| 13 | [Cavern](presets/spaces/cavern.md) |
| 14 | [Stone Quarry](presets/spaces/stone-quarry.md) |
| 15 | [Europa](presets/spaces/europa.md) |
| 16 | [Gated Space](presets/spaces/gated-space.md) |
| 17 | [Reflect Chapel](presets/spaces/reflect-chapel.md) |
| 18 | [Reflect Church](presets/spaces/reflect-church.md) |

### [Spaces 2](presets/spaces-2/)

| Slot | Preset |
|-----:|--------|
| 0 | [Open Space](presets/spaces-2/open-space.md) |
| 1 | [Med Space](presets/spaces-2/med-space.md) |
| 2 | [Small Space](presets/spaces-2/small-space.md) |
| 3 | [Vox Ambience](presets/spaces-2/vox-ambience.md) |
| 4 | [Big Bottom](presets/spaces-2/big-bottom.md) |
| 5 | [Cathedral](presets/spaces-2/cathedral.md) |
| 6 | [Grand Stage](presets/spaces-2/grand-stage.md) |
| 7 | [Lush Church](presets/spaces-2/lush-church.md) |
| 8 | [Grand Church](presets/spaces-2/grand-church.md) |
| 9 | [Concert Wave](presets/spaces-2/concert-wave.md) |
| 10 | [Long Vox Space](presets/spaces-2/long-vox-space.md) |
| 11 | [Dark Warm Room](presets/spaces-2/dark-warm-room.md) |
| 12 | [Live Room](presets/spaces-2/live-room.md) |
| 13 | [Shimmering Sky](presets/spaces-2/shimmering-sky.md) |
| 14 | [Oak Ballroom](presets/spaces-2/oak-ballroom.md) |
| 15 | [Ice House](presets/spaces-2/ice-house.md) |
| 16 | [Ice Beads](presets/spaces-2/ice-beads.md) |
| 17 | [Music Forest](presets/spaces-2/music-forest.md) |
| 18 | [Waving Bloom](presets/spaces-2/waving-bloom.md) |
| 19 | [Brick Chamber](presets/spaces-2/brick-chamber.md) |

## Summary matrix

Decoded from each dump using the densified encoding map (series, `provided` UI walks, sheet anchors). Cell values are labeled dump readings; `~` only when a step falls between witnesses. Detail: [presets/](presets/).

| Bank | Preset | [RT](bytes/reverb-time.md) | [Size](bytes/size.md) | [PreDly](bytes/predelay.md) | [Diff](bytes/diffusion.md) | [Dens](bytes/density.md) | [Mod](bytes/modulation.md) | [Roll](bytes/rolloff.md) | [HFmpy](bytes/hf-rt-multiply.md) | [HFxo](bytes/hf-rt-crossover.md) | [LFmpy](bytes/lf-rt-multiply.md) | [LFxo](bytes/lf-rt-crossover.md) | [VLF](bytes/vlf-cut.md) | [E/R](bytes/early-to-reverb-mix.md) | [ERoll](bytes/early-rolloff.md) | [ESel](bytes/early-select.md) | [DlyLvl](bytes/delay-level.md) | [DlyTim](bytes/delay-time.md) | [DlyMod](bytes/delay-modulation.md) |
|------|--------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [Halls](presets/halls/) | [Large Hall](presets/halls/large-hall.md) | 2.2 s | 28 | 10 ms | 7 | 2 | 4 | 5200 Hz | 0.75 | 3200 Hz | 1.2 | 800 Hz | -12 dB | 7/20 | 10800 Hz | 13 | off | 100 ms | off |
| [Halls](presets/halls/) | [Medium Hall](presets/halls/medium-hall.md) | 1.8 s | 23 | 24 ms | 6 | 3 | 4 | 6000 Hz | 0.75 | 3600 Hz | 1.2 | 800 Hz | -10 dB | 10/20 | 8800 Hz | 17 | off | 100 ms | off |
| [Halls](presets/halls/) | [Small Hall](presets/halls/small-hall.md) | 1.4 s | 6 | 0 ms | 5 | 5 | 2 | 5600 Hz | 0.75 | 3600 Hz | 1.05 | 800 Hz | -10 dB | 16/20 | 8000 Hz | 6 | off | 100 ms | off |
| [Halls](presets/halls/) | [Large & Near](presets/halls/large-and-near.md) | 2.2 s | 20 | 10 ms | 7 | 2 | 4 | 6000 Hz | 0.75 | 3200 Hz | 1.1 | 720 Hz | -11 dB | 20/20 | 10400 Hz | 14 | off | 100 ms | off |
| [Halls](presets/halls/) | [Medium & Near](presets/halls/medium-and-near.md) | 1.8 s | 20 | 24 ms | 6 | 3 | 4 | 6000 Hz | 0.75 | 3600 Hz | 1.1 | 800 Hz | -10 dB | 18/20 | 15600 Hz | 17 | off | 100 ms | off |
| [Halls](presets/halls/) | [Small & Near](presets/halls/small-and-near.md) | 1.4 s | 6 | 0 ms | 5 | 5 | 2 | 5600 Hz | 0.75 | 3600 Hz | 1.05 | 800 Hz | -7 dB | 20/16 | 9600 Hz | 7 | off | 100 ms | off |
| [Halls](presets/halls/) | [Large & Dark](presets/halls/large-and-dark.md) | 2.15 s | 20 | 0 ms | 6 | 5 | off | 4800 Hz | 0.75 | 2800 Hz | 1.15 | 720 Hz | -5 dB | 14/20 | 5200 Hz | 6 | off | 100 ms | off |
| [Halls](presets/halls/) | [Large & Deep](presets/halls/large-and-deep.md) | 2.15 s | 25 | 40 ms | 7 | 5 | 1 | 5200 Hz | 0.85 | 4000 Hz | 1.05 | 720 Hz | -10 dB | 5/20 | 7200 Hz | 17 | off | 100 ms | off |
| [Halls](presets/halls/) | [Medium & Deep](presets/halls/medium-and-deep.md) | 1.8 s | 15 | 20 ms | 7 | 4 | 1 | 5600 Hz | 0.75 | 4000 Hz | 1.05 | 800 Hz | -5 dB | 6/20 | 9600 Hz | 17 | off | 100 ms | off |
| [Halls](presets/halls/) | [Concert Hall](presets/halls/concert-hall.md) | 2.2 s | 20 | 18 ms | 5 | 1 | 6 | 5200 Hz | 0.75 | 3200 Hz | 1.2 | 560 Hz | -10 dB | 20/20 | 17200 Hz | 19 | off | 100 ms | off |
| [Halls](presets/halls/) | [Gold Hall](presets/halls/gold-hall.md) | 1.8 s | 23 | 30 ms | 3 | 1 | 4 | 6000 Hz | 0.7 | 6400 Hz | 1.25 | 480 Hz | 0 dB | 20/20 | 15200 Hz | 19 | off | 100 ms | off |
| [Halls](presets/halls/) | [Sandors Hall](presets/halls/sandors-hall.md) | 2.6 s | 20 | 20 ms | 3 | 2 | 5 | 5600 Hz | 0.7 | 3600 Hz | 1.2 | 1000 Hz | -14 dB | 19/20 | full | 19 | off | 100 ms | off |
| [Halls](presets/halls/) | [Dense Hall](presets/halls/dense-hall.md) | 2 s | 18 | 10 ms | 5 | 6 | 9 | 5600 Hz | 0.75 | 2800 Hz | 1.3 | 160 Hz | -3 dB | 20/20 | 12400 Hz | 18 | off | 100 ms | off |
| [Halls](presets/halls/) | [Clear Hall](presets/halls/clear-hall.md) | 2.2 s | 10 | 0 ms | 5 | 1 | off | 6800 Hz | 0.6 | 4800 Hz | 1 | 400 Hz | -4 dB | 20/20 | 11200 Hz | 9 | off | 100 ms | off |
| [Halls](presets/halls/) | [Brass Hall](presets/halls/brass-hall.md) | 2 s | 15 | 20 ms | 5 | 5 | 2 | 8400 Hz | 0.7 | 4800 Hz | 1 | 800 Hz | -11 dB | 20/18 | 13600 Hz | 19 | off | 100 ms | off |
| [Halls](presets/halls/) | [Amsterdam Hall](presets/halls/amsterdam-hall.md) | 2.3 s | 12 | 0 ms | 7 | 4 | low | 6800 Hz | 0.65 | 3600 Hz | 1.1 | 640 Hz | -6 dB | 18/20 | 14000 Hz | 15 | off | 100 ms | off |
| [Halls](presets/halls/) | [Berliner Hall](presets/halls/berliner-hall.md) | 2.5 s | 7 | 0 ms | 6 | 3 | low | 6400 Hz | 0.6 | 3200 Hz | 1.2 | 320 Hz | -6 dB | 20/18 | 18000 Hz | 10 | off | 100 ms | off |
| [Halls](presets/halls/) | [Boston Hall A](presets/halls/boston-hall-a.md) | 2.1 s | 10 | 0 ms | 6 | 4 | off | 6000 Hz | 0.7 | 3600 Hz | 1.05 | 280 Hz | -2 dB | 18/20 | 15600 Hz | 12 | off | 100 ms | off |
| [Halls](presets/halls/) | [Boston Hall B](presets/halls/boston-hall-b.md) | 1.8 s | 12 | 0 ms | 3 | 6 | off | 4800 Hz | 0.7 | 2800 Hz | 1.05 | 720 Hz | -9 dB | 18/20 | 10400 Hz | 9 | off | 100 ms | off |
| [Halls](presets/halls/) | [Chicago Hall](presets/halls/chicago-hall.md) | 2.1 s | 20 | 0 ms | 7 | 4 | off | 5600 Hz | 0.8 | 3200 Hz | 1.05 | 800 Hz | 0 dB | 15/20 | 6400 Hz | 8 | off | 100 ms | off |
| [Halls](presets/halls/) | [Vienna Hall](presets/halls/vienna-hall.md) | 2.3 s | 7 | 0 ms | 8 | 6 | low | 5600 Hz | 0.55 | 2800 Hz | 1 | 720 Hz | -9 dB | 20/19 | full | 16 | off | 100 ms | off |
| [Halls](presets/halls/) | [Worcester Hall](presets/halls/worcester-hall.md) | 2.25 s | 8 | 0 ms | 6 | 4 | off | 7600 Hz | 0.7 | 1800 Hz | 1.4 | 360 Hz | -11 dB | 16/20 | 15600 Hz | 19 | off | 100 ms | off |
| [Halls](presets/halls/) | [The ArchDuke](presets/halls/the-archduke.md) | 1.8 s | 7 | 0 ms | 5 | 5 | off | 5200 Hz | 0.75 | 3200 Hz | 1 | 720 Hz | -13 dB | 16/20 | 10000 Hz | 6 | off | 100 ms | off |
| [Halls](presets/halls/) | [Troy Hall](presets/halls/troy-hall.md) | 2.3 s | 10 | 10 ms | 5 | 4 | 1 | 8800 Hz | 0.85 | 1200 Hz | 1.2 | 640 Hz | -10 dB | 18/20 | 14000 Hz | 12 | off | 100 ms | off |
| [Halls](presets/halls/) | [Saint Sylvain](presets/halls/saint-sylvain.md) | 3.5 s | 8 | 10 ms | 5 | 8 | off | 8400 Hz | 0.95 | 800 Hz | 2.5 | 360 Hz | -11 dB | 20/20 | 15600 Hz | 7 | off | 100 ms | off |
| [Halls](presets/halls/) | [Mechanics Hall](presets/halls/mechanics-hall.md) | 2.25 s | 10 | 0 ms | 6 | 3 | low | 7200 Hz | 0.8 | 4000 Hz | 1.5 | 240 Hz | -5 dB | 20/17 | 5600 Hz | 6 | -20 dB | 428 ms | off |
| [Halls](presets/halls/) | [Saint Gerold](presets/halls/saint-gerold.md) | 3 s | 10 | 10 ms | 6 | 2 | off | 5600 Hz | 0.55 | 4000 Hz | 2 | 400 Hz | -3 dB | 20/17 | 4400 Hz | 14 | off | 100 ms | off |
| [Halls](presets/halls/) | [Pepes Hall A](presets/halls/pepes-hall-a.md) | 1.9 s | 10 | 30 ms | 3 | 6 | low | 4000 Hz | 0.8 | 2000 Hz | 0.9 | 640 Hz | -18 dB | 20/18 | 10000 Hz | 22 | off | 100 ms | off |
| [Halls](presets/halls/) | [Pepes Hall B](presets/halls/pepes-hall-b.md) | 1.9 s | 10 | 30 ms | 3 | 6 | low | 4000 Hz | 0.8 | 2400 Hz | 0.9 | 640 Hz | -18 dB | 20/18 | 10000 Hz | 22 | -12 dB | 300 ms | 2 |
| [Halls](presets/halls/) | [Reflect Hall A](presets/halls/reflect-hall-a.md) | 2.3 s | 7 | 0 ms | 6 | 3 | 1 | 7200 Hz | 0.65 | 2000 Hz | 1.35 | 2400 Hz | -10 dB | 20/20 | 8800 Hz | 21 | -18 dB | 444 ms | off |
| [Halls](presets/halls/) | [Reflect Hall B](presets/halls/reflect-hall-b.md) | 2.25 s | 22 | 20 ms | 6 | 5 | low | 6400 Hz | 0.75 | 3200 Hz | 1.3 | 720 Hz | -6 dB | 16/20 | 10400 Hz | 15 | -18 dB | 300 ms | low |
| [Halls](presets/halls/) | [Piano Hall](presets/halls/piano-hall.md) | 2 s | 16 | 24 ms | 3 | 5 | 1 | 6400 Hz | 0.8 | 2800 Hz | 1 | 560 Hz | -8 dB | 16/20 | 10400 Hz | 16 | off | 100 ms | off |
| [Plates](presets/plates/) | [Bright Plate](presets/plates/bright-plate.md) | 2 s | 4 | 0 ms | 3 | 7 | 2 | 6400 Hz | 0.8 | 5600 Hz | 0.7 | 1200 Hz | -15 dB | 20/20 | 10400 Hz | 15 | off | 100 ms | off |
| [Plates](presets/plates/) | [Dark Plate](presets/plates/dark-plate.md) | 1.5 s | 4 | 0 ms | 3 | 7 | 2 | 4800 Hz | 0.8 | 4000 Hz | 0.9 | 800 Hz | -15 dB | 20/20 | 6800 Hz | 8 | off | 100 ms | off |
| [Plates](presets/plates/) | [London Plate](presets/plates/london-plate.md) | 1.8 s | 4 | 0 ms | 1 | 10 | off | 4400 Hz | 0.95 | 3200 Hz | 1 | 800 Hz | -10 dB | 20/20 | 7200 Hz | 2 | off | 100 ms | off |
| [Plates](presets/plates/) | [Snare Plate A](presets/plates/snare-plate-a.md) | 1.2 s | 10 | 0 ms | 2 | 9 | 3 | 6800 Hz | 0.9 | 3200 Hz | 1 | 1000 Hz | -9 dB | 20/20 | 12000 Hz | 5 | off | 100 ms | off |
| [Plates](presets/plates/) | [Snare Plate B](presets/plates/snare-plate-b.md) | 1 s | 10 | 20 ms | 3 | 9 | 1 | 7200 Hz | 0.85 | 3600 Hz | 0.95 | 800 Hz | -10 dB | 19/20 | 10400 Hz | 3 | off | 100 ms | off |
| [Plates](presets/plates/) | [Vocal Plate](presets/plates/vocal-plate.md) | 1.5 s | 5 | 24 ms | 5 | 7 | 3 | 6400 Hz | 0.9 | 5600 Hz | 0.85 | 1200 Hz | -19 dB | 20/20 | 8000 Hz | 15 | off | 100 ms | off |
| [Plates](presets/plates/) | [Old Plate](presets/plates/old-plate.md) | 1.25 s | 6 | 0 ms | 4 | 2 | off | 7600 Hz | 0.85 | 5600 Hz | 1 | 400 Hz | -8 dB | 20/18 | 10000 Hz | 7 | off | 100 ms | off |
| [Plates](presets/plates/) | [Rich Plate](presets/plates/rich-plate.md) | 1.9 s | 5 | 0 ms | 8 | 4 | 3 | 9200 Hz | 1.0 | 6400 Hz | 0.95 | 800 Hz | -9 dB | 18/20 | 15200 Hz | 4 | off | 100 ms | off |
| [Plates](presets/plates/) | [Gold Plate](presets/plates/gold-plate.md) | 1.8 s | 10 | 0 ms | 2 | 8 | off | 5200 Hz | 0.8 | 3600 Hz | 1.2 | 480 Hz | -10 dB | 15/20 | 9600 Hz | 2 | off | 100 ms | off |
| [Plates](presets/plates/) | [Dense Plate](presets/plates/dense-plate.md) | 1.7 s | 3 | 0 ms | 3 | 10 | 7 | 5600 Hz | 0.8 | 4800 Hz | 0.9 | 1000 Hz | -15 dB | 20/20 | 6400 Hz | 4 | off | 100 ms | off |
| [Plates](presets/plates/) | [Silver Plate](presets/plates/silver-plate.md) | 2 s | 8 | 10 ms | 3 | 8 | 2 | 8800 Hz | 0.8 | 4800 Hz | 0.95 | 1000 Hz | -15 dB | 18/20 | 10400 Hz | 5 | off | 100 ms | off |
| [Plates](presets/plates/) | [Percussion](presets/plates/percussion.md) | 1.1 s | 2 | 0 ms | 3 | 7 | 3 | 5200 Hz | 0.8 | 5600 Hz | 0.8 | 1200 Hz | -10 dB | 20/18 | 6400 Hz | 3 | off | 100 ms | off |
| [Plates](presets/plates/) | [Echo Plate](presets/plates/echo-plate.md) | 1.7 s | 3 | 60 ms | 4 | 8 | 2 | 5600 Hz | 0.8 | 4800 Hz | 0.9 | 1000 Hz | -15 dB | 18/20 | 7200 Hz | 19 | off | 100 ms | off |
| [Plates](presets/plates/) | [CD Plate A](presets/plates/cd-plate-a.md) | 1.7 s | 8 | 0 ms | 3 | 8 | high | 6400 Hz | 0.75 | 5600 Hz | 0.8 | 1000 Hz | -11 dB | 20/18 | 9600 Hz | 0 | off | 100 ms | off |
| [Plates](presets/plates/) | [CD Plate B](presets/plates/cd-plate-b.md) | 1.6 s | 7 | 0 ms | 2 | 10 | 5 | 5600 Hz | 0.9 | 2800 Hz | 1.3 | 400 Hz | -6 dB | 20/20 | 9600 Hz | 2 | off | 100 ms | off |
| [Plates](presets/plates/) | [Large Plate](presets/plates/large-plate.md) | 2.2 s | 10 | 0 ms | 1 | 9 | off | 4800 Hz | 0.8 | 3200 Hz | 1.1 | 800 Hz | -10 dB | 20/20 | 9600 Hz | 7 | off | 100 ms | off |
| [Plates](presets/plates/) | [Small Plate](presets/plates/small-plate.md) | 0.9 s | 5 | 0 ms | 3 | 9 | off | 5600 Hz | 0.8 | 4800 Hz | 0.95 | 400 Hz | -10 dB | 20/18 | 10000 Hz | 4 | off | 100 ms | off |
| [Plates](presets/plates/) | [Fat Plate](presets/plates/fat-plate.md) | 0.95 s | 5 | 0 ms | 3 | 8 | 9 | 6000 Hz | 0.8 | 3600 Hz | 1.2 | 240 Hz | -2 dB | 20/20 | 9600 Hz | 2 | off | 100 ms | off |
| [Plates](presets/plates/) | [Crystal Plate](presets/plates/crystal-plate.md) | 1.35 s | 17 | 18 ms | 3 | 4 | 4 | 12000 Hz | 0.8 | 2800 Hz | 0.75 | 4000 Hz | -20 dB | 20/10 | 15200 Hz | 4 | off | 100 ms | off |
| [Plates](presets/plates/) | [Sun Plate A](presets/plates/sun-plate-a.md) | 2.55 s | 2 | 0 ms | 6 | 5 | 1 | 10000 Hz | 0.85 | 1800 Hz | 1.05 | 560 Hz | -11 dB | 20/16 | full | 15 | off | 100 ms | off |
| [Plates](presets/plates/) | [Sun Plate B](presets/plates/sun-plate-b.md) | 2.55 s | 2 | 0 ms | 6 | 5 | 3 | 10400 Hz | 0.9 | 1600 Hz | 1.05 | 560 Hz | -11 dB | 20/16 | full | 15 | off | 100 ms | off |
| [Plates](presets/plates/) | [Sun Plate C](presets/plates/sun-plate-c.md) | 2.15 s | 3 | 0 ms | 5 | 7 | off | 8400 Hz | 0.8 | 3600 Hz | 1.4 | 400 Hz | -20 dB | 20/16 | 15200 Hz | 6 | off | 100 ms | off |
| [Plates](presets/plates/) | [Vocal Plate B](presets/plates/vocal-plate-b.md) | 2.3 s | 2 | 0 ms | 6 | 5 | 3 | 10000 Hz | 0.9 | 1600 Hz | 1.05 | 560 Hz | -11 dB | 20/16 | 11600 Hz | 15 | -12 dB | 260 ms | off |
| [Plates](presets/plates/) | [Repro Plate](presets/plates/repro-plate.md) | 1.9 s | 10 | 0 ms | 7 | 4 | 2 | 6000 Hz | 0.9 | 2000 Hz | 1.1 | 320 Hz | -10 dB | 18/20 | 11200 Hz | 9 | -10 dB | 276 ms | low |
| [Rooms](presets/rooms/) | [Studio A](presets/rooms/studio-a.md) | 0.7 s | 2 | 4 ms | 2 | 8 | low | 8400 Hz | 0.85 | 6400 Hz | 0.7 | 1200 Hz | -3 dB | 20/15 | 11600 Hz | 4 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Studio B Close](presets/rooms/studio-b-close.md) | 0.75 s | 2 | 0 ms | 1 | 10 | low | 8000 Hz | 0.7 | 2800 Hz | 1.15 | 560 Hz | 0 dB | 20/13 | 8000 Hz | 7 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Studio B Far](presets/rooms/studio-b-far.md) | 0.65 s | 5 | 0 ms | 3 | 7 | off | 9200 Hz | 0.8 | 2000 Hz | 1.15 | 480 Hz | -3 dB | 20/19 | 10000 Hz | 12 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Studio C](presets/rooms/studio-c.md) | 0.55 s | 2 | 0 ms | 3 | 0 | off | 7200 Hz | 0.9 | 3600 Hz | 1.15 | 560 Hz | -2 dB | 20/17 | 8000 Hz | 4 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Studio D](presets/rooms/studio-d.md) | 0.45 s | 5 | 0 ms | 5 | 3 | off | 7200 Hz | 0.8 | 4000 Hz | 1.5 | 320 Hz | 0 dB | 18/20 | 14800 Hz | 2 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Studio E](presets/rooms/studio-e.md) | 1 s | 1 | 0 ms | 3 | 0 | off | 4800 Hz | 0.8 | 3200 Hz | 1 | 560 Hz | -1 dB | 20/19 | 12000 Hz | 4 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Deep Stone](presets/rooms/deep-stone.md) | 1.2 s | 5 | 20 ms | 4 | 6 | 1 | 5600 Hz | 0.9 | 5600 Hz | 0.8 | 1000 Hz | -8 dB | 17/20 | 16000 Hz | 9 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Music Room](presets/rooms/music-room.md) | 1 s | 20 | 0 ms | 5 | 4 | 2 | 7600 Hz | 0.9 | 5600 Hz | 1 | 800 Hz | -9 dB | 13/20 | 8800 Hz | 17 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Heavy Room](presets/rooms/heavy-room.md) | 0.6 s | 5 | 0 ms | 5 | 2 | off | 9600 Hz | 0.75 | 7200 Hz | 1.35 | 560 Hz | 0 dB | 20/19 | 6400 Hz | 9 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Large Wooden](presets/rooms/large-wooden.md) | 1.2 s | 6 | 0 ms | 3 | 3 | low | 8000 Hz | 0.75 | 4800 Hz | 0.85 | 1000 Hz | -9 dB | 20/19 | 10400 Hz | 9 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Small Wooden](presets/rooms/small-wooden.md) | 0.6 s | 5 | 0 ms | 5 | 3 | off | 9600 Hz | 0.75 | 7200 Hz | 0.9 | 1000 Hz | -7 dB | 20/20 | 10400 Hz | 9 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Large Tiled](presets/rooms/large-tiled.md) | 1.2 s | 10 | 0 ms | 3 | 2 | off | 9600 Hz | 0.7 | 6400 Hz | 0.7 | 1400 Hz | -10 dB | 20/18 | 16000 Hz | 18 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Medium Tiled](presets/rooms/medium-tiled.md) | 1 s | 4 | 0 ms | 1 | 1 | off | 9600 Hz | 0.75 | 6400 Hz | 0.75 | 1400 Hz | -10 dB | 20/16 | 16000 Hz | 9 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Small Tiled](presets/rooms/small-tiled.md) | 0.7 s | small | 0 ms | 4 | 0 | off | 9600 Hz | 0.8 | 6400 Hz | 0.45 | 1400 Hz | -12 dB | 20/16 | 16800 Hz | 9 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Drum & Chamber](presets/rooms/drum-and-chamber.md) | 1.2 s | 10 | 60 ms | 5 | 4 | high | 6400 Hz | 0.7 | 3600 Hz | 0.9 | 1000 Hz | -6 dB | 18/20 | 11200 Hz | 9 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Djangos Room](presets/rooms/djangos-room.md) | 0.8 s | 2 | 4 ms | 5 | 3 | 3 | 5200 Hz | 0.85 | 3200 Hz | 1 | 480 Hz | -10 dB | 20/18 | 12800 Hz | 6 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Small Vox Room](presets/rooms/small-vox-room.md) | 0.95 s | small | 0 ms | 4 | 6 | 2 | 7200 Hz | 0.55 | 1800 Hz | 1.75 | 2000 Hz | -12 dB | 20/8 | 7200 Hz | 1 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Glass Room](presets/rooms/glass-room.md) | 0.8 s | 3 | 0 ms | 4 | 0 | off | 6400 Hz | 0.85 | 5600 Hz | 0.6 | 1600 Hz | -13 dB | 20/17 | 18400 Hz | 19 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Percussion](presets/rooms/percussion.md) | 0.7 s | 3 | 0 ms | 3 | 3 | 3 | 7200 Hz | 0.6 | 6400 Hz | 0.7 | 720 Hz | -11 dB | 20/18 | 13600 Hz | 18 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Marble Foyer](presets/rooms/marble-foyer.md) | 1.25 s | 8 | 10 ms | 3 | 1 | off | 6400 Hz | 0.8 | 4000 Hz | 0.65 | 1600 Hz | -15 dB | 20/17 | 16400 Hz | 19 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Large Q Room](presets/rooms/large-q-room.md) | 2.6 s | 20 | 0 ms | 6 | 1 | low | 4800 Hz | 0.7 | 1000 Hz | 1.4 | 800 Hz | -9 dB | 19/20 | 16800 Hz | 19 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Small Q Room](presets/rooms/small-q-room.md) | 1.2 s | 10 | 10 ms | 6 | 2 | off | 5600 Hz | 0.7 | 2800 Hz | 1.1 | 640 Hz | -6 dB | 18/20 | 15600 Hz | 15 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Large Red Room](presets/rooms/large-red-room.md) | 1 s | 4 | 0 ms | 5 | 1 | off | 9600 Hz | 0.75 | 3600 Hz | 0.9 | 1200 Hz | -7 dB | 20/12 | 14000 Hz | 9 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Red Room](presets/rooms/red-room.md) | 0.4 s | small | 0 ms | 5 | 1 | off | 10400 Hz | 0.8 | 3600 Hz | 0.9 | 1600 Hz | -7 dB | 20/12 | 13600 Hz | 9 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Blue Room](presets/rooms/blue-room.md) | 0.6 s | 2 | 0 ms | 6 | 4 | off | 9600 Hz | 0.65 | 6400 Hz | 0.7 | 2000 Hz | -9 dB | 20/11 | 8800 Hz | 8 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Large Room](presets/rooms/large-room.md) | 1.1 s | 5 | 0 ms | 4 | 4 | 2 | 6000 Hz | 0.65 | 2400 Hz | 0.95 | 800 Hz | -12 dB | 20/16 | 7200 Hz | 7 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Small Room](presets/rooms/small-room.md) | 0.6 s | small | 0 ms | 4 | 5 | 2 | 6800 Hz | 0.55 | 2000 Hz | 1.05 | 1000 Hz | -12 dB | 20/10 | 7200 Hz | 6 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Front Room](presets/rooms/front-room.md) | 0.4 s | 2 | 0 ms | 3 | 3 | 9 | 6000 Hz | 0.75 | 4000 Hz | 0.95 | 480 Hz | -15 dB | 20/16 | 12000 Hz | 3 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Center Room](presets/rooms/center-room.md) | 0.5 s | 3 | 2 ms | 4 | 3 | 5 | 5600 Hz | 0.75 | 3600 Hz | 1 | 480 Hz | -12 dB | 20/20 | 10000 Hz | 5 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Back Room](presets/rooms/back-room.md) | 0.55 s | 4 | 4 ms | 3 | 5 | 7 | 5600 Hz | 0.65 | 3600 Hz | 1.05 | 280 Hz | -10 dB | 16/20 | 9200 Hz | 7 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Studio K](presets/rooms/studio-k.md) | 0.2 s | 2 | 6 ms | 2 | 3 | off | 6800 Hz | 0.4 | 7200 Hz | 1.4 | 640 Hz | -12 dB | 20/14 | 7200 Hz | 5 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Waits Room](presets/rooms/waits-room.md) | 0.85 s | 4 | 10 ms | 1 | 4 | off | 8400 Hz | 0.95 | 9600 Hz | 0.7 | 1200 Hz | -11 dB | 20/16 | 11600 Hz | 9 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Corn Room](presets/rooms/corn-room.md) | 2.3 s | 10 | 24 ms | 3 | 2 | off | 4800 Hz | 0.9 | 1200 Hz | 0.4 | 320 Hz | -20 dB | 20/16 | 10000 Hz | 8 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Oakland Room](presets/rooms/oakland-room.md) | 1.45 s | 15 | 20 ms | 2 | 3 | off | 5600 Hz | 0.85 | 2800 Hz | 0.9 | 1000 Hz | -10 dB | 20/12 | 5200 Hz | 15 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [SF Perf Room](presets/rooms/sf-perf-room.md) | 1.5 s | 10 | 20 ms | 2 | 2 | off | 5200 Hz | 0.7 | 3200 Hz | 0.85 | 800 Hz | -17 dB | 20/11 | 6000 Hz | 15 | off | 100 ms | off |
| [Rooms](presets/rooms/) | [Long Wood Room](presets/rooms/long-wood-room.md) | 1.2 s | 6 | 0 ms | 3 | 3 | low | 7600 Hz | 0.75 | 4800 Hz | 0.85 | 1000 Hz | -9 dB | 19/20 | 10400 Hz | 9 | -16 dB | 236 ms | off |
| [Chambers](presets/chambers/) | [Large Chamber](presets/chambers/large-chamber.md) | 1.4 s | 5 | 10 ms | 5 | 3 | 1 | 6400 Hz | 0.8 | 4000 Hz | 0.95 | 720 Hz | -15 dB | 20/20 | 10000 Hz | 6 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Medium Chamber](presets/chambers/medium-chamber.md) | 1.25 s | 3 | 4 ms | 5 | 3 | 1 | 6400 Hz | 0.8 | 4800 Hz | 0.9 | 800 Hz | -12 dB | 20/20 | 10000 Hz | 5 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Small Chamber](presets/chambers/small-chamber.md) | 1 s | 2 | 0 ms | 5 | 3 | off | 6400 Hz | 0.8 | 4800 Hz | 0.95 | 720 Hz | -12 dB | 20/20 | 10000 Hz | 5 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Large & Dark](presets/chambers/large-and-dark.md) | 1.5 s | 5 | 0 ms | 6 | 3 | 1 | 4800 Hz | 0.75 | 4800 Hz | 0.9 | 1000 Hz | -10 dB | 20/18 | 8800 Hz | 9 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Small & Dark](presets/chambers/small-and-dark.md) | 1.2 s | 3 | 0 ms | 6 | 3 | off | 5600 Hz | 0.75 | 4800 Hz | 0.9 | 1000 Hz | -8 dB | 20/18 | 8800 Hz | 9 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Large & Bright](presets/chambers/large-and-bright.md) | 1.6 s | 5 | 10 ms | 6 | 4 | 1 | 8000 Hz | 0.85 | 4800 Hz | 0.9 | 800 Hz | -12 dB | 20/20 | 14400 Hz | 6 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Small & Bright](presets/chambers/small-and-bright.md) | 1 s | 3 | 0 ms | 6 | 2 | off | 12000 Hz | 0.7 | 6400 Hz | 0.75 | 1000 Hz | -15 dB | 20/18 | 12000 Hz | 9 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Kick Chamber](presets/chambers/kick-chamber.md) | 0.7 s | 10 | 0 ms | 5 | 10 | 7 | 5600 Hz | 0.9 | 4800 Hz | 1 | 640 Hz | -6 dB | 20/20 | 14000 Hz | 3 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Snare Chamber](presets/chambers/snare-chamber.md) | 1.2 s | 3 | 10 ms | 4 | 7 | 2 | 5600 Hz | 0.9 | 4800 Hz | 0.9 | 800 Hz | -19 dB | 20/20 | 9600 Hz | 5 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Vocal Chamber](presets/chambers/vocal-chamber.md) | 1.6 s | 3 | 0 ms | 7 | 4 | 2 | 8000 Hz | 0.75 | 5600 Hz | 0.75 | 800 Hz | -10 dB | 20/20 | 10400 Hz | 9 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [A&M Chamber](presets/chambers/a-and-m-chamber.md) | 2.2 s | 15 | 20 ms | 5 | 4 | 1 | 6400 Hz | 0.8 | 5600 Hz | 1.05 | 800 Hz | -14 dB | 15/20 | 12000 Hz | 7 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [CD Chamber](presets/chambers/cd-chamber.md) | 1.9 s | 9 | 20 ms | 5 | 7 | 5 | 6000 Hz | 0.8 | 3200 Hz | 1 | 800 Hz | -10 dB | 18/20 | 10400 Hz | 6 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Old Chamber](presets/chambers/old-chamber.md) | 2.4 s | 5 | 0 ms | 5 | 4 | 3 | 6400 Hz | 0.7 | 3200 Hz | 1.25 | 560 Hz | -9 dB | 10/20 | 8000 Hz | 9 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Deep Chamber](presets/chambers/deep-chamber.md) | 1.9 s | 8 | 0 ms | 7 | 4 | off | 6400 Hz | 0.7 | 4000 Hz | 1 | 1000 Hz | -10 dB | 16/20 | 10400 Hz | 9 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Amb Chamber A](presets/chambers/amb-chamber-a.md) | 1.65 s | 20 | 0 ms | 7 | 4 | 3 | 7600 Hz | 0.75 | 5600 Hz | 0.9 | 1000 Hz | -11 dB | 14/20 | 12000 Hz | 5 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Amb Chamber B](presets/chambers/amb-chamber-b.md) | 1.5 s | 15 | 0 ms | 7 | 4 | 2 | 6000 Hz | 0.75 | 4800 Hz | 0.9 | 1000 Hz | -8 dB | 16/20 | 10400 Hz | 8 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [Sunset Chamber](presets/chambers/sunset-chamber.md) | 2.15 s | 3 | 20 ms | 2 | 7 | off | 7200 Hz | 1.0 | 3600 Hz | 0.6 | 360 Hz | -20 dB | 18/20 | 6000 Hz | 7 | off | 100 ms | off |
| [Chambers](presets/chambers/) | [A&M Chamber B](presets/chambers/a-and-m-chamber-b.md) | 2.2 s | 15 | 20 ms | 4 | 5 | 1 | 6000 Hz | 0.8 | 4800 Hz | 0.95 | 480 Hz | -17 dB | 15/20 | 12000 Hz | 7 | -15 dB | 340 ms | off |
| [Chambers](presets/chambers/) | [Stone Chamber](presets/chambers/stone-chamber.md) | 1.7 s | 8 | 10 ms | 4 | 5 | 1 | 5200 Hz | 0.8 | 3200 Hz | 0.9 | 280 Hz | -10 dB | 19/20 | 14000 Hz | 12 | -10 dB | 236 ms | 2 |
| [Chambers](presets/chambers/) | [Tiled Chamber](presets/chambers/tiled-chamber.md) | 1.7 s | 6 | 10 ms | 6 | 3 | low | 7200 Hz | 0.9 | 3200 Hz | 0.85 | 1000 Hz | -13 dB | 20/19 | 10800 Hz | 15 | -15 dB | 260 ms | 1 |
| [Chambers](presets/chambers/) | [Fat Chamber](presets/chambers/fat-chamber.md) | 1.6 s | 6 | 10 ms | 3 | 7 | 1 | 5600 Hz | 0.8 | 2000 Hz | 1.35 | 480 Hz | 0 dB | 20/18 | 12000 Hz | 12 | -12 dB | 140 ms | 4 |
| [Chambers](presets/chambers/) | [Echo Chamber](presets/chambers/echo-chamber.md) | 1.9 s | 10 | 10 ms | 4 | 5 | 3 | 6400 Hz | 0.8 | 2400 Hz | 1 | 480 Hz | -10 dB | 19/20 | 12000 Hz | 12 | -8 dB | 348 ms | off |
| [Ambience](presets/ambience/) | [Large Ambience](presets/ambience/large-ambience.md) | 0.8 s | 15 | 10 ms | 3 | 3 | off | 6000 Hz | 0.85 | 3600 Hz | 0.9 | 800 Hz | -10 dB | 20/10 | 10400 Hz | 12 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Med Ambience](presets/ambience/med-ambience.md) | 0.65 s | 8 | 2 ms | 3 | 3 | off | 6000 Hz | 0.85 | 3600 Hz | 0.9 | 800 Hz | -10 dB | 20/10 | 10400 Hz | 7 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Small Ambience](presets/ambience/small-ambience.md) | 0.45 s | 4 | 0 ms | 3 | 3 | off | 6000 Hz | 0.9 | 3600 Hz | 0.9 | 800 Hz | -10 dB | 20/13 | 10400 Hz | 1 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Large & Dark](presets/ambience/large-and-dark.md) | 1 s | 15 | 10 ms | 2 | 3 | off | 3200 Hz | 0.8 | 2800 Hz | 1.05 | 560 Hz | -10 dB | 20/13 | 5600 Hz | 9 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Medium & Dark](presets/ambience/medium-and-dark.md) | 0.9 s | 8 | 2 ms | 2 | 3 | off | 3200 Hz | 0.8 | 2800 Hz | 1.05 | 560 Hz | -10 dB | 20/13 | 3600 Hz | 5 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Small & Dark](presets/ambience/small-and-dark.md) | 0.5 s | 3 | 0 ms | 2 | 3 | off | 2800 Hz | 0.8 | 2400 Hz | 1.05 | 560 Hz | -10 dB | 20/13 | 3600 Hz | 1 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Large & Bright](presets/ambience/large-and-bright.md) | 0.95 s | 15 | 10 ms | 3 | 1 | off | 8000 Hz | 0.8 | 5600 Hz | 0.85 | 800 Hz | -15 dB | 20/12 | 15200 Hz | 12 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Med & Bright](presets/ambience/med-and-bright.md) | 0.75 s | 8 | 2 ms | 3 | 1 | off | 8000 Hz | 0.8 | 5600 Hz | 0.85 | 800 Hz | -15 dB | 20/12 | 15200 Hz | 7 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Small & Bright](presets/ambience/small-and-bright.md) | 0.4 s | 4 | 0 ms | 3 | 1 | off | 8000 Hz | 0.8 | 5600 Hz | 0.85 | 800 Hz | -11 dB | 20/13 | 15200 Hz | 3 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Deep Ambience](presets/ambience/deep-ambience.md) | 1 s | 24 | 20 ms | 3 | 1 | off | 5600 Hz | 0.8 | 4000 Hz | 0.95 | 800 Hz | -10 dB | 20/15 | 10400 Hz | 19 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Long Ambience](presets/ambience/long-ambience.md) | 1.15 s | 25 | 10 ms | 2 | 1 | off | 5600 Hz | 0.8 | 3600 Hz | 1.05 | 800 Hz | -15 dB | 20/10 | 10400 Hz | 19 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Clear Ambience](presets/ambience/clear-ambience.md) | 0.7 s | 15 | 6 ms | 2 | 0 | off | 6400 Hz | 0.8 | 4800 Hz | 0.9 | 1000 Hz | -20 dB | 20/13 | 11200 Hz | 9 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Heavy Ambience](presets/ambience/heavy-ambience.md) | 0.55 s | 7 | 6 ms | 0 | 2 | off | 7200 Hz | 0.85 | 3600 Hz | 1.1 | 240 Hz | -2 dB | 20/16 | 9600 Hz | 5 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Bass  XXL](presets/ambience/bass-xxl.md) | 1.25 s | large | 0 ms | 3 | 4 | off | 200 Hz | 0.5 | 320 Hz | 1 | 1000 Hz | 0 dB | 20/20 | 200 Hz | 19 | off | 100 ms | off |
| [Ambience](presets/ambience/) | [Percussion Air](presets/ambience/percussion-air.md) | 0.5 s | 3 | 0 ms | 10 | 7 | off | 8000 Hz | 0.8 | 2400 Hz | 0.95 | 2400 Hz | -6 dB | 20/9 | full | 6 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [North Church](presets/spaces/north-church.md) | 3.2 s | 11 | 0 ms | 5 | 3 | low | 5600 Hz | 0.5 | 2400 Hz | 1.3 | 640 Hz | -6 dB | 17/20 | 12000 Hz | 15 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [East Church](presets/spaces/east-church.md) | 3.3 s | 15 | 0 ms | 2 | 5 | low | 8000 Hz | 0.55 | 2800 Hz | 0.5 | 640 Hz | -15 dB | 20/18 | full | 19 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [South Church](presets/spaces/south-church.md) | 3.9 s | 12 | 0 ms | 5 | 4 | low | 5200 Hz | 0.6 | 1200 Hz | 1.1 | 240 Hz | -4 dB | 19/20 | 14400 Hz | 19 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [West Church](presets/spaces/west-church.md) | 5.4 s | 20 | 0 ms | 6 | 1 | low | 4800 Hz | 0.7 | 1000 Hz | 1 | 800 Hz | -9 dB | 19/20 | 16800 Hz | 16 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Cinema Room](presets/spaces/cinema-room.md) | 0.45 s | small | 4 ms | 8 | 4 | off | 4800 Hz | 0.6 | 2400 Hz | 0.8 | 1000 Hz | -4 dB | 20/20 | 5600 Hz | 9 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Scoring Stage](presets/spaces/scoring-stage.md) | 2.2 s | 18 | 0 ms | 7 | 2 | low | 7600 Hz | 0.75 | 2400 Hz | 0.9 | 720 Hz | -5 dB | 19/20 | 9600 Hz | 19 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Bath House](presets/spaces/bath-house.md) | 3.9 s | 15 | 6 ms | 9 | 6 | low | 8800 Hz | 0.85 | 1000 Hz | 0.35 | 640 Hz | -20 dB | 16/20 | full | 19 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Car Park](presets/spaces/car-park.md) | 3.5 s | large | 48 ms | 3 | 0 | off | 2000 Hz | 0.5 | 1600 Hz | 1.5 | 120 Hz | -12 dB | 18/20 | 4800 Hz | 4 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Arena](presets/spaces/arena.md) | 2.3 s | 28 | 80 ms | 2 | 1 | low | 5600 Hz | 0.6 | 2800 Hz | 1.35 | 640 Hz | -10 dB | 14/20 | 1200 Hz | 19 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Redwood Valley](presets/spaces/redwood-valley.md) | 1.9 s | large | 220 ms | 4 | 4 | low | 3200 Hz | 0.6 | 3200 Hz | 1.25 | 240 Hz | -10 dB | 20/20 | full | 19 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Tanglewood](presets/spaces/tanglewood.md) | 3 s | large | 20 ms | 3 | 3 | low | 4800 Hz | 0.65 | 2000 Hz | 1.4 | 480 Hz | -6 dB | 20/16 | 15600 Hz | 18 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Academy Yard](presets/spaces/academy-yard.md) | 3.5 s | large | 300 ms | 3 | 2 | off | 3200 Hz | 0.45 | 2400 Hz | 0.9 | 720 Hz | -12 dB | 20/8 | 7200 Hz | 19 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Hillside](presets/spaces/hillside.md) | 8 s | large | 300 ms | 3 | 9 | off | 1600 Hz | 0.35 | 1000 Hz | 0.2 | 1800 Hz | -20 dB | 20/10 | 1000 Hz | 5 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Cavern](presets/spaces/cavern.md) | 4 s | 18 | 0 ms | 4 | 3 | off | 3600 Hz | 0.6 | 1400 Hz | 4 | 200 Hz | -5 dB | 19/20 | 5600 Hz | 19 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Stone Quarry](presets/spaces/stone-quarry.md) | 5.1 s | 15 | 0 ms | 2 | 0 | low | 3600 Hz | 0.65 | 800 Hz | 4 | 200 Hz | 0 dB | 13/20 | 12000 Hz | 19 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Europa](presets/spaces/europa.md) | 25 s | large | 0 ms | 4 | 6 | high | 5200 Hz | 0.2 | 5600 Hz | 2.2 | 80 Hz | -6 dB | 8/20 | 120 Hz | 19 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Gated Space](presets/spaces/gated-space.md) | 1.5 s | 12 | 32 ms | 9 | 8 | 8 | 7600 Hz | 0.2 | 720 Hz | 0.8 | 240 Hz | -6 dB | 19/20 | 15200 Hz | 10 | off | 100 ms | off |
| [Spaces](presets/spaces/) | [Reflect Chapel](presets/spaces/reflect-chapel.md) | 3.8 s | 22 | 0 ms | 9 | 4 | 3 | 5600 Hz | 0.7 | 2400 Hz | 1.2 | 640 Hz | -6 dB | 18/20 | 11200 Hz | 20 | -13 dB | 340 ms | 1 |
| [Spaces](presets/spaces/) | [Reflect Church](presets/spaces/reflect-church.md) | 4 s | 25 | 0 ms | 3 | 4 | 4 | 5600 Hz | 0.7 | 2400 Hz | 1.3 | 320 Hz | -6 dB | 15/20 | 14000 Hz | 20 | -18 dB | 500 ms | 6 |
| [Halls 2](presets/halls-2/) | [Large Hall](presets/halls-2/large-hall.md) | 2.35 s | 25 | 24 ms | 8 | 4 | 7 | 3600 Hz | 0.75 | 3600 Hz | 1.2 | 720 Hz | -13 dB | 8/20 | 3200 Hz | 21 | off | 100 ms | off |
| [Halls 2](presets/halls-2/) | [Large & Stage](presets/halls-2/large-and-stage.md) | 2.3 s | 27 | 24 ms | 7 | 4 | 7 | 3600 Hz | 0.8 | 3600 Hz | 1.25 | 1200 Hz | -10 dB | 14/20 | 4400 Hz | 28 | off | 100 ms | off |
| [Halls 2](presets/halls-2/) | [Medium Hall](presets/halls-2/medium-hall.md) | 1.75 s | 17 | 24 ms | 8 | 5 | 7 | 4800 Hz | 0.75 | 3600 Hz | 1.25 | 720 Hz | -10 dB | 8/20 | 3200 Hz | 13 | off | 100 ms | off |
| [Halls 2](presets/halls-2/) | [Med & Stage](presets/halls-2/med-and-stage.md) | 1.75 s | 22 | 24 ms | 8 | 6 | 7 | 4000 Hz | 0.75 | 3600 Hz | 1.25 | 800 Hz | -8 dB | 14/20 | 7600 Hz | 23 | off | 100 ms | off |
| [Halls 2](presets/halls-2/) | [Small Hall](presets/halls-2/small-hall.md) | 1.15 s | 15 | 24 ms | 7 | 5 | 7 | 4400 Hz | 0.7 | 3600 Hz | 1 | 800 Hz | -10 dB | 6/20 | 3200 Hz | 6 | off | 100 ms | off |
| [Halls 2](presets/halls-2/) | [Small & Stage](presets/halls-2/small-and-stage.md) | 1.15 s | 11 | 24 ms | 7 | 5 | 7 | 4400 Hz | 0.7 | 3600 Hz | 1 | 800 Hz | -13 dB | 12/20 | 6800 Hz | 23 | off | 100 ms | off |
| [Halls 2](presets/halls-2/) | [Large Church](presets/halls-2/large-church.md) | 4.1 s | 20 | 0 ms | 1 | 5 | 6 | 2800 Hz | 0.7 | 1800 Hz | 1.55 | 1000 Hz | -8 dB | 6/20 | 6000 Hz | 24 | off | 100 ms | off |
| [Halls 2](presets/halls-2/) | [Small Church](presets/halls-2/small-church.md) | 2.5 s | 7 | 0 ms | 6 | 7 | 7 | 3600 Hz | 0.7 | 3200 Hz | 1 | 560 Hz | -17 dB | 10/20 | 6800 Hz | 20 | off | 100 ms | off |
| [Halls 2](presets/halls-2/) | [Jazz Hall](presets/halls-2/jazz-hall.md) | 1.35 s | 15 | 0 ms | 7 | 6 | 7 | 8800 Hz | 0.7 | 5600 Hz | 1.2 | 720 Hz | -10 dB | 8/20 | 10800 Hz | 20 | off | 100 ms | off |
| [Halls 2](presets/halls-2/) | [West Hall](presets/halls-2/west-hall.md) | 2.2 s | 15 | 0 ms | 5 | 4 | low | 3600 Hz | 0.7 | 3200 Hz | 1.6 | 560 Hz | -5 dB | 20/18 | 8800 Hz | 13 | off | 100 ms | off |
| [Halls 2](presets/halls-2/) | [Concert A](presets/halls-2/concert-a.md) | 2 s | 18 | 64 ms | 3 | 4 | 4 | 5200 Hz | 0.7 | 3600 Hz | 1.6 | 1000 Hz | -9 dB | 18/20 | 8800 Hz | 25 | off | 100 ms | off |
| [Halls 2](presets/halls-2/) | [Concert B](presets/halls-2/concert-b.md) | 1.9 s | 15 | 26 ms | 6 | 1 | 2 | 4800 Hz | 0.7 | 3600 Hz | 1.6 | 1000 Hz | -9 dB | 20/20 | 8800 Hz | 19 | off | 100 ms | off |
| [Halls 2](presets/halls-2/) | [Live Hall](presets/halls-2/live-hall.md) | 2.6 s | 20 | 0 ms | 4 | 5 | 3 | 3200 Hz | 0.7 | 2800 Hz | 1.2 | 720 Hz | -10 dB | 20/20 | 11200 Hz | 23 | -15 dB | 300 ms | 7 |
| [Halls 2](presets/halls-2/) | [Koncert Piano](presets/halls-2/koncert-piano.md) | 2 s | 18 | 24 ms | 3 | 4 | 2 | 4800 Hz | 0.7 | 2800 Hz | 1.4 | 800 Hz | -10 dB | 18/20 | 8800 Hz | 17 | -20 dB | 236 ms | off |
| [Plates 2](presets/plates-2/) | [Plate A](presets/plates-2/plate-a.md) | 2 s | 1 | 0 ms | 8 | 7 | 5 | 10000 Hz | 0.8 | 6400 Hz | 0.7 | 1200 Hz | -10 dB | 17/20 | 12400 Hz | 9 | off | 100 ms | off |
| [Plates 2](presets/plates-2/) | [Small Plate](presets/plates-2/small-plate.md) | 1.5 s | 3 | 0 ms | 6 | 7 | 2 | 8800 Hz | 0.9 | 2800 Hz | 1.05 | 400 Hz | -9 dB | 20/19 | 10000 Hz | 9 | off | 100 ms | off |
| [Plates 2](presets/plates-2/) | [Snare Plate](presets/plates-2/snare-plate.md) | 1.2 s | 3 | 20 ms | 6 | 9 | 4 | 9200 Hz | 1.0 | 4800 Hz | 0.8 | 640 Hz | -13 dB | 20/19 | 10000 Hz | 11 | off | 100 ms | off |
| [Plates 2](presets/plates-2/) | [Dark Plate](presets/plates-2/dark-plate.md) | 2 s | 5 | 0 ms | 7 | 8 | 2 | 3600 Hz | 1.0 | 3200 Hz | 1.1 | 280 Hz | -9 dB | 17/20 | 8800 Hz | 8 | off | 100 ms | off |
| [Plates 2](presets/plates-2/) | [Rich Plate A](presets/plates-2/rich-plate-a.md) | 2 s | 3 | 0 ms | 9 | 6 | 4 | 7200 Hz | 0.7 | 7200 Hz | 0.9 | 640 Hz | -17 dB | 13/20 | 8400 Hz | 8 | off | 100 ms | off |
| [Plates 2](presets/plates-2/) | [Rich Plate B](presets/plates-2/rich-plate-b.md) | 2 s | 3 | 0 ms | 9 | 4 | off | 7200 Hz | 0.7 | 6400 Hz | 0.9 | 640 Hz | -17 dB | 18/20 | 10800 Hz | 20 | off | 100 ms | off |
| [Plates 2](presets/plates-2/) | [Thin Plate](presets/plates-2/thin-plate.md) | 1.4 s | 4 | 0 ms | 7 | 6 | off | 17600 Hz | 0.9 | 8000 Hz | 0.6 | 640 Hz | -20 dB | 16/20 | full | 9 | off | 100 ms | off |
| [Plates 2](presets/plates-2/) | [Vocal Plate A](presets/plates-2/vocal-plate-a.md) | 1.7 s | 6 | 30 ms | 8 | 5 | 6 | 8800 Hz | 0.9 | 4800 Hz | 0.9 | 640 Hz | -15 dB | 18/20 | 14800 Hz | 8 | off | 100 ms | off |
| [Plates 2](presets/plates-2/) | [Vocal Plate B](presets/plates-2/vocal-plate-b.md) | 1.5 s | 10 | 20 ms | 6 | 6 | 6 | 6400 Hz | 0.9 | 2000 Hz | 0.85 | 280 Hz | -14 dB | 18/20 | 10800 Hz | 8 | -10 dB | 276 ms | low |
| [Plates 2](presets/plates-2/) | [Drum Plate](presets/plates-2/drum-plate.md) | 1.35 s | 5 | 0 ms | 5 | 8 | 1 | 6800 Hz | 0.9 | 2800 Hz | 1.05 | 320 Hz | -12 dB | 20/19 | 10400 Hz | 9 | -18 dB | 196 ms | off |
| [Plates 2](presets/plates-2/) | [Large Plate](presets/plates-2/large-plate.md) | 2.2 s | 5 | 0 ms | 6 | 7 | 1 | 7200 Hz | 0.9 | 2400 Hz | 1.2 | 720 Hz | -10 dB | 20/19 | 12000 Hz | 9 | off | 100 ms | off |
| [Plates 2](presets/plates-2/) | [Fat Plate](presets/plates-2/fat-plate.md) | 0.95 s | 10 | 0 ms | 5 | 8 | 8 | 5200 Hz | 0.9 | 3200 Hz | 1.5 | 1000 Hz | -2 dB | 20/20 | 7600 Hz | 5 | -15 dB | 204 ms | 3 |
| [Plates 2](presets/plates-2/) | [Alpha Plate](presets/plates-2/alpha-plate.md) | 1.9 s | 7 | 0 ms | 8 | 6 | off | 6800 Hz | 0.75 | 3200 Hz | 1 | 800 Hz | -14 dB | 20/16 | 10800 Hz | 15 | off | 100 ms | off |
| [Plates 2](presets/plates-2/) | [Vocal Shimmer](presets/plates-2/vocal-shimmer.md) | 1.8 s | 18 | 20 ms | 9 | 5 | 2 | 8000 Hz | 0.9 | 3600 Hz | 0.9 | 720 Hz | -14 dB | 18/20 | 9600 Hz | 8 | -10 dB | 236 ms | 5 |
| [Rooms 2](presets/rooms-2/) | [Music Club](presets/rooms-2/music-club.md) | 1.05 s | 8 | 0 ms | 7 | 6 | 6 | 5200 Hz | 0.75 | 3200 Hz | 1.05 | 1000 Hz | -16 dB | 9/20 | 3200 Hz | 20 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Large Room](presets/rooms-2/large-room.md) | 0.7 s | 7 | 0 ms | 7 | 5 | low | 4800 Hz | 0.75 | 3200 Hz | 1.1 | 720 Hz | -9 dB | 18/20 | 6800 Hz | 10 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Med Room](presets/rooms-2/med-room.md) | 0.55 s | 6 | 0 ms | 4 | 6 | 2 | 5200 Hz | 0.75 | 2800 Hz | 1.2 | 720 Hz | -9 dB | 18/20 | 5600 Hz | 8 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Small Room](presets/rooms-2/small-room.md) | 0.4 s | small | 0 ms | 3 | 6 | 1 | 5200 Hz | 0.6 | 2800 Hz | 1.05 | 280 Hz | -7 dB | 17/20 | 10400 Hz | 6 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Lg Wood Room](presets/rooms-2/lg-wood-room.md) | 1.2 s | 6 | 0 ms | 8 | 6 | 4 | 6000 Hz | 0.75 | 5600 Hz | 0.8 | 1000 Hz | -20 dB | 13/20 | 11200 Hz | 21 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Sm Wood Room](presets/rooms-2/sm-wood-room.md) | 0.8 s | 4 | 10 ms | 1 | 5 | off | 4800 Hz | 0.75 | 4000 Hz | 0.8 | 1800 Hz | -18 dB | 11/20 | 3200 Hz | 10 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Large Chamber](presets/rooms-2/large-chamber.md) | 2 s | 6 | 10 ms | 3 | 6 | 5 | 4800 Hz | 0.9 | 2800 Hz | 0.9 | 280 Hz | -15 dB | 20/18 | 8000 Hz | 9 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Small Chamber](presets/rooms-2/small-chamber.md) | 1.5 s | 3 | 6 ms | 4 | 6 | 4 | 5200 Hz | 0.9 | 3200 Hz | 0.9 | 320 Hz | -15 dB | 18/20 | 8800 Hz | 4 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Bright Chamber](presets/rooms-2/bright-chamber.md) | 1.85 s | 5 | 10 ms | 4 | 7 | 5 | 5600 Hz | 0.9 | 5600 Hz | 0.8 | 640 Hz | -12 dB | 20/18 | 10400 Hz | 9 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Tiled Room](presets/rooms-2/tiled-room.md) | 1.1 s | 4 | 10 ms | 7 | 7 | 1 | 6400 Hz | 0.8 | 5600 Hz | 0.85 | 1000 Hz | -15 dB | 20/20 | 11600 Hz | 10 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Fat Chamber](presets/rooms-2/fat-chamber.md) | 1.35 s | 5 | 10 ms | 9 | 10 | 8 | 2800 Hz | 0.75 | 3600 Hz | 1.5 | 120 Hz | -4 dB | 17/20 | 17200 Hz | 11 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Studio 1](presets/rooms-2/studio-1.md) | 0.75 s | small | 0 ms | 5 | 10 | off | 8400 Hz | 0.6 | 6400 Hz | 0.9 | 1200 Hz | -3 dB | 20/16 | 14000 Hz | 11 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Studio 2](presets/rooms-2/studio-2.md) | 0.6 s | 3 | 0 ms | 5 | 7 | off | 6800 Hz | 0.8 | 5600 Hz | 0.9 | 1200 Hz | -3 dB | 16/20 | 10000 Hz | 5 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Studio 3](presets/rooms-2/studio-3.md) | 0.7 s | 4 | 0 ms | 6 | 7 | 5 | 5200 Hz | 0.7 | 2800 Hz | 1.2 | 560 Hz | 0 dB | 20/16 | 2800 Hz | 7 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Studio 4](presets/rooms-2/studio-4.md) | 1.05 s | 3 | 0 ms | 1 | 7 | off | 4800 Hz | 0.7 | 2800 Hz | 1.5 | 320 Hz | 0 dB | 20/17 | 9600 Hz | 8 | off | 100 ms | off |
| [Rooms 2](presets/rooms-2/) | [Guitar Room](presets/rooms-2/guitar-room.md) | 1.2 s | 18 | 0 ms | 3 | 4 | 2 | 5200 Hz | 0.75 | 3200 Hz | 1.05 | 640 Hz | -11 dB | 20/20 | 9600 Hz | 25 | -14 dB | 300 ms | 4 |
| [Rooms 2](presets/rooms-2/) | [Marble Room](presets/rooms-2/marble-room.md) | 1.3 s | 3 | 0 ms | 2 | 8 | 3 | 6000 Hz | 0.85 | 3600 Hz | 1.15 | 360 Hz | -11 dB | 20/20 | 10000 Hz | 22 | -16 dB | 180 ms | off |
| [Rooms 2](presets/rooms-2/) | [Deep Chamber](presets/rooms-2/deep-chamber.md) | 1.9 s | 10 | 10 ms | 3 | 6 | 3 | 4400 Hz | 0.85 | 2800 Hz | 1 | 320 Hz | -14 dB | 19/20 | 8800 Hz | 9 | -17 dB | 364 ms | off |
| [Rooms 2](presets/rooms-2/) | [Dark Chamber](presets/rooms-2/dark-chamber.md) | 2 s | 9 | 10 ms | 2 | 7 | 3 | 3600 Hz | 0.8 | 2000 Hz | 1.05 | 360 Hz | -12 dB | 18/20 | 3600 Hz | 12 | -17 dB | 284 ms | off |
| [Rooms 2](presets/rooms-2/) | [Vocal Chamber](presets/rooms-2/vocal-chamber.md) | 1.7 s | 16 | 20 ms | 8 | 6 | 7 | 6800 Hz | 0.9 | 2800 Hz | 1 | 720 Hz | -17 dB | 18/20 | 12800 Hz | 4 | -17 dB | 340 ms | 8 |
| [Rooms 2](presets/rooms-2/) | [Wide Room](presets/rooms-2/wide-room.md) | 1 s | 15 | 0 ms | 4 | 4 | 3 | 4000 Hz | 0.7 | 3600 Hz | 1.05 | 560 Hz | -12 dB | 20/17 | 10000 Hz | 15 | -18 dB | 180 ms | 1 |
| [Rooms 2](presets/rooms-2/) | [Lush Room](presets/rooms-2/lush-room.md) | 0.9 s | 25 | 0 ms | 5 | 3 | 3 | 4000 Hz | 0.8 | 3200 Hz | 1.05 | 360 Hz | -10 dB | 20/20 | 6000 Hz | 19 | -11 dB | 204 ms | 6 |
| [Spaces 2](presets/spaces-2/) | [Open Space](presets/spaces-2/open-space.md) | 2.1 s | 27 | 180 ms | 1 | 0 | low | 1800 Hz | 0.7 | 2000 Hz | 1 | 800 Hz | -14 dB | 20/15 | 1800 Hz | 24 | -14 dB | 500 ms | off |
| [Spaces 2](presets/spaces-2/) | [Med Space](presets/spaces-2/med-space.md) | 1.4 s | 10 | 0 ms | 0 | 2 | off | 2800 Hz | 0.7 | 3600 Hz | 0.95 | 480 Hz | -10 dB | 20/14 | 10000 Hz | 7 | off | 100 ms | off |
| [Spaces 2](presets/spaces-2/) | [Small Space](presets/spaces-2/small-space.md) | 0.6 s | 4 | 0 ms | 0 | 2 | off | 2800 Hz | 0.7 | 3600 Hz | 0.8 | 360 Hz | -10 dB | 20/15 | 10000 Hz | 4 | off | 100 ms | off |
| [Spaces 2](presets/spaces-2/) | [Vox Ambience](presets/spaces-2/vox-ambience.md) | 1.7 s | 20 | 0 ms | 6 | 4 | 2 | 6800 Hz | 0.8 | 3200 Hz | 0.9 | 200 Hz | -13 dB | 18/20 | 8000 Hz | 12 | -17 dB | 252 ms | off |
| [Spaces 2](presets/spaces-2/) | [Big Bottom](presets/spaces-2/big-bottom.md) | 1.45 s | 25 | 0 ms | 3 | 5 | 3 | 6800 Hz | 0.7 | 4800 Hz | 4 | 400 Hz | 0 dB | 9/20 | 10000 Hz | 18 | off | 100 ms | off |
| [Spaces 2](presets/spaces-2/) | [Cathedral](presets/spaces-2/cathedral.md) | 5.5 s | 13 | 0 ms | 3 | 6 | 1 | 4000 Hz | 0.7 | 1000 Hz | 1.1 | 280 Hz | -12 dB | 16/20 | 17200 Hz | 15 | -20 dB | 500 ms | low |
| [Spaces 2](presets/spaces-2/) | [Grand Stage](presets/spaces-2/grand-stage.md) | 2.45 s | 1 | 0 ms | 2 | 6 | low | 4800 Hz | 0.8 | 2400 Hz | 1.2 | 1400 Hz | -4 dB | 20/19 | 6000 Hz | 2 | off | 100 ms | off |
| [Spaces 2](presets/spaces-2/) | [Lush Church](presets/spaces-2/lush-church.md) | 5 s | 17 | 0 ms | 3 | 1 | 7 | 4000 Hz | 0.65 | 2800 Hz | 1.15 | 280 Hz | -12 dB | 18/20 | 11600 Hz | 24 | off | 100 ms | off |
| [Spaces 2](presets/spaces-2/) | [Grand Church](presets/spaces-2/grand-church.md) | 5 s | 10 | 0 ms | 3 | 2 | 3 | 4000 Hz | 0.6 | 2800 Hz | 0.7 | 160 Hz | -13 dB | 18/20 | 10800 Hz | 14 | off | 100 ms | off |
| [Spaces 2](presets/spaces-2/) | [Concert Wave](presets/spaces-2/concert-wave.md) | 5 s | 14 | 0 ms | 3 | 1 | 3 | 3200 Hz | 0.7 | 2400 Hz | 1.15 | 720 Hz | -12 dB | 18/20 | 9600 Hz | 24 | -15 dB | 692 ms | off |
| [Spaces 2](presets/spaces-2/) | [Long Vox Space](presets/spaces-2/long-vox-space.md) | 2.4 s | 12 | 0 ms | 4 | 3 | 5 | 7200 Hz | 0.6 | 5600 Hz | 0.5 | 2000 Hz | -20 dB | 0/20 | 14800 Hz | 31 | off | 100 ms | off |
| [Spaces 2](presets/spaces-2/) | [Dark Warm Room](presets/spaces-2/dark-warm-room.md) | 1 s | 15 | 10 ms | 4 | 6 | 3 | 3600 Hz | 0.7 | 3200 Hz | 1.3 | 480 Hz | -10 dB | 19/20 | 2400 Hz | 11 | -18 dB | 204 ms | 3 |
| [Spaces 2](presets/spaces-2/) | [Live Room](presets/spaces-2/live-room.md) | 1.5 s | 20 | 10 ms | 3 | 5 | 4 | 4000 Hz | 0.9 | 4800 Hz | 1 | 560 Hz | -15 dB | 20/18 | 12000 Hz | 22 | -13 dB | 244 ms | 7 |
| [Spaces 2](presets/spaces-2/) | [Shimmering Sky](presets/spaces-2/shimmering-sky.md) | 8.4 s | 28 | 0 ms | 6 | 4 | 6 | 3600 Hz | 0.7 | 2400 Hz | 1.25 | 720 Hz | -6 dB | 18/20 | 9600 Hz | 22 | -12 dB | 660 ms | 3 |
| [Spaces 2](presets/spaces-2/) | [Oak Ballroom](presets/spaces-2/oak-ballroom.md) | 7 s | large | 0 ms | 2 | 4 | 4 | 2000 Hz | 0.6 | 2400 Hz | 2.1 | 360 Hz | -5 dB | 18/20 | 7600 Hz | 27 | -12 dB | 676 ms | 3 |
| [Spaces 2](presets/spaces-2/) | [Ice House](presets/spaces-2/ice-house.md) | 8 s | 25 | 0 ms | 10 | 4 | 4 | 7600 Hz | 1.0 | 5600 Hz | 0.5 | 640 Hz | -4 dB | 20/20 | 10000 Hz | 20 | -12 dB | 660 ms | 4 |
| [Spaces 2](presets/spaces-2/) | [Ice Beads](presets/spaces-2/ice-beads.md) | 5.5 s | 20 | 24 ms | 8 | 6 | 7 | 16000 Hz | 1.0 | 9600 Hz | 0.2 | 3200 Hz | -20 dB | 0/20 | 11600 Hz | 16 | off | 100 ms | off |
| [Spaces 2](presets/spaces-2/) | [Music Forest](presets/spaces-2/music-forest.md) | 2.6 s | large | 34 ms | 0 | 0 | 1 | 2000 Hz | 0.7 | 2000 Hz | 1.25 | 800 Hz | -6 dB | 20/15 | 2800 Hz | 31 | -14 dB | 100 ms | off |
| [Spaces 2](presets/spaces-2/) | [Waving Bloom](presets/spaces-2/waving-bloom.md) | 5.8 s | large | 236 ms | 0 | 0 | low | 1800 Hz | 0.2 | 2000 Hz | 1 | 240 Hz | -20 dB | 20/15 | 6400 Hz | 31 | -6 dB | 780 ms | off |
| [Spaces 2](presets/spaces-2/) | [Brick Chamber](presets/spaces-2/brick-chamber.md) | 0.7 s | 21 | 0 ms | 8 | 2 | 1 | 7600 Hz | 0.2 | 9600 Hz | 1.5 | 1200 Hz | -18 dB | 10/20 | 12000 Hz | 29 | off | 100 ms | off |
| [NonLin](presets/nonlin/) | [NonLin A](presets/nonlin/nonlin-a.md) | 0.2 s | 7 | 0 ms | 0 | 0 | off | 6000 Hz | 0.2 | 200 Hz | 0.2 | 80 Hz | -20 dB | 0/20 | 6000 Hz | 0 | off | 100 ms | off |
| [NonLin](presets/nonlin/) | [NonLin B](presets/nonlin/nonlin-b.md) | 0.2 s | 5 | 0 ms | 0 | 0 | off | 6400 Hz | 0.2 | 200 Hz | 0.2 | 80 Hz | -20 dB | 17/20 | 8000 Hz | 9 | off | 100 ms | off |
| [NonLin](presets/nonlin/) | [NonLin C](presets/nonlin/nonlin-c.md) | 0.2 s | 10 | 0 ms | 0 | 0 | off | 4800 Hz | 0.2 | 200 Hz | 0.2 | 80 Hz | -20 dB | 15/20 | 8400 Hz | 20 | off | 100 ms | off |
| [NonLin](presets/nonlin/) | [NonLin D](presets/nonlin/nonlin-d.md) | 0.2 s | 10 | 0 ms | 0 | 0 | off | 8000 Hz | 0.2 | 200 Hz | 0.2 | 80 Hz | -20 dB | 20/16 | 6400 Hz | 23 | off | 100 ms | off |

## Decoder sources

| Parameter | Offsets | Encoding | Kind |
|-----------|---------|----------|------|
| [reverb time](bytes/reverb-time.md) | 100-101 | `nibble_hilo` | table |
| [size](bytes/size.md) | 102-103 | `nibble_hilo` | affine |
| [predelay](bytes/predelay.md) | 104-105 | `nibble_hilo` | table |
| [diffusion](bytes/diffusion.md) | 107 | `raw_u8` | affine |
| [density](bytes/density.md) | 109 | `raw_u8` | affine |
| [modulation](bytes/modulation.md) | 111 | `raw_u8` | affine |
| [rolloff](bytes/rolloff.md) | 112-113 | `nibble_hilo` | table |
| [hf rt multiply](bytes/hf-rt-multiply.md) | 114-115 | `nibble_hilo` | affine |
| [hf rt crossover](bytes/hf-rt-crossover.md) | 116-117 | `nibble_hilo` | table |
| [lf rt multiply](bytes/lf-rt-multiply.md) | 118-119 | `nibble_hilo` | table |
| [lf rt crossover](bytes/lf-rt-crossover.md) | 120-121 | `nibble_hilo` | table |
| [vlf cut](bytes/vlf-cut.md) | 122-123 | `nibble_hilo` | affine |
| [early to reverb mix](bytes/early-to-reverb-mix.md) | 124-125 | `nibble_hilo` | affine |
| [early rolloff](bytes/early-rolloff.md) | 126-127 | `nibble_hilo` | table |
| [early select](bytes/early-select.md) | 128-129 | `nibble_hilo` | affine |
| [delay level](bytes/delay-level.md) | 133 | `raw_u8` | affine |
| [delay time](bytes/delay-time.md) | 134-135 | `nibble_hilo` | affine |
| [delay modulation](bytes/delay-modulation.md) | 139 | `raw_u8` | affine |


_Last exported: 2026-07-21_
