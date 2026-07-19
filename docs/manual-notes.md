# Bricasti manual notes (SysEx context)

Hand-maintained notes from Bricasti’s published docs. These **do not** define
byte layouts — dumps and [../specification/](../specification/) remain authoritative.
Use this page to interpret captures and plan what to record next.

## Which document to read

| Document | What it gives this project |
|----------|----------------------------|
| [M7 Owner’s Manual (PDF)](https://www.bricasti.com/images/M7.pdf) | V1-era **UI**: parameter names, printed ranges, preset bank names, registers. Says MIDI “has no function for V1” — **thin on SysEx**. |
| [MIDI App Notes (PDF)](https://www.bricasti.com/images/Midi_app_note.pdf) | **SysEx workflow**: PROG / EDIT / SYSTEM dumps; full **bank index** table; program-change mapping. |
| [V2 Manual Addendum (PDF)](https://www.bricasti.com/images/M7_V2_Manual_Addendum_Upgrade.pdf) | **Firmware V2**: delay parameters, `* 2` banks, NonLin algorithm, Early Select 20–31, algorithm behavior. |
| [Preset sheet (PDF)](https://www.bricasti.com/images/preset_sheet.pdf) | Factory parameter values (parsed → [reference/preset_sheet.json](reference/preset_sheet.json)). Classic banks only — no Halls 2 / Plates 2 / etc. |

Printed ranges are catalog **hints** only — see [parameter-catalog.md](parameter-catalog.md).

## SysEx dump types

From Bricasti MIDI notes (all are **channel-less** SysEx):

| Dump | Send | Contents | This repo |
|------|------|----------|-----------|
| **Program** | Hold **PROG** | Running program + edits + **UI state**; may include register/favorite basis | **`sysex/prog/parameters/`** (series) and **`sysex/prog/presets/`** (identity) |
| **Edit buffer** | Hold **EDIT** | Same **157-byte** program-dump frame/header as PROG; bank word **88–89 = 11**, slot often **0**, mirror **137** keeps the source bank | **`sysex/prog/edit/`** |
| **System** | Hold **SYSTEM** | I/O, routing, dry/wet, register lock, etc. (not sound parameters) | **`sysex/system/`** — see [../specification/system/](../specification/system/) |

Program dumps explicitly carry UI/edit state — consistent with secondary movers at
offsets **92**, **98–99**, and **146–147** (`nibble_hilo` display) in
single-parameter series.

Bricasti MIDI notes say receiving an EDIT dump creates ephemeral bank **118**
(cleared on power-off). That is distinct from the **send** marker **11** observed
in hold-EDIT captures.

## Bank index (MIDI + dumps)

Factory/user bank select at SysEx offsets **88–89** (`nibble_hilo`); mirrored at
**137**. Confirmed against [program-identity.md](../specification/prog/program-identity.md).

| Index | Bank | Algorithm (manual) | Offset 130 (engine class) |
|------:|------|--------------------|---------------------------|
| 0 | Halls | V1 | 0 |
| 1 | Plates | V1 | 0 |
| 2 | Rooms | V1 | 0 |
| 3 | Chambers | V1 | 0 |
| 4 | Ambience | V1 | 0 |
| 5 | Spaces | V1 | 0 |
| 6 | Halls 2 | V2 | 1 |
| 7 | Plates 2 | V2 | 1 |
| 8 | Rooms 2 | V2 | 1 |
| 9 | Spaces 2 | V2 | 1 |
| 10 | NonLin | Non-linear (AMS-style) | **2** |
| **11** | **Edit (hold EDIT send)** | Same engine as source program | (source) |
| 118 | Edit (receive) | Ephemeral bank created when an EDIT dump is *received* | — |
| 119 | Favorites | Front-panel favorites 1–4 | — |
| 120 | Registers | User registers (5×10) | — |

On hold-**EDIT** sends, offsets **88–89** are always index **11**, while offset
**137** still equals the source bank’s low nibble (Rooms→2, Ambience→4, …).
Do not treat 11 as a factory bank in `prog/presets/` validation.

MIDI **program change** bank selects use the same indices (see MIDI app notes).

## Algorithms and byte-map hints

### V1 vs V2 (offset 97)

V2 addendum: classic banks use the **V1** reverb algorithm; **Halls 2 / Plates 2 /
Rooms 2 / Spaces 2** use the **V2** algorithm (same parameter set, different
character). Offset **97** (mirrored at **145**) is a **family / algorithm flag**,
not a user parameter and **not** a clean V1/V2 bit: Halls dumps are all **3**;
most other banks are **4**, with a few bank-leading presets also **3**
(Chambers Large Chamber, Plates Bright Plate, Rooms Studio A, Halls 2 Large
Hall). Mirror: **145=0** when **97=3**, **145=1** when **97=4**.

### Engine/bank-class flag (offset 130)

Offset **130** selects engine/bank class in this corpus:

| Value | Banks |
|------:|-------|
| 0 | Classic: Halls, Plates, Rooms, Chambers, Ambience, Spaces |
| 1 | `* 2`: Halls 2, Plates 2, Rooms 2, Spaces 2 |
| 2 | NonLin |

Parameter-series dumps also show **1** because they were captured from **Large
Church** (Halls 2). Companion **131–132** is always `02 00` here — see
[byte-map-overview.md](../specification/prog/byte-map-overview.md).

### Program slots (Rooms)

Most banks use contiguous slots from 0. **Rooms** uses slots **0–35**
(including **Long Wood Room** at 35). The V2 addendum lists 26 Rooms programs;
this unit has 36 (slots 25–34 fill names not in the addendum PDF).

### NonLin (bank 10)

V2 addendum: NonLin is a **separate simple algorithm** (inspired by AMS RMX 16).
Only these controls materially affect the sound:

- Rolloff
- Size
- Early Select
- Early/Reverb Mix (“Early Balance” in addendum)
- Early Rolloff

Other parameters may appear in dumps but are not part of the NonLin engine —
useful when validating decoded values. Factory preset names are spelled **Nonlin
A**…**D** on the unit (lowercase *lin*); filename `NonLin A.syx` is an export
convention.

### Early Select 20–31

Base manual lists **0–20**. V2 addendum adds **21–31** as larger early-reflection
variants (same early engine as V1). This unit’s captures use **0–31** at offsets
**128–129**.

### Delay block (V2+, offsets 133–139)

Added in firmware V2 on **all** presets (V1 and V2 algorithms):

- **Delay Level** — off or −20…−6 dB
- **Delay Time** — 100 ms…1 s (eight diffused voices into late reverb)
- **Delay Modulation** — off, low…high

Requires V2 firmware.

## Parameter semantics (manual vs SysEx)

| Parameter | Manual note | SysEx note |
|-----------|-------------|------------|
| Diffusion | “Percentage change from the **preset’s initial value**” | Stored as raw identity @ 107 in dumps — likely absolute encoding, UI-relative |
| HF / LF RT multiply | Scaling of **Reverb Time** | HF: `0.05×enc+0.2` confirmed; LF @ 118–119: 0.05 steps ≤ 2.0×, then 0.1 steps to 4.0× (captured) |
| Early/Reverb Mix | Two 0–20 ranges (early vs late) | Balance path **0…40** @ 124–125 (`A/B` UI; dumps named `A.B`) |
| VLF Cut | 0…−18 dB | This unit to **−20** @ 122–123 |
| Rolloff | LPF on overall late-reverb output; frequency only (no dB/oct) | Measures ≈ **12 dB/oct** (V1); V2 gentler — see [rolloff-slopes.md](rolloff-slopes.md) |
| Early Rolloff | Separate LPF for the early-reflection field | Measures ≈ **6 dB/oct** one-pole; displayed Hz is not the −3 dB corner — see [rolloff-slopes.md](rolloff-slopes.md) |

## System settings (SYSTEM menu)

Eight dedicated capture series under `sysex/system/`. Manual-aligned descriptions
are in `src/m7_sysex/system/catalog.py` and flow into
`specification/system/m7_system_dump.spec.json` and the web UI tooltips.

| Setting | Manual role | SysEx offsets |
|---------|-------------|---------------|
| Wet Gain | Internal wet (reverb) mix; normally Full with Dry Off for sidechain use | 8–9 |
| Dry Gain | Internal dry path; normally Off for sidechain; unity dry for mastering / I/O test | 10–11 |
| Audio Routing | Wet-path Mono L / Mono R / Stereo (dry stays stereo) | 13 |
| Audio Format | Analog vs AES digital I/O selection and lock behaviour | 15 |
| Output Level | Analog out trim in three steps (−8 / −16 / −24 dB on this unit) | 17 |
| Display Level | Front-panel brightness: Dim, 1, 2, 3, Bright | 21 |
| MIDI Channel | Program-change channel 1–16 or Omni (SysEx itself is channel-less) | 22–23 |
| MIDI Bank | MIDI program-change bank select | 25 |

**Offset 25 coupling:** dedicated **midi bank** captures use offset **25** as the
primary field (`m7_system_dump.ksy`, web UI, [midi-bank.md](../specification/system/bytes/midi-bank.md)).
**Display level** captures also move offset **25** as a secondary byte (see
[display-level.md](../specification/system/bytes/display-level.md)). The
byte-map export still labels offset 25 as padding until that secondary role is
fully reconciled.

## Header and identity fields

| Bytes | Status |
|-------|--------|
| **4–7** `70 08 01 00` | Program-dump family; **not** documented in manuals. Hold **EDIT** uses the same header/length |
| **8–23** | Program name: **16-byte** wire window; **14-character** editable label (manual); offsets **22–23** space-padded in this corpus |
| **24–87** | Factory: space-padded (`0x20`). Reg-backed hold-EDIT: nibble-packed **register basis blob** (unedited basis copy) |
| **93** | **`register_bank`** — manual Bank (`raw_u8`, B0–B4 = `00`–`04`); `00` on factory dumps |
| **94** | Constant `08` (structure/version) |
| **95** | **`register`** — manual Register within bank (`0`–`9`); `00` on factory dumps |
| **96** | Reserved/unknown (`00` in witnessed captures) |
| **EDIT** identity | Program bank **11** @ 88–89; source factory slot @ 90–91; source bank @ mirror **137**; see `sysex/prog/edit/` and `sysex/prog/edit/registers/` |
| **SYSTEM** layout | 77 bytes, header `70 08 02 00`; **8** settings captured — see [system/](../specification/system/) |

Register-basis hold-EDIT captures prove the full **5 Banks × 10 Registers**
inventory (`fullsweep-rooms-studio-a.syx`), plus earlier B0/B1 Large Hall and
Ambience/NonLin samples under [`sysex/prog/edit/registers/`](../sysex/prog/edit/registers/).
LCD `display` (146–147) does **not** encode Bank/Register (fullsweep fixed at
164). Partial blob decode: **50–55** ≈ predelay / reverb time / diffusion /
density; remainder of **24–47** / **56–72** still open. One Halls 2 capture with
atypical meta is documented as an outlier, not the primary path.

## Suggested captures (from manual + gaps)

All 18 sound parameters and **8** SYSTEM settings now have dedicated series.
Remaining optional work:

1. **EDIT receive path** — confirm MIDI-notes bank **118** when loading an EDIT
   dump back into the unit (distinct from send marker 11).
2. **Favorites**-based PROG dumps (bank **119**); finish mapping register basis
   blob **24–47** / **56–72**.
3. **Offset 25 secondary** — reconcile display-level secondary mover vs midi-bank
   primary in the byte-map export (Kaitai + web UI already model midi bank @ 25).
4. **SYSTEM** knobs not yet in dedicated series (e.g. register lock) if you
   need to edit them over SysEx.

## References in code

- Bank hints: `HINT_BANK_INDEX` / `EDIT_DUMP_BANK_INDEX` in `src/m7_sysex/prog/names.py`
- Printed ranges: `src/m7_sysex/prog/catalog.py`
- Corpus meta bytes (97 / 130 / reserved): `src/m7_sysex/prog/corpus_layout.py`
- SYSTEM hints: `src/m7_sysex/system/catalog.py`
- Name alias (`NonLin` → `Nonlin`): `check_name_bytes()` in `prog/names.py`
