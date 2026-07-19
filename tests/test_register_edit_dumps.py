"""Register-basis hold-EDIT dumps under sysex/prog/edit/registers/."""

from pathlib import Path

import pytest

from m7_sysex.frame import (
    BRICASTI_MFR_ID,
    PROGRAM_DUMP_HEADER,
    PROGRAM_MESSAGE_LENGTH,
    PROGRAM_NAME_LENGTH,
    REGISTER_BASIS_BLOB_LENGTH,
    REGISTER_BASIS_BLOB_OFFSET,
    parse_sysex,
    verify_program_dump_checksum,
)
from m7_sysex.names import (
    EDIT_DUMP_BANK_INDEX,
    HINT_BANK_INDEX,
    bank_index_from_raw,
    edit_source_bank_index,
    is_edit_buffer_dump,
    program_slot_from_raw,
    register_page_from_raw,
    register_slot_from_raw,
)

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "sysex" / "prog" / "edit" / "registers"
B0 = REG / "b0-halls-large-hall"
B1 = REG / "b1-halls-large-hall"
SAMPLES = REG / "samples"


def _assert_reg_edit_frame(raw: bytes, *, page: int, slot: int, name_prefix: str) -> None:
    assert len(raw) == PROGRAM_MESSAGE_LENGTH
    frame = parse_sysex(raw)
    assert frame.manufacturer_id == BRICASTI_MFR_ID
    assert frame.header == PROGRAM_DUMP_HEADER
    assert verify_program_dump_checksum(raw)
    assert is_edit_buffer_dump(raw)
    assert bank_index_from_raw(raw) == EDIT_DUMP_BANK_INDEX
    assert register_page_from_raw(raw) == page
    assert raw[94] == 0x08
    assert register_slot_from_raw(raw) == slot
    assert raw[96] == 0x00
    assert frame.name.startswith(name_prefix)
    assert len(frame.name) <= PROGRAM_NAME_LENGTH
    blob = raw[
        REGISTER_BASIS_BLOB_OFFSET : REGISTER_BASIS_BLOB_OFFSET
        + REGISTER_BASIS_BLOB_LENGTH
    ]
    assert all(b <= 0x0F for b in blob), "basis blob should be nibble-packed"
    assert not all(b == 0x20 for b in blob)


@pytest.mark.parametrize("slot", range(10))
def test_b0_halls_large_hall_slots(slot: int):
    path = B0 / f"slot-{slot}.syx"
    assert path.is_file(), path
    raw = path.read_bytes()
    _assert_reg_edit_frame(raw, page=0, slot=slot, name_prefix="Large Hall")
    assert edit_source_bank_index(raw) == HINT_BANK_INDEX["Halls"]
    assert program_slot_from_raw(raw) == 0


@pytest.mark.parametrize("slot", [0, 1])
def test_b1_halls_large_hall_slots(slot: int):
    path = B1 / f"slot-{slot}.syx"
    assert path.is_file(), path
    raw = path.read_bytes()
    _assert_reg_edit_frame(raw, page=1, slot=slot, name_prefix="Large Hall")
    assert edit_source_bank_index(raw) == HINT_BANK_INDEX["Halls"]


def test_sample_ambience_b0s0():
    path = SAMPLES / "ambience-large-ambience-b0s0.syx"
    raw = path.read_bytes()
    _assert_reg_edit_frame(raw, page=0, slot=0, name_prefix="Large Ambience")
    assert edit_source_bank_index(raw) == HINT_BANK_INDEX["Ambience"]


def test_sample_nonlin_b0s2():
    path = SAMPLES / "nonlin-a-b0s2.syx"
    raw = path.read_bytes()
    _assert_reg_edit_frame(raw, page=0, slot=2, name_prefix="Nonlin")
    assert edit_source_bank_index(raw) == HINT_BANK_INDEX["NonLin"]


def test_halls2_subtype_is_documented_outlier():
    """Halls 2 sample may not follow the classic bank-11 Reg EDIT path."""
    path = SAMPLES / "halls2-large-hall-b0s1-subtype.syx"
    assert path.is_file()
    raw = path.read_bytes()
    assert len(raw) == PROGRAM_MESSAGE_LENGTH
    assert verify_program_dump_checksum(raw)
    # Documented outlier: bank left as Halls 2, atypical meta (92=04, 94≠08).
    assert not is_edit_buffer_dump(raw)
    assert bank_index_from_raw(raw) == HINT_BANK_INDEX["Halls 2"]
    assert raw[92] == 0x04
    assert raw[94] != 0x08
    assert register_slot_from_raw(raw) == 1


def test_large_hall_blob_encodes_core_params_at_50_55():
    """Offsets 50–55 match Large Hall predelay / RT / diffusion / density nibbles."""
    factory = (ROOT / "sysex" / "prog" / "presets" / "Halls.Large Hall.syx").read_bytes()
    predelay = (factory[104], factory[105])
    reverb = (factory[100], factory[101])
    diffusion = factory[107]
    density = factory[109]

    reg = (B0 / "slot-0.syx").read_bytes()
    assert (reg[50], reg[51]) == predelay
    assert (reg[52], reg[53]) == reverb
    assert reg[54] == diffusion
    assert reg[55] == density


def test_registers_readme_exists():
    assert (REG / "README.md").is_file()
