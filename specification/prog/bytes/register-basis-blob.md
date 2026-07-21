[Overview](../README.md) | [Bytes](../bytes/README.md) | [Program identity](../program-identity.md) | [Preset inventory](../preset-inventory.md) | [Preset sheet](../preset-sheet.md) | [Byte map](../byte-map-overview.md) | [Cross-series](../cross.md) | [System dumps](../../system/README.md)


# Register basis blob

_Generated 2026-07-21. Register hold-EDIT captures under `sysex/prog/edit/registers/` (fullsweep + witness samples) plus favorites captures under `sysex/prog/favorites/`. Layout table generated from `REGISTER_BLOB_FIELDS` in `m7_sysex.prog.register_blob`._

## SysEx summary

- **Offsets:** 24–87
- **Encoding:** `nibble_bitstream`
- **Confidence:** high
- **Role:** Bit-packed snapshot of the **stored register** (name, store counter, all 18 parameters incl. the V2 delay block); factory dumps space-pad this region with `0x20`
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

On Reg-backed hold-EDIT dumps, offsets **24–87** hold a snapshot of the register as it was **stored**. Read the low nibble of each byte (4 bits per byte, MSB first) as a 256-bit stream; the fields below were verified against every register-basis frame in the corpus (each matches the corresponding live payload field unless the register has unstored edits). For **register** bases the blob is untouched by live edits: payload bytes 100–139 track the edit buffer, the blob keeps the stored values (witness: `samples/charset-b1s1-rt5s-unstored-edit.syx`, where reverb time reads 5.0 s in the payload but the stored 1.0 s here). **Favorite** saves write the same blob layout (store counter always 0) and auto-commit pending edits on hold-PROG from the favorites screen — see the Favorites section below. Factory and parameter-series dumps space-pad this region (`0x20`), so check for nibble bytes before decoding.

## Bit layout

Bits count from the first nibble (offset 24 low nibble = bits 0–3). Field widths are provisional at boundaries where the leading bits were always zero in this corpus; positions/order are exact.

| Bits | Width | Field | Payload twin | Notes |
|------|------:|-------|--------------|-------|
| 0–83 | 84 | register name | [program name](program-name.md) @ 8–21 | 14 characters x 6-bit code (see charset table); matches the ASCII name at offsets 8-21 on every corpus capture |
| 84–95 | 12 | zero pad | — | Always 0 in witnessed captures |
| 96–100 | 5 | store-generation counter | — | Increments each time the register slot is overwritten (wire offsets 48-49) |
| 101–103 | 3 | constant 001 | — | Constant 1 in every witnessed register capture |
| 104–111 | 8 | predelay | [predelay](predelay.md) @ 104–105 |  |
| 112–119 | 8 | reverb time | [reverb time](reverb-time.md) @ 100–101 |  |
| 120–123 | 4 | diffusion | [diffusion](diffusion.md) @ 106–107 |  |
| 124–127 | 4 | density | [density](density.md) @ 108–109 |  |
| 128–133 | 6 | hf rt crossover | [hf rt crossover](hf-rt-crossover.md) @ 116–117 |  |
| 134–139 | 6 | lf rt multiply | [lf rt multiply](lf-rt-multiply.md) @ 118–119 |  |
| 140–143 | 4 | modulation | [modulation](modulation.md) @ 110–111 |  |
| 144–149 | 6 | early to reverb mix | [early to reverb mix](early-to-reverb-mix.md) @ 124–125 |  |
| 150–154 | 5 | vlf cut | [vlf cut](vlf-cut.md) @ 122–123 |  |
| 155–159 | 5 | early select | [early select](early-select.md) @ 128–129 |  |
| 160–161 | 2 | engine/bank-class flag | [engine/bank-class flag](engine-bank-class-flag.md) @ 130 | 0 classic banks, 1 on `* 2` banks, 2 NonLin (same as payload 130) |
| 162–168 | 7 | early rolloff | [early rolloff](early-rolloff.md) @ 126–127 |  |
| 169–175 | 7 | rolloff | [rolloff](rolloff.md) @ 112–113 |  |
| 176–181 | 6 | size | [size](size.md) @ 102–103 |  |
| 182–186 | 5 | hf rt multiply | [hf rt multiply](hf-rt-multiply.md) @ 114–115 |  |
| 187–191 | 5 | lf rt crossover | [lf rt crossover](lf-rt-crossover.md) @ 120–121 |  |
| 192–196 | 5 | source factory bank | [bank index mirror](bank-index.md) @ 136–137 | Factory bank the register was stored from (same as payload 136–137) |
| 197–200 | 4 | delay level | [delay level](delay-level.md) @ 132–133 | V2 delay block; located by samples/charset-b1s1-rt5s-stored.syx (reads 15) |
| 201–207 | 7 | delay time | [delay time](delay-time.md) @ 134–135 | V2 delay block; stored capture reads 11 |
| 208–211 | 4 | delay modulation | [delay modulation](delay-modulation.md) @ 138–139 | V2 delay block; stored capture reads 6 |
| 212–255 | 44 | zero tail | — | Always 0 in witnessed captures |

