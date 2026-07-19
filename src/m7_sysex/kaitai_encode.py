"""Serialize Kaitai-parsed M7 dump objects back to on-wire SysEx bytes.

Kaitai Struct generates decoders only. This module mirrors the committed
``.spec.json`` field layout so callers can rebuild messages from parsed
objects and recompute checksums after edits.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from m7_sysex.frame import (
    PROGRAM_MESSAGE_LENGTH,
    SYSTEM_MESSAGE_LENGTH,
    write_program_dump_checksum,
    write_system_dump_checksum,
)


def field_wire_bytes(parsed: Any, field: dict[str, Any]) -> bytes:
    """Reconstruct the on-wire bytes for one spec field from a parsed dump."""
    val = getattr(parsed, field["id"])
    encoding = field.get("encoding")
    kind = field.get("kind")

    if field.get("contents") is not None:
        return val if isinstance(val, bytes) else bytes(field["contents"])

    if kind == "checksum":
        return bytes(parsed.checksum) if isinstance(val, (bytes, bytearray)) else val

    if kind == "string" or encoding == "ascii_space_padded":
        if isinstance(val, str):
            size = int(field.get("size", len(val)))
            return val.encode("ascii").ljust(size, b" ")[:size]
        return val

    if encoding == "nibble_hilo" or (
        hasattr(val, "hi_nibble") and hasattr(val, "lo_nibble")
    ):
        return bytes([val.hi_nibble, val.lo_nibble])

    if encoding == "nibble_lohi":
        return bytes([val.lo_nibble, val.hi_nibble])

    if isinstance(val, Enum):
        return bytes([val.value])

    if isinstance(val, bytes):
        return val

    if isinstance(val, int):
        return bytes([val])

    raise TypeError(
        f"cannot extract wire bytes for field {field['id']!r}: {type(val)!r}"
    )


def serialize_parsed_dump(
    parsed: Any,
    fields: list[dict[str, Any]],
    *,
    system: bool = False,
    message_length: int | None = None,
) -> bytes:
    """
    Serialize a Kaitai-parsed dump to on-wire bytes.

    Non-checksum fields are taken from ``parsed``; the checksum is always
    recomputed from the serialized cover range (same rule as the hardware).
    """
    if message_length is None:
        message_length = SYSTEM_MESSAGE_LENGTH if system else PROGRAM_MESSAGE_LENGTH

    buf = bytearray(message_length)
    for field in fields:
        if field.get("kind") == "checksum":
            continue
        wire = field_wire_bytes(parsed, field)
        start = int(field["start"])
        end = int(field["end"])
        span = end - start + 1
        if len(wire) != span:
            raise ValueError(
                f"field {field['id']!r}: wire length {len(wire)} != span {span}"
            )
        buf[start : end + 1] = wire

    if system:
        write_system_dump_checksum(buf)
    else:
        write_program_dump_checksum(buf)
    return bytes(buf)


def write_dump_checksum(buf: bytearray, *, system: bool = False) -> None:
    """Recompute and write the trailing checksum nibbles in place."""
    if system:
        write_system_dump_checksum(buf)
    else:
        write_program_dump_checksum(buf)
