"""Compile Kaitai specs and round-trip every committed SysEx dump."""

from __future__ import annotations

from enum import Enum
from pathlib import Path

import pytest

from m7_sysex.corpus_layout import is_prog_corpus_dump
from m7_sysex.paths import prog_full_sweep_root, prog_menus_root
from m7_sysex.encodings import decode_at_offsets
from m7_sysex.frame import (
    SYSTEM_MESSAGE_LENGTH,
    parse_sysex,
    verify_program_dump_checksum,
    verify_system_dump_checksum,
)
from m7_sysex.prog.decode_preset import PARAMETER_ORDER, build_parameter_decoders, decode_dump_parameters
from m7_sysex.prog.names import (
    EDIT_DUMP_BANK_INDEX,
    HINT_BANK_INDEX,
    bank_index_from_raw,
    bank_name_for_index,
    check_name_bytes,
    edit_source_bank_index,
    is_edit_buffer_dump,
    parse_preset_stem,
    program_slot_from_raw,
)
from tests.kaitai_support import (
    assert_checksum_matches_native,
    assert_message_roundtrip,
    encoded_int_from_field,
    field_parsed_value,
    fields_by_parameter,
    fields_with_value_map,
    load_spec,
    load_spec_fields,
    split_sysex_messages,
)

ROOT = Path(__file__).resolve().parents[1]
SYSEX = ROOT / "sysex"
PROG_SPEC_PATH = ROOT / "specification" / "prog" / "m7_program_dump.spec.json"
SYSTEM_SPEC_PATH = ROOT / "specification" / "system" / "m7_system_dump.spec.json"

PROG_DUMPS = sorted(p for p in SYSEX.rglob("*.syx") if is_prog_corpus_dump(p, SYSEX))
PROG_MENU_DUMPS = sorted(prog_menus_root(SYSEX).glob("*.syx"))
PRESET_DUMPS = sorted((SYSEX / "prog" / "presets").glob("*.syx"))
SYSTEM_DUMPS = sorted(
    p for p in (SYSEX / "system").rglob("*.syx") if "_system" not in p.parts
)
PROG_FIELDS = load_spec_fields(PROG_SPEC_PATH)
SYSTEM_FIELDS = load_spec_fields(SYSTEM_SPEC_PATH)
PROG_PARAM_FIELDS = {
    param: matches[0]
    for param, matches in fields_by_parameter(PROG_FIELDS).items()
    if matches[0].get("value_map")
}
SYSTEM_PARAM_FIELDS = {
    param: matches[0]
    for param, matches in fields_by_parameter(SYSTEM_FIELDS).items()
    if matches[0].get("value_map")
}

PROG_SERIES = sorted(
    p.name
    for p in (SYSEX / "prog" / "parameters").iterdir()
    if p.is_dir() and not p.name.startswith("_")
)
SYSTEM_SERIES = sorted(
    p.name
    for p in (SYSEX / "system").iterdir()
    if p.is_dir() and not p.name.startswith("_")
)
SYSTEM_SERIES_IN_SPEC = sorted(
    name
    for name in SYSTEM_SERIES
    if name in {f.get("parameter") for f in SYSTEM_FIELDS if f.get("value_map")}
)


def test_kaitai_specs_compile(kaitai_prog_parser, kaitai_system_parser):
    """Both committed ``.ksy`` files compile to Python (generated code is ephemeral)."""


@pytest.mark.slow
def test_fresh_exported_specs_compile(kaitai_fresh_prog_parser, kaitai_fresh_system_parser):
    """Live ``write_*_dump_spec`` output also compiles."""


@pytest.mark.slow
@pytest.mark.parametrize(
    "path", PROG_MENU_DUMPS, ids=lambda p: f"prog/menus/{p.name}"
)
def test_prog_menu_kaitai_roundtrip(path: Path, kaitai_prog_parser):
    raw = path.read_bytes()
    assert len(raw) == 157
    assert verify_program_dump_checksum(raw)

    parsed = kaitai_prog_parser.from_bytes(raw)
    assert_message_roundtrip(parsed, raw, PROG_FIELDS, path=path)
    assert_checksum_matches_native(parsed, raw, system=False)


