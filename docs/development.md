# Development

## Setup

```bash
# From the repo root
pip install -e .
# Optional: only needed to re-parse the Bricasti PDF into sheet JSON
pip install -e ".[sheet]"
```

## Commands

```bash
# Full pipeline (analyze PROG + SYSTEM + regenerate specification/)
python run.py

# Same via module after pip install -e .
python -m m7_sysex export

# Analyze only (parameter series under sysex/prog/parameters/)
python run.py analyze sysex
python run.py analyze "sysex/prog/parameters/predelay" --stdout
python run.py analyze sysex --no-write

# Cross-series meta only
python run.py cross
python run.py cross --no-docs

# Preset inventory vs V2 addendum (no full export)
python run.py inventory
python run.py inventory --markdown
python run.py inventory --write

# Compare decoded presets to Bricasti's published preset sheet
python run.py sheet
python run.py sheet --verbose
python run.py sheet --refresh   # re-parse PDF (needs pymupdf)
```

`run.py` lives at the repo root, puts `src/` on `sys.path`, and defaults to
`export` when given no arguments.

## Tests

```bash
pip install pytest kaitaistruct
# or: pip install -e ".[dev]"
python -m pytest tests -q
```

Default runs skip tests marked `slow` (corpus-wide Kaitai round-trips and extra
compile targets). To include them:

```bash
python -m pytest tests -q -o addopts=
python -m pytest tests -q -m slow          # slow Kaitai tests only
```

Kaitai round-trip tests compile `specification/**/*.ksy` to ephemeral Python
under pytest temp dirs (requires Java for `kaitai-struct-compiler`; downloaded
to `.pytest_cache/` on first run if not on PATH). Kaitai generates decoders
only; message **encoding** uses [`kaitai_encode.py`](../src/m7_sysex/kaitai_encode.py)
— see [kaitai-encode.md](kaitai-encode.md).

| File | Covers |
|------|--------|
| `tests/test_frame.py` | Frame parsing, CRC-16/ARC, PROG + SYSTEM samples |
| `tests/test_encodings.py` | Nibble/MIDI-14 primitives, fitting |
| `tests/test_encoding_table.py` | Encoding-map table export |
| `tests/test_corpus.py` | Every committed `.syx` under `sysex/prog/` + `sysex/system/` |
| `tests/test_doc_claims.py` | Factual claims in hand-written docs (counts, offsets, ranges) |
| `tests/test_system.py` | SYSTEM series analysis |
| `tests/test_menus_analysis.py` | PROG menu-navigation (`sysex/prog/menus/`) UI-state analysis |
| `tests/test_decode_preset.py` | Full preset decode vs published sheet |
| `tests/test_analyze.py` | Label parsing, encoding fits, preset validation |
| `tests/test_dump_codec.py` | Decode/encode CLI round trips (`run.py decode` / `encode`) |
| `tests/test_edit_dumps.py` | Hold-EDIT buffer dumps (`sysex/prog/edit/`) |
| `tests/test_favorites.py` | Favorites session (`sysex/prog/favorites/`): slot codes, panel-mode flag, auto-commit |
| `tests/test_kaitai_spec.py` | PROG + SYSTEM Kaitai / `.spec.json` |
| `tests/test_kaitai_encode.py` | Parse → serialize encode round-trips ([details](kaitai-encode.md)) |
| `tests/test_kaitai_roundtrip.py` | Per-field wire extract vs raw (decode-side layout) |
| `tests/test_kaitai_validation.py` | Kaitai `.spec.json` field validation |
| `tests/test_prog_algorithms.py` | Algorithm / family-flag corpus checks |
| `tests/test_register_blob.py` | Register basis blob decode (24–87): charset, counter, delay block |
| `tests/test_register_blob_docs.py` | Generated register-blob doc page (layout table, links) |
| `tests/test_register_edit_dumps.py` | Register hold-EDIT dumps (`sysex/prog/edit/registers/`) |
| `tests/test_types.py` | Dump-family registry paths |
| `tests/test_presets_json.py` | `prog/presets/presets.json` export |
| `tests/test_parameters_readme.py` | Generated parameter index pages |
| `tests/test_preset_sheet_page.py` | Generated preset-sheet page |
| `tests/test_byte_map_links.py` | Byte-map cross-links |
| `tests/test_doc_table_links.py` | Doc table link integrity |
| `tests/test_markdown_links.py` | Relative links in README / docs / specification (also run after export) |
| `tests/test_parameter_description.py` | Parameter description blocks |
| `tests/test_unseen_values.py` | Unseen-value / gap reporting in encoding maps |
| `tests/test_web_ui_sync.py` | `web-ui/public/m7-runtime.json` + `param-manifest.json` after export sync |

