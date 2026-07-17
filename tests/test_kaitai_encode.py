"""True encode round-trips: Kaitai parse → serialize → bytes / re-parse."""

from __future__ import annotations

from pathlib import Path

import pytest

from m7_sysex.corpus_layout import is_prog_corpus_dump
from m7_sysex.frame import (
    SYSTEM_MESSAGE_LENGTH,
    verify_program_dump_checksum,
    verify_system_dump_checksum,
    write_program_dump_checksum,
)
from m7_sysex.kaitai_encode import serialize_parsed_dump
from tests.kaitai_support import load_spec_fields

ROOT = Path(__file__).resolve().parents[1]
SYSEX = ROOT / "sysex"
PROG_SAMPLE = SYSEX / "prog" / "parameters" / "diffusion" / "low.syx"
SYSTEM_SAMPLE = SYSEX / "system" / "midi channel" / "1.syx"
PRESET_SAMPLE = SYSEX / "prog" / "presets" / "Chambers.Large Chamber.syx"
PROG_FIELDS = load_spec_fields(ROOT / "specification" / "prog" / "m7_program_dump.spec.json")
SYSTEM_FIELDS = load_spec_fields(ROOT / "specification" / "system" / "m7_system_dump.spec.json")

PROG_DUMPS = sorted(p for p in SYSEX.rglob("*.syx") if is_prog_corpus_dump(p, SYSEX))
SYSTEM_DUMPS = sorted(
    p for p in (SYSEX / "system").rglob("*.syx") if "_system" not in p.parts
)


def test_serialize_prog_sample_matches_capture(kaitai_prog_parser):
    raw = PROG_SAMPLE.read_bytes()
    parsed = kaitai_prog_parser.from_bytes(raw)
    encoded = serialize_parsed_dump(parsed, PROG_FIELDS, system=False)
    assert encoded == raw
    assert verify_program_dump_checksum(encoded)


def test_serialize_system_sample_matches_capture(kaitai_system_parser):
    raw = SYSTEM_SAMPLE.read_bytes()
    assert len(raw) == SYSTEM_MESSAGE_LENGTH
    parsed = kaitai_system_parser.from_bytes(raw)
    encoded = serialize_parsed_dump(parsed, SYSTEM_FIELDS, system=True)
    assert encoded == raw
    assert verify_system_dump_checksum(encoded)


def test_serialize_preset_reparse_is_byte_identical(kaitai_prog_parser):
    raw = PRESET_SAMPLE.read_bytes()
    parsed = kaitai_prog_parser.from_bytes(raw)
    encoded = serialize_parsed_dump(parsed, PROG_FIELDS, system=False)
    again = kaitai_prog_parser.from_bytes(encoded)
    assert serialize_parsed_dump(again, PROG_FIELDS, system=False) == encoded
    assert encoded == raw


def test_serialize_repairs_corrupt_checksum(kaitai_prog_parser):
    raw = bytearray(PROG_SAMPLE.read_bytes())
    raw[152] = (raw[152] + 1) % 16
    assert not verify_program_dump_checksum(bytes(raw))

    parsed = kaitai_prog_parser.from_bytes(bytes(raw))
    encoded = serialize_parsed_dump(parsed, PROG_FIELDS, system=False)
    assert verify_program_dump_checksum(encoded)
    assert encoded != bytes(raw)
    assert encoded[:152] == bytes(raw)[:152]


def test_write_program_dump_checksum_matches_serializer(kaitai_prog_parser):
    raw = bytearray(PROG_SAMPLE.read_bytes())
    parsed = kaitai_prog_parser.from_bytes(bytes(raw))
    buf = bytearray(serialize_parsed_dump(parsed, PROG_FIELDS, system=False))
    buf[152:156] = b"\x00\x00\x00\x00"
    write_program_dump_checksum(buf)
    assert bytes(buf) == serialize_parsed_dump(parsed, PROG_FIELDS, system=False)


@pytest.mark.slow
@pytest.mark.parametrize("path", PROG_DUMPS, ids=lambda p: p.relative_to(SYSEX).as_posix())
def test_prog_serialize_roundtrip_corpus(path: Path, kaitai_prog_parser):
    raw = path.read_bytes()
    parsed = kaitai_prog_parser.from_bytes(raw)
    encoded = serialize_parsed_dump(parsed, PROG_FIELDS, system=False)
    assert encoded == raw
    reparsed = kaitai_prog_parser.from_bytes(encoded)
    assert serialize_parsed_dump(reparsed, PROG_FIELDS, system=False) == encoded


@pytest.mark.slow
@pytest.mark.parametrize(
    "path", SYSTEM_DUMPS, ids=lambda p: p.relative_to(SYSEX / "system").as_posix()
)
def test_system_serialize_roundtrip_corpus(path: Path, kaitai_system_parser):
    raw = path.read_bytes()
    parsed = kaitai_system_parser.from_bytes(raw)
    encoded = serialize_parsed_dump(parsed, SYSTEM_FIELDS, system=True)
    assert encoded == raw
    reparsed = kaitai_system_parser.from_bytes(encoded)
    assert serialize_parsed_dump(reparsed, SYSTEM_FIELDS, system=True) == encoded
