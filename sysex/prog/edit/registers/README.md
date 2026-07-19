# Register-basis hold-EDIT dumps

Captures of **hold EDIT** program dumps (157-byte frame, bank word **88–89 = 11**)
taken while the running program’s basis is a **User Register**.

Bricasti MIDI app notes: when a register or favorite is the basis of the running
program, the dump also carries an **unedited copy** of that basis. In these
captures that shows up as:

| Offsets | Role |
|---------|------|
| 8–23 | ASCII program name (16-char window) |
| 24–87 | Register basis blob (nibble-packed; not name spaces) |
| 93 | Register bank page (`B0`=`00` …) |
| 94 | Constant `08` |
| 95 | Register slot within the page (`0`–`9`) |
| 137 | Source factory bank mirror |

Factory/parameter-series dumps still space-pad **8–87** and keep **93/95** at
`0`. See [docs/manual-notes.md](../../../../docs/manual-notes.md) and
[docs/capture-guide.md](../../../../docs/capture-guide.md).

## Layout here

- `b0-halls-large-hall/slot-*.syx` — Reg page B0, slots 0–9, Halls / Large Hall
- `b1-halls-large-hall/slot-*.syx` — Reg page B1, slots 0–1, same preset
- `samples/` — earlier mixed-preset EDIT captures (Ambience, Halls 2 subtype, NonLin)

## How to capture

1. Store a factory preset into the target Reg page/slot.
2. Load that register so it is the running program basis.
3. Hold **EDIT** briefly; save the 157-byte SysEx.
4. Name files by page and slot (`b0-…/slot-3.syx`).
