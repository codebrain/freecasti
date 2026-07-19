[Overview](../../README.md) | [Bytes](../../bytes/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Halls

_Generated 2026-07-19. Bank index **0** (32 captured presets)._

Machine-readable dump list: [presets.json](../presets.json).

## Presets

| Slot | Preset |
|-----:|--------|
| 0 | [Large Hall](large-hall.md) |
| 1 | [Medium Hall](medium-hall.md) |
| 2 | [Small Hall](small-hall.md) |
| 3 | [Large & Near](large-and-near.md) |
| 4 | [Medium & Near](medium-and-near.md) |
| 5 | [Small & Near](small-and-near.md) |
| 6 | [Large & Dark](large-and-dark.md) |
| 7 | [Large & Deep](large-and-deep.md) |
| 8 | [Medium & Deep](medium-and-deep.md) |
| 9 | [Concert Hall](concert-hall.md) |
| 10 | [Gold Hall](gold-hall.md) |
| 11 | [Sandors Hall](sandors-hall.md) |
| 12 | [Dense Hall](dense-hall.md) |
| 13 | [Clear Hall](clear-hall.md) |
| 14 | [Brass Hall](brass-hall.md) |
| 15 | [Amsterdam Hall](amsterdam-hall.md) |
| 16 | [Berliner Hall](berliner-hall.md) |
| 17 | [Boston Hall A](boston-hall-a.md) |
| 18 | [Boston Hall B](boston-hall-b.md) |
| 19 | [Chicago Hall](chicago-hall.md) |
| 20 | [Vienna Hall](vienna-hall.md) |
| 21 | [Worcester Hall](worcester-hall.md) |
| 22 | [The ArchDuke](the-archduke.md) |
| 23 | [Troy Hall](troy-hall.md) |
| 24 | [Saint Sylvain](saint-sylvain.md) |
| 25 | [Mechanics Hall](mechanics-hall.md) |
| 26 | [Saint Gerold](saint-gerold.md) |
| 27 | [Pepes Hall A](pepes-hall-a.md) |
| 28 | [Pepes Hall B](pepes-hall-b.md) |
| 29 | [Reflect Hall A](reflect-hall-a.md) |
| 30 | [Reflect Hall B](reflect-hall-b.md) |
| 31 | [Piano Hall](piano-hall.md) |

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
