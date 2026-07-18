"""Kaitai / machine byte-spec generation from the byte map."""

from pathlib import Path

import pytest

from tests.kaitai_support import PROG_KSY, SYSTEM_KSY

ROOT = Path(__file__).resolve().parents[1]


def _inputs():
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
    return byte_map, results, names


def test_build_program_dump_spec_covers_full_message():
    from m7_sysex.kaitai_spec import build_program_dump_spec

    byte_map, results, names = _inputs()
    spec = build_program_dump_spec(byte_map, results, names=names)
    assert spec["message_length"] == 157
    assert spec["fields"][0]["id"] == "sysex_start"
    assert spec["fields"][-1]["id"] == "sysex_end"
    assert any(f["id"] == "reverb_time" for f in spec["fields"])
    assert any(f["id"] == "checksum" for f in spec["fields"])
    assert spec["checksum"]["algorithm"] == "CRC-16/ARC"
    # Contiguous coverage already asserted inside builder.


def test_render_kaitai_yaml_has_layout_and_nibble_type():
    from m7_sysex.kaitai_spec import build_program_dump_spec, render_kaitai_yaml

    byte_map, results, names = _inputs()
    spec = build_program_dump_spec(byte_map, results, names=names)
    ksy = render_kaitai_yaml(spec)
    assert "meta:" in ksy
    assert "id: m7_program_dump" in ksy
    assert "id: reverb_time" in ksy
    assert "id: delay_level" in ksy
    assert "contents: [0xf0]" in ksy
    assert "types:" in ksy
    assert "enums:" in ksy
    assert "bank_index_values:" in ksy
    assert "diffusion_values:" in ksy
    assert "enum: diffusion_values" in ksy
    assert "0: low  # Low" in ksy
    assert "1: v_1  # 1" in ksy
    assert "type: reverb_time_encoded" in ksy
    assert "valid:" in ksy
    assert "max: 15" in ksy
    diffusion = next(f for f in spec["fields"] if f["id"] == "diffusion")
    assert diffusion.get("value_map")
    assert any(f.get("value_map") for f in spec["fields"] if f.get("parameter"))


def test_display_enum_lists_menu_names():
    from m7_sysex.kaitai_spec import build_program_dump_spec, render_kaitai_yaml
    from m7_sysex.paths import prog_menus_root
    from m7_sysex.prog.menus import analyze_menus_folder

    byte_map, results, names = _inputs()
    menus = analyze_menus_folder(prog_menus_root(ROOT / "sysex"), ROOT / "sysex")
    spec = build_program_dump_spec(
        byte_map, results, names=names, menus_analysis=menus
    )
    cursor = next(f for f in spec["fields"] if f["id"] == "display")
    value_map = cursor.get("value_map") or {}
    entries = value_map.get("entries") or []
    labels = [str(e["label"]) for e in entries]
    assert value_map.get("enum_id") == "display_values"
    assert any("idle (no menu)" in label for label in labels)
    assert any("browse: reverb time (0)" in label for label in labels)
    assert any("edit: predelay (2)" in label for label in labels)
    assert cursor.get("series_root") == "sysex/prog/menus"
    assert "parameter" not in cursor

    ksy = render_kaitai_yaml(spec)
    assert "display_values:" in ksy
    assert "type: display_encoded" in ksy
    assert "browse: reverb time (0)" in ksy


def test_render_kaitai_yaml_keeps_generic_nibble_for_unmapped_fields():
    from m7_sysex.kaitai_spec import build_program_dump_spec, render_kaitai_yaml

    byte_map, results, names = _inputs()
    ksy = render_kaitai_yaml(
        build_program_dump_spec(byte_map, results, names=names)
    )
    assert "type: nibble_u8_hilo" in ksy
    assert "program_slot" in ksy


