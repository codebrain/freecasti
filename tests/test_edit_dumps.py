"""Hold-EDIT buffer dumps under sysex/prog/edit/."""

from pathlib import Path

from m7_sysex.frame import (
    BRICASTI_MFR_ID,
    PROGRAM_DUMP_HEADER,
    PROGRAM_MESSAGE_LENGTH,
    parse_sysex,
    verify_program_dump_checksum,
)
from m7_sysex.names import (
    EDIT_DUMP_BANK_INDEX,
    HINT_BANK_INDEX,
    bank_index_from_raw,
    bank_name_for_index,
    edit_source_bank_index,
    is_edit_buffer_dump,
    program_slot_from_raw,
)

ROOT = Path(__file__).resolve().parents[1]
EDIT = ROOT / "sysex" / "prog" / "edit"


def _split_sysex_messages(data: bytes) -> list[bytes]:
    msgs: list[bytes] = []
    i = 0
    while i < len(data):
        if data[i] == 0xF0:
            j = i + 1
            while j < len(data) and data[j] != 0xF7:
                j += 1
            if j < len(data):
                msgs.append(data[i : j + 1])
                i = j + 1
                continue
        i += 1
    return msgs


def test_edit_stream_messages_are_prog_framed_with_bank_11():
    path = EDIT / "stream.syx"
    assert path.is_file()
    msgs = _split_sysex_messages(path.read_bytes())
    assert len(msgs) >= 1
    for raw in msgs:
        assert len(raw) == PROGRAM_MESSAGE_LENGTH
        frame = parse_sysex(raw)
        assert frame.manufacturer_id == BRICASTI_MFR_ID
        assert frame.header == PROGRAM_DUMP_HEADER
        assert verify_program_dump_checksum(raw)
        assert is_edit_buffer_dump(raw)
        assert bank_index_from_raw(raw) == EDIT_DUMP_BANK_INDEX
        assert bank_name_for_index(EDIT_DUMP_BANK_INDEX) == "Edit"
        # Mirror keeps the source factory bank; bank word does not.
        assert raw[137] != raw[89]
        source = edit_source_bank_index(raw)
        assert source in HINT_BANK_INDEX.values()
        assert bank_name_for_index(source) is not None


def test_edit_stream_source_bank_is_rooms_for_sf_perf_room():
    msgs = _split_sysex_messages((EDIT / "stream.syx").read_bytes())
    for raw in msgs:
        assert parse_sysex(raw).name == "SF Perf Room"
        assert edit_source_bank_index(raw) == HINT_BANK_INDEX["Rooms"]
        assert program_slot_from_raw(raw) == 0
