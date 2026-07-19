# Open questions

Auto-generated from `src/m7_sysex/export/open_items.py` on each export.

## Program dumps

1. **Unseen / undocumented values** — documented or otherwise possible values not yet witnessed on the wire are tracked per field in the **Unseen values** section of each [bytes/](prog/bytes/README.md) page
2. **EDIT receive** path (MIDI-notes bank **118**) — hold-EDIT *sends* use bank **11** (`sysex/prog/edit/`)
3. Semantics of PROG header bytes `70 08 01 00` and fixed field 93–94 (`00 08`)
4. **Offset 25 coupling** — `midi bank` (primary @ 25) and display-level captures also move offset 25 (secondary)
5. Closed-form mapping for table parameters (see medium-confidence rows in the parameter index)
6. Optional: register/favorite-based PROG dumps; rarely used SYSTEM knobs (e.g. register lock) not yet in dedicated series

## System dumps

1. **Offset 25 coupling** — `midi bank` primary @ 25; display-level series also moves offset 25 (secondary)
2. Rarely used SYSTEM knobs (e.g. register lock) not yet in dedicated series
