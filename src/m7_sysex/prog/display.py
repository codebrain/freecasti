"""Program-dump display field at offsets 146–147 (`nibble_hilo`)."""

from __future__ import annotations

from collections.abc import Callable

DISPLAY_OFFSETS = (146, 147)
DISPLAY_HI, DISPLAY_LO = DISPLAY_OFFSETS


def nibble_hilo(hi: int, lo: int) -> int:
    return (int(hi) << 4) | int(lo)


def _hex_nibble(changing: dict[str, str], offset: int) -> int | None:
    raw = changing.get(str(offset))
    if raw is None or raw == "??":
        return None
    return int(raw, 16)


def has_full_display(offsets: list[int]) -> bool:
    s = set(int(o) for o in offsets)
    return DISPLAY_HI in s and DISPLAY_LO in s


def describe_secondary_offsets(offsets: list[int]) -> str:
    """Human-readable secondary-offset phrase for parameter docs."""
    parts: list[str] = []
    remaining = sorted(set(int(o) for o in offsets))

    if has_full_display(remaining):
        parts.append("146–147 (`nibble_hilo` display)")
        remaining = [o for o in remaining if o not in DISPLAY_OFFSETS]
    elif DISPLAY_LO in remaining:
        parts.append("147 (display low nibble)")
        remaining.remove(DISPLAY_LO)
    elif DISPLAY_HI in remaining:
        parts.append("146 (display high nibble)")
        remaining.remove(DISPLAY_HI)

    if 98 in remaining and 99 in remaining:
        parts.append("98–99 (`nibble_hilo` menu index)")
        remaining = [o for o in remaining if o not in (98, 99)]
    for off in remaining:
        if off == 92:
            parts.append("92 (menu browse flag)")
        else:
            parts.append(str(off))
    return ", ".join(parts) if parts else "-"


def secondary_dump_columns(
    secondary: list[int],
) -> list[tuple[str, Callable[[dict[str, str]], str]]]:
    """Extra dump-table columns for secondary movers (after primary fields)."""
    cols: list[tuple[str, Callable[[dict[str, str]], str]]] = []
    remaining = sorted(set(int(o) for o in secondary))

    if has_full_display(remaining):
        cols.append(
            (
                "Display 146–147",
                lambda c: (
                    f"`{c.get(str(DISPLAY_HI), '??')} "
                    f"{c.get(str(DISPLAY_LO), '??')}`"
                ),
            )
        )
        cols.append(
            (
                "display `nibble_hilo`",
                lambda c: (
                    str(nibble_hilo(_hex_nibble(c, DISPLAY_HI) or 0, _hex_nibble(c, DISPLAY_LO) or 0))
                    if _hex_nibble(c, DISPLAY_HI) is not None
                    and _hex_nibble(c, DISPLAY_LO) is not None
                    else "-"
                ),
            )
        )
        remaining = [o for o in remaining if o not in DISPLAY_OFFSETS]
    elif DISPLAY_LO in remaining:
        cols.append(
            (
                "Display lo 147",
                lambda c: f"`{c.get(str(DISPLAY_LO), '??')}`",
            )
        )
        remaining.remove(DISPLAY_LO)
    elif DISPLAY_HI in remaining:
        cols.append(
            (
                "Display hi 146",
                lambda c: f"`{c.get(str(DISPLAY_HI), '??')}`",
            )
        )
        remaining.remove(DISPLAY_HI)

    for off in remaining:
        cols.append((f"Offset {off}", lambda c, o=off: f"`{c.get(str(o), '??')}`"))
    return cols


def build_display_value_map(prog_ui: dict) -> dict:
    """Kaitai enum entries for known idle / browse / edit display positions."""
    from ..kaitai_value_maps import _slug_enum_member

    menu_order = list(prog_ui["menu_order"])
    by_param = prog_ui["by_parameter"]
    idle = prog_ui["idle"]

    labels_by_enc: dict[int, list[str]] = {}

    def add(enc: int, label: str) -> None:
        bucket = labels_by_enc.setdefault(int(enc), [])
        if label not in bucket:
            bucket.append(label)

    add(nibble_hilo(idle["146"], idle["147"]), "idle (no menu)")

    for i, name in enumerate(menu_order):
        row = by_param.get(name) or {}
        browse = row.get("browse")
        if browse:
            add(
                nibble_hilo(browse["146"], browse["147"]),
                f"browse: {name} ({i})",
            )
        edit = row.get("edit")
        if edit:
            add(
                nibble_hilo(edit["146"], edit["147"]),
                f"edit: {name} ({i})",
            )

    used_names: set[str] = set()
    entries: list[dict] = []
    for enc in sorted(labels_by_enc):
        label = " / ".join(labels_by_enc[enc])
        entries.append(
            {
                "encoded": enc,
                "name": _slug_enum_member(label, enc, used_names),
                "label": label,
            }
        )
    return {"enum_id": "display_values", "entries": entries}
