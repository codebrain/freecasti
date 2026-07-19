[Overview](README.md) | [Bytes](bytes/README.md) | [Program identity](program-identity.md) | [Preset inventory](preset-inventory.md) | **Preset sheet** | [Byte map](byte-map-overview.md) | [Cross-series](cross.md) | [System dumps](../system/README.md)

# Preset sheet errata

_Generated 2026-07-19. Comparing decoded `sysex/prog/presets/` dumps to [Bricasti's published preset sheet](https://www.bricasti.com/images/preset_sheet.pdf) (parsed data: `docs/reference/preset_sheet.json`)._

The classic PDF covers **V1-era banks only** (Ambience, Chambers, Halls, Plates, Rooms, Spaces). V2 banks (Halls 2, Plates 2, Rooms 2, Spaces 2), NonLin, and many later factory presets are **not on the sheet** — see [preset-inventory.md](preset-inventory.md) for the full capture list.

**Sheet presets:** 119 (Ambience=15, Chambers=16, Halls=23, Plates=20, Rooms=30, Spaces=15)

**Dumps:** 222 matched 98 (exact 87, soft-only 3, hard 8)

Hard = sheet value disagrees with the SysEx dump beyond tolerance. Soft = modest drift (often print rounding on Hz tables) once hardware UI walks densify the decode maps. SysEx dumps are treated as authoritative when they conflict with the PDF. Dump labels come from the densified encoding map (series captures, `provided` UI walks, and sheet anchors); `~` only when an encoding falls between labeled steps.

See also [program-identity.md](program-identity.md), [presets/](presets/), and [bytes/README.md](bytes/README.md).

## Hard discrepancies by parameter

| Parameter | Presets |
|-----------|--------:|
| [early select](bytes/early-select.md) | 4 |
| [hf rt crossover](bytes/hf-rt-crossover.md) | 2 |
| [diffusion](bytes/diffusion.md) | 1 |
| [early rolloff](bytes/early-rolloff.md) | 1 |
| [predelay](bytes/predelay.md) | 1 |

## Soft discrepancies by parameter (table / rounding)

| Parameter | Presets |
|-----------|--------:|
| [rolloff](bytes/rolloff.md) | 3 |

## Hard discrepancies

| Bank | Preset | Parameter | Encoded | Dump | Sheet | Δ |
|------|--------|-----------|--------:|------|------:|--:|
| [Halls](presets/halls/) | [Large & Near](presets/halls/large-and-near.md) | [early select](bytes/early-select.md) | 14 | 14 | 20 | -6 |
| [Halls](presets/halls/) | [Large Hall](presets/halls/large-hall.md) | [early select](bytes/early-select.md) | 13 | 13 | 17 | -4 |
| [Halls](presets/halls/) | [Medium & Near](presets/halls/medium-and-near.md) | [hf rt crossover](bytes/hf-rt-crossover.md) | 20 | 3600 Hz | 4800 | -1200 |
| [Halls](presets/halls/) | [Medium Hall](presets/halls/medium-hall.md) | [hf rt crossover](bytes/hf-rt-crossover.md) | 20 | 3600 Hz | 4800 | -1200 |
| [Halls](presets/halls/) | [Medium Hall](presets/halls/medium-hall.md) | [early select](bytes/early-select.md) | 17 | 17 | 13 | 4 |
| [Rooms](presets/rooms/) | [Large Tiled](presets/rooms/large-tiled.md) | [early rolloff](bytes/early-rolloff.md) | 54 | 16000 Hz | 1600 | 14400 |
| [Spaces](presets/spaces/) | [Bath House](presets/spaces/bath-house.md) | [early select](bytes/early-select.md) | 19 | 19 | 25 | -6 |
| [Spaces](presets/spaces/) | [Redwood Valley](presets/spaces/redwood-valley.md) | [predelay](bytes/predelay.md) | 50 | 220 ms | 100 | 120 |
| [Spaces](presets/spaces/) | [Stone Quarry](presets/spaces/stone-quarry.md) | [diffusion](bytes/diffusion.md) | 2 | 2 | 1 | 1 |

## Soft discrepancies (table / rounding)

| Bank | Preset | Parameter | Encoded | Dump | Sheet | Δ |
|------|--------|-----------|--------:|------|------:|--:|
| [Chambers](presets/chambers/) | [Kick Chamber](presets/chambers/kick-chamber.md) | [rolloff](bytes/rolloff.md) | 28 | 5600 Hz | 6400 | -800 |
| [Plates](presets/plates/) | [Bright Plate](presets/plates/bright-plate.md) | [rolloff](bytes/rolloff.md) | 30 | 6400 Hz | 7600 | -1200 |
| [Plates](presets/plates/) | [London Plate](presets/plates/london-plate.md) | [rolloff](bytes/rolloff.md) | 25 | 4400 Hz | 5200 | -800 |

## Dumps not on the sheet

These factory dumps are in `sysex/prog/presets/` but have no row on the classic PDF (likely later additions):

- [Ambience](presets/ambience/) / [Heavy Ambience](presets/ambience/heavy-ambience.md)
- [Ambience](presets/ambience/) / [Med & Bright](presets/ambience/med-and-bright.md)
- [Ambience](presets/ambience/) / [Med Ambience](presets/ambience/med-ambience.md)
- [Ambience](presets/ambience/) / [Small Ambience](presets/ambience/small-ambience.md)
- [Chambers](presets/chambers/) / [A&M Chamber B](presets/chambers/a-and-m-chamber-b.md)
- [Chambers](presets/chambers/) / [Echo Chamber](presets/chambers/echo-chamber.md)
- [Chambers](presets/chambers/) / [Fat Chamber](presets/chambers/fat-chamber.md)
- [Chambers](presets/chambers/) / [Large & Dark](presets/chambers/large-and-dark.md)
- [Chambers](presets/chambers/) / [Small & Bright](presets/chambers/small-and-bright.md)
- [Chambers](presets/chambers/) / [Small & Dark](presets/chambers/small-and-dark.md)
- [Chambers](presets/chambers/) / [Stone Chamber](presets/chambers/stone-chamber.md)
- [Chambers](presets/chambers/) / [Sunset Chamber](presets/chambers/sunset-chamber.md)
- [Chambers](presets/chambers/) / [Tiled Chamber](presets/chambers/tiled-chamber.md)
- [Chambers](presets/chambers/) / [Vocal Chamber](presets/chambers/vocal-chamber.md)
- [Halls](presets/halls/) / [Mechanics Hall](presets/halls/mechanics-hall.md)
- [Halls](presets/halls/) / [Pepes Hall A](presets/halls/pepes-hall-a.md)
- [Halls](presets/halls/) / [Pepes Hall B](presets/halls/pepes-hall-b.md)
- [Halls](presets/halls/) / [Piano Hall](presets/halls/piano-hall.md)
- [Halls](presets/halls/) / [Reflect Hall A](presets/halls/reflect-hall-a.md)
- [Halls](presets/halls/) / [Reflect Hall B](presets/halls/reflect-hall-b.md)
- [Halls](presets/halls/) / [Saint Gerold](presets/halls/saint-gerold.md)
- [Halls](presets/halls/) / [Saint Sylvain](presets/halls/saint-sylvain.md)
- [Halls](presets/halls/) / [Troy Hall](presets/halls/troy-hall.md)
- [NonLin](presets/nonlin/) / [NonLin A](presets/nonlin/nonlin-a.md)
- [NonLin](presets/nonlin/) / [NonLin B](presets/nonlin/nonlin-b.md)
- [NonLin](presets/nonlin/) / [NonLin C](presets/nonlin/nonlin-c.md)
- [NonLin](presets/nonlin/) / [NonLin D](presets/nonlin/nonlin-d.md)
- [Plates 2](presets/plates-2/) / [Alpha Plate](presets/plates-2/alpha-plate.md)
- [Plates 2](presets/plates-2/) / [Dark Plate](presets/plates-2/dark-plate.md)
- [Plates 2](presets/plates-2/) / [Drum Plate](presets/plates-2/drum-plate.md)
- [Plates 2](presets/plates-2/) / [Fat Plate](presets/plates-2/fat-plate.md)
- [Plates 2](presets/plates-2/) / [Large Plate](presets/plates-2/large-plate.md)
- [Plates 2](presets/plates-2/) / [Plate A](presets/plates-2/plate-a.md)
- [Plates 2](presets/plates-2/) / [Rich Plate A](presets/plates-2/rich-plate-a.md)
- [Plates 2](presets/plates-2/) / [Rich Plate B](presets/plates-2/rich-plate-b.md)
- [Plates 2](presets/plates-2/) / [Small Plate](presets/plates-2/small-plate.md)
- [Plates 2](presets/plates-2/) / [Snare Plate](presets/plates-2/snare-plate.md)
- [Plates 2](presets/plates-2/) / [Thin Plate](presets/plates-2/thin-plate.md)
- [Plates 2](presets/plates-2/) / [Vocal Plate A](presets/plates-2/vocal-plate-a.md)
- [Plates 2](presets/plates-2/) / [Vocal Plate B](presets/plates-2/vocal-plate-b.md)
- [Plates 2](presets/plates-2/) / [Vocal Shimmer](presets/plates-2/vocal-shimmer.md)
- [Plates](presets/plates/) / [Old Plate](presets/plates/old-plate.md)
- [Plates](presets/plates/) / [Repro Plate](presets/plates/repro-plate.md)
- [Plates](presets/plates/) / [Rich Plate](presets/plates/rich-plate.md)
- [Plates](presets/plates/) / [Sun Plate A](presets/plates/sun-plate-a.md)
- [Plates](presets/plates/) / [Sun Plate B](presets/plates/sun-plate-b.md)
- [Plates](presets/plates/) / [Sun Plate C](presets/plates/sun-plate-c.md)
- [Plates](presets/plates/) / [Vocal Plate B](presets/plates/vocal-plate-b.md)
- [Plates](presets/plates/) / [Vocal Plate](presets/plates/vocal-plate.md)
- [Rooms 2](presets/rooms-2/) / [Bright Chamber](presets/rooms-2/bright-chamber.md)
- [Rooms 2](presets/rooms-2/) / [Dark Chamber](presets/rooms-2/dark-chamber.md)
- [Rooms 2](presets/rooms-2/) / [Deep Chamber](presets/rooms-2/deep-chamber.md)
- [Rooms 2](presets/rooms-2/) / [Fat Chamber](presets/rooms-2/fat-chamber.md)
- [Rooms 2](presets/rooms-2/) / [Guitar Room](presets/rooms-2/guitar-room.md)
- [Rooms 2](presets/rooms-2/) / [Large Chamber](presets/rooms-2/large-chamber.md)
- [Rooms 2](presets/rooms-2/) / [Large Room](presets/rooms-2/large-room.md)
- [Rooms 2](presets/rooms-2/) / [Lg Wood Room](presets/rooms-2/lg-wood-room.md)
- [Rooms 2](presets/rooms-2/) / [Lush Room](presets/rooms-2/lush-room.md)
- [Rooms 2](presets/rooms-2/) / [Marble Room](presets/rooms-2/marble-room.md)
- [Rooms 2](presets/rooms-2/) / [Med Room](presets/rooms-2/med-room.md)
- [Rooms 2](presets/rooms-2/) / [Music Club](presets/rooms-2/music-club.md)
- [Rooms 2](presets/rooms-2/) / [Sm Wood Room](presets/rooms-2/sm-wood-room.md)
- [Rooms 2](presets/rooms-2/) / [Small Chamber](presets/rooms-2/small-chamber.md)
- [Rooms 2](presets/rooms-2/) / [Small Room](presets/rooms-2/small-room.md)
- [Rooms 2](presets/rooms-2/) / [Studio 1](presets/rooms-2/studio-1.md)
- [Rooms 2](presets/rooms-2/) / [Studio 2](presets/rooms-2/studio-2.md)
- [Rooms 2](presets/rooms-2/) / [Studio 3](presets/rooms-2/studio-3.md)
- [Rooms 2](presets/rooms-2/) / [Studio 4](presets/rooms-2/studio-4.md)
- [Rooms 2](presets/rooms-2/) / [Tiled Room](presets/rooms-2/tiled-room.md)
- [Rooms 2](presets/rooms-2/) / [Vocal Chamber](presets/rooms-2/vocal-chamber.md)
- [Rooms 2](presets/rooms-2/) / [Wide Room](presets/rooms-2/wide-room.md)
- [Rooms](presets/rooms/) / [Blue Room](presets/rooms/blue-room.md)
- [Rooms](presets/rooms/) / [Corn Room](presets/rooms/corn-room.md)
- [Rooms](presets/rooms/) / [Large Red Room](presets/rooms/large-red-room.md)
- [Rooms](presets/rooms/) / [Long Wood Room](presets/rooms/long-wood-room.md)
- [Rooms](presets/rooms/) / [Medium Tiled](presets/rooms/medium-tiled.md)
- [Rooms](presets/rooms/) / [Oakland Room](presets/rooms/oakland-room.md)
- [Rooms](presets/rooms/) / [Percussion](presets/rooms/percussion.md)
- [Rooms](presets/rooms/) / [Red Room](presets/rooms/red-room.md)
- [Rooms](presets/rooms/) / [SF Perf Room](presets/rooms/sf-perf-room.md)
- [Rooms](presets/rooms/) / [Studio B Close](presets/rooms/studio-b-close.md)
- [Rooms](presets/rooms/) / [Studio K](presets/rooms/studio-k.md)
- [Rooms](presets/rooms/) / [Waits Room](presets/rooms/waits-room.md)
- [Spaces 2](presets/spaces-2/) / [Big Bottom](presets/spaces-2/big-bottom.md)
- [Spaces 2](presets/spaces-2/) / [Brick Chamber](presets/spaces-2/brick-chamber.md)
- [Spaces 2](presets/spaces-2/) / [Cathedral](presets/spaces-2/cathedral.md)
- [Spaces 2](presets/spaces-2/) / [Concert Wave](presets/spaces-2/concert-wave.md)
- [Spaces 2](presets/spaces-2/) / [Dark Warm Room](presets/spaces-2/dark-warm-room.md)
- [Spaces 2](presets/spaces-2/) / [Grand Church](presets/spaces-2/grand-church.md)
- [Spaces 2](presets/spaces-2/) / [Grand Stage](presets/spaces-2/grand-stage.md)
- [Spaces 2](presets/spaces-2/) / [Ice Beads](presets/spaces-2/ice-beads.md)
- [Spaces 2](presets/spaces-2/) / [Ice House](presets/spaces-2/ice-house.md)
- [Spaces 2](presets/spaces-2/) / [Live Room](presets/spaces-2/live-room.md)
- [Spaces 2](presets/spaces-2/) / [Long Vox Space](presets/spaces-2/long-vox-space.md)
- [Spaces 2](presets/spaces-2/) / [Lush Church](presets/spaces-2/lush-church.md)
- [Spaces 2](presets/spaces-2/) / [Med Space](presets/spaces-2/med-space.md)
- [Spaces 2](presets/spaces-2/) / [Music Forest](presets/spaces-2/music-forest.md)
- [Spaces 2](presets/spaces-2/) / [Oak Ballroom](presets/spaces-2/oak-ballroom.md)
- [Spaces 2](presets/spaces-2/) / [Open Space](presets/spaces-2/open-space.md)
- [Spaces 2](presets/spaces-2/) / [Shimmering Sky](presets/spaces-2/shimmering-sky.md)
- [Spaces 2](presets/spaces-2/) / [Small Space](presets/spaces-2/small-space.md)
- [Spaces 2](presets/spaces-2/) / [Vox Ambience](presets/spaces-2/vox-ambience.md)
- [Spaces 2](presets/spaces-2/) / [Waving Bloom](presets/spaces-2/waving-bloom.md)
- [Spaces](presets/spaces/) / [Academy Yard](presets/spaces/academy-yard.md)
- [Spaces](presets/spaces/) / [Cavern](presets/spaces/cavern.md)
- [Spaces](presets/spaces/) / [Europa](presets/spaces/europa.md)
- [Spaces](presets/spaces/) / [Gated Space](presets/spaces/gated-space.md)
- [Spaces](presets/spaces/) / [Hillside](presets/spaces/hillside.md)
- [Spaces](presets/spaces/) / [Reflect Chapel](presets/spaces/reflect-chapel.md)
- [Spaces](presets/spaces/) / [Reflect Church](presets/spaces/reflect-church.md)

## Skipped (bank not on classic sheet)

- [Halls 2](presets/halls-2/) / [Concert A](presets/halls-2/concert-a.md) — not listed as a separate bank on the classic sheet
- [Halls 2](presets/halls-2/) / [Concert B](presets/halls-2/concert-b.md) — not listed as a separate bank on the classic sheet
- [Halls 2](presets/halls-2/) / [Jazz Hall](presets/halls-2/jazz-hall.md) — not listed as a separate bank on the classic sheet
- [Halls 2](presets/halls-2/) / [Koncert Piano](presets/halls-2/koncert-piano.md) — not listed as a separate bank on the classic sheet
- [Halls 2](presets/halls-2/) / [Large & Stage](presets/halls-2/large-and-stage.md) — not listed as a separate bank on the classic sheet
- [Halls 2](presets/halls-2/) / [Large Church](presets/halls-2/large-church.md) — not listed as a separate bank on the classic sheet
- [Halls 2](presets/halls-2/) / [Large Hall](presets/halls-2/large-hall.md) — not listed as a separate bank on the classic sheet
- [Halls 2](presets/halls-2/) / [Live Hall](presets/halls-2/live-hall.md) — not listed as a separate bank on the classic sheet
- [Halls 2](presets/halls-2/) / [Med & Stage](presets/halls-2/med-and-stage.md) — not listed as a separate bank on the classic sheet
- [Halls 2](presets/halls-2/) / [Medium Hall](presets/halls-2/medium-hall.md) — not listed as a separate bank on the classic sheet
- [Halls 2](presets/halls-2/) / [Small & Stage](presets/halls-2/small-and-stage.md) — not listed as a separate bank on the classic sheet
- [Halls 2](presets/halls-2/) / [Small Church](presets/halls-2/small-church.md) — not listed as a separate bank on the classic sheet
- [Halls 2](presets/halls-2/) / [Small Hall](presets/halls-2/small-hall.md) — not listed as a separate bank on the classic sheet
- [Halls 2](presets/halls-2/) / [West Hall](presets/halls-2/west-hall.md) — not listed as a separate bank on the classic sheet

## Notes

- Table parameters densify with hardware UI walks (`provided`) when available; otherwise sheet-derived points fill gaps between capture anchors (series dumps always win on conflict).
- Soft diffs are usually print rounding or off-grid sheet values (especially predelay and Hz fields) once provided walks exist.
- Halls 2 is skipped - the classic PDF has no Halls 2 section.
- SysEx dumps are authoritative when they conflict with the PDF.
- Sheet data: `docs/reference/preset_sheet.json` (json)
- Analysis: `sysex/prog/presets/analysis.json`

_Last exported: 2026-07-19_
