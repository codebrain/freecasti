[Overview](../../README.md) | [Bytes](../../bytes/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Bath House

_Generated 2026-07-19. Bank: [Spaces](README.md) (index **5**). Source: `sysex/prog/presets/Spaces.Bath House.syx`._

[All presets](../../README.md) · [Spaces bank](README.md) · [Program identity](../../program-identity.md)

### Identity

| Field | Value |
|-------|-------|
| Bank | Spaces (index 5) |
| Program slot | 6 |
| Name field | `Bath House` (matches filename) |
| Name region 8-87 | match filename preset (ASCII space-padded) |
| Dump file | `Spaces.Bath House.syx` |

> **Sheet discrepancies (1 hard):** dump values disagree with the [published preset sheet](../../preset-sheet.md). Highlighted in the Status column below. **SysEx dump is authoritative.**

> Hard = beyond tolerance (likely sheet print error or unit/firmware variance).

## Parameters

Decoded from independent `sysex/prog/parameters/<parameter>/` series. `Dump` is the labeled value from the densified encoding map; `Encoded` is the raw step stored in SysEx. `~` means the step fell between labeled witnesses (rare once `provided` UI walks are merged).

| Parameter | Dump | Encoded | Sheet | Status |
|-----------|------|--------:|-------|--------|
| [reverb time](../../bytes/reverb-time.md) | 3.9 s | 65 | 3.90 | match |
| [size](../../bytes/size.md) | 15 | 15 | 15 | match |
| [predelay](../../bytes/predelay.md) | 6 ms | 3 | 6 | match |
| [diffusion](../../bytes/diffusion.md) | 9 | 9 | 9 | match |
| [density](../../bytes/density.md) | 6 | 6 | 6 | match |
| [modulation](../../bytes/modulation.md) | low | 1 | low | match |
| [rolloff](../../bytes/rolloff.md) | 8800 Hz | 36 | 8800 | match |
| [hf rt multiply](../../bytes/hf-rt-multiply.md) | 0.85 | 13 | 0.85 | match |
| [hf rt crossover](../../bytes/hf-rt-crossover.md) | 1000 Hz | 11 | 1000 | match |
| [lf rt multiply](../../bytes/lf-rt-multiply.md) | 0.35 | 3 | 0.35 | match |
| [lf rt crossover](../../bytes/lf-rt-crossover.md) | 640 Hz | 11 | 640 | match |
| [vlf cut](../../bytes/vlf-cut.md) | -20 dB | 0 | -20 | match |
| [early to reverb mix](../../bytes/early-to-reverb-mix.md) | 16/20 | 16 | 16/20 | match |
| [early rolloff](../../bytes/early-rolloff.md) | full | 70 | full | match |
| [early select](../../bytes/early-select.md) | 19 | 19 | 25 | **hard** (Δ -6) |
| [delay level](../../bytes/delay-level.md) | off | 0 | — | not on sheet |
| [delay time](../../bytes/delay-time.md) | 100 ms | 0 | — | not on sheet |
| [delay modulation](../../bytes/delay-modulation.md) | off | 0 | — | not on sheet |

## Other presets in this bank

- [North Church](north-church.md)
- [East Church](east-church.md)
- [South Church](south-church.md)
- [West Church](west-church.md)
- [Cinema Room](cinema-room.md)
- [Scoring Stage](scoring-stage.md)
- **Bath House** (this page)
- [Car Park](car-park.md)
- [Arena](arena.md)
- [Redwood Valley](redwood-valley.md)
- [Tanglewood](tanglewood.md)
- [Academy Yard](academy-yard.md)
- [Hillside](hillside.md)
- [Cavern](cavern.md)
- [Stone Quarry](stone-quarry.md)
- [Europa](europa.md)
- [Gated Space](gated-space.md)
- [Reflect Chapel](reflect-chapel.md)
- [Reflect Church](reflect-church.md)

_Last exported: 2026-07-19_
