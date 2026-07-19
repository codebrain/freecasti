"""Unit tests for SysEx frame parsing and the program-dump checksum."""

from pathlib import Path

import pytest

from m7_sysex.frame import (
    BRICASTI_MFR_ID,
    CHECKSUM_NIBBLE_COUNT,
    DATA_OFFSET,
    PROGRAM_DUMP_HEADER,
    SYSTEM_CHECKSUM_COVER_END,
    SYSTEM_DUMP_HEADER,
    SYSTEM_MESSAGE_LENGTH,
    crc16_arc,
    is_nibble_payload,
    pack_u16_be_nibbles,
    parse_sysex,
    parse_system_sysex,
    program_dump_checksum,
    system_dump_checksum,
    verify_program_dump_checksum,
    verify_system_dump_checksum,
    write_program_dump_checksum,
)

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "sysex" / "prog" / "parameters" / "diffusion" / "low.syx"
SYSTEM_SAMPLE = ROOT / "sysex" / "system" / "midi channel" / "1.syx"


def test_parse_sysex_fields():
    raw = SAMPLE.read_bytes()
    frame = parse_sysex(raw)
    assert frame.manufacturer_id == BRICASTI_MFR_ID
    assert frame.header == PROGRAM_DUMP_HEADER
    assert frame.length == len(raw)
    assert frame.name  # ASCII program name, space padding stripped
    # data_nibbles covers offsets 88 .. checksum start
    assert len(frame.data_nibbles) == len(raw) - DATA_OFFSET - 1 - CHECKSUM_NIBBLE_COUNT
    assert len(frame.checksum_nibbles) == CHECKSUM_NIBBLE_COUNT
    assert is_nibble_payload(frame.data_nibbles)
    assert is_nibble_payload(frame.checksum_nibbles)


def test_parse_sysex_rejects_bad_input():
    raw = SAMPLE.read_bytes()
    with pytest.raises(ValueError, match="empty"):
        parse_sysex(b"")
    with pytest.raises(ValueError, match="F0 start"):
        parse_sysex(b"\x00" + raw[1:])
    with pytest.raises(ValueError, match="F7 end"):
        parse_sysex(raw[:-1] + b"\x00")
    with pytest.raises(ValueError, match="too short"):
        parse_sysex(b"\xf0\x00\x62\x63\xf7")


def test_crc16_arc_check_vector():
    # Standard CRC-16/ARC check value for "123456789".
    assert crc16_arc(b"123456789") == 0xBB3D


def test_pack_u16_be_nibbles():
    assert pack_u16_be_nibbles(0x0000) == bytes((0, 0, 0, 0))
    assert pack_u16_be_nibbles(0xBB3D) == bytes((0x0B, 0x0B, 0x03, 0x0D))
    assert pack_u16_be_nibbles(0xFFFF) == bytes((0x0F, 0x0F, 0x0F, 0x0F))


def test_checksum_round_trip_after_edit():
    """Mutating a payload nibble invalidates then recomputes the checksum."""
    raw = bytearray(SAMPLE.read_bytes())
    assert verify_program_dump_checksum(bytes(raw))

    raw[100] = (raw[100] + 1) % 16
    assert not verify_program_dump_checksum(bytes(raw))

    write_program_dump_checksum(raw)
    assert verify_program_dump_checksum(bytes(raw))


def test_checksum_excludes_header():
    """Changing the (excluded) header must not affect the computed checksum."""
    raw = bytearray(SAMPLE.read_bytes())
    before = program_dump_checksum(bytes(raw))
    raw[5] = (raw[5] + 1) & 0x7F
    assert program_dump_checksum(bytes(raw)) == before


def test_parse_system_sysex_fields():
    raw = SYSTEM_SAMPLE.read_bytes()
    frame = parse_system_sysex(raw)
    assert frame.manufacturer_id == BRICASTI_MFR_ID
    assert frame.header == SYSTEM_DUMP_HEADER
    assert frame.length == SYSTEM_MESSAGE_LENGTH
    assert len(frame.payload_nibbles) == SYSTEM_CHECKSUM_COVER_END - 8
    assert len(frame.checksum_nibbles) == CHECKSUM_NIBBLE_COUNT
    assert is_nibble_payload(frame.payload_nibbles)
    assert verify_system_dump_checksum(raw)


def test_system_checksum_matches_prog_algorithm_on_cover():
    """SYSTEM CRC uses the same algorithm over its shorter cover range."""
    raw = SYSTEM_SAMPLE.read_bytes()
    cover = raw[8:SYSTEM_CHECKSUM_COVER_END]
    assert system_dump_checksum(raw) == pack_u16_be_nibbles(crc16_arc(cover))
