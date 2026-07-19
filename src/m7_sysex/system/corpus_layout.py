"""Corpus-derived layout hints for system-dump payload bytes."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from ..frame import parse_system_sysex
from ..paths import system_root


def _is_system_dump(path: Path, sysex_root: Path) -> bool:
    try:
        rel = path.resolve().relative_to(sysex_root.resolve())
    except ValueError:
        return False
    parts = rel.parts
    if not parts or parts[0] != "system":
        return False
    return "_system" not in parts


CORPUS_LAYOUT_CLAIMS: tuple[dict[str, Any], ...] = (
    {
        "offsets": list(range(8, 17)),
        "status": "known",
        "role": "Fixed header/prefix block (constant in this corpus)",
        "encoding": None,
        "confidence": "medium",
        "label": "fixed prefix",
    },
    {
        "offsets": [18],
        "status": "known",
        "role": "Reserved (always 0 in this corpus)",
        "encoding": None,
        "confidence": "medium",
        "label": "reserved (always 0)",
    },
    {
        "offsets": [19, 20],
        "status": "known",
        "role": "Fixed field (always `02 00` in this corpus)",
        "encoding": None,
        "confidence": "medium",
        "label": "fixed (always 02 00)",
    },
    {
        "offsets": [24],
        "status": "known",
        "role": "Reserved / padding (constant in this corpus)",
        "encoding": None,
        "confidence": "medium",
        "label": "reserved padding",
    },
    {
        "offsets": list(range(26, 72)),
        "status": "known",
        "role": "Reserved / padding (constant in this corpus)",
        "encoding": None,
        "confidence": "medium",
        "label": "reserved padding",
    },
)


def verify_corpus_constants(sysex_root: Path) -> dict[int, int | None]:
    """Return per-offset constant value across all system .syx dumps, or None if varied."""
    root = system_root(sysex_root)
    if not root.is_dir():
        return {}
    values: dict[int, set[int]] = {}
    for path in root.rglob("*.syx"):
        if not _is_system_dump(path, sysex_root):
            continue
        try:
            raw = parse_system_sysex(path.read_bytes()).raw
        except ValueError:
            continue
        for off in range(len(raw)):
            values.setdefault(off, set()).add(raw[off])
    return {off: next(iter(s)) if len(s) == 1 else None for off, s in values.items()}


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
        if sysex_root is not None and spec.get("label", "").startswith("reserved"):
            if any(verified.get(o) not in (None, 0) for o in offsets):
                continue
        claim(
            offsets,
            status=spec["status"],
            role=spec["role"],
            parameter="_corpus",
            confidence=spec.get("confidence") or "medium",
            encoding=spec.get("encoding"),
            example=example,
            example_source=example_source,
        )
        applied.append({**spec, "offsets": offsets})
    return applied


def overview_label_for_offsets(offsets: list[int]) -> str | None:
    """Short overview label if these offsets match a corpus claim."""
    key = tuple(offsets)
    for spec in CORPUS_LAYOUT_CLAIMS:
        if tuple(spec["offsets"]) == key:
            return spec.get("label")
        if len(offsets) == 1 and offsets[0] in spec["offsets"]:
            return spec.get("label")
    return None
