# Unofficial Bricasti M7 SysEx protocol specification

An unofficial specification of the Bricasti M7 reverb's MIDI SysEx **program**
(157-byte) and **system** (77-byte) dump formats: frame layout, checksum
algorithm, and byte-level encodings derived from labeled hardware captures.

This specification powers **[Freecasti](https://codebrain.github.io/freecasti/)**,
a browser-based editor for M7 program and system dumps — factory presets,
live SysEx serialization, and optional Web MIDI.

Specs live under **[specification/](specification/)** — split into
[prog/](specification/prog/) (sound parameters, presets, identity) and
[system/](specification/system/) (I/O settings). For codegen:

| Family | Kaitai | Machine schema |
|--------|--------|----------------|
| PROG | [m7_program_dump.ksy](specification/prog/m7_program_dump.ksy) | [m7_program_dump.spec.json](specification/prog/m7_program_dump.spec.json) |
| SYSTEM | [m7_system_dump.ksy](specification/system/m7_system_dump.ksy) | [m7_system_dump.spec.json](specification/system/m7_system_dump.spec.json) |

## Project status

The **157-byte program-dump format is fully annotated** for this unit — the
byte map has **no unknown bytes left**
([byte-map-overview.md](specification/prog/byte-map-overview.md)).

The **77-byte system-dump format is fully annotated** as well — see
[system/byte-map.md](specification/system/byte-map.md).

| Area | Status |
|------|--------|
| Frame (start, mfr ID, header, name, end) | Solved; validated on **379** PROG corpus dumps + **61** SYSTEM dumps (**440** total) |
| Checksum | **Solved**: CRC-16/ARC over offsets 8–151, packed as 4 high-nibble-first bytes; verified corpus-wide |
| Sound parameters | **18 / 18 captured and decodable** from dedicated series; tables densified with hardware UI walks (`provided`) and sheet/preset anchors |
| Program identity | Solved: name @ 8–87, bank @ 88–89 (mirror 137), slot @ 90–91 |
| Meta / reserved bytes | Mapped from a corpus scan (family flag 97/145, engine class 130, fixed fields, padding) — medium confidence |
| Factory presets | **222 captured** ([presets/](specification/prog/presets/)); see [preset-inventory.md](specification/prog/preset-inventory.md) |
| Sheet cross-check | 98 classic presets matched; errata in [preset-sheet.md](specification/prog/preset-sheet.md) |
| Hardware UI walks | **15** parameters in [provided_labels.json](docs/reference/provided_labels.json) (14 program + output level) |
| Machine byte spec | PROG + SYSTEM Kaitai `.ksy` and `.spec.json` (regenerated each export) |
| SYSTEM settings | **8** settings captured; **77-byte map fully annotated** (no unknown bytes) — [system/](specification/system/) |
| Tests | **222** pytest tests (default run; more with `-m slow`), corpus-wide PROG + SYSTEM validation |
| Web UI | Static editor in [`web-ui/`](web-ui/) — vitest encode tests; tooltips from manual descriptions in `param-manifest.json` |

Encodings with agreeing edge slopes are closed-form (**high** confidence);
Hz/time controls are monotonic tables (**medium** when only sparse dumps —
full `provided` walks still leave the series confidence as medium).

### Open items

Tracked in the generated specification (single source of truth):

- [Open questions](specification/open-items.md) — consolidated PROG + SYSTEM list
- [Program overview](specification/prog/README.md#open-questions) — includes export/update notes

## Quick start

```bash
# From the repo root (Python 3.11+)
python run.py

# Same pipeline via the installed module (after pip install -e .)
pip install -e .
python -m m7_sysex export

# Analyze only (writes analysis.json per parameter)
python run.py analyze sysex
python run.py analyze "sysex/prog/parameters/predelay"

# Preset inventory only
python run.py inventory

# Cross-series meta-analysis only
python run.py cross

# Compare decoded presets to the published sheet
# (uses committed docs/reference/preset_sheet.json — no PDF needed)
python run.py sheet
```

`python run.py` runs the **full export**: `sysex/prog/parameters/`,
`sysex/prog/presets/`, `sysex/system/`, then regenerates
`sysex/prog/byte_map.json`, `sysex/prog/cross_analysis.json`,
`sysex/system/byte_map.json`, and [specification/](specification/)
(`prog/` + `system/` subtrees).

On Windows, if `m7-sysex` is not on your PATH after install, keep using
`python run.py` or `python -m m7_sysex`.

## Web UI

Static browser control surface in [`web-ui/`](web-ui/) — program + system SysEx
editor with live serialization, 222 factory presets, optional Web MIDI (off by
default), parameter tooltips from the manual, and a deployable `dist/` bundle.

```bash
python run.py              # syncs specification/ → web-ui/public/m7-runtime.json
                           # and web-ui/src/generated/param-manifest.json
cd web-ui
npm install
npm run build              # → web-ui/dist/
npm run preview            # local static preview
```

Prerequisites: Node 20+; Java or `kaitai-struct-compiler` 0.10 at build time only.

Details: [web-ui/README.md](web-ui/README.md), [docs/kaitai-encode.md](docs/kaitai-encode.md).

## Capture workflow

1. Load a known program on the M7 (e.g. Large Hall).
2. Change **only one** parameter for that series.
3. Hold **PROG** briefly to send a program dump; save it as a `.syx` file.
4. Name files after the value: **`off.syx`** (optional), **`low.syx`** /
   **`small.syx`**, mids as **`<number><unit>.syx`** (e.g. `120hz.syx`,
   `100ms.syx`, `0.2s.syx`), **`high.syx`** / **`full.syx`** / **`large.syx`**.
5. Put all dumps for that parameter in `sysex/prog/parameters/<parameter>/`.
6. Optional: dump whole presets into `sysex/prog/presets/` as
   `<bank name>.<preset name>.syx` for identity fields.
7. Re-run `python run.py` (or `python -m m7_sysex export`).

See [docs/capture-guide.md](docs/capture-guide.md),
[docs/encoding-sources.md](docs/encoding-sources.md) (dump / provided / preset),
[docs/parameter-catalog.md](docs/parameter-catalog.md),
[docs/manual-notes.md](docs/manual-notes.md) (Bricasti manual/MIDI context), and
[specification/](specification/).

## Repository layout

```
run.py                     # full export (default) or CLI subcommands
sysex/
  prog/
    parameters/            # one folder per sound parameter (18 series)
    presets/                 # <bank>.<preset>.syx (222 dumps)
    edit/                    # hold-EDIT buffer captures
    byte_map.json            # generated
    cross_analysis.json      # generated
  system/                    # SYSTEM setting series (8 captured)
    byte_map.json            # generated
src/m7_sysex/
  paths.py, types.py, series.py, frame.py, kaitai_render.py
  prog/                      # program-dump analysis + preset tooling
  system/                    # system-dump analysis + Kaitai
  export/                    # specification/{prog,system}/ generator
  cli.py
tests/
docs/
  reference/                 # preset_sheet.json, provided_labels.json (hand-maintained)
specification/               # generated — prog/ + system/
web-ui/                      # static SPA (see web-ui/README.md)
```

## Filename conventions

Capture series as **extremes + adjacent-to-extremes + sample mids** (optional
OFF). Mids are a sparse sample of the range, not every intermediate value.

| Example | Parsed as |
|---------|-----------|
| `80hz.syx`, `120hz.syx`, `20000hz.syx` | number + unit **Hz** |
| `0ms.syx`, `500ms.syx` | number + unit **ms** |
| `0.2s.syx`, `30s.syx` | number + unit **s** |
| `-6dB.syx`, `50%.syx` | number + unit |
| `0.20.syx` … `20.0.syx` | balance `A/B` (dot stands in for `/`; early/reverb mix) |
| `off.syx` | endpoint — discrete off |
| `low.syx` / `small.syx` | endpoint — minimum |
| `high.syx` / `full.syx` / `large.syx` | endpoint — maximum |
| `1.syx`, `on.syx` | bare number / boolean |
| `Halls.Large Hall.syx` | `prog/presets/` only: bank + preset |

Aliases: `min` / `small` → low; `max` / `maximum` / `full` / `large` → high.
Units are case-insensitive (`Hz`, `hz`, `kHz`, `s`, `ms`, `dB`).

## What the analyzer reports

**Parameter folders** → `analysis.json`:

- **changing_offsets** — bytes that differ within that folder only
- **classification** — parameter vs checksum vs secondary
- **encoding_hypotheses** / **best_encoding** — scored maps (affine or table)
- **hypothesis.how_to_set** — encode steps + CRC-16/ARC checksum

**`sysex/prog/presets/`** → identity analysis (name / bank / program slot). Offsets
8–87 must equal the filename preset as ASCII, space-padded to 80 bytes.

**Sheet compare** → [specification/prog/preset-sheet.md](specification/prog/preset-sheet.md)
from committed [docs/reference/preset_sheet.json](docs/reference/preset_sheet.json).
Refresh the JSON from the PDF with `python run.py sheet --refresh` (needs
`pymupdf`).

Folders are analyzed independently. Export merges per-folder conclusions into
the layout map only — never treats absolute dump bytes from one folder as
another parameter’s state.

## Findings (summary)

Authoritative detail: **[specification/prog/](specification/prog/)**
(program) and **[specification/system/](specification/system/)**
(system settings). Decoded factory presets: [presets/](specification/prog/presets/)
(bank pages + [presets.json](specification/prog/presets/presets.json);
overview [program-identity.md](specification/prog/program-identity.md)).

All **18 program parameters** have dedicated capture series under
`sysex/prog/parameters/`. See the [parameter index](specification/prog/README.md)
and [byte-map.md](specification/prog/byte-map.md) for offsets and encodings.

**SYSTEM** dumps (77 bytes, header `70 08 02 00`) are documented separately.
Eight settings have dedicated capture series (audio format/routing, dry/wet gain,
display level, MIDI channel/bank, output level); the byte map has **no unknown
bytes left** ([system/byte-map.md](specification/system/byte-map.md)).

## Tests

```bash
python -m pytest tests -q
```

The suite covers frame parsing / checksum round trips, encoding primitives,
label parsing, per-series encoding fits, preset decoding against the published
sheet, and **corpus-wide validation** — every committed `.syx` must parse,
carry a valid checksum, and satisfy all documented layout claims (reserved
constants, mirror relations, bank/slot identity).

## Requirements

- Python 3.11+
- Core analyze / export: no third-party dependencies
- Tests: `pip install pytest`
- Optional: `pip install pymupdf` (or `pip install -e ".[sheet]"`) only to
  re-parse the PDF into `docs/reference/preset_sheet.json`

## Contributing

Contributions are welcome — especially labeled hardware SysEx captures. See
[CONTRIBUTING.md](CONTRIBUTING.md) for setup, PR expectations, and capture
workflow. Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

Licensed under the [Apache License, Version 2.0](LICENSE). See [NOTICE](NOTICE)
for attribution and trademark notes.

Bricasti and M7 are trademarks of their respective owners. This is an
unofficial community project and is not affiliated with or endorsed by
Bricasti.
