"""Emit a codegen-ready Bricasti M7 system-dump byte spec (JSON + Kaitai)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from ..frame import (
    BRICASTI_MFR_ID,
    CHECKSUM_NIBBLE_COUNT,
    SYSTEM_CHECKSUM_COVER_END,
    SYSTEM_CHECKSUM_COVER_START,
    SYSTEM_DUMP_HEADER,
    SYSEX_END,
    SYSEX_START,
)
from ..kaitai_render import render_kaitai_yaml
from ..kaitai_value_maps import attach_parameter_value_maps
from .byte_map import _overview_label
from .catalog import lookup_system_parameter

SPEC_JSON_NAME = "m7_system_dump.spec.json"
KAITAI_NAME = "m7_system_dump.ksy"
SPEC_FORMAT = "bricasti-m7-system-dump"
SPEC_VERSION = 1


def build_system_dump_spec(
    byte_map: dict[str, Any],
    results: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build an ordered field schema for the 77-byte system dump."""
    length = int(byte_map["message_length"])
    bytes_ = byte_map.get("bytes") or []
    regions = byte_map.get("regions") or []
    by_param = {
        r["parameter"]: r for r in (results or []) if r.get("parameter")
    }

    checksum_start = length - 1 - CHECKSUM_NIBBLE_COUNT
    fields: list[dict[str, Any]] = []
    used_ids: set[str] = set()

    for region in regions:
        start = int(region["start"])
        end = int(region["end"])
        size = int(region["length"])
        status = region.get("status") or "unknown"
        role = region.get("role") or ""
        params = [
            p for p in (region.get("parameters") or []) if p not in {"_corpus"}
        ]
        label, encoding = _overview_label(region, byte_map)
        if not encoding and 0 <= start < len(bytes_):
            encoding = bytes_[start].get("encoding")

        sound = (
            _primary_parameter_for_region(params, start, by_param)
            if params and status == "known"
            else None
        )
        analysis = by_param.get(sound) if sound else None
        best = (analysis or {}).get("best_encoding") or {}
        if sound and best.get("encoding"):
            encoding = best["encoding"]

        field_id = _unique_id(_slug_id(sound or label), start, used_ids)
        field: dict[str, Any] = {
            "id": field_id,
            "label": sound or label,
            "offsets": list(range(start, end + 1)),
            "start": start,
            "end": end,
            "size": size,
            "status": status,
            "role": role,
            "encoding": encoding,
            "series_root": "sysex/system",
        }
        if sound:
            field["parameter"] = sound
            catalog = lookup_system_parameter(sound)
            if catalog:
                if catalog.get("description"):
                    field["description"] = catalog["description"]
                if catalog.get("notes"):
                    field["encoding_notes"] = catalog["notes"]
            if best:
                if best.get("exact") and best.get("scale") is not None:
                    field["kind"] = "affine"
                    field["scale"] = best.get("scale")
                    field["offset"] = best.get("offset")
                else:
                    field["kind"] = "table"
                conf = ((analysis or {}).get("hypothesis") or {}).get("confidence")
                if conf:
                    field["confidence"] = conf
        elif status == "checksum":
            field["kind"] = "checksum"
            field["encoding"] = "crc16_arc_u16_be_nibbles"
        elif status == "frame":
            field["kind"] = "frame"
        elif status == "secondary":
            field["kind"] = "secondary"
        else:
            field["kind"] = "meta"

        if start == 0 and size == 1:
            field["contents"] = [SYSEX_START]
            field["id"] = _force_id("sysex_start", used_ids, field_id)
        elif start == 1 and size == 3:
            field["contents"] = list(BRICASTI_MFR_ID)
            field["id"] = _force_id("manufacturer_id", used_ids, field_id)
        elif start == 4 and size == 4:
            field["contents"] = list(SYSTEM_DUMP_HEADER)
            field["id"] = _force_id("system_dump_header", used_ids, field_id)
        elif status == "checksum":
            field["id"] = _force_id("checksum", used_ids, field_id)
        elif start == length - 1 and size == 1:
            field["contents"] = [SYSEX_END]
            field["id"] = _force_id("sysex_end", used_ids, field_id)

        fields.append(field)

    attach_parameter_value_maps(fields, results)

    covered = 0
    for f in fields:
        if f["start"] != covered:
            raise ValueError(
                f"byte-spec gap/overlap at offset {covered} "
                f"(next field {f['id']} starts at {f['start']})"
            )
        covered = f["end"] + 1
    if covered != length:
        raise ValueError(f"byte-spec covers {covered} bytes, expected {length}")

    return {
        "format": SPEC_FORMAT,
        "version": SPEC_VERSION,
        "kaitai_id": KAITAI_NAME.removesuffix(".ksy"),
        "title": "Bricasti M7 system-dump SysEx",
        "message_length": length,
        "file_extension": "syx",
        "disclaimer": (
            "Reverse-engineered from labeled system captures in this repository. "
            "Not an official Bricasti specification."
        ),
        "kaitai_doc_extra": (
            "System-parameter encodings are documented in "
            "specification/system/parameters/."
        ),
        "frame": {
            "sysex_start": SYSEX_START,
            "manufacturer_id": list(BRICASTI_MFR_ID),
            "system_dump_header": list(SYSTEM_DUMP_HEADER),
            "sysex_end": SYSEX_END,
        },
        "checksum": {
            "offsets": list(
                range(checksum_start, checksum_start + CHECKSUM_NIBBLE_COUNT)
            ),
            "algorithm": "CRC-16/ARC",
            "cover_start": SYSTEM_CHECKSUM_COVER_START,
            "cover_end_exclusive": SYSTEM_CHECKSUM_COVER_END,
            "pack": "u16_be_high_nibble_first",
        },
        "encodings": {
            "raw_u8": "Single SysEx data byte used as an unsigned integer.",
            "nibble_hilo": (
                "Two MIDI data bytes (each 0x00-0x0F); value = (hi<<4)|lo."
            ),
            "crc16_arc_u16_be_nibbles": (
                "CRC-16/ARC packed as four high-nibble-first SysEx bytes."
            ),
        },
        "fields": fields,
        "sources": {
            "byte_map_regions": len(regions),
            "system_series": len(by_param),
        },
    }


