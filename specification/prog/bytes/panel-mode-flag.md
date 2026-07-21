[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Panel mode flag

_Generated 2026-07-22. Menu-navigation captures under `sysex/prog/menus/` and the favorites session under `sysex/prog/favorites/`._

## SysEx summary

- **Offsets:** 92
- **Encoding:** `raw_u8`
- **Confidence:** high
- **Role:** Front-panel screen state at dump time: `00` idle / value edit, `02` parameter menu highlighted, `08` favorites screen shown
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Offset **92** reflects what the front panel was showing when the dump was taken — UI state, not a program property. `00` = program screen (idle or while a value is being edited); `02` = a parameter menu is highlighted (pair with [selected menu index](selected-menu-index.md) at 98–99 and [display](display.md) at 146–147); `08` = the favorites screen is shown. Holding PROG while this reads `08` **commits pending edits into the favorite slot** (see `sysex/prog/favorites/`).

## Encoding map

| Value | Meaning | Witness |
|-------|---------|---------|
| `00` | Idle / value edit on the program screen | `sysex/prog/menus/no menu.syx` |
| `02` | Parameter menu highlighted | `sysex/prog/menus/` (one capture per menu) |
| `08` | Favorites screen shown | `sysex/prog/favorites/` (hold-PROG from the favorites screen) |

## Notes

- Not persistent: leaving the favorites screen drops this back to `00`/`02` while [favorite slot](favorite-slot.md) at 94 keeps the favorite marker.
- Disambiguates Reverb Time (menu index 0) from idle at 98–99.
- Full idle/browse/edit byte tables: [ui-state.md](../ui-state.md).

## Related

- [Program identity](../program-identity.md) — name / bank / slot overview
- [Register captures](../../../sysex/prog/edit/registers/README.md) — hold-EDIT register corpus
- [Owner’s manual notes](../../../docs/manual-notes.md)

_Last exported: 2026-07-22_
