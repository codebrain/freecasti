[Overview](../../README.md) | [Bytes](../../bytes/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Large & Near

_Generated 2026-07-19. Bank: [Halls](README.md) (index **0**). Source: `sysex/prog/presets/Halls.Large & Near.syx`._

[All presets](../../README.md) · [Halls bank](README.md) · [Program identity](../../program-identity.md)

### Identity

| Field | Value |
|-------|-------|
| Bank | Halls (index 0) |
| Program slot | 3 |
| Name field | `Large & Near` (matches filename) |
| Name bytes 8-87 | match filename preset (ASCII space-padded) |
| Dump file | `Halls.Large & Near.syx` |

> **Sheet discrepancies (1 hard):** dump values disagree with the [published preset sheet](../../preset-sheet.md). Highlighted in the Status column below. **SysEx dump is authoritative.**

> Hard = beyond tolerance (likely sheet print error or unit/firmware variance).

## Parameters

Decoded from independent `sysex/prog/parameters/<parameter>/` series. `Dump` is the labeled value from the densified encoding map; `Encoded` is the raw step stored in SysEx. `~` means the step fell between labeled witnesses (rare once `provided` UI walks are merged).

| Parameter | Dump | Encoded | Sheet | Status |
|-----------|------|--------:|-------|--------|
| [reverb time](../../bytes/reverb-time.md) | 2.2 s | 40 | 2.20 | match |
| [size](../../bytes/size.md) | 20 | 20 | 20 | match |
| [predelay](../../bytes/predelay.md) | 10 ms | 5 | 10 | match |
| [diffusion](../../bytes/diffusion.md) | 7 | 7 | 7 | match |
| [density](../../bytes/density.md) | 2 | 2 | 2 | match |
| [modulation](../../bytes/modulation.md) | 4 | 5 | 4 | match |
| [rolloff](../../bytes/rolloff.md) | 6000 Hz | 29 | 6000 | match |
| [hf rt multiply](../../bytes/hf-rt-multiply.md) | 0.75 | 11 | 0.75 | match |
| [hf rt crossover](../../bytes/hf-rt-crossover.md) | 3200 Hz | 19 | 3200 | match |
| [lf rt multiply](../../bytes/lf-rt-multiply.md) | 1.1 | 18 | 1.10 | match |
| [lf rt crossover](../../bytes/lf-rt-crossover.md) | 720 Hz | 12 | 720 | match |
| [vlf cut](../../bytes/vlf-cut.md) | -11 dB | 9 | -11 | match |
| [early to reverb mix](../../bytes/early-to-reverb-mix.md) | 20/20 | 20 | 20/20 | match |
| [early rolloff](../../bytes/early-rolloff.md) | 10400 Hz | 40 | 10400 | match |
| [early select](../../bytes/early-select.md) | 14 | 14 | 20 | **hard** (Δ -6) |
| [delay level](../../bytes/delay-level.md) | off | 0 | — | not on sheet |
| [delay time](../../bytes/delay-time.md) | 100 ms | 0 | — | not on sheet |
| [delay modulation](../../bytes/delay-modulation.md) | off | 0 | — | not on sheet |

## Other presets in this bank

- [Large Hall](large-hall.md)
- [Medium Hall](medium-hall.md)
- [Small Hall](small-hall.md)
- **Large & Near** (this page)
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

_Last exported: 2026-07-19_
