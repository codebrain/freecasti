"""Full encoding maps: series + provided + preset anchors."""

from pathlib import Path

from m7_sysex.preset_inferred import (
    densify_encoding_map,
    pack_encoded_bytes,
)


def test_tidy_label_preserves_half_db_steps():
    from m7_sysex.preset_inferred import _tidy_label

    assert _tidy_label(-59.5, "db") == -59.5
    assert _tidy_label(-0.5, "db") == -0.5
    assert _tidy_label(-41.5, "db") == -41.5
    assert _tidy_label(-60.0, "db") == -60


def test_densify_priority_series_over_preset():
    rows = densify_encoding_map(
        series={0: 80.0, 2: 160.0},
        preset={0: 999.0, 1: 120.0},
        unit="hz",
        preset_refs={0: [("Halls", "Large Hall")], 1: [("Plates", "Bright Plate")]},
    )
    by_enc = {r["encoded"]: r for r in rows}
    assert by_enc[0]["label"] == 80  # dump label wins
    assert by_enc[0]["source"] == "dump"
    assert by_enc[0]["sources"] == ["dump", "preset"]
    assert by_enc[0]["preset_refs"] == [("Halls", "Large Hall")]
    assert by_enc[1]["label"] == 120
    assert by_enc[1]["source"] == "preset"
    assert by_enc[1]["sources"] == ["preset"]
    assert by_enc[2]["source"] == "dump"
    assert by_enc[2]["sources"] == ["dump"]


def test_densify_provided_beats_preset():
    """Hardware UI walk wins labels over preset; dump still wins over both."""
    rows = densify_encoding_map(
        series={0: 0.0, 4: 4.0},
        preset={2: 99.0},
        provided={1: 1.0, 2: 2.0, 3: 3.0},
        unit=None,
    )
    by_enc = {r["encoded"]: r for r in rows}
    assert by_enc[0]["sources"] == ["dump"]
    assert by_enc[1]["sources"] == ["provided"]
    assert by_enc[1]["label"] == 1
    assert by_enc[2]["sources"] == ["provided", "preset"]
    assert by_enc[2]["label"] == 2  # provided wins over preset
    assert by_enc[3]["sources"] == ["provided"]
    assert by_enc[4]["sources"] == ["dump"]
    assert sorted(by_enc) == [0, 1, 2, 3, 4]


def test_densify_inferred_between_dump_and_preset():
    rows = densify_encoding_map(
        series={0: 0.0},
        preset={2: 2.0},
        inferred={1: 1.0},
    )
    by_enc = {r["encoded"]: r for r in rows}
    assert by_enc[1]["sources"] == ["inferred"]
    assert by_enc[1]["label"] == 1.0
    assert by_enc[2]["sources"] == ["preset"]


def test_densify_does_not_invent_gap_fills():
    """Only dump / provided / preset anchors appear — no synthetic mid-steps."""
    rows = densify_encoding_map(
        series={0: 80.0, 2: 160.0},
        preset=None,
        unit="hz",
    )
    by_enc = {r["encoded"]: r for r in rows}
    assert sorted(by_enc) == [0, 2]
    assert by_enc[0]["source"] == "dump"
    assert by_enc[2]["source"] == "dump"


def test_pack_encoded_bytes_nibble_hilo():
    assert pack_encoded_bytes(0x3A, "nibble_hilo", 2) == ["03", "0A"]
    assert pack_encoded_bytes(70, "nibble_hilo", 2) == ["04", "06"]
    assert pack_encoded_bytes(5, "raw_u8", 1) == ["05"]


def test_export_early_rolloff_page_has_source_column():
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _encoding_map_table, _full_encoding_rows
    from m7_sysex.provided import clear_provided_cache

    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "early rolloff")
    best = result["best_encoding"]
    densified = _full_encoding_rows(result, best, sysex_root=root / "sysex")
    assert densified is not None
    primary = {r["source"] for r in densified}
    all_sources = {s for r in densified for s in (r.get("sources") or [])}
    assert "dump" in primary
    assert "provided" in all_sources
    assert "preset" in all_sources
    assert all_sources <= {"dump", "provided", "inferred", "preset"}
    from m7_sysex.export import _format_encoding_source

    md = _encoding_map_table(result, best, densified)
    assert "| Source |" in md
    assert "dump" in md
    assert "provided" in md
    # Preset rows use numbered links to factory preset pages.
    assert "](../presets/" in md
    assert "[1](../presets/" in md
    # When dump and preset both witness a step, both appear comma-separated.
    dual = next(
        (
            r
            for r in densified
            if "dump" in (r.get("sources") or [])
            and "preset" in (r.get("sources") or [])
        ),
        None,
    )
    assert dual is not None, "expected at least one dump+preset overlap"
    formatted = _format_encoding_source(dual)
    assert formatted.startswith("dump,")
    assert "](../presets/" in formatted
    by_enc = {r["encoded"]: r for r in densified}
    assert by_enc[6]["label"] == 320
    assert by_enc[27]["label"] == 5200  # was sheet 5000
    assert by_enc[46]["label"] == 12800  # was sheet 12900
    assert by_enc[70]["display"] == "Full"


def test_export_delay_level_full_affine_table():
    """Delay level page must list every encoded step 0..15 with sources."""
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _encoding_map_table, _full_encoding_rows

    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "delay level")
    best = result["best_encoding"]
    densified = _full_encoding_rows(result, best, sysex_root=root / "sysex")
    assert densified is not None
    by_enc = {r["encoded"]: r for r in densified}
    assert sorted(by_enc) == list(range(0, 16))
    assert by_enc[0]["display"] == "off"
    assert by_enc[0]["source"] == "dump"
    assert by_enc[1]["source"] == "dump"
    assert by_enc[1]["label"] == -20
    assert by_enc[3]["source"] in {"provided", "preset", "dump"}
    assert by_enc[3]["label"] == -18
    assert by_enc[15]["source"] == "dump"
    md = _encoding_map_table(result, best, densified)
    assert "| Source |" in md
    assert "| off |" in md or "off" in md


