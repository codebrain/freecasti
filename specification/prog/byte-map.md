[Overview](README.md) | [Bytes](bytes/README.md) | [Program identity](program-identity.md) | [Preset inventory](preset-inventory.md) | [Preset sheet](preset-sheet.md) | [Byte map](byte-map-overview.md) | [Cross-series](cross.md) | [System dumps](../system/README.md)

# Full byte map

Every offset in the 157-byte program-dump layout.

Short consolidated view: [byte-map-overview.md](byte-map-overview.md).

Codegen layout: [m7_program_dump.ksy](m7_program_dump.ksy) ([Kaitai Struct](https://kaitai.io/)) · [m7_program_dump.spec.json](m7_program_dump.spec.json).

Each sysex/prog/parameters/<parameter>/ folder is an independent dump stream. Byte values are never compared across folders; only per-folder conclusions are merged into this layout map. sysex/prog/presets/ is a separate preset-identity series (bank/program/name). Additional reserved/meta roles come from a corpus scan of all dumps.

Coverage: **154** known/frame/checksum, **3** secondary, **0** unknown (of 157).

Example hex for a known parameter comes only from that parameter’s own folder. Unknown payload bytes show `-` (no shared cross-folder snapshot).

### Regions

| Offsets | Len | Example hex | Status | Meaning |
|---------|-----|-------------|--------|---------|
| 0 | 1 | `F0` | frame | SysEx start (F0) |
| 1-3 | 3 | `00 62 63` | frame | Manufacturer ID (00 62 63) |
| 4-7 | 4 | `70 08 01 00` | frame | Program-dump header (70 08 01 00) |
| 8-21 | 14 | `42 61 73 73 20 20 58 58 ...` | frame | Program name (ASCII, 14-character editable label per manual; space-padded within this field) - confirmed against [sysex/prog/presets/](program-identity.md) filename preset (bank name is not stored here) — see [program name (ASCII)](bytes/program-name.md) |
| 22-23 | 2 | `20 20` | frame | Program name trailing pad (always `0x20` in this corpus; offsets 22–23 complete the 16-byte wire name window) — see [program name pad](bytes/program-name-pad.md) |
| 24-87 | 64 | `20 20 20 20 20 20 20 20 ...` | frame | Register basis blob: factory dumps space-pad with `0x20`; Reg-backed hold-EDIT dumps store a bit-packed snapshot of the **stored register** (low nibbles as a 256-bit stream: 14-char 6-bit name, store-generation counter, all 18 parameters incl. the V2 delay block) — fully decoded in [bytes/register-basis-blob.md](bytes/register-basis-blob.md) (see `sysex/prog/edit/registers/`) |
| 88-89 | 2 | `00 04` | known | Bank index (`nibble_hilo`) from [sysex/prog/presets/](program-identity.md) [Halls](presets/halls/)=0, [Plates](presets/plates/)=1, [Rooms](presets/rooms/)=2, [Chambers](presets/chambers/)=3, [Ambience](presets/ambience/)=4, [Spaces](presets/spaces/)=5, [Halls 2](presets/halls-2/)=6, [Plates 2](presets/plates-2/)=7, [Rooms 2](presets/rooms-2/)=8, [Spaces 2](presets/spaces-2/)=9, [NonLin](presets/nonlin/)=10; mirrored at offsets 136–137 (`nibble_hilo`); hold EDIT sends use index 11 here while mirror 136–137 keep the source bank (see sysex/prog/edit/) — see [bank index](bytes/bank-index.md) |
| 90-91 | 2 | `00 0D` | known | Program slot within bank (`nibble_hilo`) from [sysex/prog/presets/](program-identity.md) (not a global program number) — see [program slot](bytes/program-slot.md) |
| 92 | 1 | `00` | secondary | Panel-mode flag: `00` when no parameter menu is open or while editing a value; `02` while a parameter menu is highlighted (see `sysex/prog/menus/` captures); `08` while the front-panel **favorites** screen is shown (see `sysex/prog/favorites/`). Hold-PROG while this reads `08` commits pending edits into the favorite slot (moved in independent series: [early rolloff](bytes/early-rolloff.md), _corpus) — see [panel mode flag](bytes/panel-mode-flag.md) |
| 93 | 1 | `00` | known | Register bank (`raw_u8`, manual Bank): `B0`–`B4` = `00`–`04` of the register currently **loaded as the running basis** (see `sysex/prog/edit/registers/`); a store alone does not update it (witnessed `00` after storing to B1 R1 with a factory basis); `00` on factory/parameter-series dumps in this corpus — see [register bank](bytes/register-bank.md) |
| 94 | 1 | `08` | known | Favorite-source slot: `(slot - 1) * 2` (`00`/`02`/`04`/`06` = favorites 1–4) when the running program was loaded from a front-panel favorite (PROG frames only; persists across edits and panel-mode changes — see `sysex/prog/favorites/`); `08` otherwise (all factory/parameter-series and hold-EDIT dumps) — not a sound parameter — see [favorite slot (8 = none)](bytes/favorite-slot.md) |
| 95 | 1 | `00` | known | Register within bank (`raw_u8`, manual Register `0`–`9`) of the register currently **loaded as the running basis**; a store alone does not update it (see `sysex/prog/edit/registers/`); `00` on factory/parameter-series dumps in this corpus — see [register](bytes/register.md) |
| 96-97 | 2 | `00 04` | known | Algorithm/family flag (`nibble_hilo`) from corpus presets (Halls all 3; most other presets 4, with a few bank-leading exceptions also 3). High nibble at 96 is always 0. Mirrored at 145 as 0 when value=3 and 1 when value=4 — not a clean V1/V2 bit — see [algorithm/family flag](bytes/algorithm-family-flag.md) |
| 98-99 | 2 | `00 01` | secondary | Selected front-panel menu index (`nibble_hilo`, 0–17) when a parameter menu is open; `00 00` when idle. Hardware menu order matches `PROGRAM_PARAMETERS` in catalog. Offset 92 disambiguates idle vs Reverb Time (both may show index 0) (moved in independent series: _corpus) — see [selected menu index](bytes/selected-menu-index.md) |
| 100-101 | 2 | `00 01` | known | Parameter [`reverb time`](bytes/reverb-time.md) (from independent series [sysex/prog/parameters/reverb time/](bytes/reverb-time.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 102-103 | 2 | `00 01` | known | Parameter [`size`](bytes/size.md) (from independent series [sysex/prog/parameters/size/](bytes/size.md)) (nibble_hilo, label = encoded * 1) |
| 104-105 | 2 | `00 00` | known | Parameter [`predelay`](bytes/predelay.md) (from independent series [sysex/prog/parameters/predelay/](bytes/predelay.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 106-107 | 2 | `00 00` | known | Parameter [`diffusion`](bytes/diffusion.md) (from independent series [sysex/prog/parameters/diffusion/](bytes/diffusion.md)) (nibble_hilo, label = encoded * 1) |
| 108-109 | 2 | `00 00` | known | Parameter [`density`](bytes/density.md) (from independent series [sysex/prog/parameters/density/](bytes/density.md)) (nibble_hilo, label = encoded * 1) |
| 110-111 | 2 | `00 01` | known | Parameter [`modulation`](bytes/modulation.md) (from independent series [sysex/prog/parameters/modulation/](bytes/modulation.md)) (nibble_hilo, label = encoded + (-1)) |
| 112-113 | 2 | `00 01` | known | Parameter [`rolloff`](bytes/rolloff.md) (from independent series [sysex/prog/parameters/rolloff/](bytes/rolloff.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 114-115 | 2 | `00 00` | known | Parameter [`hf rt multiply`](bytes/hf-rt-multiply.md) (from independent series [sysex/prog/parameters/hf rt multiply/](bytes/hf-rt-multiply.md)) (nibble_hilo, label = encoded * 0.05 + (0.2)) |
| 116-117 | 2 | `01 0E` | known | Parameter [`hf rt crossover`](bytes/hf-rt-crossover.md) (from independent series [sysex/prog/parameters/hf rt crossover/](bytes/hf-rt-crossover.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 118-119 | 2 | `00 00` | known | Parameter [`lf rt multiply`](bytes/lf-rt-multiply.md) (from independent series [sysex/prog/parameters/lf rt multiply/](bytes/lf-rt-multiply.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 120-121 | 2 | `00 01` | known | Parameter [`lf rt crossover`](bytes/lf-rt-crossover.md) (from independent series [sysex/prog/parameters/lf rt crossover/](bytes/lf-rt-crossover.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 122-123 | 2 | `00 0A` | known | Parameter [`vlf cut`](bytes/vlf-cut.md) (from independent series [sysex/prog/parameters/vlf cut/](bytes/vlf-cut.md)) (nibble_hilo, label = encoded + (-20)) |
| 124-125 | 2 | `00 00` | known | Parameter [`early to reverb mix`](bytes/early-to-reverb-mix.md) (from independent series [sysex/prog/parameters/early to reverb mix/](bytes/early-to-reverb-mix.md)) (nibble_hilo, label = encoded * 1) |
| 126-127 | 2 | `00 01` | known | Parameter [`early rolloff`](bytes/early-rolloff.md) (from independent series [sysex/prog/parameters/early rolloff/](bytes/early-rolloff.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 128-129 | 2 | `00 00` | known | Parameter [`early select`](bytes/early-select.md) (from independent series [sysex/prog/parameters/early select/](bytes/early-select.md)) (nibble_hilo, label = encoded * 1) |
| 130 | 1 | `00` | known | Engine/bank-class flag: 0 on classic banks (Halls…Spaces), 1 on `* 2` banks (Halls 2…Spaces 2), 2 on NonLin. Most parameter-series dumps show 1 (captured from Large Church, Halls 2); the LF RT multiply/crossover series show 0 (Large Hall) — see [engine/bank-class flag](bytes/engine-bank-class-flag.md) |
| 131 | 1 | `02` | known | Fixed companion to offset 130 (always `02` in this corpus) |
| 132-133 | 2 | `00 00` | known | Parameter [`delay level`](bytes/delay-level.md) (from independent series [sysex/prog/parameters/delay level/](bytes/delay-level.md)) (nibble_hilo, label = encoded + (-21)) |
| 134-135 | 2 | `00 00` | known | Parameter [`delay time`](bytes/delay-time.md) (from independent series [sysex/prog/parameters/delay time/](bytes/delay-time.md)) (nibble_hilo, label = encoded * 8 + (100)) |
| 136-137 | 2 | `00 04` | known | Bank index mirror (`nibble_hilo`, equals bank word at 88–89) from [sysex/prog/presets/](program-identity.md); on hold-EDIT dumps this stays the source bank while 88-89 are Edit index 11 — see [bank index mirror](bytes/bank-index.md) |
| 138-139 | 2 | `00 01` | known | Parameter [`delay modulation`](bytes/delay-modulation.md) (from independent series [sysex/prog/parameters/delay modulation/](bytes/delay-modulation.md)) (nibble_hilo, label = encoded + (-1)) |
| 140-144 | 5 | `00 00 00 00 00` | known | Reserved block (always 0 in this corpus) |
| 145 | 1 | `01` | known | Mirror of algorithm/family flag at 96–97 (145=0 when value=3; 145=1 when value=4 in this corpus) — see [family-flag mirror](bytes/algorithm-family-flag.md) |
| 146-147 | 2 | `03 0D` | known | Display (`nibble_hilo`): front-panel UI focus code (not a sound parameter). Browse (`92=02`): menu-row highlight (`menu_index+28` for indices 1–17; reverb time → 46). Edit (`92=00`): value-focus code in a parameter-specific band that advances as the shown value changes (not a fixed edit anchor). From `sysex/prog/menus/` + parameter series — see [display](bytes/display.md) |
| 148-151 | 4 | `00 00 00 00` | known | Reserved (always 0) immediately before checksum nibbles |
| 152-155 | 4 | - | checksum | Checksum: CRC-16/ARC over offsets 8-151 (name + payload), packed as four high-nibble-first SysEx bytes (per-dump; recompute after edits - do not copy across parameter series) |
| 156 | 1 | `F7` | frame | SysEx end (F7) |


_Last exported: 2026-07-21_
