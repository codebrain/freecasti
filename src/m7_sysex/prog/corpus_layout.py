"""Corpus-derived layout hints for bytes that never get a one-parameter series.

Findings from scanning every ``sysex/**/*.syx`` dump (parameter series +
``_presets``): most former “unknown” payload nibbles are reserved zeros,
fixed constants, or non-sound meta (family flag / edit generation /
engine/bank-class flag).

These claims are medium-confidence until a targeted capture proves otherwise.
Series sound-parameter claims always win on conflict.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from ..frame import parse_sysex
from ..types import is_prog_corpus_dump


# Re-export for backward compatibility.
__all__ = ["is_prog_corpus_dump", "CORPUS_LAYOUT_CLAIMS", "verify_corpus_constants"]
# (offsets, status, role, encoding, confidence)
# status: known | secondary
CORPUS_LAYOUT_CLAIMS: tuple[dict[str, Any], ...] = (
    {
        "offsets": [92],
        "status": "secondary",
        "role": (
            "Menu-browse flag: `00` when no parameter menu is open or while "
            "editing a value; `02` while a parameter menu is highlighted "
            "(see `sysex/prog/menus/` captures)"
        ),
        "encoding": "raw_u8",
        "confidence": "high",
        "label": "menu browse flag",
    },
    {
        "offsets": [93],
        "status": "known",
        "role": (
            "Register bank page (`raw_u8`): `B0`=`00` … when the dump basis is a "
            "user register (see `sysex/prog/edit/registers/`); `00` on "
            "factory/parameter-series dumps in this corpus"
        ),
        "encoding": "raw_u8",
        "confidence": "high",
        "label": "register page",
    },
    {
        "offsets": [94],
        "status": "known",
        "role": (
            "Structure/version constant (`08` in all witnessed program dumps) — "
            "not a sound parameter"
        ),
        "encoding": "raw_u8",
        "confidence": "high",
        "label": "structure version (always 8)",
    },
    {
        "offsets": [95],
        "status": "known",
        "role": (
            "Register slot within page (`0`–`9`) when the dump basis is a user "
            "register; `00` on factory/parameter-series dumps in this corpus"
        ),
        "encoding": "raw_u8",
        "confidence": "high",
        "label": "register slot",
    },
    {
        "offsets": [96],
        "status": "known",
        "role": "Reserved/unknown (always `00` in witnessed captures)",
        "encoding": None,
        "confidence": "medium",
        "label": "reserved (always 0)",
    },
    {
        "offsets": [97],
        "status": "known",
        "role": (
            "Algorithm/family flag from corpus presets (Halls all 3; most other "
            "presets 4, with a few bank-leading exceptions also 3). Mirrored at "
            "145 as 0 when 97=3 and 1 when 97=4 — not a clean V1/V2 bit"
        ),
        "encoding": "raw_u8",
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
        "offsets": [106],
        "status": "known",
        "role": "Reserved padding (always 0) between predelay and diffusion",
        "encoding": None,
        "confidence": "medium",
        "label": "reserved padding",
    },
    {
        "offsets": [108],
        "status": "known",
        "role": "Reserved padding (always 0) between diffusion and density",
        "encoding": None,
        "confidence": "medium",
        "label": "reserved padding",
    },
    {
        "offsets": [110],
        "status": "known",
        "role": "Reserved padding (always 0) between density and modulation",
        "encoding": None,
        "confidence": "medium",
        "label": "reserved padding",
    },
    {
        "offsets": [130],
        "status": "known",
        "role": (
            "Engine/bank-class flag: 0 on classic banks (Halls…Spaces), 1 on "
            "`* 2` banks (Halls 2…Spaces 2), 2 on NonLin. Parameter-series "
            "dumps also show 1 because they were captured from Large Church "
            "(Halls 2)"
        ),
        "encoding": "raw_u8",
        "confidence": "medium",
        "label": "engine/bank-class flag",
    },
    {
        "offsets": [131, 132],
        "status": "known",
        "role": "Fixed companion to offset 130 (always `02 00` in this corpus)",
        "encoding": None,
        "confidence": "medium",
        "label": "fixed (always 02 00)",
    },
    {
        "offsets": [136],
        "status": "known",
        "role": "Reserved (always 0) between delay time and bank-index mirror",
        "encoding": None,
        "confidence": "medium",
        "label": "reserved (always 0)",
    },
    {
        "offsets": [138],
        "status": "known",
        "role": "Reserved (always 0) between bank-index mirror and delay modulation",
        "encoding": None,
        "confidence": "medium",
        "label": "reserved (always 0)",
    },
    {
        "offsets": [140, 141, 142, 143, 144],
        "status": "known",
        "role": "Reserved block (always 0 in this corpus)",
        "encoding": None,
        "confidence": "medium",
        "label": "reserved (always 0)",
    },
    {
        "offsets": [145],
        "status": "known",
        "role": (
            "Mirror of algorithm/family flag at 97 "
            "(145=0 when 97=3; 145=1 when 97=4 in this corpus)"
        ),
        "encoding": "raw_u8",
        "confidence": "medium",
        "label": "family-flag mirror",
    },
    {
        "offsets": [146, 147],
        "status": "known",
        "role": (
            "Display (`nibble_hilo`): high nibble = page/row while browsing "
            "(`92=02`) or edit anchor while changing a value (`92=00`); low "
            "nibble = position within the menu page, or value-display position "
            "while editing. Documented in bytes/display.md from "
            "`sysex/prog/menus/` captures"
        ),
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
        if sysex_root is not None and "always 8" in (spec.get("label") or ""):
            # Offset 94 must stay 08 across the factory corpus.
            if verified.get(94) not in (None, 8):
                continue
        if sysex_root is not None and "always 02 00" in (spec.get("label") or ""):
            if verified.get(131) not in (None, 2) or verified.get(132) not in (None, 0):
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
            raw = parse_sysex(path.read_bytes()).raw
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
