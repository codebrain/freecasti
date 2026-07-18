"""Canonical sysex corpus paths (type-first layout)."""

from __future__ import annotations

from pathlib import Path

PROG_DIR = "prog"
SYSTEM_DIR = "system"
SPECIFICATION_DIR = "specification"
PROG_PARAMETERS_DIR = "parameters"
PROG_PRESETS_DIR = "presets"
PROG_EDIT_DIR = "edit"
PROG_FULL_SWEEP_DIR = "full sweep"
PROG_MENUS_DIR = "menus"
SYSTEM_MENUS_DIR = "menus"

LEGACY_PRESETS_DIR = "_presets"
LEGACY_EDIT_DIR = "_edit"
LEGACY_SYSTEM_DIR = "_system"


def resolve_sysex_root(sysex_root: Path) -> Path:
    return Path(sysex_root).resolve()


def prog_root(sysex_root: Path) -> Path:
    return resolve_sysex_root(sysex_root) / PROG_DIR


def prog_parameters_root(sysex_root: Path) -> Path:
    return prog_root(sysex_root) / PROG_PARAMETERS_DIR


def prog_presets_root(sysex_root: Path) -> Path:
    return prog_root(sysex_root) / PROG_PRESETS_DIR


def prog_edit_root(sysex_root: Path) -> Path:
    return prog_root(sysex_root) / PROG_EDIT_DIR


def prog_full_sweep_root(sysex_root: Path) -> Path:
    return prog_root(sysex_root) / PROG_FULL_SWEEP_DIR


def prog_menus_root(sysex_root: Path) -> Path:
    return prog_root(sysex_root) / PROG_MENUS_DIR


def system_root(sysex_root: Path) -> Path:
    return resolve_sysex_root(sysex_root) / SYSTEM_DIR


def prog_byte_map_path(sysex_root: Path) -> Path:
    return prog_root(sysex_root) / "byte_map.json"


def prog_cross_analysis_path(sysex_root: Path) -> Path:
    return prog_root(sysex_root) / "cross_analysis.json"


def system_byte_map_path(sysex_root: Path) -> Path:
    return system_root(sysex_root) / "byte_map.json"


def specification_root(repo_root: Path | None = None) -> Path:
    """Root folder for generated SysEx specification docs (``specification/``)."""
    base = Path(repo_root) if repo_root is not None else Path.cwd()
    return base.resolve() / SPECIFICATION_DIR


def corpus_sysex_root(path: Path) -> Path:
    """Return the top-level ``sysex/`` directory for any path inside the corpus."""
    p = Path(path).resolve()
    if (p / PROG_DIR).is_dir():
        return p
    if p.name == PROG_DIR:
        return p.parent
    if p.parent.name == PROG_DIR:
        return p.parent.parent
    if p.name.startswith("_"):
        return p.parent
    for ancestor in p.parents:
        if (ancestor / PROG_DIR).is_dir():
            return ancestor
        if (ancestor / LEGACY_PRESETS_DIR).is_dir():
            return ancestor
    return p
