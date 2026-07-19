"""Decode known sound-parameter values out of a full program-dump message.

Uses per-parameter ``analysis.json`` / export results (offsets, encoding, scale
or sparse table mapping) to interpret factory/user presets in
``sysex/prog/presets/``.

Parameters still missing a dedicated capture series may also be filled from
``preset_inferred`` (factory dumps × published preset sheet).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..encodings import decode_at_offsets
from ..labels import format_value_with_unit
from .preset_inferred import (
    build_sheet_mode_mapping,
    merge_inferred_mapping,
    preset_inferred_decoders,
)
from .provided import provided_mapping_for
from .names import validate_preset_dump


# Display order matching the M7 program-parameter menu / catalog.
PARAMETER_ORDER = (
    "reverb time",
    "size",
    "predelay",
    "diffusion",
    "density",
    "modulation",
    "rolloff",
    "hf rt multiply",
    "hf rt crossover",
    "lf rt multiply",
    "lf rt crossover",
    "vlf cut",
    "early to reverb mix",
    "early rolloff",
    "early select",
    "delay level",
    "delay time",
    "delay modulation",
)

# Short headers for the cross-preset summary matrix.
SHORT_NAMES = {
    "reverb time": "RT",
    "size": "Size",
    "predelay": "PreDly",
    "diffusion": "Diff",
    "density": "Dens",
    "modulation": "Mod",
    "rolloff": "Roll",
    "hf rt multiply": "HFmpy",
    "hf rt crossover": "HFxo",
    "lf rt multiply": "LFmpy",
    "lf rt crossover": "LFxo",
    "vlf cut": "VLF",
    "early to reverb mix": "E/R",
    "early rolloff": "ERoll",
    "early select": "ESel",
    "delay level": "DlyLvl",
    "delay time": "DlyTim",
    "delay modulation": "DlyMod",
}


def enrich_names_with_parameters(
    names: dict[str, Any],
    parameter_results: list[dict[str, Any]],
) -> dict[str, Any]:
    """Attach decoded parameter values to each preset dump in-place."""
    folder = Path(names["folder"])
    from ..paths import corpus_sysex_root

    sysex_root = corpus_sysex_root(folder)
    decoders = build_parameter_decoders(parameter_results, sysex_root=sysex_root)
    for dump in names.get("dumps") or []:
        path = folder / dump["file"]
        if not path.is_file():
            dump["parameters"] = {}
            dump["parameters_note"] = f"missing file {path.name}"
            continue
        raw = path.read_bytes()
        validate_preset_dump(path, raw)
        decoded = decode_dump_parameters(raw, decoders)
        dump["parameters"] = {
            name: {
                "display": row["display"],
                "value": row.get("value"),
                "encoded": row["encoded"],
                "approx": row.get("approx", False),
                "unit": row.get("unit"),
            }
            for name, row in decoded.items()
        }
    names["parameter_decoders"] = [
        {
            "parameter": d["parameter"],
            "offsets": d["offsets"],
            "encoding": d["encoding"],
            "kind": d["kind"],
            "unit": d.get("unit"),
            "source": d.get("source", "series"),
            "confidence": d.get("confidence"),
            "notes": d.get("notes"),
            "scale": d.get("scale"),
            "offset": d.get("offset"),
            "mapping": d.get("mapping") or {},
        }
        for d in decoders
    ]
    names["parameters_decoded"] = True
    return names


def build_parameter_decoders(
    parameter_results: list[dict[str, Any]],
    *,
    sysex_root: Path | None = None,
) -> list[dict[str, Any]]:
    """Build decode specs from series analysis, plus sheet densify points."""
    by_name = {r["parameter"]: r for r in parameter_results}
    inferred = {
        d["parameter"]: d
        for d in preset_inferred_decoders(sysex_root=sysex_root)
    }
    decoders: list[dict[str, Any]] = []
    for name in PARAMETER_ORDER:
        result = by_name.get(name)
        if result:
            best = result.get("best_encoding")
            if best and best.get("offsets"):
                spec = _decoder_from_series(name, result, best)
                # Sparse series tables gain sheet-derived points between the
                # captured anchors (series values win on conflict). Prefer the
                # dedicated LF-RT inferred decoder when present; otherwise pull
                # a live sheet map for any table parameter.
                dump_keys = set(spec.get("mapping") or {})
                densify = inferred.get(name)
                if densify is None and sysex_root is not None and spec["kind"] == "table":
                    sheet_map = build_sheet_mode_mapping(
                        sysex_root,
                        name,
                        spec["offsets"],
                        encoding=spec["encoding"],
                    )
                    if sheet_map:
                        densify = {
                            "offsets": list(spec["offsets"]),
                            "encoding": spec["encoding"],
                            "mapping": sheet_map,
                        }
                spec = merge_inferred_mapping(spec, densify)
                # Hardware UI walks beat sheet/preset fills; series dumps win.
                if sysex_root is not None and spec["kind"] == "table":
                    provided = provided_mapping_for(name, sysex_root=sysex_root)
                    if provided:
                        mapping = {
                            int(k): float(v)
                            for k, v in (spec.get("mapping") or {}).items()
                        }
                        full_enc = spec.get("full_encoded")
                        for enc, label in provided.items():
                            enc_i = int(enc)
                            if enc_i in dump_keys:
                                continue
                            # Keep Full as a discrete endpoint, not 22000 Hz.
                            if full_enc is not None and enc_i == int(full_enc):
                                continue
                            mapping[enc_i] = float(label)
                        spec["mapping"] = dict(sorted(mapping.items()))
                        sources = list(spec.get("mapping_sources") or ["series"])
                        if "provided" not in sources:
                            sources.append("provided")
                        spec["mapping_sources"] = sources
                decoders.append(spec)
                continue
        if name in inferred:
            decoders.append(dict(inferred[name]))
    return decoders


def _decoder_from_series(
    name: str,
    result: dict[str, Any],
    best: dict[str, Any],
) -> dict[str, Any]:
    kind = "affine" if best.get("exact") and best.get("scale") is not None else "table"
    notes = best.get("notes") or ""
    if best.get("scale") is not None and "table/index" not in notes:
        kind = "affine"
    if "table/index" in notes:
        kind = "table"

    mapping = {
        int(row["encoded"]): row["label"]
        for row in (best.get("mapping") or [])
        if "encoded" in row and "label" in row
    }
    value_range = result.get("value_range") or {}
    balance = value_range.get("balance") or {}
    sampling = result.get("sampling") or {}
    extreme_high = (
        ((sampling.get("edge_steps") or {}).get("points") or {}).get("extreme_high")
        or {}
    )
    full_encoded = None
    if (
        extreme_high.get("endpoint") == "high"
        and str(extreme_high.get("file") or "").lower().startswith("full.")
        and extreme_high.get("encoded") is not None
    ):
        full_encoded = int(extreme_high["encoded"])
    return {
        "parameter": name,
        "offsets": list(best["offsets"]),
        "encoding": best["encoding"],
        "kind": kind,
        "scale": best.get("scale"),
        "offset": best.get("offset"),
        "mapping": mapping,
        "unit": result.get("unit"),
        "has_off": bool(value_range.get("off")),
        "balance_side_max": balance.get("side_max"),
        "observed_min": value_range.get("min"),
        "observed_max": value_range.get("max"),
        "full_encoded": full_encoded,
        "source": "series",
        "confidence": (result.get("hypothesis") or {}).get("confidence"),
    }


def decode_dump_parameters(
    raw: bytes,
    decoders: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Decode every known parameter from one program-dump blob."""
    out: dict[str, dict[str, Any]] = {}
    for spec in decoders:
        name = spec["parameter"]
        field = decode_at_offsets(raw, spec["offsets"], spec["encoding"])
        encoded = int(field.value)
        value, approx = _encoded_to_label(encoded, spec)
        display = _format_display(name, value, encoded, approx, spec)
        out[name] = {
            "encoded": encoded,
            "value": value,
            "approx": approx and str(display).startswith("~"),
            "display": display,
            "unit": spec.get("unit"),
            "offsets": spec["offsets"],
        }
    return out


