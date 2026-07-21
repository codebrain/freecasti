[Overview](README.md) | [Bytes](bytes/README.md) | [Program identity](program-identity.md) | [Preset inventory](preset-inventory.md) | [Preset sheet](preset-sheet.md) | [Byte map](byte-map-overview.md) | [Cross-series](cross.md) | [System dumps](../system/README.md)

# Cross-series analysis

Cross analysis does not transfer absolute parameter values between folders. Each sysex/prog/parameters/<parameter>/ stream remains independent; this pass only looks for stable bytes, recurrent movers, claim conflicts, untouched offsets, and checksum hypotheses across the message corpus.

Corpus: **157** messages from **18** independent series (`delay level`, `delay modulation`, `delay time`, `density`, `diffusion`, `early rolloff`, `early select`, `early to reverb mix`, `hf rt crossover`, `hf rt multiply`, `lf rt crossover`, `lf rt multiply`, `modulation`, `predelay`, `reverb time`, `rolloff`, `size`, `vlf cut`).

Run standalone with `python -m m7_sysex cross` (also included in `python -m m7_sysex export`).

### Stable bytes (identical in every captured message)

**105** offsets never change in this corpus (22 of those are in the payload before the checksum).

Stable payload offsets: `88`, `90`, `93-96`, `106`, `108`, `110`, `131-132`, `136`, `138`, `140-144`, `148-151`

_Stable-in-corpus ≠ immutable forever - only unused or fixed in these captures._

### Recurrent secondary movers

Offsets that moved as non-primary fields in **two or more** independent series (likely shared edit/UI/state, not a sound parameter):

_None yet._

### Primary offset conflicts

No primary-offset conflicts between series.

### Untouched in parameter series

**25** payload offsets never changed in any independent `sysex/prog/parameters/<name>/` capture series:

`88-91`, `93-99`, `130-131`, `136-137`, `140-145`, `148-151`

Many of these are already documented elsewhere — program identity (offsets 88–91), fixed/reserved fields, and corpus-derived meta — see [byte-map-overview.md](byte-map-overview.md). This list means no dedicated single-parameter series has moved them yet, not that the byte map is unknown.

### Checksum hypotheses

**Verified:** `CRC-16/ARC` (also CRC-16/IBM, CRC-16/ANSI).

- Cover: offsets 8..151 (name window + register-basis blob + payload as stored)
- Exclude: F0, manufacturer ID, header 70 08 01 00, checksum, F7
- Poly/init: 0x8005 (reflected 0xA001), init 0x0000, refin=True, refout=True, xorout=0x0000
- Pack: 16-bit CRC as four high-nibble-first SysEx bytes

Hypotheses that fit **all** messages (273 tried):

- `id16(crc16_arc[8:cs))/nibs_be` - id16 of crc16_arc[8:cs), packed as nibs_be (verified cover)
- `id16(crc16_arc[8:cs))/u16_be_nibs` - id16 of crc16_arc[8:cs), packed as u16_be_nibs (verified cover)


_Last exported: 2026-07-22_
