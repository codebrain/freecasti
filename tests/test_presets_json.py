"""Regression tests for exported presets.json."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRESETS_JSON = ROOT / "specification" / "prog" / "presets" / "presets.json"


def test_presets_json_exists_after_export():
    if not PRESETS_JSON.is_file():
        import subprocess
        subprocess.run(["python", "run.py", "export"], cwd=ROOT, check=True)
    assert PRESETS_JSON.is_file()


def test_presets_json_shape():
    if not PRESETS_JSON.is_file():
        return
    payload = json.loads(PRESETS_JSON.read_text(encoding="utf-8"))
    assert payload["source"] == "sysex/prog/presets/"
    assert payload["dump_count"] == len(payload["presets"])
    assert payload["dump_count"] > 200
    row = payload["presets"][0]
    assert {"bank", "preset", "bank_index", "program_slot", "file"} <= set(row)


def test_preset_tables_use_provided_labels_not_interpolation():
    """Factory preset decode must use densified maps (no spurious ~ values)."""
    if not PRESETS_JSON.is_file():
        return
    payload = json.loads(PRESETS_JSON.read_text(encoding="utf-8"))
    by_key = {(d["bank"], d["preset"]): d for d in payload["presets"]}

    med_dark = by_key[("Ambience", "Medium & Dark")]["parameters"]["early rolloff"]
    assert med_dark["display"] == "3600 Hz"
    assert med_dark["encoded"] == 23
    assert not med_dark.get("approx")

    redwood = by_key[("Spaces", "Redwood Valley")]["parameters"]["predelay"]
    assert redwood["display"] == "220 ms"
    assert redwood["encoded"] == 50
    assert not redwood.get("approx")

    tilde_displays = [
        (d["bank"], d["preset"], name, row.get("display"))
        for d in payload["presets"]
        for name, row in (d.get("parameters") or {}).items()
        if str(row.get("display", "")).startswith("~")
    ]
    assert tilde_displays == []


def test_export_redecodes_preset_parameters(tmp_path):
    """Export must refresh preset parameters even if names were not pre-enriched."""
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.export.prog import export_sysex_format
    from m7_sysex.names import analyze_names_folder, find_names_folder

    sysex = ROOT / "sysex"
    results = analyze_tree(sysex)
    names = analyze_names_folder(find_names_folder(sysex))
    # Simulate stale analysis: clear decoded parameters.
    for dump in names["dumps"]:
        dump.pop("parameters", None)
    names.pop("parameters_decoded", None)

    export_sysex_format(results, tmp_path / "sysex-format", names=names)
    payload = json.loads(
        (tmp_path / "sysex-format" / "prog" / "presets" / "presets.json").read_text()
    )
    med_dark = next(
        d for d in payload["presets"]
        if d["bank"] == "Ambience" and d["preset"] == "Medium & Dark"
    )
    assert med_dark["parameters"]["early rolloff"]["display"] == "3600 Hz"

    preset_md = (
        tmp_path / "sysex-format" / "prog" / "presets" / "ambience" / "medium-and-dark.md"
    ).read_text(encoding="utf-8")
    assert "~5190" not in preset_md
    assert "3600 Hz | 23 |" in preset_md
