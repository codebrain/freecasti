# Encoding-map sources

Every field page under [../specification/prog/bytes/](../specification/prog/bytes/)
(PROG) or [../specification/system/bytes/](../specification/system/bytes/)
(SYSTEM) publishes a **full encoding map**: each SysEx-encoded step, the bytes at the
parameter offsets, the human label the unit (or sheet) shows, and a **Source**
cell.

Source lists every witness for that step, comma-separated. A step can have more
than one (for example `dump, provided, [1](…)`).

| Source | Meaning | How it gets into the map |
|--------|---------|--------------------------|
| **dump** | Labeled capture in `sysex/prog/parameters/<parameter>/` or `sysex/system/<setting>/` | Filename is the ground-truth label; bytes come from that `.syx` |
| **provided** | Hardware UI walk (no SysEx) | Ordered list in [reference/provided_labels.json](reference/provided_labels.json) |
| **inferred** | Affine fill between sparse dumps | Export computes missing integer steps from a confirmed exact affine scale when dumps and presets do not witness them |
| **preset** | Factory program dump × published sheet | Encoded value from `sysex/prog/presets/`; label from the sheet column when present |

## Priority (which label wins)

When several witnesses disagree on the **numeric label** for the same encoding:

1. **dump** — labeled single-parameter capture
2. **provided** — observed UI walk on the unit
3. **inferred** — integer steps filled from a confirmed affine scale (no UI walk, no dedicated dump)
4. **preset** — sheet value paired with a factory dump’s encoded bytes

For **display strings** (for example output level “−8 dB”), `provided_labels.json`
can supply tooltip text even when a dump row wins the numeric label.

All witnesses still appear in the Source cell; priority only picks the label
shown in the Label column.

Sheet compare for whole presets is separate: when a factory dump disagrees with
the printed PDF, **the dump wins** and the mismatch is recorded as errata in
[../specification/prog/preset-sheet.md](../specification/prog/preset-sheet.md). Encoding-map
`provided` can also override a bad sheet label for a given encoded step (for
example Early Select encoded 13 labeled 17 on the Large Hall sheet row).

## dump

A `.syx` in `sysex/prog/parameters/<parameter>/` named for the value (`120hz.syx`, `off.syx`,
`20.6.syx` for Early/Reverb Mix UI `20/6`, and so on).

- Strongest evidence: you set that control, dumped, and labeled the file.
- Capture series are usually **sparse** (extremes, adjacent-to-extremes, a few
  mids) — see [capture-guide.md](capture-guide.md).
- Dump rows are never replaced by provided/inferred/preset labels.

## inferred

Integer encoding steps computed by export when:

- The parameter has an **exact** affine encoding (`score` ≥ 0.999).
- Sparse dumps and/or presets witness endpoints but not every integer in range.
- No `provided_labels.json` walk supplies that step.

These rows are **not** hardware UI walks — they extrapolate labels from the
fitted scale. Re-capture as `dump` or add to `provided_labels.json` to
strengthen evidence.

## provided

An ordered walk of every display value seen on the hardware while stepping the
control, stored under that parameter’s key in
[reference/provided_labels.json](reference/provided_labels.json). Most keys are
program parameters; **output level** is a system setting (tooltip/display densify
only — no `sysex/prog/parameters/` folder).

- No SysEx required — useful when dumping every mid-step is tedious.
- List index is the encoded step (`values[0]` → encoded 0).
- Tokens can include units (`124 mSec`, `320 Hz`) and endpoints (`off`, `Low`,
  `High`, `Full`) as shown on the unit.
- Export tags matching map rows `provided`.

After editing the JSON, run `python run.py` (or `python -m m7_sysex export`).
Export clears the provided-label cache and rewrites every parameter page’s
encoding map.

## preset

Witnesses from factory programs in `sysex/prog/presets/`:

- The **encoded** integer is read from the dump at the parameter’s offsets.
- The **label** preferably comes from the matching column on Bricasti’s
  published preset sheet ([reference/preset_sheet.json](reference/preset_sheet.json)).
- For closed-form (affine) parameters, factory dumps can also contribute
  mid-steps labeled via the fitted scale even when the sheet has no column.

On parameter pages, preset witnesses render as numbered links to
[../specification/prog/presets/](../specification/prog/presets/) pages, not the bare word
`preset`.

**System parameters:** encoding maps use dump and provided witnesses only.
Program preset anchors at the same byte offsets are ignored — program dumps at
system offsets are unrelated data and previously produced spurious value-map rows
(for example bogus output-level steps).

## Practical workflow

1. Capture sparse dumps → establish offsets, encoding, and confidence.
2. Let export densify with preset sheet points.
3. Walk remaining gaps on the unit → append to `provided_labels.json`.
4. Optionally capture mid-step `.syx` files later to promote `provided` →
   `dump`.

```text
dump  >  provided  >  inferred  >  preset
 ↑         ↑            ↑           ↑
 SysEx   UI walk    affine fill  factory×sheet
 labeled              (no walk)
```
