"""Decode and encode single M7 dumps against the committed spec JSON.

Backs the user-facing ``m7-sysex decode`` / ``m7-sysex encode`` commands.
Field layout, encodings, and value maps come from the committed
``specification/{prog,system}/*.spec.json`` files (the same source the
web-ui runtime bundle is generated from), so a decode -> encode round trip
of a checksum-valid dump is byte-identical.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

from .encodings import decode_at_offsets, encode_at_offsets
from .frame import (
    PROGRAM_DUMP_HEADER,
    PROGRAM_MESSAGE_LENGTH,
    SYSTEM_DUMP_HEADER,
    SYSTEM_MESSAGE_LENGTH,
    verify_program_dump_checksum,
    verify_system_dump_checksum,
    write_program_dump_checksum,
    write_system_dump_checksum,
)
from .labels import format_value_with_unit
from .paths import specification_root
from .prog.register_blob import (
    RegisterBasis,
    blob_kind,
    decode_register_blob,
    encode_register_blob,
)

_SPEC_FILES = {
    "prog": ("prog", "m7_program_dump.spec.json"),
    "system": ("system", "m7_system_dump.spec.json"),
}

_INT_ENCODINGS = {"raw_u8", "nibble_hilo", "nibble_lohi", "midi14_be", "midi14_le"}


def _default_spec_root() -> Path:
    """Committed specification/ folder: cwd first, then repo-relative."""
    cwd_root = specification_root()
    if cwd_root.is_dir():
        return cwd_root
    repo_root = Path(__file__).resolve().parents[2]
    return specification_root(repo_root)


def load_dump_spec(kind: str, spec_root: Path | None = None) -> dict[str, Any]:
    """Load the committed spec JSON for ``kind`` ("prog" or "system")."""
    if kind not in _SPEC_FILES:
        raise ValueError(f"unknown dump kind: {kind!r}")
    root = Path(spec_root) if spec_root is not None else _default_spec_root()
    subdir, filename = _SPEC_FILES[kind]
    path = root / subdir / filename
    if not path.is_file():
        raise FileNotFoundError(f"spec not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def detect_dump_kind(message: bytes) -> str:
    """Classify one SysEx message as "prog" or "system" by header + length."""
    if len(message) < 8:
        raise ValueError(f"SysEx message too short: {len(message)} bytes")
    header = bytes(message[4:8])
    if header == PROGRAM_DUMP_HEADER:
        if len(message) != PROGRAM_MESSAGE_LENGTH:
            raise ValueError(
                f"program dump length {len(message)} != {PROGRAM_MESSAGE_LENGTH}"
            )
        return "prog"
    if header == SYSTEM_DUMP_HEADER:
        if len(message) != SYSTEM_MESSAGE_LENGTH:
            raise ValueError(
                f"system dump length {len(message)} != {SYSTEM_MESSAGE_LENGTH}"
            )
        return "system"
    raise ValueError(f"unrecognized dump header: {header.hex(' ')}")


def _value_map_labels(field: dict[str, Any]) -> dict[int, str]:
    value_map = field.get("value_map") or {}
    return {
        int(entry["encoded"]): str(entry["label"])
        for entry in value_map.get("entries") or []
    }


def _field_bytes(message: bytes, field: dict[str, Any]) -> bytes:
    return bytes(message[int(field["start"]) : int(field["end"]) + 1])


def _display_label(label: str, unit: str | None) -> str:
    """Append the unit only when the label is a bare number ("6 ms" stays)."""
    try:
        float(label)
    except ValueError:
        return label
    return format_value_with_unit(label, unit)


def _decode_field(message: bytes, field: dict[str, Any]) -> dict[str, Any] | None:
    kind = field.get("kind")
    encoding = field.get("encoding")
    raw = _field_bytes(message, field)

    if kind in ("frame", "checksum"):
        return None

    entry: dict[str, Any] = {"label": field.get("label") or field["id"]}

    if kind == "string" or encoding == "ascii_space_padded":
        entry["text"] = raw.decode("ascii", errors="replace").rstrip(" ")
        return entry

    if encoding in _INT_ENCODINGS:
        decoded = decode_at_offsets(message, field["offsets"], encoding)
        encoded = int(decoded.value)
        entry["encoded"] = encoded
        labels = _value_map_labels(field)
        if labels:
            label = labels.get(encoded)
            entry["value"] = label
            if field.get("unit"):
                entry["unit"] = field["unit"]
            if label is not None:
                entry["display"] = _display_label(label, field.get("unit"))
        return entry

    # raw_bytes / reserved regions: hex is authoritative for round trips.
    entry["hex"] = raw.hex()
    if field["id"] == "register_basis_blob":
        entry["blob_kind"] = blob_kind(raw)
        if entry["blob_kind"] == "register_basis":
            basis = decode_register_blob(raw)
            entry["register"] = {"name": basis.name, "values": dict(basis.values)}
    return entry


def decode_dump(
    message: bytes, *, spec_root: Path | None = None
) -> dict[str, Any]:
    """Decode one SysEx message into a JSON-friendly document."""
    dump_kind = detect_dump_kind(message)
    spec = load_dump_spec(dump_kind, spec_root)

    for field in spec["fields"]:
        contents = field.get("contents")
        if contents is not None and _field_bytes(message, field) != bytes(contents):
            raise ValueError(
                f"field {field['id']!r}: expected {bytes(contents).hex(' ')}, "
                f"got {_field_bytes(message, field).hex(' ')}"
            )

    if dump_kind == "prog":
        checksum_ok = verify_program_dump_checksum(message)
    else:
        checksum_ok = verify_system_dump_checksum(message)

    fields: dict[str, Any] = {}
    for field in spec["fields"]:
        entry = _decode_field(message, field)
        if entry is not None:
            fields[field["id"]] = entry

    doc: dict[str, Any] = {
        "format": spec["format"],
        "kind": dump_kind,
        "message_length": len(message),
        "checksum_ok": checksum_ok,
        "fields": fields,
    }
    name = fields.get("program_name", {}).get("text")
    if name is not None:
        doc["program_name"] = name
    return doc


def _load_skeleton(kind: str, spec_root: Path | None = None) -> bytearray:
    root = Path(spec_root) if spec_root is not None else _default_spec_root()
    path = root / "web_serialize_skeletons.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    entry = raw[kind]
    skeleton = bytearray(base64.standard_b64decode(entry["b64"]))
    if len(skeleton) != int(entry["message_length"]):
        raise ValueError(f"skeleton length mismatch for {kind}")
    return skeleton


def _encode_field(
    buf: bytearray, field: dict[str, Any], entry: dict[str, Any]
) -> None:
    start = int(field["start"])
    end = int(field["end"])
    span = end - start + 1
    kind = field.get("kind")
    encoding = field.get("encoding")

    if kind == "string" or encoding == "ascii_space_padded":
        text = str(entry.get("text", ""))
        wire = text.encode("ascii").ljust(span, b" ")
        if len(wire) != span:
            raise ValueError(
                f"field {field['id']!r}: text longer than {span} chars"
            )
    elif "hex" in entry:
        wire = bytes.fromhex(entry["hex"])
    elif field["id"] == "register_basis_blob" and "register" in entry:
        reg = entry["register"]
        basis = RegisterBasis(
            name=str(reg["name"]),
            values={k: int(v) for k, v in reg["values"].items()},
        )
        wire = encode_register_blob(basis)
    elif "encoded" in entry:
        if encoding not in _INT_ENCODINGS:
            raise ValueError(
                f"field {field['id']!r}: cannot encode integer with "
                f"encoding {encoding!r}"
            )
        wire = bytes(encode_at_offsets(int(entry["encoded"]), encoding, span))
    else:
        raise ValueError(
            f"field {field['id']!r}: entry needs 'text', 'hex', 'encoded', "
            f"or 'register'"
        )

    if len(wire) != span:
        raise ValueError(
            f"field {field['id']!r}: wire length {len(wire)} != span {span}"
        )
    buf[start : end + 1] = wire


def encode_dump(doc: dict[str, Any], *, spec_root: Path | None = None) -> bytes:
    """Rebuild a checksum-valid SysEx message from a decoded document.

    Fields absent from ``doc["fields"]`` keep the committed serialize
    skeleton's bytes, so a minimal document (e.g. just parameter values)
    still produces a well-formed dump.
    """
    dump_kind = doc.get("kind")
    if dump_kind not in _SPEC_FILES:
        raise ValueError(f"document 'kind' must be 'prog' or 'system', got {dump_kind!r}")
    spec = load_dump_spec(dump_kind, spec_root)
    buf = _load_skeleton(dump_kind, spec_root)
    if len(buf) != int(spec["message_length"]):
        raise ValueError("skeleton length != spec message_length")

    fields_doc = doc.get("fields") or {}
    known_ids = {field["id"] for field in spec["fields"]}
    unknown = sorted(set(fields_doc) - known_ids)
    if unknown:
        raise ValueError(f"unknown field ids: {', '.join(unknown)}")

    for field in spec["fields"]:
        if field.get("kind") in ("frame", "checksum"):
            continue
        entry = fields_doc.get(field["id"])
        if entry is None:
            continue
        _encode_field(buf, field, entry)

    if dump_kind == "prog":
        write_program_dump_checksum(buf)
    else:
        write_system_dump_checksum(buf)
    return bytes(buf)
