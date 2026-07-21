# Capture guide

How to collect SysEx dumps from a Bricasti M7 for this project.

## MIDI setup

1. Connect M7 MIDI Out → computer MIDI In (interface or USB MIDI).
2. On the M7, open **SYSTEM** and confirm MIDI is enabled.
3. SysEx dumps do **not** use the MIDI channel setting (channel is only for
   program changes).
4. Use any SysEx librarian that can save a received message as `.syx` (MIDI-OX,
   SysEx Librarian, Elektron Transfer, DAW SysEx capture, etc.).

Official overview:
[Bricasti M7 MIDI App Notes](https://www.bricasti.com/images/Midi_app_note.pdf).

## Dump types (from Bricasti)

| Dump | How to send | Use for this project |
|------|-------------|----------------------|
| **Program dump** | Hold **PROG** briefly | **Preferred** — full running program + edits + UI state |
| Edit buffer dump | Hold **EDIT** briefly | Same 157-byte frame as PROG; bank **88–89 = 11**, mirror **136–137** = source bank — keep under `sysex/prog/edit/` |
| System dump | Hold **SYSTEM** briefly | I/O / system config only — not program parameters |

**Favorites caution:** holding **PROG** while the favorites screen is displayed
(offset 92 = `08`) silently **commits pending edits into the favorite slot** —
see [Favorites captures](#favorites-captures-sysexprogfavorites) below.

Program dumps include UI/edit state (Bricasti MIDI notes) — expect offsets **146–147**
as one **`nibble_hilo` display** field (browse = menu-row highlight; edit = value-focus
band that moves with the shown value), plus **92**
(panel-mode flag) and **98–99** (menu index) for menu browse/edit, even in
single-parameter series.

This repo expects **program dumps** for parameter series and `sysex/prog/presets/`.
EDIT captures go in `sysex/prog/edit/` (excluded from the PROG corpus scan). See
[manual-notes.md](manual-notes.md) for bank context.

## Bank index (for `sysex/prog/presets/` naming)

SysEx offsets **88–89** / mirror **136–137** use these factory bank indices (from
[Bricasti MIDI app notes](https://www.bricasti.com/images/Midi_app_note.pdf)):

| Index | Bank |
|------:|------|
| 0 | Halls |
| 1 | Plates |
| 2 | Rooms |
| 3 | Chambers |
| 4 | Ambience |
| 5 | Spaces |
| 6 | Halls 2 |
| 7 | Plates 2 |
| 8 | Rooms 2 |
| 9 | Spaces 2 |
| 10 | NonLin |
| **11** | **Edit** (hold **EDIT** send — bank word only; mirror 136–137 stays source bank) |
| 118 | Edit (ephemeral on *receive*, per MIDI notes) |
| 119 | Favorites (*receive only* — favorite-loaded PROG sends carry the source bank here, with the favorite slot at offset **94**; see `sysex/prog/favorites/`) |
| 120 | Registers |

Filename convention stays `<bank name>.<preset name>.syx` (e.g. `NonLin.NonLin A.syx`).
Factory NonLin presets spell **Nonlin** on the unit; the analyzer accepts that alias.

**Validation:** every preset dump is checked before decode — offsets **8–87**
must match the filename preset (ASCII space-padded), and offsets **88–89** must
match the filename bank name (see table above, indices **0–10** only). A mismatch
fails the export with an error naming the file. Do not put hold-EDIT dumps
(bank 11) in `sysex/prog/presets/`.

## Single-parameter method

Goal: every file in **one** folder differs in **exactly one** sound parameter
(plus inevitable checksum / status bytes).

Each `sysex/prog/parameters/<parameter>/` folder is an **independent stream**. Do not
byte-compare dumps across folders — other parameters may have drifted between
capture sessions.

1. Load a stable starting program (factory preset is fine).
2. Note the program name; keep it identical across **this** series.
3. Set the target parameter to value A.
4. Send a program dump; save as `<value><unit>.syx` (example: `0ms.syx`).
5. Change **only** that parameter to value B.
6. Dump again (`100ms.syx`, …).
7. Repeat across the useful range (include endpoints and several midpoints).
8. Keep the whole series in its own folder (`sysex/prog/parameters/predelay/`, …).

### Naming rules

- Prefer **extremes + adjacent-to-extremes + sample mids**: usable min and max,
  one step in from each, and a few values in between
- Mid dumps are a **sparse sample only** — not every intermediate setting; do
  not infer missing steps from gaps between mid filenames
- Optional discrete **OFF**: `off.syx`
- Extremes: `low.syx` / `high.syx` / `full.syx` / `small.syx` / `large.syx`, or
  numeric extremes (`0db.syx`, `-20db.syx`, `80hz.syx`, `0.2s.syx`, …)
- **Balance/mix displays** (early/reverb): on-device / sheet show `A/B`
  (`0/20` … `20/20` … `20/0`). Filenames cannot contain `/`, so dumps use a
  dot: `0.20.syx` … `20.20.syx` … `20.6.syx` … `20.0.syx` (`20.6` = `20/6`,
  not the float 20.6)
- Units glued to the value: `80hz`, `500ms`, `0.2s`, `-6dB`, `50%`
  (case-insensitive)
- Some controls are **0 and negative only** (VLF cut): `0db.syx` … `-20db.syx`
- Bare numbers (`1.syx`) when the control has no unit
- Pure on/off: `on.syx` / `off.syx`
- Avoid spaces in **parameter** filenames (preset names in `prog/presets/` may contain
  spaces)
- One parameter per folder

The analyzer uses extremes and adjacent-to-extreme dumps to decide between
closed-form scales (when both edges share the same dlabel/dencoded) and
table/index maps (when the edge slopes disagree). Sample mids confirm the fit;
gaps between mids are expected.

### Quality tips

- Do not touch other knobs between dumps in the same series.
- If you bump something by accident, restart the series from the same base
  program.
- Capture at least **5–8** values for continuous parameters; more near
  discontinuities.
- For **table** candidates (predelay, reverb time, rolloff, crossovers, early
  rolloff), denser sampling at both ends helps confirm the index map — there is
  no single global ms-per-step or Hz-per-step.
- Keep raw `.syx` files; never hand-edit them before analysis.

## Running the analyzer

```bash
pip install -e .   # optional
python run.py
```

Open `sysex/prog/parameters/<parameter>/analysis.json` and
`specification/prog/bytes/<slug>.md`, and check:

1. `changing_offsets` — should be small (parameter + checksum ± maybe one status
   byte; **146–147** often move together as the `nibble_hilo` display)
2. `best_encoding` — mapping table from label → encoded value
3. `hypothesis.confidence` — `high` when a closed-form scale fits; `medium` is
   normal for monotonic tables

If many offsets change, another parameter (or the program name) shifted —
recapture.

## Preset identity captures (`sysex/prog/presets/`)

To reverse-engineer **program name**, **bank index**, and **program slot**, dump
whole factory (or user) presets into `sysex/prog/presets/` named:

```text
<bank name>.<preset name>.syx
```

Examples: `Halls.Large Hall.syx`, `Plates.Bright Plate.syx`,
`Halls 2.Large Hall.syx`.

- Split on the **first** `.` — bank left, preset right
- For **factory** presets, SysEx offsets **8–87** must equal the preset half as
  ASCII, space-padded to 80 bytes (display name is **8–23**; **24–87** is spaces).
  Bank name is **not** stored in the name field
- Capture several banks and several slots within one bank (factory order helps)
- Folders starting with `_` are meta series — not treated as parameters

Results land under
[../specification/prog/presets/](../specification/prog/presets/) (bank pages +
[presets.json](../specification/prog/presets/presets.json)),
[../specification/prog/program-identity.md](../specification/prog/program-identity.md), and
[../specification/prog/preset-sheet.md](../specification/prog/preset-sheet.md) (errata vs the
[published preset sheet](https://www.bricasti.com/images/preset_sheet.pdf),
using [reference/preset_sheet.json](reference/preset_sheet.json)).

## PROG menu navigation (`sysex/prog/menus/`)

To decode front-panel **menu highlight** bytes (offsets **92**, **98–99**, **146–147**
`nibble_hilo` display) without changing sound parameters:

1. Load a stable program; keep parameter values fixed for the whole series.
2. Dump with **no parameter menu open** → `no menu.syx` (idle baseline).
3. For each parameter: highlight that menu **only** (do not turn the encoder) →
   PROG dump → `sysex/prog/menus/<folder_hint>.syx` (lowercase; matches
   `sysex/prog/parameters/<folder_hint>/`).
4. Re-run `python run.py`.

The analyzer writes `sysex/prog/menus/analysis.json` and
`prog_ui_state.json`, and exports [ui-state.md](../specification/prog/ui-state.md).

**SYSTEM menu highlight** does not change SYSTEM dump bytes (confirmed with
`sysex/system/menus/` captures). Register lock still needs value-change series,
not menu-navigation dumps.

## Favorites captures (`sysex/prog/favorites/`)

Front-panel favorites (the four shortcut buttons) are decoded from the session
in [sysex/prog/favorites/README.md](../sysex/prog/favorites/README.md):

- Save the running program to a favorite, then hold **EDIT** — a standard
  bank-11 edit frame whose basis blob snapshots the favorite slot (store
  counter always 0).
- Load a favorite, then hold **PROG** — the dump carries the **source
  program's** bank/slot at 88–91 plus favorite markers: offset **94** =
  `(slot − 1) × 2` and offset **92** = `08` while the favorites screen shows.
- **Caution:** hold-PROG from the favorites screen commits pending edits into
  the favorite slot. Capture edit-buffer state with hold-EDIT first if you
  need the uncommitted values.
- These dumps are **excluded from the PROG corpus scan** (94 ≠ 8 / 92 = 8
  would break the factory-corpus constants) — keep them out of
  `sysex/prog/presets/` and `sysex/prog/parameters/`.

## Suggested captures (remaining)

**All 18 program parameters are captured** as dedicated series under
`sysex/prog/parameters/`, plus `sysex/prog/presets/` identity dumps and the sheet compare.

### Register-basis hold-EDIT (`sysex/prog/edit/registers/`)

When a **User Register** is the running program basis, hold **EDIT** and save
the 157-byte dump. Name is still at **8–23** (16-byte wire / 14-char editable);
**24–87** carries a nibble-packed basis blob; **93** = `register_bank` (B0–B4);
**94** = `08`; **95** = `register` (0–9). Exhaustive 5×10 witness:
`fullsweep-rooms-studio-a.syx`. See
[registers/README.md](../sysex/prog/edit/registers/README.md).

To capture a bank×register grid:

1. Store a factory preset into the target register bank/register.
2. Load that register so it is the running basis.
3. Hold **EDIT**; save as `b<bank>-…/slot-<n>.syx` (filename `slot-N` = Register N).

Optional follow-ups:

- More `sysex/prog/presets/` banks if Bricasti adds firmware banks
- **EDIT receive** confirmation (MIDI-notes bank 118) — send marker **11** is documented from `sysex/prog/edit/`; same for **Favorites receive** (bank 119 — sends decoded in `sysex/prog/favorites/`)
- **Favorites follow-ups** — re-confirm the auto-commit rule (hold PROG from the favorites screen with a pending edit) and power-cycle persistence of an auto-committed favorite
- **SYSTEM** follow-up series under `sysex/system/` — **8** settings captured
  (audio format/routing, dry/wet gain, display level, MIDI channel/bank, output
  level); see [../specification/system/](../specification/system/). **MIDI bank**
  is in `m7_system_dump.ksy` and the web UI; offset 25 also moves as a
  secondary field in display-level captures. Optional: register lock and other
  rarely touched SYSTEM knobs
- `0.1s.syx` for reverb time if the UI reaches the printed 0.1 s floor
- Denser mid samples for medium-confidence tables when you need a full decode table
- **Display edit-band sweeps** (optional): every discrete UI step for 2–3
  parameters with different encodings (e.g. diffusion `nibble_hilo`, reverb time
  `nibble_hilo`, early select) while holding edit (`92 = 00`). Goal: test
  whether 146–147 increments once per step vs digit/cursor cell vs string-pool
  ID — see [bytes/display.md](../specification/prog/bytes/display.md)
- Reconcile hard sheet errata (early select / HF crossover on a few Halls) if you re-dump those factory programs
- Hardware UI value walks (no SysEx) in
  [reference/provided_labels.json](reference/provided_labels.json) — see
  [encoding-sources.md](encoding-sources.md)

Add a new folder under `sysex/prog/parameters/` for each parameter; re-run `export` after each
series.
