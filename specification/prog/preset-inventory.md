[Overview](README.md) | [Bytes](bytes/README.md) | [Program identity](program-identity.md) | **Preset inventory** | [Preset sheet](preset-sheet.md) | [Byte map](byte-map-overview.md) | [Cross-series](cross.md) | [System dumps](../system/README.md)
# Preset inventory

_Generated 2026-07-21. Compares `sysex/prog/presets/` captures to the [V2 addendum](https://www.bricasti.com/images/M7_V2_Manual_Addendum_Upgrade.pdf) factory lists and common marketing totals (222 = 134 V1 + 88 V2-tier positions)._

## Corpus counts

| Bank | Dumps | Slot range |
|------|------:|------------|
| [Ambience](presets/ambience/) | 15 | 0–14 |
| [Chambers](presets/chambers/) | 22 | 0–21 |
| [Halls](presets/halls/) | 32 | 0–31 |
| [Halls 2](presets/halls-2/) | 14 | 0–13 |
| [NonLin](presets/nonlin/) | 4 | 0–3 |
| [Plates](presets/plates/) | 24 | 0–23 |
| [Plates 2](presets/plates-2/) | 14 | 0–13 |
| [Rooms](presets/rooms/) | 36 | 0–35 |
| [Rooms 2](presets/rooms-2/) | 22 | 0–21 |
| [Spaces](presets/spaces/) | 19 | 0–18 |
| [Spaces 2](presets/spaces-2/) | 20 | 0–19 |
| **Total** | **222** | |

## vs V2 addendum

| Group | Captured | Addendum |
|-------|--------:|---------:|
| V1 banks (incl. Ambience) | 148 | 138 |
| V2 `* 2` banks | 70 | 70 |
| [NonLin](presets/nonlin/) | 4 | 4 |
| **Grand total** | **222** | **212** |

## Missing captures

Suggested filenames for `sysex/prog/presets/`:

- `Halls 2.Berliner Hall.syx`

## Name diffs (addendum vs unit spelling)

### Halls 2

Addendum names not matched (after alias map):
- Berliner Hall

### Spaces 2

Captured but not in addendum PDF:
- Brick Chamber

## V1 count gaps

- **Rooms**: have 36, addendum 26 (+10)

## Marketing totals (third-party)

Published marketing totals often cite **222** factory presets as **134** V1 + **88** V2-tier program positions. The addendum names **70** programs across the four `* 2` banks; **18** extra positions are unused slots in the 22×4 MIDI bank grid (see below).

| | Captured | Marketing |
|--|--------:|----------:|
| V1 | 148 | 134 |
| V2 tier (named) | 70 | 88 positions |

## V2 bank slot capacity

Rooms 2 uses slots 0–21 → **22** programs per `* 2` bank.

| Bank | Named | Capacity | Slots used | Trailing empty |
|------|------:|---------:|-----------|---------------:|
| [Halls 2](presets/halls-2/) | 14 | 22 | 0–13 | 8 |
| [Plates 2](presets/plates-2/) | 14 | 22 | 0–13 | 8 |
| [Rooms 2](presets/rooms-2/) | 22 | 22 | 0–21 | 0 |
| [Spaces 2](presets/spaces-2/) | 20 | 22 | 0–19 | 2 |

## preset_sheet.json

Classic-bank PDF sheet only (pre-V2). All `* 2` and NonLin dumps, plus newer V1 additions, have no sheet row.

- Sheet rows: **119** ({'Ambience': 15, 'Chambers': 16, 'Halls': 23, 'Plates': 20, 'Rooms': 30, 'Spaces': 15})
- Dumps without sheet row: **103**

_Last exported: 2026-07-21_

