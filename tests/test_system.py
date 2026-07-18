"""Tests for M7 system-dump SysEx (sysex/system/)."""

from pathlib import Path

import pytest

from m7_sysex.frame import (
    BRICASTI_MFR_ID,
    SYSTEM_DUMP_HEADER,
    SYSTEM_MESSAGE_LENGTH,
    is_nibble_payload,
    parse_system_sysex,
    system_dump_checksum,
    verify_system_dump_checksum,
)
from m7_sysex.system import analyze_system_series_folder, analyze_system_tree

ROOT = Path(__file__).resolve().parents[1]
SYSEX = ROOT / "sysex"
SYSTEM = SYSEX / "system"

SYSTEM_DUMPS = sorted(SYSTEM.rglob("*.syx"))


def test_system_corpus_is_present():
    assert len(SYSTEM_DUMPS) == 73


@pytest.mark.parametrize("path", SYSTEM_DUMPS, ids=lambda p: p.relative_to(SYSTEM).as_posix())
def test_every_system_dump_parses_with_valid_frame_and_checksum(path: Path):
    raw = path.read_bytes()
    frame = parse_system_sysex(raw)
    assert frame.manufacturer_id == BRICASTI_MFR_ID
    assert frame.header == SYSTEM_DUMP_HEADER
    assert len(raw) == SYSTEM_MESSAGE_LENGTH
    assert verify_system_dump_checksum(raw)
    assert is_nibble_payload(raw[8:72])


def test_system_checksum_round_trip_after_edit():
    raw = bytearray(SYSTEM_DUMPS[0].read_bytes())
    assert verify_system_dump_checksum(bytes(raw))
    raw[20] = (raw[20] + 1) % 16
    assert not verify_system_dump_checksum(bytes(raw))
    raw[72:76] = system_dump_checksum(bytes(raw))
    assert verify_system_dump_checksum(bytes(raw))


def test_audio_routing_encoding():
    result = analyze_system_series_folder(SYSTEM / "audio routing")
    best = result["best_encoding"]
    assert best is not None
    assert best["encoding"] == "raw_u8"
    assert best["offsets"] == [13]
    assert best["score"] == 1.0

    enc_by_stem: dict[str, int] = {}
    for dump in result["dumps"]:
        dec = dump["decoded_parameter"]
        enc_by_stem[dump["label"]["stem"]] = dec["encoded_value"]

    assert enc_by_stem["Stereo"] == 0
    assert enc_by_stem["Mono L"] == 1
    assert enc_by_stem["Mono R"] == 2


def test_analyze_system_tree_finds_eight_series():
    results = analyze_system_tree(SYSEX)
    names = {r["parameter"] for r in results}
    assert names == {
        "audio format",
        "audio routing",
        "dry gain",
        "midi bank",
        "midi channel",
        "display level",
        "output level",
        "wet gain",
    }
    assert sum(r["dump_count"] for r in results) == 61


def test_dry_gain_encoding():
    result = analyze_system_series_folder(SYSTEM / "dry gain")
    best = result["best_encoding"]
    assert best is not None
    assert best["encoding"] == "nibble_hilo"
    assert best["offsets"] == [10, 11]
    assert best["scale"] == 0.5
    assert best["offset"] == -60.5
    assert best["score"] == 1.0

    by_label = {
        d["label"]["value"]: d["decoded_parameter"]["encoded_value"]
        for d in result["dumps"]
        if d["label"]["kind"] == "number"
    }
    assert by_label[-60] == 1
    assert by_label[-59.5] == 2
    assert by_label[-59] == 3
    assert by_label[-45.5] == 30
    assert by_label[-30.5] == 60
    assert by_label[-1] == 119
    assert by_label[-0.5] == 120

    off = next(d for d in result["dumps"] if d["label"]["endpoint"] == "off")
    full = next(d for d in result["dumps"] if d["label"]["endpoint"] == "high")
    assert off["decoded_parameter"]["encoded_value"] == 0
    assert full["decoded_parameter"]["encoded_value"] == 121


