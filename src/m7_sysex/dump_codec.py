"""Decode and encode single M7 dumps against the committed spec JSON.

Backs the user-facing ``m7-sysex decode`` / ``m7-sysex encode`` commands.
Field layout, encodings, and value maps come from the committed
``specification/{prog,system}/*.spec.json`` files (the same source the
web-ui runtime bundle is generated from), so a decode -> encode round trip
of a checksum-valid dump is byte-identical.
"""

from __future__ import annotations

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


# Baseline values for fields whose documented rest state is not zero. All
# other non-frame fields default to encoded 0, which is a valid documented
# state everywhere (bank 0 / slot 0 = Halls Large Hall identity, engine
# class 0 = classic banks, panel idle, first encoding step per parameter).
_SKELETON_DEFAULTS: dict[str, bytes | int] = {
    "program_name_pad": b"\x20\x20",  # factory space pad
    "register_basis_blob": b"\x20" * 64,  # factory space pad
    "favorite_slot": 8,  # not loaded from a favorite
    "algorithm_family_flag": 3,  # Halls baseline (mirror 145 stays 0)
    "fixed_always_02_00": b"\x02\x00",  # PROG 131-132 / SYSTEM 19-20
}


def build_serialize_skeleton(spec: dict[str, Any]) -> bytes:
    """Synthesize a checksum-valid baseline message from a dump spec.

    The byte map has no unknown bytes, so the serialize skeleton is derived
    from the committed spec instead of a captured template dump: frame
    ``contents``, factory space padding for the name window and register
    basis blob, documented rest values (favorite slot ``08``, companion
    ``02 00``), and zeros everywhere else.
    """
    buf = bytearray(int(spec["message_length"]))
    for field in spec["fields"]:
        start = int(field["start"])
        end = int(field["end"])
        contents = field.get("contents")
        if contents is not None:
            buf[start : end + 1] = bytes(contents)
            continue
        if field.get("kind") == "string" or field.get("encoding") == "ascii_space_padded":
            buf[start : end + 1] = b"\x20" * (end - start + 1)
            continue
        default = _SKELETON_DEFAULTS.get(field["id"])
        if default is None:
            continue
        if isinstance(default, int):
            wire = bytes(
                encode_at_offsets(default, field["encoding"], end - start + 1)
            )
        else:
            wire = default
        if len(wire) != end - start + 1:
            raise ValueError(f"skeleton default for {field['id']!r}: bad length")
        buf[start : end + 1] = wire
    if bytes(buf[4:8]) == PROGRAM_DUMP_HEADER:
        write_program_dump_checksum(buf)
    else:
        write_system_dump_checksum(buf)
    return bytes(buf)


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

    Fields absent from ``doc["fields"]`` keep the spec-derived serialize
    skeleton's bytes, so a minimal document (e.g. just parameter values)
    still produces a well-formed dump.
    """
    dump_kind = doc.get("kind")
    if dump_kind not in _SPEC_FILES:
        raise ValueError(f"document 'kind' must be 'prog' or 'system', got {dump_kind!r}")
    spec = load_dump_spec(dump_kind, spec_root)
    buf = bytearray(build_serialize_skeleton(spec))

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
