[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Register bank

_Generated 2026-07-21. Register hold-EDIT captures under `sysex/prog/edit/registers/` (including `fullsweep-rooms-studio-a.syx`)._

## SysEx summary

- **Offsets:** 93
- **Encoding:** `raw_u8`
- **Confidence:** high
- **Role:** Manual **Bank** of the register **loaded as the running basis** (`B0`–`B4` = `00`–`04`); `00` on factory/parameter-series dumps
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

When a **User Register** is loaded as the running program basis, offset **93** stores the register **Bank** (owner's manual: 5 Banks of 10 Registers). Witnessed exhaustively as `00`–`04` in `fullsweep-rooms-studio-a.syx`. A **store alone does not update it**: the delay-edit and rename captures (stored to B1 R1 while the basis remained the factory program) read `00`, while `charset-b1s1-rt5s-stored.syx` reads `01` because B1 R0 was the active basis at dump time. Factory and parameter-series dumps keep this at `00`. Distinct from factory **program bank** at 88–89 / mirror 136–137. Pair with [register](register.md) at offset 95.

## Encoding map

Witness sources: register-basis hold-EDIT dumps (`sysex/prog/edit/registers/`).

| Label | Offset 93 | Decoded | Source |
|-------|-----------|--------:|--------|
| B0 | `00` | 0 | dump |
| B1 | `01` | 1 | dump |
| B2 | `02` | 2 | dump |
| B3 | `03` | 3 | dump |
| B4 | `04` | 4 | dump |

## Notes

- Hold-EDIT dumps use program bank word **11** at 88–89; register identity is only at **93/95**.
- LCD `display` (146–147) does **not** encode Bank/Register (fullsweep stayed at 164).

## Related

- [Program identity](../program-identity.md) — name / bank / slot overview
- [Register captures](../../../sysex/prog/edit/registers/README.md) — hold-EDIT register corpus
- [Owner’s manual notes](../../../docs/manual-notes.md)

_Last exported: 2026-07-21_
