"""Generated parameters/README.md index pages."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARAMS = ROOT / "sysex" / "prog" / "parameters"


def test_prog_parameters_readme_lists_all_catalog_entries():
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.catalog import PROGRAM_PARAMETERS
    from m7_sysex.export.parameters_index import build_prog_parameters_readme

    results = analyze_tree(ROOT / "sysex")
    md = build_prog_parameters_readme(results, today="2026-07-17")
    assert "# Program dump bytes" in md
    assert "## Description" not in md
    assert "| Parameter | SysEx" in md
    for entry in PROGRAM_PARAMETERS:
        assert entry["description"] in md
        assert f"]({entry['folder_hint'].replace(' ', '-')}" in md or (
            entry["folder_hint"] in md
        )


def test_prog_parameters_readme_includes_manual_description_sample():
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.export.parameters_index import build_prog_parameters_readme

    results = analyze_tree(ROOT / "sysex")
    md = build_prog_parameters_readme(results, today="2026-07-17")
    assert "onset of reverberation" in md
    assert "eight voices" in md


def test_system_parameters_readme_lists_descriptions():
    from m7_sysex.export.parameters_index import build_system_parameters_readme
    from m7_sysex.system import analyze_system_tree

    results = analyze_system_tree(ROOT / "sysex")
    md = build_system_parameters_readme(results, today="2026-07-17")
    assert "# System dump bytes" in md
    assert "MIDI channel" in md or "MIDI Channel" in md
    assert "front-panel display" in md
    assert "analog output level trim" in md
    assert "AES digital audio" in md


def test_system_catalog_has_description_for_every_parameter():
    from m7_sysex.system.catalog import SYSTEM_PARAMETERS

    for entry in SYSTEM_PARAMETERS:
        assert entry.get("description"), entry["id"]
        assert entry.get("description_source"), entry["id"]
        assert entry.get("description_url"), entry["id"]


def test_export_writes_parameters_readme(tmp_path):
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.export.prog import export_sysex_format

    results = analyze_tree(ROOT / "sysex")
    export_sysex_format(results, tmp_path / "sysex-format")
    readme = tmp_path / "sysex-format" / "prog" / "bytes" / "README.md"
    assert readme.is_file()
    text = readme.read_text(encoding="utf-8")
    assert "**Bytes**" in text
    assert "Reverb Time" in text
