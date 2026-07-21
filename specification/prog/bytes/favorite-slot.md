[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Favorite slot

_Generated 2026-07-21. Favorites captures under `sysex/prog/favorites/` (Deep Ambience and Nonlin C sessions)._

## SysEx summary

- **Offsets:** 94
- **Encoding:** `raw_u8`
- **Confidence:** high
- **Role:** Favorite-source slot: `(slot - 1) * 2` for favorites 1–4 on PROG frames; `08` = not loaded from a favorite
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

When the running program was loaded from one of the four front-panel **favorite** shortcut slots, hold-PROG dumps carry the source slot at offset **94** as `(slot - 1) * 2` (`00`/`02`/`04`/`06`). The marker **persists across edits and panel-mode changes** — it survives dirtying the program and leaving the favorites screen. Every other witnessed program dump (factory presets, parameter series, register bases, and all hold-EDIT frames, which always use bank word 11) reads `08`, previously misread as a structure/version constant. Favorite-loaded PROG dumps otherwise carry the **source program identity** at 88–91 (never the MIDI-notes Favorites bank 119, which applies to receive only). The favorites **screen** state is flagged separately at offset 92 (panel-mode flag, `08` = favorites screen displayed).

## Encoding map

Witness sources: favorite-loaded hold-PROG dumps (`sysex/prog/favorites/`), all four slots.

| Label | Offset 94 | Decoded | Source |
|-------|-----------|--------:|--------|
| Favorite 1 | `00` | 0 | dump |
| Favorite 2 | `02` | 2 | dump |
| Favorite 3 | `04` | 4 | dump |
| Favorite 4 | `06` | 6 | dump |
| not from a favorite | `08` | 8 | dump (entire factory corpus) |

## Notes

- Hold-EDIT dumps always read `08` here regardless of basis; the favorite marker appears on PROG frames only.
- Favorites auto-commit pending edits on hold-PROG from the favorites screen — see [register basis blob](register-basis-blob.md) (Favorites carve-out) and `sysex/prog/favorites/README.md`.

## Related

- [Program identity](../program-identity.md) — name / bank / slot overview
- [Register captures](../../../sysex/prog/edit/registers/README.md) — hold-EDIT register corpus
- [Owner’s manual notes](../../../docs/manual-notes.md)

_Last exported: 2026-07-21_
