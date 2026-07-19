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
    PROGRAM_NAME_EDITABLE_LENGTH,
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
        elif start == NAME_OFFSET and size == PROGRAM_NAME_EDITABLE_LENGTH:
            field["kind"] = "string"
            field["encoding"] = "ascii_space_padded"
            field["id"] = _force_id("program_name", used_ids, field_id)
        elif (
            start == NAME_OFFSET + PROGRAM_NAME_EDITABLE_LENGTH
            and size == PROGRAM_NAME_LENGTH - PROGRAM_NAME_EDITABLE_LENGTH
        ):
            field["kind"] = "meta"
            field["encoding"] = "raw_bytes"
            field["id"] = _force_id("program_name_pad", used_ids, field_id)
        elif (
            start == REGISTER_BASIS_BLOB_OFFSET
            and size == REGISTER_BASIS_BLOB_LENGTH
        ):
            field["kind"] = "meta"
            field["encoding"] = "raw_bytes"
            field["id"] = _force_id("register_basis_blob", used_ids, field_id)
        elif start == 93 and size == 1:
            field["id"] = _force_id("register_bank", used_ids, field_id)
        elif start == 94 and size == 1:
            field["id"] = _force_id("structure_version", used_ids, field_id)
        elif start == 95 and size == 1:
            field["id"] = _force_id("register", used_ids, field_id)
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
    _attach_register_blob_type(fields)

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
                "length": PROGRAM_NAME_EDITABLE_LENGTH,
                "wire_window_length": PROGRAM_NAME_LENGTH,
                "encoding": "ascii_space_padded",
                "doc": (
                    f"{PROGRAM_NAME_EDITABLE_LENGTH}-character editable label "
                    f"(manual) inside a {PROGRAM_NAME_LENGTH}-byte wire window; "
                    "trailing two bytes are program_name_pad"
                ),
            },
            "program_name_pad": {
                "offset": NAME_OFFSET + PROGRAM_NAME_EDITABLE_LENGTH,
                "length": PROGRAM_NAME_LENGTH - PROGRAM_NAME_EDITABLE_LENGTH,
                "encoding": "raw_bytes",
                "doc": "Trailing space pad completing the 16-byte wire name window",
            },
            "register_basis_blob": {
                "offset": REGISTER_BASIS_BLOB_OFFSET,
                "length": REGISTER_BASIS_BLOB_LENGTH,
                "encoding": "raw_bytes",
                "doc": (
                    "Factory dumps: 0x20 space pad. Reg-backed hold-EDIT "
                    "dumps: bit-packed stored-register snapshot decoded by "
                    "the register_basis_blob type value instances"
                ),
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


def _blob_bit_expr(bit_offset: int, bit_width: int) -> str:
    """Kaitai expression extracting a bitfield from the blob nibble stream.

    The logical stream is the low nibble of each ``data`` byte, MSB first.
    Expressions stay within 32-bit shifts so compiled JS parsers are safe.
    """
    first = bit_offset // 4
    last = (bit_offset + bit_width - 1) // 4
    parts: list[str] = []
    for idx in range(first, last + 1):
        shift = 4 * (last - idx)
        term = f"(data[{idx}] & 0x0f)"
        if shift:
            term = f"({term} << {shift})"
        parts.append(term)
    combined = parts[0] if len(parts) == 1 else "(" + " | ".join(parts) + ")"
    drop = (last + 1) * 4 - (bit_offset + bit_width)
    if drop:
        combined = f"({combined} >> {drop})"
    lead = bit_offset - first * 4
    if lead:
        mask = (1 << bit_width) - 1
        combined = f"{combined} & 0x{mask:x}"
    return combined


def _attach_register_blob_type(fields: list[dict[str, Any]]) -> None:
    """Attach the nested register_basis_blob Kaitai type to the blob field.

    Every value instance is generated from ``REGISTER_BLOB_FIELDS`` in
    ``m7_sysex.prog.register_blob`` (single source of truth). Stored
    parameters reuse the same enums as their live payload twins.
    """
    from .register_blob import (
        REGISTER_BASIS_BLOB_LENGTH,
        REGISTER_BLOB_FIELDS,
        REGISTER_NAME_CHARSET,
        REGISTER_NAME_CHAR_BITS,
        REGISTER_NAME_LENGTH,
        register_name_char_enum_entries,
    )

    blob_field = next(
        (f for f in fields if f["id"] == "register_basis_blob"), None
    )
    if blob_field is None:
        return
    enum_by_payload_id = {
        f["id"]: f["value_map"]["enum_id"]
        for f in fields
        if f.get("value_map")
    }

    instances: list[dict[str, Any]] = [
        {
            "id": "is_register_basis",
            "value": "((data[0] | data[1] | data[2] | data[3]) & 0xf0) == 0",
            "doc": (
                "True when 24-87 is a nibble-packed stored-register "
                "snapshot; false on factory / parameter-series dumps "
                "(space pad 0x20). Check before reading other instances."
            ),
        }
    ]
    for i in range(REGISTER_NAME_LENGTH):
        instances.append(
            {
                "id": f"name_code_{i:02d}",
                "value": _blob_bit_expr(
                    i * REGISTER_NAME_CHAR_BITS, REGISTER_NAME_CHAR_BITS
                ),
                "enum": "register_name_char",
                "doc": (
                    f"Register name character {i + 1} of "
                    f"{REGISTER_NAME_LENGTH} (6-bit code, space padded; "
                    "witness: samples/charset-b1s1-renamed.syx)"
                ),
            }
        )
    tail = None
    for field in REGISTER_BLOB_FIELDS:
        if field.id == "name":
            continue
        if field.id == "tail":
            tail = field
            continue
        inst: dict[str, Any] = {
            "id": field.id,
            "value": _blob_bit_expr(field.bit_offset, field.bit_width),
            "bit_offset": field.bit_offset,
            "bit_width": field.bit_width,
        }
        doc = field.doc or f"Stored {field.label}"
        if field.payload_field:
            offs = list(field.payload_offsets)
            off_txt = (
                f"{offs[0]}-{offs[-1]}" if len(offs) > 1 else str(offs[0])
            )
            doc = (
                f"Stored {field.label} (bits {field.bit_offset}-"
                f"{field.bit_end}); equals live payload field "
                f"{field.payload_field} @ {off_txt} unless the register "
                "has unstored edits"
            )
            if field.doc:
                doc += ". " + field.doc
            enum_id = enum_by_payload_id.get(field.payload_field)
            if enum_id:
                inst["enum"] = enum_id
        inst["doc"] = doc
        instances.append(inst)
    if tail is not None:
        first = tail.bit_offset // 4
        last = tail.bit_end // 4
        ored = " | ".join(f"data[{i}]" for i in range(first, last + 1))
        instances.append(
            {
                "id": "tail_is_zero",
                "value": f"(({ored}) & 0x0f) == 0",
                "doc": (
                    f"Zero tail (bits {tail.bit_offset}-{tail.bit_end}); "
                    "always true in witnessed captures"
                ),
            }
        )

    blob_field["type_ref"] = "register_basis_blob"
    blob_field["blob"] = {
        "type_id": "register_basis_blob",
        "size": REGISTER_BASIS_BLOB_LENGTH,
        "doc": (
            "Bit-packed snapshot of the stored register (Reg-backed "
            "hold-EDIT dumps); factory dumps space-pad this region with "
            "0x20 - check is_register_basis before reading instances. The "
            "low nibble of each byte forms a 256-bit stream (4 bits per "
            "byte, MSB first): 14x6-bit name, store-generation counter, "
            "all 18 parameters incl. the V2 delay block at bits 197-211. "
            "Field widths are provisional at boundaries where leading bits "
            "were always zero in this corpus. Verified against every "
            "register capture under sysex/prog/edit/registers/; layout "
            "source: REGISTER_BLOB_FIELDS in m7_sysex.prog.register_blob. "
            "Docs: specification/prog/bytes/register-basis-blob.md"
        ),
        "char_enum": {
            "enum_id": "register_name_char",
            "entries": register_name_char_enum_entries(),
        },
        "charset": REGISTER_NAME_CHARSET,
        "instances": instances,
        "fields": [
            {
                "id": f.id,
                "label": f.label,
                "bit_offset": f.bit_offset,
                "bit_width": f.bit_width,
                "payload_field": f.payload_field,
                "payload_offsets": list(f.payload_offsets),
            }
            for f in REGISTER_BLOB_FIELDS
        ],
    }
    blob_field["role"] = (
        "Register basis blob: factory dumps space-pad with 0x20; Reg-backed "
        "hold-EDIT dumps store a bit-packed snapshot of the stored register "
        "(name, store counter, all 18 parameters incl. delay block)"
    )


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
