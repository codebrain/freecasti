[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Program name

_Generated 2026-07-19. Factory presets under `sysex/prog/presets/` plus register hold-EDIT captures._

## SysEx summary

- **Offsets:** 8–21
- **Encoding:** `ascii_space_padded`
- **Confidence:** high
- **Role:** 14-character editable ASCII label (manual); space-padded within this field
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Front-panel / register label text stored as ASCII in the program dump. The owner's manual documents a **14-character** location display when naming a register. Significant glyphs live at offsets **8–21**; trailing pad at **22–23** completes the 16-byte wire window (see [program name pad](program-name-pad.md)). Factory preset dumps also space-pad through offset 87; Reg-backed hold-EDIT dumps reuse 24–87 for the register basis blob instead.

## Encoding map

Space-padded ASCII. Factory corpus: every preset name fits in **14** significant characters (offsets 22–23 always `0x20`).

| Layer | Offsets | Length | Notes |
|-------|---------|-------:|-------|
| Editable label | 8–21 | 14 | Manual rename limit |
| Trailing pad | 22–23 | 2 | Always spaces in this corpus ([program name pad](program-name-pad.md)) |
| Wire window | 8–23 | 16 | SysEx allocation |

## Related

- [Program identity](../program-identity.md) — name / bank / slot overview
- [Register captures](../../../sysex/prog/edit/registers/README.md) — hold-EDIT register corpus
- [Owner’s manual notes](../../../docs/manual-notes.md)

_Last exported: 2026-07-19_
