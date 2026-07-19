# Register-basis hold-EDIT dumps

Captures of **hold EDIT** program dumps (157-byte frame, program bank word
**88–89 = 11**) taken while the running program’s basis is a **User Register**.

Per the [M7 Owner’s Manual](https://www.bricasti.com/images/M7.pdf), user storage
is **5 Banks × 10 Registers** (e.g. BANK 0, REG 0). On the wire:

| Offsets | Role |
|---------|------|
| 8–23 | Program name: **16-byte** wire window; **14-character** editable label (manual); trailing two bytes space-padded |
| 24–87 | Register basis blob (nibble-packed; not name spaces) |
| 93 | **`register_bank`** — manual Bank (`B0`–`B4` = `00`–`04`) |
| 94 | Constant `08` |
| 95 | **`register`** — manual Register within bank (`0`–`9`) |
| 137 | Source factory program-bank mirror |

Factory/parameter-series dumps still space-pad **8–87** and keep **93/95** at
`0`. See [docs/manual-notes.md](../../../../docs/manual-notes.md) and
[docs/capture-guide.md](../../../../docs/capture-guide.md).

## Layout here

- `fullsweep-rooms-studio-a.syx` — **exhaustive** inventory: Banks 0–4 × Registers
  0–9 (50 concatenated dumps), Rooms / Studio A. Identity only at **93/95**;
  LCD `display` (146–147) stayed at **164** for every frame (not Bank/Register
  addressing).
- `b0-halls-large-hall/slot-*.syx` — Bank 0, Registers 0–9, Halls / Large Hall
  (`slot-N` filename = Register N)
- `b1-halls-large-hall/slot-*.syx` — Bank 1, Registers 0–1, same preset
- `samples/` — earlier mixed-preset EDIT captures (Ambience, Halls 2 subtype, NonLin)

## How to capture

1. Store a factory preset into the target register bank/register.
2. Load that register so it is the running program basis.
3. Hold **EDIT** briefly; save the 157-byte SysEx (or concatenate a bank sweep).
4. Name single-dump files by bank and register (`b0-…/slot-3.syx` = Bank 0, Register 3).
