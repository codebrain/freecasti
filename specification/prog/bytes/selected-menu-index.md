[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Selected menu index

_Generated 2026-07-22. Menu-navigation captures under `sysex/prog/menus/` (one capture per highlighted menu)._

## SysEx summary

- **Offsets:** 98–99
- **Encoding:** `nibble_hilo`
- **Confidence:** high
- **Role:** Front-panel menu position (`nibble_hilo`, 0–17) while a parameter menu is open; `00 00` when idle
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Offsets **98–99** carry the highlighted front-panel menu as a `nibble_hilo` index matching the hardware menu order (identical to the catalog order below). UI state, not a program property. Reverb Time is index 0, so an idle dump and a Reverb-Time-highlighted dump both read `00 00` here — disambiguate with [panel mode flag](panel-mode-flag.md) at 92 (`02` = menu open).

## Menu order

| Index | Menu (parameter) |
|------:|------------------|
| 0 | [Reverb Time](reverb-time.md) |
| 1 | [Size](size.md) |
| 2 | [Pre Delay](predelay.md) |
| 3 | [Diffusion](diffusion.md) |
| 4 | [Density](density.md) |
| 5 | [Modulation](modulation.md) |
| 6 | [Rolloff](rolloff.md) |
| 7 | [HF RT Multiply](hf-rt-multiply.md) |
| 8 | [HF RT Crossover](hf-rt-crossover.md) |
| 9 | [LF RT Multiply](lf-rt-multiply.md) |
| 10 | [LF RT Crossover](lf-rt-crossover.md) |
| 11 | [VLF Cut](vlf-cut.md) |
| 12 | [Early/Reverb Mix](early-to-reverb-mix.md) |
| 13 | [Early Rolloff](early-rolloff.md) |
| 14 | [Early Select](early-select.md) |
| 15 | [Delay Level](delay-level.md) |
| 16 | [Delay Time](delay-time.md) |
| 17 | [Delay Modulation](delay-modulation.md) |

## Notes

- The LCD cursor position is separate: [display](display.md) at 146–147.
- Full idle/browse/edit byte tables: [ui-state.md](../ui-state.md).

## Related

- [Program identity](../program-identity.md) — name / bank / slot overview
- [Register captures](../../../sysex/prog/edit/registers/README.md) — hold-EDIT register corpus
- [Owner’s manual notes](../../../docs/manual-notes.md)

_Last exported: 2026-07-22_
