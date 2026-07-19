"""Corpus-wide validation: every committed .syx dump must satisfy the parser
and the layout claims documented in corpus_layout / docs.

These tests are the ground-truth check that code declarations (frame constants,
checksum, reserved/meta bytes, identity fields) agree with the actual dumps.
"""

from pathlib import Path

import pytest

from m7_sysex.corpus_layout import CORPUS_LAYOUT_CLAIMS, is_prog_corpus_dump, verify_corpus_constants
from m7_sysex.frame import (
    BRICASTI_MFR_ID,
    DATA_OFFSET,
    PROGRAM_DUMP_HEADER,
    is_nibble_payload,
    parse_sysex,
    verify_program_dump_checksum,
)
from m7_sysex.names import (
    HINT_BANK_INDEX,
    bank_index_from_raw,
    parse_preset_stem,
    program_slot_from_raw,
)

ROOT = Path(__file__).resolve().parents[1]
SYSEX = ROOT / "sysex"

ALL_DUMPS = sorted(p for p in SYSEX.rglob("*.syx") if is_prog_corpus_dump(p, SYSEX))
PRESET_DUMPS = sorted((SYSEX / "prog" / "presets").glob("*.syx"))
SYSTEM_DUMPS = sorted(
    p
    for p in (SYSEX / "system").rglob("*.syx")
    if "_system" not in p.parts
)


def test_corpus_is_present():
    assert len(ALL_DUMPS) > 300
    assert len(PRESET_DUMPS) > 200


def test_every_dump_parses_with_valid_frame_and_checksum():
    for path in ALL_DUMPS:
        raw = path.read_bytes()
        frame = parse_sysex(raw)
        assert frame.manufacturer_id == BRICASTI_MFR_ID, path
        assert frame.header == PROGRAM_DUMP_HEADER, path
        assert len(raw) == 157, path
        assert verify_program_dump_checksum(raw), path
        assert is_nibble_payload(raw[DATA_OFFSET:-1]), path
        # Name field is printable ASCII on factory/parameter dumps (8–87 spaces).
        assert all(32 <= b < 127 for b in raw[8:88]), path


def test_corpus_layout_constant_claims_hold():
    """Every 'reserved'/'fixed' offset claimed in corpus_layout is constant."""
    constants = verify_corpus_constants(SYSEX)
    expected_fixed = {
        93: 0,  # register page (0 on factory corpus)
        94: 8,  # structure version
        95: 0,  # register slot (0 on factory corpus)
        96: 0,
        106: 0,
        108: 0,
        110: 0,
        131: 2,
        132: 0,  # fixed companion `02 00`
        136: 0,
        138: 0,
        140: 0,
        141: 0,
        142: 0,
        143: 0,
        144: 0,
        148: 0,
        149: 0,
        150: 0,
        151: 0,
    }
    for off, value in expected_fixed.items():
        assert constants.get(off) == value, f"offset {off}"


def test_corpus_layout_claims_cover_expected_offsets():
    claimed = sorted(o for spec in CORPUS_LAYOUT_CLAIMS for o in spec["offsets"])
    assert claimed == [
        92, 93, 94, 95, 96, 97, 98, 99, 106, 108, 110, 130, 131, 132,
        136, 138, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151,
    ]


def test_bank_mirror_and_family_flag_mirror_relations():
    """137 mirrors bank low nibble (89); 145 mirrors family flag (97: 3->0, 4->1)."""
    for path in ALL_DUMPS:
        raw = path.read_bytes()
        assert raw[137] == raw[89], path
        assert raw[97] in (3, 4), path
        assert raw[145] == {3: 0, 4: 1}[raw[97]], path


def test_preset_bank_indices_match_addendum_table():
    seen: dict[str, set[int]] = {}
    for path in PRESET_DUMPS:
        raw = path.read_bytes()
        bank, _preset = parse_preset_stem(path.stem)
        seen.setdefault(bank, set()).add(bank_index_from_raw(raw))
    assert seen
    for bank, indices in seen.items():
        assert indices == {HINT_BANK_INDEX[bank]}, bank