@pytest.mark.slow
def test_prog_menu_ui_bytes_match_analysis(kaitai_prog_parser):
    from m7_sysex.prog.menus import analyze_menus_folder

    analysis = analyze_menus_folder(prog_menus_root(SYSEX), SYSEX)
    browse_field = _field("edit_generation_counter")
    menu_field = _field("selected_menu_index")
    cursor_field = _field("display")

    for capture in analysis["captures"]:
        raw = prog_menus_root(SYSEX) / capture["file"]
        parsed = kaitai_prog_parser.from_bytes(raw.read_bytes())
        ui = capture["ui"]
        assert encoded_int_from_field(parsed, browse_field) == ui["92"], capture["file"]
        assert encoded_int_from_field(parsed, menu_field) == capture["menu_index_encoded"], (
            capture["file"]
        )
        expected_cursor = (ui["146"] << 4) | ui["147"]
        assert encoded_int_from_field(parsed, cursor_field) == expected_cursor, (
            capture["file"]
        )
        _assert_field_resolves_to_enum(parsed, cursor_field, capture["file"])


@pytest.mark.slow
@pytest.mark.parametrize("path", PROG_DUMPS, ids=lambda p: p.relative_to(SYSEX).as_posix())
def test_prog_kaitai_roundtrip(path: Path, kaitai_prog_parser):
    raw = path.read_bytes()
    assert len(raw) == 157
    assert verify_program_dump_checksum(raw)

    parsed = kaitai_prog_parser.from_bytes(raw)
    assert_message_roundtrip(parsed, raw, PROG_FIELDS, path=path)
    assert_checksum_matches_native(parsed, raw, system=False)

    frame = parse_sysex(raw)
    assert parsed.manufacturer_id == bytes(frame.manufacturer_id)
    assert parsed.program_dump_header == bytes(frame.header)


@pytest.mark.slow
@pytest.mark.parametrize(
    "path", SYSTEM_DUMPS, ids=lambda p: p.relative_to(SYSEX / "system").as_posix()
)
def test_system_kaitai_roundtrip(path: Path, kaitai_system_parser):
    raw = path.read_bytes()
    assert len(raw) == SYSTEM_MESSAGE_LENGTH
    assert verify_system_dump_checksum(raw)

    parsed = kaitai_system_parser.from_bytes(raw)
    assert_message_roundtrip(parsed, raw, SYSTEM_FIELDS, path=path)
    assert_checksum_matches_native(parsed, raw, system=True)


@pytest.mark.slow
@pytest.mark.parametrize("series", PROG_SERIES)
def test_prog_parameter_series_match_analysis(series: str, kaitai_prog_parser):
    from m7_sysex.prog.analyze import analyze_parameter_folder

    folder = SYSEX / "prog" / "parameters" / series
    result = analyze_parameter_folder(folder)
    field = PROG_PARAM_FIELDS[result["parameter"]]
    best = result["best_encoding"]
    offsets = list(best["offsets"])
    encoding = best["encoding"]

    for dump in result["dumps"]:
        raw = (folder / dump["file"]).read_bytes()
        parsed = kaitai_prog_parser.from_bytes(raw)
        expected = int(dump["decoded_parameter"]["encoded_value"])
        assert decode_at_offsets(raw, offsets, encoding).value == expected, dump["file"]
        assert encoded_int_from_field(parsed, field) == expected, dump["file"]
        _assert_field_resolves_to_enum(parsed, field, dump["file"])


def _assert_field_resolves_to_enum(parsed, field: dict, label: str) -> None:
    if not field.get("value_map"):
        return
    value = field_parsed_value(parsed, field)
    if field.get("encoding") == "nibble_hilo":
        inner = value.value
        assert isinstance(inner, Enum), label
    else:
        assert isinstance(value, Enum), label


@pytest.mark.slow
@pytest.mark.parametrize("series", SYSTEM_SERIES_IN_SPEC)
def test_system_parameter_series_match_analysis(series: str, kaitai_system_parser):
    from m7_sysex.system.analyze import analyze_system_series_folder

    folder = SYSEX / "system" / series
    result = analyze_system_series_folder(folder)
    field = SYSTEM_PARAM_FIELDS[result["parameter"]]
    best = result["best_encoding"]
    offsets = list(best["offsets"])
    encoding = best["encoding"]

    for dump in result["dumps"]:
        raw = (folder / dump["file"]).read_bytes()
        parsed = kaitai_system_parser.from_bytes(raw)
        expected = int(dump["decoded_parameter"]["encoded_value"])
        assert decode_at_offsets(raw, offsets, encoding).value == expected, dump["file"]
        assert encoded_int_from_field(parsed, field) == expected, dump["file"]
        _assert_field_resolves_to_enum(parsed, field, dump["file"])


