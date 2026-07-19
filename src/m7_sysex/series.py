"""Shared parameter-series analysis helpers (PROG and SYSTEM)."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .encodings import decode_at_offsets, is_enum_table_fit
from .frame import PROG_CHECKSUM_COVER
from .labels import display_unit, format_value_with_unit
from .sampling import CAPTURE_CONVENTION, sampling_range_summary


def write_analysis(result: dict[str, Any], path: Path | None = None) -> Path:
    """Overwrite analysis JSON next to the dumps (or at an explicit path)."""
    if path is None:
        path = Path(result["folder"]) / "analysis.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return path


def balance_series_meta(parsed: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Summarize balance/mix A/B labeling when the folder uses that display."""
    numbered = [p for p in parsed if p["label"].kind == "number" and p["label"].pair]
    if len(numbered) < 3:
        return None
    if not all(p["label"].pair for p in numbered):
        return None
    side = numbered[0]["label"].balance_side_max
    if side is None:
        return None
    return {
        "side_max": side,
        "position_max": 2 * side,
        "display": (
            f"A/B mix with side max {side}: "
            f"0/{side} -> {side}/{side} -> {side}/0 "
            f"(filenames use A.B because '/' is illegal); "
            f"fitted value is path position 0..{2 * side}"
        ),
    }


def changing_offsets(blobs: list[bytes]) -> list[int]:
    length = len(blobs[0])
    changing = []
    for i in range(length):
        values = {b[i] for b in blobs}
        if len(values) > 1:
            changing.append(i)
    return changing


def group_regions(offsets: list[int]) -> list[tuple[int, int]]:
    if not offsets:
        return []
    regions: list[tuple[int, int]] = []
    start = prev = offsets[0]
    for off in offsets[1:]:
        if off == prev + 1:
            prev = off
            continue
        regions.append((start, prev))
        start = prev = off
    regions.append((start, prev))
    return regions


def contiguous_pairs(offsets: list[int]) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    offset_set = set(offsets)
    for off in offsets:
        if off + 1 in offset_set:
            pairs.append((off, off + 1))
    return pairs