def test_write_program_dump_spec(tmp_path):
    from m7_sysex.kaitai_spec import (
        KAITAI_NAME,
        SPEC_JSON_NAME,
        write_program_dump_spec,
    )

    byte_map, results, names = _inputs()
    json_path, ksy_path, spec = write_program_dump_spec(
        tmp_path, byte_map, results, names=names
    )
    assert json_path.name == SPEC_JSON_NAME
    assert ksy_path.name == KAITAI_NAME
    assert json_path.is_file()
    assert ksy_path.is_file()
    assert spec["format"] == "bricasti-m7-program-dump"


def _system_inputs():
    from m7_sysex.system import analyze_system_tree, build_system_byte_map

    results = analyze_system_tree(ROOT / "sysex")
    byte_map = build_system_byte_map(results, sysex_root=ROOT / "sysex")
    return byte_map, results


def test_build_system_dump_spec_covers_full_message():
    from m7_sysex.system.kaitai_spec import build_system_dump_spec

    byte_map, results = _system_inputs()
    spec = build_system_dump_spec(byte_map, results)
    assert spec["message_length"] == 77
    assert spec["fields"][0]["id"] == "sysex_start"
    assert spec["fields"][-1]["id"] == "sysex_end"
    assert any(f["id"] == "checksum" for f in spec["fields"])
    assert any(f.get("parameter") == "midi channel" for f in spec["fields"])


def test_render_system_kaitai_yaml():
    from m7_sysex.kaitai_render import render_kaitai_yaml
    from m7_sysex.system.kaitai_spec import build_system_dump_spec

    byte_map, results = _system_inputs()
    spec = build_system_dump_spec(byte_map, results)
    ksy = render_kaitai_yaml(spec)
    assert "id: m7_system_dump" in ksy
    assert "contents: [0xf0]" in ksy
    assert "enums:" in ksy
    assert "audio_format_values:" in ksy
    assert "audio_routing_values:" in ksy
    assert "enum: audio_routing_values" in ksy
    assert "1: mono_l  # mono l" in ksy
    audio_routing = next(f for f in spec["fields"] if f["id"] == "audio_routing")
    assert audio_routing.get("value_map")
    assert "wet path" in audio_routing["description"].lower()
    assert audio_routing.get("encoding_notes")


def test_system_dump_spec_uses_manual_descriptions_not_encoding_notes():
    from m7_sysex.system.kaitai_spec import build_system_dump_spec

    byte_map, results = _system_inputs()
    spec = build_system_dump_spec(byte_map, results)
    by_param = {
        f["parameter"]: f
        for f in spec["fields"]
        if f.get("parameter")
    }
    assert "internal mixing" in by_param["wet gain"]["description"].lower()
    assert "AES digital" in by_param["audio format"]["description"]
    assert by_param["wet gain"].get("encoding_notes")
    assert "0.5" in by_param["wet gain"]["encoding_notes"]
    assert "offset 13" not in by_param["audio routing"]["description"].lower()


def test_write_system_dump_spec(tmp_path):
    from m7_sysex.system.kaitai_spec import (
        KAITAI_NAME,
        SPEC_JSON_NAME,
        write_system_dump_spec,
    )

    byte_map, results = _system_inputs()
    json_path, ksy_path, spec = write_system_dump_spec(
        tmp_path, byte_map, results
    )
    assert json_path.name == SPEC_JSON_NAME
    assert ksy_path.name == KAITAI_NAME
    assert spec["format"] == "bricasti-m7-system-dump"


def test_committed_prog_specs_match_live_export():
    import json

    from m7_sysex.kaitai_render import render_kaitai_yaml
    from m7_sysex.kaitai_spec import build_program_dump_spec
    from m7_sysex.paths import prog_menus_root
    from m7_sysex.prog.menus import analyze_menus_folder

    byte_map, results, names = _inputs()
    menus = analyze_menus_folder(prog_menus_root(ROOT / "sysex"), ROOT / "sysex")
    live_spec = build_program_dump_spec(
        byte_map, results, names=names, menus_analysis=menus
    )
    live_ksy = render_kaitai_yaml(live_spec)

    committed_spec = json.loads(
        (ROOT / "specification" / "prog" / "m7_program_dump.spec.json").read_text(
            encoding="utf-8"
        )
    )
    committed_ksy = (
        ROOT / "specification" / "prog" / "m7_program_dump.ksy"
    ).read_text(encoding="utf-8")

    assert live_spec == committed_spec
    assert live_ksy == committed_ksy


