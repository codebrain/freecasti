"""Menu-navigation capture series under sysex/prog/menus/."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from m7_sysex.paths import prog_menus_root, resolve_sysex_root
from m7_sysex.prog.menus import analyze_menus_folder, hardware_menu_order
from m7_sysex.prog.corpus_layout import CORPUS_LAYOUT_CLAIMS
from m7_sysex.types import is_prog_corpus_dump


ROOT = Path(__file__).resolve().parent.parent
SYSEX = ROOT / "sysex"


def test_hardware_menu_order_matches_catalog():
    order = hardware_menu_order()
    assert len(order) == 18
    assert order[0] == "reverb time"
    assert order[-1] == "delay modulation"
    assert "predelay" in order


def test_menus_folder_excluded_from_prog_corpus():
    path = prog_menus_root(SYSEX) / "size.syx"
    assert path.is_file()
    assert is_prog_corpus_dump(path, SYSEX) is False


def test_analyze_menus_idle_and_indices():
    menus_root = prog_menus_root(SYSEX)
    analysis = analyze_menus_folder(menus_root, SYSEX)
    prog_ui = analysis["prog_ui"]

    assert analysis["capture_count"] == 19
    assert prog_ui["idle"]["92"] == 0
    assert prog_ui["idle"]["98"] == 0
    assert prog_ui["idle"]["99"] == 0
    assert prog_ui["idle"]["146"] == 1
    assert prog_ui["idle"]["147"] == 12

    assert prog_ui["by_parameter"]["size"]["index"] == 1
    assert prog_ui["by_parameter"]["reverb time"]["browse"]["92"] == 2
    assert prog_ui["by_parameter"]["delay modulation"]["index"] == 17

    reverb = next(
        c for c in analysis["captures"] if c["stem"] == "reverb time"
    )
    idle = next(c for c in analysis["captures"] if c["stem"] == "no menu")
    assert reverb["menu_index_encoded"] == 0
    assert idle["menu_index_encoded"] == 0
    assert reverb["ui"]["92"] == 2
    assert idle["ui"]["92"] == 0


def test_prog_ui_state_json_on_disk():
    path = prog_menus_root(SYSEX) / "prog_ui_state.json"
    assert path.is_file()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["menu_order"] == hardware_menu_order()
    assert "edit" in data["by_parameter"]["modulation"]


def test_ui_state_markdown_edit_table_sorted_by_menu_index():
    from m7_sysex.export.ui_state import render_ui_state_markdown

    analysis = analyze_menus_folder(prog_menus_root(SYSEX), SYSEX)
    body = render_ui_state_markdown(analysis, today="2026-07-18")
    section = body.split("## Edit mode (single parameter change)", 1)[1]
    section = section.split("## Related", 1)[0]
    rows = [
        line
        for line in section.splitlines()
        if line.startswith("| ") and not line.startswith("| Index")
        and not line.startswith("|------")
    ]
    indices = [int(row.split("|", 3)[1].strip()) for row in rows]
    assert indices == list(range(18))
    assert rows[0].startswith("| 0 | reverb time |")
    assert rows[-1].startswith("| 17 | delay modulation |")


def test_corpus_layout_labels_menu_ui():
    labels = {tuple(c["offsets"]): c for c in CORPUS_LAYOUT_CLAIMS}
    assert labels[(98, 99)]["label"] == "selected menu index"
    assert labels[(92,)]["label"] == "panel mode flag"
    assert labels[(146, 147)]["label"] == "display"
    assert labels[(146, 147)]["status"] == "known"


def test_display_region_is_known_in_byte_map():
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.byte_map import build_byte_map
    from m7_sysex.decode_preset import enrich_names_with_parameters
    from m7_sysex.names import analyze_names_folder, find_names_folder

    results = analyze_tree(SYSEX)
    names = enrich_names_with_parameters(
        analyze_names_folder(find_names_folder(SYSEX)),
        results,
    )
    byte_map = build_byte_map(results, names=names, sysex_root=SYSEX)
    region = next(
        r for r in byte_map["regions"] if r.get("offsets") == "146-147"
    )
    assert region["status"] == "known"
    assert "_menus" in region["parameters"]


def test_cross_recurrent_secondary_excludes_display():
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.cross import cross_analyze

    cross = cross_analyze(analyze_tree(SYSEX), SYSEX)
    offsets = {row["offset"] for row in cross["recurrent_secondary"]}
    assert 146 not in offsets
    assert 147 not in offsets
    assert "146" not in offsets and "147" not in offsets


def test_display_parameter_page_export():
    from m7_sysex.export.ui_state import render_display_parameter_page

    analysis = analyze_menus_folder(prog_menus_root(SYSEX), SYSEX)
    body = render_display_parameter_page(analysis, today="2026-07-18")
    assert "# Display" in body
    assert "146–147" in body
    assert "`nibble_hilo`" in body
    assert "browse: size" in body
    # Browse and edit tables are sorted by decoded `nibble_hilo`.
    browse_section = body.split("### Edit mode witnesses")[0]
    assert browse_section.index("browse: size") < browse_section.index(
        "browse: reverb time"
    )
    edit_section = body.split("### Edit mode witnesses", 1)[1]
    assert edit_section.index("| 2 | predelay |") < edit_section.index(
        "| 0 | reverb time |"
    )
