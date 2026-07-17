"""Capture-sampling roles: extremes, adjacent-to-extremes, and sample mids.

Capture convention used in this repo: whenever possible each series includes
the usable extremes, the settings adjacent to those extremes, and a *sparse
sample* of values in between (not every step). That structure is first-class
evidence for encoding fits (edge slopes) and for authoritative min/max ranges.
Mids must never be treated as a complete enumeration of the control.
"""

from __future__ import annotations

from typing import Any

from .encodings import decode_at_offsets
from .labels import DumpLabel, display_unit, format_value_with_unit


CAPTURE_CONVENTION = (
    "Wherever possible, each series includes the usable extremes, the "
    "adjacent-to-extreme settings, and a sparse sample of values in between "
    "(optional discrete off). Mids are samples only - not every intermediate "
    "value. Extremes are treated as authoritative range bounds."
)


def classify_sampling(
    parsed: list[dict[str, Any]],
    best: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Assign sampling roles to dumps and summarize edge steps.

    Roles: off | extreme_low | adjacent_low | mid | adjacent_high | extreme_high
    """
    endpoints = {
        p["label"].endpoint: p
        for p in parsed
        if p["label"].kind == "endpoint" and p["label"].endpoint
    }
    numbered = [p for p in parsed if p["label"].kind == "number"]
    numbered_sorted = sorted(numbered, key=lambda p: float(p["label"].value))

    roles: dict[str, str] = {}
    role_files: dict[str, list[str]] = {
        "off": [],
        "extreme_low": [],
        "adjacent_low": [],
        "mid": [],
        "adjacent_high": [],
        "extreme_high": [],
    }

    if "off" in endpoints:
        name = endpoints["off"]["path"].name
        roles[name] = "off"
        role_files["off"].append(name)

    # Extremes: prefer named low/high, else min/max numbered labels.
    extreme_low_p = endpoints.get("low")
    extreme_high_p = endpoints.get("high")
    if extreme_low_p is None and numbered_sorted:
        extreme_low_p = numbered_sorted[0]
    if extreme_high_p is None and numbered_sorted:
        extreme_high_p = numbered_sorted[-1]

    if extreme_low_p is not None:
        name = extreme_low_p["path"].name
        roles[name] = "extreme_low"
        role_files["extreme_low"].append(name)
    if extreme_high_p is not None:
        name = extreme_high_p["path"].name
        # Avoid double-tagging a single dump as both extremes.
        if name not in roles:
            roles[name] = "extreme_high"
            role_files["extreme_high"].append(name)

    # Adjacents: numbered dumps nearest the interior of each extreme.
    low_anchor = _label_anchor(extreme_low_p)
    high_anchor = _label_anchor(extreme_high_p)

    interior = [
        p
        for p in numbered_sorted
        if p["path"].name not in roles
    ]

    adjacent_low_p = None
    adjacent_high_p = None
    if interior and low_anchor is not None:
        above = [p for p in interior if float(p["label"].value) > low_anchor]
        if above:
            adjacent_low_p = min(above, key=lambda p: float(p["label"].value))
    if interior and high_anchor is not None:
        below = [p for p in interior if float(p["label"].value) < high_anchor]
        if below:
            adjacent_high_p = max(below, key=lambda p: float(p["label"].value))

    # Named low/high extremes: nearest numbered dump is the adjacent.
    # Numeric extremes: second-min / second-max are the adjacents.
    if adjacent_low_p is None and numbered_sorted:
        if extreme_low_p is not None and extreme_low_p["label"].kind == "endpoint":
            candidate = numbered_sorted[0]
        elif len(numbered_sorted) >= 2:
            candidate = numbered_sorted[1]
        else:
            candidate = None
        if candidate is not None and candidate["path"].name not in roles:
            adjacent_low_p = candidate
    if adjacent_high_p is None and numbered_sorted:
        if extreme_high_p is not None and extreme_high_p["label"].kind == "endpoint":
            candidate = numbered_sorted[-1]
        elif len(numbered_sorted) >= 2:
            candidate = numbered_sorted[-2]
        else:
            candidate = None
        if candidate is not None and candidate["path"].name not in roles:
            adjacent_high_p = candidate

    if adjacent_low_p is not None and adjacent_low_p["path"].name not in roles:
        name = adjacent_low_p["path"].name
        roles[name] = "adjacent_low"
        role_files["adjacent_low"].append(name)
    if (
        adjacent_high_p is not None
        and adjacent_high_p["path"].name not in roles
        and adjacent_high_p["path"].name
        != (adjacent_low_p["path"].name if adjacent_low_p else None)
    ):
        name = adjacent_high_p["path"].name
        roles[name] = "adjacent_high"
        role_files["adjacent_high"].append(name)

    for p in parsed:
        name = p["path"].name
        if name in roles:
            continue
        if p["label"].kind == "endpoint":
            continue
        roles[name] = "mid"
        role_files["mid"].append(name)

    edge = _edge_steps(parsed, best, roles)
    coverage = {
        "has_extreme_low": bool(role_files["extreme_low"]),
        "has_extreme_high": bool(role_files["extreme_high"]),
        "has_adjacent_low": bool(role_files["adjacent_low"]),
        "has_adjacent_high": bool(role_files["adjacent_high"]),
        "mid_count": len(role_files["mid"]),
        "mids_are_sparse_sample": True,
        "complete_edge_pair": bool(
            role_files["extreme_low"]
            and role_files["adjacent_low"]
            and role_files["extreme_high"]
            and role_files["adjacent_high"]
        ),
    }

    return {
        "convention": CAPTURE_CONVENTION,
        "roles_by_file": roles,
        "files_by_role": role_files,
        "coverage": coverage,
        "edge_steps": edge,
    }


def _label_anchor(p: dict[str, Any] | None) -> float | None:
    if p is None:
        return None
    label: DumpLabel = p["label"]
    if label.kind == "number":
        return float(label.value)
    # Named low/high: use encoded->label only when caller also passes best;
    # for adjacency we only need ordering among numbered dumps, so None is ok
    # when extreme is an unlabeled endpoint - adjacency then uses second-min/max.
    return None


def _edge_steps(
    parsed: list[dict[str, Any]],
    best: dict[str, Any] | None,
    roles: dict[str, str],
) -> dict[str, Any] | None:
    if not best:
        return None

    by_role: dict[str, dict[str, Any]] = {}
    for p in parsed:
        role = roles.get(p["path"].name)
        if role not in {
            "extreme_low",
            "adjacent_low",
            "adjacent_high",
            "extreme_high",
        }:
            continue
        field = decode_at_offsets(p["raw"], best["offsets"], best["encoding"])
        label = p["label"]
        entry: dict[str, Any] = {
            "file": p["path"].name,
            "encoded": field.value,
            "raw_bytes": [f"{b:02X}" for b in field.raw_bytes],
        }
        if label.kind == "number":
            entry["label"] = label.value
            entry["label_display"] = format_value_with_unit(label.value, label.unit)
        else:
            entry["endpoint"] = label.endpoint
        by_role[role] = entry

    out: dict[str, Any] = {"points": by_role}
    for side, extreme_key, adj_key in (
        ("low", "extreme_low", "adjacent_low"),
        ("high", "extreme_high", "adjacent_high"),
    ):
        extreme = by_role.get(extreme_key)
        adj = by_role.get(adj_key)
        if not extreme or not adj:
            continue
        if "label" not in extreme or "label" not in adj:
            # Named endpoint without numeric label - still report encoded delta.
            d_enc = adj["encoded"] - extreme["encoded"]
            out[f"{side}_edge"] = {
                "delta_encoded": d_enc,
                "extreme_file": extreme["file"],
                "adjacent_file": adj["file"],
            }
            continue
        d_label = float(adj["label"]) - float(extreme["label"])
        d_enc = adj["encoded"] - extreme["encoded"]
        ratio = (d_label / d_enc) if d_enc else None
        out[f"{side}_edge"] = {
            "delta_label": d_label,
            "delta_encoded": d_enc,
            "label_per_encoded": ratio,
            "extreme_file": extreme["file"],
            "adjacent_file": adj["file"],
            "extreme_label": extreme["label"],
            "adjacent_label": adj["label"],
        }

    low = out.get("low_edge") or {}
    high = out.get("high_edge") or {}
    low_r = low.get("label_per_encoded")
    high_r = high.get("label_per_encoded")
    if low_r is not None and high_r is not None:
        agree = abs(low_r - high_r) <= max(1e-6, 1e-4 * max(abs(low_r), abs(high_r), 1.0))
        out["edge_slopes_agree"] = agree
        if agree:
            out["agreed_label_per_encoded"] = (low_r + high_r) / 2.0
            out["note"] = (
                "Low and high extreme->adjacent slopes agree - strong evidence "
                "for a global linear/affine map."
            )
        else:
            out["note"] = (
                "Low and high extreme->adjacent slopes disagree - prefer a "
                "table/index interpretation over a partial closed-form scale."
            )
    return out


def sampling_range_summary(
    sampling: dict[str, Any],
    unit: str | None,
) -> dict[str, Any] | None:
    """Build min/max from classified extremes when numeric labels exist."""
    points = (sampling.get("edge_steps") or {}).get("points") or {}
    low = points.get("extreme_low")
    high = points.get("extreme_high")
    if not low or not high:
        return None
    if "label" not in low or "label" not in high:
        return None

    result: dict[str, Any] = {
        "min": low["label"],
        "max": high["label"],
        "extreme_low_file": low["file"],
        "extreme_high_file": high["file"],
        "range_authority": "capture_extremes",
    }
    pretty = display_unit(unit)
    unit_suffix = f" {pretty}" if pretty else ""
    if pretty == "%":
        unit_suffix = "%"
    result["summary"] = (
        f"Range {result['min']} ... {result['max']}{unit_suffix} "
        f"(capture extremes)"
    )
    return result
