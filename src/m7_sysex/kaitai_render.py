"""Shared Kaitai Struct YAML rendering for PROG and SYSTEM dump specs."""

from __future__ import annotations

import json
import re
from typing import Any


def render_kaitai_yaml(spec: dict[str, Any]) -> str:
    """Render a Kaitai Struct ``.ksy`` document from a dump spec dict."""
    kaitai_id = spec.get("kaitai_id") or _default_kaitai_id(spec)
    fields = spec["fields"]
    value_enums = _collect_value_enums(fields)
    needs_generic_nibble = _needs_generic_nibble_type(fields)

    lines: list[str] = [
        "# GENERATED FILE — do not hand-edit.",
        "# Produced by m7_sysex export from byte_map + parameter analyses.",
        f"# Compile with: kaitai-struct-compiler {kaitai_id}.ksy",
        "# Spec: https://kaitai.io/",
        "",
        "meta:",
        f"  id: {kaitai_id}",
        f"  title: {_yaml_str(spec['title'])}",
        "  application: Bricasti M7",
        f"  file-extension: {spec['file_extension']}",
        "  endian: be",
        "  ks-version: '0.10'",
        "doc: |",
    ]
    for paragraph in _doc_paragraphs(spec):
        for row in _wrap(paragraph, 76):
            lines.append(f"  {row}")
        lines.append("  ")
    if lines[-1] == "  ":
        lines.pop()

    lines.append("seq:")
    for field in fields:
        lines.extend(_kaitai_seq_entry(field))

    blob_specs = [field["blob"] for field in fields if field.get("blob")]
    for blob in blob_specs:
        char_enum = blob.get("char_enum")
        if char_enum:
            value_enums.append(
                (str(char_enum["enum_id"]), list(char_enum["entries"]))
            )

    if value_enums:
        lines.append("enums:")
        for enum_id, entries in value_enums:
            lines.extend(_render_enum(enum_id, entries))
        lines.append("")

    lines.append("types:")
    for field in fields:
        if _field_uses_nibble_value_map(field):
            lines.extend(_nibble_encoded_type(field))
    if needs_generic_nibble:
        lines.extend(_generic_nibble_type_lines())
    for blob in blob_specs:
        lines.extend(_blob_type_lines(blob))

    return "\n".join(lines).rstrip() + "\n"


def _default_kaitai_id(spec: dict[str, Any]) -> str:
    fmt = str(spec.get("format") or "dump")
    if "system" in fmt:
        return "m7_system_dump"
    return "m7_program_dump"


def _doc_paragraphs(spec: dict[str, Any]) -> list[str]:
    cs = spec["checksum"]
    paragraphs = [
        spec["disclaimer"],
        (
            f"Fixed length {spec['message_length']} bytes. "
            f"Checksum: {cs['algorithm']} over offsets "
            f"[{cs['cover_start']}, {cs['cover_end_exclusive']}), "
            f"packed as {cs['pack']} at offsets {cs['offsets']}."
        ),
    ]
    extra = spec.get("kaitai_doc_extra")
    if extra:
        paragraphs.append(str(extra))
    return paragraphs


def _collect_value_enums(
    fields: list[dict[str, Any]],
) -> list[tuple[str, list[dict[str, Any]]]]:
    seen: set[str] = set()
    out: list[tuple[str, list[dict[str, Any]]]] = []
    for field in fields:
        value_map = field.get("value_map")
        if not value_map:
            continue
        enum_id = str(value_map["enum_id"])
        if enum_id in seen:
            continue
        seen.add(enum_id)
        out.append((enum_id, list(value_map["entries"])))
    return out


def _render_enum(
    enum_id: str, entries: list[dict[str, Any]]
) -> list[str]:
    lines = [f"  {enum_id}:"]
    for entry in entries:
        enc = int(entry["encoded"])
        name = str(entry["name"])
        label = str(entry.get("label") or name).replace("\n", " ").strip()
        label = label.replace("#", "")
        comment = f"  # {label}" if label else ""
        lines.append(f"    {enc}: {name}{comment}")
    return lines


def _field_uses_nibble_value_map(field: dict[str, Any]) -> bool:
    return bool(
        field.get("value_map")
        and field.get("encoding") == "nibble_hilo"
        and int(field.get("size") or 0) == 2
    )


def _needs_generic_nibble_type(fields: list[dict[str, Any]]) -> bool:
    for field in fields:
        if (
            field.get("encoding") == "nibble_hilo"
            and int(field.get("size") or 0) == 2
            and not field.get("value_map")
        ):
            return True
    return False


def _nibble_encoded_type(field: dict[str, Any]) -> list[str]:
    fid = field["id"]
    enum_id = field["value_map"]["enum_id"]
    type_id = f"{fid}_encoded"
    return [
        f"  {type_id}:",
        "    doc: |",
        f"      Two SysEx data bytes (each 0x00-0x0F); decoded value is a",
        f"      member of {enum_id}.",
        "    seq:",
        "      - id: hi_nibble",
        "        type: u1",
        "        valid:",
        "          max: 15",
        "      - id: lo_nibble",
        "        type: u1",
        "        valid:",
        "          max: 15",
        "    instances:",
        "      value:",
        "        value: (hi_nibble << 4) | lo_nibble",
        f"        enum: {enum_id}",
        "",
    ]


