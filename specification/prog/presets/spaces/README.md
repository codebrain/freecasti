[Overview](../../README.md) | [Bytes](../../bytes/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Spaces

_Generated 2026-07-20. Bank index **5** (19 captured presets)._

Machine-readable dump list: [presets.json](../presets.json).

## Presets

| Slot | Preset |
|-----:|--------|
| 0 | [North Church](north-church.md) |
| 1 | [East Church](east-church.md) |
| 2 | [South Church](south-church.md) |
| 3 | [West Church](west-church.md) |
| 4 | [Cinema Room](cinema-room.md) |
| 5 | [Scoring Stage](scoring-stage.md) |
| 6 | [Bath House](bath-house.md) |
| 7 | [Car Park](car-park.md) |
| 8 | [Arena](arena.md) |
| 9 | [Redwood Valley](redwood-valley.md) |
| 10 | [Tanglewood](tanglewood.md) |
| 11 | [Academy Yard](academy-yard.md) |
| 12 | [Hillside](hillside.md) |
| 13 | [Cavern](cavern.md) |
| 14 | [Stone Quarry](stone-quarry.md) |
| 15 | [Europa](europa.md) |
| 16 | [Gated Space](gated-space.md) |
| 17 | [Reflect Chapel](reflect-chapel.md) |
| 18 | [Reflect Church](reflect-church.md) |

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

_Last exported: 2026-07-20_
