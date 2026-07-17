"""Basic unit tests for label parsing and known parameter fits."""

from pathlib import Path

from m7_sysex.analyze import analyze_parameter_folder
from m7_sysex.labels import parse_dump_label


ROOT = Path(__file__).resolve().parents[1]
PARAMS = ROOT / "sysex" / "prog" / "parameters"


def test_parse_hz_unit():
    label = parse_dump_label("120hz")
    assert label.kind == "number"
    assert label.value == 120
    assert label.unit == "hz"
    from m7_sysex.labels import display_unit, format_value_with_unit
    assert display_unit("hz") == "Hz"
    assert format_value_with_unit(120, "hz") == "120 Hz"


def test_parse_low_high_endpoints():
    low = parse_dump_label("low")
    high = parse_dump_label("HIGH")
    assert low.kind == "endpoint" and low.endpoint == "low"
    assert high.kind == "endpoint" and high.endpoint == "high"


def test_parse_off_endpoint():
    off = parse_dump_label("off")
    assert off.kind == "endpoint" and off.endpoint == "off"
    assert off.kind != "bool"


def test_parse_full_as_high():
    full = parse_dump_label("FULL")
    assert full.kind == "endpoint"
    assert full.endpoint == "high"
    assert full.stem == "FULL"


def test_diffusion_identity_and_range():
    result = analyze_parameter_folder(PARAMS / "diffusion")
    best = result["best_encoding"]
    assert best["encoding"] == "raw_u8"
    assert best["offsets"] == [107]
    assert best["score"] == 1.0
    assert result["hypothesis"]["confidence"] == "high"
    value_range = result["value_range"]
    assert value_range["min"] == 0
    assert value_range["max"] == 10
    assert value_range["low"]["encoded_value"] == 0
    assert value_range["high"]["encoded_value"] == 10


def test_predelay_field_location():
    result = analyze_parameter_folder(PARAMS / "predelay")
    best = result["best_encoding"]
    assert best["offsets"] == [104, 105]
    assert best["encoding"] == "nibble_hilo"
    assert 104 in result["changing_offsets"]
    assert 105 in result["changing_offsets"]


def test_cross_analysis_has_meta_fields():
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.cross import cross_analyze, render_cross_markdown

    results = analyze_tree(ROOT / "sysex")
    cross = cross_analyze(results)
    assert cross["kind"] == "cross_series_meta"
    assert cross["message_count"] >= 2
    assert "coverage_gaps" in cross
    assert "checksum" in cross
    assert cross["checksum"].get("algorithm", {}).get("name") == "CRC-16/ARC"
    md = render_cross_markdown(cross)
    assert "## Cross-series analysis" in md
    assert "Untouched in parameter series" in md
    assert "CRC-16/ARC" in md


def test_vlf_cut_negative_db_offset():
    """VLF cut is 0 and negative dB only: label = encoded - 20."""
    result = analyze_parameter_folder(PARAMS / "vlf cut")
    best = result["best_encoding"]
    assert best["encoding"] == "nibble_hilo"
    assert best["offsets"] == [122, 123]
    assert best["exact"] is True
    assert best["score"] == 1.0
    assert best["scale"] == 1.0
    assert best["offset"] == -20.0
    assert "label = encoded + (-20)" in best["notes"]
    assert result["hypothesis"]["confidence"] == "high"
    value_range = result["value_range"]
    assert value_range["min"] == -20
    assert value_range["max"] == 0
    assert value_range["unit"] == "db"
    sampling = result["sampling"]
    assert sampling["coverage"]["complete_edge_pair"] is True
    assert sampling["edge_steps"]["edge_slopes_agree"] is True


def test_hf_rt_multiply_edge_affine():
    """Agreeing extreme↔adjacent slopes recover label = 0.05*encoded + 0.2."""
    result = analyze_parameter_folder(PARAMS / "hf rt multiply")
    best = result["best_encoding"]
    assert best["encoding"] == "nibble_hilo"
    assert best["offsets"] == [114, 115]
    assert best["exact"] is True
    assert best["score"] == 1.0
    assert abs(best["scale"] - 0.05) < 1e-9
    assert abs(best["offset"] - 0.2) < 1e-9
    assert result["hypothesis"]["confidence"] == "high"


def test_predelay_edge_disagreement_prefers_table():
    """Predelay low/high edge slopes disagree — table beats partial *2."""
    result = analyze_parameter_folder(PARAMS / "predelay")
    best = result["best_encoding"]
    assert best["offsets"] == [104, 105]
    assert best["exact"] is False
    assert "table/index" in (best.get("notes") or "")
    assert result["sampling"]["edge_steps"]["edge_slopes_agree"] is False


