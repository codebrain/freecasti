"""Factual claims made in the hand-written docs, verified against the corpus.

Covers README.md, docs/capture-guide.md, docs/parameter-catalog.md,
docs/manual-notes.md, docs/kaitai-encode.md, docs/README.md,
docs/development.md, and web-ui/README.md. Each test names the doc making the
claim; a failure means either the doc went stale or a regression broke the
documented behavior.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from m7_sysex.encodings import encode_at_offsets
from m7_sysex.frame import iter_sysex_messages, parse_sysex
from m7_sysex.names import EDIT_DUMP_BANK_INDEX, HINT_BANK_INDEX
from m7_sysex.types import is_prog_corpus_dump

ROOT = Path(__file__).resolve().parents[1]
SYSEX = ROOT / "sysex"
DOCS = ROOT / "docs"
PARAMETERS = SYSEX / "prog" / "parameters"
SYSTEM = SYSEX / "system"


def _analysis(folder: Path) -> dict:
    path = folder / "analysis.json"
    if not path.is_file():
        pytest.skip(f"run `python run.py` first ({path} missing)")
    return json.loads(path.read_text(encoding="utf-8"))


def _parameter_folders() -> list[Path]:
    return sorted(
        p for p in PARAMETERS.iterdir() if p.is_dir() and not p.name.startswith("_")
    )


def _system_folders() -> list[Path]:
    return sorted(
        p
        for p in SYSTEM.iterdir()
        if p.is_dir() and not p.name.startswith("_") and p.name != "menus"
    )


# --- README.md -------------------------------------------------------------


def test_readme_corpus_counts_match_prose():
    """README status table: 'validated on **N** PROG corpus dumps + **M**
    SYSTEM dumps (**T** total)' must match the committed corpus."""
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    m = re.search(
        r"validated on \*\*(\d+)\*\* PROG corpus dumps \+ \*\*(\d+)\*\* SYSTEM "
        r"dumps \(\*\*(\d+)\*\* total\)",
        text,
    )
    assert m, "README frame-status sentence not found"
    claimed_prog, claimed_system, claimed_total = map(int, m.groups())

    prog_msgs = sum(
        len(list(iter_sysex_messages(p.read_bytes())))
        for p in (SYSEX / "prog").rglob("*.syx")
        if is_prog_corpus_dump(p, SYSEX)
    )
    system_msgs = sum(
        len(list(iter_sysex_messages(p.read_bytes())))
        for p in SYSTEM.rglob("*.syx")
    )
    assert claimed_prog == prog_msgs
    assert claimed_system == system_msgs
    assert claimed_total == prog_msgs + system_msgs


def test_readme_preset_and_series_counts():
    """README: '**222 captured**' presets, 18 parameter series, 8 SYSTEM
    settings."""
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*(\d+) captured\*\*", text)
    assert m, "README preset-count claim not found"
    presets = len(list((SYSEX / "prog" / "presets").glob("*.syx")))
    assert int(m.group(1)) == presets
    assert len(_parameter_folders()) == 18
    assert len(_system_folders()) == 8


def test_readme_provided_labels_inventory():
    """README + docs/README: 15 hardware UI walks (14 program parameters +
    output level)."""
    data = json.loads(
        (DOCS / "reference" / "provided_labels.json").read_text(encoding="utf-8")
    )
    params = data["parameters"]
    assert len(params) == 15
    assert "output level" in params
    program_keys = set(params) - {"output level"}
    assert len(program_keys) == 14
    folders = {p.name for p in _parameter_folders()}
    assert program_keys <= folders


# --- docs/parameter-catalog.md ----------------------------------------------

# Program-parameters table: folder -> (offsets, encoding).
CATALOG_OFFSETS = {
    "reverb time": ([100, 101], "nibble_hilo"),
    "size": ([102, 103], "nibble_hilo"),
    "predelay": ([104, 105], "nibble_hilo"),
    "diffusion": ([106, 107], "nibble_hilo"),
    "density": ([108, 109], "nibble_hilo"),
    "modulation": ([110, 111], "nibble_hilo"),
    "rolloff": ([112, 113], "nibble_hilo"),
    "hf rt multiply": ([114, 115], "nibble_hilo"),
    "hf rt crossover": ([116, 117], "nibble_hilo"),
    "lf rt multiply": ([118, 119], "nibble_hilo"),
    "lf rt crossover": ([120, 121], "nibble_hilo"),
    "vlf cut": ([122, 123], "nibble_hilo"),
    "early to reverb mix": ([124, 125], "nibble_hilo"),
    "early rolloff": ([126, 127], "nibble_hilo"),
    "early select": ([128, 129], "nibble_hilo"),
    "delay level": ([132, 133], "nibble_hilo"),
    "delay time": ([134, 135], "nibble_hilo"),
    "delay modulation": ([138, 139], "nibble_hilo"),
}

