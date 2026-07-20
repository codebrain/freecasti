[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Bank index

_Generated 2026-07-20. Factory presets under `sysex/prog/presets/` (222 dumps), hold-EDIT captures, and the Bricasti MIDI app notes bank table._

## SysEx summary

- **Offsets:** 88–89 (mirror at 137)
- **Encoding:** `nibble_hilo`
- **Confidence:** high
- **Role:** Program bank of the running program (`nibble_hilo`); hold-EDIT sends always use **11** here while mirror **137** keeps the source bank
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Offsets **88–89** carry the program bank as a `nibble_hilo` word (high nibble at 88). Factory banks are 0–10 in preset-list order; the MIDI app notes add receive-side banks 118–120. Offset **137** mirrors the bank's low nibble and, on hold-EDIT sends (bank word = 11), still carries the **source** bank. Favorite-loaded PROG dumps carry the source program's bank here — never the Favorites bank 119 (see [favorite slot](favorite-slot.md)). Full identity walkthrough: [program identity](../program-identity.md).

## Encoding map

| Bank | Bytes 88–89 (low nibble) | Decoded | Source |
|------|--------------------------|--------:|--------|
| Halls | `00` | 0 | dump/manual |
| Plates | `01` | 1 | dump/manual |
| Rooms | `02` | 2 | dump/manual |
| Chambers | `03` | 3 | dump/manual |
| Ambience | `04` | 4 | dump/manual |
| Spaces | `05` | 5 | dump/manual |
| Halls 2 | `06` | 6 | dump/manual |
| Plates 2 | `07` | 7 | dump/manual |
| Rooms 2 | `08` | 8 | dump/manual |
| Spaces 2 | `09` | 9 | dump/manual |
| NonLin | `0A` | 10 | dump/manual |
| Edit | `0B` | 11 | dump/manual |
| Edit (receive) | `76` | 118 | dump/manual |
| Favorites | `77` | 119 | dump/manual |
| Registers | `78` | 120 | dump/manual |

## Notes

- Banks 118–120 are **receive-side** (MIDI app notes): they never appear at 88–89 in dumps sent by the unit.
- Mirror **137** equals the bank low nibble on PROG frames and the source bank on hold-EDIT frames (`sysex/prog/edit/`).

## Related

- [Program identity](../program-identity.md) — name / bank / slot overview
- [Register captures](../../../sysex/prog/edit/registers/README.md) — hold-EDIT register corpus
- [Owner’s manual notes](../../../docs/manual-notes.md)

_Last exported: 2026-07-20_