def test_early_to_reverb_balance_path():
    """Early/reverb mix is A/B balance path; filenames use A.B for '/'."""
    from m7_sysex.labels import (
        detect_balance_series,
        format_balance_pair,
        load_dumps,
        parse_balance_pair_token,
    )

    folder = PARAMS / "early to reverb mix"
    stems = [p.stem for p in folder.glob("*.syx")]
    balance = detect_balance_series(stems)
    assert balance is not None
    assert balance["side_max"] == 20
    assert balance["positions"]["0.20"]["position"] == 0
    assert balance["positions"]["0.20"]["display"] == "0/20"
    assert balance["positions"]["20.20"]["position"] == 20
    assert balance["positions"]["20.6"]["pair"] == (20, 6)
    assert balance["positions"]["20.6"]["display"] == "20/6"
    assert balance["positions"]["20.6"]["position"] == 34
    assert balance["positions"]["20.0"]["position"] == 40
    assert parse_balance_pair_token("20/6") == (20, 6)
    assert parse_balance_pair_token("20.6") == (20, 6)
    assert format_balance_pair(0, 20) == "0/20"

    # Genuine floats must not be detected as balance.
    assert detect_balance_series(["0.2", "0.25", "0.95", "1"]) is None

    result = analyze_parameter_folder(folder)
    best = result["best_encoding"]
    assert best["offsets"] == [124, 125]
    assert best["encoding"] == "nibble_hilo"
    assert best["exact"] is True
    assert best["score"] == 1.0
    assert best["scale"] == 1.0
    assert best["offset"] in (0, 0.0)
    assert result["hypothesis"]["confidence"] == "high"
    assert result["value_range"]["min"] == 0
    assert result["value_range"]["max"] == 40
    assert result["value_range"]["balance"]["side_max"] == 20
    assert "A/B" in result["value_range"]["balance"]["display"]

    # load_dumps exposes pair metadata
    dumps = load_dumps(folder)
    by_stem = {p.stem: label for p, label, _ in dumps}
    assert by_stem["20.6"].pair == (20, 6)
    assert by_stem["20.6"].value == 34
    assert by_stem["20.6"].raw_label == "20/6"


def test_catalog_annotates_known_parameters():
    from m7_sysex.catalog import annotate_series, lookup_parameter, missing_parameters

    assert lookup_parameter("vlf cut")["id"] == "vlf_cut"
    assert lookup_parameter("hf rt multiply")["min"] == 0.2
    assert lookup_parameter("early select")["observed_max"] == 31
    ann = annotate_series(
        "vlf cut",
        {"min": -20, "max": 0, "unit": "db"},
        unit="db",
    )
    assert ann["matched"] is True
    assert ann["role"] == "hint"
    # -20 is allowed via observed_min vs printed -18.
    assert ann["agreement"] in {"match", "differs_from_hint", "partial"}

    early = annotate_series("early select", {"min": 0, "max": 31})
    assert early["matched"] is True
    assert early["agreement"] in {"match", "differs_from_hint"}
    assert not any("incomplete" in w for w in early.get("warnings") or [])

    bal = annotate_series(
        "early to reverb mix",
        {
            "min": 0,
            "max": 40,
            "balance": {"side_max": 20},
        },
    )
    assert bal["agreement"] == "match"

    missing = missing_parameters(["predelay", "density"])
    ids = {m["id"] for m in missing}
    assert "reverb_time" in ids
    assert "predelay" not in ids
    assert "density" not in ids


def test_program_dump_checksum_arc():
    from m7_sysex.frame import program_dump_checksum, verify_program_dump_checksum

    path = PARAMS / "diffusion" / "low.syx"
    raw = path.read_bytes()
    assert verify_program_dump_checksum(raw)
    assert raw[152:156] == program_dump_checksum(raw)


def test_expected_name_bytes_space_padded():
    from m7_sysex.names import NAME_LENGTH, check_name_bytes, expected_name_bytes

    expected = expected_name_bytes("Amsterdam Hall")
    assert len(expected) == NAME_LENGTH
    assert expected.startswith(b"Amsterdam Hall")
    assert expected.endswith(b" " * (NAME_LENGTH - len(b"Amsterdam Hall")))

    raw = bytearray(160)
    raw[8:88] = expected
    ok = check_name_bytes(bytes(raw), "Amsterdam Hall")
    assert ok["name_bytes_match"] is True
    assert ok["name_field"] == "Amsterdam Hall"

    raw[8] = ord("X")
    bad = check_name_bytes(bytes(raw), "Amsterdam Hall")
    assert bad["name_bytes_match"] is False
    assert bad["name_mismatch"]["offset"] == 8
    assert bad["name_mismatch"]["expected_byte"] == "41"
    assert bad["name_mismatch"]["actual_byte"] == "58"


