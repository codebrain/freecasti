[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Register

_Generated 2026-07-19. Register hold-EDIT captures under `sysex/prog/edit/registers/` (including `fullsweep-rooms-studio-a.syx`)._

## SysEx summary

- **Offsets:** 95
- **Encoding:** `raw_u8`
- **Confidence:** high
- **Role:** Manual **Register** within a register bank (`0`–`9`); `00` on factory/parameter-series dumps
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

When a **User Register** is the running program basis, offset **95** stores the **Register** number within the bank (owner's manual: 10 registers per bank). Witnessed exhaustively as `00`–`09` in `fullsweep-rooms-studio-a.syx`. Factory and parameter-series dumps keep this at `00`. Distinct from factory **program slot** at 90–91. Pair with [register bank](register-bank.md) at offset 93.

## Encoding map

Witness sources: register-basis hold-EDIT dumps (`sysex/prog/edit/registers/`).

| Label | Offset 95 | Decoded | Source |
|-------|-----------|--------:|--------|
| Register 0 | `00` | 0 | dump |
| Register 1 | `01` | 1 | dump |
| Register 2 | `02` | 2 | dump |
| Register 3 | `03` | 3 | dump |
| Register 4 | `04` | 4 | dump |
| Register 5 | `05` | 5 | dump |
| Register 6 | `06` | 6 | dump |
| Register 7 | `07` | 7 | dump |
| Register 8 | `08` | 8 | dump |
| Register 9 | `09` | 9 | dump |

## Notes

- Filename convention in the corpus: `b0-…/slot-3.syx` means Bank 0, Register 3.
- Reserved offset **96** stays `00` in witnessed captures.

## Related

- [Program identity](../program-identity.md) — name / bank / slot overview
- [Register captures](../../../sysex/prog/edit/registers/README.md) — hold-EDIT register corpus
- [Owner’s manual notes](../../../docs/manual-notes.md)

_Last exported: 2026-07-19_
