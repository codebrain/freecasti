"""Preset pages include dump vs printed-sheet comparison."""

from pathlib import Path

from m7_sysex.analyze import analyze_tree
from m7_sysex.decode_preset import PARAMETER_ORDER, enrich_names_with_parameters
from m7_sysex.export import _render_preset_page
from m7_sysex.names import analyze_names_folder, find_names_folder
from m7_sysex.preset_sheet import run_compare

ROOT = Path(__file__).resolve().parents[1]
SYSEX = ROOT / "sysex"


def _names_with_params():
    results = analyze_tree(SYSEX)
    names_folder = find_names_folder(SYSEX)
    assert names_folder is not None
    names = analyze_names_folder(names_folder)
    return enrich_names_with_parameters(names, results)


def test_hard_discrepancy_preset_page_callout():
    names = _names_with_params()
    sheet = run_compare(sysex_root=SYSEX)
    dump = next(
        d
        for d in names["dumps"]
        if d["bank"] == "Halls" and d["preset"] == "Large Hall"
    )
    param_names = [
        p for p in PARAMETER_ORDER if p in (dump.get("parameters") or {})
    ]
    page = _render_preset_page(
        dump,
        all_dumps=names["dumps"],
        bank_siblings=[dump],
        param_names=param_names,
        decoders=names.get("parameter_decoders") or [],
        today="2026-07-16",
        sheet_compare=sheet,
    )
    assert "Sheet discrepancies (1 hard)" in page
    assert "**hard**" in page
    assert "| Dump | Encoded | Sheet | Status |" in page
    assert "early select" in page
    # Large Hall: sheet early select 17 vs dump 13.
    assert "17" in page
    assert "SysEx dump is authoritative" in page


def test_missing_on_sheet_preset_page():
    names = _names_with_params()
    sheet = run_compare(sysex_root=SYSEX)
    dump = next(
        d
        for d in names["dumps"]
        if d["bank"] == "Chambers" and d["preset"] == "Stone Chamber"
    )
    param_names = [
        p for p in PARAMETER_ORDER if p in (dump.get("parameters") or {})
    ]
    page = _render_preset_page(
        dump,
        all_dumps=names["dumps"],
        bank_siblings=[dump],
        param_names=param_names,
        decoders=names.get("parameter_decoders") or [],
        today="2026-07-16",
        sheet_compare=sheet,
    )
    assert "Not on the published sheet" in page
    assert "not on sheet" in page  # delay params
    assert "| Dump | Encoded | Sheet | Status |" in page


def test_exact_match_preset_page():
    names = _names_with_params()
    sheet = run_compare(sysex_root=SYSEX)
    # Pick a known exact comparison if available.
    exact = next(
        (
            c
            for c in sheet["comparisons"]
            if not c["hard"] and not c["soft"]
        ),
        None,
    )
    assert exact is not None
    dump = next(
        d
        for d in names["dumps"]
        if d["bank"] == exact["bank"] and d["preset"] == exact["preset"]
    )
    param_names = [
        p for p in PARAMETER_ORDER if p in (dump.get("parameters") or {})
    ]
    page = _render_preset_page(
        dump,
        all_dumps=names["dumps"],
        bank_siblings=[dump],
        param_names=param_names,
        decoders=names.get("parameter_decoders") or [],
        today="2026-07-16",
        sheet_compare=sheet,
    )
    assert "all printable sheet columns match" in page
    assert "| match |" in page or "match |" in page


def test_standalone_preset_page_single_source_line():
    names = _names_with_params()
    sheet = run_compare(sysex_root=SYSEX)
    dump = names["dumps"][0]
    param_names = [
        p for p in PARAMETER_ORDER if p in (dump.get("parameters") or {})
    ]
    page = _render_preset_page(
        dump,
        all_dumps=names["dumps"],
        bank_siblings=[dump],
        param_names=param_names,
        decoders=names.get("parameter_decoders") or [],
        today="2026-07-16",
        sheet_compare=sheet,
    )
    assert page.count(f"sysex/prog/presets/{dump.get('file')}") == 1
    assert "_Source:" not in page
