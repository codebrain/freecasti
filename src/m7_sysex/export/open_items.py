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
        "bank **11** (`sysex/prog/edit/`); **Favorites receive** (MIDI-notes "
        "bank **119**) also unconfirmed — favorites *sends* carry the source "
        "identity instead (`sysex/prog/favorites/`)"
    ),
    "Semantics of PROG header bytes `70 08 01 00`",
    "Halls 2 subtype EDIT outlier",
    (
        "Closed-form mapping for table parameters (see medium-confidence rows "
        "in the parameter index)"
    ),
    (
        "**Favorites follow-ups** — one more commit-rule confirmation "
        "(hold-PROG from the favorites screen with a pending edit) and "
        "power-cycle persistence of an auto-committed favorite "
        "(`sysex/prog/favorites/README.md`)"
    ),
]

# Resolved questions kept for context (not counted as open).
PROG_RESOLVED_ITEMS: list[str] = [
    (
        "Register basis blob **24–87** is fully decoded — complete 6-bit name "
        "charset, per-register store counter, all 18 parameters incl. the "
        "delay block at bits **197–211**; snapshots stored register values; "
        "offsets **93/95** track the *loaded* register basis (see "
        "`sysex/prog/edit/registers/README.md`)"
    ),
    (
        "**Favorites**-based PROG dumps are decoded — sends carry the source "
        "program identity at **88–91** (never bank 119); offset **94** is the "
        "favorite-source slot (`(slot-1)*2`, `08` = none), offset **92** is a "
        "panel-mode flag (`08` = favorites screen); favorite saves write the "
        "register basis blob with store counter 0 and auto-commit edits on "
        "hold-PROG from the favorites screen (see "
        "`sysex/prog/favorites/README.md`)"
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
    lines.extend(["", "## Resolved", ""])
    for item in PROG_RESOLVED_ITEMS:
        lines.append(f"- {item}")
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
