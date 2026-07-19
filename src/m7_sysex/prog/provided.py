"""Hardware-provided UI labels for encoding-map densify.

Committed lists live in ``docs/reference/provided_labels.json``. Each entry is
an ordered walk of display values as seen on the unit; list index is the
encoded step. Export tags matching rows ``provided``.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from ..labels import balance_path_position, parse_balance_pair_token

DEFAULT_PROVIDED_JSON = Path("docs/reference/provided_labels.json")

# Balance path side max when the parameter uses A/B display.
_BALANCE_SIDE_MAX = {
    "early to reverb mix": 20,
}

# Discrete UI endpoints → numeric densify labels (display still comes from
# capture specials like ``off.syx`` when present, or the provided token).
_ENDPOINT_LABELS = {
    ("delay level", "off"): -21.0,
    ("density", "low"): 0.0,
    ("density", "high"): 10.0,
    ("diffusion", "low"): 0.0,
    ("diffusion", "high"): 10.0,
    ("size", "small"): 0.0,
    ("size", "large"): 30.0,
    # Full is past the last Hz step; numeric is a placeholder (display = full).
    ("early rolloff", "full"): 22000.0,
    ("rolloff", "full"): 22000.0,
}


def default_provided_json_path(sysex_root: Path | None = None) -> Path:
    """Resolve ``docs/reference/provided_labels.json`` next to the repo root."""
    if sysex_root is not None:
        return Path(sysex_root).resolve().parent / DEFAULT_PROVIDED_JSON
    return Path(DEFAULT_PROVIDED_JSON)


def load_provided_file(path: Path) -> dict[str, Any]:
    """Load the provided-labels JSON document."""
    path = Path(path)
    if not path.is_file():
        return {"version": 1, "parameters": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"provided labels root must be an object: {path}")
    params = data.get("parameters")
    if params is None:
        data["parameters"] = {}
    elif not isinstance(params, dict):
        raise ValueError(f"provided labels 'parameters' must be an object: {path}")
    return data


def parse_provided_token(token: str, *, parameter: str) -> float:
    """Parse one hardware display token into the numeric densify label."""
    text = str(token).strip()
    if not text:
        raise ValueError(f"empty provided label for {parameter!r}")

    endpoint_key = (parameter, text.lower())
    if endpoint_key in _ENDPOINT_LABELS:
        return float(_ENDPOINT_LABELS[endpoint_key])

    # Balance A/B (or filename A.B) only for known mix parameters. Dot-decimals
    # like ``0.2`` / ``1.05`` must not be treated as balance pairs.
    if parameter in _BALANCE_SIDE_MAX:
        pair = parse_balance_pair_token(text)
        if pair is not None:
            side = _BALANCE_SIDE_MAX[parameter]
            pos = balance_path_position(pair[0], pair[1], side)
            if pos is None:
                raise ValueError(
                    f"provided label {text!r} is not on the {side}/{side} "
                    f"balance path for {parameter!r}"
                )
            return float(pos)

    # Plain number (optional unit suffix stripped for densify numeric label).
    # Longer unit spellings first so ``mSec`` is not trimmed as ``ms``.
    cleaned = text.replace(",", "")
    lower = cleaned.lower()
    for suffix in (
        " msec",
        "msec",
        " ms",
        "ms",
        " hz",
        "hz",
        " khz",
        "khz",
        " sec",
        "sec",
        " s",
        "s",
        " db",
        "db",
        "×",
        "x",
        "%",
    ):
        if lower.endswith(suffix):
            cleaned = cleaned[: -len(suffix)].strip()
            break
    try:
        return float(cleaned)
    except ValueError as exc:
        raise ValueError(
            f"cannot parse provided label {text!r} for {parameter!r}"
        ) from exc


def provided_mapping_for(
    parameter: str,
    *,
    path: Path | None = None,
    sysex_root: Path | None = None,
) -> dict[int, float]:
    """Return ``{encoded: numeric_label}`` for one parameter, or ``{}``."""
    entries = _all_provided_mappings(path=path, sysex_root=sysex_root)
    return dict(entries.get(parameter.lower(), {}))


def provided_display_mapping_for(
    parameter: str,
    *,
    path: Path | None = None,
    sysex_root: Path | None = None,
) -> dict[int, str]:
    """Return ``{encoded: hardware display token}`` for one parameter, or ``{}``."""
    key = parameter.strip().lower()
    resolved = Path(path) if path is not None else default_provided_json_path(sysex_root)
    data = load_provided_file(resolved)
    entry = (data.get("parameters") or {}).get(key)
    if entry is None:
        return {}
    if isinstance(entry, list):
        values = entry
    elif isinstance(entry, dict):
        values = entry.get("values")
    else:
        return {}
    if not isinstance(values, list) or not values:
        return {}
    return {enc: str(token) for enc, token in enumerate(values)}


@lru_cache(maxsize=4)
def _cached_load(path_key: str) -> dict[str, dict[int, float]]:
    data = load_provided_file(Path(path_key))
    out: dict[str, dict[int, float]] = {}
    for name, entry in (data.get("parameters") or {}).items():
        key = str(name).strip().lower()
        if isinstance(entry, list):
            values = entry
        elif isinstance(entry, dict):
            values = entry.get("values")
        else:
            raise ValueError(
                f"provided entry for {name!r} must be a list or object with values"
            )
        if not isinstance(values, list) or not values:
            raise ValueError(f"provided values missing/empty for {name!r}")
        mapping: dict[int, float] = {}
        for enc, token in enumerate(values):
            label = parse_provided_token(str(token), parameter=key)
            # Ordered walks are contiguous from encoded 0; balance paths should
            # match index == path position.
            if key in _BALANCE_SIDE_MAX and int(label) != enc:
                raise ValueError(
                    f"provided {name!r}[{enc}]={token!r} maps to position "
                    f"{int(label)}, expected {enc}"
                )
            mapping[enc] = label
        out[key] = mapping
    return out


def _all_provided_mappings(
    *,
    path: Path | None = None,
    sysex_root: Path | None = None,
) -> dict[str, dict[int, float]]:
    resolved = Path(path) if path is not None else default_provided_json_path(sysex_root)
    return _cached_load(str(resolved.resolve()) if resolved.is_file() else str(resolved))


def has_provided_labels(
    parameter: str,
    *,
    sysex_root: Path | None = None,
) -> bool:
    """True when ``docs/reference/provided_labels.json`` has a walk for *parameter*."""
    return bool(provided_mapping_for(parameter, sysex_root=sysex_root))


def clear_provided_cache() -> None:
    """Drop cached provided-label maps (tests / after rewriting the JSON)."""
    _cached_load.cache_clear()
