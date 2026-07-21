[Overview](README.md) | [Bytes](bytes/README.md) | [Program identity](program-identity.md) | [Preset inventory](preset-inventory.md) | [Preset sheet](preset-sheet.md) | **Byte map** | [Cross-series](cross.md) | [System dumps](../system/README.md)

# Byte map overview

**157**-byte program dump. Known/frame/checksum **154** · secondary **3** · unknown **0**.

Full regions table: [byte-map.md](byte-map.md).

Codegen layout: [m7_program_dump.ksy](m7_program_dump.ksy) ([Kaitai Struct](https://kaitai.io/)) · [m7_program_dump.spec.json](m7_program_dump.spec.json).

Reserved/meta roles (padding, family flag, display @ 146–147, engine/bank class) come from a corpus scan of all `.syx` dumps — medium confidence.

### Layout

| Offsets | Len | Status | Field |
|---------|----:|--------|-------|
| 0 | 1 | frame | SysEx start (F0) |
| 1-3 | 3 | frame | manufacturer ID |
| 4-7 | 4 | frame | program-dump header |
| 8-21 | 14 | frame | [program name (ASCII)](bytes/program-name.md) |
| 22-23 | 2 | frame | [program name pad](bytes/program-name-pad.md) |
| 24-87 | 64 | frame | [register basis blob](bytes/register-basis-blob.md) |
| 88-89 | 2 | known | [bank index](bytes/bank-index.md) (`nibble_hilo`) |
| 90-91 | 2 | known | [program slot](bytes/program-slot.md) (`nibble_hilo`) |
| 92 | 1 | secondary | [panel mode flag](bytes/panel-mode-flag.md) (`raw_u8`) |
| 93 | 1 | known | [register bank](bytes/register-bank.md) (`raw_u8`) |
| 94 | 1 | known | [favorite slot (8 = none)](bytes/favorite-slot.md) (`raw_u8`) |
| 95 | 1 | known | [register](bytes/register.md) (`raw_u8`) |
| 96 | 1 | known | reserved (always 0) |
| 97 | 1 | known | [algorithm/family flag](bytes/algorithm-family-flag.md) (`raw_u8`) |
| 98-99 | 2 | secondary | [selected menu index](bytes/selected-menu-index.md) (`nibble_hilo`) |
| 100-101 | 2 | known | [reverb time](bytes/reverb-time.md) (`nibble_hilo`) |
| 102-103 | 2 | known | [size](bytes/size.md) (`nibble_hilo`) |
| 104-105 | 2 | known | [predelay](bytes/predelay.md) (`nibble_hilo`) |
| 106 | 1 | known | reserved padding |
| 107 | 1 | known | [diffusion](bytes/diffusion.md) (`raw_u8`) |
| 108 | 1 | known | reserved padding |
| 109 | 1 | known | [density](bytes/density.md) (`raw_u8`) |
| 110 | 1 | known | reserved padding |
| 111 | 1 | known | [modulation](bytes/modulation.md) (`raw_u8`) |
| 112-113 | 2 | known | [rolloff](bytes/rolloff.md) (`nibble_hilo`) |
| 114-115 | 2 | known | [hf rt multiply](bytes/hf-rt-multiply.md) (`nibble_hilo`) |
| 116-117 | 2 | known | [hf rt crossover](bytes/hf-rt-crossover.md) (`nibble_hilo`) |
| 118-119 | 2 | known | [lf rt multiply](bytes/lf-rt-multiply.md) (`nibble_hilo`) |
| 120-121 | 2 | known | [lf rt crossover](bytes/lf-rt-crossover.md) (`nibble_hilo`) |
| 122-123 | 2 | known | [vlf cut](bytes/vlf-cut.md) (`nibble_hilo`) |
| 124-125 | 2 | known | [early to reverb mix](bytes/early-to-reverb-mix.md) (`nibble_hilo`) |
| 126-127 | 2 | known | [early rolloff](bytes/early-rolloff.md) (`nibble_hilo`) |
| 128-129 | 2 | known | [early select](bytes/early-select.md) (`nibble_hilo`) |
| 130 | 1 | known | [engine/bank-class flag](bytes/engine-bank-class-flag.md) (`raw_u8`) |
| 131-132 | 2 | known | fixed (always 02 00) |
| 133 | 1 | known | [delay level](bytes/delay-level.md) (`raw_u8`) |
| 134-135 | 2 | known | [delay time](bytes/delay-time.md) (`nibble_hilo`) |
| 136 | 1 | known | reserved (always 0) |
| 137 | 1 | known | [bank index mirror](bytes/bank-index.md) (`raw_u8`) |
| 138 | 1 | known | reserved (always 0) |
| 139 | 1 | known | [delay modulation](bytes/delay-modulation.md) (`raw_u8`) |
| 140-144 | 5 | known | reserved (always 0) |
| 145 | 1 | known | [family-flag mirror](bytes/algorithm-family-flag.md) (`raw_u8`) |
| 146-147 | 2 | known | [display](bytes/display.md) (`nibble_hilo`) |
| 148-151 | 4 | known | reserved (always 0) |
| 152-155 | 4 | checksum | checksum (CRC-16/ARC) |
| 156 | 1 | frame | SysEx end (F7) |

### Parameters (by offset)

| Offsets | Parameter | Encoding | Source |
|---------|-----------|----------|--------|
| 88-89 | [bank index](bytes/bank-index.md) | `nibble_hilo` | [_presets](program-identity.md) |
| 90-91 | [program slot](bytes/program-slot.md) | `nibble_hilo` | [_presets](program-identity.md) |
| 93 | [register bank](bytes/register-bank.md) | `raw_u8` | corpus |
| 94 | [favorite slot (8 = none)](bytes/favorite-slot.md) | `raw_u8` | corpus |
| 95 | [register](bytes/register.md) | `raw_u8` | corpus |
| 97 | [algorithm/family flag](bytes/algorithm-family-flag.md) | `raw_u8` | corpus |
| 100-101 | [reverb time](bytes/reverb-time.md) | `nibble_hilo` | series |
| 102-103 | [size](bytes/size.md) | `nibble_hilo` | series |
| 104-105 | [predelay](bytes/predelay.md) | `nibble_hilo` | series |
| 107 | [diffusion](bytes/diffusion.md) | `raw_u8` | series |
| 109 | [density](bytes/density.md) | `raw_u8` | series |
| 111 | [modulation](bytes/modulation.md) | `raw_u8` | series |
| 112-113 | [rolloff](bytes/rolloff.md) | `nibble_hilo` | series |
| 114-115 | [hf rt multiply](bytes/hf-rt-multiply.md) | `nibble_hilo` | series |
| 116-117 | [hf rt crossover](bytes/hf-rt-crossover.md) | `nibble_hilo` | series |
| 118-119 | [lf rt multiply](bytes/lf-rt-multiply.md) | `nibble_hilo` | series |
| 120-121 | [lf rt crossover](bytes/lf-rt-crossover.md) | `nibble_hilo` | series |
| 122-123 | [vlf cut](bytes/vlf-cut.md) | `nibble_hilo` | series |
| 124-125 | [early to reverb mix](bytes/early-to-reverb-mix.md) | `nibble_hilo` | series |
| 126-127 | [early rolloff](bytes/early-rolloff.md) | `nibble_hilo` | series |
| 128-129 | [early select](bytes/early-select.md) | `nibble_hilo` | series |
| 130 | [engine/bank-class flag](bytes/engine-bank-class-flag.md) | `raw_u8` | corpus |
| 133 | [delay level](bytes/delay-level.md) | `raw_u8` | series |
| 134-135 | [delay time](bytes/delay-time.md) | `nibble_hilo` | series |
| 137 | [bank index mirror](bytes/bank-index.md) | `raw_u8` | [_presets](program-identity.md) |
| 139 | [delay modulation](bytes/delay-modulation.md) | `raw_u8` | series |
| 145 | [family-flag mirror](bytes/algorithm-family-flag.md) | `raw_u8` | corpus |
| 146-147 | [display](bytes/display.md) | `nibble_hilo` | [_menus](bytes/display.md) |

### Secondary

Edit/UI state (not a sound parameter): `92`, `98-99`

See [panel mode flag](bytes/panel-mode-flag.md), [selected menu index](bytes/selected-menu-index.md), [ui-state.md](ui-state.md), and [bytes/display.md](bytes/display.md) for menu captures.


_Last exported: 2026-07-21_
