"""Official manual descriptions appear on parameter pages."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARAMS = ROOT / "sysex" / "prog" / "parameters"


def test_catalog_has_description_for_every_parameter():
    from m7_sysex.catalog import PROGRAM_PARAMETERS

    for entry in PROGRAM_PARAMETERS:
        assert entry.get("description"), entry["id"]
        assert entry.get("description_source"), entry["id"]
        assert entry.get("description_url"), entry["id"]


def test_parameter_page_includes_manual_description():
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _render_parameter_page

    result = analyze_parameter_folder(PARAMS / "predelay")
    md = _render_parameter_page(
        result, all_results=[result], today="2026-07-16"
    )
    assert "## Description" in md
    assert "onset of reverberation" in md
    assert "bricasti.com/images/M7.pdf" in md


def test_delay_description_cites_v2_addendum():
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _render_parameter_page

    result = analyze_parameter_folder(PARAMS / "delay time")
    md = _render_parameter_page(
        result, all_results=[result], today="2026-07-16"
    )
    assert "eight voices" in md
    assert "M7_V2_Manual_Addendum" in md
