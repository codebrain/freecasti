[Overview](../../README.md) | [Parameters](../../parameters/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Plates 2

_Generated 2026-07-18. Bank index **7** (14 captured presets)._

Machine-readable dump list: [presets.json](../presets.json).

## Presets

| Slot | Preset |
|-----:|--------|
| 0 | [Plate A](plate-a.md) |
| 1 | [Small Plate](small-plate.md) |
| 2 | [Snare Plate](snare-plate.md) |
| 3 | [Dark Plate](dark-plate.md) |
| 4 | [Rich Plate A](rich-plate-a.md) |
| 5 | [Rich Plate B](rich-plate-b.md) |
| 6 | [Thin Plate](thin-plate.md) |
| 7 | [Vocal Plate A](vocal-plate-a.md) |
| 8 | [Vocal Plate B](vocal-plate-b.md) |
| 9 | [Drum Plate](drum-plate.md) |
| 10 | [Large Plate](large-plate.md) |
| 11 | [Fat Plate](fat-plate.md) |
| 12 | [Alpha Plate](alpha-plate.md) |
| 13 | [Vocal Shimmer](vocal-shimmer.md) |

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
