[Overview](../../README.md) | [Bytes](../../bytes/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Kick Chamber

_Generated 2026-07-19. Bank: [Chambers](README.md) (index **3**). Source: `sysex/prog/presets/Chambers.Kick Chamber.syx`._

[All presets](../../README.md) · [Chambers bank](README.md) · [Program identity](../../program-identity.md)

### Identity

| Field | Value |
|-------|-------|
| Bank | Chambers (index 3) |
| Program slot | 7 |
| Name field | `Kick Chamber` (matches filename) |
| Name bytes 8-87 | match filename preset (ASCII space-padded) |
| Dump file | `Chambers.Kick Chamber.syx` |

> **Sheet discrepancies (1 soft):** dump values disagree with the [published preset sheet](../../preset-sheet.md). Highlighted in the Status column below. **SysEx dump is authoritative.**

> Soft = within table/rounding band (sparse-table interpolation or print rounding).

## Parameters

Decoded from independent `sysex/prog/parameters/<parameter>/` series. `Dump` is the labeled value from the densified encoding map; `Encoded` is the raw step stored in SysEx. `~` means the step fell between labeled witnesses (rare once `provided` UI walks are merged).

| Parameter | Dump | Encoded | Sheet | Status |
|-----------|------|--------:|-------|--------|
| [reverb time](../../bytes/reverb-time.md) | 0.7 s | 10 | 0.70 | match |
| [size](../../bytes/size.md) | 10 | 10 | 10 | match |
| [predelay](../../bytes/predelay.md) | 0 ms | 0 | 0 | match |
| [diffusion](../../bytes/diffusion.md) | 5 | 5 | 5 | match |
| [density](../../bytes/density.md) | 10 | 10 | h | match |
| [modulation](../../bytes/modulation.md) | 7 | 8 | 7 | match |
| [rolloff](../../bytes/rolloff.md) | 5600 Hz | 28 | 6400 | **soft** (Δ -800) |
| [hf rt multiply](../../bytes/hf-rt-multiply.md) | 0.9 | 14 | 0.90 | match |
| [hf rt crossover](../../bytes/hf-rt-crossover.md) | 4800 Hz | 22 | 4800 | match |
| [lf rt multiply](../../bytes/lf-rt-multiply.md) | 1 | 16 | 1.00 | match |
| [lf rt crossover](../../bytes/lf-rt-crossover.md) | 640 Hz | 11 | 640 | match |
| [vlf cut](../../bytes/vlf-cut.md) | -6 dB | 14 | -6 | match |
| [early to reverb mix](../../bytes/early-to-reverb-mix.md) | 20/20 | 20 | 20/20 | match |
| [early rolloff](../../bytes/early-rolloff.md) | 14000 Hz | 49 | 14000 | match |
| [early select](../../bytes/early-select.md) | 3 | 3 | 3 | match |
| [delay level](../../bytes/delay-level.md) | off | 0 | — | not on sheet |
| [delay time](../../bytes/delay-time.md) | 100 ms | 0 | — | not on sheet |
| [delay modulation](../../bytes/delay-modulation.md) | off | 0 | — | not on sheet |

## Other presets in this bank

- [Large Chamber](large-chamber.md)
- [Medium Chamber](medium-chamber.md)
- [Small Chamber](small-chamber.md)
- [Large & Dark](large-and-dark.md)
- [Small & Dark](small-and-dark.md)
- [Large & Bright](large-and-bright.md)
- [Small & Bright](small-and-bright.md)
- **Kick Chamber** (this page)
- [Snare Chamber](snare-chamber.md)
- [Vocal Chamber](vocal-chamber.md)
- [A&M Chamber](a-and-m-chamber.md)
- [CD Chamber](cd-chamber.md)
- [Old Chamber](old-chamber.md)
- [Deep Chamber](deep-chamber.md)
- [Amb Chamber A](amb-chamber-a.md)
- [Amb Chamber B](amb-chamber-b.md)
- [Sunset Chamber](sunset-chamber.md)
- [A&M Chamber B](a-and-m-chamber-b.md)
- [Stone Chamber](stone-chamber.md)
- [Tiled Chamber](tiled-chamber.md)
- [Fat Chamber](fat-chamber.md)
- [Echo Chamber](echo-chamber.md)

_Last exported: 2026-07-19_
