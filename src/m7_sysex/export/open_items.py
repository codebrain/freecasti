"""Open questions surfaced in generated specification docs."""

from __future__ import annotations


def _unseen_values_open_item(*, bytes_link: str) -> str:
    return (
        "**Unseen / undocumented values** — documented or otherwise possible "
        "values not yet witnessed on the wire are tracked per field in the "
        f"**Unseen values** section of each [bytes/]({bytes_link}) page"
    )


def _prog_open_items_with_unseen_link(bytes_link: str) -> list[str]:
    return [_unseen_values_open_item(bytes_link=bytes_link), *PROG_OPEN_ITEMS_CORE]


PROG_OPEN_ITEMS_CORE: list[str] = [
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

# prog/README.md overview links relative to prog/ (``bytes/README.md``).
PROG_OPEN_ITEMS: list[str] = _prog_open_items_with_unseen_link("bytes/README.md")

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
    prog_items = _prog_open_items_with_unseen_link("prog/bytes/README.md")
    lines = [
        f"# {title}",
        "",
        "Auto-generated from `src/m7_sysex/export/open_items.py` on each export.",
        "",
        "## Program dumps",
        "",
    ]
    for i, item in enumerate(prog_items, start=1):
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
