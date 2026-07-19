"""Tests for the spec-driven dump codec and the decode/encode CLI."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from m7_sysex.cli import main as cli_main
from m7_sysex.dump_codec import decode_dump, detect_dump_kind, encode_dump
from m7_sysex.frame import (
    verify_program_dump_checksum,
    verify_system_dump_checksum,
)

ROOT = Path(__file__).resolve().parents[1]
PROG_SAMPLE = ROOT / "sysex" / "prog" / "parameters" / "diffusion" / "low.syx"
PRESET_SAMPLE = ROOT / "sysex" / "prog" / "presets" / "Ambience.Clear Ambience.syx"
REGISTER_SAMPLE = (
    ROOT
    / "sysex"
    / "prog"
    / "edit"
    / "registers"
    / "samples"
    / "charset-b1s1-renamed.syx"
)
SYSTEM_SAMPLE = ROOT / "sysex" / "system" / "midi channel" / "1.syx"


def test_detect_dump_kind():
    assert detect_dump_kind(PROG_SAMPLE.read_bytes()) == "prog"
    assert detect_dump_kind(SYSTEM_SAMPLE.read_bytes()) == "system"
    with pytest.raises(ValueError, match="unrecognized dump header"):
        detect_dump_kind(b"\xf0\x00\x62\x63\x00\x00\x00\x00\xf7")


def test_decode_prog_dump_fields():
    doc = decode_dump(PRESET_SAMPLE.read_bytes())
    assert doc["kind"] == "prog"
    assert doc["checksum_ok"] is True
    assert doc["program_name"] == "Clear Ambience"
    fields = doc["fields"]
    assert "reverb_time" in fields
    assert isinstance(fields["reverb_time"]["encoded"], int)
    assert fields["reverb_time"]["display"].endswith("s")
    assert fields["register_basis_blob"]["blob_kind"] == "factory_pad"


def test_decode_register_basis_blob():
    doc = decode_dump(REGISTER_SAMPLE.read_bytes())
    blob = doc["fields"]["register_basis_blob"]
    assert blob["blob_kind"] == "register_basis"
    assert blob["register"]["name"] == "&123456789ABCD"


def test_decode_system_dump():
    doc = decode_dump(SYSTEM_SAMPLE.read_bytes())
    assert doc["kind"] == "system"
    assert doc["checksum_ok"] is True
    assert doc["fields"]["midi_channel"]["encoded"] >= 0


@pytest.mark.parametrize(
    "sample",
    [PROG_SAMPLE, PRESET_SAMPLE, REGISTER_SAMPLE, SYSTEM_SAMPLE],
    ids=lambda p: p.stem,
)
def test_decode_encode_round_trip(sample: Path):
    raw = sample.read_bytes()
    doc = decode_dump(raw)
    assert encode_dump(doc) == raw


def test_encode_minimal_document_uses_skeleton():
    doc = {
        "kind": "prog",
        "fields": {
            "program_name": {"text": "Codec Test"},
            "reverb_time": {"encoded": 36},
        },
    }
    raw = encode_dump(doc)
    assert len(raw) == 157
    assert verify_program_dump_checksum(raw)
    decoded = decode_dump(raw)
    assert decoded["program_name"] == "Codec Test"
    assert decoded["fields"]["reverb_time"]["encoded"] == 36


def test_encode_minimal_system_document():
    doc = {"kind": "system", "fields": {"midi_channel": {"encoded": 3}}}
    raw = encode_dump(doc)
    assert len(raw) == 77
    assert verify_system_dump_checksum(raw)
    assert decode_dump(raw)["fields"]["midi_channel"]["encoded"] == 3


def test_encode_rejects_unknown_fields():
    with pytest.raises(ValueError, match="unknown field ids"):
        encode_dump({"kind": "prog", "fields": {"bogus": {"encoded": 1}}})


def test_cli_decode_summary(capsys):
    assert cli_main(["decode", str(PRESET_SAMPLE)]) == 0
    out = capsys.readouterr().out
    assert "Clear Ambience" in out
    assert "checksum: OK" in out
    assert "reverb time" in out


def test_cli_decode_json_output(tmp_path, capsys):
    out_path = tmp_path / "decoded.json"
    assert cli_main(["decode", str(PRESET_SAMPLE), "--json", "-o", str(out_path)]) == 0
    printed = json.loads(
        capsys.readouterr().out.split("wrote ")[0]
    )
    assert printed["program_name"] == "Clear Ambience"
    on_disk = json.loads(out_path.read_text(encoding="utf-8"))
    assert on_disk == printed


def test_cli_decode_reports_bad_checksum(tmp_path, capsys):
    raw = bytearray(PRESET_SAMPLE.read_bytes())
    raw[100] ^= 0x01  # corrupt a payload nibble without touching the checksum
    bad = tmp_path / "bad.syx"
    bad.write_bytes(bytes(raw))
    assert cli_main(["decode", str(bad)]) == 1
    assert "checksum: INVALID" in capsys.readouterr().out


def test_cli_decode_encode_round_trip(tmp_path, capsys):
    doc_path = tmp_path / "doc.json"
    out_syx = tmp_path / "out.syx"
    assert cli_main(["decode", str(PRESET_SAMPLE), "-o", str(doc_path)]) == 0
    assert cli_main(["encode", str(doc_path), str(out_syx)]) == 0
    capsys.readouterr()
    assert out_syx.read_bytes() == PRESET_SAMPLE.read_bytes()


def test_cli_encode_rejects_missing_file(tmp_path, capsys):
    assert cli_main(["encode", str(tmp_path / "nope.json"), str(tmp_path / "o.syx")]) == 1
    assert "file not found" in capsys.readouterr().err
