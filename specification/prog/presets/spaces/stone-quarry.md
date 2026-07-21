[Overview](../../README.md) | [Bytes](../../bytes/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Stone Quarry

_Generated 2026-07-21. Bank: [Spaces](README.md) (index **5**). Source: `sysex/prog/presets/Spaces.Stone Quarry.syx`._

[All presets](../../README.md) · [Spaces bank](README.md) · [Program identity](../../program-identity.md)

### Identity

| Field | Value |
|-------|-------|
| Bank | Spaces (index 5) |
| Program slot | 14 |
| Name field | `Stone Quarry` (matches filename) |
| Name window 8-87 (name + factory space pad) | match filename preset (ASCII space-padded) |
| Dump file | `Spaces.Stone Quarry.syx` |

> **Sheet discrepancies (1 hard):** dump values disagree with the [published preset sheet](../../preset-sheet.md). Highlighted in the Status column below. **SysEx dump is authoritative.**

> Hard = beyond tolerance (likely sheet print error or unit/firmware variance).

## Parameters

Decoded from independent `sysex/prog/parameters/<parameter>/` series. `Dump` is the labeled value from the densified encoding map; `Encoded` is the raw step stored in SysEx. `~` means the step fell between labeled witnesses (rare once `provided` UI walks are merged).

| Parameter | Dump | Encoded | Sheet | Status |
|-----------|------|--------:|-------|--------|
| [reverb time](../../bytes/reverb-time.md) | 5.1 s | 77 | 5.10 | match |
| [size](../../bytes/size.md) | 15 | 15 | 15 | match |
| [predelay](../../bytes/predelay.md) | 0 ms | 0 | 0 | match |
| [diffusion](../../bytes/diffusion.md) | 2 | 2 | 1 | **hard** (Δ +1) |
| [density](../../bytes/density.md) | 0 | 0 | low | match |
| [modulation](../../bytes/modulation.md) | low | 1 | low | match |
| [rolloff](../../bytes/rolloff.md) | 3600 Hz | 23 | 3600 | match |
| [hf rt multiply](../../bytes/hf-rt-multiply.md) | 0.65 | 9 | 0.65 | match |
| [hf rt crossover](../../bytes/hf-rt-crossover.md) | 800 Hz | 10 | 800 | match |
| [lf rt multiply](../../bytes/lf-rt-multiply.md) | 4 | 56 | 4.00 | match |
| [lf rt crossover](../../bytes/lf-rt-crossover.md) | 200 Hz | 3 | 200 | match |
| [vlf cut](../../bytes/vlf-cut.md) | 0 dB | 20 | 0 | match |
| [early to reverb mix](../../bytes/early-to-reverb-mix.md) | 13/20 | 13 | 13/20 | match |
| [early rolloff](../../bytes/early-rolloff.md) | 12000 Hz | 44 | 12000 | match |
| [early select](../../bytes/early-select.md) | 19 | 19 | 19 | match |
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
- [Bath House](bath-house.md)
- [Car Park](car-park.md)
- [Arena](arena.md)
- [Redwood Valley](redwood-valley.md)
- [Tanglewood](tanglewood.md)
- [Academy Yard](academy-yard.md)
- [Hillside](hillside.md)
- [Cavern](cavern.md)
- **Stone Quarry** (this page)
- [Europa](europa.md)
- [Gated Space](gated-space.md)
- [Reflect Chapel](reflect-chapel.md)
- [Reflect Church](reflect-church.md)

_Last exported: 2026-07-21_
