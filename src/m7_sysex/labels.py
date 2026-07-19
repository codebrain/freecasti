"""Parse human-readable parameter values from dump filenames."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DumpLabel:
    """Value extracted from a dump filename stem."""

    stem: str
    kind: str  # number | endpoint | bool | enum | unknown
    value: Any
    unit: str | None = None  # canonical lowercase token, e.g. hz, ms, db
    raw_label: str | None = None
    # "off" | "low" | "high" when kind == endpoint
    endpoint: str | None = None
    # Balance-style A.B display (e.g. early/reverb mix): integer pair + path position
    pair: tuple[int, int] | None = None
    balance_side_max: int | None = None


_NUMBER_RE = re.compile(
    r"""
    ^
    (?P<sign>[-+])?
    (?P<number>\d+(?:\.\d+)?)
    \s*
    (?P<unit>[a-zA-Z%]+)?
    $
    """,
    re.VERBOSE,
)

# Balance/mix filenames use a dot because ``/`` is illegal in filenames:
# ``0.20.syx`` means UI/sheet ``0/20``, ``20.6.syx`` means ``20/6``.
_PAIR_RE = re.compile(r"^(\d+)\.(\d+)$")
_SLASH_PAIR_RE = re.compile(r"^(\d+)\s*/\s*(\d+)$")

# Filename units are usually glued on: 120hz.syx, 500ms.syx, -6dB.syx
_UNIT_CANONICAL = {
    "hz": "hz",
    "khz": "khz",
    "ms": "ms",
    "s": "s",
    "sec": "s",
    "secs": "s",
    "db": "db",
    "%": "%",
    "pct": "%",
    "percent": "%",
}

_UNIT_DISPLAY = {
    "hz": "Hz",
    "khz": "kHz",
    "ms": "ms",
    "s": "s",
    "db": "dB",
    "%": "%",
}

_BOOL_MAP = {
    "on": True,
    "true": True,
    "false": False,
    "yes": True,
    "no": False,
    "enable": True,
    "enabled": True,
    "disable": False,
    "disabled": False,
}

# Capture convention: optional OFF, then LOW ... mid numbers ... HIGH/FULL.
# Checked before the bool map so `off.syx` is an endpoint, not a boolean.
_ENDPOINT_MAP = {
    "off": "off",
    "low": "low",
    "min": "low",
    "minimum": "low",
    "small": "low",  # Size: Small ... Large
    "high": "high",
    "max": "high",
    "maximum": "high",
    "full": "high",  # M7 often labels the max as FULL
    "large": "high",  # Size: Small ... Large
}

_ENDPOINT_SORT = {
    "off": 0,
    "low": 1,
    "high": 3,
}


def canonical_unit(unit: str | None) -> str | None:
    """Normalize a unit token from a filename (Hz, hz, kHz -> hz/khz/...)."""
    if not unit:
        return None
    lowered = unit.strip().lower()
    return _UNIT_CANONICAL.get(lowered, lowered)


def display_unit(unit: str | None) -> str | None:
    """Pretty unit for docs/tables (hz -> Hz)."""
    canon = canonical_unit(unit)
    if canon is None:
        return None
    return _UNIT_DISPLAY.get(canon, canon)


def format_value_with_unit(value: Any, unit: str | None) -> str:
    """Format a numeric label with its unit, e.g. 120 + hz -> '120 Hz'."""
    pretty = display_unit(unit)
    if pretty is None:
        return str(value)
    if pretty == "%":
        return f"{value}%"
    return f"{value} {pretty}"


def parse_pair_parts(stem: str) -> tuple[int, int] | None:
    """Parse filename `A.B` as two integers (not a float). `20.6` -> (20, 6)."""
    match = _PAIR_RE.match(stem.strip())
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def parse_balance_pair_token(text: str) -> tuple[int, int] | None:
    """Parse UI/sheet ``A/B`` or filename ``A.B`` into an integer pair."""
    t = (text or "").strip()
    if not t:
        return None
    slash = _SLASH_PAIR_RE.match(t)
    if slash:
        return int(slash.group(1)), int(slash.group(2))
    return parse_pair_parts(t)


def format_balance_pair(a: int, b: int) -> str:
    """Canonical Early/Reverb Mix display (slash form used on the unit/sheet)."""
    return f"{int(a)}/{int(b)}"


def balance_path_position(a: int, b: int, side_max: int) -> int | None:
    """Map balance pair (A, B) on the L-path to position 0..2M, or None."""
    side = int(side_max)
    if b == side and 0 <= a <= side:
        return int(a)
    if a == side and 0 <= b <= side:
        return side + (side - int(b))
    return None


def detect_balance_series(stems: list[str]) -> dict[str, Any] | None:
    """
    Detect M7 balance/mix displays that walk an L-shaped path:

      (0, M) -> (1, M) -> ... -> (M, M) -> (M, M-1) -> ... -> (M, 0)

    Capture filenames join the two integers with a dot (`0.20`, `20.20`,
    `20.6`, `20.0`) because ``/`` is illegal in filenames; the UI and printed
    sheet show the same values with a slash (`0/20`, `20/20`, `20/6`, `20/0`).
    The fitted numeric value is the path position 0 .. 2M (identity with the
    encoded mix index on early-to-reverb).

    Returns None when the folder is ordinary floats (e.g. `0.25`, `0.95`).
    """
    if len(stems) < 3:
        return None

    parsed: list[tuple[str, int, int]] = []
    for stem in stems:
        parts = parse_pair_parts(stem)
        if parts is None:
            return None
        parsed.append((stem, parts[0], parts[1]))

    side_max = max(max(a, b) for _stem, a, b in parsed)
    if side_max < 2:
        return None

    positions: dict[str, dict[str, Any]] = {}
    for stem, a, b in parsed:
        pos = balance_path_position(a, b, side_max)
        if pos is None:
            return None
        positions[stem] = {
            "position": pos,
            "pair": (a, b),
            "display": format_balance_pair(a, b),
        }

    # Require that path positions are not all identical.
    pos_values = {info["position"] for info in positions.values()}
    if len(pos_values) < 2:
        return None

    return {
        "side_max": side_max,
        "position_max": 2 * side_max,
        "positions": positions,
        "notes": (
            f"Balance/mix A/B with side max {side_max}: "
            f"(0/{side_max})...({side_max}/{side_max})...({side_max}/0); "
            f"filenames use A.B because '/' is illegal. "
            f"Path positions 0...{2 * side_max}."
        ),
    }


def balance_label_for(stem: str, balance: dict[str, Any]) -> DumpLabel:
    """Build a numeric DumpLabel from a detected balance series."""
    info = balance["positions"][stem]
    a, b = info["pair"]
    return DumpLabel(
        stem=stem,
        kind="number",
        value=info["position"],
        raw_label=info["display"],
        pair=(a, b),
        balance_side_max=balance["side_max"],
    )


def parse_dump_label(stem: str) -> DumpLabel:
    """
    Interpret a dump filename stem as a parameter value.

    Typical series:
      off.syx, low.syx, 1.syx, ..., high.syx
      80hz.syx, 120hz.syx, ..., full.syx
      0ms.syx, 100ms.syx, 500ms.syx
      0.20.syx ... 20.20.syx ... 20.0.syx  (balance A/B; dot stands in for '/')
    Number dumps usually include units glued to the value: <number><unit>.syx
    """
    text = stem.strip()
    lowered = text.lower()

    if lowered in _ENDPOINT_MAP:
        which = _ENDPOINT_MAP[lowered]
        return DumpLabel(
            stem=stem,
            kind="endpoint",
            value=which,
            raw_label=text,
            endpoint=which,
        )

    if lowered in _BOOL_MAP:
        return DumpLabel(stem=stem, kind="bool", value=_BOOL_MAP[lowered], raw_label=text)

    match = _NUMBER_RE.match(text)
    if match:
        number = float(match.group("number"))
        if match.group("sign") == "-":
            number = -number
        if number.is_integer():
            number = int(number)
        unit = canonical_unit(match.group("unit"))
        return DumpLabel(
            stem=stem,
            kind="number",
            value=number,
            unit=unit,
            raw_label=text,
        )

    return DumpLabel(stem=stem, kind="enum", value=text, raw_label=text)


def load_dumps(folder: Path) -> list[tuple[Path, DumpLabel, bytes]]:
    """Load all .syx / .SYX files in a parameter folder."""
    files = list(folder.glob("*.syx")) + list(folder.glob("*.SYX"))
    # Deduplicate case-insensitive double matches on Windows.
    seen: set[str] = set()
    unique: list[Path] = []
    for path in files:
        key = str(path).lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)

    balance = detect_balance_series([path.stem for path in unique])

    out: list[tuple[Path, DumpLabel, bytes]] = []
    for path in unique:
        if balance and path.stem in balance["positions"]:
            label = balance_label_for(path.stem, balance)
        else:
            label = parse_dump_label(path.stem)
        out.append((path, label, path.read_bytes()))

    out.sort(key=lambda item: _label_sort_key(item[1], item[0].stem))
    return out


def common_unit(labels: list[DumpLabel]) -> str | None:
    """Return the shared unit from numeric dumps, if unanimous."""
    units = {label.unit for label in labels if label.kind == "number" and label.unit}
    if len(units) == 1:
        return next(iter(units))
    return None


def _label_sort_key(label: DumpLabel, stem: str) -> tuple:
    """Sort OFF, LOW, numeric/balance positions, HIGH/FULL, then everything else."""
    if label.kind == "endpoint" and label.endpoint in _ENDPOINT_SORT:
        return (_ENDPOINT_SORT[label.endpoint], 0.0, stem.lower())
    if label.kind == "number":
        return (2, float(label.value), stem.lower())
    if label.kind == "bool":
        return (4, 0 if label.value else 1, stem.lower())
    return (5, 0.0, stem.lower())
