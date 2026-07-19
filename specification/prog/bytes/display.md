[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Display

_Generated 2026-07-19. Source folder: `sysex/prog/menus/` (19 captures)._

## SysEx summary

- **Offsets:** 146–147
- **Encoding:** `nibble_hilo` — combined value `(byte[146] << 4) | byte[147]`
- **Confidence:** high
- **Role:** LCD cursor / edit-display position (not a sound parameter)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Front-panel cursor position packed as two nibbles in the program dump. High nibble (offset 146) is the page/row while browsing (`92 = 02`) or the edit anchor while changing a value (`92 = 00`). Low nibble (offset 147) is the column/position within the menu page, or the value-display position while editing.

Menu index remains authoritative at offsets **98–99**. See [Program UI state](../ui-state.md) for idle/browse/edit tables across all UI bytes.

## Encoding map

Witness sources: menu-navigation captures only (parameter values held constant). Wire bytes shown as two nibbles; decoded column is `nibble_hilo`.

| Label | Offset 146 | Offset 147 | `nibble_hilo` | Source |
|-------|------------|------------|--------------:|--------|
| idle (`no menu`) | `01` | `0C` | 28 | dump |
| browse: size (1) | `01` | `0D` | 29 | dump |
| browse: predelay (2) | `01` | `0E` | 30 | dump |
| browse: diffusion (3) | `01` | `0F` | 31 | dump |
| browse: density (4) | `02` | `00` | 32 | dump |
| browse: modulation (5) | `02` | `01` | 33 | dump |
| browse: rolloff (6) | `02` | `02` | 34 | dump |
| browse: hf rt multiply (7) | `02` | `03` | 35 | dump |
| browse: hf rt crossover (8) | `02` | `04` | 36 | dump |
| browse: lf rt multiply (9) | `02` | `05` | 37 | dump |
| browse: lf rt crossover (10) | `02` | `06` | 38 | dump |
| browse: vlf cut (11) | `02` | `07` | 39 | dump |
| browse: early to reverb mix (12) | `02` | `08` | 40 | dump |
| browse: early rolloff (13) | `02` | `09` | 41 | dump |
| browse: early select (14) | `02` | `0A` | 42 | dump |
| browse: delay level (15) | `02` | `0B` | 43 | dump |
| browse: delay time (16) | `02` | `0C` | 44 | dump |
| browse: delay modulation (17) | `02` | `0D` | 45 | dump |
| browse: reverb time (0) | `02` | `0E` | 46 | dump |

### Edit mode witnesses

Typical cursor bytes while turning a control (from parameter series dumps with `92 = 00`):

| Index | Parameter | Offset 146 | Offset 147 | `nibble_hilo` |
|------:|-----------|------------|------------|--------------:|
| 2 | predelay | `02` | `02` | 34 |
| 3 | diffusion | `02` | `09` | 41 |
| 4 | density | `03` | `07` | 55 |
| 5 | modulation | `04` | `06` | 70 |
| 6 | rolloff | `04` | `0E` | 78 |
| 7 | hf rt multiply | `06` | `05` | 101 |
| 8 | hf rt crossover | `07` | `03` | 115 |
| 11 | vlf cut | `07` | `0C` | 124 |
| 12 | early to reverb mix | `08` | `03` | 131 |
| 13 | early rolloff | `09` | `02` | 146 |
| 14 | early select | `09` | `0C` | 156 |
| 15 | delay level | `0A` | `05` | 165 |
| 16 | delay time | `0B` | `00` | 176 |
| 17 | delay modulation | `0B` | `0B` | 187 |
| 9 | lf rt multiply | `0B` | `0F` | 191 |
| 0 | reverb time | `0C` | `04` | 196 |
| 10 | lf rt crossover | `0C` | `07` | 199 |
| 1 | size | `0D` | `02` | 210 |

## Unseen values

The cursor packs two nibbles, so **256** `nibble_hilo` values are possible (0–255). Only **35** are witnessed in `sysex/prog/menus/` captures; the rest are unseen and shown as ranges below. The first witnessed position is idle (28), so `0–27` are never observed before it.

- **Witnessed positions:** 35 of 256
- **Unseen positions (221):** 0–27, 47–54, 56–69, 71–77, 79–100, 102–114, 116–123, 125–130, 132–145, 147–155, 157–164, 166–175, 177–186, 188–190, 192–195, 197–198, 200–209, 211–255

## Interpretation

- **Primary field:** offsets **146–147**, encoding `nibble_hilo`.
- **Confidence:** high — consistent across `sysex/prog/menus/` captures.
- **How to set:**
  1. `byte[146] = (value >> 4) & 0x0F`
  2. `byte[147] = value & 0x0F`
  3. Recompute trailing checksum: CRC-16/ARC over bytes[8:152], packed as four high-nibble-first SysEx bytes at offsets 152–155

## Related

- [Program UI state](../ui-state.md)
- [Byte map overview](../byte-map-overview.md)
- [Capture guide](../../../docs/capture-guide.md)

_Last exported: 2026-07-19_