def test_preset_name_bytes_match_filenames():
    from m7_sysex.names import analyze_names_folder, find_names_folder, validate_preset_dump

    folder = find_names_folder(ROOT / "sysex")
    assert folder is not None
    result = analyze_names_folder(folder)
    assert result["fields"]["program_name"]["bytes_mismatch_count"] == 0
    assert all(d["name_bytes_match"] for d in result["dumps"])
    for path in folder.glob("*.syx"):
        identity = validate_preset_dump(path)
        assert identity["name_bytes_match"] is True


def test_validate_preset_dump_rejects_name_mismatch():
    import pytest
    from m7_sysex.names import PresetDumpError, expected_name_bytes, validate_preset_dump

    path = ROOT / "sysex" / "prog" / "presets" / "Chambers.Large Chamber.syx"
    raw = bytearray(path.read_bytes())
    raw[8:88] = expected_name_bytes("Wrong Name")
    with pytest.raises(PresetDumpError, match="name field"):
        validate_preset_dump(path, bytes(raw))


def test_validate_preset_dump_rejects_bank_mismatch():
    import pytest
    from m7_sysex.names import PresetDumpError, validate_preset_dump

    path = ROOT / "sysex" / "prog" / "presets" / "Chambers.Large Chamber.syx"
    raw = path.read_bytes()
    wrong_bank_path = path.with_name("Halls.Large Chamber.syx")
    with pytest.raises(PresetDumpError, match="bank index"):
        validate_preset_dump(wrong_bank_path, raw)


def test_validate_preset_dump_accepts_nonlin_alias():
    from m7_sysex.frame import parse_sysex
    from m7_sysex.names import validate_preset_dump

    path = ROOT / "sysex" / "prog" / "presets" / "NonLin.NonLin A.syx"
    identity = validate_preset_dump(path)
    assert identity["bank"] == "NonLin"
    assert identity["bank_index"] == 10
    assert identity["name_field"] == "Nonlin A"
    # NonLin uses engine/bank-class 2 at offset 130 (not classic 0 / *2 1).
    assert parse_sysex(path.read_bytes()).raw[130] == 2


def test_lf_rt_series_confirm_inferred_offsets():
    """Dedicated LF RT series confirm the offsets first inferred from the sheet."""
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.decode_preset import build_parameter_decoders, decode_dump_parameters
    from m7_sysex.encodings import nibble_hilo
    from m7_sysex.frame import parse_sysex
    from m7_sysex.names import analyze_names_folder, find_names_folder
    from m7_sysex.preset_inferred import build_lf_crossover_mapping

    multiply = analyze_parameter_folder(PARAMS / "lf rt multiply")
    assert multiply["best_encoding"]["offsets"] == [118, 119]
    assert multiply["best_encoding"]["encoding"] == "nibble_hilo"
    assert multiply["value_range"]["min"] == 0.2
    assert multiply["value_range"]["max"] == 4
    # Non-uniform steps: 0.05 below 2.0x, 0.1 above - table, not affine.
    assert multiply["best_encoding"]["exact"] is False
    assert multiply["sampling"]["edge_steps"]["edge_slopes_agree"] is False

    crossover = analyze_parameter_folder(PARAMS / "lf rt crossover")
    assert crossover["best_encoding"]["offsets"] == [120, 121]
    assert crossover["best_encoding"]["encoding"] == "nibble_hilo"
    assert crossover["value_range"]["min"] == 80
    assert crossover["value_range"]["max"] == 4800
    assert crossover["unit"] == "hz"

    results = analyze_tree(ROOT / "sysex")
    decoders = build_parameter_decoders(results, sysex_root=ROOT / "sysex")
    by_name = {d["parameter"]: d for d in decoders}
    assert by_name["lf rt multiply"]["source"] == "series"
    assert by_name["lf rt multiply"]["kind"] == "table"
    assert by_name["lf rt crossover"]["source"] == "series"
    assert by_name["lf rt crossover"]["kind"] == "table"
    # Series tables are densified with sheet points, then hardware provided walks.
    assert by_name["lf rt multiply"]["mapping_sources"] == [
        "series",
        "preset_sheet",
        "provided",
    ]
    assert by_name["lf rt multiply"]["mapping"][15] == 0.95
    assert by_name["lf rt crossover"]["mapping"][12] == 720
    # Sheet Worcester printed 340 at enc 7; hardware walk is 360.
    assert by_name["lf rt crossover"]["mapping"][7] == 360
    assert "provided" in by_name["lf rt crossover"]["mapping_sources"]

    # Large Chamber sheet LF multiply 0.95 → enc 15; crossover 720 → enc 12
    path = ROOT / "sysex" / "prog" / "presets" / "Chambers.Large Chamber.syx"
    raw = path.read_bytes()
    decoded = decode_dump_parameters(raw, decoders)
    assert decoded["lf rt multiply"]["encoded"] == 15
    assert decoded["lf rt multiply"]["value"] == 0.95
    assert decoded["lf rt crossover"]["encoded"] == 12
    assert decoded["lf rt crossover"]["value"] == 720

    mapping = build_lf_crossover_mapping(ROOT / "sysex")
    assert mapping[12] == 720.0
    assert nibble_hilo(parse_sysex(raw).raw[118], parse_sysex(raw).raw[119]) == 15

    folder = find_names_folder(ROOT / "sysex")
    names = analyze_names_folder(folder)
    from m7_sysex.decode_preset import enrich_names_with_parameters
    from m7_sysex.byte_map import build_byte_map

    names = enrich_names_with_parameters(names, results)
    byte_map = build_byte_map(results, names=names)
    roles = {b["offset"]: b for b in byte_map["bytes"]}
    assert "lf rt multiply" in roles[118]["role"]
    assert "lf rt crossover" in roles[120]["role"]
    assert "independent series" in roles[118]["role"]
    assert roles[118]["status"] == "known"
    assert roles[120]["status"] == "known"


