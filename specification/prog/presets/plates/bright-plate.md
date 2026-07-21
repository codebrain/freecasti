[Overview](../../README.md) | [Bytes](../../bytes/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Bright Plate

_Generated 2026-07-22. Bank: [Plates](README.md) (index **1**). Source: `sysex/prog/presets/Plates.Bright Plate.syx`._

[All presets](../../README.md) · [Plates bank](README.md) · [Program identity](../../program-identity.md)

### Identity

| Field | Value |
|-------|-------|
| Bank | Plates (index 1) |
| Program slot | 0 |
| Name field | `Bright Plate` (matches filename) |
| Name window 8-87 (name + factory space pad) | match filename preset (ASCII space-padded) |
| Dump file | `Plates.Bright Plate.syx` |

> **Sheet discrepancies (1 soft):** dump values disagree with the [published preset sheet](../../preset-sheet.md). Highlighted in the Status column below. **SysEx dump is authoritative.**

> Soft = within table/rounding band (sparse-table interpolation or print rounding).

## Parameters

Decoded from independent `sysex/prog/parameters/<parameter>/` series. `Dump` is the labeled value from the densified encoding map; `Encoded` is the raw step stored in SysEx. `~` means the step fell between labeled witnesses (rare once `provided` UI walks are merged).

| Parameter | Dump | Encoded | Sheet | Status |
|-----------|------|--------:|-------|--------|
| [reverb time](../../bytes/reverb-time.md) | 2 s | 36 | 2.00 | match |
| [size](../../bytes/size.md) | 4 | 4 | 4 | match |
| [predelay](../../bytes/predelay.md) | 0 ms | 0 | 0 | match |
| [diffusion](../../bytes/diffusion.md) | 3 | 3 | 3 | match |
| [density](../../bytes/density.md) | 7 | 7 | 7 | match |
| [modulation](../../bytes/modulation.md) | 2 | 3 | 2 | match |
| [rolloff](../../bytes/rolloff.md) | 6400 Hz | 30 | 7600 | **soft** (Δ -1200) |
| [hf rt multiply](../../bytes/hf-rt-multiply.md) | 0.8 | 12 | 0.80 | match |
| [hf rt crossover](../../bytes/hf-rt-crossover.md) | 5600 Hz | 23 | 5600 | match |
| [lf rt multiply](../../bytes/lf-rt-multiply.md) | 0.7 | 10 | 0.70 | match |
| [lf rt crossover](../../bytes/lf-rt-crossover.md) | 1200 Hz | 15 | 1200 | match |
| [vlf cut](../../bytes/vlf-cut.md) | -15 dB | 5 | -15 | match |
| [early to reverb mix](../../bytes/early-to-reverb-mix.md) | 20/20 | 20 | 20/20 | match |
| [early rolloff](../../bytes/early-rolloff.md) | 10400 Hz | 40 | 10400 | match |
| [early select](../../bytes/early-select.md) | 15 | 15 | 15 | match |
| [delay level](../../bytes/delay-level.md) | off | 0 | — | not on sheet |
| [delay time](../../bytes/delay-time.md) | 100 ms | 0 | — | not on sheet |
| [delay modulation](../../bytes/delay-modulation.md) | off | 0 | — | not on sheet |

## Other presets in this bank

- **Bright Plate** (this page)
- [Dark Plate](dark-plate.md)
- [London Plate](london-plate.md)
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

_Last exported: 2026-07-22_