def test_engine_bank_class_flag_by_bank():
    """Offset 130: 0 for classic banks, 1 for `* 2` banks, 2 for NonLin."""
    classic = {"Halls", "Plates", "Rooms", "Chambers", "Ambience", "Spaces"}
    v2 = {"Halls 2", "Plates 2", "Rooms 2", "Spaces 2"}
    for path in PRESET_DUMPS:
        raw = path.read_bytes()
        bank, _preset = parse_preset_stem(path.stem)
        expected = 0 if bank in classic else (1 if bank in v2 else 2)
        assert raw[130] == expected, path


def test_program_slot_nibble_hilo_proved_by_rooms_slot_35():
    """Rooms Long Wood Room sits at slot 35 = `02 03` - proves nibble packing."""
    path = SYSEX / "prog" / "presets" / "Rooms.Long Wood Room.syx"
    raw = path.read_bytes()
    assert (raw[90], raw[91]) == (0x02, 0x03)
    assert program_slot_from_raw(raw) == 35


def test_bank_slots_are_contiguous_from_zero():
    slots_by_bank: dict[str, list[int]] = {}
    for path in PRESET_DUMPS:
        raw = path.read_bytes()
        bank, _preset = parse_preset_stem(path.stem)
        slots_by_bank.setdefault(bank, []).append(program_slot_from_raw(raw))
    for bank, slots in slots_by_bank.items():
        slots = sorted(slots)
        assert slots[0] == 0, bank
        assert len(set(slots)) == len(slots), f"duplicate slot in {bank}"
        assert slots == list(range(len(slots))), bank


def test_family_flag_exceptions_are_bank_leading_presets():
    """Non-Halls presets with family flag 3 are exactly the documented four
    (all at slot 0 in their bank) - see docs/manual-notes.md."""
    exceptions = set()
    for path in PRESET_DUMPS:
        raw = path.read_bytes()
        bank, preset = parse_preset_stem(path.stem)
        if raw[97] == 3 and bank != "Halls":
            assert program_slot_from_raw(raw) == 0, path
            exceptions.add((bank, preset))
    assert exceptions == {
        ("Chambers", "Large Chamber"),
        ("Halls 2", "Large Hall"),
        ("Plates", "Bright Plate"),
        ("Rooms", "Studio A"),
    }


def test_size_sheet_l_matches_dump_large():
    """Sheet ``L`` / ``Large`` are the same Size extreme as dump ``large``."""
    from m7_sysex.preset_sheet import parse_ours_value, parse_sheet_value

    assert parse_sheet_value("size", "L") == ("tok", "large")
    assert parse_sheet_value("size", "Large") == ("tok", "large")
    assert parse_sheet_value("size", "Sm") == ("tok", "small")
    assert parse_ours_value("size", "large") == ("tok", "large")
    # ``L`` must not be treated as Low (that mapping is for density/diffusion).
    assert parse_sheet_value("density", "L") == ("num", 0.0)


def test_preset_sheet_compare_regression():
    """Decoded presets vs the committed published-sheet JSON.

    Counts are a regression snapshot of the committed corpus + sheet data;
    update deliberately when captures or decoders change.
    """
    from m7_sysex.preset_sheet import run_compare

    analysis = SYSEX / "prog" / "presets" / "analysis.json"
    if not analysis.is_file():
        pytest.skip("run `python run.py` first to decode presets")

    result = run_compare(sysex_root=SYSEX)
    assert result["matched_count"] == 98
    # Densified table maps (series + provided + sheet anchors) keep most classic
    # presets exact; remaining hard rows are documented errata.
    # Early/reverb mix compares path position (A/B), so former false "20 vs 20.9"
    # hard rows are exact matches. Size sheet ``L`` == dump ``large``.
    # Provided UI walks supply exact dump labels (no ``~`` interpolation) when
    # preset decode resolves the corpus root correctly.
    assert result["hard_count"] == 8
    assert result["exact_count"] == 87
    assert result["soft_only_count"] == 3
    hard_keys = {
        (c["bank"], c["preset"], iss["param"])
        for c in result["comparisons"]
        for iss in c["hard"]
    }
    assert ("Spaces", "Tanglewood", "size") not in hard_keys
    assert ("Spaces", "Redwood Valley", "predelay") in hard_keys
    assert ("Ambience", "Medium & Dark", "early rolloff") not in hard_keys
    assert ("Spaces", "Stone Quarry", "reverb time") not in hard_keys
    # Every Halls 2 dump is intentionally skipped (not on the classic sheet).
    assert all(r["bank"] == "Halls 2" for r in result["skipped_banks"])