def resolve_value_range(
    parsed: list[dict[str, Any]],
    best: dict[str, Any] | None,
    unit: str | None = None,
    sampling: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Discover OFF / LOW / HIGH|FULL extremes using the best encoding."""
    endpoints = {
        p["label"].endpoint: p
        for p in parsed
        if p["label"].kind == "endpoint" and p["label"].endpoint
    }
    numbered = [p for p in parsed if p["label"].kind == "number"]
    sampling = sampling or {}

    if not endpoints:
        result: dict[str, Any] = {
            "convention": CAPTURE_CONVENTION,
        }
        if unit:
            result["unit"] = unit
            result["unit_display"] = display_unit(unit)
        extreme_summary = sampling_range_summary(sampling, unit)
        if extreme_summary:
            result.update(extreme_summary)
        elif numbered:
            values = [float(p["label"].value) for p in numbered]
            result["min"] = min(values)
            result["max"] = max(values)
            if float(result["min"]).is_integer():
                result["min"] = int(result["min"])
            if float(result["max"]).is_integer():
                result["max"] = int(result["max"])
            unit_suffix = f" {display_unit(unit)}" if display_unit(unit) else ""
            if display_unit(unit) == "%":
                unit_suffix = "%"
            result["summary"] = (
                f"Observed range {result['min']} ... {result['max']}{unit_suffix}"
            )
        if sampling.get("edge_steps"):
            result["edge_steps"] = sampling["edge_steps"]
        return result if (unit or numbered or extreme_summary) else None

    result = {
        "convention": CAPTURE_CONVENTION,
    }
    if unit is None:
        unit = next(
            (
                p["label"].unit
                for p in parsed
                if p["label"].kind == "number" and p["label"].unit
            ),
            None,
        )
    if unit:
        result["unit"] = unit
        result["unit_display"] = display_unit(unit)

    can_infer = bool(
        best
        and best.get("exact")
        and best.get("score", 0) >= 0.999
        and best.get("scale") is not None
    )

    numbered = [p for p in parsed if p["label"].kind == "number"]
    max_numbered = max(numbered, key=lambda p: float(p["label"].value), default=None)
    max_numbered_encoded = None
    if best and max_numbered is not None:
        max_numbered_encoded = decode_at_offsets(
            max_numbered["raw"], best["offsets"], best["encoding"]
        ).value

    for which in ("off", "low", "high"):
        p = endpoints.get(which)
        if not p:
            continue
        entry: dict[str, Any] = {"file": p["path"].name, "endpoint": which}
        if best:
            field = decode_at_offsets(p["raw"], best["offsets"], best["encoding"])
            entry["encoded_value"] = field.value
            entry["raw_bytes"] = [f"{b:02X}" for b in field.raw_bytes]
            if can_infer and which != "off":
                inferred = infer_label_from_encoded(field.value, best)
                if inferred is not None:
                    entry["inferred_label"] = inferred
                    entry["inferred_label_display"] = format_value_with_unit(
                        inferred, unit
                    )
            elif which == "off":
                entry["note"] = "discrete off (not converted through the mid-value scale)"
            elif which == "high" and max_numbered is not None and max_numbered_encoded is not None:
                max_label = max_numbered["label"].value
                if field.value > max_numbered_encoded:
                    entry["bound"] = "above_max_numbered"
                    entry["above"] = max_label
                    entry["above_encoded"] = max_numbered_encoded
                    entry["note"] = (
                        f"encoded {field.value} is {field.value - max_numbered_encoded} "
                        f"step(s) above {format_value_with_unit(max_label, unit)} "
                        f"(encoded {max_numbered_encoded}); absolute unit value unknown "
                        f"(likely a non-linear table / 'full' max)."
                    )
                elif field.value == max_numbered_encoded:
                    entry["bound"] = "same_as_max_numbered"
                    entry["note"] = (
                        f"same encoded value as max numbered mid "
                        f"({format_value_with_unit(max_label, unit)})"
                    )
                else:
                    entry["bound"] = "below_max_numbered"
                    entry["note"] = (
                        f"encoded {field.value} < max numbered "
                        f"{format_value_with_unit(max_label, unit)} "
                        f"(encoded {max_numbered_encoded})"
                    )
        result[which] = entry

    low = result.get("low", {}).get("inferred_label")
    high = result.get("high", {}).get("inferred_label")
    off_entry = result.get("off")

    unit_suffix = f" {display_unit(unit)}" if display_unit(unit) else ""
    if display_unit(unit) == "%":
        unit_suffix = "%"

    if low is not None and high is not None:
        result["min"] = low
        result["max"] = high
        if off_entry and "encoded_value" in off_entry:
            result["summary"] = (
                f"off encoded={off_entry['encoded_value']}; "
                f"range {low} ... {high}{unit_suffix}"
            )
        else:
            result["summary"] = f"Observed range {low} ... {high}{unit_suffix}"
    elif low is not None and result.get("high", {}).get("bound") == "above_max_numbered":
        high_entry = result["high"]
        result["min"] = low
        prefix = ""
        if off_entry and "encoded_value" in off_entry:
            prefix = f"off encoded={off_entry['encoded_value']}; "
        result["summary"] = (
            f"{prefix}from {format_value_with_unit(low, unit)}; "
            f"full/high encoded={high_entry['encoded_value']} "
            f"(> {format_value_with_unit(high_entry['above'], unit)})"
        )
    else:
        extreme_summary = sampling_range_summary(sampling, unit)
        if extreme_summary:
            result["min"] = extreme_summary["min"]
            result["max"] = extreme_summary["max"]
            result["range_authority"] = extreme_summary.get("range_authority")
            if off_entry and "encoded_value" in off_entry:
                result["summary"] = (
                    f"off encoded={off_entry['encoded_value']}; "
                    f"range {result['min']} ... {result['max']}{unit_suffix}"
                )
            else:
                result["summary"] = extreme_summary["summary"]
        elif numbered:
            values = [float(p["label"].value) for p in numbered]
            result["min"] = min(values)
            result["max"] = max(values)
            if float(result["min"]).is_integer():
                result["min"] = int(result["min"])
            if float(result["max"]).is_integer():
                result["max"] = int(result["max"])
            if off_entry and "encoded_value" in off_entry:
                result["summary"] = (
                    f"off encoded={off_entry['encoded_value']}; "
                    f"range {result['min']} ... {result['max']}{unit_suffix}"
                )
            else:
                result["summary"] = (
                    f"Observed range {result['min']} ... {result['max']}{unit_suffix}"
                )
        else:
            parts = []
            for which in ("off", "low", "high"):
                entry = result.get(which)
                if not entry or "encoded_value" not in entry:
                    continue
                if which == "off":
                    parts.append(f"off encoded={entry['encoded_value']}")
                elif "inferred_label_display" in entry:
                    parts.append(f"{which}={entry['inferred_label_display']}")
                elif which == "high" and entry.get("bound") == "above_max_numbered":
                    parts.append(
                        f"full/high encoded={entry['encoded_value']} "
                        f"(> {format_value_with_unit(entry['above'], unit)})"
                    )
                else:
                    parts.append(f"{which} encoded={entry['encoded_value']}")
            if parts:
                result["summary"] = "; ".join(parts)

    if sampling.get("edge_steps"):
        result["edge_steps"] = sampling["edge_steps"]
    return result


def infer_label_from_encoded(
    encoded: int, best: dict[str, Any]
) -> float | int | None:
    if not best.get("exact") or best.get("score", 0) < 0.999:
        return None
    scale = best.get("scale")
    if scale is None:
        return None
    offset = best.get("offset") or 0.0
    label = encoded * float(scale) + float(offset)
    if float(label).is_integer():
        return int(label)
    return label


def secondary_offsets(
    param_offsets: list[int], best: dict[str, Any] | None
) -> list[int]:
    if not best:
        return list(param_offsets)
    primary = set(best["offsets"])
    return [i for i in param_offsets if i not in primary]


def fit_to_dict(fit: Any) -> dict[str, Any]:
    data = asdict(fit)
    data["offsets"] = list(fit.offsets)
    return data


def build_hypothesis(
    parameter: str,
    best: dict[str, Any] | None,
    param_offsets: list[int],
    checksum_offsets: list[int],
    nibble_payload: bool,
    value_range: dict[str, Any] | None = None,
    sampling: dict[str, Any] | None = None,
    *,
    payload_note: str | None = None,
    checksum_cover: str | None = None,
) -> dict[str, Any]:
    if not best:
        return {
            "summary": (
                f"Bytes change at offsets {param_offsets}, but no encoding "
                "fit was found. Capture more labeled dumps or check filename labels."
            ),
            "confidence": "low",
        }

    score = best["score"]
    exact = best.get("exact", False)
    if score >= 1.0 and (exact or is_enum_table_fit(best)):
        confidence = "high"
    elif score >= 0.5:
        confidence = "medium"
    else:
        confidence = "low"

    notes = best.get("notes") or ""
    offsets = best["offsets"]
    encoding = best["encoding"]

    if is_enum_table_fit(best):
        summary_parts = [
            (
                f"Parameter '{parameter}' appears at SysEx offset(s) {offsets} "
                f"as an enum table using encoding '{encoding}' "
                f"({notes.split(';', 1)[0].strip()})"
            ),
        ]
    else:
        summary_parts = [
            f"Parameter '{parameter}' appears at SysEx offset(s) {offsets}",
            f"using encoding '{encoding}'",
        ]
        if exact and notes:
            summary_parts.append(f"({notes.split(';', 1)[0].strip()})")
        elif notes:
            summary_parts.append(f"({notes})")

    if value_range and value_range.get("summary"):
        summary_parts.append(value_range["summary"])

    edge = (sampling or {}).get("edge_steps") or {}
    if edge.get("edge_slopes_agree") is True:
        summary_parts.append(
            "extreme<->adjacent edge slopes agree "
            f"(dlabel/denc~={edge.get('agreed_label_per_encoded'):.6g})"
        )
    elif edge.get("edge_slopes_agree") is False:
        summary_parts.append(
            "extreme<->adjacent edge slopes disagree (table/index more likely)"
        )

    if checksum_offsets:
        summary_parts.append(
            f"Offsets {checksum_offsets} also change and are treated as checksum nibbles"
        )

    if param_offsets:
        secondary = [i for i in param_offsets if i not in offsets]
        if secondary:
            from .prog.display import describe_secondary_offsets

            summary_parts.append(
                f"Additional non-checksum offsets {describe_secondary_offsets(secondary)} "
                "also change (edit/UI state, not the parameter word)"
            )

    if nibble_payload:
        summary_parts.append(
            payload_note
            or "All post-name payload bytes are nibble-sized (0x00-0x0F)"
        )

    return {
        "summary": ". ".join(summary_parts) + ".",
        "confidence": confidence,
        "match_rate": score,
        "how_to_set": how_to_set(
            encoding,
            offsets,
            best.get("scale"),
            best.get("offset"),
            notes,
            checksum_cover=checksum_cover or PROG_CHECKSUM_COVER,
        ),
    }


def how_to_set(
    encoding: str,
    offsets: list[int],
    scale: float | None,
    offset: float | None,
    notes: str,
    *,
    checksum_cover: str = PROG_CHECKSUM_COVER,
) -> dict[str, Any]:
    guidance: dict[str, Any] = {
        "offsets": offsets,
        "encoding": encoding,
    }
    if scale is not None:
        guidance["scale"] = scale
    if offset is not None:
        guidance["offset"] = offset
    encode_prefix = scale_step(scale, offset)
    cs = f"recompute trailing checksum: CRC-16/ARC over {checksum_cover}"
    if encoding == "nibble_hilo" and scale is not None and exact_scale_note(notes):
        guidance["encode_steps"] = [
            encode_prefix,
            "byte[offset0] = (encoded >> 4) & 0x0F",
            "byte[offset1] = encoded & 0x0F",
            cs,
        ]
    elif encoding == "nibble_lohi" and scale is not None and exact_scale_note(notes):
        guidance["encode_steps"] = [
            encode_prefix,
            "byte[offset0] = encoded & 0x0F",
            "byte[offset1] = (encoded >> 4) & 0x0F",
            cs,
        ]
    elif encoding == "raw_u8" and scale is not None and exact_scale_note(notes):
        guidance["encode_steps"] = [
            encode_prefix,
            "byte[offset0] = encoded & 0x0F  # M7 payload nibbles are 0x00-0x0F",
            cs,
        ]
    elif is_enum_table_fit({"notes": notes}):
        if encoding == "raw_u8":
            write_step = "byte[offset0] = encoded & 0x0F  # M7 payload nibbles are 0x00-0x0F"
        elif encoding == "nibble_hilo":
            write_step = (
                "byte[offset0] = (encoded >> 4) & 0x0F; "
                "byte[offset1] = encoded & 0x0F"
            )
        elif encoding == "nibble_lohi":
            write_step = (
                "byte[offset0] = encoded & 0x0F; "
                "byte[offset1] = (encoded >> 4) & 0x0F"
            )
        else:
            write_step = "write encoded bytes per the capture encoding map"
        guidance["encode_steps"] = [
            "encoded = lookup desired label in the capture encoding map (enum table)",
            write_step,
            cs,
        ]
    else:
        guidance["encode_steps"] = [
            "Use the per-dump mapping table in encoding_hypotheses until a closed-form scale is confirmed",
            cs,
        ]
    guidance["notes"] = notes
    return guidance


def exact_scale_note(notes: str | None) -> bool:
    return bool(notes) and notes.startswith("label = encoded")


def scale_step(scale: float | None, offset: float | None = None) -> str:
    off = float(offset or 0.0)
    if scale is None:
        return "encoded = <unknown mapping>"
    if scale == 1 and off == 0:
        return "encoded = desired_label"
    if scale == 1:
        return f"encoded = desired_label - ({off:g})"
    if float(scale).is_integer() and off == 0:
        return f"encoded = round(desired_label / {int(scale)})"
    if off == 0:
        return f"encoded = round(desired_label / {scale})"
    return f"encoded = round((desired_label - ({off:g})) / {scale})"
