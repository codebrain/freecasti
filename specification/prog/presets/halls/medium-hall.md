[Overview](../../README.md) | [Bytes](../../bytes/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Medium Hall

_Generated 2026-07-19. Bank: [Halls](README.md) (index **0**). Source: `sysex/prog/presets/Halls.Medium Hall.syx`._

[All presets](../../README.md) · [Halls bank](README.md) · [Program identity](../../program-identity.md)

### Identity

| Field | Value |
|-------|-------|
| Bank | Halls (index 0) |
| Program slot | 1 |
| Name field | `Medium Hall` (matches filename) |
| Name window 8-87 (name + factory space pad) | match filename preset (ASCII space-padded) |
| Dump file | `Halls.Medium Hall.syx` |

> **Sheet discrepancies (2 hard):** dump values disagree with the [published preset sheet](../../preset-sheet.md). Highlighted in the Status column below. **SysEx dump is authoritative.**

> Hard = beyond tolerance (likely sheet print error or unit/firmware variance).

## Parameters

Decoded from independent `sysex/prog/parameters/<parameter>/` series. `Dump` is the labeled value from the densified encoding map; `Encoded` is the raw step stored in SysEx. `~` means the step fell between labeled witnesses (rare once `provided` UI walks are merged).

| Parameter | Dump | Encoded | Sheet | Status |
|-----------|------|--------:|-------|--------|
| [reverb time](../../bytes/reverb-time.md) | 1.8 s | 32 | 1.80 | match |
| [size](../../bytes/size.md) | 23 | 23 | 23 | match |
| [predelay](../../bytes/predelay.md) | 24 ms | 12 | 24 | match |
| [diffusion](../../bytes/diffusion.md) | 6 | 6 | 6 | match |
| [density](../../bytes/density.md) | 3 | 3 | 3 | match |
| [modulation](../../bytes/modulation.md) | 4 | 5 | 4 | match |
| [rolloff](../../bytes/rolloff.md) | 6000 Hz | 29 | 6400 | match |
| [hf rt multiply](../../bytes/hf-rt-multiply.md) | 0.75 | 11 | 0.75 | match |
| [hf rt crossover](../../bytes/hf-rt-crossover.md) | 3600 Hz | 20 | 4800 | **hard** (Δ -1200) |
| [lf rt multiply](../../bytes/lf-rt-multiply.md) | 1.2 | 20 | 1.20 | match |
| [lf rt crossover](../../bytes/lf-rt-crossover.md) | 800 Hz | 13 | 800 | match |
| [vlf cut](../../bytes/vlf-cut.md) | -10 dB | 10 | -10 | match |
| [early to reverb mix](../../bytes/early-to-reverb-mix.md) | 10/20 | 10 | 10/20 | match |
| [early rolloff](../../bytes/early-rolloff.md) | 8800 Hz | 36 | 8800 | match |
| [early select](../../bytes/early-select.md) | 17 | 17 | 13 | **hard** (Δ +4) |
| [delay level](../../bytes/delay-level.md) | off | 0 | — | not on sheet |
| [delay time](../../bytes/delay-time.md) | 100 ms | 0 | — | not on sheet |
| [delay modulation](../../bytes/delay-modulation.md) | off | 0 | — | not on sheet |

## Other presets in this bank

- [Large Hall](large-hall.md)
- **Medium Hall** (this page)
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

_Last exported: 2026-07-19_
