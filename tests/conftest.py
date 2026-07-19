"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.kaitai_support import (
    KaitaiCompileCache,
    PROG_KSY,
    SYSTEM_KSY,
    ensure_kaitai_compiler,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def kaitai_compiler():
    pytest.importorskip("kaitaistruct")
    return ensure_kaitai_compiler()


@pytest.fixture(scope="session")
def kaitai_cache(kaitai_compiler, tmp_path_factory) -> KaitaiCompileCache:
    cache = KaitaiCompileCache(kaitai_compiler)
    cache.out_root = tmp_path_factory.mktemp("kaitai_generated")
    return cache


@pytest.fixture(scope="session")
def kaitai_prog_parser(kaitai_cache: KaitaiCompileCache):
    return kaitai_cache.parser_for(PROG_KSY, kaitai_cache.out_root / "prog")


@pytest.fixture(scope="session")
def kaitai_system_parser(kaitai_cache: KaitaiCompileCache):
    return kaitai_cache.parser_for(SYSTEM_KSY, kaitai_cache.out_root / "system")


@pytest.fixture(scope="session")
def kaitai_fresh_prog_export(kaitai_cache: KaitaiCompileCache, tmp_path_factory):
    """Write a live-exported PROG spec (compile deferred to parser fixture)."""
    from m7_sysex.analyze import analyze_tree
    from m7_sysex.byte_map import build_byte_map
    from m7_sysex.decode_preset import enrich_names_with_parameters
    from m7_sysex.kaitai_spec import write_program_dump_spec
    from m7_sysex.names import analyze_names_folder, find_names_folder
    from m7_sysex.paths import prog_menus_root
    from m7_sysex.prog.menus import analyze_menus_folder

    sysex = ROOT / "sysex"
    results = analyze_tree(sysex)
    names = enrich_names_with_parameters(
        analyze_names_folder(find_names_folder(sysex)),
        results,
    )
    byte_map = build_byte_map(results, names=names, sysex_root=sysex)
    menus_analysis = analyze_menus_folder(prog_menus_root(sysex), sysex)
    out = tmp_path_factory.mktemp("kaitai_fresh_prog")
    write_program_dump_spec(
        out, byte_map, results, names=names, menus_analysis=menus_analysis
    )
    return out


@pytest.fixture(scope="session")
def kaitai_fresh_system_export(kaitai_cache: KaitaiCompileCache, tmp_path_factory):
    """Write a live-exported SYSTEM spec (compile deferred to parser fixture)."""
    from m7_sysex.system import analyze_system_tree, build_system_byte_map
    from m7_sysex.system.kaitai_spec import write_system_dump_spec

    sysex = ROOT / "sysex"
    results = analyze_system_tree(sysex)
    byte_map = build_system_byte_map(results, sysex_root=sysex)
    out = tmp_path_factory.mktemp("kaitai_fresh_system")
    write_system_dump_spec(out, byte_map, results)
    return out


@pytest.fixture(scope="session")
def kaitai_fresh_prog_parser(kaitai_cache: KaitaiCompileCache, kaitai_fresh_prog_export):
    ksy = kaitai_fresh_prog_export / "m7_program_dump.ksy"
    return kaitai_cache.parser_for(ksy, kaitai_fresh_prog_export / "py")


@pytest.fixture(scope="session")
def kaitai_fresh_system_parser(kaitai_cache: KaitaiCompileCache, kaitai_fresh_system_export):
    ksy = kaitai_fresh_system_export / "m7_system_dump.ksy"
    return kaitai_cache.parser_for(ksy, kaitai_fresh_system_export / "py")
