[Overview](../../README.md) | [Bytes](../../bytes/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Plates

_Generated 2026-07-21. Bank index **1** (24 captured presets)._

Machine-readable dump list: [presets.json](../presets.json).

## Presets

| Slot | Preset |
|-----:|--------|
| 0 | [Bright Plate](bright-plate.md) |
| 1 | [Dark Plate](dark-plate.md) |
| 2 | [London Plate](london-plate.md) |
| 3 | [Snare Plate A](snare-plate-a.md) |
| 4 | [Snare Plate B](snare-plate-b.md) |
| 5 | [Vocal Plate](vocal-plate.md) |
| 6 | [Old Plate](old-plate.md) |
| 7 | [Rich Plate](rich-plate.md) |
| 8 | [Gold Plate](gold-plate.md) |
| 9 | [Dense Plate](dense-plate.md) |
| 10 | [Silver Plate](silver-plate.md) |
| 11 | [Percussion](percussion.md) |
| 12 | [Echo Plate](echo-plate.md) |
| 13 | [CD Plate A](cd-plate-a.md) |
| 14 | [CD Plate B](cd-plate-b.md) |
| 15 | [Large Plate](large-plate.md) |
| 16 | [Small Plate](small-plate.md) |
| 17 | [Fat Plate](fat-plate.md) |
| 18 | [Crystal Plate](crystal-plate.md) |
| 19 | [Sun Plate A](sun-plate-a.md) |
| 20 | [Sun Plate B](sun-plate-b.md) |
| 21 | [Sun Plate C](sun-plate-c.md) |
| 22 | [Vocal Plate B](vocal-plate-b.md) |
| 23 | [Repro Plate](repro-plate.md) |

## Decoder sources

| Parameter | Offsets | Encoding | Kind |
|-----------|---------|----------|------|
| [reverb time](../../bytes/reverb-time.md) | 100-101 | `nibble_hilo` | table |
| [size](../../bytes/size.md) | 102-103 | `nibble_hilo` | affine |
| [predelay](../../bytes/predelay.md) | 104-105 | `nibble_hilo` | table |
| [diffusion](../../bytes/diffusion.md) | 106-107 | `nibble_hilo` | affine |
| [density](../../bytes/density.md) | 108-109 | `nibble_hilo` | affine |
| [modulation](../../bytes/modulation.md) | 110-111 | `nibble_hilo` | affine |
| [rolloff](../../bytes/rolloff.md) | 112-113 | `nibble_hilo` | table |
| [hf rt multiply](../../bytes/hf-rt-multiply.md) | 114-115 | `nibble_hilo` | affine |
| [hf rt crossover](../../bytes/hf-rt-crossover.md) | 116-117 | `nibble_hilo` | table |
| [lf rt multiply](../../bytes/lf-rt-multiply.md) | 118-119 | `nibble_hilo` | table |
| [lf rt crossover](../../bytes/lf-rt-crossover.md) | 120-121 | `nibble_hilo` | table |
| [vlf cut](../../bytes/vlf-cut.md) | 122-123 | `nibble_hilo` | affine |
| [early to reverb mix](../../bytes/early-to-reverb-mix.md) | 124-125 | `nibble_hilo` | affine |
| [early rolloff](../../bytes/early-rolloff.md) | 126-127 | `nibble_hilo` | table |
| [early select](../../bytes/early-select.md) | 128-129 | `nibble_hilo` | affine |
| [delay level](../../bytes/delay-level.md) | 132-133 | `nibble_hilo` | affine |
| [delay time](../../bytes/delay-time.md) | 134-135 | `nibble_hilo` | affine |
| [delay modulation](../../bytes/delay-modulation.md) | 138-139 | `nibble_hilo` | affine |

[All presets](../) · [Program identity](../../program-identity.md)

_Last exported: 2026-07-21_
