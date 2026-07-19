"""Analyze PROG menu-navigation captures (``sysex/prog/menus/``)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..frame import parse_sysex
from ..paths import prog_menus_root, prog_parameters_root
from .catalog import PROGRAM_PARAMETERS

UI_OFFSETS = (92, 98, 99, 146, 147)
IDLE_STEM = "no menu"

from .display import nibble_hilo as _nibble_hilo


def hardware_menu_order() -> list[str]:
    """Front-panel menu order (``folder_hint`` per catalog entry)."""
    return [entry["folder_hint"] for entry in PROGRAM_PARAMETERS]


def _ui_bytes(raw: bytes) -> dict[str, int]:
    return {str(off): int(raw[off]) for off in UI_OFFSETS}


def _stem_to_parameter(stem: str) -> str | None:
    key = stem.strip().casefold()
    if key == IDLE_STEM:
        return None
    for entry in PROGRAM_PARAMETERS:
        if entry["folder_hint"].casefold() == key:
            return entry["folder_hint"]
    return stem


def _edit_bytes_from_series(
    parameters_root: Path,
    folder_hint: str,
    menu_index: int,
) -> dict[str, int] | None:
    """Derive typical edit-mode UI bytes from a parameter capture series."""
    folder = parameters_root / folder_hint
    if not folder.is_dir():
        return None

    candidates: list[tuple[bytes, str]] = []
    for path in sorted(folder.glob("*.syx")):
        try:
            raw = parse_sysex(path.read_bytes()).raw
        except ValueError:
            continue
        if raw[92] != 0:
            continue
        if _nibble_hilo(raw[98], raw[99]) != menu_index:
            continue
        candidates.append((raw, path.stem))

    if not candidates:
        return None

    # Prefer a mid-range labeled dump over extremes when available.
    prefer = ("low", "1", "2", "3", "small", "off")
    chosen = candidates[0][0]
    for pref in prefer:
        for raw, stem in candidates:
            if stem.casefold() == pref:
                chosen = raw
                break
        else:
            continue
        break

    return {
        "92": 0,
        "146": int(chosen[146]),
        "147": int(chosen[147]),
    }


def analyze_menus_folder(menus_root: Path, sysex_root: Path) -> dict[str, Any]:
    """Build menu-series analysis and ``prog_ui`` runtime payload."""
    menus_root = Path(menus_root)
    if not menus_root.is_dir():
        raise ValueError(f"menu folder not found: {menus_root}")

    menu_order = hardware_menu_order()
    index_by_param = {name: i for i, name in enumerate(menu_order)}

    captures: list[dict[str, Any]] = []
    idle: dict[str, int] | None = None

    for path in sorted(menus_root.glob("*.syx")):
        raw = parse_sysex(path.read_bytes()).raw
        stem = path.stem
        param = _stem_to_parameter(stem)
        ui = _ui_bytes(raw)
        entry: dict[str, Any] = {
            "file": path.name,
            "stem": stem,
            "parameter": param,
            "menu_index": index_by_param.get(param) if param else None,
            "ui": ui,
            "menu_index_encoded": _nibble_hilo(raw[98], raw[99]),
        }
        captures.append(entry)
        if stem.casefold() == IDLE_STEM:
            idle = ui

    if idle is None:
        raise ValueError(f"missing idle capture: {IDLE_STEM}.syx in {menus_root}")

    parameters_root = prog_parameters_root(sysex_root)
    by_parameter: dict[str, Any] = {}
    for i, folder_hint in enumerate(menu_order):
        browse: dict[str, int] | None = None
        for cap in captures:
            if cap.get("parameter") == folder_hint:
                browse = cap["ui"]
                break
        edit = _edit_bytes_from_series(parameters_root, folder_hint, i)
        by_parameter[folder_hint] = {
            "index": i,
            "browse": browse,
            "edit": edit,
        }

    prog_ui = {
        "idle": idle,
        "menu_order": menu_order,
        "by_parameter": by_parameter,
    }

    return {
        "kind": "prog_menu_navigation",
        "folder": str(menus_root.resolve()),
        "capture_count": len(captures),
        "idle_stem": IDLE_STEM,
        "menu_order": menu_order,
        "captures": captures,
        "prog_ui": prog_ui,
    }


def write_menus_analysis(analysis: dict[str, Any], menus_root: Path) -> list[Path]:
    menus_root = Path(menus_root)
    menus_root.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    analysis_path = menus_root / "analysis.json"
    analysis_path.write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    written.append(analysis_path)

    prog_ui_path = menus_root / "prog_ui_state.json"
    prog_ui_path.write_text(
        json.dumps(analysis["prog_ui"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    written.append(prog_ui_path)

    return written
