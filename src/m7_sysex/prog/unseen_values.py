"""Unseen / undocumented value gaps for PROG program dumps."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..frame import iter_sysex_messages, parse_sysex
from ..paths import prog_edit_root
from ..types import is_prog_corpus_dump
from .display import nibble_hilo

NIBBLE_PAYLOAD_START = 88
NIBBLE_PAYLOAD_END = 151  # inclusive
ALL_NIBBLES = list(range(16))
DISPLAY_NIBBLE_HILO_SPACE = 256  # two nibbles → 0..255


def format_int_ranges(values: list[int]) -> str:
    """Collapse a sorted int list into ``"0–27, 47–54, 210"`` style ranges."""
    ordered = sorted(set(int(v) for v in values))
    if not ordered:
        return ""
    runs: list[str] = []
    start = prev = ordered[0]
    for value in ordered[1:]:
        if value == prev + 1:
            prev = value
            continue
        runs.append(str(start) if start == prev else f"{start}\u2013{prev}")
        start = prev = value
    runs.append(str(start) if start == prev else f"{start}\u2013{prev}")
    return ", ".join(runs)


def unseen_nibbles_at(observed: dict[int, list[int]], offset: int) -> list[str]:
    """Hex nibbles ``0``–``F`` never observed at ``offset`` across the corpus."""
    seen = set(observed.get(offset, []))
    return [f"{v:X}" for v in ALL_NIBBLES if v not in seen]


def observed_values_by_offset(sysex_root: Path) -> dict[int, list[int]]:
    """Return sorted unique byte values seen at each offset across PROG dumps.

    Includes the factory/parameter corpus plus ``sysex/prog/edit/registers/``
    (multi-message files supported) so register-bank / register / display
    witnesses from hold-EDIT captures are visible.
    """
    root = Path(sysex_root)
    if not root.is_dir():
        return {}
    values: dict[int, set[int]] = {}
    paths = {
        p.resolve()
        for p in root.rglob("*.syx")
        if is_prog_corpus_dump(p, root)
    }
    registers_root = prog_edit_root(root) / "registers"
    if registers_root.is_dir():
        paths.update(p.resolve() for p in registers_root.rglob("*.syx"))
        paths.update(p.resolve() for p in registers_root.rglob("*.SYX"))
    for path in sorted(paths):
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
    return {off: sorted(s) for off, s in sorted(values.items())}


def _offset_role(byte_map: dict[str, Any] | None, offset: int) -> dict[str, Any]:
    if not byte_map:
        return {"offset": offset, "status": "unknown", "role": "?"}
    cells = byte_map.get("bytes") or []
    if offset < 0 or offset >= len(cells):
        return {"offset": offset, "status": "unknown", "role": "?"}
    cell = cells[offset]
    return {
        "offset": offset,
        "status": cell.get("status", "unknown"),
        "role": cell.get("role", "?"),
        "parameters": list(cell.get("parameters") or []),
        "encoding": cell.get("encoding"),
    }


def parameter_unseen_gaps(
    result: dict[str, Any],
    *,
    sysex_root: Path,
) -> dict[str, Any] | None:
    """Documented-but-unseen encoded steps, gaps, and manual-range shortfall."""
    from ..encoding_map_rows import full_encoding_rows, format_row_display_label

    best = result.get("best_encoding")
    if not best or not best.get("offsets"):
        return None

    rows = full_encoding_rows(result, best, sysex_root=sysex_root)
    if not rows:
        return None

    documented_unseen: list[dict[str, Any]] = []
    known_encs: set[int] = set()
    for row in rows:
        enc = int(row["encoded"])
        known_encs.add(enc)
        sources = list(row.get("sources") or [])
        if not sources and row.get("source"):
            sources = [str(row["source"])]
        if "dump" not in sources:
            documented_unseen.append(
                {
                    "encoded": enc,
                    "label": format_row_display_label(result, row),
                    "sources": sources,
                }
            )

    lo, hi = min(known_encs), max(known_encs)
    encoded_gaps = [enc for enc in range(lo, hi + 1) if enc not in known_encs]

    manual_range_uncaptured: dict[str, Any] | None = None
    official = result.get("official") or {}
    value_range = result.get("value_range") or {}
    if official.get("matched"):
        exp = official.get("expected") or {}
        manual_min = exp.get("manual_min")
        manual_max = exp.get("manual_max")
        captured_min = value_range.get("min")
        captured_max = value_range.get("max")
        notes: list[str] = []
        if (
            manual_min is not None
            and captured_min is not None
            and float(manual_min) < float(captured_min)
        ):
            notes.append(
                f"manual floor {manual_min} below captured min {captured_min}"
            )
        if (
            manual_max is not None
            and captured_max is not None
            and float(manual_max) > float(captured_max)
        ):
            notes.append(
                f"manual ceiling {manual_max} above captured max {captured_max}"
            )
        if notes:
            manual_range_uncaptured = {
                "manual_min": manual_min,
                "manual_max": manual_max,
                "captured_min": captured_min,
                "captured_max": captured_max,
                "notes": notes,
            }

    return {
        "offsets": list(best["offsets"]),
        "encoding": best.get("encoding"),
        "documented_unseen": documented_unseen,
        "documented_unseen_count": len(documented_unseen),
        "encoded_gaps": encoded_gaps,
        "encoded_gap_count": len(encoded_gaps),
        "known_encoded_count": len(known_encs),
        "known_encoded_min": lo,
        "known_encoded_max": hi,
        "manual_range_uncaptured": manual_range_uncaptured,
    }


def display_unseen(menus_analysis: dict[str, Any] | None) -> dict[str, Any]:
    """Witnessed vs. never-observed display cursor (`nibble_hilo`) positions."""
    if not menus_analysis:
        return {
            "witnessed": [],
            "witnessed_nibble_hilo": [],
            "unseen_nibble_hilo": list(range(DISPLAY_NIBBLE_HILO_SPACE)),
            "unseen_nibble_hilo_ranges": format_int_ranges(
                list(range(DISPLAY_NIBBLE_HILO_SPACE))
            ),
            "missing_edit_witness": [],
            "unwitnessed_nibble_hilo_count": DISPLAY_NIBBLE_HILO_SPACE,
        }

    prog_ui = menus_analysis.get("prog_ui") or {}
    idle = prog_ui.get("idle") or {}
    menu_order = list(prog_ui.get("menu_order") or [])
    by_param = prog_ui.get("by_parameter") or {}

    witnessed: list[dict[str, Any]] = []
    witnessed_enc: set[int] = set()
    missing_edit: list[str] = []

    if idle:
        enc = nibble_hilo(idle.get("146", 0), idle.get("147", 0))
        witnessed_enc.add(enc)
        witnessed.append(
            {
                "label": "idle (no menu)",
                "mode": "idle",
                "nibble_hilo": enc,
                "146": idle.get("146"),
                "147": idle.get("147"),
            }
        )

    for name in menu_order:
        row = by_param.get(name) or {}
        idx = row.get("index")
        browse = row.get("browse")
        if browse:
            enc = nibble_hilo(browse.get("146", 0), browse.get("147", 0))
            witnessed_enc.add(enc)
            witnessed.append(
                {
                    "label": f"browse: {name} ({idx})",
                    "mode": "browse",
                    "nibble_hilo": enc,
                    "146": browse.get("146"),
                    "147": browse.get("147"),
                }
            )
        edit = row.get("edit")
        if edit:
            enc = nibble_hilo(edit.get("146", 0), edit.get("147", 0))
            witnessed_enc.add(enc)
            witnessed.append(
                {
                    "label": f"edit: {name} ({idx})",
                    "mode": "edit",
                    "nibble_hilo": enc,
                    "146": edit.get("146"),
                    "147": edit.get("147"),
                }
            )
        else:
            missing_edit.append(name)

    unseen_enc = [
        v for v in range(DISPLAY_NIBBLE_HILO_SPACE) if v not in witnessed_enc
    ]
    return {
        "witnessed": witnessed,
        "witnessed_nibble_hilo": sorted(witnessed_enc),
        "witnessed_count": len(witnessed_enc),
        "unseen_nibble_hilo": unseen_enc,
        "unseen_nibble_hilo_ranges": format_int_ranges(unseen_enc),
        "missing_edit_witness": missing_edit,
        "unwitnessed_nibble_hilo_count": DISPLAY_NIBBLE_HILO_SPACE
        - len(witnessed_enc),
    }


def build_unseen_values(
    results: list[dict[str, Any]],
    byte_map: dict[str, Any] | None,
    menus_analysis: dict[str, Any] | None,
    sysex_root: Path,
) -> dict[str, Any]:
    """Build unseen / undocumented gap report for the PROG 157-byte layout."""
    sysex_root = Path(sysex_root)
    message_length = int(
        (byte_map or {}).get("message_length")
        or (results[0]["message_length"] if results else 157)
    )
    observed = observed_values_by_offset(sysex_root)

    parameters: dict[str, Any] = {}
    total_documented_unseen = 0
    total_encoded_gaps = 0
    params_with_manual_gap = 0

    for result in sorted(results, key=lambda r: r["parameter"]):
        gaps = parameter_unseen_gaps(result, sysex_root=sysex_root)
        if gaps is None:
            continue
        parameters[result["parameter"]] = gaps
        total_documented_unseen += gaps["documented_unseen_count"]
        total_encoded_gaps += gaps["encoded_gap_count"]
        if gaps.get("manual_range_uncaptured"):
            params_with_manual_gap += 1

    offsets: list[dict[str, Any]] = []
    total_unseen_nibbles = 0
    offsets_with_nibble_gaps = 0

    for off in range(message_length):
        meta = _offset_role(byte_map, off)
        seen = observed.get(off, [])
        entry: dict[str, Any] = {
            **meta,
            "observed_values": [f"{v:02X}" for v in seen],
            "observed_count": len(seen),
        }
        if NIBBLE_PAYLOAD_START <= off <= NIBBLE_PAYLOAD_END:
            unseen = [v for v in ALL_NIBBLES if v not in seen]
            entry["unseen_nibble_values"] = [f"{v:X}" for v in unseen]
            entry["unseen_nibble_count"] = len(unseen)
            if unseen:
                offsets_with_nibble_gaps += 1
                total_unseen_nibbles += len(unseen)
        offsets.append(entry)

    display = display_unseen(menus_analysis)

    summary = {
        "message_length": message_length,
        "parameter_count": len(parameters),
        "total_documented_unseen_rows": total_documented_unseen,
        "total_encoded_gaps": total_encoded_gaps,
        "parameters_with_manual_range_gap": params_with_manual_gap,
        "offsets_with_unseen_nibbles": offsets_with_nibble_gaps,
        "total_unseen_nibble_slots": total_unseen_nibbles,
        "display_witnessed_positions": display.get("witnessed_count", 0),
        "display_unwitnessed_nibble_hilo": display.get(
            "unwitnessed_nibble_hilo_count", 256
        ),
        "display_missing_edit_witness": len(display.get("missing_edit_witness") or []),
    }

    return {
        "kind": "prog_unseen_values",
        "message_length": message_length,
        "summary": summary,
        "parameters": parameters,
        "offsets": offsets,
        "display": display,
    }
