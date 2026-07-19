"""Sound-parameter knowledge inferred from factory presets + the published sheet.

Two uses:

1. Fallback decoders when a dedicated ``sysex/prog/parameters/<parameter>/``
   capture series does not exist yet (series analysis always wins once a
   folder is present).
2. Extra ``encoded -> sheet value`` mapping points that densify a sparse
   series table for decoding (series points win on conflict).
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, Sequence

from ..paths import prog_presets_root

from ..encodings import decode_at_offsets
from .names import validate_preset_dump

# Sheet-matched dumps fit label = 0.05×enc + 0.2 for values ≤ 2.0×.
# The dedicated capture series shows the step doubles to 0.1 above 2.0×
# (enc 36 → 2.0 ... enc 56 → 4.0) - so the affine is a low-range fallback
# only; decoding prefers the series table merged with sheet points.
LF_RT_MULTIPLY = {
    "parameter": "lf rt multiply",
    "offsets": [118, 119],
    "encoding": "nibble_hilo",
    "kind": "affine",
    "scale": 0.05,
    "offset": 0.2,
    "unit": None,
    "source": "preset_sheet",
    "confidence": "medium",
    "notes": (
        "Inferred from sysex/prog/presets/ vs Bricasti preset sheet. Valid for "
        "labels ≤ 2.0× only - steps are 0.1 above 2.0× (see "
        "sysex/prog/parameters/lf rt multiply/ series)."
    ),
}

LF_RT_CROSSOVER = {
    "parameter": "lf rt crossover",
    "offsets": [120, 121],
    "encoding": "nibble_hilo",
    "kind": "table",
    "unit": "hz",
    "source": "preset_sheet",
    "confidence": "medium",
    "notes": (
        "Inferred from sysex/prog/presets/ vs Bricasti preset sheet "
        "(own Hz table, not shared with HF RT crossover). "
        "Confirm with a dedicated capture series."
    ),
}

# Fallback table (mode sheet Hz per encoding) from the current corpus.
# Regenerated at runtime when presets + sheet JSON are available.
LF_RT_CROSSOVER_FALLBACK: dict[int, float] = {
    1: 120.0,
    2: 160.0,
    3: 200.0,
    4: 240.0,  # sheet also prints 320 for South Church (soft/hard)
    5: 280.0,
    6: 320.0,
    7: 360.0,  # sheet prints 340 for Worcester Hall (off-grid; hardware is 360)
    8: 400.0,
    9: 480.0,  # sheet also prints 500 for some presets (soft)
    10: 560.0,
    11: 640.0,
    12: 720.0,  # sheet also prints 780 for one preset (soft)
    13: 800.0,
    14: 1000.0,
    15: 1200.0,
    20: 2400.0,
    24: 4000.0,
}

PRESET_INFERRED = (LF_RT_MULTIPLY, LF_RT_CROSSOVER)

# encoding → (label, [(bank, preset_name), ...])
PresetAnchors = dict[int, tuple[float, list[tuple[str, str]]]]


def preset_inferred_decoders(
    *,
    sysex_root: Path | None = None,
    sheet_json: Path | None = None,
) -> list[dict[str, Any]]:
    """Return decode specs for parameters known from presets + sheet.

    Each spec carries a sheet-derived ``encoded -> value`` mapping so callers
    can densify sparse series tables (``merge_inferred_mapping``).
    """
    decoders: list[dict[str, Any]] = []
    for base in PRESET_INFERRED:
        spec = dict(base)
        mapping: dict[int, float] = {}
        if sysex_root is not None:
            mapping = build_sheet_mode_mapping(
                sysex_root,
                spec["parameter"],
                tuple(spec["offsets"]),
                sheet_json=sheet_json,
            )
        if not mapping and spec["parameter"] == "lf rt crossover":
            mapping = dict(LF_RT_CROSSOVER_FALLBACK)
        spec["mapping"] = mapping
        spec.setdefault("has_off", False)
        spec.setdefault("balance_side_max", None)
        spec.setdefault("observed_min", None)
        spec.setdefault("observed_max", None)
        decoders.append(spec)
    return decoders


def merge_inferred_mapping(
    series_spec: dict[str, Any],
    inferred_spec: dict[str, Any] | None,
) -> dict[str, Any]:
    """Densify a sparse series table with sheet-derived mapping points.

    Only applies when the inferred spec targets the same offsets/encoding.
    Series capture points always win on conflicting encodings.
    """
    if (
        series_spec.get("kind") != "table"
        or not inferred_spec
        or not inferred_spec.get("mapping")
        or list(inferred_spec.get("offsets") or []) != list(series_spec["offsets"])
        or inferred_spec.get("encoding") != series_spec.get("encoding")
    ):
        return series_spec

    merged = {int(k): float(v) for k, v in inferred_spec["mapping"].items()}
    merged.update(series_spec.get("mapping") or {})
    series_spec["mapping"] = dict(sorted(merged.items()))
    series_spec["mapping_sources"] = ["series", "preset_sheet"]
    return series_spec


def build_lf_crossover_mapping(
    sysex_root: Path,
    *,
    sheet_json: Path | None = None,
) -> dict[int, float]:
    """Map nibble_hilo encodings at 120-121 → sheet LF crossover Hz (mode)."""
    return build_sheet_mode_mapping(
        sysex_root,
        "lf rt crossover",
        (120, 121),
        encoding="nibble_hilo",
        sheet_json=sheet_json,
    )


def build_sheet_preset_anchors(
    sysex_root: Path,
    parameter: str,
    offsets: Sequence[int],
    *,
    encoding: str = "nibble_hilo",
    sheet_json: Path | None = None,
) -> PresetAnchors:
    """Sheet-matched anchors: encoding → (modal label, agreeing presets).

    Each preset is ``(bank, preset_name)``. Only dumps whose sheet value equals
    the modal label for that encoding are listed.
    """
    from .preset_sheet import (
        build_sheet_index,
        default_sheet_json_path,
        load_sheet_json,
        match_sheet_row,
        parse_sheet_value,
    )

    offsets = tuple(offsets)
    if not offsets:
        return {}

    presets_dir = prog_presets_root(sysex_root)
    if not presets_dir.is_dir():
        return {}

    json_path = Path(sheet_json) if sheet_json else default_sheet_json_path(sysex_root)
    if not json_path.is_file():
        return {}

    sheet_rows = load_sheet_json(json_path)
    index = build_sheet_index(sheet_rows)
    observations: dict[int, list[tuple[float, str, str]]] = {}

    for path in sorted(presets_dir.glob("*.syx")):
        raw = path.read_bytes()
        identity = validate_preset_dump(path, raw)
        bank = identity["bank"]
        preset_name = identity["preset"]
        dump = {"bank": bank, "preset": preset_name}
        sheet = match_sheet_row(dump, index, sheet_rows)
        if sheet is None:
            continue
        token = (sheet.get("sheet") or {}).get(parameter)
        if token is None:
            continue
        _kind, val = parse_sheet_value(parameter, token)
        if not isinstance(val, (int, float)):
            continue
        try:
            enc = int(decode_at_offsets(raw, offsets, encoding).value)
        except (ValueError, IndexError):
            continue
        observations.setdefault(enc, []).append((float(val), bank, preset_name))

    if not observations:
        return {}

    out: PresetAnchors = {}
    for enc, rows in sorted(observations.items()):
        counts: Counter[float] = Counter(label for label, _b, _p in rows)
        mode = float(counts.most_common(1)[0][0])
        refs = sorted(
            {(bank, preset) for label, bank, preset in rows if label == mode}
        )
        out[enc] = (mode, refs)
    return out


def build_sheet_mode_mapping(
    sysex_root: Path,
    parameter: str,
    offsets: Sequence[int],
    *,
    encoding: str = "nibble_hilo",
    sheet_json: Path | None = None,
) -> dict[int, float]:
    """Map encodings at ``offsets`` → sheet values for ``parameter`` (mode)."""
    anchors = build_sheet_preset_anchors(
        sysex_root,
        parameter,
        offsets,
        encoding=encoding,
        sheet_json=sheet_json,
    )
    return {enc: label for enc, (label, _refs) in anchors.items()}


def build_affine_preset_anchors(
    sysex_root: Path,
    offsets: Sequence[int],
    *,
    encoding: str,
    scale: float,
    offset: float = 0.0,
    skip_encodings: Sequence[int] | None = None,
) -> PresetAnchors:
    """Affine anchors from factory dumps: encoding → (label, presets)."""
    offsets = tuple(offsets)
    if not offsets:
        return {}

    presets_dir = prog_presets_root(sysex_root)
    if not presets_dir.is_dir():
        return {}

    skip = {int(e) for e in (skip_encodings or ())}
    scale_f = float(scale)
    add = float(offset)
    by_enc: dict[int, list[tuple[str, str]]] = {}

    for path in sorted(presets_dir.glob("*.syx")):
        raw = path.read_bytes()
        identity = validate_preset_dump(path, raw)
        try:
            enc = int(decode_at_offsets(raw, offsets, encoding).value)
        except (ValueError, IndexError):
            continue
        if enc in skip:
            continue
        by_enc.setdefault(enc, []).append((identity["bank"], identity["preset"]))

    return {
        enc: (enc * scale_f + add, sorted(set(refs)))
        for enc, refs in sorted(by_enc.items())
    }


def build_affine_preset_mapping(
    sysex_root: Path,
    offsets: Sequence[int],
    *,
    encoding: str,
    scale: float,
    offset: float = 0.0,
    skip_encodings: Sequence[int] | None = None,
) -> dict[int, float]:
    """Map encodings seen in ``_presets`` via a closed-form affine label."""
    anchors = build_affine_preset_anchors(
        sysex_root,
        offsets,
        encoding=encoding,
        scale=scale,
        offset=offset,
        skip_encodings=skip_encodings,
    )
    return {enc: label for enc, (label, _refs) in anchors.items()}


def densify_encoding_map(
    series: dict[int, float],
    preset: dict[int, float] | None = None,
    *,
    provided: dict[int, float] | None = None,
    inferred: dict[int, float] | None = None,
    unit: str | None = None,
    preset_refs: dict[int, list[tuple[str, str]]] | None = None,
) -> list[dict[str, Any]]:
    """Merge capture-dump + provided + inferred + preset anchors into encoding-map rows.

    Label priority when multiple witnesses disagree on the **numeric label**:
    **dump** > **provided** > **inferred** > **preset**. Source lists every witness.

    Returns rows sorted by encoded value:
    ``{encoded, label, source, sources[, preset_refs]}`` where ``sources`` is
    an ordered list of ``dump`` / ``provided`` / ``inferred`` / ``preset``, and
    ``source`` is the primary (first) entry for compatibility.
    """
    refs_by_enc = {
        int(enc): list(refs) for enc, refs in (preset_refs or {}).items()
    }
    dump_labels = {int(enc): float(label) for enc, label in series.items()}
    provided_labels = {
        int(enc): float(label) for enc, label in (provided or {}).items()
    }
    inferred_labels = {
        int(enc): float(label) for enc, label in (inferred or {}).items()
    }
    preset_labels = {
        int(enc): float(label) for enc, label in (preset or {}).items()
    }
    known_encs = sorted(
        set(dump_labels)
        | set(provided_labels)
        | set(inferred_labels)
        | set(preset_labels)
    )
    if not known_encs:
        return []

    rows: list[dict[str, Any]] = []
    for enc in known_encs:
        sources: list[str] = []
        label: float | None = None
        if enc in dump_labels:
            label = dump_labels[enc]
            sources.append("dump")
        if enc in provided_labels:
            if label is None:
                label = provided_labels[enc]
            sources.append("provided")
        if enc in inferred_labels:
            if label is None:
                label = inferred_labels[enc]
            sources.append("inferred")
        if enc in preset_labels:
            if label is None:
                label = preset_labels[enc]
            sources.append("preset")
        assert label is not None and sources
        row: dict[str, Any] = {
            "encoded": enc,
            "label": _tidy_label(label, unit),
            "source": sources[0],
            "sources": list(sources),
        }
        if "preset" in sources and enc in refs_by_enc:
            row["preset_refs"] = refs_by_enc[enc]
        rows.append(row)
    return rows



def _tidy_label(value: float, unit: str | None) -> float | int:
    """Round interpolated / sheet values for stable table display."""
    if unit == "db":
        # Wet gain and similar controls use 0.5 dB steps between off/full.
        half = round(value * 2) / 2
        if abs(value - half) < 1e-9:
            if half == int(half):
                return int(half)
            return half
        return int(round(value))
    if unit in {"ms", "hz"}:
        return int(round(value))
    if unit == "s":
        return round(value, 2)
    if abs(value - round(value)) < 1e-9:
        return int(round(value))
    rounded = round(value, 6)
    if abs(rounded - round(rounded, 2)) < 1e-9:
        return round(rounded, 2)
    return rounded


def pack_encoded_bytes(encoded: int, encoding: str, n_offsets: int) -> list[str]:
    """Pack an encoded integer into hex SysEx data-byte strings for docs."""
    from ..encodings import encode_at_offsets

    return [f"{b:02X}" for b in encode_at_offsets(encoded, encoding, n_offsets)]