@pytest.mark.slow
@pytest.mark.parametrize("path", PRESET_DUMPS, ids=lambda p: p.name)
def test_preset_parameters_match_native_decoders(path: Path, kaitai_prog_parser):
    from m7_sysex.analyze import analyze_tree

    results = analyze_tree(SYSEX)
    decoders = build_parameter_decoders(results, sysex_root=SYSEX)
    raw = path.read_bytes()
    parsed = kaitai_prog_parser.from_bytes(raw)
    native = decode_dump_parameters(raw, decoders)

    assert set(native) == set(PARAMETER_ORDER)
    for param in PARAMETER_ORDER:
        field = PROG_PARAM_FIELDS[param]
        assert encoded_int_from_field(parsed, field) == native[param]["encoded"], param


@pytest.mark.slow
@pytest.mark.parametrize("path", PRESET_DUMPS, ids=lambda p: p.name)
def test_preset_identity_fields_match_filename(path: Path, kaitai_prog_parser):
    bank, preset = parse_preset_stem(path.stem)
    raw = path.read_bytes()
    parsed = kaitai_prog_parser.from_bytes(raw)

    assert check_name_bytes(raw, preset)["name_bytes_match"]
    assert encoded_int_from_field(parsed, _field("bank_index")) == HINT_BANK_INDEX[bank]
    assert program_slot_from_raw(raw) == encoded_int_from_field(
        parsed, _field("program_slot")
    )
    assert bank_index_from_raw(raw) == encoded_int_from_field(
        parsed, _field("bank_index")
    )
    mirror = encoded_int_from_field(parsed, _field("bank_index_mirror"))
    assert mirror == (raw[137] & 0x0F)


def test_full_sweep_reverb_time_roundtrips(kaitai_prog_parser):
    sweep_path = prog_full_sweep_root(SYSEX) / "reverb time.syx"
    messages = split_sysex_messages(sweep_path.read_bytes())
    assert len(messages) == 137
    rt_field = _field("reverb_time")
    encoded_values: list[int] = []

    for raw in messages:
        assert len(raw) == 157
        assert verify_program_dump_checksum(raw)
        parsed = kaitai_prog_parser.from_bytes(raw)
        assert_message_roundtrip(parsed, raw, PROG_FIELDS, path=sweep_path)
        assert_checksum_matches_native(parsed, raw, system=False)
        encoded_values.append(encoded_int_from_field(parsed, rt_field))

    assert encoded_values == list(range(137))


def test_edit_stream_parses_with_edit_bank_index(kaitai_prog_parser):
    edit_path = SYSEX / "prog" / "edit" / "stream.syx"
    bank_field = _field("bank_index")
    mirror_field = _field("bank_index_mirror")

    for raw in split_sysex_messages(edit_path.read_bytes()):
        parsed = kaitai_prog_parser.from_bytes(raw)
        assert is_edit_buffer_dump(raw)
        assert encoded_int_from_field(parsed, bank_field) == EDIT_DUMP_BANK_INDEX
        assert bank_name_for_index(EDIT_DUMP_BANK_INDEX) == "Edit"
        assert encoded_int_from_field(parsed, mirror_field) == edit_source_bank_index(raw)
        assert encoded_int_from_field(parsed, bank_field) != encoded_int_from_field(
            parsed, mirror_field
        )


def test_midi_bank_series_in_system_kaitai_spec():
    """Midi bank primary field is at offset 25 (display level only moves it secondarily)."""
    assert "midi bank" in SYSTEM_PARAM_FIELDS
    field = SYSTEM_PARAM_FIELDS["midi bank"]
    assert field["start"] == 25
    assert field["id"] == "midi_bank"


def _field(field_id: str) -> dict:
    for field in PROG_FIELDS:
        if field["id"] == field_id:
            return field
    raise KeyError(field_id)


def _system_field(field_id: str) -> dict:
    for field in SYSTEM_FIELDS:
        if field["id"] == field_id:
            return field
    raise KeyError(field_id)
