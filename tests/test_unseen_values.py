"""Tests for unseen / undocumented value gap report."""

from __future__ import annotations

from pathlib import Path

import pytest

from m7_sysex.analyze import analyze_tree
from m7_sysex.byte_map import build_byte_map
from m7_sysex.decode_preset import enrich_names_with_parameters
from m7_sysex.export import export_sysex_format, resolve_export_dir
from m7_sysex.names import analyze_names_folder, find_names_folder
from m7_sysex.paths import prog_menus_root
from m7_sysex.prog.menus import analyze_menus_folder
from m7_sysex.prog.unseen_values import build_unseen_values, observed_values_by_offset

ROOT = Path(__file__).resolve().parents[1]
SYSEX = ROOT / "sysex"


@pytest.fixture(scope="module")
def prog_analysis_bundle():
    results = analyze_tree(SYSEX)
    names_folder = find_names_folder(SYSEX)
    names = enrich_names_with_parameters(
        analyze_names_folder(names_folder),
        results,
    )
    byte_map = build_byte_map(results, names=names, sysex_root=SYSEX)
    menus_analysis = analyze_menus_folder(prog_menus_root(SYSEX), SYSEX)
    unseen = build_unseen_values(results, byte_map, menus_analysis, SYSEX)
    return {
        "results": results,
        "byte_map": byte_map,
        "menus_analysis": menus_analysis,
        "unseen": unseen,
    }


def test_reverb_time_has_documented_unseen_rows(prog_analysis_bundle):
    unseen = prog_analysis_bundle["unseen"]
    rt = unseen["parameters"].get("reverb time")
    assert rt is not None
    assert rt["documented_unseen_count"] > 0
    assert all("dump" not in row["sources"] for row in rt["documented_unseen"])


def test_reserved_offset_reports_unseen_nibbles(prog_analysis_bundle):
    unseen = prog_analysis_bundle["unseen"]
    # Offset 95 = register (0–9 witnessed via edit/registers fullsweep).
    off95 = next(e for e in unseen["offsets"] if e["offset"] == 95)
    assert off95["observed_count"] == 10
    assert off95["unseen_nibble_count"] == 6
    assert off95["unseen_nibble_values"] == ["A", "B", "C", "D", "E", "F"]
    off93 = next(e for e in unseen["offsets"] if e["offset"] == 93)
    assert off93["observed_count"] == 5  # register banks B0–B4


def test_observed_values_by_offset_covers_corpus():
    observed = observed_values_by_offset(SYSEX)
    assert 95 in observed
    assert observed[95] == list(range(10))
    assert observed[93] == list(range(5))
    # Fullsweep witnesses display=164 (`0A 04`).
    assert 0x0A in observed[146]
    assert 0x04 in observed[147]


def test_export_writes_unseen_sections_per_byte(tmp_path, prog_analysis_bundle):
    out = resolve_export_dir(tmp_path / "spec")
    export_sysex_format(
        prog_analysis_bundle["results"],
        out,
        byte_map=prog_analysis_bundle["byte_map"],
        menus_analysis=prog_analysis_bundle["menus_analysis"],
    )
    prog = out / "prog"

    # The standalone page is gone; each field page carries its own section.
    assert not (prog / "unseen-values.md").exists()

    reverb = (prog / "bytes" / "reverb-time.md").read_text(encoding="utf-8")
    assert "## Unseen values" in reverb
    assert "Never captured on the wire" in reverb
    assert "Encoding range:" in reverb

    display = (prog / "bytes" / "display.md").read_text(encoding="utf-8")
    assert "## Unseen values" in display
    # Display cursor gap before idle (28) surfaces as a leading 0–27 range.
    assert "Unseen positions" in display
    assert "0\u201327" in display


def test_nav_strip_drops_unseen_values_link(tmp_path, prog_analysis_bundle):
    out = resolve_export_dir(tmp_path / "spec")
    export_sysex_format(
        prog_analysis_bundle["results"],
        out,
        byte_map=prog_analysis_bundle["byte_map"],
        menus_analysis=prog_analysis_bundle["menus_analysis"],
    )
    overview = (out / "prog" / "README.md").read_text(encoding="utf-8")
    assert "unseen-values.md" not in overview
    assert "Unseen values" not in overview.splitlines()[0]
