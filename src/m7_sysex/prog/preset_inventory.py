"""Compare captured ``sysex/_presets/`` dumps to official V2 addendum lists."""

from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

# V2 addendum preset tables (M7_V2_Manual_Addendum_Upgrade.pdf)
OFFICIAL_V1_COUNTS: dict[str, int] = {
    "Halls": 32,
    "Plates": 24,
    "Rooms": 26,
    "Chambers": 22,
    "Ambience": 15,
    "Spaces": 19,
}

OFFICIAL_V2_NAMES: dict[str, list[str]] = {
    "Halls 2": [
        "Large Hall",
        "Large & Stage",
        "Medium Hall",
        "Medium & Stage",
        "Small Hall",
        "Small & Stage",
        "Large Church",
        "Small Church",
        "Jazz Hall",
        "West Hall",
        "Concert A",
        "Concert B",
        "Live Hall",
        "Koncert Piano",
        "Berliner Hall",
    ],
    "Plates 2": [
        "Plate A",
        "Small Plate",
        "Snare Plate",
        "Dark Plate",
        "Rich Plate A",
        "Rich Plate B",
        "Thin Plate",
        "Vocal Plate A",
        "Vocal Plate B",
        "Drum Plate",
        "Large Plate",
        "Fat Plate",
        "Alpha Plate",
        "Vocal Shimmer",
    ],
    "Rooms 2": [
        "Music Club",
        "Large Room",
        "Med Room",
        "Small Room",
        "Lg Wood Room",
        "Sm Wood Room",
        "Large Chamber",
        "Small Chamber",
        "Bright Chamber",
        "Tiled Room",
        "Fat Chamber",
        "Studio 1",
        "Studio 2",
        "Studio 3",
        "Studio 4",
        "Guitar Room",
        "Marble Room",
        "Deep Chamber",
        "Dark Chamber",
        "Vocal Chamber",
        "Wide Room",
        "Lush Room",
    ],
    "Spaces 2": [
        "Open Space",
        "Med Space",
        "Small Space",
        "VOX Ambience",
        "Big Bottom",
        "Cathedral",
        "Grand Stage",
        "Lush Church",
        "Grand Church",
        "Concert Wave",
        "Long Vox Space",
        "Dark Warm Room",
        "Live Room",
        "Shimmering Sky",
        "Oak Ballroom",
        "Ice House",
        "Ice Beads",
        "Music Forest",
        "Waving Bloom",
    ],
    "NonLin": ["Nonlin A", "Nonlin B", "Nonlin C", "Nonlin D"],
}

# Addendum name → common on-unit spellings in this corpus.
ADDENDUM_NAME_ALIASES: dict[str, str] = {
    "Medium & Stage": "Med & Stage",
    "VOX Ambience": "Vox Ambience",
}

MARKETING_V1 = 134
MARKETING_V2_TIER = 88
MARKETING_TOTAL = 222
V2_BANK_CAPACITY = 22


def _normalize_addendum_name(name: str) -> str:
    return ADDENDUM_NAME_ALIASES.get(name, name)


def _addendum_v1_total() -> int:
    return sum(OFFICIAL_V1_COUNTS.values())


def _addendum_v2_named_total() -> int:
    return sum(
        len(names)
        for bank, names in OFFICIAL_V2_NAMES.items()
        if bank != "NonLin"
    )


def _addendum_grand_total() -> int:
    return _addendum_v1_total() + sum(len(v) for v in OFFICIAL_V2_NAMES.values())


def _format_slot_range(slots: list[int]) -> str:
    """Compact slot list: contiguous → ``0–21``; gaps → ``0–13, 15``."""
    if not slots:
        return ""
    ordered = sorted(set(slots))
    runs: list[tuple[int, int]] = []
    start = prev = ordered[0]
    for slot in ordered[1:]:
        if slot == prev + 1:
            prev = slot
            continue
        runs.append((start, prev))
        start = prev = slot
    runs.append((start, prev))
    parts = [f"{a}–{b}" if a != b else str(a) for a, b in runs]
    return ", ".join(parts)


