"""Verify web-ui runtime assets after export sync."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from m7_sysex.export.web_ui import (
    _compact_preset_catalog,
    _compact_runtime_spec,
    _load_serialize_skeletons,
    _runtime_bundle,
    sync_web_ui_assets,
)
from m7_sysex.prog.algorithms import PROG_ALGORITHM_CONSTRAINTS


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_sync_web_ui_assets_writes_runtime_assets(repo_root: Path) -> None:
    sync_web_ui_assets(repo_root)
    public = repo_root / "web-ui" / "public"
    spec = repo_root / "specification"

    presets_full = json.loads(
        (spec / "prog" / "presets" / "presets.json").read_text(encoding="utf-8")
    )
    prog_spec = json.loads(
        (spec / "prog" / "m7_program_dump.spec.json").read_text(encoding="utf-8")
    )
    system_spec = json.loads(
        (spec / "system" / "m7_system_dump.spec.json").read_text(encoding="utf-8")
    )

    runtime = json.loads((public / "m7-runtime.json").read_text(encoding="utf-8"))
    expected = _runtime_bundle(
        prog_spec,
        system_spec,
        presets_full,
        serialize_skeletons=_load_serialize_skeletons(spec),
    )
    assert runtime == expected

    public_presets = runtime["presets"]
    assert public_presets == _compact_preset_catalog(presets_full)
    assert public_presets["algorithms"] == PROG_ALGORITHM_CONSTRAINTS
    assert len(public_presets["presets"]) == presets_full["dump_count"]

    assert runtime["prog"] == _compact_runtime_spec(prog_spec)
    assert runtime["system"] == _compact_runtime_spec(system_spec)

    assert not (public / "spec" / "prog" / "m7_program_dump.spec.json").exists()
    assert not (public / "spec" / "system" / "m7_system_dump.spec.json").exists()
    assert not (public / "spec" / "prog" / "m7_program_dump.ksy").exists()
    assert not (public / "spec" / "system" / "m7_system_dump.ksy").exists()
    assert not (public / "presets" / "presets.json").exists()
    assert not (public / "sync-manifest.json").exists()

    assert not (public / "spec").exists()
    assert not (public / "presets").exists()
    assert not (public / "templates").exists()

    param_manifest = repo_root / "web-ui" / "src" / "generated" / "param-manifest.json"
    assert param_manifest.is_file()

    # Compact JSON (no pretty-print whitespace).
    assert "\n  " not in (public / "m7-runtime.json").read_text(encoding="utf-8")


def test_compress_dist_prunes_legacy_public_mirror_dirs(
    repo_root: Path,
) -> None:
    """Vite copies public/ into dist/; post-build step must drop obsolete trees."""
    import subprocess

    web_ui = repo_root / "web-ui"
    dist = web_ui / "dist"
    dist.mkdir(parents=True, exist_ok=True)
    (dist / "index.html").write_text("<!doctype html><title>t</title>", encoding="utf-8")
    (dist / "spec" / "prog").mkdir(parents=True)
    (dist / "presets").mkdir(parents=True)

    subprocess.run(
        ["node", "scripts/compress-dist.mjs"],
        cwd=web_ui,
        check=True,
    )

    assert not (dist / "spec").exists()
    assert not (dist / "presets").exists()
