"""Per-byte "Unseen values" section renderers.

These sections live inside each field page under ``bytes/`` (sound parameters
and the display cursor) rather than in a standalone report. They list values
that are **documented** (encoding map / manual / layout) or otherwise
**possible** for the field but never witnessed on the wire, collapsed into
ranges when there are many.
"""

from __future__ import annotations

from typing import Any

from ..prog.unseen_values import (
    DISPLAY_NIBBLE_HILO_SPACE,
    format_int_ranges,
    unseen_nibbles_at,
)

# List individual documented-but-unseen rows up to this many; beyond it,
# collapse to encoded-value ranges and defer labels to the encoding map.
MAX_INLINE_UNSEEN_ROWS = 16


def _wire_nibble_lines(gaps: dict[str, Any], observed: dict[int, list[int]]) -> list[str]:
    offsets = list(gaps.get("offsets") or [])
    if not offsets or not observed:
        return []
    encoding = gaps.get("encoding") or ""
    parts: list[str] = []
    for i, off in enumerate(offsets):
        if encoding == "nibble_hilo" and len(offsets) == 2:
            role = "high" if i == 0 else "low"
            tag = f"offset {off} ({role})"
        else:
            tag = f"offset {off}"
        unseen = unseen_nibbles_at(observed, off)
        parts.append(f"{tag}: {' '.join(f'`{n}`' for n in unseen) if unseen else 'none'}")
    return [
        f"- **Wire nibbles never observed (`0`–`F`):** {'; '.join(parts)}"
    ]


def render_parameter_unseen_section(
    gaps: dict[str, Any] | None,
    *,
    observed: dict[int, list[int]] | None = None,
) -> list[str]:
    """Markdown lines for a sound-parameter ``## Unseen values`` section."""
    if not gaps:
        return []

    observed = observed or {}
    lo = gaps.get("known_encoded_min")
    hi = gaps.get("known_encoded_max")
    steps = gaps.get("known_encoded_count", 0)

    lines: list[str] = [
        "## Unseen values",
        "",
        "Documented in the spec (encoding map / manual) but not yet witnessed "
        "in a committed dump. \"Possible\" spans every encoded step in this "
        "field's range; missing steps are listed as ranges when there are many.",
        "",
    ]
    if lo is not None and hi is not None:
        lines.append(
            f"- **Encoding range:** encoded {lo}\u2013{hi} "
            f"({steps} step{'s' if steps != 1 else ''} documented)."
        )

    manual = gaps.get("manual_range_uncaptured")
    if manual:
        notes = "; ".join(manual.get("notes") or [])
        lines.append(f"- **Manual range not fully captured:** {notes}.")

    unseen = gaps.get("documented_unseen") or []
    if not unseen:
        lines.append(
            "- **Never captured on the wire:** none — every documented step "
            "has a `dump` witness."
        )
    elif len(unseen) <= MAX_INLINE_UNSEEN_ROWS:
        lines.append(f"- **Never captured on the wire ({len(unseen)}):**")
        for row in unseen:
            sources = ", ".join(row.get("sources") or [])
            suffix = f" ({sources})" if sources else ""
            lines.append(
                f"  - encoded **{row['encoded']}** \u2192 {row['label']}{suffix}"
            )
    else:
        ranges = format_int_ranges([int(r["encoded"]) for r in unseen])
        lines.append(
            f"- **Never captured on the wire ({len(unseen)}):** encoded "
            f"{ranges} — see the [encoding map](#encoding-map) above for each "
            "label."
        )

    enc_gaps = gaps.get("encoded_gaps") or []
    if enc_gaps:
        lines.append(
            f"- **Documented gaps (no row at all, {len(enc_gaps)}):** encoded "
            f"{format_int_ranges(enc_gaps)}."
        )
    else:
        lines.append(
            "- **Documented gaps (no row at all):** none between documented "
            "min/max."
        )

    lines.extend(_wire_nibble_lines(gaps, observed))
    lines.append("")
    return lines


def render_display_unseen_section(display_gaps: dict[str, Any]) -> list[str]:
    """Markdown lines for the display ``## Unseen values`` section (ranges)."""
    witnessed = display_gaps.get("witnessed_count", 0)
    unseen = display_gaps.get("unseen_nibble_hilo") or []
    ranges = display_gaps.get("unseen_nibble_hilo_ranges") or format_int_ranges(
        unseen
    )
    idle_note = ""
    if unseen and unseen[0] == 0:
        # Contiguous unseen block starting at 0 → the gap before idle.
        end = 0
        for value in unseen:
            if value == end:
                end += 1
            else:
                break
        idle_note = (
            f" The first witnessed position is idle (28), so `0\u2013{end - 1}` "
            "are never observed before it."
        )

    return [
        "## Unseen values",
        "",
        "The cursor packs two nibbles, so "
        f"**{DISPLAY_NIBBLE_HILO_SPACE}** `nibble_hilo` values are possible "
        f"(0\u2013{DISPLAY_NIBBLE_HILO_SPACE - 1}). Only **{witnessed}** are "
        "witnessed in `sysex/prog/menus/` captures; the rest are unseen and "
        f"shown as ranges below.{idle_note}",
        "",
        f"- **Witnessed positions:** {witnessed} of {DISPLAY_NIBBLE_HILO_SPACE}",
        f"- **Unseen positions ({len(unseen)}):** {ranges or 'none'}",
        "",
    ]