def analyze_preset_inventory(names: dict[str, Any]) -> dict[str, Any]:
    """Build inventory report from ``analyze_names_folder`` result."""
    dumps = names.get("dumps") or []
    by_bank: dict[str, list[dict[str, Any]]] = {}
    for dump in dumps:
        by_bank.setdefault(dump["bank"], []).append(dump)

    bank_rows: list[dict[str, Any]] = []
    total = 0
    for bank in sorted(by_bank):
        rows = sorted(by_bank[bank], key=lambda d: d["program_slot"])
        slots = [d["program_slot"] for d in rows]
        smin, smax = min(slots), max(slots)
        bank_rows.append(
            {
                "bank": bank,
                "count": len(rows),
                "slot_min": smin,
                "slot_max": smax,
                "slot_range": _format_slot_range(slots),
                "capacity_used": smax + 1,
            }
        )
        total += len(rows)

    v1_have = sum(len(by_bank.get(b, [])) for b in OFFICIAL_V1_COUNTS)
    v2_have = sum(
        len(by_bank.get(b, []))
        for b in OFFICIAL_V2_NAMES
        if b != "NonLin"
    )
    nonlin_have = len(by_bank.get("NonLin", []))

    v1_gaps: list[dict[str, Any]] = []
    for bank, expected in OFFICIAL_V1_COUNTS.items():
        have = len(by_bank.get(bank, []))
        if have != expected:
            v1_gaps.append(
                {
                    "bank": bank,
                    "have": have,
                    "expected": expected,
                    "delta": have - expected,
                }
            )

    name_gaps: list[dict[str, Any]] = []
    for bank, expected_names in OFFICIAL_V2_NAMES.items():
        have_names = {d["name_field"] for d in by_bank.get(bank, [])}
        expected_matched: set[str] = set()
        for exp in expected_names:
            expected_matched.add(exp)
            expected_matched.add(_normalize_addendum_name(exp))
        missing = [
            exp
            for exp in expected_names
            if exp not in have_names
            and _normalize_addendum_name(exp) not in have_names
        ]
        extra = sorted(have_names - expected_matched)
        if missing or extra:
            name_gaps.append(
                {
                    "bank": bank,
                    "missing": missing,
                    "extra": extra,
                }
            )

    capture_gaps: list[dict[str, str]] = []
    rooms = {d["preset"] for d in by_bank.get("Rooms", [])}
    if "Long Wood Room" not in rooms:
        capture_gaps.append(
            {"bank": "Rooms", "preset": "Long Wood Room", "file": "Rooms.Long Wood Room.syx"}
        )
    halls2 = {d["name_field"] for d in by_bank.get("Halls 2", [])}
    if "Berliner Hall" not in halls2:
        capture_gaps.append(
            {
                "bank": "Halls 2",
                "preset": "Berliner Hall",
                "file": "Halls 2.Berliner Hall.syx",
            }
        )

    v2_capacity: list[dict[str, Any]] = []
    for bank in ("Halls 2", "Plates 2", "Rooms 2", "Spaces 2"):
        rows = sorted(by_bank.get(bank, []), key=lambda d: d["program_slot"])
        max_slot = max((d["program_slot"] for d in rows), default=-1)
        cap = max_slot + 1 if rows else 0
        trailing = V2_BANK_CAPACITY - cap if cap <= V2_BANK_CAPACITY else 0
        v2_capacity.append(
            {
                "bank": bank,
                "named": len(rows),
                "capacity": V2_BANK_CAPACITY,
                "slot_max": max_slot,
                "trailing_empty": trailing,
            }
        )

    addendum_total = _addendum_grand_total()
    return {
        "kind": "preset_inventory",
        "dump_count": total,
        "banks": bank_rows,
        "totals": {
            "v1_have": v1_have,
            "v1_addendum": _addendum_v1_total(),
            "v2_have": v2_have,
            "v2_addendum": _addendum_v2_named_total(),
            "nonlin_have": nonlin_have,
            "nonlin_addendum": len(OFFICIAL_V2_NAMES["NonLin"]),
            "addendum_grand": addendum_total,
            "marketing_v1": MARKETING_V1,
            "marketing_v2_tier": MARKETING_V2_TIER,
            "marketing_total": MARKETING_TOTAL,
        },
        "v1_count_gaps": v1_gaps,
        "v2_name_gaps": name_gaps,
        "capture_gaps": capture_gaps,
        "v2_slot_capacity": v2_capacity,
        "complete_vs_addendum": total >= addendum_total and not capture_gaps,
    }


