[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Display

_Generated 2026-07-22. Source folder: `sysex/prog/menus/` (19 captures) + edit bands from `sysex/prog/parameters/`._

## SysEx summary

- **Offsets:** 146–147
- **Encoding:** `nibble_hilo` — combined value `(byte[146] << 4) | byte[147]`
- **Confidence:** high (UI field / not sound); edit-band geometry medium
- **Role:** Front-panel UI focus code (not a sound parameter)
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Packed UI focus code in the program dump. Discriminate modes with offset **92** (panel mode) and the menu index at **98–99**.

- **Browse** (`92 = 02`): stable **menu-row highlight** code. Indices 1–17 use `menu_index + 28`; reverb time (index 0) uses **46**; idle uses **28**.
- **Edit** (`92 = 00`): **value-focus** code inside a parameter-specific band. The code advances as the shown value changes (often only offset 147 until nibble wrap). It is **not** a fixed per-parameter edit anchor, not `encoding + constant`, and not 1:1 with large wire-encoding steps.

Safe to ignore when patching sound parameters (already treated as a secondary mover). Factory presets often latch a non-browse display value from the last UI focus.

## Encoding map (browse)

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

### Edit mode bands

Observed `nibble_hilo` ranges while turning a control (`92 = 00`, matching menu index at 98–99). Sparse series — bands are lower bounds on the true span. Sample is one mid dump, not a fixed anchor. Sorted by band minimum:

| Index | Parameter | Band | Unique/dumps | Monotonic | Sample 146–147 | Sample `nibble_hilo` |
|------:|-----------|-----:|-------------:|:---------:|----------------|-------------------:|
| 2 | predelay | 34–39 | 5/6 | yes | `02 06` | 38 |
| 3 | diffusion | 41–50 | 9/9 | yes | `02 0D` | 45 |
| 4 | density | 55–61 | 6/7 | yes | `03 0A` | 58 |
| 5 | modulation | 69–75 | 7/7 | yes | `04 08` | 72 |
| 6 | rolloff | 77–90 | 11/12 | yes | `05 04` | 84 |
| 7 | hf rt multiply | 92–101 | 9/10 | yes | `06 02` | 98 |
| 8 | hf rt crossover | 104–117 | 10/10 | yes | `06 0F` | 111 |
| 11 | vlf cut | 120–128 | 9/9 | yes | `07 0C` | 124 |
| 12 | early to reverb mix | 131–140 | 10/12 | yes | `08 08` | 136 |
| 13 | early rolloff | 146–153 | 5/5 | yes | `09 07` | 151 |
| 14 | early select | 155–163 | 8/8 | yes | `0A 00` | 160 |
| 15 | delay level | 165–171 | 6/6 | no | `0A 09` | 169 |
| 16 | delay time | 176–183 | 8/10 | yes | `0B 05` | 181 |
| 17 | delay modulation | 186–192 | 6/7 | yes | `0B 0E` | 190 |
| 9 | lf rt multiply | 191–197 | 7/8 | yes | `0C 02` | 194 |
| 0 | reverb time | 194–207 | 11/13 | yes | `0C 0A` | 202 |
| 10 | lf rt crossover | 199–205 | 7/8 | yes | `0C 0A` | 202 |
| 1 | size | 209–215 | 7/8 | yes | `0D 05` | 213 |

## Unseen values

The cursor packs two nibbles, so **256** `nibble_hilo` values are possible (0–255). Only **35** are witnessed in `sysex/prog/menus/` captures; the rest are unseen and shown as ranges below. The first witnessed position is idle (28), so `0–27` are never observed before it.

- **Witnessed positions:** 35 of 256
- **Unseen positions (221):** 0–27, 47–54, 56–69, 71–77, 79–100, 102–114, 116–123, 125–130, 132–145, 147–155, 157–164, 166–175, 177–186, 188–190, 192–195, 197–198, 200–209, 211–255

## Interpretation

- **Primary field:** offsets **146–147**, encoding `nibble_hilo`.
- **Confidence:** high that this is ephemeral UI state (not sound); **medium** for edit-mode band / value-focus geometry.
- **Browse:** menu-row highlight codes (see encoding map).
- **Edit:** parameter-specific value-focus bands (see table); reject fixed edit-anchor and second-parameter-word readings.
- **How to set (when synthesizing UI state):**
  1. `byte[146] = (value >> 4) & 0x0F`
  2. `byte[147] = value & 0x0F`
  3. Recompute trailing checksum: CRC-16/ARC over bytes[8:152], packed as four high-nibble-first SysEx bytes at offsets 152–155

### Hypothesis ranking

- **browse_menu_row** — `accepted` (high): Browse (`92=02`): display is a stable menu-row highlight code (idle 28; indices 1–17 → index+28; reverb time → 46).
- **fixed_edit_anchor** — `rejected` (high): Edit mode is not a fixed per-parameter anchor: within each parameter series display moves as the value changes (18 of 18 series have multiple display codes).
- **edit_value_focus_band** — `working` (medium): Edit (`92=00`): each parameter occupies a band of display codes that advances (usually non-decreasing) with the wire encoding, but is not encoding+constant and not 1:1 with large encoding steps. Discriminate overlapping codes via 98–99.
- **lcd_ddram_address** — `rejected` (high): HD44780-style DDRAM addresses (≤ ~0x67) cannot explain observed edit codes up to 215.
- **second_parameter_word** — `rejected` (high): Not a second copy of the parameter word (const display−encoded is false for every series).

### Edit-code collisions

Same display code witnessed under multiple parameters while editing (use 98–99 to disambiguate):

- `191`: delay modulation, lf rt multiply
- `192`: delay modulation, lf rt multiply
- `194`: lf rt multiply, reverb time
- `196`: lf rt multiply, reverb time
- `197`: lf rt multiply, reverb time
- `199`: lf rt crossover, reverb time
- `200`: lf rt crossover, reverb time
- `202`: lf rt crossover, reverb time
- `203`: lf rt crossover, reverb time
- `205`: lf rt crossover, reverb time

### Open

- Without dense every-step sweeps for a few parameters, edit display cannot be proven to equal discrete UI step index vs digit/cursor cell vs firmware string-pool ID.

## Related

- [Program UI state](../ui-state.md)
- [Byte map overview](../byte-map-overview.md)
- [Capture guide](../../../docs/capture-guide.md)

_Last exported: 2026-07-22_
