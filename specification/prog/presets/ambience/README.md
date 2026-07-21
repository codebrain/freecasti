[Overview](../../README.md) | [Bytes](../../bytes/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Ambience

_Generated 2026-07-21. Bank index **4** (15 captured presets)._

Machine-readable dump list: [presets.json](../presets.json).

## Presets

| Slot | Preset |
|-----:|--------|
| 0 | [Large Ambience](large-ambience.md) |
| 1 | [Med Ambience](med-ambience.md) |
| 2 | [Small Ambience](small-ambience.md) |
| 3 | [Large & Dark](large-and-dark.md) |
| 4 | [Medium & Dark](medium-and-dark.md) |
| 5 | [Small & Dark](small-and-dark.md) |
| 6 | [Large & Bright](large-and-bright.md) |
| 7 | [Med & Bright](med-and-bright.md) |
| 8 | [Small & Bright](small-and-bright.md) |
| 9 | [Deep Ambience](deep-ambience.md) |
| 10 | [Long Ambience](long-ambience.md) |
| 11 | [Clear Ambience](clear-ambience.md) |
| 12 | [Heavy Ambience](heavy-ambience.md) |
| 13 | [Bass  XXL](bass-xxl.md) |
| 14 | [Percussion Air](percussion-air.md) |

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