def _encoded_to_label(
    encoded: int,
    spec: dict[str, Any],
) -> tuple[float | int | None, bool]:
    if spec["kind"] == "affine":
        scale = float(spec["scale"] if spec["scale"] is not None else 1.0)
        add = float(spec["offset"] if spec["offset"] is not None else 0.0)
        value = encoded * scale + add
        if float(value).is_integer() and scale == int(scale) and add == int(add):
            return int(value), False
        # Keep one or two decimals for multiply / seconds-ish values.
        rounded = round(value, 6)
        if abs(rounded - round(rounded, 2)) < 1e-9:
            rounded = round(rounded, 2)
        return rounded, False

    mapping: dict[int, float] = spec.get("mapping") or {}
    if encoded in mapping:
        label = mapping[encoded]
        if float(label).is_integer():
            return int(label), False
        return label, False

    if not mapping:
        return None, True

    keys = sorted(mapping)
    if encoded < keys[0] or encoded > keys[-1]:
        return None, True
    for i in range(len(keys) - 1):
        e0, e1 = keys[i], keys[i + 1]
        if e0 <= encoded <= e1:
            if e0 == e1:
                return mapping[e0], False
            t = (encoded - e0) / (e1 - e0)
            v = mapping[e0] + t * (mapping[e1] - mapping[e0])
            unit = spec.get("unit")
            if unit == "s":
                return round(v, 2), True
            if unit in {"ms", "hz", "db"}:
                return int(round(v)), True
            if float(mapping[e0]).is_integer() and float(mapping[e1]).is_integer():
                return int(round(v)), True
            return round(v, 3), True
    return None, True