# Affine claims: folder -> (scale, offset). `label = scale * encoded + offset`.
CATALOG_AFFINE = {
    "size": (1.0, 0.0),
    "diffusion": (1.0, 0.0),
    "density": (1.0, 0.0),
    "modulation": (1.0, -1.0),
    "hf rt multiply": (0.05, 0.2),
    "vlf cut": (1.0, -20.0),
    "early to reverb mix": (1.0, 0.0),
    "early select": (1.0, 0.0),
    "delay level": (1.0, -21.0),
    "delay time": (8.0, 100.0),
    "delay modulation": (1.0, -1.0),
}

# Observed range claims: folder -> (min, max).
CATALOG_RANGES = {
    "reverb time": (0.2, 30),
    "size": (0, 30),
    "predelay": (0, 500),
    "rolloff": (80, 22000),
    "hf rt multiply": (0.2, 1),
    "hf rt crossover": (200, 16000),
    "lf rt multiply": (0.2, 4),
    "lf rt crossover": (80, 4800),
    "vlf cut": (-20, 0),
    "early to reverb mix": (0, 40),
    "early select": (0, 31),
    "delay time": (100, 996),
    "diffusion": (0, 10),
    "density": (0, 10),
    "modulation": (0, 10),
    "delay modulation": (0, 10),
}


def test_parameter_catalog_offsets_and_encodings():
    for folder, (offsets, encoding) in CATALOG_OFFSETS.items():
        best = _analysis(PARAMETERS / folder)["best_encoding"]
        assert best["offsets"] == offsets, folder
        assert best["encoding"] == encoding, folder


def test_parameter_catalog_affine_scales():
    for folder, (scale, offset) in CATALOG_AFFINE.items():
        best = _analysis(PARAMETERS / folder)["best_encoding"]
        assert best["exact"], folder
        assert best["scale"] == pytest.approx(scale), folder
        assert best["offset"] == pytest.approx(offset), folder


def test_parameter_catalog_table_parameters_are_not_affine():
    """Reverb time / predelay / rolloff / crossovers / LF multiply are tables
    (edge slopes disagree), not closed-form scales."""
    for folder in (
        "reverb time",
        "predelay",
        "rolloff",
        "hf rt crossover",
        "lf rt crossover",
        "lf rt multiply",
        "early rolloff",
    ):
        best = _analysis(PARAMETERS / folder)["best_encoding"]
        assert not best["exact"], folder


def test_parameter_catalog_observed_ranges():
    for folder, (lo, hi) in CATALOG_RANGES.items():
        value_range = _analysis(PARAMETERS / folder)["value_range"]
        assert value_range["min"] == lo, folder
        assert value_range["max"] == hi, folder


def test_rolloff_full_is_one_step_above_22khz():
    """parameter-catalog: rolloff is 80–22000 Hz plus a discrete `full` step
    (encoded 70, one step above 22000 Hz at encoded 69)."""
    value_range = _analysis(PARAMETERS / "rolloff")["value_range"]
    high = value_range["high"]
    assert high["encoded_value"] == 70
    assert high["above"] == 22000
    assert high["above_encoded"] == 69


def test_lf_rt_multiply_breakpoints_from_provided_walk():
    """parameter-catalog / manual-notes: LF RT multiply reaches 2.0x at
    encoded 36 and 4.0x at encoded 56 (0.05 steps below 2.0, 0.1 above)."""
    data = json.loads(
        (DOCS / "reference" / "provided_labels.json").read_text(encoding="utf-8")
    )
    entry = data["parameters"]["lf rt multiply"]
    values = entry["values"] if isinstance(entry, dict) else entry
    assert len(values) == 57  # encoded 0..56
    assert float(values[36]) == 2.0
    assert float(values[56]) == 4.0
    # 0.05/step below the 2.0x knee, 0.1/step above it.
    assert float(values[1]) - float(values[0]) == pytest.approx(0.05)
    assert float(values[37]) - float(values[36]) == pytest.approx(0.1)


# --- docs/parameter-catalog.md (system table) --------------------------------