## Name charset (6-bit)

14 characters × 6-bit code, space-padded. Complete 64-entry charset, pinned down by `samples/charset-b1s1-renamed.syx` (register renamed to `&123456789ABCD`):

| Codes | Characters | Range | Status |
|-------|------------|-------|--------|
| 0 | ` ` | space | witnessed |
| 1 | `&` | `&` | witnessed |
| 2–11 | `0123456789` | digits `0`–`9` | code 2 (`0`) inferred by continuity; all others witnessed |
| 12–37 | `ABCDEFGHIJKLMNOPQRSTUVWXYZ` | uppercase `A`–`Z` | witnessed |
| 38–63 | `abcdefghijklmnopqrstuvwxyz` | lowercase `a`–`z` | witnessed |

## Store-generation counter

Bits 96–100 (wire offsets 48–49) increment each time the register slot is overwritten. Witness history:

- `fullsweep-rooms-studio-a.syx`: 3 for B0 R0–R2, 2 for B0 R3–B1 R1, 1 for all remaining registers — matching the corpus capture history exactly (the only non-identity bytes that vary inside the fullsweep).
- `samples/rooms-studio-a-b1s1-delay-edit.syx`: one more store to B1 R1 bumped its counter from 2 to 3 with the rest of the blob unchanged.
- `samples/charset-b1s1-renamed.syx`: reads 5 — renaming stores twice.
- `samples/charset-b1s1-rt5s-stored.syx`: targeted B1 R0 and reads exactly R0's expected next count, 3.

## Stored snapshot semantics

- **The blob snapshots the stored register values (not the factory source), delay block included.** After storing a program with reverb time edited to 5.0 s and the delay block engaged (`samples/charset-b1s1-rt5s-stored.syx`), the blob's reverb-time field reads encoded 76 (5.0 s, not the factory 10) and bits 197–211 carry delay level 15 / time 11 / mod 6, exactly matching the payload.
- **Zero delay tail with delay in the payload** (`samples/rooms-studio-a-b1s1-delay-edit.syx`) means the store happened *before* the delay was dialed in: the delay lived only in the edit buffer, not in the stored register.
- **Register identity at offsets 93/95 = the register currently loaded as the running basis** ([register bank](register-bank.md) / [register](register.md)). A store alone does **not** update them: the delay-edit and rename captures (stored to B1 R1 while the basis remained the factory program) read `0/0`, while `charset-b1s1-rt5s-stored.syx` reads `1/0` because B1 R0 was the active basis at dump time.
- **Consumers should prefer the blob over the payload when it is present.** The web UI does this on MIDI receive: when an incoming program dump carries a register basis frame, the stored blob values (and register name) replace the live payload bytes, so unstored edit-buffer values are not adopted (`applyRegisterBasis` in `web-ui/src/app/midiReceive.ts`). This stays safe for favorite bases: the blob converges on the committed slot values.

## Favorites carve-out

Front-panel **favorite** slots (`sysex/prog/favorites/`) reuse this blob layout with different lifecycle rules:

- A favorite save writes a full blob snapshot with the store-generation counter always **0** (re-saves do not increment it — favorites do not participate in the per-slot counter).
- Unstored edits stay payload-only per frame, but the favorite slot **auto-commits the edit buffer** (blob included) when a hold-PROG dump is taken while the favorites screen is displayed (offset 92 = `08`); waiting, a brief PROG press, and hold-PROG from other screens do not commit (witnesses: `nonlin-c/13-rt075-favscreen-hold-prog-commit.syx` vs captures 18/21).
- Offsets **93/95** stay register-only: a favorite basis does not update them. The favorite source is flagged at offset **94** instead ([favorite slot](favorite-slot.md)).

## Witness captures

All under `sysex/prog/edit/registers/`:

- `fullsweep-rooms-studio-a.syx` — 50 registers (Banks 0–4 × Registers 0–9), layout + store counter
- `samples/rooms-studio-a-b1s1-delay-edit.syx` — counter bump; delay in payload only (stored before the delay was dialed in)
- `samples/charset-b1s1-renamed.syx` — name `&123456789ABCD` pins charset codes 1–11
- `samples/charset-b1s1-rt5s-unstored-edit.syx` — unstored 5.0 s edit: payload diverges from blob
- `samples/charset-b1s1-rt5s-stored.syx` — stored 5.0 s + delay: blob updates; locates the delay block at bits 197–211

## Related

- [Program identity](../program-identity.md) — name / bank / slot overview
- [Register captures](../../../sysex/prog/edit/registers/README.md) — hold-EDIT register corpus
- [Owner’s manual notes](../../../docs/manual-notes.md)

_Last exported: 2026-07-21_
