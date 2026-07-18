[Overview](../../README.md) | [Bytes](../../bytes/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Rooms 2

_Generated 2026-07-18. Bank index **8** (22 captured presets)._

Machine-readable dump list: [presets.json](../presets.json).

## Presets

| Slot | Preset |
|-----:|--------|
| 0 | [Music Club](music-club.md) |
| 1 | [Large Room](large-room.md) |
| 2 | [Med Room](med-room.md) |
| 3 | [Small Room](small-room.md) |
| 4 | [Lg Wood Room](lg-wood-room.md) |
| 5 | [Sm Wood Room](sm-wood-room.md) |
| 6 | [Large Chamber](large-chamber.md) |
| 7 | [Small Chamber](small-chamber.md) |
| 8 | [Bright Chamber](bright-chamber.md) |
| 9 | [Tiled Room](tiled-room.md) |
| 10 | [Fat Chamber](fat-chamber.md) |
| 11 | [Studio 1](studio-1.md) |
| 12 | [Studio 2](studio-2.md) |
| 13 | [Studio 3](studio-3.md) |
| 14 | [Studio 4](studio-4.md) |
| 15 | [Guitar Room](guitar-room.md) |
| 16 | [Marble Room](marble-room.md) |
| 17 | [Deep Chamber](deep-chamber.md) |
| 18 | [Dark Chamber](dark-chamber.md) |
| 19 | [Vocal Chamber](vocal-chamber.md) |
| 20 | [Wide Room](wide-room.md) |
| 21 | [Lush Room](lush-room.md) |

## Decoder sources

| Parameter | Offsets | Encoding | Kind |
|-----------|---------|----------|------|
| [reverb time](../../bytes/reverb-time.md) | 100-101 | `nibble_hilo` | table |
| [size](../../bytes/size.md) | 102-103 | `nibble_hilo` | affine |
| [predelay](../../bytes/predelay.md) | 104-105 | `nibble_hilo` | table |
| [diffusion](../../bytes/diffusion.md) | 107 | `raw_u8` | affine |
| [density](../../bytes/density.md) | 109 | `raw_u8` | affine |
| [modulation](../../bytes/modulation.md) | 111 | `raw_u8` | affine |
| [rolloff](../../bytes/rolloff.md) | 112-113 | `nibble_hilo` | table |
| [hf rt multiply](../../bytes/hf-rt-multiply.md) | 114-115 | `nibble_hilo` | affine |
| [hf rt crossover](../../bytes/hf-rt-crossover.md) | 116-117 | `nibble_hilo` | table |
| [lf rt multiply](../../bytes/lf-rt-multiply.md) | 118-119 | `nibble_hilo` | table |
| [lf rt crossover](../../bytes/lf-rt-crossover.md) | 120-121 | `nibble_hilo` | table |
| [vlf cut](../../bytes/vlf-cut.md) | 122-123 | `nibble_hilo` | affine |
| [early to reverb mix](../../bytes/early-to-reverb-mix.md) | 124-125 | `nibble_hilo` | affine |
| [early rolloff](../../bytes/early-rolloff.md) | 126-127 | `nibble_hilo` | table |
| [early select](../../bytes/early-select.md) | 128-129 | `nibble_hilo` | affine |
| [delay level](../../bytes/delay-level.md) | 133 | `raw_u8` | affine |
| [delay time](../../bytes/delay-time.md) | 134-135 | `nibble_hilo` | affine |
| [delay modulation](../../bytes/delay-modulation.md) | 139 | `raw_u8` | affine |

[All presets](../) · [Program identity](../../program-identity.md)

_Last exported: 2026-07-18_
