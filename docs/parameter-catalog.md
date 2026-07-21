# M7 parameter catalog (hint only)

Published Bricasti ranges are a **starting hint for capture
planning**, not ground truth for every unit. Firmware and hardware variation
are real — this project’s M7 has **Early Select 0–31** while the manual prints
**0–20**, **Size 0–30** vs printed 1–24, and so on.

**Authoritative source:** labeled `.syx` dumps from *your* unit + generated
docs in [../specification/](../specification/).
**Machine-readable hints:** `src/m7_sysex/prog/catalog.py` (annotates series with an
`official` block; never overrides encodings or offsets).

## Sources

- Bricasti M7 Owner’s Manual — printed control ranges (V1-era UI; MIDI section
  obsolete pre-V2)
  ([M7.pdf](https://www.bricasti.com/images/M7.pdf))
- Bricasti [MIDI App Notes](https://www.bricasti.com/images/Midi_app_note.pdf) /
  [V2 addendum](https://www.bricasti.com/images/M7_V2_Manual_Addendum_Upgrade.pdf)
  — dump types (PROG / EDIT / SYSTEM); bank index; V2 delay; algorithms
- Consolidated notes: [manual-notes.md](manual-notes.md)
- [Bricasti preset sheet PDF](https://www.bricasti.com/images/preset_sheet.pdf)
  — factory preset value tables (parsed into
  [reference/preset_sheet.json](reference/preset_sheet.json))

## Program parameters (menu order)

| Parameter | Printed hint | This unit (dumps) | Folder |
|-----------|--------------|-------------------|--------|
| Reverb Time | 0.1 – 30 s | 0.2 – 30 s, **table** @ 100–101 | `reverb time` |
| Size | Small 1 – 24 Large | Small…Large = **0…30** identity @ 102–103 | `size` |
| Pre Delay | 0 – 500 ms | 0 – 500 ms, **table** @ 104–105 | `predelay` |
| Diffusion | Low 1 – 9 High | **0…10** identity `nibble_hilo` @ 106–107 | `diffusion` |
| Density | Low 1 – 9 High | **0…10** identity `nibble_hilo` @ 108–109 | `density` |
| Modulation | Off, Low 1 – 9 High | off + **0…10** (`enc−1`) `nibble_hilo` @ 110–111 | `modulation` |
| Rolloff | 80 Hz – 28 kHz | 80 – 22000 Hz (+`full`), **table** @ 112–113 | `rolloff` |
| HF RT Multiply | 0.2 – 1.0 | `0.05×enc+0.2` @ 114–115 | `hf rt multiply` |
| HF RT Crossover | 200 Hz – 16 kHz | **table** @ 116–117 | `hf rt crossover` |
| LF RT Multiply | 0.2 – 4.0× | **table** @ 118–119: 0.05/step ≤ 2.0×, 0.1/step above | `lf rt multiply` |
| LF RT Crossover | 80 Hz – 4.8 kHz | 80 – 4800 Hz, **table** @ 120–121 | `lf rt crossover` |
| VLF Cut | 0 – −18 dB | **−20…0** dB (`enc−20`) @ 122–123 | `vlf cut` |
| Early/Reverb Mix | 0/20 … 20/20 … 20/0 | balance positions **0…40** @ 124–125; dumps named `A.B` (= `A/B`) | `early to reverb mix` |
| Early Rolloff | 80 Hz – 20 kHz | 80 – 22000 Hz, **table** @ 126–127 | `early rolloff` |
| Early Select | 0 – 20 | **0…31** identity @ 128–129 | `early select` |
| Delay Level | Off, or −20 – −6 dB | off + −20…−6 (`enc−21`) `nibble_hilo` @ 132–133 | `delay level` |
| Delay Time | 100 ms – 1 s | 100 – **996** ms (`8×enc+100`) @ 134–135 | `delay time` |
| Delay Modulation | Off, Low 1 – 9 High | off + **0…10** (`enc−1`) `nibble_hilo` @ 138–139 | `delay modulation` |

When a capture exceeds the printed range, keep the dump labels — update
`observed_*` in `catalog.py` if the wider span is confirmed on this unit.

Full dump tables and how-to-set notes:
[../specification/prog/bytes/](../specification/prog/bytes/).

## Program identity (not a sound parameter)

From `sysex/prog/presets/` dumps named `<bank>.<preset>.syx` — see
[../specification/prog/program-identity.md](../specification/prog/program-identity.md).
Decoded factory values are also checked against Bricasti’s published sheet
([preset-sheet.md](../specification/prog/preset-sheet.md); data in
[reference/preset_sheet.json](reference/preset_sheet.json)).

| Field | Offsets | Notes |
|-------|---------|-------|
| Program name | 8–23 | ASCII space-padded within 16-byte window; factory filename check also requires 24–87 spaces |
| Register basis blob | 24–87 | Factory: `0x20` spaces. Reg EDIT: nibble-packed unedited basis (`sysex/prog/edit/registers/`) |
| Bank index | 88–89 | `nibble_hilo` — full table in [manual-notes.md](manual-notes.md) |
| Program slot | 90–91 | Slot within bank (factory list order); on Reg EDIT this stays the *source factory* slot |
| Register page | 93 | Reg bank page (B0=0 …); `0` on factory dumps |
| Favorite slot | 94 | `(slot-1)*2` for favorites 1–4 on favorite-loaded PROG frames; `08` = not from a favorite (`sysex/prog/favorites/`) |
| Register slot | 95 | Reg slot 0–9; `0` on factory dumps |
| Bank mirror | 136–137 | `nibble_hilo`; equals bank word 88–89 (source bank on hold-EDIT) |
| Algorithm/family flag | 96–97 / 144–145 | `nibble_hilo` (96 and 144 always `00`); Halls≈3 / most others≈4; not a clean V1/V2 bit — see manual-notes |
| Engine/bank-class flag | 130 | `0` classic, `1` `* 2`, `2` NonLin; companion 131 = `02` |

## Algorithms (manual context)

| Family | Banks | Active parameters (manual) |
|--------|-------|----------------------------|
| V1 reverb | Halls, Plates, Rooms, Chambers, Ambience, Spaces | Full parameter menu (18 controls + delay on V2 firmware) |
| V2 reverb | Halls 2, Plates 2, Rooms 2, Spaces 2 | Same controls, different algorithm character |
| NonLin | NonLin (index 10) | **Rolloff, Size, Early Select, Early/Reverb Mix, Early Rolloff only** |

NonLin and V1/V2 behavior explain why some decoded preset fields may sit at
defaults without affecting sound. Details: [manual-notes.md](manual-notes.md).

## System settings (not program parameters)

Captured while holding **SYSTEM** on the M7. Full tables:
[../specification/system/bytes/](../specification/system/bytes/).

| Setting | Offsets | Notes |
|---------|---------|-------|
| Wet Gain | 8–9 | `nibble_hilo`; Off / −60…0 dB (Full) in 0.5 dB steps |
| Dry Gain | 10–11 | Same encoding as wet gain |
| Audio Routing | 13 | Stereo / Mono L / Mono R (`raw_u8`) |
| Audio Format | 15 | Analog / Digital (`raw_u8`) |
| Output Level | 17 | Analog out trim: −8 / −16 / −24 dB (`raw_u8`; three steps only) |
| Display Level | 21 | Dim / 1 / 2 / 3 / Bright (`raw_u8`; offset 25 also moves in this series) |
| MIDI Channel | 22–23 | Channels 1–16 or Omni (`nibble_hilo`) |
| MIDI Bank | 25 | Program-change bank select (`raw_u8`); in [midi-bank.md](../specification/system/bytes/midi-bank.md), `m7_system_dump.ksy`, and the web UI (offset 25 also moves in display-level captures) |

User-facing descriptions (from the owner’s manual / MIDI notes) live in
`src/m7_sysex/system/catalog.py` and appear in the machine spec and web UI
tooltips after `python run.py`.

The 77-byte SYSTEM layout has no unknown payload bytes in this corpus — see
[../specification/system/byte-map.md](../specification/system/byte-map.md).

## Display conventions

### Early / Reverb Mix (`A.B` balance)

Printed **0–20 / 0–20** balance path. Analyzer maps `(0,20)→(20,20)→(20,0)` to
positions `0…40`.

### Cuts in dB

Zero and negative-only (`0db`, `-1db`, …). Printed VLF floor −18 dB; this unit
has shown −20. Delay Level uses discrete **off** below −20.

### Diffusion (UI vs dump)

The owner’s manual describes diffusion as a **percentage change from the preset’s
built-in initial value**. SysEx stores an absolute encoded value as
`nibble_hilo` @ 106–107 — treat dumps as absolute; UI semantics may be relative
to the factory preset base.

### HF/LF RT multiply

HF multiply is a clean affine (`0.05×enc + 0.2`, 0.2–1.0×). LF multiply covers
0.2–4.0× with **non-uniform steps**: 0.05 per encoded step up to 2.0×
(enc 36), then 0.1 per step to 4.0× (enc 56) — a table, not a single affine.
Factory presets only exercise the ≤ 2.0× region, which is why the sheet
inference originally looked affine.

### Size / Modulation endpoints

Size uses **Small** / numbers / **Large** (aliases of low/high). Modulation and
Delay Modulation use **Off**, **Low**, numbers, **High**.

### Table vs affine

Hz and time controls often use **non-linear tables** (edge slopes disagree:
fine steps at one end, coarse at the other). Agreeing edge slopes → closed-form
affine map (`label = a×encoded + b`).

## MIDI / dump workflow reminders

- Program dump: hold **PROG** — preferred here
- Edit buffer dump: hold **EDIT**
- System dump: hold **SYSTEM** — I/O / system only
- SysEx is channel-less; dedicated physical MIDI port recommended
- Firmware **v2+** required for the Delay parameters

## How this helps reverse engineering

1. Read [manual-notes.md](manual-notes.md) for bank table, dump types, algorithms.
2. All 18 program parameters have dedicated capture series; densify sparse
   tables when you need finer decode resolution.
3. Expect display families: identity, dB cuts, Hz/time tables, balance `A.B`,
   multiply scales, off+integer.
4. Soft catalog notes after `export` when extremes differ from the hint — never
   override dumps.
5. Cross-check factory dumps against the published sheet
   ([preset-sheet.md](../specification/prog/preset-sheet.md)); dumps win on hard
   disagreements.
6. Do not treat third-party controller UIs as a source of byte offsets.
7. Optional: EDIT/Favorites *receive* confirmation and rarely used SYSTEM
   knobs (e.g. register lock) per [manual-notes.md](manual-notes.md).
   (Favorites-based sends and the register basis blob are fully decoded —
   `sysex/prog/favorites/` and
   [register-basis-blob.md](../specification/prog/bytes/register-basis-blob.md).)