def inventory_summary_line(result: dict[str, Any]) -> str:
    """One-line status for export console output."""
    t = result["totals"]
    have = result["dump_count"]
    exp = t["addendum_grand"]
    gaps = result.get("capture_gaps") or []
    if gaps:
        missing = ", ".join(g["file"] for g in gaps[:3])
        extra = ""
        if len(gaps) > 3:
            extra = f" (+{len(gaps) - 3} more)"
        return (
            f"[preset inventory] {have}/{exp} vs V2 addendum — "
            f"missing capture: {missing}{extra}"
        )
    if have == exp:
        return f"[preset inventory] {have}/{exp} — complete vs V2 addendum"
    return (
        f"[preset inventory] {have}/{exp} vs V2 addendum "
        f"(delta {have - exp:+d})"
    )


def render_preset_inventory_markdown(
    result: dict[str, Any],
    *,
    today: str | None = None,
    nav: str = "",
) -> str:
    """Markdown page for specification/prog/preset-inventory.md."""
    today = today or date.today().isoformat()
    t = result["totals"]
    lines = [
        nav.rstrip(),
        "# Preset inventory",
        "",
        f"_Generated {today}. Compares `sysex/prog/presets/` captures to the "
        "[V2 addendum](https://www.bricasti.com/images/M7_V2_Manual_Addendum_Upgrade.pdf) "
        "factory lists and common marketing totals (222 = 134 V1 + 88 V2-tier positions)._",
        "",
        "## Corpus counts",
        "",
        "| Bank | Dumps | Slot range |",
        "|------|------:|------------|",
    ]
    from ..export import bank_md_link

    for row in result["banks"]:
        slot_range = row.get("slot_range") or (
            f"{row['slot_min']}–{row['slot_max']}"
        )
        lines.append(
            f"| {bank_md_link(row['bank'])} | {row['count']} | {slot_range} |"
        )
    lines.extend(
        [
            f"| **Total** | **{result['dump_count']}** | |",
            "",
            "## vs V2 addendum",
            "",
            f"| Group | Captured | Addendum |",
            f"|-------|--------:|---------:|",
            f"| V1 banks (incl. Ambience) | {t['v1_have']} | {t['v1_addendum']} |",
            f"| V2 `* 2` banks | {t['v2_have']} | {t['v2_addendum']} |",
            f"| {bank_md_link('NonLin')} | {t['nonlin_have']} | {t['nonlin_addendum']} |",
            f"| **Grand total** | **{result['dump_count']}** | **{t['addendum_grand']}** |",
            "",
        ]
    )

    gaps = result.get("capture_gaps") or []
    if gaps:
        lines.extend(
            [
                "## Missing captures",
                "",
                "Suggested filenames for `sysex/prog/presets/`:",
                "",
            ]
        )
        for g in gaps:
            lines.append(f"- `{g['file']}`")
        lines.append("")

    if result.get("v2_name_gaps"):
        lines.extend(["## Name diffs (addendum vs unit spelling)", ""])
        for block in result["v2_name_gaps"]:
            lines.append(f"### {block['bank']}")
            if block.get("missing"):
                lines.append("")
                lines.append("Addendum names not matched (after alias map):")
                for name in block["missing"]:
                    alias = ADDENDUM_NAME_ALIASES.get(name)
                    hint = f" (unit may spell `{alias}`)" if alias else ""
                    lines.append(f"- {name}{hint}")
            if block.get("extra"):
                lines.append("")
                lines.append("Captured but not in addendum PDF:")
                for name in block["extra"]:
                    lines.append(f"- {name}")
            lines.append("")

    if result.get("v1_count_gaps"):
        lines.extend(["## V1 count gaps", ""])
        for row in result["v1_count_gaps"]:
            lines.append(
                f"- **{row['bank']}**: have {row['have']}, addendum {row['expected']} "
                f"({row['delta']:+d})"
            )
        lines.append("")

    lines.extend(
        [
            "## Marketing totals (third-party)",
            "",
            f"Published marketing totals often cite **{t['marketing_total']}** factory presets "
            f"as **{t['marketing_v1']}** V1 + **{t['marketing_v2_tier']}** V2-tier program "
            "positions. The addendum names **70** programs across the four `* 2` banks; "
            f"**{t['marketing_v2_tier'] - t['v2_addendum']}** extra positions are unused "
            "slots in the 22×4 MIDI bank grid (see below).",
            "",
            f"| | Captured | Marketing |",
            f"|--|--------:|----------:|",
            f"| V1 | {t['v1_have']} | {t['marketing_v1']} |",
            f"| V2 tier (named) | {t['v2_have']} | {t['marketing_v2_tier']} positions |",
            "",
            "## V2 bank slot capacity",
            "",
            "Rooms 2 uses slots 0–21 → **22** programs per `* 2` bank.",
            "",
            "| Bank | Named | Capacity | Slots used | Trailing empty |",
            "|------|------:|---------:|-----------|---------------:|",
        ]
    )
    for row in result["v2_slot_capacity"]:
        lines.append(
            f"| {bank_md_link(row['bank'])} | {row['named']} | {row['capacity']} | "
            f"0–{row['slot_max']} | {row['trailing_empty']} |"
        )
    lines.extend(
        [
            "",
            "## preset_sheet.json",
            "",
            "Classic-bank PDF sheet only (pre-V2). All `* 2` and NonLin dumps, plus "
            "newer V1 additions, have no sheet row.",
            "",
            f"_Last exported: {today}_",
            "",
        ]
    )
    return "\n".join(lines)