def test_lf_rt_multiply_piecewise_table():
    """Series anchors: 0.05/step to 2.0x (enc 36), then 0.1/step to 4.0x (enc 56)."""
    result = analyze_parameter_folder(PARAMS / "lf rt multiply")
    mapping = {
        int(row["encoded"]): row["label"]
        for row in result["best_encoding"]["mapping"]
    }
    assert mapping[0] == 0.2
    assert mapping[1] == 0.25
    assert mapping[11] == 0.75
    assert mapping[42] == 2.6
    assert mapping[56] == 4.0
    for enc, label in mapping.items():
        if enc <= 36:
            expected = 0.2 + 0.05 * enc
        else:
            expected = 2.0 + 0.1 * (enc - 36)
        assert abs(label - expected) < 1e-9, (enc, label)


def test_corpus_layout_claims_in_byte_map():
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.byte_map import build_byte_map
    from m7_sysex.decode_preset import enrich_names_with_parameters
    from m7_sysex.names import analyze_names_folder, find_names_folder

    results = analyze_tree(ROOT / "sysex")
    names = enrich_names_with_parameters(
        analyze_names_folder(find_names_folder(ROOT / "sysex")),
        results,
    )
    byte_map = build_byte_map(results, names=names, sysex_root=ROOT / "sysex")
    by_off = {b["offset"]: b for b in byte_map["bytes"]}

    assert by_off[106]["status"] == "known"
    assert "padding" in by_off[106]["role"].lower()
    assert by_off[97]["status"] == "known"
    assert "family" in by_off[97]["role"].lower()
    assert by_off[145]["status"] == "known"
    assert by_off[98]["status"] == "secondary"
    assert by_off[99]["status"] == "secondary"
    assert by_off[130]["status"] == "known"
    assert "nonlin" in by_off[130]["role"].lower()
    assert "engine/bank-class" in by_off[130]["role"].lower()
    assert by_off[148]["status"] == "known"
    assert "bank index" in by_off[88]["role"].lower()
    assert by_off[88]["status"] == "known"
    assert byte_map["counts"]["unknown"] == 0
    assert byte_map.get("corpus_layout_claims")


def test_preset_inventory_gaps():
    from m7_sysex.names import analyze_names_folder, find_names_folder
    from m7_sysex.preset_inventory import analyze_preset_inventory

    folder = find_names_folder(ROOT / "sysex")
    assert folder is not None
    names = analyze_names_folder(folder)
    inv = analyze_preset_inventory(names)
    assert inv["dump_count"] == len(names["dumps"])
    assert inv["totals"]["addendum_grand"] == 212
    assert len(inv["banks"]) == 11
    rooms = next(r for r in inv["banks"] if r["bank"] == "Rooms")
    assert rooms["count"] == 36
    assert rooms["slot_range"] == "0–35"
    gaps = {g["file"] for g in inv["capture_gaps"]}
    assert "Halls 2.Berliner Hall.syx" in gaps
    assert "Rooms.Long Wood Room.syx" not in gaps
    v1_gaps = {r["bank"]: r for r in inv["v1_count_gaps"]}
    assert v1_gaps["Rooms"]["have"] == 36
    assert v1_gaps["Rooms"]["expected"] == 26
    halls2 = next(b for b in inv["v2_name_gaps"] if b["bank"] == "Halls 2")
    assert "Berliner Hall" in halls2["missing"]
