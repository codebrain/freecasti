"""Byte map markdown tables link parameter / identity cells."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _byte_map():
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.byte_map import build_byte_map
    from m7_sysex.decode_preset import enrich_names_with_parameters
    from m7_sysex.names import analyze_names_folder, find_names_folder

    results = analyze_tree(ROOT / "sysex")
    names = enrich_names_with_parameters(
        analyze_names_folder(find_names_folder(ROOT / "sysex")),
        results,
    )
    return build_byte_map(results, names=names, sysex_root=ROOT / "sysex")


def test_overview_links_parameters_and_identity():
    from m7_sysex.byte_map import render_byte_map_overview_markdown

    md = render_byte_map_overview_markdown(_byte_map())
    assert "[reverb time](parameters/reverb-time.md)" in md
    assert "[delay level](parameters/delay-level.md)" in md
    assert "[bank index](program-identity.md)" in md
    assert "[_presets](program-identity.md)" in md
    # Plain names should not remain unlinked in the parameter index.
    assert "| reverb time |" not in md


def test_full_map_links_meaning_cells():
    from m7_sysex.byte_map import render_byte_map_markdown

    md = render_byte_map_markdown(_byte_map())
    assert "Parameter [`reverb time`](parameters/reverb-time.md)" in md
    assert "[sysex/reverb time/](parameters/reverb-time.md)" in md
    assert "[sysex/_presets/](program-identity.md)" in md
    assert "moved in independent series: [early rolloff](parameters/early-rolloff.md)" in md
    assert "[Halls](presets/halls/)=0" in md
    assert "[Halls 2](presets/halls-2/)=6" in md
