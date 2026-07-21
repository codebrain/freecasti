[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Program slot

_Generated 2026-07-21. Factory presets under `sysex/prog/presets/` (222 dumps, all banks/slots)._

## SysEx summary

- **Offsets:** 90–91
- **Encoding:** `nibble_hilo`
- **Confidence:** high
- **Role:** Program slot within the bank (`nibble_hilo`, preset-list order); stays the *source factory* slot on hold-EDIT dumps
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Offsets **90–91** carry the program's slot within its bank as a `nibble_hilo` word (high nibble at 90), counting from 0 in factory preset-list order. Hold-EDIT dumps keep the source program's slot even though the bank word switches to 11; favorite-loaded PROG dumps carry the source program's slot (see [favorite slot](favorite-slot.md)). Register identity lives elsewhere ([register bank](register-bank.md) / [register](register.md)). Per-bank slot tables: [program identity](../program-identity.md) and [preset inventory](../preset-inventory.md).

## Notes

- Most banks use contiguous slots from 0; **Rooms** runs 0–35 on this unit (more than the published sheet).
- Not a MIDI program-change number — program changes use the bank-select mapping in the MIDI app notes.

## Related

- [Program identity](../program-identity.md) — name / bank / slot overview
- [Register captures](../../../sysex/prog/edit/registers/README.md) — hold-EDIT register corpus
- [Owner’s manual notes](../../../docs/manual-notes.md)

_Last exported: 2026-07-21_
