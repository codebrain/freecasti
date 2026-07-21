# Open questions

Auto-generated from `src/m7_sysex/export/open_items.py` on each export.

## Program dumps

1. **Unseen / undocumented values** — documented or otherwise possible values not yet witnessed on the wire are tracked per field in the **Unseen values** section of each [bytes/](prog/bytes/README.md) page
2. **EDIT receive** path (MIDI-notes bank **118**) — hold-EDIT *sends* use bank **11** (`sysex/prog/edit/`); **Favorites receive** (MIDI-notes bank **119**) also unconfirmed — favorites *sends* carry the source identity instead (`sysex/prog/favorites/`)
3. Semantics of PROG header bytes `70 08 01 00`
4. Halls 2 subtype EDIT outlier
5. Closed-form mapping for table parameters (see medium-confidence rows in the parameter index)
6. **Favorites follow-ups** — one more commit-rule confirmation (hold-PROG from the favorites screen with a pending edit) and power-cycle persistence of an auto-committed favorite (`sysex/prog/favorites/README.md`)

## System dumps

1. **Offset 25 coupling** — `midi bank` primary @ 25; display-level series also moves offset 25 (secondary)
2. Rarely used SYSTEM knobs (e.g. register lock) not yet in dedicated series

## Resolved

- Register basis blob **24–87** is fully decoded — complete 6-bit name charset, per-register store counter, all 18 parameters incl. the delay block at bits **197–211**; snapshots stored register values; offsets **93/95** track the *loaded* register basis (see `sysex/prog/edit/registers/README.md`)
- **Favorites**-based PROG dumps are decoded — sends carry the source program identity at **88–91** (never bank 119); offset **94** is the favorite-source slot (`(slot-1)*2`, `08` = none), offset **92** is a panel-mode flag (`08` = favorites screen); favorite saves write the register basis blob with store counter 0 and auto-commit edits on hold-PROG from the favorites screen (see `sysex/prog/favorites/README.md`)