def test_committed_system_specs_match_live_export():
    import json

    from m7_sysex.kaitai_render import render_kaitai_yaml
    from m7_sysex.system.kaitai_spec import build_system_dump_spec

    byte_map, results = _system_inputs()
    live_spec = build_system_dump_spec(byte_map, results)
    live_ksy = render_kaitai_yaml(live_spec)

    committed_spec = json.loads(
        (ROOT / "specification" / "system" / "m7_system_dump.spec.json").read_text(
            encoding="utf-8"
        )
    )
    committed_ksy = (
        ROOT / "specification" / "system" / "m7_system_dump.ksy"
    ).read_text(encoding="utf-8")

    assert live_spec == committed_spec
    assert live_ksy == committed_ksy


def test_spec_json_ksy_and_python_enums_agree(kaitai_prog_parser, kaitai_system_parser):
    from tests.kaitai_support import (
        assert_compiled_enums_match_value_maps,
        assert_spec_json_ksy_value_maps_agree,
        fields_with_value_map,
        load_spec,
        value_maps_from_fields,
    )

    for spec_path, parser, ksy_path in (
        (
            ROOT / "specification" / "prog" / "m7_program_dump.spec.json",
            kaitai_prog_parser,
            ROOT / "specification" / "prog" / "m7_program_dump.ksy",
        ),
        (
            ROOT / "specification" / "system" / "m7_system_dump.spec.json",
            kaitai_system_parser,
            ROOT / "specification" / "system" / "m7_system_dump.ksy",
        ),
    ):
        fields = load_spec(spec_path)["fields"]
        ksy_text = ksy_path.read_text(encoding="utf-8")
        assert_spec_json_ksy_value_maps_agree(fields, ksy_text)
        value_maps = value_maps_from_fields(fields)
        assert value_maps, spec_path.name
        assert_compiled_enums_match_value_maps(parser, value_maps)
        assert all(f.get("value_map") for f in fields if f.get("parameter"))
        if "prog" in spec_path.parts:
            bank = next(f for f in fields if f["id"] == "bank_index")
            assert bank.get("value_map")


@pytest.mark.slow
def test_kaitai_compile_cache_compiles_once_per_spec(
    kaitai_cache,
    kaitai_prog_parser,
    kaitai_system_parser,
    kaitai_fresh_prog_parser,
    kaitai_fresh_system_parser,
    kaitai_fresh_prog_export,
    kaitai_fresh_system_export,
    tmp_path,
):
    """Each ``.ksy`` is passed to kaitai-struct-compiler at most once per run."""
    fresh_prog_ksy = kaitai_fresh_prog_export / "m7_program_dump.ksy"
    fresh_system_ksy = kaitai_fresh_system_export / "m7_system_dump.ksy"

    assert kaitai_cache.compile_count(PROG_KSY) == 1
    assert kaitai_cache.compile_count(SYSTEM_KSY) == 1
    assert kaitai_cache.compile_count(fresh_prog_ksy) == 1
    assert kaitai_cache.compile_count(fresh_system_ksy) == 1

    again = kaitai_cache.parser_for(PROG_KSY, kaitai_cache.out_root / "prog")
    assert again is kaitai_prog_parser
    assert kaitai_cache.compile_count(PROG_KSY) == 1

    for target in ("javascript", "csharp"):
        out = tmp_path / target
        kaitai_cache.compile_target(PROG_KSY, out, target)
        assert any(out.iterdir())
        kaitai_cache.compile_target(PROG_KSY, out, target)
        assert kaitai_cache.compile_count(PROG_KSY, target) == 1
