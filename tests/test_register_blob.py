"""Register basis blob decoder: corpus decode, witnesses, round-trip."""

from pathlib import Path

import pytest

from m7_sysex.frame import (
    REGISTER_BASIS_BLOB_LENGTH,
    iter_sysex_messages,
    parse_sysex,
)
from m7_sysex.prog.register_blob import (
    BLOB_BIT_LENGTH,
    INFERRED_CHARSET_CODES,
    REGISTER_BLOB_FIELDS,
    REGISTER_NAME_CHARSET,
    REGISTER_NAME_LENGTH,
    RegisterBasis,
    blob_kind,
    decode_register_blob,
    decode_register_name,
    encode_register_blob,
    encode_register_name,
    frame_blob,
    payload_value,
    register_name_char_enum_entries,
    register_name_codes,
    runtime_reg_blob,
    stored_vs_payload,
)

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "sysex" / "prog" / "edit" / "registers"
SAMPLES = REG / "samples"
FULLSWEEP = REG / "fullsweep-rooms-studio-a.syx"

# Captures whose payload diverges from the blob (unstored edits): the delay
# block was dialed in after the B1 R1 store, and the rt5s-unstored capture
# additionally edited reverb time without storing.
DIVERGENT = {
    "rooms-studio-a-b1s1-delay-edit.syx": {
        "delay_level",
        "delay_time",
        "delay_modulation",
    },
    "charset-b1s1-renamed.syx": {
        "delay_level",
        "delay_time",
        "delay_modulation",
    },
    "charset-b1s1-rt5s-unstored-edit.syx": {
        "reverb_time",
        "delay_level",
        "delay_time",
        "delay_modulation",
    },
}


def _register_frames() -> list[tuple[str, bytes]]:
    out = []
    for path in sorted(REG.rglob("*.syx")):
        for i, msg in enumerate(iter_sysex_messages(path.read_bytes())):
            out.append((f"{path.name}[{i}]", msg))
    return out


FRAMES = _register_frames()


def test_corpus_has_expected_size():
    assert len(FRAMES) >= 66


def test_field_table_covers_256_bits_contiguously():
    covered = 0
    for field in REGISTER_BLOB_FIELDS:
        assert field.bit_offset == covered, field.id
        assert field.bit_width > 0
        covered += field.bit_width
    assert covered == BLOB_BIT_LENGTH == 256


@pytest.mark.parametrize("label,raw", FRAMES, ids=[l for l, _ in FRAMES])
def test_corpus_blob_decodes_and_matches_frame(label: str, raw: bytes):
    frame = parse_sysex(raw)
    blob = frame_blob(raw)
    assert blob_kind(blob) == "register_basis"
    basis = decode_register_blob(blob)

    # Name field matches the ASCII wire name.
    assert basis.name == frame.name

    # Structural constants.
    assert basis.values["pad"] == 0
    assert basis.values["tail"] == 0
    assert basis.values["store_marker"] == 1
    assert 1 <= basis.store_counter <= 31

    # Byte-identical round trip.
    assert encode_register_blob(basis) == blob


@pytest.mark.parametrize("label,raw", FRAMES, ids=[l for l, _ in FRAMES])
def test_blob_params_match_payload_except_witnessed_edits(
    label: str, raw: bytes
):
    filename = label.split("[")[0]
    expected_divergent = DIVERGENT.get(filename, set())
    diverged = stored_vs_payload(raw)
    assert set(diverged) == expected_divergent, label


def test_blob_equals_payload_for_stored_fields_directly():
    """Spot-check payload extraction against the blob on a slot capture."""
    raw = (REG / "b0-halls-large-hall" / "slot-0.syx").read_bytes()
    basis = decode_register_blob(frame_blob(raw))
    for field in REGISTER_BLOB_FIELDS:
        live = payload_value(raw, field)
        if live is None:
            continue
        assert basis.values[field.id] == live, field.id


# --- Charset witnesses -----------------------------------------------------