def test_export_delay_modulation_same_logic_as_others():
    """Delay modulation (V2, not on sheet) still gets full series/preset map."""
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _encoding_map_table, _full_encoding_rows

    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "delay modulation")
    best = result["best_encoding"]
    densified = _full_encoding_rows(result, best, sysex_root=root / "sysex")
    assert densified is not None
    by_enc = {r["encoded"]: r for r in densified}
    assert sorted(by_enc) == list(range(0, 12))
    assert by_enc[0]["display"] == "off"
    assert by_enc[0]["source"] == "dump"
    assert "inferred" in by_enc[0]["sources"]
    assert "provided" not in by_enc[0]["sources"]
    assert by_enc[1]["source"] == "dump"
    assert by_enc[1]["label"] == 0
    # Factory dumps witness mid encodings even without a sheet column.
    assert by_enc[4]["source"] == "preset"
    assert by_enc[4]["label"] == 3
    assert by_enc[4].get("preset_refs")
    sources = {r["source"] for r in densified}
    assert sources >= {"dump", "preset"}
    md = _encoding_map_table(result, best, densified)
    assert "| Source |" in md
    assert "[1](../presets/" in md
    # Numbered links only — not the bare word "preset".
    assert "| preset |" not in md


def test_every_parameter_page_has_full_encoding_map():
    """Same densify path for every capture series — no sparse-only pages."""
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.export import _encoding_map_table, _full_encoding_rows

    root = Path(__file__).resolve().parents[1]
    results = analyze_tree(root / "sysex")
    assert len(results) >= 18
    for result in results:
        best = result.get("best_encoding")
        assert best is not None, result["parameter"]
        densified = _full_encoding_rows(
            result, best, sysex_root=root / "sysex"
        )
        assert densified, f"{result['parameter']} missing encoding map"
        assert len(densified) >= 2, result["parameter"]
        assert all(
            set(r.get("sources") or []) <= {"dump", "provided", "inferred", "preset"}
            for r in densified
        ), result["parameter"]
        md = _encoding_map_table(result, best, densified)
        from m7_sysex.export import _parameter_body

        assert "## Encoding map" in _parameter_body(result, sysex_root=root / "sysex")
        assert "| Source |" in md


def test_encoding_maps_have_no_holes():
    """Witnessed encodings cover every integer from min to max per parameter."""
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.export import _full_encoding_rows
    from m7_sysex.provided import clear_provided_cache

    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    for result in analyze_tree(root / "sysex"):
        densified = _full_encoding_rows(
            result, result["best_encoding"], sysex_root=root / "sysex"
        )
        assert densified
        encs = sorted(int(r["encoded"]) for r in densified)
        assert encs == list(range(encs[0], encs[-1] + 1)), result["parameter"]


def test_system_how_to_set_uses_system_checksum():
    from m7_sysex.system.analyze import analyze_system_series_folder

    root = Path(__file__).resolve().parents[1]
    result = analyze_system_series_folder(root / "sysex" / "system" / "output level")
    steps = (result["hypothesis"]["how_to_set"]["encode_steps"] or [])
    assert any("bytes[8:72]" in step for step in steps)
    assert not any("bytes[8:152]" in step for step in steps)


def test_parameter_page_uses_catalog_title():
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _render_parameter_page

    result = analyze_parameter_folder(
        Path(__file__).resolve().parents[1] / "sysex" / "prog" / "parameters" / "predelay"
    )
    md = _render_parameter_page(
        result, all_results=[result], today="2026-07-16"
    )
    assert "# Pre Delay" in md
    assert "## SysEx summary" in md
    assert "byte map overview" in md


def test_system_byte_map_midi_bank_at_offset_25():
    from m7_sysex.system.analyze import analyze_system_tree
    from m7_sysex.system.byte_map import build_system_byte_map

    root = Path(__file__).resolve().parents[1]
    results = analyze_system_tree(root / "sysex")
    byte_map = build_system_byte_map(results, sysex_root=root / "sysex")
    cell = byte_map["bytes"][25]
    assert "midi bank" in cell["role"].lower()
    assert cell["status"] == "known"
    assert "display level" in cell["role"].lower()


def test_cross_untouched_series_wording():
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.cross import cross_analyze, render_cross_markdown

    root = Path(__file__).resolve().parents[1]
    cross = cross_analyze(analyze_tree(root / "sysex"), root / "sysex")
    md = render_cross_markdown(cross)
    assert "### Untouched in parameter series" in md
    assert "byte-map-overview.md" in md
    assert "coverage gaps" not in md.lower()
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import (
        _format_encoding_source,
        _full_encoding_rows,
        _render_parameter_page,
    )
    from m7_sysex.export.prog import _preset_witnesses_appendix

    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "predelay")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    row0 = next(r for r in densified if int(r["encoded"]) == 0)
    formatted = _format_encoding_source(row0)
    assert "+51 more" in formatted or "+5" in formatted  # depends on preset count
    assert formatted.count("](../presets/") <= 5
    appendix = _preset_witnesses_appendix(densified)
    assert "### Preset witnesses" in appendix
    assert "Large Hall" in appendix or "ambience" in appendix.lower()

    md = _render_parameter_page(result, all_results=[result], today="2026-07-17")
    assert "## Encoding map" in md
    assert "**Summary:**" not in md
    assert "bytes[8:152]" not in md or result.get("kind") != "system"
