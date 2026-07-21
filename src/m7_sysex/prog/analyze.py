"""Diff M7 program dumps and reverse-engineer parameter byte layouts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .catalog import annotate_series
from ..encodings import decode_at_offsets, fit_numeric_encoding, rank_key
from ..frame import (
    BRICASTI_MFR_ID,
    CHECKSUM_NIBBLE_COUNT,
    DATA_OFFSET,
    PROGRAM_DUMP_HEADER,
    is_nibble_payload,
    parse_sysex,
)
from ..labels import DumpLabel, common_unit, display_unit, load_dumps
from ..paths import (
    prog_byte_map_path,
    prog_cross_analysis_path,
    prog_parameters_root,
    prog_presets_root,
    system_root,
)
from ..sampling import classify_sampling
from ..series import (
    balance_series_meta,
    build_hypothesis,
    changing_offsets,
    contiguous_pairs,
    fit_to_dict,
    group_regions,
    infer_label_from_encoded,
    leading_zero_nibble_pairs,
    resolve_value_range,
    secondary_offsets,
    write_analysis,
)


def analyze_parameter_folder(folder: Path) -> dict[str, Any]:
    """
    Analyze all SysEx dumps in a single-parameter capture folder.

    The folder is treated as an independent stream: only dumps inside it are
    compared. Results must not be byte-diffed against other parameter folders.
    """
    folder = folder.resolve()
    dumps = load_dumps(folder)
    if len(dumps) < 2:
        raise ValueError(
            f"{folder}: need at least 2 .syx dumps to diff (found {len(dumps)})"
        )

    parsed = []
    for path, label, raw in dumps:
        frame = parse_sysex(raw)
        parsed.append(
            {
                "path": path,
                "label": label,
                "raw": raw,
                "frame": frame,
            }
        )

    lengths = {len(p["raw"]) for p in parsed}
    if len(lengths) != 1:
        raise ValueError(f"{folder}: dump lengths differ: {sorted(lengths)}")

    length = next(iter(lengths))
    changing = changing_offsets([p["raw"] for p in parsed])
    regions = group_regions(changing)

    payload_start = DATA_OFFSET
    payload_end = length - 1  # exclusive of F7
    checksum_start = payload_end - CHECKSUM_NIBBLE_COUNT

    # Classify regions.
    checksum_offsets = [i for i in changing if i >= checksum_start]
    param_candidate_offsets = [i for i in changing if payload_start <= i < checksum_start]
    header_offsets = [i for i in changing if i < payload_start]

    nibble_payload = all(
        is_nibble_payload(p["raw"][payload_start:payload_end]) for p in parsed
    )

    # Encoding fits for contiguous parameter candidate pairs / singles.
    encoding_results: list[dict[str, Any]] = []
    numeric_dumps = [
        (p["label"].value, p["raw"])
        for p in parsed
        if p["label"].kind == "number"
    ]

    if numeric_dumps and param_candidate_offsets:
        # Prefer contiguous pairs within param candidates, plus pad+value
        # pairs where the preceding wire byte is a constant zero nibble.
        pair_offsets = contiguous_pairs(param_candidate_offsets)
        pad_pairs = leading_zero_nibble_pairs(
            [p["raw"] for p in parsed],
            param_candidate_offsets,
            payload_start=payload_start,
        )
        tried: set[tuple[str, tuple[int, ...]]] = set()

        for pair in pair_offsets:
            for encoding in ("nibble_hilo", "nibble_lohi", "midi14_be", "midi14_le"):
                key = (encoding, pair)
                if key in tried:
                    continue
                tried.add(key)
                fit = fit_numeric_encoding(numeric_dumps, pair, encoding)
                encoding_results.append(fit_to_dict(fit))

        for pair in pad_pairs:
            key = ("nibble_hilo", pair)
            if key in tried:
                continue
            tried.add(key)
            fit = fit_numeric_encoding(numeric_dumps, pair, "nibble_hilo")
            encoding_results.append(fit_to_dict(fit))

        for off in param_candidate_offsets:
            fit = fit_numeric_encoding(numeric_dumps, (off,), "raw_u8")
            encoding_results.append(fit_to_dict(fit))

        encoding_results.sort(key=rank_key)

    best = encoding_results[0] if encoding_results else None

    # Shared unit from mid dumps (e.g. hz, ms) - endpoints inherit it for display.
    unit = common_unit([p["label"] for p in parsed])

    # Capture roles: extremes, adjacent-to-extremes, mids.
    sampling = classify_sampling(parsed, best)

    # Resolve OFF/LOW/HIGH|FULL endpoints using the best encoding (discover min/max).
    value_range = resolve_value_range(parsed, best, unit, sampling)
    balance_meta = balance_series_meta(parsed)
    if value_range is not None and balance_meta:
        value_range["balance"] = balance_meta
        if value_range.get("min") is not None and value_range.get("max") is not None:
            side = balance_meta["side_max"]
            value_range["summary"] = (
                f"Balance path 0/{side} ... {side}/{side} ... {side}/0 "
                f"(positions {value_range['min']} ... {value_range['max']}; "
                f"filenames use A.B for '/')"
            )

    # Per-dump byte table for changing offsets only.
    dump_rows = []
    for p in parsed:
        label: DumpLabel = p["label"]
        row: dict[str, Any] = {
            "file": p["path"].name,
            "label": {
                "kind": label.kind,
                "value": label.value,
                "unit": label.unit,
                "unit_display": display_unit(label.unit),
                "stem": label.stem,
                "endpoint": label.endpoint,
                "raw_label": label.raw_label,
                "pair": list(label.pair) if label.pair else None,
                "balance_side_max": label.balance_side_max,
            },
            "sampling_role": sampling["roles_by_file"].get(p["path"].name),
            "program_name": p["frame"].name,
            "changing_bytes": {
                str(i): f"{p['raw'][i]:02X}" for i in changing
            },
        }
        if best and label.kind in ("number", "endpoint"):
            field = decode_at_offsets(p["raw"], best["offsets"], best["encoding"])
            inferred = infer_label_from_encoded(field.value, best)
            decoded: dict[str, Any] = {
                "encoding": best["encoding"],
                "offsets": list(best["offsets"]),
                "raw_bytes": [f"{b:02X}" for b in field.raw_bytes],
                "encoded_value": field.value,
            }
            if inferred is not None:
                decoded["inferred_label"] = inferred
            row["decoded_parameter"] = decoded
        dump_rows.append(row)

    mfr_ok = all(p["frame"].manufacturer_id == BRICASTI_MFR_ID for p in parsed)
    header_ok = all(p["frame"].header == PROGRAM_DUMP_HEADER for p in parsed)

    hypothesis = build_hypothesis(
        folder.name,
        best,
        param_candidate_offsets,
        checksum_offsets,
        nibble_payload,
        value_range,
        sampling,
    )

    official = annotate_series(folder.name, value_range, unit=unit)

    result: dict[str, Any] = {
        "parameter": folder.name,
        "folder": str(folder),
        "dump_count": len(parsed),
        "message_length": length,
        "unit": unit,
        "unit_display": display_unit(unit),
        "frame": {
            "manufacturer_id": BRICASTI_MFR_ID.hex(" "),
            "manufacturer_id_match": mfr_ok,
            "header": PROGRAM_DUMP_HEADER.hex(" "),
            "header_match": header_ok,
            "name_offset": 8,
            "name_length": 80,
            "data_offset": DATA_OFFSET,
            "checksum_offsets": list(range(checksum_start, payload_end)),
            "nibble_payload": nibble_payload,
            "notes": (
                "Payload bytes after the ASCII program name are nibble-sized "
                "(0x00-0x0F). The final four nibbles before F7 are a CRC-16/ARC "
                "over offsets 8-151, packed high-nibble-first."
                if nibble_payload
                else "Payload contains bytes > 0x0F; nibble packing may not apply."
            ),
        },
        "changing_offsets": changing,
        "changing_regions": [
            {"start": s, "end": e, "length": e - s + 1, "offsets": list(range(s, e + 1))}
            for s, e in regions
        ],
        "classification": {
            "parameter_candidate_offsets": param_candidate_offsets,
            "checksum_candidate_offsets": checksum_offsets,
            "header_or_name_offsets": header_offsets,
            "secondary_offsets": secondary_offsets(
                param_candidate_offsets, best
            ),
        },
        "sampling": sampling,
        "value_range": value_range,
        "official": official,
        "encoding_hypotheses": encoding_results,
        "best_encoding": best,
        "hypothesis": hypothesis,
        "dumps": dump_rows,
    }
    return result


def analyze_tree(sysex_root: Path) -> list[dict[str, Any]]:
    """Analyze every parameter folder under ``sysex/prog/parameters/``."""
    sysex_root = Path(sysex_root).resolve()
    params_root = prog_parameters_root(sysex_root)
    if params_root.name == "parameters" and params_root.is_dir():
        scan_root = params_root
    elif params_root.is_dir():
        scan_root = params_root
    else:
        return []

    results = []
    for child in sorted(p for p in scan_root.iterdir() if p.is_dir()):
        syx = list(child.glob("*.syx")) + list(child.glob("*.SYX"))
        if not syx:
            continue
        results.append(analyze_parameter_folder(child))
    return results


def clear_analysis_outputs(sysex_root: Path) -> list[Path]:
    """Delete generated analysis JSON and byte-map artifacts under ``sysex/``."""
    sysex_root = sysex_root.resolve()
    removed: list[Path] = []
    candidates = [
        prog_byte_map_path(sysex_root),
        prog_cross_analysis_path(sysex_root),
    ]
    params = prog_parameters_root(sysex_root)
    if params.is_dir():
        for child in params.iterdir():
            if child.is_dir():
                candidates.append(child / "analysis.json")
    presets = prog_presets_root(sysex_root)
    if presets.is_dir():
        candidates.append(presets / "analysis.json")
    sys_root = system_root(sysex_root)
    if sys_root.is_dir():
        candidates.append(sys_root / "analysis.json")
        for child in sys_root.iterdir():
            if child.is_dir():
                candidates.append(child / "analysis.json")
    for path in candidates:
        if path.is_file():
            path.unlink()
            removed.append(path)
    return removed

    """Summarize balance/mix A/B labeling when the folder uses that display."""
    numbered = [p for p in parsed if p["label"].kind == "number" and p["label"].pair]