def _blob_type_lines(blob: dict[str, Any]) -> list[str]:
    """Nested type with value instances for the register basis blob."""
    lines = [f"  {blob['type_id']}:"]
    if blob.get("doc"):
        lines.append("    doc: |")
        for row in _wrap(str(blob["doc"]), 72):
            lines.append(f"      {row}")
    lines.extend(
        [
            "    seq:",
            "      - id: data",
            f"        size: {int(blob['size'])}",
            "        doc: |",
            "          Raw wire bytes; the low nibble of each byte carries",
            "          the packed bitstream decoded by the instances below.",
            "    instances:",
        ]
    )
    for inst in blob.get("instances") or []:
        lines.append(f"      {inst['id']}:")
        if inst.get("doc"):
            lines.append("        doc: |")
            for row in _wrap(str(inst["doc"]), 66):
                lines.append(f"          {row}")
        lines.append(f"        value: {_yaml_str(str(inst['value']))}")
        if inst.get("enum"):
            lines.append(f"        enum: {inst['enum']}")
    lines.append("")
    return lines


def _generic_nibble_type_lines() -> list[str]:
    return [
        "  nibble_u8_hilo:",
        "    doc: |",
        "      Two SysEx data bytes that each hold a nibble (0x00-0x0F).",
        "      Decoded value = (hi_nibble << 4) | lo_nibble.",
        "    seq:",
        "      - id: hi_nibble",
        "        type: u1",
        "        valid:",
        "          max: 15",
        "      - id: lo_nibble",
        "        type: u1",
        "        valid:",
        "          max: 15",
        "    instances:",
        "      value:",
        "        value: (hi_nibble << 4) | lo_nibble",
        "",
    ]


def _kaitai_seq_entry(field: dict[str, Any]) -> list[str]:
    fid = field["id"]
    lines = [f"  - id: {fid}"]

    doc_bits: list[str] = []
    if field.get("description"):
        doc_bits.append(str(field["description"]))
    elif field.get("role"):
        role = str(field["role"])
        if len(role) > 160:
            role = role[:157] + "..."
        doc_bits.append(role)
    if field.get("parameter"):
        series_root = field.get("series_root") or "sysex/prog/parameters"
        doc_bits.append(f"Parameter series: {series_root}/{field['parameter']}/")
    elif field.get("series_root"):
        doc_bits.append(f"Capture series: {field['series_root']}/")
    value_map = field.get("value_map")
    if value_map:
        count = len(value_map.get("entries") or [])
        doc_bits.append(
            f"Locked encoding table: {count} known encoded value(s)"
        )
    elif field.get("kind") == "affine" and field.get("scale") is not None:
        scale = field["scale"]
        add = field.get("offset") or 0
        doc_bits.append(f"Affine: label = encoded * {scale:g} + ({add:g})")
    elif field.get("kind") == "table":
        doc_bits.append(
            "Value map: sparse/non-linear table (see parameter page)"
        )
    if field.get("status") == "secondary":
        doc_bits.append(
            "Secondary/edit-UI field — not a primary sound parameter"
        )
    if field.get("kind") == "checksum":
        doc_bits.append(
            "CRC-16/ARC over [8, checksum), four high-nibble-first bytes"
        )

    if doc_bits:
        lines.append("    doc: |")
        for bit in doc_bits:
            for row in _wrap(bit, 72):
                lines.append(f"      {row}")

    contents = field.get("contents")
    if contents is not None:
        hexes = ", ".join(f"0x{b:02x}" for b in contents)
        lines.append(f"    contents: [{hexes}]")
        return lines

    if field.get("type_ref"):
        lines.append(f"    type: {field['type_ref']}")
        return lines

    encoding = field.get("encoding")
    size = int(field["size"])
    if encoding == "ascii_space_padded" or field.get("kind") == "string":
        lines.append("    type: str")
        lines.append(f"    size: {size}")
        lines.append("    encoding: ASCII")
        return lines

    if value_map:
        enum_id = value_map["enum_id"]
        if encoding == "nibble_hilo" and size == 2:
            lines.append(f"    type: {fid}_encoded")
            return lines
        if (encoding == "raw_u8" or size == 1) and not contents:
            lines.append("    type: u1")
            lines.append(f"    enum: {enum_id}")
            return lines

    if encoding == "nibble_hilo" and size == 2:
        lines.append("    type: nibble_u8_hilo")
        return lines

    if encoding == "raw_u8" and size == 1:
        lines.append("    type: u1")
        return lines

    if size == 1:
        lines.append("    type: u1")
        return lines

    lines.append(f"    size: {size}")
    return lines


def _yaml_str(text: str) -> str:
    if re.search(r"[:#\[\]{}&*!|>'\"%@`]", text) or text.strip() != text:
        return json.dumps(text)
    return text


def _wrap(text: str, width: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    rows: list[str] = []
    cur = words[0]
    for word in words[1:]:
        trial = f"{cur} {word}"
        if len(trial) <= width:
            cur = trial
        else:
            rows.append(cur)
            cur = word
    rows.append(cur)
    return rows
