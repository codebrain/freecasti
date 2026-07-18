"""Tests for PROG vs SYSTEM dump-family registry."""

from pathlib import Path

from m7_sysex.frame import PROGRAM_MESSAGE_LENGTH, SYSTEM_MESSAGE_LENGTH
from m7_sysex.paths import PROG_DIR, SYSTEM_DIR, corpus_sysex_root, prog_presets_root, system_root
from m7_sysex.types import (
    PROG_FAMILY,
    SYSTEM_FAMILY,
    is_prog_corpus_dump,
    is_prog_corpus_relative,
)

ROOT = Path(__file__).resolve().parents[1]
SYSEX = ROOT / "sysex"


def test_dump_families():
    assert PROG_FAMILY.id == "prog"
    assert SYSTEM_FAMILY.id == "system"
    assert PROG_FAMILY.message_length == PROGRAM_MESSAGE_LENGTH
    assert SYSTEM_FAMILY.message_length == SYSTEM_MESSAGE_LENGTH


def test_is_prog_corpus_relative():
    assert is_prog_corpus_relative(Path("prog/parameters/diffusion/low.syx"))
    assert is_prog_corpus_relative(Path("prog/presets/Halls.Large Hall.syx"))
    assert not is_prog_corpus_relative(Path("system/midi channel/1.syx"))
    assert not is_prog_corpus_relative(Path("prog/edit/stream.syx"))
    assert not is_prog_corpus_relative(Path("prog/menus/size.syx"))
    assert not is_prog_corpus_relative(Path("prog/full sweep/reverb time.syx"))


def test_is_prog_corpus_dump_on_disk():
    preset = next(prog_presets_root(SYSEX).glob("*.syx"))
    system_dump = next(system_root(SYSEX).rglob("*.syx"))
    assert is_prog_corpus_dump(preset, SYSEX)
    assert not is_prog_corpus_dump(system_dump, SYSEX)


def test_path_helpers():
    assert prog_presets_root(SYSEX).name == "presets"
    assert system_root(SYSEX).name == SYSTEM_DIR
    assert PROG_DIR == "prog"


def test_corpus_sysex_root_from_presets():
    assert corpus_sysex_root(prog_presets_root(SYSEX)) == SYSEX.resolve()
