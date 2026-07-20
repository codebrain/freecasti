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
| 94 | `08` on all hold-EDIT frames (= favorite slot "none"; favorite-loaded PROG dumps carry slot codes here — see `../../favorites/`) |
| 95 | **`register`** — manual Register within bank (`0`–`9`) |
| 137 | Source factory program-bank mirror |

Factory/parameter-series dumps still space-pad **8–87** and keep **93/95** at
`0`. See [docs/manual-notes.md](../../../../docs/manual-notes.md) and
[docs/capture-guide.md](../../../../docs/capture-guide.md).

## Register basis blob (24–87)

The blob is a **bit-packed snapshot of the stored register** (name + all
parameter values + source-bank metadata), not opaque padding — fully decoded.
The layout, 6-bit name charset, store-generation counter semantics, and
witness citations live in the **generated** page
[specification/prog/bytes/register-basis-blob.md](../../../../specification/prog/bytes/register-basis-blob.md),
which is rendered from `REGISTER_BLOB_FIELDS` in
`src/m7_sysex/prog/register_blob.py` on every export (that module is the
single source of truth; this README keeps only the capture narrative).

Key semantics (details + witnesses on the generated page):

- The blob snapshots the **stored** register values (delay block included at
  bits 197–211); live edits stay in the payload (100–139) until stored.
- The 6-bit name charset is complete: space, `&`, `0`–`9`, `A`–`Z`, `a`–`z`.
- Bits 96–100 are a per-slot **store-generation counter** — the only
  non-identity bytes that vary inside `fullsweep-rooms-studio-a.syx`.
- Offsets **93/95** identify the register **loaded as the running basis**;
  a store alone does not update them.

## Layout here

- `fullsweep-rooms-studio-a.syx` — **exhaustive** inventory: Banks 0–4 × Registers
  0–9 (50 concatenated dumps), Rooms / Studio A. Identity only at **93/95**;
  LCD `display` (146–147) stayed at **164** for every frame (not Bank/Register
  addressing).
- `b0-halls-large-hall/slot-*.syx` — Bank 0, Registers 0–9, Halls / Large Hall
  (`slot-N` filename = Register N)
- `b1-halls-large-hall/slot-*.syx` — Bank 1, Registers 0–1, same preset
- `samples/` — earlier mixed-preset EDIT captures (Ambience, Halls 2 subtype, NonLin),
  plus `rooms-studio-a-b1s1-delay-edit.syx` — Studio A stored to B1 R1 with the
  delay block engaged (−6 dB / 188 ms / mod 5) *after* the store, so the delay
  lives only in the payload (blob delay fields read 0); re-confirms the store
  counter — and `charset-b1s1-renamed.syx` —
  same register renamed to `&123456789ABCD`, completing the 6-bit name charset
  (its store counter reads 5, two stores after the delay-edit capture's 3,
  consistent with renaming requiring re-stores) — plus
  `charset-b1s1-rt5s-unstored-edit.syx` — same register with reverb time edited
  to 5.0 s but **not stored**: payload shows the edit, blob keeps the basis
  (first direct blob-vs-payload divergence) — and
  `charset-b1s1-rt5s-stored.syx` — the 5.0 s + delay program **stored to
  B1 R0**: blob updates to the stored values and locates the delay block at
  bits 197–211

## How to capture

1. Store a factory preset into the target register bank/register.
2. Load that register so it is the running program basis.
3. Hold **EDIT** briefly; save the 157-byte SysEx (or concatenate a bank sweep).
4. Name single-dump files by bank and register (`b0-…/slot-3.syx` = Bank 0, Register 3).
