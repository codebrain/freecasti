[Overview](../../README.md) | [Parameters](../../parameters/README.md) | **Program identity** | [Preset inventory](../../preset-inventory.md) | [Preset sheet](../../preset-sheet.md) | [Byte map](../../byte-map-overview.md) | [Cross-series](../../cross.md) | [System dumps](../../../system/README.md)


# Redwood Valley

_Generated 2026-07-18. Bank: [Spaces](README.md) (index **5**). Source: `sysex/prog/presets/Spaces.Redwood Valley.syx`._

[All presets](../../README.md) · [Spaces bank](README.md) · [Program identity](../../program-identity.md)

### Identity

| Field | Value |
|-------|-------|
| Bank | Spaces (index 5) |
| Program slot | 9 |
| Name field | `Redwood Valley` (matches filename) |
| Name bytes 8-87 | match filename preset (ASCII space-padded) |
| Dump file | `Spaces.Redwood Valley.syx` |

> **Sheet discrepancies (1 hard):** dump values disagree with the [published preset sheet](../../preset-sheet.md). Highlighted in the Status column below. **SysEx dump is authoritative.**

> Hard = beyond tolerance (likely sheet print error or unit/firmware variance).

## Parameters

Decoded from independent `sysex/prog/parameters/<parameter>/` series. `Dump` is the labeled value from the densified encoding map; `Encoded` is the raw step stored in SysEx. `~` means the step fell between labeled witnesses (rare once `provided` UI walks are merged).

| Parameter | Dump | Encoded | Sheet | Status |
|-----------|------|--------:|-------|--------|
| [reverb time](../../parameters/reverb-time.md) | 1.9 s | 34 | 1.90 | match |
| [size](../../parameters/size.md) | large | 30 | Large | match |
| [predelay](../../parameters/predelay.md) | 220 ms | 50 | 100 | **hard** (Δ +120) |
| [diffusion](../../parameters/diffusion.md) | 4 | 4 | 4 | match |
| [density](../../parameters/density.md) | 4 | 4 | 4 | match |
| [modulation](../../parameters/modulation.md) | low | 1 | low | match |
| [rolloff](../../parameters/rolloff.md) | 3200 Hz | 22 | 3200 | match |
| [hf rt multiply](../../parameters/hf-rt-multiply.md) | 0.6 | 8 | 0.60 | match |
| [hf rt crossover](../../parameters/hf-rt-crossover.md) | 3200 Hz | 19 | 3200 | match |
| [lf rt multiply](../../parameters/lf-rt-multiply.md) | 1.25 | 21 | 1.25 | match |
| [lf rt crossover](../../parameters/lf-rt-crossover.md) | 240 Hz | 4 | 240 | match |
| [vlf cut](../../parameters/vlf-cut.md) | -10 dB | 10 | -10 | match |
| [early to reverb mix](../../parameters/early-to-reverb-mix.md) | 20/20 | 20 | 20/20 | match |
| [early rolloff](../../parameters/early-rolloff.md) | full | 70 | full | match |
| [early select](../../parameters/early-select.md) | 19 | 19 | 19 | match |
| [delay level](../../parameters/delay-level.md) | off | 0 | — | not on sheet |
| [delay time](../../parameters/delay-time.md) | 100 ms | 0 | — | not on sheet |
| [delay modulation](../../parameters/delay-modulation.md) | off | 0 | — | not on sheet |

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
- **Redwood Valley** (this page)
- [Tanglewood](tanglewood.md)
- [Academy Yard](academy-yard.md)
- [Hillside](hillside.md)
- [Cavern](cavern.md)
- [Stone Quarry](stone-quarry.md)
- [Europa](europa.md)
- [Gated Space](gated-space.md)
- [Reflect Chapel](reflect-chapel.md)
- [Reflect Church](reflect-church.md)

_Last exported: 2026-07-18_
