"""Doc table cells link banks, presets, and parameters where appropriate."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_preset_sheet_tables_link_names():
    from m7_sysex.preset_sheet import render_sheet_markdown, run_compare

    result = run_compare(sysex_root=ROOT / "sysex")
    md = render_sheet_markdown(result, today="2026-07-16")
    assert "sysex/prog/presets/" in md
    assert "[Halls](presets/halls/)" in md
    assert "parameters/" in md
    assert "## Hard discrepancies by parameter" in md
    assert "## Soft discrepancies by parameter" in md
    assert "| Encoded | Dump | Sheet |" in md
    assert "~" not in md.split("## Hard discrepancies")[1].split("## Soft discrepancies")[0]
    # Plain hard-row shape should not remain.
    assert "| Halls | Large" not in md
    # Missing-on-sheet dumps should link to bank pages.
    assert "[Stone Chamber](presets/chambers/stone-chamber.md)" in md


def test_inventory_tables_link_banks():
    from m7_sysex.names import analyze_names_folder, find_names_folder
    from m7_sysex.preset_inventory import (
        analyze_preset_inventory,
        render_preset_inventory_markdown,
    )

    names = analyze_names_folder(find_names_folder(ROOT / "sysex"))
    md = render_preset_inventory_markdown(
        analyze_preset_inventory(names), today="2026-07-16"
    )
    assert "[Halls](presets/halls/)" in md
    assert "[Halls 2](presets/halls-2/)" in md
    assert "| Halls |" not in md


def test_cross_seen_in_links_parameters():
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.cross import cross_analyze, render_cross_markdown

    cross = cross_analyze(analyze_tree(ROOT / "sysex"))
    md = render_cross_markdown(cross)
    assert "[delay modulation](parameters/delay-modulation.md)" in md


def test_encoding_source_formatting():
    from m7_sysex.export import _format_encoding_source

    assert _format_encoding_source({"sources": ["provided"]}) == "provided"
    assert _format_encoding_source(
        {"sources": ["dump", "provided"]}
    ) == "dump, provided"
    assert _format_encoding_source(
        {"sources": ["dump", "inferred"]}
    ) == "dump, inferred"


def test_early_to_reverb_mix_provided_covers_full_range():
    """Hardware UI walk for early/reverb mix covers every step."""
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _full_encoding_rows
    from m7_sysex.provided import clear_provided_cache

    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "early to reverb mix")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    assert sorted(r["encoded"] for r in densified) == list(range(0, 41))
    # Mid-steps come from the provided walk (and may also have dump).
    by_enc = {r["encoded"]: r for r in densified}
    for enc in (4, 33, 35, 36, 37, 38):
        assert "provided" in by_enc[enc]["sources"]


def test_delay_level_provided_covers_full_range():
    """Hardware UI walk for delay level covers -9 dB via provided."""
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _full_encoding_rows
    from m7_sysex.provided import clear_provided_cache

    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "delay level")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {r["encoded"]: r for r in densified}
    assert sorted(by_enc) == list(range(0, 16))
    assert by_enc[0]["display"] == "off"
    assert "provided" in by_enc[0]["sources"]
    assert by_enc[12]["label"] == -9
    assert by_enc[12]["sources"] == ["provided"]


def test_delay_time_provided_covers_full_range():
    """Hardware UI walk for delay time covers 100..996 ms."""
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _full_encoding_rows
    from m7_sysex.provided import clear_provided_cache, parse_provided_token

    assert parse_provided_token("124 mSec", parameter="delay time") == 124.0
    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "delay time")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {r["encoded"]: r for r in densified}
    assert sorted(by_enc) == list(range(0, 113))
    assert by_enc[0]["label"] == 100
    assert by_enc[3]["label"] == 124
    assert "provided" in by_enc[3]["sources"]
    assert by_enc[112]["label"] == 996


def test_density_provided_marks_low_high_walk():
    """Hardware UI walk for density: Low..High with provided on every step."""
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _full_encoding_rows
    from m7_sysex.provided import clear_provided_cache, parse_provided_token

    assert parse_provided_token("Low", parameter="density") == 0.0
    assert parse_provided_token("High", parameter="density") == 10.0
    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "density")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {r["encoded"]: r for r in densified}
    assert sorted(by_enc) == list(range(0, 11))
    assert by_enc[0]["display"] == "Low"
    assert by_enc[10]["display"] == "High"
    assert "provided" in by_enc[5]["sources"]
    assert all("provided" in (r.get("sources") or []) for r in densified)


def test_diffusion_provided_marks_low_high_walk():
    """Hardware UI walk for diffusion: same Low..High shape as density."""
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _full_encoding_rows
    from m7_sysex.provided import clear_provided_cache

    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "diffusion")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {r["encoded"]: r for r in densified}
    assert sorted(by_enc) == list(range(0, 11))
    assert by_enc[0]["display"] == "Low"
    assert by_enc[10]["display"] == "High"
    assert all("provided" in (r.get("sources") or []) for r in densified)


def test_early_select_provided_covers_full_range_and_sheet_glitch():
    """Hardware UI walk for early select is identity 0..31."""
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _full_encoding_rows
    from m7_sysex.provided import clear_provided_cache

    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "early select")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {r["encoded"]: r for r in densified}
    assert sorted(by_enc) == list(range(0, 32))
    # Provided beats the Large Hall sheet errata (sheet 17 at encoded 13).
    assert by_enc[13]["label"] == 13
    assert "provided" in by_enc[13]["sources"]
    assert by_enc[26]["sources"] == ["provided"]


def test_lf_rt_multiply_provided_parses_decimals_not_balance_pairs():
    """LF RT Multiply walk uses decimals; must not parse 0.2 as balance 0/2."""
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _full_encoding_rows
    from m7_sysex.provided import clear_provided_cache, parse_provided_token

    assert parse_provided_token("0.2", parameter="lf rt multiply") == 0.2
    assert parse_provided_token("1.05", parameter="lf rt multiply") == 1.05
    assert parse_provided_token("2.1", parameter="lf rt multiply") == 2.1
    assert parse_provided_token("3.0", parameter="lf rt multiply") == 3.0
    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "lf rt multiply")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {r["encoded"]: r for r in densified}
    assert sorted(by_enc) == list(range(0, 57))
    assert by_enc[0]["label"] == 0.2
    assert by_enc[4]["label"] == 0.4
    assert by_enc[36]["label"] == 2
    assert by_enc[37]["label"] == 2.1
    assert by_enc[46]["label"] == 3
    assert by_enc[56]["label"] == 4
    assert all("provided" in (r.get("sources") or []) for r in densified)


def test_lf_rt_crossover_provided_covers_full_range_and_sheet_340():
    """Hardware UI walk: enc 7 is 360 Hz (sheet Worcester 340 was off-grid)."""
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _full_encoding_rows
    from m7_sysex.provided import clear_provided_cache, parse_provided_token

    assert parse_provided_token("80 Hz", parameter="lf rt crossover") == 80.0
    assert parse_provided_token("360 Hz", parameter="lf rt crossover") == 360.0
    assert parse_provided_token("4800 Hz", parameter="lf rt crossover") == 4800.0
    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "lf rt crossover")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {r["encoded"]: r for r in densified}
    assert sorted(by_enc) == list(range(0, 27))
    assert by_enc[0]["label"] == 80
    assert by_enc[7]["label"] == 360
    assert by_enc[18]["label"] == 1800
    assert by_enc[26]["label"] == 4800
    assert "provided" in by_enc[7]["sources"]
    assert all("provided" in (r.get("sources") or []) for r in densified)


def test_predelay_provided_covers_full_range():
    """Hardware UI walk: 2 ms steps to 40, then 4 ms to 100, then 8 ms to 500."""
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _full_encoding_rows
    from m7_sysex.provided import clear_provided_cache, parse_provided_token

    assert parse_provided_token("0 ms", parameter="predelay") == 0.0
    assert parse_provided_token("44 ms", parameter="predelay") == 44.0
    assert parse_provided_token("500 ms", parameter="predelay") == 500.0
    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "predelay")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {r["encoded"]: r for r in densified}
    assert sorted(by_enc) == list(range(0, 86))
    assert by_enc[0]["label"] == 0
    assert by_enc[20]["label"] == 40
    assert by_enc[21]["label"] == 44
    assert by_enc[22]["label"] == 48  # was sheet/preset 50
    assert by_enc[35]["label"] == 100
    assert by_enc[36]["label"] == 108
    assert by_enc[85]["label"] == 500
    assert all("provided" in (r.get("sources") or []) for r in densified)


def test_rolloff_provided_covers_full_range():
    """Hardware UI walk: same Hz ladder as early rolloff, ending in Full."""
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _full_encoding_rows
    from m7_sysex.provided import clear_provided_cache, parse_provided_token

    assert parse_provided_token("80 Hz", parameter="rolloff") == 80.0
    assert parse_provided_token("240 Hz", parameter="rolloff") == 240.0
    assert parse_provided_token("22000 Hz", parameter="rolloff") == 22000.0
    assert parse_provided_token("Full", parameter="rolloff") == 22000.0
    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "rolloff")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {r["encoded"]: r for r in densified}
    assert sorted(by_enc) == list(range(0, 71))
    assert by_enc[0]["label"] == 80
    assert by_enc[4]["label"] == 240  # provided densify
    assert by_enc[13]["label"] == 800
    assert by_enc[69]["label"] == 22000
    assert by_enc[70]["label"] in (22000, "full")
    assert all("provided" in (r.get("sources") or []) for r in densified)


def test_reverb_time_provided_covers_full_range():
    """Hardware UI walk: non-linear s ladder 0.2…30 (137 steps)."""
    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import _full_encoding_rows
    from m7_sysex.provided import clear_provided_cache, parse_provided_token

    assert parse_provided_token("0.2", parameter="reverb time") == 0.2
    assert parse_provided_token("5.5", parameter="reverb time") == 5.5
    assert parse_provided_token("17", parameter="reverb time") == 17.0
    assert parse_provided_token("30", parameter="reverb time") == 30.0
    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    result = analyze_parameter_folder(root / "sysex" / "prog" / "parameters" / "reverb time")
    densified = _full_encoding_rows(
        result, result["best_encoding"], sysex_root=root / "sysex"
    )
    assert densified is not None
    by_enc = {r["encoded"]: r for r in densified}
    assert sorted(by_enc) == list(range(0, 137))
    assert by_enc[0]["label"] == 0.2
    assert by_enc[3]["label"] == 0.35  # provided
    assert by_enc[81]["label"] == 5.5  # provided
    assert by_enc[85]["label"] == 5.9
    assert by_enc[86]["label"] == 6.0  # provided
    assert by_enc[90]["label"] == 6.8
    assert by_enc[120]["label"] == 17.0  # provided
    assert by_enc[129]["label"] == 23.0
    assert by_enc[130]["label"] == 24.0  # provided
    assert by_enc[136]["label"] == 30.0
    assert all("provided" in (r.get("sources") or []) for r in densified)


def test_all_provided_labels_update_parameter_pages():
    """Every provided_labels.json walk must appear on densify + committed pages."""
    import json
    import re

    from m7_sysex.analyze import analyze_parameter_folder
    from m7_sysex.export import (
        _encoding_map_table,
        _full_encoding_rows,
        parameter_slug,
    )
    from m7_sysex.provided import clear_provided_cache, provided_mapping_for
    from m7_sysex.system.analyze import analyze_system_series_folder
    from m7_sysex.system.catalog import SYSTEM_PARAMETERS

    clear_provided_cache()
    root = Path(__file__).resolve().parents[1]
    data = json.loads(
        (root / "docs/reference/provided_labels.json").read_text(encoding="utf-8")
    )
    params = list((data.get("parameters") or {}).keys())
    assert params, "expected at least one provided parameter"

    system_folders = {e["folder_hint"].casefold() for e in SYSTEM_PARAMETERS}

    row_re = re.compile(
        r"^\|\s*(?P<enc>\d+)\s\|(?P<body>.*)\|\s*(?P<source>[^|]+)\s*\|$"
    )

    for name in params:
        mapping = provided_mapping_for(name, sysex_root=root / "sysex")
        assert mapping, name
        key = name.casefold()
        if key in system_folders:
            result = analyze_system_series_folder(root / "sysex" / "system" / name)
            page_root = root / "specification" / "system" / "parameters"
        else:
            result = analyze_parameter_folder(
                root / "sysex" / "prog" / "parameters" / name
            )
            page_root = root / "specification" / "prog" / "parameters"
        densified = _full_encoding_rows(
            result, result["best_encoding"], sysex_root=root / "sysex"
        )
        assert densified is not None, name
        by_enc = {int(r["encoded"]): r for r in densified}
        for enc in mapping:
            row = by_enc[enc]
            assert "provided" in (row.get("sources") or []), (name, enc, row)

        md = _encoding_map_table(result, result["best_encoding"], densified)
        for enc in mapping:
            matched = None
            for line in md.splitlines():
                m = row_re.match(line.strip())
                if m and int(m.group("enc")) == enc:
                    matched = m.group("source")
                    break
            assert matched is not None, f"{name} enc {enc} missing from table"
            assert "provided" in matched, (name, enc, matched)

        # Committed generated page must match (guards stale docs after JSON edits).
        page_path = page_root / f"{parameter_slug(name)}.md"
        page = page_path.read_text(encoding="utf-8")
        for enc in mapping:
            matched = None
            for line in page.splitlines():
                m = row_re.match(line.strip())
                if m and int(m.group("enc")) == enc:
                    matched = m.group("source")
                    break
            assert matched is not None, (
                f"{name} enc {enc} missing from {page_path.name}"
            )
            assert "provided" in matched, (name, enc, matched, page_path.name)


def test_bank_page_links_preset_names():
    from m7_sysex.export import _render_bank_page

    md = _render_bank_page(
        "Halls",
        [{"bank": "Halls", "preset": "Large Hall", "program_slot": 0, "bank_index": 0}],
        param_names=[],
        decoders=[],
        today="2026-07-16",
    )
    assert "| 0 | [Large Hall](large-hall.md) |" in md
