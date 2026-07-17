[Overview](../../README.md) | [Parameters](../../parameters/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Chambers

_Generated 2026-07-18. Bank index **3** (22 captured presets)._

Machine-readable dump list: [presets.json](../presets.json).

## Presets

| Slot | Preset |
|-----:|--------|
| 0 | [Large Chamber](large-chamber.md) |
| 1 | [Medium Chamber](medium-chamber.md) |
| 2 | [Small Chamber](small-chamber.md) |
| 3 | [Large & Dark](large-and-dark.md) |
| 4 | [Small & Dark](small-and-dark.md) |
| 5 | [Large & Bright](large-and-bright.md) |
| 6 | [Small & Bright](small-and-bright.md) |
| 7 | [Kick Chamber](kick-chamber.md) |
| 8 | [Snare Chamber](snare-chamber.md) |
| 9 | [Vocal Chamber](vocal-chamber.md) |
| 10 | [A&M Chamber](a-and-m-chamber.md) |
| 11 | [CD Chamber](cd-chamber.md) |
| 12 | [Old Chamber](old-chamber.md) |
| 13 | [Deep Chamber](deep-chamber.md) |
| 14 | [Amb Chamber A](amb-chamber-a.md) |
| 15 | [Amb Chamber B](amb-chamber-b.md) |
| 16 | [Sunset Chamber](sunset-chamber.md) |
| 17 | [A&M Chamber B](a-and-m-chamber-b.md) |
| 18 | [Stone Chamber](stone-chamber.md) |
| 19 | [Tiled Chamber](tiled-chamber.md) |
| 20 | [Fat Chamber](fat-chamber.md) |
| 21 | [Echo Chamber](echo-chamber.md) |

## Decoder sources

| Parameter | Offsets | Encoding | Kind |
|-----------|---------|----------|------|
| [reverb time](../../parameters/reverb-time.md) | 100-101 | `nibble_hilo` | table |
| [size](../../parameters/size.md) | 102-103 | `nibble_hilo` | affine |
| [predelay](../../parameters/predelay.md) | 104-105 | `nibble_hilo` | table |
| [diffusion](../../parameters/diffusion.md) | 107 | `raw_u8` | affine |
| [density](../../parameters/density.md) | 109 | `raw_u8` | affine |
| [modulation](../../parameters/modulation.md) | 111 | `raw_u8` | affine |
| [rolloff](../../parameters/rolloff.md) | 112-113 | `nibble_hilo` | table |
| [hf rt multiply](../../parameters/hf-rt-multiply.md) | 114-115 | `nibble_hilo` | affine |
| [hf rt crossover](../../parameters/hf-rt-crossover.md) | 116-117 | `nibble_hilo` | table |
| [lf rt multiply](../../parameters/lf-rt-multiply.md) | 118-119 | `nibble_hilo` | table |
| [lf rt crossover](../../parameters/lf-rt-crossover.md) | 120-121 | `nibble_hilo` | table |
| [vlf cut](../../parameters/vlf-cut.md) | 122-123 | `nibble_hilo` | affine |
| [early to reverb mix](../../parameters/early-to-reverb-mix.md) | 124-125 | `nibble_hilo` | affine |
| [early rolloff](../../parameters/early-rolloff.md) | 126-127 | `nibble_hilo` | table |
| [early select](../../parameters/early-select.md) | 128-129 | `nibble_hilo` | affine |
| [delay level](../../parameters/delay-level.md) | 133 | `raw_u8` | affine |
| [delay time](../../parameters/delay-time.md) | 134-135 | `nibble_hilo` | affine |
| [delay modulation](../../parameters/delay-modulation.md) | 139 | `raw_u8` | affine |

[All presets](../) · [Program identity](../../program-identity.md)

_Last exported: 2026-07-18_
