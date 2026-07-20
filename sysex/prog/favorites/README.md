# Favorites capture session

Captures of **front-panel favorites** (the four shortcut buttons) behavior:
hold-EDIT dumps taken after saving to each favorite slot, and hold-PROG dumps
taken with a favorite loaded. One continuous session, numbered in capture
order across two subfolders.

**These dumps are excluded from the PROG corpus scan** (like `../edit/`):
favorite-loaded PROG frames carry offset **94 ≠ 08** and offset **92 = 08**,
which would break the factory-corpus constants otherwise.

## Findings (witnessed here)

| Offsets | Role |
|---------|------|
| 88–91 | **Source program identity** — bank word and slot of the program the favorite was saved from (Deep Ambience = bank 4 slot 9; Nonlin C = bank 10 slot 2). Favorites PROG *sends* never use the MIDI-notes bank 119 |
| 92 | **Panel-mode flag** — `08` while the favorites screen is displayed; `00` program screen; `02` parameter menu open. Not a program property (drops to `00`/`02` when the panel leaves the favorites screen) |
| 94 | **Favorite-source slot** — `(slot − 1) × 2` = `00`/`02`/`04`/`06` for favorites 1–4 on PROG frames; `08` = not loaded from a favorite. Persists across edits and panel-mode changes. Hold-EDIT frames always read `08` |
| 24–87 | Favorite saves write a full **register basis blob** (same layout as register stores) with the store-generation counter always **0** — favorites do not participate in the per-slot counter |
| 93 / 95 | **Untouched by favorites** — they kept reading the last *user register* loaded as basis (B1 R0) through the whole session, register-only semantics confirmed |

### Auto-commit behavior

Favorites persist live edits **without an explicit save**: the edit buffer is
committed into the favorite slot when a **hold-PROG dump is taken while the
favorites screen is displayed** (offset 92 = `08` in the dump that committed,
`13-rt075-favscreen-hold-prog-commit.syx`). Witnessed non-triggers: waiting
(no timed save), a brief PROG press, hold-PROG from the program screen
(92 = `00`, capture 18), and hold-PROG with a parameter menu open (92 = `02`,
capture 21). The committed value persisted across a favorite reload
(capture 20 reads 0.75 s in blob, payload, and on the front panel).

The blob-vs-payload rule from registers still holds per-frame: unstored edits
live only in the payload (captures 12, 15–19, 21–22) until a commit updates
the blob.

## Layout

- `deep-ambience/` — Ambience / Deep Ambience stored to B1 R0, then saved to
  favorites 1–4 (hold-EDIT after each), loaded from each favorite
  (hold-PROG), and re-saved to favorite 1 (counter stays 0)
- `nonlin-c/` — NonLin / Nonlin C saved directly to favorite 1, then a
  reverb-time edit walk (0.2 → 0.75 → 1.0 → 2.0 s) probing when the favorite
  slot commits; filenames flag the commit/no-commit witnesses. Captures 16
  and 17 are byte-identical (the brief PROG press between them changed
  nothing). New reverb-time wire witnesses: encoded **11** = 0.75 s and
  encoded **36** = 2.0 s

## How to capture

1. Save the running program to a favorite (front-panel shortcut buttons);
   hold **EDIT** to dump the resulting basis frame.
2. Navigate to a favorite; hold **PROG** to dump the favorite-loaded frame
   (offsets 92/94 carry the favorite markers).
3. **Warning:** holding PROG while the favorites screen is displayed silently
   commits any unsaved edits into the favorite slot.

## Open follow-ups

- Confirm the commit rule once more with a pending edit on the favorites
  screen (the final 2.0 s commit capture was not taken).
- Power-cycle persistence of an auto-committed favorite.
- **EDIT receive** semantics for favorites (MIDI-notes bank 119 is documented
  for receive; sends never use it).
