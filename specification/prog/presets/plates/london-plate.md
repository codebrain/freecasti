[Overview](../../README.md) | [Bytes](../../bytes/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# London Plate

_Generated 2026-07-19. Bank: [Plates](README.md) (index **1**). Source: `sysex/prog/presets/Plates.London Plate.syx`._

[All presets](../../README.md) · [Plates bank](README.md) · [Program identity](../../program-identity.md)

### Identity

| Field | Value |
|-------|-------|
| Bank | Plates (index 1) |
| Program slot | 2 |
| Name field | `London Plate` (matches filename) |
| Name region 8-87 | match filename preset (ASCII space-padded) |
| Dump file | `Plates.London Plate.syx` |

> **Sheet discrepancies (1 soft):** dump values disagree with the [published preset sheet](../../preset-sheet.md). Highlighted in the Status column below. **SysEx dump is authoritative.**

> Soft = within table/rounding band (sparse-table interpolation or print rounding).

## Parameters

Decoded from independent `sysex/prog/parameters/<parameter>/` series. `Dump` is the labeled value from the densified encoding map; `Encoded` is the raw step stored in SysEx. `~` means the step fell between labeled witnesses (rare once `provided` UI walks are merged).

| Parameter | Dump | Encoded | Sheet | Status |
|-----------|------|--------:|-------|--------|
| [reverb time](../../bytes/reverb-time.md) | 1.8 s | 32 | 1.80 | match |
| [size](../../bytes/size.md) | 4 | 4 | 4 | match |
| [predelay](../../bytes/predelay.md) | 0 ms | 0 | 0 | match |
| [diffusion](../../bytes/diffusion.md) | 1 | 1 | 1 | match |
| [density](../../bytes/density.md) | 10 | 10 | H | match |
| [modulation](../../bytes/modulation.md) | off | 0 | off | match |
| [rolloff](../../bytes/rolloff.md) | 4400 Hz | 25 | 5200 | **soft** (Δ -800) |
| [hf rt multiply](../../bytes/hf-rt-multiply.md) | 0.95 | 15 | 0.95 | match |
| [hf rt crossover](../../bytes/hf-rt-crossover.md) | 3200 Hz | 19 | 3200 | match |
| [lf rt multiply](../../bytes/lf-rt-multiply.md) | 1 | 16 | 1.00 | match |
| [lf rt crossover](../../bytes/lf-rt-crossover.md) | 800 Hz | 13 | 800 | match |
| [vlf cut](../../bytes/vlf-cut.md) | -10 dB | 10 | -10 | match |
| [early to reverb mix](../../bytes/early-to-reverb-mix.md) | 20/20 | 20 | 20/20 | match |
| [early rolloff](../../bytes/early-rolloff.md) | 7200 Hz | 32 | 7200 | match |
| [early select](../../bytes/early-select.md) | 2 | 2 | 2 | match |
| [delay level](../../bytes/delay-level.md) | off | 0 | — | not on sheet |
| [delay time](../../bytes/delay-time.md) | 100 ms | 0 | — | not on sheet |
| [delay modulation](../../bytes/delay-modulation.md) | off | 0 | — | not on sheet |

## Other presets in this bank

- [Bright Plate](bright-plate.md)
- [Dark Plate](dark-plate.md)
- **London Plate** (this page)
- [Snare Plate A](snare-plate-a.md)
- [Snare Plate B](snare-plate-b.md)
- [Vocal Plate](vocal-plate.md)
- [Old Plate](old-plate.md)
- [Rich Plate](rich-plate.md)
- [Gold Plate](gold-plate.md)
- [Dense Plate](dense-plate.md)
- [Silver Plate](silver-plate.md)
- [Percussion](percussion.md)
- [Echo Plate](echo-plate.md)
- [CD Plate A](cd-plate-a.md)
- [CD Plate B](cd-plate-b.md)
- [Large Plate](large-plate.md)
- [Small Plate](small-plate.md)
- [Fat Plate](fat-plate.md)
- [Crystal Plate](crystal-plate.md)
- [Sun Plate A](sun-plate-a.md)
- [Sun Plate B](sun-plate-b.md)
- [Sun Plate C](sun-plate-c.md)
- [Vocal Plate B](vocal-plate-b.md)
- [Repro Plate](repro-plate.md)

_Last exported: 2026-07-19_
