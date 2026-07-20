[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Engine/bank-class flag

_Generated 2026-07-20. Corpus scan of all factory presets under `sysex/prog/presets/`._

## SysEx summary

- **Offsets:** 130 (companion 131–132)
- **Encoding:** `raw_u8`
- **Confidence:** medium
- **Role:** Engine/bank class: `0` classic V1 banks, `1` the V2 `* 2` banks, `2` NonLin
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Offset **130** selects the engine/bank class of the running program: `0` on the classic banks (Halls…Spaces, V1 algorithm), `1` on the `* 2` banks (Halls 2…Spaces 2, V2 algorithm), `2` on NonLin. Most parameter-series dumps read `1` (captured from Large Church, Halls 2); the LF RT multiply/crossover series read `0` (Large Hall). The companion bytes **131–132** are fixed at `02 00` across this corpus. Distinct from the [algorithm/family flag](algorithm-family-flag.md) at 97/145.

## Encoding map

| Value | Banks | Algorithm |
|------:|-------|-----------|
| `0` | Halls, Plates, Rooms, Chambers, Ambience, Spaces | V1 |
| `1` | Halls 2, Plates 2, Rooms 2, Spaces 2 | V2 |
| `2` | NonLin | Non-linear (AMS-style) |

## Notes

- Bank identity itself is at [bank index](bank-index.md) (88–89 / mirror 137).
- Manual context (V1 vs V2, NonLin engine): [manual-notes.md](../../../docs/manual-notes.md).

## Related

- [Program identity](../program-identity.md) — name / bank / slot overview
- [Register captures](../../../sysex/prog/edit/registers/README.md) — hold-EDIT register corpus
- [Owner’s manual notes](../../../docs/manual-notes.md)

_Last exported: 2026-07-20_
