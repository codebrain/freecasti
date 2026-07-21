"""Corpus analysis for program-dump display field (offsets 146–147).

Browse mode (``92 = 02``): stable menu-row codes.
Edit mode (``92 = 00``): display moves with the edited value inside
parameter-specific bands — not a fixed per-parameter "edit anchor".
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..encodings import decode_at_offsets
from ..frame import parse_sysex
from ..paths import prog_menus_root, prog_parameters_root
from .catalog import PROGRAM_PARAMETERS
from .display import DISPLAY_HI, DISPLAY_LO, nibble_hilo
from .menus import IDLE_STEM, hardware_menu_order

# Shared role text for byte-map / corpus-layout / README region lines.
DISPLAY_ROLE = (
    "Display (`nibble_hilo`): front-panel UI focus code (not a sound "
    "parameter). Browse (`92=02`): menu-row highlight "
    "(`menu_index+28` for indices 1–17; reverb time → 46). Edit "
    "(`92=00`): value-focus code in a parameter-specific band that "
    "advances as the shown value changes (not a fixed edit anchor). "
    "From `sysex/prog/menus/` + parameter series"
)

BROWSE_IDLE = 28
BROWSE_REVERB_TIME = 46  # menu index 0 special-case


def browse_expected(menu_index: int) -> int:
    """Expected browse-mode ``nibble_hilo`` for a hardware menu index."""
    if menu_index == 0:
        return BROWSE_REVERB_TIME
    return int(menu_index) + BROWSE_IDLE


def _load_best_encoding(folder: Path) -> tuple[list[int], str] | None:
    analysis_path = folder / "analysis.json"
    if not analysis_path.is_file():
        return None
    try:
        data = json.loads(analysis_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    best = data.get("best_encoding") or {}
    offsets = best.get("offsets")
    encoding = best.get("encoding")
    if not offsets or not encoding:
        return None
    return [int(o) for o in offsets], str(encoding)


def _edit_rows_for_folder(
    folder: Path,
    *,
    menu_index: int,
    offsets: list[int] | None,
    encoding: str | None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    paths: list[Path] = []
    for path in list(folder.glob("*.syx")) + list(folder.glob("*.SYX")):
        key = str(path).lower()
        if key in seen:
            continue
        seen.add(key)
        paths.append(path)
    for path in sorted(paths, key=lambda p: p.stem.casefold()):
        try:
            raw = parse_sysex(path.read_bytes()).raw
        except ValueError:
            continue
        if raw[92] != 0:
            continue
        if nibble_hilo(raw[98], raw[99]) != menu_index:
            continue
        disp = nibble_hilo(raw[DISPLAY_HI], raw[DISPLAY_LO])
        enc: int | None = None
        if offsets and encoding:
            enc = int(decode_at_offsets(raw, offsets, encoding).value)
        rows.append(
            {
                "stem": path.stem,
                "encoded": enc,
                "display": disp,
                "hi": int(raw[DISPLAY_HI]),
                "lo": int(raw[DISPLAY_LO]),
            }
        )
    return rows


def _summarize_edit_series(
    name: str,
    menu_index: int,
    rows: list[dict[str, Any]],
    *,
    offsets: list[int] | None,
    encoding: str | None,
) -> dict[str, Any]:
    if not rows:
        return {
            "parameter": name,
            "menu_index": menu_index,
            "dump_count": 0,
            "offsets": offsets,
            "encoding": encoding,
        }

    sorted_by_enc = sorted(
        rows,
        key=lambda r: (
            r["encoded"] is None,
            r["encoded"] if r["encoded"] is not None else 0,
            r["display"],
        ),
    )
    displays = [int(r["display"]) for r in sorted_by_enc]
    encs = [r["encoded"] for r in sorted_by_enc if r["encoded"] is not None]
    mono = all(displays[i] <= displays[i + 1] for i in range(len(displays) - 1))
    const_disp_minus_enc = False
    if encs and len(encs) == len(displays):
        diffs = {d - e for d, e in zip(displays, encs)}
        const_disp_minus_enc = len(diffs) == 1

    his = sorted({int(r["hi"]) for r in rows})
    los = sorted({int(r["lo"]) for r in rows})
    return {
        "parameter": name,
        "menu_index": menu_index,
        "dump_count": len(rows),
        "unique_display": len(set(displays)),
        "display_min": min(displays),
        "display_max": max(displays),
        "hi_nibbles": his,
        "lo_nibbles": los,
        "monotonic_nondecreasing": mono,
        "const_display_minus_encoded": const_disp_minus_enc,
        "offsets": offsets,
        "encoding": encoding,
        "sample": {
            "stem": sorted_by_enc[len(sorted_by_enc) // 2]["stem"],
            "hi": sorted_by_enc[len(sorted_by_enc) // 2]["hi"],
            "lo": sorted_by_enc[len(sorted_by_enc) // 2]["lo"],
            "display": sorted_by_enc[len(sorted_by_enc) // 2]["display"],
            "encoded": sorted_by_enc[len(sorted_by_enc) // 2]["encoded"],
        },
    }


def _browse_report(menus_root: Path) -> dict[str, Any]:
    menu_order = hardware_menu_order()
    index_by = {name: i for i, name in enumerate(menu_order)}
    rows: list[dict[str, Any]] = []
    idle_ok = False
    mismatches: list[dict[str, Any]] = []

    for path in sorted(menus_root.glob("*.syx")):
        raw = parse_sysex(path.read_bytes()).raw
        stem = path.stem
        disp = nibble_hilo(raw[DISPLAY_HI], raw[DISPLAY_LO])
        mode = int(raw[92])
        menu_enc = nibble_hilo(raw[98], raw[99])
        if stem.casefold() == IDLE_STEM:
            idle_ok = mode == 0 and disp == BROWSE_IDLE
            rows.append(
                {
                    "stem": stem,
                    "mode": mode,
                    "menu_index": menu_enc,
                    "display": disp,
                    "expected": BROWSE_IDLE,
                    "ok": idle_ok,
                }
            )
            if not idle_ok:
                mismatches.append(rows[-1])
            continue
        idx = index_by.get(stem)
        if idx is None:
            continue
        expected = browse_expected(idx)
        ok = mode == 2 and disp == expected and menu_enc == idx
        row = {
            "stem": stem,
            "mode": mode,
            "menu_index": menu_enc,
            "display": disp,
            "expected": expected,
            "ok": ok,
        }
        rows.append(row)
        if not ok:
            mismatches.append(row)

    return {
        "idle_display": BROWSE_IDLE,
        "rule": (
            "indices 1–17: display = menu_index + 28; "
            "index 0 (reverb time): display = 46; "
            "idle: display = 28"
        ),
        "all_match": len(mismatches) == 0,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "captures": rows,
    }


def analyze_display_corpus(sysex_root: Path) -> dict[str, Any]:
    """Scan menus + parameter series for display-field behavior."""
    sysex_root = Path(sysex_root)
    menus_root = prog_menus_root(sysex_root)
    parameters_root = prog_parameters_root(sysex_root)
    menu_order = hardware_menu_order()

    browse = _browse_report(menus_root)

    edit_series: list[dict[str, Any]] = []
    code_to_params: dict[int, set[str]] = {}
    for i, name in enumerate(menu_order):
        folder = parameters_root / name
        best = _load_best_encoding(folder) if folder.is_dir() else None
        offsets = best[0] if best else None
        encoding = best[1] if best else None
        rows = (
            _edit_rows_for_folder(
                folder, menu_index=i, offsets=offsets, encoding=encoding
            )
            if folder.is_dir()
            else []
        )
        for r in rows:
            code_to_params.setdefault(int(r["display"]), set()).add(name)
        edit_series.append(
            _summarize_edit_series(
                name, i, rows, offsets=offsets, encoding=encoding
            )
        )

    collisions = [
        {"display": code, "parameters": sorted(params)}
        for code, params in sorted(code_to_params.items())
        if len(params) > 1
    ]

    bands = [
        {
            "parameter": s["parameter"],
            "menu_index": s["menu_index"],
            "min": s.get("display_min"),
            "max": s.get("display_max"),
            "unique": s.get("unique_display"),
            "dumps": s.get("dump_count"),
            "monotonic": s.get("monotonic_nondecreasing"),
            "const_disp_minus_enc": s.get("const_display_minus_encoded"),
            "hi_nibbles": s.get("hi_nibbles"),
        }
        for s in edit_series
        if s.get("dump_count")
    ]
    bands_by_min = sorted(bands, key=lambda b: (b["min"] is None, b["min"] or 0))

    hypotheses = [
        {
            "id": "browse_menu_row",
            "verdict": "accepted",
            "confidence": "high",
            "summary": (
                "Browse (`92=02`): display is a stable menu-row highlight "
                "code (idle 28; indices 1–17 → index+28; reverb time → 46)."
            ),
        },
        {
            "id": "fixed_edit_anchor",
            "verdict": "rejected",
            "confidence": "high",
            "summary": (
                "Edit mode is not a fixed per-parameter anchor: within each "
                "parameter series display moves as the value changes "
                f"({sum(1 for s in edit_series if (s.get('unique_display') or 0) > 1)}"
                " of 18 series have multiple display codes)."
            ),
        },
        {
            "id": "edit_value_focus_band",
            "verdict": "working",
            "confidence": "medium",
            "summary": (
                "Edit (`92=00`): each parameter occupies a band of display "
                "codes that advances (usually non-decreasing) with the wire "
                "encoding, but is not encoding+constant and not 1:1 with large "
                "encoding steps. Discriminate overlapping codes via 98–99."
            ),
        },
        {
            "id": "lcd_ddram_address",
            "verdict": "rejected",
            "confidence": "high",
            "summary": (
                "HD44780-style DDRAM addresses (≤ ~0x67) cannot explain "
                "observed edit codes up to 215."
            ),
        },
        {
            "id": "second_parameter_word",
            "verdict": "rejected",
            "confidence": "high",
            "summary": (
                "Not a second copy of the parameter word "
                "(const display−encoded is false for every series)."
            ),
        },
    ]

    return {
        "kind": "prog_display_corpus",
        "offsets": [DISPLAY_HI, DISPLAY_LO],
        "encoding": "nibble_hilo",
        "role": DISPLAY_ROLE,
        "browse": browse,
        "edit_series": edit_series,
        "edit_bands_by_min": bands_by_min,
        "edit_code_collisions": collisions,
        "hypotheses": hypotheses,
        "open": [
            (
                "Without dense every-step sweeps for a few parameters, edit "
                "display cannot be proven to equal discrete UI step index vs "
                "digit/cursor cell vs firmware string-pool ID."
            ),
        ],
        "catalog_count": len(PROGRAM_PARAMETERS),
    }


def attach_display_corpus(
    menus_analysis: dict[str, Any],
    sysex_root: Path,
) -> dict[str, Any]:
    """Add ``display_corpus`` onto a menus analysis dict (in place)."""
    corpus = analyze_display_corpus(sysex_root)
    menus_analysis["display_corpus"] = corpus

    # Enrich per-parameter edit with observed band for exporters / JSON.
    by_param = menus_analysis.get("prog_ui", {}).get("by_parameter") or {}
    for series in corpus["edit_series"]:
        name = series["parameter"]
        row = by_param.get(name)
        if not row:
            continue
        if series.get("dump_count"):
            row["edit_band"] = {
                "min": series["display_min"],
                "max": series["display_max"],
                "unique": series["unique_display"],
                "dumps": series["dump_count"],
                "monotonic": series["monotonic_nondecreasing"],
                "hi_nibbles": series["hi_nibbles"],
                "sample": series.get("sample"),
            }
    return menus_analysis
