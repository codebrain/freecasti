"""Emit a codegen-ready Bricasti M7 program-dump byte spec (JSON + Kaitai).

The Markdown byte-map pages are a human view. This module builds a machine
schema from ``byte_map`` + per-parameter analysis encodings, then renders:

* ``m7_program_dump.spec.json`` — intermediate schema (other generators)
* ``m7_program_dump.ksy`` — `Kaitai Struct <https://kaitai.io/>`_ layout

Neither file is an official Bricasti specification; both are regenerated from
captures on each export.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from ..frame import (
    BRICASTI_MFR_ID,
    CHECKSUM_COVER_START,
    CHECKSUM_NIBBLE_COUNT,
    NAME_OFFSET,
    PROGRAM_DUMP_HEADER,
    PROGRAM_NAME_LENGTH,
    REGISTER_BASIS_BLOB_LENGTH,
    REGISTER_BASIS_BLOB_OFFSET,
    SYSEX_END,
    SYSEX_START,
)
from ..kaitai_render import render_kaitai_yaml
from ..kaitai_value_maps import attach_parameter_value_maps

SPEC_JSON_NAME = "m7_program_dump.spec.json"
KAITAI_NAME = "m7_program_dump.ksy"
SPEC_FORMAT = "bricasti-m7-program-dump"
SPEC_VERSION = 1


def build_program_dump_spec(
    byte_map: dict[str, Any],
    results: list[dict[str, Any]] | None = None,
    *,
    names: dict[str, Any] | None = None,
    menus_analysis: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an ordered field schema for the 157-byte program dump."""
    from .byte_map import _overview_label
    from .catalog import lookup_parameter

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
            p
            for p in (region.get("parameters") or [])
            if p not in {"_presets", "_corpus", "_menus"}
        ]
        label, encoding = _overview_label(region, byte_map)
        if not encoding and 0 <= start < len(bytes_):
            encoding = bytes_[start].get("encoding")

        # Secondary movers list the series that touched them — that is not the
        # primary sound-parameter field (those claim status=known elsewhere).
        sound = params[0] if params and status == "known" else None
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
        }
        if sound:
            field["parameter"] = sound
            catalog = lookup_parameter(sound)
            if catalog:
                if catalog.get("unit"):
                    field["unit"] = catalog["unit"]
                if catalog.get("description"):
                    field["description"] = catalog["description"]
            if best:
                if best.get("exact") and best.get("scale") is not None:
                    field["kind"] = "affine"
                    field["scale"] = best.get("scale")
                    field["offset"] = best.get("offset")
                else:
                    field["kind"] = "table"
                if best.get("notes"):
                    field["encoding_notes"] = best["notes"]
                conf = ((analysis or {}).get("hypothesis") or {}).get(
                    "confidence"
                )
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
            field["contents"] = list(PROGRAM_DUMP_HEADER)
            field["id"] = _force_id("program_dump_header", used_ids, field_id)
        elif start == NAME_OFFSET and size == PROGRAM_NAME_LENGTH:
            field["kind"] = "string"
            field["encoding"] = "ascii_space_padded"
            field["id"] = _force_id("program_name", used_ids, field_id)
        elif (
            start == REGISTER_BASIS_BLOB_OFFSET
            and size == REGISTER_BASIS_BLOB_LENGTH
        ):
            field["kind"] = "meta"
            field["encoding"] = "raw_bytes"
            field["id"] = _force_id("register_basis_blob", used_ids, field_id)
        elif start == 93 and size == 1:
            field["id"] = _force_id("register_page", used_ids, field_id)
        elif start == 94 and size == 1:
            field["id"] = _force_id("structure_version", used_ids, field_id)
        elif start == 95 and size == 1:
            field["id"] = _force_id("register_slot", used_ids, field_id)
        elif status == "checksum":
            field["id"] = _force_id("checksum", used_ids, field_id)
        elif start == length - 1 and size == 1:
            field["contents"] = [SYSEX_END]
            field["id"] = _force_id("sysex_end", used_ids, field_id)
        elif start == 146 and size == 2:
            field["id"] = _force_id("display", used_ids, field_id)

        fields.append(field)

    attach_parameter_value_maps(fields, results)
    from ..kaitai_value_maps import attach_display_value_map

    attach_display_value_map(fields, menus_analysis)

    covered = 0
    for f in fields:
        if f["start"] != covered:
            raise ValueError(
                f"byte-spec gap/overlap at offset {covered} "
                f"(next field {f['id']} starts at {f['start']})"
            )
        covered = f["end"] + 1
    if covered != length:
        raise ValueError(
            f"byte-spec covers {covered} bytes, expected {length}"
        )

    return {
        "format": SPEC_FORMAT,
        "version": SPEC_VERSION,
        "kaitai_id": KAITAI_NAME.removesuffix(".ksy"),
        "title": "Bricasti M7 program-dump SysEx",
        "message_length": length,
        "file_extension": "syx",
        "disclaimer": (
            "Reverse-engineered from labeled captures in this repository. "
            "Not an official Bricasti specification. Dump-derived encodings "
            "and offsets are authoritative for this corpus."
        ),
        "kaitai_doc_extra": (
            "Sound-parameter value maps (affine scales / sparse tables) live "
            "alongside this layout in the companion .spec.json and in "
            "specification/prog/bytes/."
        ),
        "frame": {
            "sysex_start": SYSEX_START,
            "manufacturer_id": list(BRICASTI_MFR_ID),
            "program_dump_header": list(PROGRAM_DUMP_HEADER),
            "program_name": {
                "offset": NAME_OFFSET,
                "length": PROGRAM_NAME_LENGTH,
                "encoding": "ascii_space_padded",
            },
            "register_basis_blob": {
                "offset": REGISTER_BASIS_BLOB_OFFSET,
                "length": REGISTER_BASIS_BLOB_LENGTH,
                "encoding": "raw_bytes",
            },
            "sysex_end": SYSEX_END,
        },
        "checksum": {
            "offsets": list(
                range(checksum_start, checksum_start + CHECKSUM_NIBBLE_COUNT)
            ),
            "algorithm": "CRC-16/ARC",
            "also_known_as": ["CRC-16/IBM", "CRC-16/ANSI"],
            "poly": "0x8005",
            "init": "0x0000",
            "refin": True,
            "refout": True,
            "xorout": "0x0000",
            "cover_start": CHECKSUM_COVER_START,
            "cover_end_exclusive": checksum_start,
            "pack": "u16_be_high_nibble_first",
            "doc": (
                "CRC-16/ARC over raw SysEx bytes [8, checksum_start), packed "
                "as four high-nibble-first MIDI data bytes. Manufacturer ID "
                "and header are not covered."
            ),
        },
        "encodings": {
            "raw_u8": "Single SysEx data byte used as an unsigned integer.",
            "nibble_hilo": (
                "Two MIDI data bytes (each 0x00-0x0F); value = (hi<<4)|lo."
            ),
            "ascii_space_padded": (
                "ASCII text, space-padded on the right to a fixed width."
            ),
            "raw_bytes": (
                "Opaque multi-byte region copied as-is (no scalar decode)."
            ),
            "crc16_arc_u16_be_nibbles": (
                "CRC-16/ARC packed as four high-nibble-first SysEx bytes."
            ),
        },
        "fields": fields,
        "sources": {
            "byte_map_regions": len(regions),
            "parameter_series": len(by_param),
            "has_presets": names is not None,
        },
    }


def write_program_dump_spec(
    output_dir: Path,
    byte_map: dict[str, Any],
    results: list[dict[str, Any]] | None = None,
    *,
    names: dict[str, Any] | None = None,
    menus_analysis: dict[str, Any] | None = None,
) -> tuple[Path, Path, dict[str, Any]]:
    """Write ``.spec.json`` and ``.ksy`` under ``output_dir``.

    Returns ``(json_path, ksy_path, spec)``.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    spec = build_program_dump_spec(
        byte_map, results, names=names, menus_analysis=menus_analysis
    )
    json_path = output_dir / SPEC_JSON_NAME
    ksy_path = output_dir / KAITAI_NAME
    json_path.write_text(
        json.dumps(spec, indent=2) + "\n", encoding="utf-8"
    )
    ksy_path.write_text(render_kaitai_yaml(spec), encoding="utf-8")
    return json_path, ksy_path, spec


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
    """Replace ``previous`` in ``used`` with a canonical frame/checksum id."""
    used.discard(previous)
    if desired in used:
        return _unique_id(desired, 0, used)
    used.add(desired)
    return desired
