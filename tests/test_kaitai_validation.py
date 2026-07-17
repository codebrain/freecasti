"""Negative validation and Kaitai runtime edge cases."""

from __future__ import annotations

from enum import Enum
from pathlib import Path

import kaitaistruct
import pytest

from tests.kaitai_support import (
    encoded_int_from_field,
    field_parsed_value,
    fields_with_value_map,
    load_spec_fields,
)

ROOT = Path(__file__).resolve().parents[1]
SYSEX = ROOT / "sysex"
DIFFUSION_LOW = SYSEX / "prog" / "parameters" / "diffusion" / "low.syx"
PRESET = SYSEX / "prog" / "presets" / "Chambers.Large Chamber.syx"
PROG_FIELDS = load_spec_fields(ROOT / "specification" / "prog" / "m7_program_dump.spec.json")


@pytest.mark.parametrize(
    ("offset", "value"),
    [
        (0, 0xF1),
        (4, 0xFF),
        (156, 0xF6),
    ],
    ids=["sysex_start", "header", "sysex_end"],
)
def test_kaitai_rejects_invalid_frame_bytes(
    kaitai_prog_parser, offset: int, value: int
):
    raw = bytearray(DIFFUSION_LOW.read_bytes())
    raw[offset] = value
    with pytest.raises(kaitaistruct.ValidationNotEqualError):
        kaitai_prog_parser.from_bytes(bytes(raw))


def test_kaitai_valid_enum_fields_resolve_to_enum_members(kaitai_prog_parser):
    raw = DIFFUSION_LOW.read_bytes()
    parsed = kaitai_prog_parser.from_bytes(raw)
    diffusion = next(f for f in PROG_FIELDS if f["id"] == "diffusion")
    value = field_parsed_value(parsed, diffusion)
    assert isinstance(value, Enum)
    assert encoded_int_from_field(parsed, diffusion) == 0


def test_kaitai_unknown_enum_encoding_returns_raw_int(kaitai_prog_parser):
    """Kaitai Python returns bare ints for out-of-table u1 enums (documented)."""
    raw = bytearray(DIFFUSION_LOW.read_bytes())
    raw[107] = 0x63
    parsed = kaitai_prog_parser.from_bytes(bytes(raw))
    diffusion = next(f for f in PROG_FIELDS if f["id"] == "diffusion")
    value = field_parsed_value(parsed, diffusion)
    assert isinstance(value, int)
    assert value == 0x63


def test_kaitai_unknown_nibble_enum_returns_raw_int(kaitai_prog_parser):
    raw = bytearray(DIFFUSION_LOW.read_bytes())
    raw[100] = 0x0F
    raw[101] = 0x0F
    parsed = kaitai_prog_parser.from_bytes(raw)
    assert parsed.reverb_time.value == 255


def test_kaitai_rejects_out_of_range_nibble(kaitai_prog_parser):
    raw = bytearray(PRESET.read_bytes())
    raw[100] = 0x10
    with pytest.raises(kaitaistruct.ValidationGreaterThanError):
        kaitai_prog_parser.from_bytes(bytes(raw))


@pytest.mark.slow
def test_corpus_value_map_fields_use_enum_members(kaitai_prog_parser):
    """Every locked field on a valid capture should resolve to an enum member."""
    mapped = fields_with_value_map(PROG_FIELDS)
    for path in sorted((SYSEX / "prog" / "parameters" / "diffusion").glob("*.syx")):
        parsed = kaitai_prog_parser.from_bytes(path.read_bytes())
        for field in mapped:
            if field["id"] != "diffusion":
                continue
            assert isinstance(field_parsed_value(parsed, field), Enum), path.name
