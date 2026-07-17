[Overview](../../README.md) | [Parameters](../../parameters/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Rooms

_Generated 2026-07-18. Bank index **2** (36 captured presets)._

Machine-readable dump list: [presets.json](../presets.json).

## Presets

| Slot | Preset |
|-----:|--------|
| 0 | [Studio A](studio-a.md) |
| 1 | [Studio B Close](studio-b-close.md) |
| 2 | [Studio B Far](studio-b-far.md) |
| 3 | [Studio C](studio-c.md) |
| 4 | [Studio D](studio-d.md) |
| 5 | [Studio E](studio-e.md) |
| 6 | [Deep Stone](deep-stone.md) |
| 7 | [Music Room](music-room.md) |
| 8 | [Heavy Room](heavy-room.md) |
| 9 | [Large Wooden](large-wooden.md) |
| 10 | [Small Wooden](small-wooden.md) |
| 11 | [Large Tiled](large-tiled.md) |
| 12 | [Medium Tiled](medium-tiled.md) |
| 13 | [Small Tiled](small-tiled.md) |
| 14 | [Drum & Chamber](drum-and-chamber.md) |
| 15 | [Djangos Room](djangos-room.md) |
| 16 | [Small Vox Room](small-vox-room.md) |
| 17 | [Glass Room](glass-room.md) |
| 18 | [Percussion](percussion.md) |
| 19 | [Marble Foyer](marble-foyer.md) |
| 20 | [Large Q Room](large-q-room.md) |
| 21 | [Small Q Room](small-q-room.md) |
| 22 | [Large Red Room](large-red-room.md) |
| 23 | [Red Room](red-room.md) |
| 24 | [Blue Room](blue-room.md) |
| 25 | [Large Room](large-room.md) |
| 26 | [Small Room](small-room.md) |
| 27 | [Front Room](front-room.md) |
| 28 | [Center Room](center-room.md) |
| 29 | [Back Room](back-room.md) |
| 30 | [Studio K](studio-k.md) |
| 31 | [Waits Room](waits-room.md) |
| 32 | [Corn Room](corn-room.md) |
| 33 | [Oakland Room](oakland-room.md) |
| 34 | [SF Perf Room](sf-perf-room.md) |
| 35 | [Long Wood Room](long-wood-room.md) |

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