def test_charset_capture_pins_codes_1_through_25():
    """`&123456789ABCD` witnesses & = 1, '1'-'9' = 3-11, A-D = 12-15."""
    raw = (SAMPLES / "charset-b1s1-renamed.syx").read_bytes()
    codes = register_name_codes(frame_blob(raw))
    assert codes == (1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
    assert decode_register_name(frame_blob(raw)) == "&123456789ABCD"


def test_charset_is_complete_64_entries():
    assert len(REGISTER_NAME_CHARSET) == 64
    assert REGISTER_NAME_CHARSET[0] == " "
    assert REGISTER_NAME_CHARSET[1] == "&"
    assert REGISTER_NAME_CHARSET[2:12] == "0123456789"
    assert REGISTER_NAME_CHARSET[12:38] == "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    assert REGISTER_NAME_CHARSET[38:64] == "abcdefghijklmnopqrstuvwxyz"
    assert INFERRED_CHARSET_CODES == {2}  # digit '0' inferred by continuity


def test_charset_name_round_trip_all_codes():
    for code, ch in enumerate(REGISTER_NAME_CHARSET):
        encoded = encode_register_name(ch)
        assert encoded[0] == code
        assert encoded[1:] == (0,) * (REGISTER_NAME_LENGTH - 1)


def test_encode_register_name_rejects_bad_input():
    with pytest.raises(ValueError):
        encode_register_name("bad!name")
    with pytest.raises(ValueError):
        encode_register_name("X" * (REGISTER_NAME_LENGTH + 1))


def test_register_name_char_enum_entries():
    entries = register_name_char_enum_entries()
    assert len(entries) == 64
    assert entries[0]["name"] == "space"
    assert entries[1]["name"] == "ampersand"
    assert entries[2]["name"] == "digit_0"
    assert "inferred" in entries[2]["label"]
    assert entries[11]["name"] == "digit_9"
    assert entries[12]["name"] == "upper_a"
    assert entries[37]["name"] == "upper_z"
    assert entries[38]["name"] == "lower_a"
    assert entries[63]["name"] == "lower_z"
    assert [e["encoded"] for e in entries] == list(range(64))


# --- Delay-block and stored-snapshot witnesses -------------------------------


def test_stored_capture_carries_delay_block_and_edited_reverb_time():
    """charset-b1s1-rt5s-stored.syx: blob snapshots the stored values."""
    raw = (SAMPLES / "charset-b1s1-rt5s-stored.syx").read_bytes()
    basis = decode_register_blob(frame_blob(raw))
    assert basis.values["reverb_time"] == 76  # 5.0 s, not the factory 10
    assert basis.values["delay_level"] == 15
    assert basis.values["delay_time"] == 11
    assert basis.values["delay_modulation"] == 6
    assert stored_vs_payload(raw) == {}
    # Stored to B1 R0 (operator-confirmed); loaded as the running basis.
    assert raw[93] == 1 and raw[95] == 0
    assert basis.store_counter == 3


def test_unstored_edit_diverges_blob_vs_payload():
    """charset-b1s1-rt5s-unstored-edit.syx: payload edited, blob unchanged."""
    raw = (SAMPLES / "charset-b1s1-rt5s-unstored-edit.syx").read_bytes()
    basis = decode_register_blob(frame_blob(raw))
    diff = stored_vs_payload(raw)
    assert diff["reverb_time"] == (10, 76)  # stored 1.0 s, live 5.0 s
    assert basis.values["reverb_time"] == 10


def test_delay_edit_capture_has_zero_delay_in_blob():
    """Delay dialed in after the store: payload only."""
    raw = (SAMPLES / "rooms-studio-a-b1s1-delay-edit.syx").read_bytes()
    basis = decode_register_blob(frame_blob(raw))
    assert basis.values["delay_level"] == 0
    assert basis.values["delay_time"] == 0
    assert basis.values["delay_modulation"] == 0
    diff = stored_vs_payload(raw)
    assert diff["delay_level"] == (0, 15)
    assert diff["delay_time"] == (0, 11)
    assert diff["delay_modulation"] == (0, 6)


# --- Store-generation counter witnesses --------------------------------------


def test_fullsweep_store_counter_pattern():
    """Counters 3 for B0 R0-R2, 2 for B0 R3-B1 R1, 1 for the rest."""
    frames = list(iter_sysex_messages(FULLSWEEP.read_bytes()))
    assert len(frames) == 50
    counters = [
        decode_register_blob(frame_blob(raw)).store_counter for raw in frames
    ]
    assert counters[:3] == [3, 3, 3]
    assert counters[3:12] == [2] * 9
    assert counters[12:] == [1] * 38


def test_rename_capture_counter_is_5():
    """Renaming stores twice: 3 (delay-edit) + 2 = 5."""
    raw = (SAMPLES / "charset-b1s1-renamed.syx").read_bytes()
    assert decode_register_blob(frame_blob(raw)).store_counter == 5


def test_delay_edit_capture_counter_is_3():
    raw = (SAMPLES / "rooms-studio-a-b1s1-delay-edit.syx").read_bytes()
    assert decode_register_blob(frame_blob(raw)).store_counter == 3


# --- Classification and error paths ------------------------------------------


def test_factory_blob_classified_and_rejected():
    factory = (
        ROOT / "sysex" / "prog" / "presets" / "Halls.Large Hall.syx"
    ).read_bytes()
    blob = frame_blob(factory)
    assert blob == b" " * REGISTER_BASIS_BLOB_LENGTH
    assert blob_kind(blob) == "factory_pad"
    with pytest.raises(ValueError):
        decode_register_blob(blob)


def test_blob_kind_unknown_and_length_check():
    assert blob_kind(bytes([0x00] * 63 + [0x77])) == "unknown"
    with pytest.raises(ValueError):
        blob_kind(b"\x00" * 10)


def test_encode_rejects_out_of_range_values():
    raw = (REG / "b0-halls-large-hall" / "slot-0.syx").read_bytes()
    basis = decode_register_blob(frame_blob(raw))
    bad = RegisterBasis(
        name=basis.name, values={**basis.values, "diffusion": 16}
    )
    with pytest.raises(ValueError):
        encode_register_blob(bad)


def test_runtime_reg_blob_shape():
    rt = runtime_reg_blob()
    assert rt["charset"] == REGISTER_NAME_CHARSET
    assert rt["name_length"] == 14
    assert rt["char_bits"] == 6
    assert rt["blob_offset"] == 24
    assert rt["blob_length"] == 64
    ids = [f["id"] for f in rt["fields"]]
    assert ids == [f.id for f in REGISTER_BLOB_FIELDS]
    delay = next(f for f in rt["fields"] if f["id"] == "delay_time")
    assert delay["bit"] == 201 and delay["width"] == 7
    assert delay["payloadField"] == "delay_time"
    assert delay["payloadOffsets"] == [134, 135]