SYSTEM_OFFSETS = {
    "wet gain": ([8, 9], "nibble_hilo"),
    "dry gain": ([10, 11], "nibble_hilo"),
    "audio routing": ([13], "raw_u8"),
    "audio format": ([15], "raw_u8"),
    "output level": ([17], "raw_u8"),
    "display level": ([21], "raw_u8"),
    "midi channel": ([22, 23], "nibble_hilo"),
    "midi bank": ([25], "raw_u8"),
}


def test_parameter_catalog_system_offsets():
    for folder, (offsets, encoding) in SYSTEM_OFFSETS.items():
        best = _analysis(SYSTEM / folder)["best_encoding"]
        assert best["offsets"] == offsets, folder
        assert best["encoding"] == encoding, folder


# --- docs/capture-guide.md ---------------------------------------------------


def test_capture_guide_bank_index_table():
    """Factory bank indices 0–10 plus the hold-EDIT send marker 11."""
    assert HINT_BANK_INDEX == {
        "Halls": 0,
        "Plates": 1,
        "Rooms": 2,
        "Chambers": 3,
        "Ambience": 4,
        "Spaces": 5,
        "Halls 2": 6,
        "Plates 2": 7,
        "Rooms 2": 8,
        "Spaces 2": 9,
        "NonLin": 10,
    }
    assert EDIT_DUMP_BANK_INDEX == 11


def test_capture_guide_system_menu_highlight_changes_nothing():
    """capture-guide: 'SYSTEM menu highlight does not change SYSTEM dump
    bytes' — every sysex/system/menus/ capture is byte-identical."""
    frames = {
        bytes(raw)
        for p in sorted((SYSTEM / "menus").glob("*.syx"))
        for raw in iter_sysex_messages(p.read_bytes())
    }
    assert len(frames) == 1


# --- docs/manual-notes.md ----------------------------------------------------


def test_manual_notes_series_source_programs():
    """manual-notes: most parameter series were captured from Large Church
    (Halls 2, offset 130 = 1); the LF RT multiply/crossover series from
    Large Hall (classic Halls, offset 130 = 0)."""
    for folder in _parameter_folders():
        names: set[str] = set()
        classes: set[int] = set()
        for path in folder.rglob("*.syx"):
            for raw in iter_sysex_messages(path.read_bytes()):
                names.add(parse_sysex(raw).name)
                classes.add(raw[130])
        if folder.name in ("lf rt multiply", "lf rt crossover"):
            assert names == {"Large Hall"}, folder.name
            assert classes == {0}, folder.name
        else:
            assert names == {"Large Church"}, folder.name
            assert classes == {1}, folder.name


def test_manual_notes_rooms_has_36_presets():
    """manual-notes: Rooms uses slots 0–35 (36 presets on this unit, vs 26
    in the V2 addendum). Slot contiguity is asserted in test_corpus."""
    rooms = list((SYSEX / "prog" / "presets").glob("Rooms.*.syx"))
    assert len(rooms) == 36


# --- docs/kaitai-encode.md ---------------------------------------------------


def test_kaitai_encode_doc_example():
    """kaitai-encode: `encode_at_offsets(70, "nibble_hilo", n_offsets=2)`
    returns `(4, 6)`."""
    assert encode_at_offsets(70, "nibble_hilo", n_offsets=2) == (4, 6)


# --- docs/development.md -----------------------------------------------------


def test_development_test_table_is_complete_and_accurate():
    """Every test file listed in the development.md table exists, and every
    tests/test_*.py file is listed."""
    text = (DOCS / "development.md").read_text(encoding="utf-8")
    listed = set(re.findall(r"`tests/(test_\w+\.py)`", text))
    actual = {p.name for p in (ROOT / "tests").glob("test_*.py")}
    assert listed == actual, (
        f"missing from docs: {sorted(actual - listed)}; "
        f"stale in docs: {sorted(listed - actual)}"
    )


# --- web-ui/README.md --------------------------------------------------------


def test_web_ui_readme_code_references():
    """web-ui README: localStorage key `m7.userPresets`, `applyProgUiBytes`
    in src/prog/uiState.ts, `applyRegisterBasis` in src/app/midiReceive.ts."""
    web = ROOT / "web-ui" / "src"
    assert "m7.userPresets" in (web / "presets" / "userPresets.ts").read_text(
        encoding="utf-8"
    )
    assert "applyProgUiBytes" in (web / "prog" / "uiState.ts").read_text(
        encoding="utf-8"
    )
    assert "applyRegisterBasis" in (web / "app" / "midiReceive.ts").read_text(
        encoding="utf-8"
    )
