"""Corpus-derived layout hints for bytes that never get a one-parameter series.

Findings from scanning every ``sysex/**/*.syx`` dump (parameter series +
``prog/presets``): most former “unknown” payload nibbles are reserved zeros,
fixed constants, or non-sound meta (panel-mode flag / family flag /
engine/bank-class flag). Favorites semantics for offsets 92/94 come from the
``sysex/prog/favorites/`` session (excluded from this corpus scan).

These claims are medium-confidence until a targeted capture proves otherwise.
Series sound-parameter claims always win on conflict.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from ..frame import iter_sysex_messages, parse_sysex
from ..types import is_prog_corpus_dump
from .display_corpus import DISPLAY_ROLE


# Re-export for backward compatibility.
__all__ = ["is_prog_corpus_dump", "CORPUS_LAYOUT_CLAIMS", "verify_corpus_constants"]
# (offsets, status, role, encoding, confidence)
# status: known | secondary
CORPUS_LAYOUT_CLAIMS: tuple[dict[str, Any], ...] = (
    {
        "offsets": [92],
        "status": "secondary",
        "role": (
            "Panel-mode flag: `00` when no parameter menu is open or while "
            "editing a value; `02` while a parameter menu is highlighted "
            "(see `sysex/prog/menus/` captures); `08` while the front-panel "
            "**favorites** screen is shown (see `sysex/prog/favorites/`). "
            "Hold-PROG while this reads `08` commits pending edits into the "
            "favorite slot"
        ),
        "encoding": "raw_u8",
        "confidence": "high",
        "label": "panel mode flag",
    },
    {
        "offsets": [93],
        "status": "known",
        "role": (
            "Register bank (`raw_u8`, manual Bank): `B0`–`B4` = `00`–`04` of "
            "the register currently **loaded as the running basis** (see "
            "`sysex/prog/edit/registers/`); a store alone does not update it "
            "(witnessed `00` after storing to B1 R1 with a factory basis); "
            "`00` on factory/parameter-series dumps in this corpus"
        ),
        "encoding": "raw_u8",
        "confidence": "high",
        "label": "register bank",
    },
    {
        "offsets": [94],
        "status": "known",
        "role": (
            "Favorite-source slot: `(slot - 1) * 2` (`00`/`02`/`04`/`06` = "
            "favorites 1–4) when the running program was loaded from a "
            "front-panel favorite (PROG frames only; persists across edits "
            "and panel-mode changes — see `sysex/prog/favorites/`); `08` "
            "otherwise (all factory/parameter-series and hold-EDIT dumps) — "
            "not a sound parameter"
        ),
        "encoding": "raw_u8",
        "confidence": "high",
        "label": "favorite slot (8 = none)",
    },
    {
        "offsets": [95],
        "status": "known",
        "role": (
            "Register within bank (`raw_u8`, manual Register `0`–`9`) of the "
            "register currently **loaded as the running basis**; a store "
            "alone does not update it (see `sysex/prog/edit/registers/`); "
            "`00` on factory/parameter-series dumps in this corpus"
        ),
        "encoding": "raw_u8",
        "confidence": "high",
        "label": "register",
    },
    {
        "offsets": [96, 97],
        "status": "known",
        "role": (
            "Algorithm/family flag (`nibble_hilo`) from corpus presets "
            "(Halls all 3; most other presets 4, with a few bank-leading "
            "exceptions also 3). High nibble at 96 is always 0. Mirrored at "
            "144–145 as 0 when value=3 and 1 when value=4 — not a clean "
            "V1/V2 bit"
        ),
        "encoding": "nibble_hilo",
        "confidence": "medium",
        "label": "algorithm/family flag",
    },
    {
        "offsets": [98, 99],
        "status": "secondary",
        "role": (
            "Selected front-panel menu index (`nibble_hilo`, 0–17) when a "
            "parameter menu is open; `00 00` when idle. Hardware menu order "
            "matches `PROGRAM_PARAMETERS` in catalog. Offset 92 disambiguates "
            "idle vs Reverb Time (both may show index 0)"
        ),
        "encoding": "nibble_hilo",
        "confidence": "high",
        "label": "selected menu index",
    },
    {
        "offsets": [130],
        "status": "known",
        "role": (
            "Engine/bank-class flag: 0 on classic banks (Halls…Spaces), 1 on "
            "`* 2` banks (Halls 2…Spaces 2), 2 on NonLin. Most parameter-"
            "series dumps show 1 (captured from Large Church, Halls 2); the "
            "LF RT multiply/crossover series show 0 (Large Hall)"
        ),
        "encoding": "raw_u8",
        "confidence": "medium",
        "label": "engine/bank-class flag",
    },
    {
        "offsets": [131],
        "status": "known",
        "role": "Fixed companion to offset 130 (always `02` in this corpus)",
        "encoding": None,
        "confidence": "medium",
        "label": "fixed (always 02)",
    },
    {
        "offsets": [140, 141, 142, 143],
        "status": "known",
        "role": "Reserved block (always 0 in this corpus)",
        "encoding": None,
        "confidence": "medium",
        "label": "reserved (always 0)",
    },
    {
        "offsets": [144, 145],
        "status": "known",
        "role": (
            "Mirror of algorithm/family flag at 96–97 (`nibble_hilo`; "
            "high nibble at 144 always 0). Value 0 when flag=3, 1 when "
            "flag=4 in factory/parameter corpus; live dumps may also show 2"
        ),
        "encoding": "nibble_hilo",
        "confidence": "medium",
        "label": "family-flag mirror",
    },
    {
        "offsets": [146, 147],
        "status": "known",
        "role": DISPLAY_ROLE,
        "encoding": "nibble_hilo",
        "confidence": "high",
        "label": "display",
        "source": "_menus",
    },
    {
        "offsets": [148, 149, 150, 151],
        "status": "known",
        "role": "Reserved (always 0) immediately before checksum nibbles",
        "encoding": None,
        "confidence": "medium",
        "label": "reserved (always 0)",
    },
)


def claim_corpus_layout(
    claim: Callable[..., None],
    *,
    length: int,
    sysex_root: Path | None = None,
    example: bytes | None = None,
    example_source: str | None = None,
) -> list[dict[str, Any]]:
    """Apply corpus-derived claims. Returns the claim records actually applied."""
    verified = verify_corpus_constants(sysex_root) if sysex_root else {}
    applied: list[dict[str, Any]] = []
    for spec in CORPUS_LAYOUT_CLAIMS:
        offsets = [o for o in spec["offsets"] if 0 <= o < length]
        if not offsets:
            continue
        # Skip constant-reserved claims that the live corpus contradicts.
        if sysex_root is not None and spec.get("label", "").startswith("reserved"):
            if any(verified.get(o) not in (None, 0) for o in offsets):
                continue
        if sysex_root is not None and spec["offsets"] == [94]:
            # Offset 94 must stay 08 across the factory corpus (favorite
            # frames with slot codes live outside the corpus scan, under
            # sysex/prog/favorites/).
            if verified.get(94) not in (None, 8):
                continue
        if sysex_root is not None and "always 02" in (spec.get("label") or ""):
            if verified.get(131) not in (None, 2):
                continue

        claim(
            offsets,
            status=spec["status"],
            role=spec["role"],
            parameter=spec.get("source") or "_corpus",
            confidence=spec.get("confidence") or "medium",
            encoding=spec.get("encoding"),
            example=example,
            example_source=example_source,
        )
        applied.append({**spec, "offsets": offsets})
    return applied


def verify_corpus_constants(sysex_root: Path) -> dict[int, int | None]:
    """Return per-offset constant value across all PROG .syx dumps, or None if varied."""
    root = Path(sysex_root)
    if not root.is_dir():
        return {}
    values: dict[int, set[int]] = {}
    for path in root.rglob("*.syx"):
        if not is_prog_corpus_dump(path, root):
            continue
        try:
            messages = list(iter_sysex_messages(path.read_bytes()))
        except ValueError:
            continue
        for message in messages:
            try:
                raw = parse_sysex(message).raw
            except ValueError:
                continue
            for off in range(len(raw)):
                values.setdefault(off, set()).add(raw[off])
    return {off: next(iter(s)) if len(s) == 1 else None for off, s in values.items()}


def overview_label_for_offsets(offsets: list[int]) -> str | None:
    """Short overview label if these offsets match a corpus claim."""
    key = tuple(offsets)
    for spec in CORPUS_LAYOUT_CLAIMS:
        if tuple(spec["offsets"]) == key:
            return spec.get("label")
        # Single-offset lookup inside a multi-byte reserved claim.
        if len(offsets) == 1 and offsets[0] in spec["offsets"]:
            return spec.get("label")
    return None
