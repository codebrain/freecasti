"""Freshly regenerated docs must carry every register-blob learning.

These tests render the documentation *in memory* (not from committed files),
so any future regeneration that drops a session learning fails CI.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

TODAY = "2026-07-19"

WITNESS_FILES = (
    "fullsweep-rooms-studio-a.syx",
    "samples/rooms-studio-a-b1s1-delay-edit.syx",
    "samples/charset-b1s1-renamed.syx",
    "samples/charset-b1s1-rt5s-unstored-edit.syx",
    "samples/charset-b1s1-rt5s-stored.syx",
)


@pytest.fixture(scope="module")
def blob_page() -> str:
    from m7_sysex.export.identity_bytes import render_register_basis_blob_page

    return render_register_basis_blob_page(today=TODAY)


@pytest.fixture(scope="module")
def register_bank_page() -> str:
    from m7_sysex.export.identity_bytes import render_register_bank_page

    return render_register_bank_page(today=TODAY)


@pytest.fixture(scope="module")
def register_page() -> str:
    from m7_sysex.export.identity_bytes import render_register_page

    return render_register_page(today=TODAY)


def test_blob_page_has_one_layout_row_per_field(blob_page: str):
    from m7_sysex.prog.register_blob import REGISTER_BLOB_FIELDS

    assert "## Bit layout" in blob_page
    for field in REGISTER_BLOB_FIELDS:
        bits = (
            f"{field.bit_offset}\u2013{field.bit_end}"
            if field.bit_width > 1
            else str(field.bit_offset)
        )
        row_prefix = f"| {bits} | {field.bit_width} | {field.label} |"
        assert row_prefix in blob_page, field.id


def test_blob_page_charset_table_is_complete(blob_page: str):
    assert "## Name charset (6-bit)" in blob_page
    assert "&123456789ABCD" in blob_page
    assert "`0123456789`" in blob_page
    assert "`ABCDEFGHIJKLMNOPQRSTUVWXYZ`" in blob_page
    assert "`abcdefghijklmnopqrstuvwxyz`" in blob_page
    assert "inferred by continuity" in blob_page


def test_blob_page_store_counter_semantics(blob_page: str):
    assert "## Store-generation counter" in blob_page
    assert "3 for B0 R0\u2013R2" in blob_page
    assert "renaming" in blob_page and "stores twice" in blob_page
    assert "bumped its counter from 2 to 3" in blob_page


def test_blob_page_snapshot_semantics_and_delay_block(blob_page: str):
    assert "## Stored snapshot semantics" in blob_page
    assert "stored register values" in blob_page
    assert "bits 197\u2013211" in blob_page
    assert "delay level 15 / time 11 / mod 6" in blob_page
    assert "before* the delay was dialed in" in blob_page


def test_blob_page_cites_all_witness_captures(blob_page: str):
    assert "## Witness captures" in blob_page
    for name in WITNESS_FILES:
        assert name.split("/")[-1] in blob_page, name


def test_blob_page_links_payload_twins(blob_page: str):
    assert "[program name](program-name.md)" in blob_page
    assert "[reverb time](reverb-time.md)" in blob_page
    assert "[delay level](delay-level.md)" in blob_page
    assert "[bank index mirror](bank-index.md)" in blob_page


def test_blob_page_documents_93_95_loaded_basis(blob_page: str):
    assert "loaded as the running basis" in blob_page
    assert "[register bank](register-bank.md)" in blob_page
    assert "[register](register.md)" in blob_page
    assert "store alone does **not** update them" in blob_page


def test_register_bank_and_register_pages_carry_loaded_basis_semantics(
    register_bank_page: str, register_page: str
):
    for page in (register_bank_page, register_page):
        assert "loaded as the running basis" in page
    assert "store alone" in register_bank_page
    assert "charset-b1s1-rt5s-stored.syx" in register_bank_page
    assert "store alone does not update it" in register_page.replace("**", "")


def test_identity_pages_include_blob_page_entry():
    from m7_sysex.export.identity_bytes import IDENTITY_BYTE_PAGES

    entry = next(
        p for p in IDENTITY_BYTE_PAGES if p["slug"] == "register-basis-blob"
    )
    assert entry["name"] == "Register basis blob"
    assert "24-87" in entry["sysex"]
    assert "nibble_bitstream" in entry["sysex"]


def test_frame_section_links_blob_page():
    from m7_sysex.export.prog import FRAME_SECTION

    assert (
        "[bytes/register-basis-blob.md](bytes/register-basis-blob.md)"
        in FRAME_SECTION
    )
    assert "bit-packed snapshot of the stored register" in FRAME_SECTION


def test_rendering_is_deterministic(blob_page: str):
    from m7_sysex.export.identity_bytes import render_register_basis_blob_page
    from m7_sysex.prog.register_blob import runtime_reg_blob

    assert render_register_basis_blob_page(today=TODAY) == blob_page
    assert runtime_reg_blob() == runtime_reg_blob()


@pytest.fixture(scope="module")
def fresh_byte_map():
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


def test_byte_map_overview_links_blob_page(fresh_byte_map):
    from m7_sysex.byte_map import render_byte_map_overview_markdown

    md = render_byte_map_overview_markdown(fresh_byte_map)
    assert "[register basis blob](bytes/register-basis-blob.md)" in md


def test_byte_map_24_87_row_carries_blob_role(fresh_byte_map):
    from m7_sysex.byte_map import render_byte_map_markdown

    md = render_byte_map_markdown(fresh_byte_map)
    assert "bytes/register-basis-blob.md" in md
    assert "snapshot of the **stored register**" in md


@pytest.mark.slow
def test_full_pipeline_export_smoke(fresh_byte_map, tmp_path):
    """export_sysex_format into a temp dir carries every blob artifact."""
    import json

    from m7_sysex.analyze import analyze_tree
    from m7_sysex.decode_preset import enrich_names_with_parameters
    from m7_sysex.export.prog import export_sysex_format
    from m7_sysex.names import analyze_names_folder, find_names_folder
    from m7_sysex.prog.register_blob import REGISTER_BLOB_FIELDS

    results = analyze_tree(ROOT / "sysex")
    names = enrich_names_with_parameters(
        analyze_names_folder(find_names_folder(ROOT / "sysex")),
        results,
    )
    export_sysex_format(
        results, tmp_path, byte_map=fresh_byte_map, names=names
    )
    prog_dir = tmp_path / "prog"

    page = (prog_dir / "bytes" / "register-basis-blob.md").read_text(
        encoding="utf-8"
    )
    for field in REGISTER_BLOB_FIELDS:
        assert f"| {field.label} |" in page, field.id

    overview = (prog_dir / "byte-map-overview.md").read_text(encoding="utf-8")
    assert "[register basis blob](bytes/register-basis-blob.md)" in overview

    ksy = (prog_dir / "m7_program_dump.ksy").read_text(encoding="utf-8")
    assert "  register_basis_blob:" in ksy
    assert "register_name_char:" in ksy
    assert "is_register_basis:" in ksy

    spec = json.loads(
        (prog_dir / "m7_program_dump.spec.json").read_text(encoding="utf-8")
    )
    blob_field = next(
        f for f in spec["fields"] if f["id"] == "register_basis_blob"
    )
    assert blob_field["type_ref"] == "register_basis_blob"
    assert blob_field["blob"]["instances"]

    # Determinism: a second export produces identical artifacts.
    second = tmp_path / "again"
    export_sysex_format(
        results, second, byte_map=fresh_byte_map, names=names
    )
    for rel in (
        Path("prog") / "bytes" / "register-basis-blob.md",
        Path("prog") / "m7_program_dump.ksy",
        Path("prog") / "m7_program_dump.spec.json",
    ):
        assert (second / rel).read_text(encoding="utf-8") == (
            tmp_path / rel
        ).read_text(encoding="utf-8"), rel


@pytest.mark.slow
def test_runtime_bundle_carries_reg_blob_key(tmp_path):
    import json

    from m7_sysex.export.web_ui import (
        _load_prog_ui_state,
        _runtime_bundle,
        _serialize_skeletons,
    )
    from m7_sysex.prog.register_blob import runtime_reg_blob

    spec_dir = ROOT / "specification"
    prog_spec = json.loads(
        (spec_dir / "prog" / "m7_program_dump.spec.json").read_text(
            encoding="utf-8"
        )
    )
    system_spec = json.loads(
        (spec_dir / "system" / "m7_system_dump.spec.json").read_text(
            encoding="utf-8"
        )
    )
    presets_full = json.loads(
        (spec_dir / "prog" / "presets" / "presets.json").read_text(
            encoding="utf-8"
        )
    )
    bundle = _runtime_bundle(
        prog_spec,
        system_spec,
        presets_full,
        serialize_skeletons=_serialize_skeletons(prog_spec, system_spec),
        prog_ui=_load_prog_ui_state(ROOT),
    )
    assert bundle["reg_blob"] == runtime_reg_blob()

    committed = json.loads(
        (ROOT / "web-ui" / "public" / "m7-runtime.json").read_text(
            encoding="utf-8"
        )
    )
    assert committed["reg_blob"] == runtime_reg_blob()
