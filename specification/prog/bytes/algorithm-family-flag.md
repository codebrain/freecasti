[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Algorithm/family flag

_Generated 2026-07-21. Corpus scan of all factory presets under `sysex/prog/presets/`._

## SysEx summary

- **Offsets:** 96–97 (mirror at 145)
- **Encoding:** `nibble_hilo`
- **Confidence:** medium
- **Role:** Algorithm/family flag from the factory corpus: Halls all `3`; most other presets `4`, with a few bank-leading exceptions also `3`
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Offsets **96–97** (`nibble_hilo`; high nibble at 96 always `00`) group presets into two families: every Halls preset reads `3`; most other presets read `4`, with a few bank-leading exceptions also at `3` (Chambers Large Chamber, Plates Bright Plate, Rooms Studio A, Halls 2 Large Hall). Offset **145** mirrors it as `0` when the value is `3` and `1` when the value is `4`. It is **not** a clean V1/V2 algorithm bit — the engine class lives at [engine/bank-class flag](engine-bank-class-flag.md) (offset 130). Not a user parameter; no capture series moves it.

## Encoding map

| `nibble_hilo` | Offset 96 | Offset 97 | Mirror 145 | Presets |
|--------------:|----------|----------|-----------:|---------|
| 3 | `00` | `03` | `0` | All Halls; Chambers Large Chamber, Plates Bright Plate, Rooms Studio A, Halls 2 Large Hall |
| 4 | `00` | `04` | `1` | All other factory presets in this corpus |

## Notes

- Background and manual context: [manual-notes.md](../../../docs/manual-notes.md).

## Related

- [Program identity](../program-identity.md) — name / bank / slot overview
- [Register captures](../../../sysex/prog/edit/registers/README.md) — hold-EDIT register corpus
- [Owner’s manual notes](../../../docs/manual-notes.md)

_Last exported: 2026-07-21_
