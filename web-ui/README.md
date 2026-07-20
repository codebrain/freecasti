# M7 Web UI

Browser control surface for the Bricasti M7 reverb. Edits program (157-byte) and system (77-byte) SysEx dumps with live serialization, optional Web MIDI, and a factory preset catalog.

**Do not edit generated assets by hand.** `python run.py` from the repo root syncs:

| Output | Purpose |
|--------|---------|
| `public/m7-runtime.json` | Compact prog/system specs + preset catalog + `prog_ui` menu table (loaded at runtime) |
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

## MIDI send (program UI state)

When **Send on change** or **Send** is used on the program tab, outgoing dumps patch UI bytes at offsets **92**, **98–99**, and **146–147** from `prog_ui` in `m7-runtime.json`:

- **146–147** — `nibble_hilo` display (`display` in Kaitai): high nibble = page/row, low nibble = column. Patched as separate wire bytes; combined value is `(byte[146] << 4) | byte[147]`.
- **Parameter select/focus** → browse mode (menu highlighted, byte 92 = `02`).
- **Single knob/button edit** → edit mode for that parameter’s menu (byte 92 stays `02`, menu index @ 98–99, edit cursor @ 146–147). Hardware edit captures store byte 92 = `00` while a value is being changed; outbound web-UI dumps deliberately keep the browse marker `02` (`applyProgUiBytes` in `src/prog/uiState.ts`), and the decode path accepts both.
- **Preset load** or any multi-parameter state replace → idle / **no menu** bytes (`no menu.syx` baseline).

SYSTEM dumps are unchanged (no menu-navigation bytes in SYSTEM captures).

## MIDI receive (register basis)

Incoming program dumps hydrate the active A/B slot from the live payload bytes
(100–139). If the dump carries a **register basis frame** — offsets **24–87**
nibble-packed instead of the factory `0x20` space pad — the stored register
settings win: the blob's parameter values (reverb time, size, predelay, the
delay block, …) and register name replace the payload values, since the
payload tracks the edit buffer and may hold unstored edits. See
[register-basis-blob.md](../specification/prog/bytes/register-basis-blob.md)
for the blob layout (shipped at runtime as `reg_blob` in `m7-runtime.json`).

This applies to the Web MIDI receive path only (`applyRegisterBasis` in
`src/app/midiReceive.ts`); `.syx` file import and the dump inspector show the
payload and blob side by side without overriding.

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
