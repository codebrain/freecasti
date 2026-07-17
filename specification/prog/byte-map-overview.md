[Overview](README.md) | [Parameters](parameters/README.md) | [Program identity](program-identity.md) | [Preset inventory](preset-inventory.md) | [Preset sheet](preset-sheet.md) | **Byte map** | [Cross-series](cross.md) | [System dumps](../system/README.md)

# Byte map overview

**157**-byte program dump. Known/frame/checksum **152** · secondary **5** · unknown **0**.

Full regions + per-byte table: [byte-map.md](byte-map.md).

Codegen layout: [m7_program_dump.ksy](m7_program_dump.ksy) ([Kaitai Struct](https://kaitai.io/)) · [m7_program_dump.spec.json](m7_program_dump.spec.json).

Reserved/meta roles (padding, family flag, edit counter, engine/bank class) come from a corpus scan of all `.syx` dumps — medium confidence.

### Layout

| Offsets | Len | Status | Field |
|---------|----:|--------|-------|
| 0 | 1 | frame | SysEx start (F0) |
| 1-3 | 3 | frame | manufacturer ID |
| 4-7 | 4 | frame | program-dump header |
| 8-87 | 80 | frame | [program name (ASCII)](program-identity.md) |
| 88-89 | 2 | known | [bank index](program-identity.md) (`nibble_hilo`) |
| 90-91 | 2 | known | [program slot](program-identity.md) (`nibble_hilo`) |
| 92 | 1 | secondary | secondary (edit/UI) |
| 93-94 | 2 | known | fixed field (always 8) (`nibble_hilo`) |
| 95-96 | 2 | known | reserved (always 0) |
| 97 | 1 | known | algorithm/family flag (`raw_u8`) |
| 98-99 | 2 | secondary | edit/generation counter (`nibble_hilo`) |
| 100-101 | 2 | known | [reverb time](parameters/reverb-time.md) (`nibble_hilo`) |
| 102-103 | 2 | known | [size](parameters/size.md) (`nibble_hilo`) |
| 104-105 | 2 | known | [predelay](parameters/predelay.md) (`nibble_hilo`) |
| 106 | 1 | known | reserved padding |
| 107 | 1 | known | [diffusion](parameters/diffusion.md) (`raw_u8`) |
| 108 | 1 | known | reserved padding |
| 109 | 1 | known | [density](parameters/density.md) (`raw_u8`) |
| 110 | 1 | known | reserved padding |
| 111 | 1 | known | [modulation](parameters/modulation.md) (`raw_u8`) |
| 112-113 | 2 | known | [rolloff](parameters/rolloff.md) (`nibble_hilo`) |
| 114-115 | 2 | known | [hf rt multiply](parameters/hf-rt-multiply.md) (`nibble_hilo`) |
| 116-117 | 2 | known | [hf rt crossover](parameters/hf-rt-crossover.md) (`nibble_hilo`) |
| 118-119 | 2 | known | [lf rt multiply](parameters/lf-rt-multiply.md) (`nibble_hilo`) |
| 120-121 | 2 | known | [lf rt crossover](parameters/lf-rt-crossover.md) (`nibble_hilo`) |
| 122-123 | 2 | known | [vlf cut](parameters/vlf-cut.md) (`nibble_hilo`) |
| 124-125 | 2 | known | [early to reverb mix](parameters/early-to-reverb-mix.md) (`nibble_hilo`) |
| 126-127 | 2 | known | [early rolloff](parameters/early-rolloff.md) (`nibble_hilo`) |
| 128-129 | 2 | known | [early select](parameters/early-select.md) (`nibble_hilo`) |
| 130 | 1 | known | engine/bank-class flag (`raw_u8`) |
| 131-132 | 2 | known | fixed (always 02 00) |
| 133 | 1 | known | [delay level](parameters/delay-level.md) (`raw_u8`) |
| 134-135 | 2 | known | [delay time](parameters/delay-time.md) (`nibble_hilo`) |
| 136 | 1 | known | reserved (always 0) |
| 137 | 1 | known | [bank index mirror](program-identity.md) (`raw_u8`) |
| 138 | 1 | known | reserved (always 0) |
| 139 | 1 | known | [delay modulation](parameters/delay-modulation.md) (`raw_u8`) |
| 140-144 | 5 | known | reserved (always 0) |
| 145 | 1 | known | family-flag mirror (`raw_u8`) |
| 146 | 1 | secondary | secondary (edit/UI) |
| 147 | 1 | secondary | secondary (edit/UI) |
| 148-151 | 4 | known | reserved (always 0) |
| 152-155 | 4 | checksum | checksum (CRC-16/ARC) |
| 156 | 1 | frame | SysEx end (F7) |

### Parameters (by offset)

| Offsets | Parameter | Encoding | Source |
|---------|-----------|----------|--------|
| 88-89 | [bank index](program-identity.md) | `nibble_hilo` | [_presets](program-identity.md) |
| 90-91 | [program slot](program-identity.md) | `nibble_hilo` | [_presets](program-identity.md) |
| 97 | algorithm/family flag | `raw_u8` | corpus |
| 100-101 | [reverb time](parameters/reverb-time.md) | `nibble_hilo` | series |
| 102-103 | [size](parameters/size.md) | `nibble_hilo` | series |
| 104-105 | [predelay](parameters/predelay.md) | `nibble_hilo` | series |
| 107 | [diffusion](parameters/diffusion.md) | `raw_u8` | series |
| 109 | [density](parameters/density.md) | `raw_u8` | series |
| 111 | [modulation](parameters/modulation.md) | `raw_u8` | series |
| 112-113 | [rolloff](parameters/rolloff.md) | `nibble_hilo` | series |
| 114-115 | [hf rt multiply](parameters/hf-rt-multiply.md) | `nibble_hilo` | series |
| 116-117 | [hf rt crossover](parameters/hf-rt-crossover.md) | `nibble_hilo` | series |
| 118-119 | [lf rt multiply](parameters/lf-rt-multiply.md) | `nibble_hilo` | series |
| 120-121 | [lf rt crossover](parameters/lf-rt-crossover.md) | `nibble_hilo` | series |
| 122-123 | [vlf cut](parameters/vlf-cut.md) | `nibble_hilo` | series |
| 124-125 | [early to reverb mix](parameters/early-to-reverb-mix.md) | `nibble_hilo` | series |
| 126-127 | [early rolloff](parameters/early-rolloff.md) | `nibble_hilo` | series |
| 128-129 | [early select](parameters/early-select.md) | `nibble_hilo` | series |
| 130 | engine/bank-class flag | `raw_u8` | corpus |
| 133 | [delay level](parameters/delay-level.md) | `raw_u8` | series |
| 134-135 | [delay time](parameters/delay-time.md) | `nibble_hilo` | series |
| 137 | [bank index mirror](program-identity.md) | `raw_u8` | [_presets](program-identity.md) |
| 139 | [delay modulation](parameters/delay-modulation.md) | `raw_u8` | series |
| 145 | family-flag mirror | `raw_u8` | corpus |

### Secondary

Edit/UI state (not a sound parameter): `92`, `98-99`, `146`, `147`


_Last exported: 2026-07-18_
