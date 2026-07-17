"""Dump-family registry for PROG vs SYSTEM SysEx."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .frame import (
    PROGRAM_DUMP_HEADER,
    PROGRAM_MESSAGE_LENGTH,
    SYSTEM_DUMP_HEADER,
    SYSTEM_MESSAGE_LENGTH,
    parse_sysex,
    parse_system_sysex,
)
from .paths import (
    LEGACY_EDIT_DIR,
    LEGACY_PRESETS_DIR,
    LEGACY_SYSTEM_DIR,
    PROG_DIR,
    PROG_EDIT_DIR,
    PROG_PARAMETERS_DIR,
    PROG_PRESETS_DIR,
    SYSTEM_DIR,
    prog_parameters_root,
    prog_root,
    resolve_sysex_root,
    system_root,
)


@dataclass(frozen=True)
class DumpFamily:
    id: str
    header: bytes
    message_length: int
    corpus_root_fn: Callable[[Path], Path]
    parameters_subdir: str | None
    export_subdir: str
    parse_fn: Callable[[bytes], Any]


PROG_FAMILY = DumpFamily(
    id="prog",
    header=PROGRAM_DUMP_HEADER,
    message_length=PROGRAM_MESSAGE_LENGTH,
    corpus_root_fn=prog_root,
    parameters_subdir=PROG_PARAMETERS_DIR,
    export_subdir=PROG_DIR,
    parse_fn=parse_sysex,
)

SYSTEM_FAMILY = DumpFamily(
    id="system",
    header=SYSTEM_DUMP_HEADER,
    message_length=SYSTEM_MESSAGE_LENGTH,
    corpus_root_fn=system_root,
    parameters_subdir=None,
    export_subdir=SYSTEM_DIR,
    parse_fn=parse_system_sysex,
)

DUMP_FAMILIES: tuple[DumpFamily, ...] = (PROG_FAMILY, SYSTEM_FAMILY)


def is_prog_corpus_relative(rel: Path) -> bool:
    """True for parameter series and preset dumps under ``sysex/prog/``."""
    parts = rel.parts
    if not parts:
        return False
    if parts[0] == PROG_DIR:
        if len(parts) < 2:
            return False
        if parts[1] in (PROG_EDIT_DIR, LEGACY_EDIT_DIR):
            return False
        return True
    if parts[0].startswith("_") and parts[0] not in (LEGACY_PRESETS_DIR,):
        return False
    return parts[0] != LEGACY_SYSTEM_DIR and parts[0] != SYSTEM_DIR


def is_prog_corpus_dump(path: Path, sysex_root: Path | None = None) -> bool:
    path = Path(path)
    if sysex_root is None:
        return is_prog_corpus_relative(Path(path.name))
    try:
        rel = path.resolve().relative_to(resolve_sysex_root(sysex_root))
    except ValueError:
        return False
    return is_prog_corpus_relative(rel)


def prog_parameters_dir(sysex_root: Path) -> Path:
    return prog_parameters_root(sysex_root)
