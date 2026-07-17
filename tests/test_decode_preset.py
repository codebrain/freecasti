"""Tests for decoding full presets and display formatting helpers."""

from pathlib import Path

from m7_sysex.analyze import analyze_tree
from m7_sysex.decode_preset import (
    PARAMETER_ORDER,
    _balance_pair,
    build_parameter_decoders,
    decode_dump_parameters,
)

ROOT = Path(__file__).resolve().parents[1]
SYSEX = ROOT / "sysex"
PARAMS = SYSEX / "prog" / "parameters"


def test_balance_pair_inverts_path_position():
    """Position 0..2M on the L-path maps back to the A/B display pair."""
    side = 20
    assert _balance_pair(0, side) == (0, 20)
    assert _balance_pair(20, side) == (20, 20)
    assert _balance_pair(34, side) == (20, 6)
    assert _balance_pair(40, side) == (20, 0)
    # Round trip across the whole path.
    for pos in range(0, 2 * side + 1):
        a, b = _balance_pair(pos, side)
        recovered = a if b == side else side + (side - b)
        assert recovered == pos


def test_decode_all_known_parameters_from_a_preset():
    results = analyze_tree(SYSEX)
    decoders = build_parameter_decoders(results, sysex_root=SYSEX)
    decoded_names = [d["parameter"] for d in decoders]
    # All 18 catalog parameters are decodable from dedicated capture series.
    assert decoded_names == list(PARAMETER_ORDER)
    assert all(d["source"] == "series" for d in decoders)

    raw = (SYSEX / "prog" / "presets" / "Chambers.Large Chamber.syx").read_bytes()
    decoded = decode_dump_parameters(raw, decoders)
    assert set(decoded) == set(PARAMETER_ORDER)
    for name, row in decoded.items():
        assert isinstance(row["encoded"], int), name
        assert row["display"], name

    # Spot checks against the published sheet row for Large Chamber
    # (docs/reference/preset_sheet.json: size 5, diffusion 5, density 3,
    # HF mult 0.80, LF mult 0.95, LF xover 720, VLF -15, mix 20/20, ESel 6).
    assert decoded["size"]["value"] == 5
    assert decoded["diffusion"]["display"] == "5"
    assert decoded["density"]["display"] == "3"
    assert decoded["vlf cut"]["value"] == -15
    assert decoded["hf rt multiply"]["value"] == 0.8
    assert decoded["lf rt multiply"]["value"] == 0.95
    assert decoded["lf rt crossover"]["value"] == 720
    assert decoded["early select"]["value"] == 6
    assert decoded["early to reverb mix"]["display"] == "20/20"
    assert decoded["reverb time"]["value"] == 1.4


def test_enrich_resolves_corpus_root_from_presets_folder():
    """Preset decode must load provided labels (sysex root, not presets/)."""
    from m7_sysex.decode_preset import enrich_names_with_parameters
    from m7_sysex.names import analyze_names_folder, find_names_folder

    results = analyze_tree(SYSEX)
    names = analyze_names_folder(find_names_folder(SYSEX))
    enrich_names_with_parameters(names, results)
    dump = next(
        d for d in names["dumps"]
        if d["bank"] == "Ambience" and d["preset"] == "Medium & Dark"
    )
    er = dump["parameters"]["early rolloff"]
    assert er["display"] == "3600 Hz"
    assert er["encoded"] == 23
    assert not er.get("approx")


def test_delay_block_decoding_off_states():
    """Parameter-series dumps come from Large Church; off.syx encodes off as 0."""
    results = analyze_tree(SYSEX)
    decoders = build_parameter_decoders(results, sysex_root=SYSEX)
    raw = (PARAMS / "delay level" / "off.syx").read_bytes()
    decoded = decode_dump_parameters(raw, decoders)
    assert decoded["delay level"]["encoded"] == 0
    assert decoded["delay level"]["display"] == "off"
