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
| Edit buffer dump | Hold **EDIT** briefly | Same 157-byte frame as PROG; bank **88–89 = 11**, mirror **137** = source bank — keep under `sysex/prog/edit/` |
| System dump | Hold **SYSTEM** briefly | I/O / system config only — not program parameters |

Program dumps include UI/edit state (Bricasti MIDI notes) — expect offsets **146–147**
(and sometimes **92** or **98–99**) to move even in single-parameter series.

This repo expects **program dumps** for parameter series and `sysex/prog/presets/`.
EDIT captures go in `sysex/prog/edit/` (excluded from the PROG corpus scan). See
[manual-notes.md](manual-notes.md) for bank context.

## Bank index (for `sysex/prog/presets/` naming)

SysEx offsets **88–89** / mirror **137** use these factory bank indices (from
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
| **11** | **Edit** (hold **EDIT** send — bank word only; mirror 137 stays source bank) |
| 118 | Edit (ephemeral on *receive*, per MIDI notes) |
| 119 | Favorites |
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
`specification/prog/parameters/<slug>.md`, and check:

1. `changing_offsets` — should be small (parameter + checksum ± maybe one status
   byte; 146–147 often move as edit/UI state)
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
- SysEx offsets **8–87** must equal the preset half as ASCII, space-padded to
  80 bytes (bank name is **not** stored in the name field)
- Capture several banks and several slots within one bank (factory order helps)
- Folders starting with `_` are meta series — not treated as parameters

Results land under
[../specification/prog/presets/](../specification/prog/presets/) (bank pages +
[presets.json](../specification/prog/presets/presets.json)),
[../specification/prog/program-identity.md](../specification/prog/program-identity.md), and
[../specification/prog/preset-sheet.md](../specification/prog/preset-sheet.md) (errata vs the
[published preset sheet](https://www.bricasti.com/images/preset_sheet.pdf),
using [reference/preset_sheet.json](reference/preset_sheet.json)).

## Suggested captures (remaining)

**All 18 program parameters are captured** as dedicated series under
`sysex/prog/parameters/`, plus `sysex/prog/presets/` identity dumps and the sheet compare.

Optional follow-ups:

- More `sysex/prog/presets/` banks if Bricasti adds firmware banks
- **EDIT receive** confirmation (MIDI-notes bank 118) — send marker **11** is documented from `sysex/prog/edit/`
- **SYSTEM** follow-up series under `sysex/system/` — **8** settings captured
  (audio format/routing, dry/wet gain, display level, MIDI channel/bank, output
  level); see [../specification/system/](../specification/system/). **MIDI bank**
  is in `m7_system_dump.ksy` and the web UI; offset 25 also moves as a
  secondary field in display-level captures. Optional: register lock and other
  rarely touched SYSTEM knobs
- Register or Favorite-based PROG dumps (manual: basis slot may be stored in dump)
- `0.1s.syx` for reverb time if the UI reaches the printed 0.1 s floor
- Denser mid samples for medium-confidence tables when you need a full decode table
- Reconcile hard sheet errata (early select / HF crossover on a few Halls) if you re-dump those factory programs
- Hardware UI value walks (no SysEx) in
  [reference/provided_labels.json](reference/provided_labels.json) — see
  [encoding-sources.md](encoding-sources.md)

Add a new folder under `sysex/prog/parameters/` for each parameter; re-run `export` after each
series.