def _format_display(
    name: str,
    value: float | int | None,
    encoded: int,
    approx: bool,
    spec: dict[str, Any],
) -> str:
    unit = spec.get("unit")

    # Discrete off endpoints (modulation family, delay level).
    if spec.get("has_off") and encoded == 0:
        return "off"

    # Rolloff / early rolloff hardware max past the last Hz step.
    full_enc = spec.get("full_encoded")
    if full_enc is not None and encoded == int(full_enc):
        return "full"

    if name == "size":
        if encoded == 0:
            return "small"
        obs_max = spec.get("observed_max")
        if obs_max is not None and encoded == int(obs_max):
            return "large"
        return str(int(value) if value is not None else encoded)

    if name in {"modulation", "delay modulation"}:
        if value is not None and int(value) == 0 and encoded == 1:
            return "low"
        obs_max = spec.get("observed_max")
        if (
            value is not None
            and obs_max is not None
            and int(value) == int(obs_max)
        ):
            return "high"
        if value is not None:
            return str(int(value))

    if name == "early to reverb mix" and value is not None:
        from ..labels import format_balance_pair

        side = int(spec.get("balance_side_max") or 20)
        pos = int(value)
        a, b = _balance_pair(pos, side)
        return format_balance_pair(a, b)

    if value is None:
        return f"idx {encoded}"

    text = format_value_with_unit(value, unit)
    # format_value_with_unit already appends unit display; for bare numbers without
    # unit it returns the number. Prefix approx for interpolated table hits.
    if approx:
        return f"~{text}"
    return text


def _balance_pair(position: int, side_max: int) -> tuple[int, int]:
    """Invert L-path position 0..2M back to A/B display pair."""
    if position <= side_max:
        return position, side_max
    return side_max, side_max - (position - side_max)


def short_name(parameter: str) -> str:
    return SHORT_NAMES.get(parameter, parameter)
