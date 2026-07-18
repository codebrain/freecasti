[Overview](README.md) | [Bytes](bytes/README.md) | [Program identity](program-identity.md) | [Preset inventory](preset-inventory.md) | [Preset sheet](preset-sheet.md) | [Byte map](byte-map-overview.md) | [Cross-series](cross.md) | [System dumps](../system/README.md)

# Full byte map

Every offset in the 157-byte program-dump layout.

Short consolidated view: [byte-map-overview.md](byte-map-overview.md).

Codegen layout: [m7_program_dump.ksy](m7_program_dump.ksy) ([Kaitai Struct](https://kaitai.io/)) · [m7_program_dump.spec.json](m7_program_dump.spec.json).

Each sysex/<parameter>/ folder is an independent dump stream. Byte values are never compared across folders; only per-folder conclusions are merged into this layout map. sysex/_presets/ is a separate preset-identity series (bank/program/name). Additional reserved/meta roles come from a corpus scan of all dumps.

Coverage: **154** known/frame/checksum, **3** secondary, **0** unknown (of 157).

Example hex for a known parameter comes only from that parameter’s own folder. Unknown payload bytes show `-` (no shared cross-folder snapshot).

### Regions

| Offsets | Len | Example hex | Status | Meaning |
|---------|-----|-------------|--------|---------|
| 0 | 1 | `F0` | frame | SysEx start (F0) |
| 1-3 | 3 | `00 62 63` | frame | Manufacturer ID (00 62 63) |
| 4-7 | 4 | `70 08 01 00` | frame | Program-dump header (70 08 01 00) |
| 8-87 | 80 | `42 61 73 73 20 20 58 58 ...` | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 88-89 | 2 | `00 04` | known | Bank index (`nibble_hilo`) from [sysex/_presets/](program-identity.md) [Halls](presets/halls/)=0, [Plates](presets/plates/)=1, [Rooms](presets/rooms/)=2, [Chambers](presets/chambers/)=3, [Ambience](presets/ambience/)=4, [Spaces](presets/spaces/)=5, [Halls 2](presets/halls-2/)=6, [Plates 2](presets/plates-2/)=7, [Rooms 2](presets/rooms-2/)=8, [Spaces 2](presets/spaces-2/)=9, [NonLin](presets/nonlin/)=10; mirrored at offset 137; hold EDIT sends use index 11 here while mirror 137 keeps the source bank (see sysex/_edit/) |
| 90-91 | 2 | `00 0D` | known | Program slot within bank (`nibble_hilo`) from [sysex/_presets/](program-identity.md) (not a global program number) |
| 92 | 1 | `00` | secondary | Menu-browse flag: `00` when no parameter menu is open or while editing a value; `02` while a parameter menu is highlighted (see `sysex/prog/menus/` captures) (moved in independent series: [early rolloff](bytes/early-rolloff.md), _corpus) |
| 93-94 | 2 | `00 08` | known | Fixed field (always `00 08` / encoded 8 in this corpus) — likely structure/version; not a sound parameter |
| 95-96 | 2 | `00 00` | known | Reserved (always `00 00` in this corpus) |
| 97 | 1 | `04` | known | Algorithm/family flag from corpus presets (Halls all 3; most other presets 4, with a few bank-leading exceptions also 3). Mirrored at 145 as 0 when 97=3 and 1 when 97=4 — not a clean V1/V2 bit |
| 98-99 | 2 | `00 01` | secondary | Selected front-panel menu index (`nibble_hilo`, 0–17) when a parameter menu is open; `00 00` when idle. Hardware menu order matches `PROGRAM_PARAMETERS` in catalog. Offset 92 disambiguates idle vs Reverb Time (both may show index 0) (moved in independent series: _corpus) |
| 100-101 | 2 | `00 01` | known | Parameter [`reverb time`](bytes/reverb-time.md) (from independent series [sysex/reverb time/](bytes/reverb-time.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 102-103 | 2 | `00 01` | known | Parameter [`size`](bytes/size.md) (from independent series [sysex/size/](bytes/size.md)) (nibble_hilo, label = encoded * 1) |
| 104-105 | 2 | `00 00` | known | Parameter [`predelay`](bytes/predelay.md) (from independent series [sysex/predelay/](bytes/predelay.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 106 | 1 | `00` | known | Reserved padding (always 0) between predelay and diffusion |
| 107 | 1 | `00` | known | Parameter [`diffusion`](bytes/diffusion.md) (from independent series [sysex/diffusion/](bytes/diffusion.md)) (raw_u8, label = encoded * 1) |
| 108 | 1 | `00` | known | Reserved padding (always 0) between diffusion and density |
| 109 | 1 | `00` | known | Parameter [`density`](bytes/density.md) (from independent series [sysex/density/](bytes/density.md)) (raw_u8, label = encoded * 1) |
| 110 | 1 | `00` | known | Reserved padding (always 0) between density and modulation |
| 111 | 1 | `01` | known | Parameter [`modulation`](bytes/modulation.md) (from independent series [sysex/modulation/](bytes/modulation.md)) (raw_u8, label = encoded + (-1)) |
| 112-113 | 2 | `00 01` | known | Parameter [`rolloff`](bytes/rolloff.md) (from independent series [sysex/rolloff/](bytes/rolloff.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 114-115 | 2 | `00 00` | known | Parameter [`hf rt multiply`](bytes/hf-rt-multiply.md) (from independent series [sysex/hf rt multiply/](bytes/hf-rt-multiply.md)) (nibble_hilo, label = encoded * 0.05 + (0.2)) |
| 116-117 | 2 | `01 0E` | known | Parameter [`hf rt crossover`](bytes/hf-rt-crossover.md) (from independent series [sysex/hf rt crossover/](bytes/hf-rt-crossover.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 118-119 | 2 | `00 00` | known | Parameter [`lf rt multiply`](bytes/lf-rt-multiply.md) (from independent series [sysex/lf rt multiply/](bytes/lf-rt-multiply.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 120-121 | 2 | `00 01` | known | Parameter [`lf rt crossover`](bytes/lf-rt-crossover.md) (from independent series [sysex/lf rt crossover/](bytes/lf-rt-crossover.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 122-123 | 2 | `00 0A` | known | Parameter [`vlf cut`](bytes/vlf-cut.md) (from independent series [sysex/vlf cut/](bytes/vlf-cut.md)) (nibble_hilo, label = encoded + (-20)) |
| 124-125 | 2 | `00 00` | known | Parameter [`early to reverb mix`](bytes/early-to-reverb-mix.md) (from independent series [sysex/early to reverb mix/](bytes/early-to-reverb-mix.md)) (nibble_hilo, label = encoded * 1) |
| 126-127 | 2 | `00 01` | known | Parameter [`early rolloff`](bytes/early-rolloff.md) (from independent series [sysex/early rolloff/](bytes/early-rolloff.md)) (nibble_hilo, table/index candidate (monotonic 100%)) |
| 128-129 | 2 | `00 00` | known | Parameter [`early select`](bytes/early-select.md) (from independent series [sysex/early select/](bytes/early-select.md)) (nibble_hilo, label = encoded * 1) |
| 130 | 1 | `00` | known | Engine/bank-class flag: 0 on classic banks (Halls…Spaces), 1 on `* 2` banks (Halls 2…Spaces 2), 2 on NonLin. Parameter-series dumps also show 1 because they were captured from Large Church (Halls 2) |
| 131-132 | 2 | `02 00` | known | Fixed companion to offset 130 (always `02 00` in this corpus) |
| 133 | 1 | `00` | known | Parameter [`delay level`](bytes/delay-level.md) (from independent series [sysex/delay level/](bytes/delay-level.md)) (raw_u8, label = encoded + (-21)) |
| 134-135 | 2 | `00 00` | known | Parameter [`delay time`](bytes/delay-time.md) (from independent series [sysex/delay time/](bytes/delay-time.md)) (nibble_hilo, label = encoded * 8 + (100)) |
| 136 | 1 | `00` | known | Reserved (always 0) between delay time and bank-index mirror |
| 137 | 1 | `04` | known | Bank index mirror (equals offset 89) from [sysex/_presets/](program-identity.md); on hold-EDIT dumps this stays the source bank while 88-89 are Edit index 11 |
| 138 | 1 | `00` | known | Reserved (always 0) between bank-index mirror and delay modulation |
| 139 | 1 | `01` | known | Parameter [`delay modulation`](bytes/delay-modulation.md) (from independent series [sysex/delay modulation/](bytes/delay-modulation.md)) (raw_u8, label = encoded + (-1)) |
| 140-144 | 5 | `00 00 00 00 00` | known | Reserved block (always 0 in this corpus) |
| 145 | 1 | `01` | known | Mirror of algorithm/family flag at 97 (145=0 when 97=3; 145=1 when 97=4 in this corpus) |
| 146-147 | 2 | `03 0D` | known | Display (`nibble_hilo`): high nibble = page/row while browsing (`92=02`) or edit anchor while changing a value (`92=00`); low nibble = position within the menu page, or value-display position while editing. From `sysex/prog/menus/` captures |
| 148-151 | 4 | `00 00 00 00` | known | Reserved (always 0) immediately before checksum nibbles |
| 152-155 | 4 | - | checksum | Checksum: CRC-16/ARC over offsets 8-151 (name + payload), packed as four high-nibble-first SysEx bytes (per-dump; recompute after edits - do not copy across parameter series) |
| 156 | 1 | `F7` | frame | SysEx end (F7) |

### Per-byte map

| Offset | Hex | Source | Status | Meaning |
|--------|-----|--------|--------|---------|
| 0 | `F0` | frame constant | frame | SysEx start (F0) |
| 1 | `00` | frame constant | frame | Manufacturer ID (00 62 63) |
| 2 | `62` | frame constant | frame | Manufacturer ID (00 62 63) |
| 3 | `63` | frame constant | frame | Manufacturer ID (00 62 63) |
| 4 | `70` | frame constant | frame | Program-dump header (70 08 01 00) |
| 5 | `08` | frame constant | frame | Program-dump header (70 08 01 00) |
| 6 | `01` | frame constant | frame | Program-dump header (70 08 01 00) |
| 7 | `00` | frame constant | frame | Program-dump header (70 08 01 00) |
| 8 | `42` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 9 | `61` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 10 | `73` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 11 | `73` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 12 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 13 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 14 | `58` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 15 | `58` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 16 | `4C` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 17 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 18 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 19 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 20 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 21 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 22 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 23 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 24 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 25 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 26 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 27 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 28 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 29 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 30 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 31 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 32 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 33 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 34 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 35 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 36 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 37 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 38 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 39 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 40 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 41 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 42 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 43 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 44 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 45 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 46 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 47 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 48 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 49 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 50 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 51 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 52 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 53 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 54 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 55 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 56 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 57 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 58 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 59 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 60 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 61 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 62 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 63 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 64 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 65 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 66 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 67 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 68 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 69 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 70 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 71 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 72 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 73 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 74 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 75 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 76 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 77 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 78 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 79 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 80 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 81 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 82 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 83 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 84 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 85 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 86 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 87 | `20` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | frame | Program name (ASCII, space-padded) - confirmed against [sysex/_presets/](program-identity.md) filename preset (bank name is not stored here) |
| 88 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Bank index (`nibble_hilo`) from [sysex/_presets/](program-identity.md) [Halls](presets/halls/)=0, [Plates](presets/plates/)=1, [Rooms](presets/rooms/)=2, [Chambers](presets/chambers/)=3, [Ambience](presets/ambience/)=4, [Spaces](presets/spaces/)=5, [Halls 2](presets/halls-2/)=6, [Plates 2](presets/plates-2/)=7, [Rooms 2](presets/rooms-2/)=8, [Spaces 2](presets/spaces-2/)=9, [NonLin](presets/nonlin/)=10; mirrored at offset 137; hold EDIT sends use index 11 here while mirror 137 keeps the source bank (see sysex/_edit/) [high] |
| 89 | `04` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Bank index (`nibble_hilo`) from [sysex/_presets/](program-identity.md) [Halls](presets/halls/)=0, [Plates](presets/plates/)=1, [Rooms](presets/rooms/)=2, [Chambers](presets/chambers/)=3, [Ambience](presets/ambience/)=4, [Spaces](presets/spaces/)=5, [Halls 2](presets/halls-2/)=6, [Plates 2](presets/plates-2/)=7, [Rooms 2](presets/rooms-2/)=8, [Spaces 2](presets/spaces-2/)=9, [NonLin](presets/nonlin/)=10; mirrored at offset 137; hold EDIT sends use index 11 here while mirror 137 keeps the source bank (see sysex/_edit/) [high] |
| 90 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Program slot within bank (`nibble_hilo`) from [sysex/_presets/](program-identity.md) (not a global program number) [high] |
| 91 | `0D` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Program slot within bank (`nibble_hilo`) from [sysex/_presets/](program-identity.md) (not a global program number) [high] |
| 92 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | secondary | Menu-browse flag: `00` when no parameter menu is open or while editing a value; `02` while a parameter menu is highlighted (see `sysex/prog/menus/` captures) (moved in independent series: [early rolloff](bytes/early-rolloff.md), _corpus) |
| 93 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Fixed field (always `00 08` / encoded 8 in this corpus) — likely structure/version; not a sound parameter [medium] |
| 94 | `08` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Fixed field (always `00 08` / encoded 8 in this corpus) — likely structure/version; not a sound parameter [medium] |
| 95 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved (always `00 00` in this corpus) [medium] |
| 96 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved (always `00 00` in this corpus) [medium] |
| 97 | `04` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Algorithm/family flag from corpus presets (Halls all 3; most other presets 4, with a few bank-leading exceptions also 3). Mirrored at 145 as 0 when 97=3 and 1 when 97=4 — not a clean V1/V2 bit [medium] |
| 98 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | secondary | Selected front-panel menu index (`nibble_hilo`, 0–17) when a parameter menu is open; `00 00` when idle. Hardware menu order matches `PROGRAM_PARAMETERS` in catalog. Offset 92 disambiguates idle vs Reverb Time (both may show index 0) (moved in independent series: _corpus) |
| 99 | `01` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | secondary | Selected front-panel menu index (`nibble_hilo`, 0–17) when a parameter menu is open; `00 00` when idle. Hardware menu order matches `PROGRAM_PARAMETERS` in catalog. Offset 92 disambiguates idle vs Reverb Time (both may show index 0) (moved in independent series: _corpus) |
| 100 | `00` | C:\m7\sysex\prog\parameters\reverb time\0.25s.syx | known | Parameter [`reverb time`](bytes/reverb-time.md) (from independent series [sysex/reverb time/](bytes/reverb-time.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 101 | `01` | C:\m7\sysex\prog\parameters\reverb time\0.25s.syx | known | Parameter [`reverb time`](bytes/reverb-time.md) (from independent series [sysex/reverb time/](bytes/reverb-time.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 102 | `00` | C:\m7\sysex\prog\parameters\size\1.syx | known | Parameter [`size`](bytes/size.md) (from independent series [sysex/size/](bytes/size.md)) (nibble_hilo, label = encoded * 1) [high] |
| 103 | `01` | C:\m7\sysex\prog\parameters\size\1.syx | known | Parameter [`size`](bytes/size.md) (from independent series [sysex/size/](bytes/size.md)) (nibble_hilo, label = encoded * 1) [high] |
| 104 | `00` | C:\m7\sysex\prog\parameters\predelay\0ms.syx | known | Parameter [`predelay`](bytes/predelay.md) (from independent series [sysex/predelay/](bytes/predelay.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 105 | `00` | C:\m7\sysex\prog\parameters\predelay\0ms.syx | known | Parameter [`predelay`](bytes/predelay.md) (from independent series [sysex/predelay/](bytes/predelay.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 106 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved padding (always 0) between predelay and diffusion [medium] |
| 107 | `00` | C:\m7\sysex\prog\parameters\diffusion\low.syx | known | Parameter [`diffusion`](bytes/diffusion.md) (from independent series [sysex/diffusion/](bytes/diffusion.md)) (raw_u8, label = encoded * 1) [high] |
| 108 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved padding (always 0) between diffusion and density [medium] |
| 109 | `00` | C:\m7\sysex\prog\parameters\density\low.syx | known | Parameter [`density`](bytes/density.md) (from independent series [sysex/density/](bytes/density.md)) (raw_u8, label = encoded * 1) [high] |
| 110 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved padding (always 0) between density and modulation [medium] |
| 111 | `01` | C:\m7\sysex\prog\parameters\modulation\low.syx | known | Parameter [`modulation`](bytes/modulation.md) (from independent series [sysex/modulation/](bytes/modulation.md)) (raw_u8, label = encoded + (-1)) [high] |
| 112 | `00` | C:\m7\sysex\prog\parameters\rolloff\120hz.syx | known | Parameter [`rolloff`](bytes/rolloff.md) (from independent series [sysex/rolloff/](bytes/rolloff.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 113 | `01` | C:\m7\sysex\prog\parameters\rolloff\120hz.syx | known | Parameter [`rolloff`](bytes/rolloff.md) (from independent series [sysex/rolloff/](bytes/rolloff.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 114 | `00` | C:\m7\sysex\prog\parameters\hf rt multiply\0.2.syx | known | Parameter [`hf rt multiply`](bytes/hf-rt-multiply.md) (from independent series [sysex/hf rt multiply/](bytes/hf-rt-multiply.md)) (nibble_hilo, label = encoded * 0.05 + (0.2)) [high] |
| 115 | `00` | C:\m7\sysex\prog\parameters\hf rt multiply\0.2.syx | known | Parameter [`hf rt multiply`](bytes/hf-rt-multiply.md) (from independent series [sysex/hf rt multiply/](bytes/hf-rt-multiply.md)) (nibble_hilo, label = encoded * 0.05 + (0.2)) [high] |
| 116 | `01` | C:\m7\sysex\prog\parameters\hf rt crossover\11200hz.syx | known | Parameter [`hf rt crossover`](bytes/hf-rt-crossover.md) (from independent series [sysex/hf rt crossover/](bytes/hf-rt-crossover.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 117 | `0E` | C:\m7\sysex\prog\parameters\hf rt crossover\11200hz.syx | known | Parameter [`hf rt crossover`](bytes/hf-rt-crossover.md) (from independent series [sysex/hf rt crossover/](bytes/hf-rt-crossover.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 118 | `00` | C:\m7\sysex\prog\parameters\lf rt multiply\0.2.syx | known | Parameter [`lf rt multiply`](bytes/lf-rt-multiply.md) (from independent series [sysex/lf rt multiply/](bytes/lf-rt-multiply.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 119 | `00` | C:\m7\sysex\prog\parameters\lf rt multiply\0.2.syx | known | Parameter [`lf rt multiply`](bytes/lf-rt-multiply.md) (from independent series [sysex/lf rt multiply/](bytes/lf-rt-multiply.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 120 | `00` | C:\m7\sysex\prog\parameters\lf rt crossover\120hz.syx | known | Parameter [`lf rt crossover`](bytes/lf-rt-crossover.md) (from independent series [sysex/lf rt crossover/](bytes/lf-rt-crossover.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 121 | `01` | C:\m7\sysex\prog\parameters\lf rt crossover\120hz.syx | known | Parameter [`lf rt crossover`](bytes/lf-rt-crossover.md) (from independent series [sysex/lf rt crossover/](bytes/lf-rt-crossover.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 122 | `00` | C:\m7\sysex\prog\parameters\vlf cut\-10db.syx | known | Parameter [`vlf cut`](bytes/vlf-cut.md) (from independent series [sysex/vlf cut/](bytes/vlf-cut.md)) (nibble_hilo, label = encoded + (-20)) [high] |
| 123 | `0A` | C:\m7\sysex\prog\parameters\vlf cut\-10db.syx | known | Parameter [`vlf cut`](bytes/vlf-cut.md) (from independent series [sysex/vlf cut/](bytes/vlf-cut.md)) (nibble_hilo, label = encoded + (-20)) [high] |
| 124 | `00` | C:\m7\sysex\prog\parameters\early to reverb mix\0.20.syx | known | Parameter [`early to reverb mix`](bytes/early-to-reverb-mix.md) (from independent series [sysex/early to reverb mix/](bytes/early-to-reverb-mix.md)) (nibble_hilo, label = encoded * 1) [high] |
| 125 | `00` | C:\m7\sysex\prog\parameters\early to reverb mix\0.20.syx | known | Parameter [`early to reverb mix`](bytes/early-to-reverb-mix.md) (from independent series [sysex/early to reverb mix/](bytes/early-to-reverb-mix.md)) (nibble_hilo, label = encoded * 1) [high] |
| 126 | `00` | C:\m7\sysex\prog\parameters\early rolloff\120hz.syx | known | Parameter [`early rolloff`](bytes/early-rolloff.md) (from independent series [sysex/early rolloff/](bytes/early-rolloff.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 127 | `01` | C:\m7\sysex\prog\parameters\early rolloff\120hz.syx | known | Parameter [`early rolloff`](bytes/early-rolloff.md) (from independent series [sysex/early rolloff/](bytes/early-rolloff.md)) (nibble_hilo, table/index candidate (monotonic 100%)) [medium] |
| 128 | `00` | C:\m7\sysex\prog\parameters\early select\0.syx | known | Parameter [`early select`](bytes/early-select.md) (from independent series [sysex/early select/](bytes/early-select.md)) (nibble_hilo, label = encoded * 1) [high] |
| 129 | `00` | C:\m7\sysex\prog\parameters\early select\0.syx | known | Parameter [`early select`](bytes/early-select.md) (from independent series [sysex/early select/](bytes/early-select.md)) (nibble_hilo, label = encoded * 1) [high] |
| 130 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Engine/bank-class flag: 0 on classic banks (Halls…Spaces), 1 on `* 2` banks (Halls 2…Spaces 2), 2 on NonLin. Parameter-series dumps also show 1 because they were captured from Large Church (Halls 2) [medium] |
| 131 | `02` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Fixed companion to offset 130 (always `02 00` in this corpus) [medium] |
| 132 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Fixed companion to offset 130 (always `02 00` in this corpus) [medium] |
| 133 | `00` | C:\m7\sysex\prog\parameters\delay level\off.syx | known | Parameter [`delay level`](bytes/delay-level.md) (from independent series [sysex/delay level/](bytes/delay-level.md)) (raw_u8, label = encoded + (-21)) [high] |
| 134 | `00` | C:\m7\sysex\prog\parameters\delay time\100ms.syx | known | Parameter [`delay time`](bytes/delay-time.md) (from independent series [sysex/delay time/](bytes/delay-time.md)) (nibble_hilo, label = encoded * 8 + (100)) [high] |
| 135 | `00` | C:\m7\sysex\prog\parameters\delay time\100ms.syx | known | Parameter [`delay time`](bytes/delay-time.md) (from independent series [sysex/delay time/](bytes/delay-time.md)) (nibble_hilo, label = encoded * 8 + (100)) [high] |
| 136 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved (always 0) between delay time and bank-index mirror [medium] |
| 137 | `04` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Bank index mirror (equals offset 89) from [sysex/_presets/](program-identity.md); on hold-EDIT dumps this stays the source bank while 88-89 are Edit index 11 [high] |
| 138 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved (always 0) between bank-index mirror and delay modulation [medium] |
| 139 | `01` | C:\m7\sysex\prog\parameters\delay modulation\low.syx | known | Parameter [`delay modulation`](bytes/delay-modulation.md) (from independent series [sysex/delay modulation/](bytes/delay-modulation.md)) (raw_u8, label = encoded + (-1)) [high] |
| 140 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved block (always 0 in this corpus) [medium] |
| 141 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved block (always 0 in this corpus) [medium] |
| 142 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved block (always 0 in this corpus) [medium] |
| 143 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved block (always 0 in this corpus) [medium] |
| 144 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved block (always 0 in this corpus) [medium] |
| 145 | `01` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Mirror of algorithm/family flag at 97 (145=0 when 97=3; 145=1 when 97=4 in this corpus) [medium] |
| 146 | `03` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Display (`nibble_hilo`): high nibble = page/row while browsing (`92=02`) or edit anchor while changing a value (`92=00`); low nibble = position within the menu page, or value-display position while editing. From `sysex/prog/menus/` captures [high] |
| 147 | `0D` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Display (`nibble_hilo`): high nibble = page/row while browsing (`92=02`) or edit anchor while changing a value (`92=00`); low nibble = position within the menu page, or value-display position while editing. From `sysex/prog/menus/` captures [high] |
| 148 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved (always 0) immediately before checksum nibbles [medium] |
| 149 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved (always 0) immediately before checksum nibbles [medium] |
| 150 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved (always 0) immediately before checksum nibbles [medium] |
| 151 | `00` | C:\m7\sysex\prog\presets\Ambience.Bass  XXL.syx | known | Reserved (always 0) immediately before checksum nibbles [medium] |
| 152 | - | - | checksum | Checksum: CRC-16/ARC over offsets 8-151 (name + payload), packed as four high-nibble-first SysEx bytes (per-dump; recompute after edits - do not copy across parameter series) |
| 153 | - | - | checksum | Checksum: CRC-16/ARC over offsets 8-151 (name + payload), packed as four high-nibble-first SysEx bytes (per-dump; recompute after edits - do not copy across parameter series) |
| 154 | - | - | checksum | Checksum: CRC-16/ARC over offsets 8-151 (name + payload), packed as four high-nibble-first SysEx bytes (per-dump; recompute after edits - do not copy across parameter series) |
| 155 | - | - | checksum | Checksum: CRC-16/ARC over offsets 8-151 (name + payload), packed as four high-nibble-first SysEx bytes (per-dump; recompute after edits - do not copy across parameter series) |
| 156 | `F7` | frame constant | frame | SysEx end (F7) |


_Last exported: 2026-07-18_
