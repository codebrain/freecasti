# Docs index

Project status summary lives in the [root README](../README.md). Generated SysEx
specifications live under [specification/](../specification/) at the repo root.

| Doc | Purpose |
|-----|---------|
| [capture-guide.md](capture-guide.md) | How to capture `.syx` dumps (PROG / EDIT / SYSTEM) |
| [encoding-sources.md](encoding-sources.md) | Encoding-map Source: dump vs provided vs preset |
| [parameter-catalog.md](parameter-catalog.md) | Printed hints vs this unit’s dump findings |
| [manual-notes.md](manual-notes.md) | Bricasti manual/MIDI context (algorithms, banks, dump types) |
| [development.md](development.md) | Setup, CLI, tests, package map |
| [reference/preset_sheet.json](reference/preset_sheet.json) | Parsed Bricasti preset sheet (sheet compare source) |
| [reference/provided_labels.json](reference/provided_labels.json) | Hardware UI walks (15 entries: 14 program + output level; encoding-map `provided` witnesses) |
| [../web-ui/README.md](../web-ui/README.md) | Static browser editor (`m7-runtime.json`, build, deploy) |
| [../specification/](../specification/) | **Generated** SysEx specs (run `python run.py`) |

### Generated specification

| Page | Contents |
|------|----------|
| [specification/README.md](../specification/README.md) | Index → PROG + SYSTEM subtrees |
| [specification/prog/README.md](../specification/prog/README.md) | 157-byte program dump overview |
| [specification/prog/parameters/](../specification/prog/parameters/) | One page per captured sound parameter |
| [specification/prog/presets/](../specification/prog/presets/) | Bank pages + [presets.json](../specification/prog/presets/presets.json) |
| [specification/prog/m7_program_dump.ksy](../specification/prog/m7_program_dump.ksy) | PROG [Kaitai Struct](https://kaitai.io/) layout |
| [specification/prog/m7_program_dump.spec.json](../specification/prog/m7_program_dump.spec.json) | PROG machine schema |
| [specification/system/README.md](../specification/system/README.md) | 77-byte system dump overview |
| [specification/system/parameters/](../specification/system/parameters/) | Captured SYSTEM settings (8 series; 77-byte map complete) |
| [specification/system/m7_system_dump.ksy](../specification/system/m7_system_dump.ksy) | SYSTEM Kaitai layout |
| [specification/system/m7_system_dump.spec.json](../specification/system/m7_system_dump.spec.json) | SYSTEM machine schema |

Do not hand-edit files under `specification/` — they are overwritten by `export`.
Refresh `reference/preset_sheet.json` with `python run.py sheet --refresh` (needs pymupdf).

Preset inventory only (no full export): `python run.py inventory`.
