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
    assert "[reverb time](bytes/reverb-time.md)" in md
    assert "[delay level](bytes/delay-level.md)" in md
    assert "[bank index](program-identity.md)" in md
    assert "[display](bytes/display.md)" in md
    assert "[program name (ASCII)](bytes/program-name.md)" in md
    assert "[program name pad](bytes/program-name-pad.md)" in md
    assert "[register bank](bytes/register-bank.md)" in md
    assert "[register](bytes/register.md)" in md
    assert "bytes/display.md)" in md
    assert "[_presets](program-identity.md)" in md
    # Plain names should not remain unlinked in the parameter index.
    assert "| reverb time |" not in md


def test_full_map_links_meaning_cells():
    from m7_sysex.byte_map import render_byte_map_markdown

    md = render_byte_map_markdown(_byte_map())
    assert "Parameter [`reverb time`](bytes/reverb-time.md)" in md
    assert "[sysex/prog/parameters/reverb time/](bytes/reverb-time.md)" in md
    assert "[sysex/prog/presets/](program-identity.md)" in md
    assert "moved in independent series: [early rolloff](bytes/early-rolloff.md)" in md
    assert "[Halls](presets/halls/)=0" in md
    assert "[Halls 2](presets/halls-2/)=6" in md


def _system_byte_map():
    from m7_sysex.system import analyze_system_tree
    from m7_sysex.system.byte_map import build_system_byte_map

    results = analyze_system_tree(ROOT / "sysex")
    return build_system_byte_map(results, sysex_root=ROOT / "sysex")


def test_system_overview_links_settings():
    from m7_sysex.system.byte_map import render_system_byte_map_overview_markdown

    md = render_system_byte_map_overview_markdown(_system_byte_map())
    assert "[wet gain](bytes/wet-gain.md)" in md
    assert "[midi channel](bytes/midi-channel.md)" in md
    assert "[midi bank](bytes/midi-bank.md)" in md
    assert "byte-map.md" in md
    assert "### Settings (by offset)" in md
    assert "Coupled offsets" in md


def test_system_full_map_links_to_overview():
    from m7_sysex.system.byte_map import render_system_byte_map_markdown

    md = render_system_byte_map_markdown(_system_byte_map())
    assert "[byte-map-overview.md](byte-map-overview.md)" in md
    assert "[wet gain](bytes/wet-gain.md)" in md
