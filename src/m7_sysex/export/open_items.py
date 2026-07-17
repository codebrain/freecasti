"""Open questions surfaced in generated specification docs."""

from __future__ import annotations

PROG_OPEN_ITEMS: list[str] = [
    (
        "**EDIT receive** path (MIDI-notes bank **118**) — hold-EDIT *sends* use "
        "bank **11** (`sysex/prog/edit/`)"
    ),
    "Semantics of PROG header bytes `70 08 01 00` and fixed field 93–94 (`00 08`)",
    (
        "**Offset 25 coupling** — `midi bank` (primary @ 25) and display-level "
        "captures also move offset 25 (secondary)"
    ),
    (
        "Closed-form mapping for table parameters (see medium-confidence rows "
        "in the parameter index)"
    ),
    (
        "Optional: register/favorite-based PROG dumps; rarely used SYSTEM knobs "
        "(e.g. register lock) not yet in dedicated series"
    ),
]

SYSTEM_OPEN_ITEMS: list[str] = [
    (
        "**Offset 25 coupling** — `midi bank` primary @ 25; display-level series "
        "also moves offset 25 (secondary)"
    ),
    "Rarely used SYSTEM knobs (e.g. register lock) not yet in dedicated series",
]


def render_open_items_markdown(
    *,
    title: str = "Open questions",
) -> str:
    """Standalone open-questions page covering PROG and SYSTEM items."""
    lines = [
        f"# {title}",
        "",
        "Auto-generated from `src/m7_sysex/export/open_items.py` on each export.",
        "",
        "## Program dumps",
        "",
    ]
    for i, item in enumerate(PROG_OPEN_ITEMS, start=1):
        lines.append(f"{i}. {item}")
    lines.extend(["", "## System dumps", ""])
    for i, item in enumerate(SYSTEM_OPEN_ITEMS, start=1):
        lines.append(f"{i}. {item}")
    lines.append("")
    return "\n".join(lines)


def render_open_items_section(
    items: list[str],
    *,
    title: str = "Open questions",
    footer: str = "",
) -> str:
    """Numbered open-questions block for overview pages."""
    lines = [f"## {title}", ""]
    for i, item in enumerate(items, start=1):
        lines.append(f"{i}. {item}")
    lines.append("")
    if footer:
        lines.append(footer.rstrip())
        lines.append("")
    return "\n".join(lines)
