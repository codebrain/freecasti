"""Build full encoded→label tables for parameter docs and Kaitai enums."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def sysex_root_from_series_folder(folder: Path) -> Path:
    """Return ``sysex/`` for a parameter-series folder path."""
    parts = folder.parts
    if "prog" in parts:
        idx = parts.index("prog")
        return Path(*parts[:idx])
    if "system" in parts:
        idx = parts.index("system")
        return Path(*parts[:idx])
    return folder.parent


def is_table_encoding(best: dict[str, Any]) -> bool:
    notes = best.get("notes") or ""
    if "table/index" in notes:
        return True
    if best.get("exact") and best.get("scale") is not None:
        return False
    return bool(best.get("mapping"))


def series_numeric_mapping(
    result: dict[str, Any], best: dict[str, Any]
) -> dict[int, float]:
    """Encoded → numeric label from capture dumps / best_encoding mapping."""
    mapping: dict[int, float] = {}
    for row in best.get("mapping") or []:
        if "encoded" in row and "label" in row:
            try:
                mapping[int(row["encoded"])] = float(row["label"])
            except (TypeError, ValueError):
                continue
    for dump in result.get("dumps") or []:
        label = dump.get("label") or {}
        decoded = dump.get("decoded_parameter") or {}
        if "encoded_value" not in decoded:
            continue
        enc = int(decoded["encoded_value"])
        if label.get("kind") == "number":
            try:
                mapping[enc] = float(label["value"])
            except (TypeError, ValueError):
                continue
        elif label.get("kind") == "endpoint" and decoded.get("inferred_label") is not None:
            if label.get("endpoint") != "off":
                try:
                    mapping[enc] = float(decoded["inferred_label"])
                except (TypeError, ValueError):
                    continue
    return mapping


def synthetic_affine_provided_mapping(
    series: dict[int, float],
    special: dict[int, str],
    scale: float,
    offset: float,
) -> dict[int, float]:
    """Fill every encoded step on a confirmed affine scale (e.g. 0.5 dB steps)."""
    if not series:
        return {}
    lo = min(int(enc) for enc in series)
    hi = max(int(enc) for enc in series)
    for enc, token in special.items():
        tok = str(token).lower()
        if tok in {"full", "high", "max"}:
            hi = max(hi, int(enc))
        elif tok == "off":
            lo = min(lo, int(enc))
    return {enc: enc * scale + offset for enc in range(lo, hi + 1)}


def series_special_labels(result: dict[str, Any]) -> dict[int, str]:
    """Encoded → display token for discrete endpoints and enum-named dumps."""
    special: dict[int, str] = {}
    param = str(result.get("parameter") or "").lower()
    endpoint_ui = {
        "density": {"low", "high"},
        "diffusion": {"low", "high"},
        "size": {"low", "high", "small", "large"},
    }.get(param, set())
    for dump in result.get("dumps") or []:
        label = dump.get("label") or {}
        decoded = dump.get("decoded_parameter") or {}
        if "encoded_value" not in decoded:
            continue
        kind = label.get("kind")
        enc = int(decoded["encoded_value"])
        if kind == "enum":
            token = str(label.get("stem") or label.get("value") or "enum")
            special[enc] = token.lower()
            continue
        if kind != "endpoint":
            continue
        endpoint = label.get("endpoint")
        stem = str(label.get("stem") or endpoint or "endpoint").lower()
        if endpoint == "off":
            special[enc] = "off"
        elif endpoint in endpoint_ui or stem in endpoint_ui:
            if param == "size":
                special[enc] = (
                    "small"
                    if endpoint in {"low", "small"} or stem in {"low", "small"}
                    else "large"
                )
            else:
                special[enc] = endpoint if endpoint in {"low", "high"} else stem
        elif decoded.get("inferred_label") is None:
            special[enc] = stem
    return special


def _full_endpoint_encoded(special: dict[int, str]) -> int | None:
    for enc, token in special.items():
        if str(token).lower() in {"full", "high", "max"}:
            return int(enc)
    return None


def _cap_affine_endpoint_rows(
    by_enc: dict[int, dict[str, Any]],
    *,
    special: dict[int, str],
    scale: float | None,
    offset: float | None,
    unit: str | None,
) -> dict[int, dict[str, Any]]:
    """Drop spurious preset anchors past discrete full/off endpoints."""
    from .preset_inferred import densify_encoding_map

    full_enc = _full_endpoint_encoded(special)
    if full_enc is not None:
        by_enc = {enc: row for enc, row in by_enc.items() if enc <= full_enc}

    if scale is None or full_enc is None:
        return by_enc

    # Wet/dry gain: fill every 0.5 dB step from off through full.
    lo = 0 if 0 in special and str(special[0]).lower() == "off" else min(by_enc, default=0)
    seed = {enc: enc * scale + (offset or 0.0) for enc in range(lo, full_enc + 1)}
    filled = densify_encoding_map(seed, unit=unit)
    for row in filled:
        enc = int(row["encoded"])
        if enc not in by_enc:
            by_enc[enc] = row
    return by_enc


def full_encoding_rows(
    result: dict[str, Any],
    best: dict[str, Any],
    *,
    sysex_root: Path | None,
) -> list[dict[str, Any]] | None:
    """Full encoded→label map for a parameter (dump / provided / preset)."""
    series = series_numeric_mapping(result, best)
    special = series_special_labels(result)
    if not series and not special:
        return None

    from .preset_inferred import (
        build_affine_preset_anchors,
        build_sheet_preset_anchors,
        densify_encoding_map,
    )

    unit = result.get("unit")
    scale = None
    offset = None
    if (
        not is_table_encoding(best)
        and best.get("exact")
        and best.get("scale") is not None
        and best.get("score", 0) >= 0.999
    ):
        scale = float(best["scale"])
        offset = float(best.get("offset") or 0.0)

    preset: dict[int, float] = {}
    preset_refs: dict[int, list[tuple[str, str]]] = {}
    # System dumps use different payload layout; prog preset bytes at the same
    # offset are unrelated and produce spurious affine anchors.
    if sysex_root is not None and result.get("kind") != "system":
        sheet_anchors = build_sheet_preset_anchors(
            sysex_root,
            result["parameter"],
            best["offsets"],
            encoding=best["encoding"],
        )
        for enc, (label, refs) in sheet_anchors.items():
            preset[enc] = label
            preset_refs[enc] = refs
        if scale is not None:
            skip_special = {
                enc
                for enc, token in special.items()
                if str(token).lower() in {"off", "full"}
            }
            corpus = build_affine_preset_anchors(
                sysex_root,
                best["offsets"],
                encoding=best["encoding"],
                scale=scale,
                offset=offset or 0.0,
                skip_encodings=skip_special,
            )
            for enc, (label, refs) in corpus.items():
                if enc not in preset:
                    preset[enc] = label
                    preset_refs[enc] = refs

    from .provided import provided_display_mapping_for, provided_mapping_for

    provided = provided_mapping_for(
        result["parameter"],
        sysex_root=sysex_root,
    )
    inferred: dict[int, float] | None = None
    if scale is not None and best.get("exact") and best.get("score", 0) >= 0.999:
        synthetic = synthetic_affine_provided_mapping(
            series, special, scale, offset or 0.0
        )
        if synthetic:
            inferred = {
                enc: label
                for enc, label in synthetic.items()
                if enc not in series
                and enc not in preset
                and enc not in (provided or {})
            } or None

    seed = dict(series)
    for enc in special:
        if enc in seed:
            continue
        if scale is not None:
            seed[enc] = enc * scale + (offset or 0.0)
        else:
            seed[enc] = float(enc)

    if len(seed) < 1 and not preset and not provided and not inferred:
        if not special:
            return None
        return [
            {
                "encoded": enc,
                "label": token,
                "display": token,
                "source": "dump",
                "sources": ["dump"],
            }
            for enc, token in sorted(special.items())
        ]

    rows = densify_encoding_map(
        seed,
        preset,
        provided=provided,
        inferred=inferred,
        unit=unit,
        preset_refs=preset_refs,
    )

    by_enc = {int(r["encoded"]): r for r in rows}
    for enc, token in special.items():
        prev = by_enc.get(enc) or {}
        sources = list(prev.get("sources") or [])
        if "dump" not in sources:
            sources = ["dump", *sources]
        overlay: dict[str, Any] = {
            "encoded": enc,
            "label": token,
            "display": token,
            "source": "dump",
            "sources": sources or ["dump"],
        }
        if prev.get("preset_refs"):
            overlay["preset_refs"] = prev["preset_refs"]
        by_enc[enc] = overlay

    by_enc = _cap_affine_endpoint_rows(
        by_enc,
        special=special,
        scale=scale,
        offset=offset,
        unit=unit,
    )

    for enc, display in provided_display_mapping_for(
        result["parameter"],
        sysex_root=sysex_root,
    ).items():
        if enc in by_enc:
            by_enc[enc]["display"] = display

    return [by_enc[e] for e in sorted(by_enc)]


def format_row_display_label(result: dict[str, Any], row: dict[str, Any]) -> str:
    """Human label for one densified encoding row (balance A/B, units)."""
    from .labels import format_value_with_unit

    if row.get("display") is not None:
        return str(row["display"])
    if isinstance(row.get("label"), str):
        return str(row["label"])

    balance = (result.get("value_range") or {}).get("balance") or {}
    balance_side = balance.get("side_max")
    if balance_side is not None and isinstance(row.get("label"), (int, float)):
        from .decode_preset import _balance_pair
        from .labels import format_balance_pair

        a, b = _balance_pair(int(row["label"]), int(balance_side))
        return format_balance_pair(a, b)
    return format_value_with_unit(row["label"], result.get("unit"))