def test_dry_gain_full_encoding_map_half_db_steps():
    from m7_sysex.export import _full_encoding_rows

    result = analyze_system_series_folder(SYSTEM / "dry gain")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=None
    )
    assert densified is not None
    by_enc = {int(r["encoded"]): r for r in densified}
    assert sorted(by_enc) == list(range(0, 122))
    assert by_enc[0]["display"] == "off"
    assert by_enc[1]["label"] == -60
    assert by_enc[2]["label"] == -59.5
    assert by_enc[3]["label"] == -59
    assert by_enc[30]["label"] == -45.5
    assert by_enc[120]["label"] == -0.5
    assert by_enc[121]["display"] == "full"


def test_wet_gain_encoding():
    result = analyze_system_series_folder(SYSTEM / "wet gain")
    best = result["best_encoding"]
    assert best is not None
    assert best["encoding"] == "nibble_hilo"
    assert best["offsets"] == [8, 9]
    assert best["scale"] == 0.5
    assert best["offset"] == -60.5
    assert best["score"] == 1.0

    by_label = {
        d["label"]["value"]: d["decoded_parameter"]["encoded_value"]
        for d in result["dumps"]
        if d["label"]["kind"] == "number"
    }
    assert by_label[-60] == 1
    assert by_label[-59.5] == 2
    assert by_label[-0.5] == 120

    off = next(d for d in result["dumps"] if d["label"]["endpoint"] == "off")
    full = next(d for d in result["dumps"] if d["label"]["endpoint"] == "high")
    assert off["decoded_parameter"]["encoded_value"] == 0
    assert full["decoded_parameter"]["encoded_value"] == 121


def test_wet_gain_full_encoding_map_half_db_steps():
    from m7_sysex.export import _full_encoding_rows

    result = analyze_system_series_folder(SYSTEM / "wet gain")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=None
    )
    assert densified is not None
    by_enc = {int(r["encoded"]): r for r in densified}
    assert sorted(by_enc) == list(range(0, 122))
    assert by_enc[0]["display"] == "off"
    assert by_enc[1]["label"] == -60
    assert by_enc[2]["label"] == -59.5
    assert by_enc[120]["label"] == -0.5
    assert by_enc[121]["display"] == "full"
    assert by_enc[38]["label"] == -41.5


def test_wet_gain_full_encoding_map_ignores_spurious_preset_anchors():
    from m7_sysex.export import _full_encoding_rows

    root = Path(__file__).resolve().parents[1]
    result = analyze_system_series_folder(SYSTEM / "wet gain")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {int(r["encoded"]): r for r in densified}
    assert sorted(by_enc) == list(range(0, 122))
    assert by_enc[121]["display"] == "full"


def test_dry_gain_full_encoding_map_ignores_spurious_preset_anchors():
    from m7_sysex.export import _full_encoding_rows

    root = Path(__file__).resolve().parents[1]
    result = analyze_system_series_folder(SYSTEM / "dry gain")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {int(r["encoded"]): r for r in densified}
    assert sorted(by_enc) == list(range(0, 122))
    assert by_enc[121]["display"] == "full"


def test_midi_bank_encoding():
    result = analyze_system_series_folder(SYSTEM / "midi bank")
    best = result["best_encoding"]
    assert best is not None
    assert best["encoding"] == "raw_u8"
    assert best["offsets"] == [25]
    assert best["score"] == 1.0

    enc_by_stem: dict[str, int] = {}
    for dump in result["dumps"]:
        dec = dump["decoded_parameter"]
        enc_by_stem[dump["label"]["stem"]] = dec["encoded_value"]

    assert enc_by_stem["Halls"] == 0
    assert enc_by_stem["Plates"] == 1
    assert enc_by_stem["Rooms"] == 2
    assert enc_by_stem["Chambers"] == 3
    assert enc_by_stem["Ambience"] == 4
    assert enc_by_stem["Spaces"] == 5
    assert enc_by_stem["Halls 2"] == 6
    assert enc_by_stem["Plates 2"] == 7
    assert enc_by_stem["Rooms 2"] == 8
    assert enc_by_stem["Spaces 2"] == 9
    assert enc_by_stem["NonLin"] == 0x0A
    assert enc_by_stem["Edit"] == 0x0B
    assert enc_by_stem["Regs"] == 0x0C
    assert enc_by_stem["Favs"] == 0x0D