def write_preset_inventory(
    names: dict[str, Any],
    out_dir: Path,
    *,
    repo_root: Path | None = None,
) -> tuple[dict[str, Any], Path]:
    """Analyze inventory and write ``preset-inventory.md``."""
    result = analyze_preset_inventory(names)
    sheet_note = _sheet_note(repo_root, dump_count=result["dump_count"])
    if sheet_note:
        result["preset_sheet"] = sheet_note
    from ..export import _page_nav

    text = render_preset_inventory_markdown(
        result,
        nav=_page_nav(depth=0, current="Preset inventory"),
    )
    if sheet_note:
        text = text.replace(
            "newer V1 additions, have no sheet row.",
            "newer V1 additions, have no sheet row.\n\n"
            f"- Sheet rows: **{sheet_note['row_count']}** "
            f"({sheet_note['by_bank']})\n"
            f"- Dumps without sheet row: **{sheet_note['dumps_without_sheet']}**",
        )
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "preset-inventory.md"
    if path.exists():
        path.unlink()
    path.write_text(text + "\n", encoding="utf-8")
    return result, path


def _sheet_note(
    repo_root: Path | None,
    *,
    dump_count: int,
) -> dict[str, Any] | None:
    if repo_root is None:
        return None
    json_path = Path(repo_root) / "docs/reference/preset_sheet.json"
    if not json_path.is_file():
        return None
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    rows = payload["presets"] if isinstance(payload, dict) else payload
    by_bank = dict(sorted(Counter(r["bank"] for r in rows).items()))
    return {
        "row_count": len(rows),
        "by_bank": by_bank,
        "dumps_without_sheet": dump_count - len(rows),
    }