## Web UI

After `python run.py`, export writes:

- `web-ui/public/m7-runtime.json` — compact prog/system specs, preset catalog, and `tpl` serialize skeletons (synthesized from the specs — the byte map has no unknown bytes, so no captured template dump is needed)
- `web-ui/src/generated/param-manifest.json` — parameter descriptions for tooltips

Build the static SPA separately:

```bash
cd web-ui
npm install
npm run dev       # Vite dev server
npm run build     # dist/ for deploy
npm test          # vitest encode/serialize tests
```

See [web-ui/README.md](../web-ui/README.md). Skip sync with
`python run.py export --no-web-ui`.

## Adding a PROG parameter series

1. Create `sysex/prog/parameters/<name>/`
2. Drop labeled `.syx` dumps (extremes, adjacent-to-extremes, sparse mids).
3. Run `python run.py`
4. Commit dumps + `analysis.json` + regenerated `specification/` when clean

## Adding preset-identity dumps

1. Dump factory presets into `sysex/prog/presets/` as `<bank>.<preset>.syx`
2. Ensure offsets 8–87 match the preset name (ASCII, space-padded). Display
   name is 8–23 (**16-byte** wire window; **14-character** editable label per
   the manual; trailing two bytes space-padded). Factory dumps space-pad 24–87.
   Reg-backed hold-EDIT dumps (basis blob at 24–87, `register_bank` /
   `register` at 93/95) belong under `sysex/prog/edit/registers/` — not the
   factory presets folder.
3. Run `python run.py` — refreshes [program-identity.md](../specification/prog/program-identity.md),
   [presets/](../specification/prog/presets/), [preset-sheet.md](../specification/prog/preset-sheet.md)

## Adding a SYSTEM series

1. Create `sysex/system/<setting>/` with labeled dumps
2. Run `python run.py` — refreshes [system/](../specification/system/) docs and
   `m7_system_dump.{ksy,spec.json}`

## Package map

```
m7_sysex/
  frame.py, encodings.py, labels.py, sampling.py, series.py
  paths.py, types.py, kaitai_render.py, cli.py
  prog/          # program-dump analysis + preset tooling
  system/        # system-dump analysis, byte map, catalog.py, Kaitai
  export/        # specification/{prog,system}/ generator + web-ui sync
```

Top-level modules (`analyze.py`, `byte_map.py`, …) are thin re-exports into
`prog/` for backward compatibility.

## Design notes

- Each `sysex/prog/parameters/<name>/` folder is an independent capture stream.
- EDIT buffer dumps share the PROG frame; keep under `sysex/prog/edit/`.
- Favorites captures share the PROG frame but carry non-corpus identity bytes
  (offsets 92/94); keep under `sysex/prog/favorites/` (excluded from the
  corpus scan like `edit/` and `menus/`).
- SYSTEM dumps are separate (77 bytes); keep under `sysex/system/`.
- Generated docs: `specification/prog/` and `specification/system/`.
- Machine specs: `m7_program_dump.*` and `m7_system_dump.*` (Kaitai + JSON).
