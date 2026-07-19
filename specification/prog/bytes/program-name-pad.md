[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Program name pad

_Generated 2026-07-19. Factory presets under `sysex/prog/presets/` (all dumps) and register fullsweep captures._

## SysEx summary

- **Offsets:** 22–23
- **Encoding:** `raw_bytes`
- **Confidence:** high
- **Role:** Trailing space pad completing the 16-byte wire name window
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Offsets **22–23** are always `0x20` in this corpus. They are not part of the editable 14-character label ([program name](program-name.md)); together with that field they form the 16-byte SysEx name window before the register basis blob / factory space pad at offset 24.

## Encoding map

| Value | Bytes | Source |
|-------|-------|--------|
| space pad | `20 20` | dump (all factory + register captures) |

## Related

- [Program identity](../program-identity.md) — name / bank / slot overview
- [Register captures](../../../sysex/prog/edit/registers/README.md) — hold-EDIT register corpus
- [Owner’s manual notes](../../../docs/manual-notes.md)

_Last exported: 2026-07-19_
