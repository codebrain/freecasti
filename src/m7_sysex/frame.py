"""Bricasti M7 SysEx constants and frame parsing."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

SYSEX_START = 0xF0
SYSEX_END = 0xF7

# Bricasti Design 3-byte manufacturer ID observed in M7 program dumps.
BRICASTI_MFR_ID = bytes((0x00, 0x62, 0x63))

# Observed program-dump header after manufacturer ID:
#   70 08 01 00  ("p", then three command/version bytes)
# Hold EDIT uses this same header and 157-byte length; identity differs
# (bank word 88-89 = 11). See EDIT_DUMP_BANK_INDEX in names.py.
PROGRAM_DUMP_HEADER = bytes((0x70, 0x08, 0x01, 0x00))

# Observed system-dump header (hold SYSTEM on the unit):
#   70 08 02 00
SYSTEM_DUMP_HEADER = bytes((0x70, 0x08, 0x02, 0x00))

NAME_OFFSET = 8
# Wire name window (ASCII, space-padded within 8–23).
PROGRAM_NAME_LENGTH = 16
# Manual/UI editable label length (14-character location display); trailing
# two bytes of the wire window (offsets 22–23) are space pad in this corpus.
PROGRAM_NAME_EDITABLE_LENGTH = 14
# Opaque register-basis copy on Reg-backed hold-EDIT dumps; factory dumps
# fill this region with 0x20 spaces (same as trailing name padding).
REGISTER_BASIS_BLOB_OFFSET = 24
REGISTER_BASIS_BLOB_LENGTH = 64
# Factory preset validation still compares the full 8–87 window (name + spaces).
NAME_REGION_LENGTH = PROGRAM_NAME_LENGTH + REGISTER_BASIS_BLOB_LENGTH  # 80
NAME_LENGTH = NAME_REGION_LENGTH  # alias: factory space-padded window
DATA_OFFSET = NAME_OFFSET + NAME_REGION_LENGTH  # 88
PROGRAM_MESSAGE_LENGTH = 157

# System dumps: no name/blob region; payload nibbles start at offset 8.
SYSTEM_PAYLOAD_OFFSET = 8
SYSTEM_MESSAGE_LENGTH = 77
SYSTEM_CHECKSUM_COVER_START = SYSTEM_PAYLOAD_OFFSET  # 8
SYSTEM_CHECKSUM_COVER_END = 72  # exclusive (checksum at 72-75)

# Trailing 4 nibbles before F7: CRC-16/ARC over name+blob+payload (offsets 8..151),
# packed high-nibble-first as four SysEx data bytes.
CHECKSUM_NIBBLE_COUNT = 4
CHECKSUM_COVER_START = NAME_OFFSET  # 8 - excludes F0, mfr id, and header

# Checksum guidance strings for hypothesis / export docs.
PROG_CHECKSUM_COVER = (
    "bytes[8:152], pack as four high-nibble-first SysEx bytes at offsets 152-155"
)
SYSTEM_CHECKSUM_COVER = (
    "bytes[8:72], pack as four high-nibble-first SysEx bytes at offsets 72-75"
)
PROG_CHECKSUM_RANGE_DESC = "offsets 8-151"
SYSTEM_CHECKSUM_RANGE_DESC = "offsets 8-71"


@dataclass(frozen=True)
class SysexFrame:
    """Parsed M7 program-dump SysEx message."""

    raw: bytes
    manufacturer_id: bytes
    header: bytes
    name: str
    data_nibbles: bytes  # bytes from after name through byte before checksum
    checksum_nibbles: bytes

    @property
    def length(self) -> int:
        return len(self.raw)


def iter_sysex_messages(data: bytes) -> Iterator[bytes]:
    """Yield each ``F0``…``F7`` SysEx message from a blob (concatenated dumps OK)."""
    if not data:
        return
    i = 0
    n = len(data)
    while i < n:
        if data[i] != SYSEX_START:
            i += 1
            continue
        j = i + 1
        while j < n and data[j] != SYSEX_END:
            j += 1
        if j >= n:
            raise ValueError(f"truncated SysEx starting at offset {i}")
        yield data[i : j + 1]
        i = j + 1


def parse_sysex(data: bytes) -> SysexFrame:
    """Parse a single M7 program-dump .syx blob."""
    if not data:
        raise ValueError("empty SysEx file")
    if data[0] != SYSEX_START:
        raise ValueError(f"missing F0 start status (got 0x{data[0]:02X})")
    if data[-1] != SYSEX_END:
        raise ValueError(f"missing F7 end status (got 0x{data[-1]:02X})")
    if len(data) < DATA_OFFSET + CHECKSUM_NIBBLE_COUNT + 1:
        raise ValueError(f"SysEx too short: {len(data)} bytes")

    mfr = data[1:4]
    header = data[4:8]
    name_bytes = data[NAME_OFFSET : NAME_OFFSET + PROGRAM_NAME_LENGTH]
    payload = data[DATA_OFFSET:-1]  # exclusive of F7

    if len(payload) < CHECKSUM_NIBBLE_COUNT:
        raise ValueError("payload shorter than checksum field")

    data_nibbles = payload[:-CHECKSUM_NIBBLE_COUNT]
    checksum_nibbles = payload[-CHECKSUM_NIBBLE_COUNT:]

    name = name_bytes.decode("ascii", errors="replace").rstrip(" ")

    return SysexFrame(
        raw=data,
        manufacturer_id=mfr,
        header=header,
        name=name,
        data_nibbles=data_nibbles,
        checksum_nibbles=checksum_nibbles,
    )


@dataclass(frozen=True)
class SystemSysexFrame:
    """Parsed M7 system-dump SysEx message (I/O and routing, not program params)."""

    raw: bytes
    manufacturer_id: bytes
    header: bytes
    payload_nibbles: bytes
    checksum_nibbles: bytes

    @property
    def length(self) -> int:
        return len(self.raw)


def parse_system_sysex(data: bytes) -> SystemSysexFrame:
    """Parse a single M7 system-dump .syx blob."""
    if not data:
        raise ValueError("empty SysEx file")
    if data[0] != SYSEX_START:
        raise ValueError(f"missing F0 start status (got 0x{data[0]:02X})")
    if data[-1] != SYSEX_END:
        raise ValueError(f"missing F7 end status (got 0x{data[-1]:02X})")
    if len(data) != SYSTEM_MESSAGE_LENGTH:
        raise ValueError(
            f"system SysEx length {len(data)} != {SYSTEM_MESSAGE_LENGTH}"
        )

    mfr = data[1:4]
    header = data[4:8]
    checksum_start = SYSTEM_CHECKSUM_COVER_END
    payload_nibbles = data[SYSTEM_PAYLOAD_OFFSET:checksum_start]
    checksum_nibbles = data[checksum_start : checksum_start + CHECKSUM_NIBBLE_COUNT]

    if header != SYSTEM_DUMP_HEADER:
        raise ValueError(
            f"unexpected system header {header.hex(' ')} "
            f"(expected {SYSTEM_DUMP_HEADER.hex(' ')})"
        )

    return SystemSysexFrame(
        raw=data,
        manufacturer_id=mfr,
        header=header,
        payload_nibbles=payload_nibbles,
        checksum_nibbles=checksum_nibbles,
    )


def system_dump_checksum(raw: bytes) -> bytes:
    """Compute checksum nibbles for an M7 system-dump message (CRC over 8..71)."""
    if len(raw) != SYSTEM_MESSAGE_LENGTH:
        raise ValueError(f"system SysEx length {len(raw)} != {SYSTEM_MESSAGE_LENGTH}")
    cover = raw[SYSTEM_CHECKSUM_COVER_START:SYSTEM_CHECKSUM_COVER_END]
    return pack_u16_be_nibbles(crc16_arc(cover))


def verify_system_dump_checksum(raw: bytes) -> bool:
    """Return True if trailing checksum nibbles match CRC-16/ARC over 8..71."""
    checksum_start = SYSTEM_CHECKSUM_COVER_END
    actual = raw[checksum_start : checksum_start + CHECKSUM_NIBBLE_COUNT]
    return actual == system_dump_checksum(raw)


def is_nibble_payload(data: bytes) -> bool:
    """Return True if every byte is a MIDI data nibble (0x00-0x0F)."""
    return all(b <= 0x0F for b in data)


def crc16_arc(data: bytes) -> int:
    """
    CRC-16/ARC (aka CRC-16/IBM / CRC-16/ANSI).

    poly=0x8005, init=0x0000, refin=true, refout=true, xorout=0x0000.
    Implemented via the reflected form (poly 0xA001).
    """
    crc = 0x0000
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF


def pack_u16_be_nibbles(value: int) -> bytes:
    """Pack a 16-bit value as four high-nibble-first SysEx data bytes."""
    v = value & 0xFFFF
    return bytes(
        (
            (v >> 12) & 0x0F,
            (v >> 8) & 0x0F,
            (v >> 4) & 0x0F,
            v & 0x0F,
        )
    )


def program_dump_checksum(raw: bytes) -> bytes:
    """
    Compute the 4 checksum nibbles for an M7 program-dump message.

    Covers offsets 8 inclusive through checksum_start exclusive
    (name window + register-basis blob + payload nibbles). Manufacturer ID
    and header are excluded.
    """
    if len(raw) < DATA_OFFSET + CHECKSUM_NIBBLE_COUNT + 1:
        raise ValueError(f"SysEx too short for checksum: {len(raw)} bytes")
    checksum_start = len(raw) - 1 - CHECKSUM_NIBBLE_COUNT
    cover = raw[CHECKSUM_COVER_START:checksum_start]
    return pack_u16_be_nibbles(crc16_arc(cover))


def write_program_dump_checksum(buf: bytearray) -> None:
    """Write CRC-16/ARC checksum nibbles into a program-dump message."""
    checksum_start = len(buf) - 1 - CHECKSUM_NIBBLE_COUNT
    buf[checksum_start : checksum_start + CHECKSUM_NIBBLE_COUNT] = (
        program_dump_checksum(bytes(buf))
    )


def write_system_dump_checksum(buf: bytearray) -> None:
    """Write CRC-16/ARC checksum nibbles into a system-dump message."""
    checksum_start = SYSTEM_CHECKSUM_COVER_END
    buf[checksum_start : checksum_start + CHECKSUM_NIBBLE_COUNT] = (
        system_dump_checksum(bytes(buf))
    )


def verify_program_dump_checksum(raw: bytes) -> bool:
    """Return True if trailing checksum nibbles match CRC-16/ARC over name+payload."""
    checksum_start = len(raw) - 1 - CHECKSUM_NIBBLE_COUNT
    actual = raw[checksum_start : checksum_start + CHECKSUM_NIBBLE_COUNT]
    return actual == program_dump_checksum(raw)
