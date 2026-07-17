[Overview](../../README.md) | [Parameters](../../parameters/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Large Hall

_Generated 2026-07-18. Bank: [Halls](README.md) (index **0**). Source: `sysex/prog/presets/Halls.Large Hall.syx`._

[All presets](../../README.md) · [Halls bank](README.md) · [Program identity](../../program-identity.md)

### Identity

| Field | Value |
|-------|-------|
| Bank | Halls (index 0) |
| Program slot | 0 |
| Name field | `Large Hall` (matches filename) |
| Name bytes 8-87 | match filename preset (ASCII space-padded) |
| Dump file | `Halls.Large Hall.syx` |

> **Sheet discrepancies (1 hard):** dump values disagree with the [published preset sheet](../../preset-sheet.md). Highlighted in the Status column below. **SysEx dump is authoritative.**

> Hard = beyond tolerance (likely sheet print error or unit/firmware variance).

## Parameters

Decoded from independent `sysex/prog/parameters/<parameter>/` series. `Dump` is the labeled value from the densified encoding map; `Encoded` is the raw step stored in SysEx. `~` means the step fell between labeled witnesses (rare once `provided` UI walks are merged).

| Parameter | Dump | Encoded | Sheet | Status |
|-----------|------|--------:|-------|--------|
| [reverb time](../../parameters/reverb-time.md) | 2.2 s | 40 | 2.20 | match |
| [size](../../parameters/size.md) | 28 | 28 | 28 | match |
| [predelay](../../parameters/predelay.md) | 10 ms | 5 | 10 | match |
| [diffusion](../../parameters/diffusion.md) | 7 | 7 | 7 | match |
| [density](../../parameters/density.md) | 2 | 2 | 2 | match |
| [modulation](../../parameters/modulation.md) | 4 | 5 | 4 | match |
| [rolloff](../../parameters/rolloff.md) | 5200 Hz | 27 | 5200 | match |
| [hf rt multiply](../../parameters/hf-rt-multiply.md) | 0.75 | 11 | 0.75 | match |
| [hf rt crossover](../../parameters/hf-rt-crossover.md) | 3200 Hz | 19 | 3200 | match |
| [lf rt multiply](../../parameters/lf-rt-multiply.md) | 1.2 | 20 | 1.20 | match |
| [lf rt crossover](../../parameters/lf-rt-crossover.md) | 800 Hz | 13 | 800 | match |
| [vlf cut](../../parameters/vlf-cut.md) | -12 dB | 8 | -12 | match |
| [early to reverb mix](../../parameters/early-to-reverb-mix.md) | 7/20 | 7 | 7/20 | match |
| [early rolloff](../../parameters/early-rolloff.md) | 10800 Hz | 41 | 10800 | match |
| [early select](../../parameters/early-select.md) | 13 | 13 | 17 | **hard** (Δ -4) |
| [delay level](../../parameters/delay-level.md) | off | 0 | — | not on sheet |
| [delay time](../../parameters/delay-time.md) | 100 ms | 0 | — | not on sheet |
| [delay modulation](../../parameters/delay-modulation.md) | off | 0 | — | not on sheet |

## Other presets in this bank

- **Large Hall** (this page)
- [Medium Hall](medium-hall.md)
- [Small Hall](small-hall.md)
- [Large & Near](large-and-near.md)
- [Medium & Near](medium-and-near.md)
- [Small & Near](small-and-near.md)
- [Large & Dark](large-and-dark.md)
- [Large & Deep](large-and-deep.md)
- [Medium & Deep](medium-and-deep.md)
- [Concert Hall](concert-hall.md)
- [Gold Hall](gold-hall.md)
- [Sandors Hall](sandors-hall.md)
- [Dense Hall](dense-hall.md)
- [Clear Hall](clear-hall.md)
- [Brass Hall](brass-hall.md)
- [Amsterdam Hall](amsterdam-hall.md)
- [Berliner Hall](berliner-hall.md)
- [Boston Hall A](boston-hall-a.md)
- [Boston Hall B](boston-hall-b.md)
- [Chicago Hall](chicago-hall.md)
- [Vienna Hall](vienna-hall.md)
- [Worcester Hall](worcester-hall.md)
- [The ArchDuke](the-archduke.md)
- [Troy Hall](troy-hall.md)
- [Saint Sylvain](saint-sylvain.md)
- [Mechanics Hall](mechanics-hall.md)
- [Saint Gerold](saint-gerold.md)
- [Pepes Hall A](pepes-hall-a.md)
- [Pepes Hall B](pepes-hall-b.md)
- [Reflect Hall A](reflect-hall-a.md)
- [Reflect Hall B](reflect-hall-b.md)
- [Piano Hall](piano-hall.md)

_Last exported: 2026-07-18_
