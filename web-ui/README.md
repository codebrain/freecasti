# M7 Web UI

Browser control surface for the Bricasti M7 reverb. Edits program (157-byte) and system (77-byte) SysEx dumps with live serialization, optional Web MIDI, and a factory preset catalog.

**Do not edit generated assets by hand.** `python run.py` from the repo root syncs:

| Output | Purpose |
|--------|---------|
| `public/m7-runtime.json` | Compact prog/system specs + preset catalog (loaded at runtime) |
| `specification/web_serialize_skeletons.json` | Serialize skeleton bytes (embedded in runtime bundle as `tpl`) |
| `src/generated/param-manifest.json` | Parameter descriptions for control tooltips |
| `src/generated/sysex-parsers/` | SysEx dump parsers (also rebuilt by `npm run compile-parsers`) |

## Prerequisites

- Node.js 20+
- Java runtime (build-time only, for compiling SysEx parsers from `.ksy` specs)

## Development

```bash
# From repo root — sync runtime bundle + param manifest
python run.py

cd web-ui
npm install
npm run dev
```

If `public/m7-runtime.json` is missing, the app shows a banner asking you to run `python run.py`.

Dev fallback (without full export):

```bash
npm run prepare:assets
```

## Build static bundle

```bash
cd web-ui
npm install
npm run build    # → dist/ (index.html + hashed JS/CSS + public assets)
npm run preview  # verify production bundle locally
```

Upload the **contents of `dist/`** to any static host (GitHub Pages, S3, nginx). No backend required.

At load time the app fetches `m7-runtime.json` and expands the compact prog/system specs in memory. `.ksy` layout files are build-time only (read from `specification/` during `npm run compile-parsers`). Legacy paths (`public/spec/`, `public/presets/presets.json`, `sync-manifest.json`) are not shipped.

```bash
npm run build:analyze   # build + print dist size table
```

Pre-compressed `.gz` / `.br` siblings are written next to assets by `scripts/compress-dist.mjs` (for hosts with `gzip_static` / `brotli_static`).

## Controls

Control definitions are built from the synced specs in `src/spec/controls.ts`:

| Widget | System parameters |
|--------|---------------------|
| Knobs | Wet gain, dry gain, MIDI channel |
| Buttons | Audio routing, audio format, display level, output level (−8 / −16 / −24 dB), MIDI bank |

Tooltips use manual descriptions from `param-manifest.json` (sourced from `src/m7_sysex/system/catalog.py` and `prog/catalog.py` at export time).

## Tests

```bash
cd web-ui
npm test
```

Vitest covers TypeScript encode/serialize logic aligned with `src/m7_sysex/` in Python.

## Web MIDI

**Off by default.** Enable the MIDI toggle in the header to request `sysex: true` access. Works best in Chromium-based browsers.

## Known limitations (v1)

| Topic | Behavior |
|-------|----------|
| Saved presets | Stored in browser `localStorage` (`m7.userPresets`); export `.syx` to share across browsers |
| EDIT bank 118 | Receive path not implemented |
| Web MIDI | Opt-in; requires user gesture for permission |

See also [docs/development.md](../docs/development.md).
