"""Analyze M7 system-dump SysEx captures (I/O and routing, not program params)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..encodings import (
    decode_at_offsets,
    fit_enum_encoding,
    fit_numeric_encoding,
    rank_key,
)
from ..frame import (
    BRICASTI_MFR_ID,
    CHECKSUM_NIBBLE_COUNT,
    SYSTEM_CHECKSUM_COVER,
    SYSTEM_CHECKSUM_COVER_END,
    SYSTEM_DUMP_HEADER,
    SYSTEM_MESSAGE_LENGTH,
    SYSTEM_PAYLOAD_OFFSET,
    is_nibble_payload,
    parse_system_sysex,
)
from ..labels import DumpLabel, common_unit, display_unit, load_dumps
from ..paths import system_root
from ..sampling import classify_sampling
from ..series import (
    build_hypothesis,
    changing_offsets,
    contiguous_pairs,
    fit_to_dict,
    group_regions,
    resolve_value_range,
    secondary_offsets,
    write_analysis,
)


def analyze_system_series_folder(folder: Path) -> dict[str, Any]:
    """Analyze all system dumps in a single series folder under ``sysex/system/``."""
    folder = folder.resolve()
    dumps = load_dumps(folder)
    if len(dumps) < 2:
        raise ValueError(
            f"{folder}: need at least 2 .syx dumps to diff (found {len(dumps)})"
        )

    parsed = []
    for path, label, raw in dumps:
        frame = parse_system_sysex(raw)
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

    payload_start = SYSTEM_PAYLOAD_OFFSET
    payload_end = SYSTEM_CHECKSUM_COVER_END
    checksum_start = payload_end

    checksum_offsets = [i for i in changing if i >= checksum_start]
    param_candidate_offsets = [
        i for i in changing if payload_start <= i < checksum_start
    ]
    header_offsets = [i for i in changing if i < payload_start]

    nibble_payload = all(
        is_nibble_payload(p["raw"][payload_start:payload_end]) for p in parsed
    )

    encoding_results: list[dict[str, Any]] = []
    numeric_dumps = [
        (p["label"].value, p["raw"])
        for p in parsed
        if p["label"].kind == "number"
    ]
    enum_dumps = [
        (p["label"].stem, p["raw"])
        for p in parsed
        if p["label"].kind == "enum"
    ]

    if param_candidate_offsets and (numeric_dumps or enum_dumps):
        pair_offsets = contiguous_pairs(param_candidate_offsets)
        tried: set[tuple[str, tuple[int, ...]]] = set()

        if numeric_dumps:
            for pair in pair_offsets:
                for encoding in (
                    "nibble_hilo",
                    "nibble_lohi",
                    "midi14_be",
                    "midi14_le",
                ):
                    key = (encoding, pair)
                    if key in tried:
                        continue
                    tried.add(key)
                    fit = fit_numeric_encoding(numeric_dumps, pair, encoding)
                    encoding_results.append(fit_to_dict(fit))

            for off in param_candidate_offsets:
                key = ("raw_u8", (off,))
                if key in tried:
                    continue
                tried.add(key)
                fit = fit_numeric_encoding(numeric_dumps, (off,), "raw_u8")
                encoding_results.append(fit_to_dict(fit))

        if enum_dumps:
            for pair in pair_offsets:
                for encoding in ("nibble_hilo", "nibble_lohi"):
                    key = (encoding, pair)
                    if key in tried:
                        continue
                    tried.add(key)
                    fit = fit_enum_encoding(enum_dumps, pair, encoding)
                    encoding_results.append(fit_to_dict(fit))

            for off in param_candidate_offsets:
                key = ("raw_u8", (off,))
                if key in tried:
                    continue
                tried.add(key)
                fit = fit_enum_encoding(enum_dumps, (off,), "raw_u8")
                encoding_results.append(fit_to_dict(fit))

        encoding_results.sort(key=rank_key)

    best = encoding_results[0] if encoding_results else None
    unit = common_unit([p["label"] for p in parsed])
    sampling = classify_sampling(parsed, best)
    value_range = resolve_value_range(parsed, best, unit, sampling)

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
            },
            "sampling_role": sampling["roles_by_file"].get(p["path"].name),
            "changing_bytes": {
                str(i): f"{p['raw'][i]:02X}" for i in changing
            },
        }
        if best and label.kind in ("number", "endpoint", "enum"):
            field = decode_at_offsets(p["raw"], best["offsets"], best["encoding"])
            decoded: dict[str, Any] = {
                "encoding": best["encoding"],
                "offsets": list(best["offsets"]),
                "raw_bytes": [f"{b:02X}" for b in field.raw_bytes],
                "encoded_value": field.value,
            }
            row["decoded_parameter"] = decoded
        dump_rows.append(row)

    duplicate_notes = _duplicate_byte_notes(parsed, changing)

    mfr_ok = all(p["frame"].manufacturer_id == BRICASTI_MFR_ID for p in parsed)
    header_ok = all(p["frame"].header == SYSTEM_DUMP_HEADER for p in parsed)

    hypothesis = build_hypothesis(
        folder.name,
        best,
        param_candidate_offsets,
        checksum_offsets,
        nibble_payload,
        value_range,
        sampling,
        payload_note="Payload bytes 8-71 are nibble-sized (0x00-0x0F)",
        checksum_cover=SYSTEM_CHECKSUM_COVER,
    )
    if duplicate_notes:
        hypothesis = {
            **hypothesis,
            "notes": (hypothesis.get("notes") or "") + " " + duplicate_notes,
        }

    return {
        "kind": "system",
        "parameter": folder.name,
        "folder": str(folder),
        "dump_count": len(parsed),
        "message_length": length,
        "unit": unit,
        "unit_display": display_unit(unit),
        "frame": {
            "manufacturer_id": BRICASTI_MFR_ID.hex(" "),
            "manufacturer_id_match": mfr_ok,
            "header": SYSTEM_DUMP_HEADER.hex(" "),
            "header_match": header_ok,
            "payload_offset": SYSTEM_PAYLOAD_OFFSET,
            "payload_end": SYSTEM_CHECKSUM_COVER_END,
            "checksum_offsets": list(
                range(checksum_start, checksum_start + CHECKSUM_NIBBLE_COUNT)
            ),
            "nibble_payload": nibble_payload,
            "notes": (
                "Payload bytes 8-71 are nibble-sized (0x00-0x0F). "
                "The final four nibbles before F7 are a CRC-16/ARC over offsets "
                "8-71, packed high-nibble-first. No program-name / "
                "register-basis region (payload starts at offset 8)."
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
            "secondary_offsets": secondary_offsets(param_candidate_offsets, best),
        },
        "sampling": sampling,
        "value_range": value_range,
        "encoding_hypotheses": encoding_results,
        "best_encoding": best,
        "hypothesis": hypothesis,
        "duplicate_byte_notes": duplicate_notes or None,
        "dumps": dump_rows,
    }


def _duplicate_byte_notes(
    parsed: list[dict[str, Any]], changing: list[int]
) -> str | None:
    """Flag distinct labels that share identical changing-byte patterns."""
    if not changing:
        return None
    by_pattern: dict[tuple[str, ...], list[str]] = {}
    for p in parsed:
        key = tuple(f"{p['raw'][i]:02X}" for i in changing)
        by_pattern.setdefault(key, []).append(p["path"].stem)
    groups = [stems for stems in by_pattern.values() if len(stems) > 1]
    if not groups:
        return None
    parts = ["/".join(sorted(g)) for g in groups]
    return (
        "Distinct labels share identical changing bytes in this capture set: "
        + "; ".join(parts)
        + "."
    )


def analyze_system_tree(sysex_root: Path) -> list[dict[str, Any]]:
    """Analyze every series folder under ``sysex/system/`` that contains dumps."""
    root = system_root(sysex_root)
    if not root.is_dir():
        return []

    results = []
    for child in sorted(p for p in root.iterdir() if p.is_dir()):
        if child.name.startswith("_") or child.name == "menus":
            continue
        syx = list(child.glob("*.syx")) + list(child.glob("*.SYX"))
        if len(syx) < 2:
            continue
        results.append(analyze_system_series_folder(child))
    return results


def write_system_analysis(result: dict[str, Any], path: Path | None = None) -> Path:
    """Write analysis JSON next to the system series dumps."""
    return write_analysis(result, path)


def write_system_summary(
    results: list[dict[str, Any]], sysex_root: Path
) -> Path | None:
    """Write ``sysex/system/analysis.json`` index when series exist."""
    if not results:
        return None
    root = system_root(sysex_root)
    summary = {
        "kind": "system_summary",
        "folder": str(root),
        "series_count": len(results),
        "dump_count": sum(r["dump_count"] for r in results),
        "message_length": SYSTEM_MESSAGE_LENGTH,
        "header": SYSTEM_DUMP_HEADER.hex(" "),
        "series": [
            {
                "parameter": r["parameter"],
                "folder": r["folder"],
                "dump_count": r["dump_count"],
                "changing_offsets": r["changing_offsets"],
                "best_encoding": r.get("best_encoding"),
            }
            for r in sorted(results, key=lambda r: r["parameter"])
        ],
    }
    path = root / "analysis.json"
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return path


def clear_system_analysis_outputs(sysex_root: Path) -> list[Path]:
    """Delete ``analysis.json`` under ``sysex/system`` and each series folder."""
    root = system_root(sysex_root)
    removed: list[Path] = []
    if not root.is_dir():
        return removed
    candidates = [root / "analysis.json"]
    for child in root.iterdir():
        if child.is_dir():
            candidates.append(child / "analysis.json")
    for path in candidates:
        if path.is_file():
            path.unlink()
            removed.append(path)
    return removed
