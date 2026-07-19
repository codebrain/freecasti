[Overview](../../README.md) | [Bytes](../../bytes/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Spaces 2

_Generated 2026-07-19. Bank index **9** (20 captured presets)._

Machine-readable dump list: [presets.json](../presets.json).

## Presets

| Slot | Preset |
|-----:|--------|
| 0 | [Open Space](open-space.md) |
| 1 | [Med Space](med-space.md) |
| 2 | [Small Space](small-space.md) |
| 3 | [Vox Ambience](vox-ambience.md) |
| 4 | [Big Bottom](big-bottom.md) |
| 5 | [Cathedral](cathedral.md) |
| 6 | [Grand Stage](grand-stage.md) |
| 7 | [Lush Church](lush-church.md) |
| 8 | [Grand Church](grand-church.md) |
| 9 | [Concert Wave](concert-wave.md) |
| 10 | [Long Vox Space](long-vox-space.md) |
| 11 | [Dark Warm Room](dark-warm-room.md) |
| 12 | [Live Room](live-room.md) |
| 13 | [Shimmering Sky](shimmering-sky.md) |
| 14 | [Oak Ballroom](oak-ballroom.md) |
| 15 | [Ice House](ice-house.md) |
| 16 | [Ice Beads](ice-beads.md) |
| 17 | [Music Forest](music-forest.md) |
| 18 | [Waving Bloom](waving-bloom.md) |
| 19 | [Brick Chamber](brick-chamber.md) |

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

_Last exported: 2026-07-19_