def test_midi_bank_full_encoding_map():
    from m7_sysex.export import _full_encoding_rows

    result = analyze_system_series_folder(SYSTEM / "midi bank")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=None
    )
    assert densified is not None
    by_enc = {int(r["encoded"]): r for r in densified}
    assert len(by_enc) == 14
    assert by_enc[0]["display"] == "halls"
    assert by_enc[0x0D]["display"] == "favs"


def test_midi_channel_encoding():
    result = analyze_system_series_folder(SYSTEM / "midi channel")
    best = result["best_encoding"]
    assert best is not None
    assert best["encoding"] == "nibble_hilo"
    assert best["offsets"] == [22, 23]

    enc_by_stem: dict[str, int] = {}
    for dump in result["dumps"]:
        dec = dump["decoded_parameter"]
        enc_by_stem[dump["label"]["stem"]] = dec["encoded_value"]

    assert enc_by_stem["1"] == 0
    assert enc_by_stem["16"] == 15
    assert enc_by_stem["omni"] == 16


def test_midi_channel_full_encoding_map_includes_omni():
    from m7_sysex.export import _full_encoding_rows

    result = analyze_system_series_folder(SYSTEM / "midi channel")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=None
    )
    assert densified is not None
    by_enc = {int(r["encoded"]): r for r in densified}
    assert by_enc[16]["display"] == "omni"


def test_display_level_encoding():
    result = analyze_system_series_folder(SYSTEM / "display level")
    best = result["best_encoding"]
    assert best is not None
    assert best["encoding"] == "raw_u8"
    assert best["offsets"] == [21]

    by_stem = {
        d["label"]["stem"]: d["decoded_parameter"]["encoded_value"]
        for d in result["dumps"]
        if "decoded_parameter" in d
    }
    assert by_stem["dim"] == 0
    assert by_stem["1"] == 1
    assert by_stem["3"] == 3
    assert by_stem["bright"] == 4


def test_display_level_full_encoding_map_includes_enum_dumps():
    from m7_sysex.export import _full_encoding_rows

    result = analyze_system_series_folder(SYSTEM / "display level")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=None
    )
    assert densified is not None
    by_enc = {int(r["encoded"]): r for r in densified}
    assert sorted(by_enc) == [0, 1, 2, 3, 4]
    assert by_enc[0]["display"] == "dim"
    assert by_enc[4]["display"] == "bright"
    assert by_enc[1]["label"] == 1
    assert by_enc[2]["label"] == 2
    assert by_enc[3]["label"] == 3


def test_output_level_encoding():
    result = analyze_system_series_folder(SYSTEM / "output level")
    best = result["best_encoding"]
    assert best is not None
    assert best["encoding"] == "raw_u8"
    assert best["offsets"] == [17]

    by_label = {
        d["label"]["value"]: d["decoded_parameter"]["encoded_value"]
        for d in result["dumps"]
    }
    assert by_label[8] == 0
    assert by_label[16] == 1
    assert by_label[24] == 2


def test_output_level_full_encoding_map_only_three_steps():
    from m7_sysex.export import _full_encoding_rows

    root = Path(__file__).resolve().parents[1]
    result = analyze_system_series_folder(SYSTEM / "output level")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {int(r["encoded"]): r for r in densified}
    assert sorted(by_enc) == [0, 1, 2]
    assert by_enc[0]["display"] == "-8 dB"
    assert by_enc[1]["display"] == "-16 dB"
    assert by_enc[2]["display"] == "-24 dB"


def test_display_level_full_encoding_map_ignores_spurious_preset_anchors():
    from m7_sysex.export import _full_encoding_rows

    root = Path(__file__).resolve().parents[1]
    result = analyze_system_series_folder(SYSTEM / "display level")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {int(r["encoded"]): r for r in densified}
    assert sorted(by_enc) == [0, 1, 2, 3, 4]
    assert by_enc[0]["display"] == "dim"
    assert by_enc[4]["display"] == "bright"


def test_parse_system_sysex_rejects_prog_dump():
    prog = next(
        p
        for p in SYSEX.rglob("*.syx")
        if p.relative_to(SYSEX).parts[0] != "system"
    )
    with pytest.raises(ValueError, match="system SysEx length"):
        parse_system_sysex(prog.read_bytes())
