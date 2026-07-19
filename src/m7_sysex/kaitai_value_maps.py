"""Attach encoding-table enums to Kaitai / machine byte-spec fields."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .encoding_map_rows import full_encoding_rows, sysex_root_from_series_folder


def attach_parameter_value_maps(
    fields: list[dict[str, Any]],
    results: list[dict[str, Any]] | None,
    *,
    sysex_root: Path | None = None,
) -> None:
    """Mutate ``fields`` in place, adding ``value_map`` for locked-down enums."""
    if not results:
        return
    root = sysex_root
    if root is None:
        root = sysex_root_from_series_folder(Path(results[0]["folder"]))
    by_param = {r["parameter"]: r for r in results if r.get("parameter")}

    for field in fields:
        param = field.get("parameter")
        if param and param in by_param:
            analysis = by_param[param]
            best = analysis.get("best_encoding") or {}
            if not best.get("encoding"):
                continue
            rows = full_encoding_rows(analysis, best, sysex_root=root)
            if rows:
                field["value_map"] = build_value_map(field["id"], rows, analysis)
            continue

        if field.get("id") == "bank_index":
            field["value_map"] = build_bank_index_value_map()
        elif field.get("id") == "register_bank":
            field["value_map"] = build_register_bank_value_map()
        elif field.get("id") == "register":
            field["value_map"] = build_register_value_map()


def attach_display_value_map(
    fields: list[dict[str, Any]],
    menus_analysis: dict[str, Any] | None,
) -> None:
    """Attach menu-name enum for offsets 146–147 when menu captures exist."""
    if not menus_analysis:
        return
    prog_ui = menus_analysis.get("prog_ui")
    if not prog_ui:
        return
    from .prog.display import build_display_value_map

    value_map = build_display_value_map(prog_ui)
    for field in fields:
        if field.get("id") != "display":
            continue
        field["value_map"] = value_map
        field["kind"] = "table"
        field["series_root"] = "sysex/prog/menus"
        field.pop("parameter", None)
        break


def build_value_map(
    field_id: str,
    rows: list[dict[str, Any]],
    result: dict[str, Any],
) -> dict[str, Any]:
    """Turn densified encoding rows into a Kaitai enum definition."""
    from .encoding_map_rows import format_row_display_label

    enum_id = f"{field_id}_values"
    used_names: set[str] = set()
    entries: list[dict[str, Any]] = []
    for row in rows:
        enc = int(row["encoded"])
        label_text = format_row_display_label(result, row)
        name = _slug_enum_member(label_text, enc, used_names)
        entries.append(
            {
                "encoded": enc,
                "name": name,
                "label": label_text,
            }
        )
    return {"enum_id": enum_id, "entries": entries}


def build_bank_index_value_map() -> dict[str, Any]:
    from .prog.names import HINT_BANK_INDEX, SPECIAL_BANK_LABELS

    enum_id = "bank_index_values"
    used_names: set[str] = set()
    entries: list[dict[str, Any]] = []
    for bank, idx in sorted(HINT_BANK_INDEX.items(), key=lambda kv: kv[1]):
        name = _slug_enum_member(bank, idx, used_names)
        entries.append({"encoded": idx, "name": name, "label": bank})
    for idx, label in sorted(SPECIAL_BANK_LABELS.items()):
        name = _slug_enum_member(label, idx, used_names)
        entries.append({"encoded": idx, "name": name, "label": label})
    return {"enum_id": enum_id, "entries": entries}


def build_register_bank_value_map() -> dict[str, Any]:
    """Manual register Banks B0–B4 (offsets 93 = 0–4)."""
    enum_id = "register_bank_values"
    used_names: set[str] = set()
    entries: list[dict[str, Any]] = []
    for idx in range(5):
        label = f"B{idx}"
        name = _slug_enum_member(label, idx, used_names)
        entries.append({"encoded": idx, "name": name, "label": label})
    return {"enum_id": enum_id, "entries": entries}


def build_register_value_map() -> dict[str, Any]:
    """Manual Registers 0–9 within a register bank (offset 95)."""
    enum_id = "register_values"
    used_names: set[str] = set()
    entries: list[dict[str, Any]] = []
    for idx in range(10):
        label = str(idx)
        name = _slug_enum_member(f"reg_{idx}", idx, used_names)
        entries.append({"encoded": idx, "name": name, "label": label})
    return {"enum_id": enum_id, "entries": entries}


def _slug_enum_member(label: str, encoded: int, used: set[str]) -> str:
    text = str(label).strip().lower()
    text = (
        text.replace("/", "_")
        .replace(".", "_")
        .replace("%", "pct")
        .replace("+", "plus")
    )
    text = re.sub(r"[^a-z0-9_]+", "_", text)
    text = text.strip("_")
    if text.startswith("-"):
        text = "neg_" + text.lstrip("-")
    if not text:
        text = f"enc_{encoded}"
    if text[0].isdigit():
        text = f"v_{text}"
    candidate = text
    n = 2
    while candidate in used:
        candidate = f"{text}_e{encoded}" if n == 2 else f"{text}_e{encoded}_{n}"
        n += 1
    used.add(candidate)
    return candidate