def write_system_dump_spec(
    output_dir: Path,
    byte_map: dict[str, Any],
    results: list[dict[str, Any]] | None = None,
) -> tuple[Path, Path, dict[str, Any]]:
    """Write ``.spec.json`` and ``.ksy`` under ``output_dir``."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    spec = build_system_dump_spec(byte_map, results)
    json_path = output_dir / SPEC_JSON_NAME
    ksy_path = output_dir / KAITAI_NAME
    json_path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    ksy_path.write_text(render_kaitai_yaml(spec), encoding="utf-8")
    return json_path, ksy_path, spec


def _primary_parameter_for_region(
    params: list[str],
    start: int,
    by_param: dict[str, dict[str, Any]],
) -> str:
    """Prefer the series whose primary encoding offsets include ``start``."""
    primaries: list[str] = []
    for name in params:
        analysis = by_param.get(name) or {}
        offsets = (analysis.get("best_encoding") or {}).get("offsets") or []
        if start in offsets:
            primaries.append(name)
    return primaries[0] if primaries else params[0]


def _slug_id(label: str) -> str:
    text = label.strip().casefold()
    text = text.replace("/", " ")
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "field"


def _unique_id(base: str, start: int, used: set[str]) -> str:
    candidate = base
    if candidate in used or not candidate:
        candidate = f"{base}_{start}" if base else f"field_{start}"
    n = 2
    while candidate in used:
        candidate = f"{base}_{start}_{n}"
        n += 1
    used.add(candidate)
    return candidate


def _force_id(desired: str, used: set[str], previous: str) -> str:
    used.discard(previous)
    if desired in used:
        return _unique_id(desired, 0, used)
    used.add(desired)
    return desired
