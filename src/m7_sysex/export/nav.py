"""Shared navigation helpers and export path utilities."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from ..paths import PROG_DIR, SYSTEM_DIR


def parameter_slug(name: str) -> str:
    """Filesystem-safe slug for a parameter page filename."""
    return "-".join(name.strip().casefold().split())


def preset_slugs(bank: str, preset: str) -> tuple[str, str]:
    """Bank and preset directory slugs under presets/."""
    bank_slug = parameter_slug(bank.replace("&", " and "))
    preset_slug = parameter_slug(preset.replace("&", " and "))
    return bank_slug, preset_slug


def parameter_md_link(name: str, *, prefix: str = "") -> str:
    """Markdown link to a parameter page (``prefix`` is relative path prefix)."""
    return f"[{name}]({prefix}parameters/{parameter_slug(name)}.md)"


def bank_md_link(bank: str, *, prefix: str = "") -> str:
    """Markdown link to a bank index under ``presets/``."""
    bank_slug, _ = preset_slugs(bank, "x")
    return f"[{bank}]({prefix}presets/{bank_slug}/)"


def preset_md_link(
    bank: str,
    preset: str,
    *,
    prefix: str = "",
    page: bool = True,
) -> str:
    """Markdown link to a preset page (``page=True``) or bank-page anchor."""
    bank_slug, preset_slug = preset_slugs(bank, preset)
    if page:
        return f"[{preset}]({prefix}presets/{bank_slug}/{preset_slug}.md)"
    return f"[{preset}]({prefix}presets/{bank_slug}/#{preset_slug})"


def preset_dir(output_dir: Path, bank: str, preset: str) -> Path:
    bank_slug, preset_slug = preset_slugs(bank, preset)
    return Path(output_dir) / "presets" / bank_slug / preset_slug


def parameter_page_path(output_dir: Path, name: str) -> Path:
    return Path(output_dir) / "parameters" / f"{parameter_slug(name)}.md"


def resolve_export_dir(path: Path) -> Path:
    """Treat --out as a directory; map a legacy `.md` path to its stem folder."""
    path = Path(path)
    if path.suffix.lower() == ".md":
        return path.with_suffix("")
    return path


def prog_export_dir(output_root: Path) -> Path:
    return resolve_export_dir(output_root) / PROG_DIR


def system_export_dir(output_root: Path) -> Path:
    return resolve_export_dir(output_root) / SYSTEM_DIR


_LEGACY_ROOT_ARTIFACTS = (
    "README.md",
    "parameters",
    "presets",
    "program-identity.md",
    "preset-sheet.md",
    "preset-inventory.md",
    "byte-map-overview.md",
    "byte-map.md",
    "cross.md",
    "m7_program_dump.ksy",
    "m7_program_dump.spec.json",
)


def remove_legacy_export_roots(repo_root: Path | None = None) -> list[Path]:
    """Drop pre-rename export trees (``docs/sysex-format/``)."""
    base = Path(repo_root) if repo_root is not None else Path.cwd()
    removed: list[Path] = []
    legacy = base.resolve() / "docs" / "sysex-format"
    if legacy.is_dir():
        shutil.rmtree(legacy)
        removed.append(legacy)
    return removed


def clear_export_dir(output_dir: Path) -> list[Path]:
    """Remove prior generated docs (legacy flat layout and prog/ + system/)."""
    cleared: list[Path] = []
    output_dir = resolve_export_dir(output_dir)
    legacy_md = output_dir.parent / f"{output_dir.name}.md"
    if legacy_md.is_file():
        legacy_md.unlink()
        cleared.append(legacy_md)
    for name in _LEGACY_ROOT_ARTIFACTS:
        path = output_dir / name
        if path.is_dir():
            shutil.rmtree(path)
            cleared.append(path)
        elif path.is_file():
            path.unlink()
            cleared.append(path)
    for sub in (PROG_DIR, SYSTEM_DIR):
        path = output_dir / sub
        if path.is_dir():
            shutil.rmtree(path)
            cleared.append(path)
    if output_dir.is_file():
        output_dir.unlink()
        cleared.append(output_dir)
    return cleared


def _page_nav(*, depth: int, current: str | None = None) -> str:
    """Relative nav strip. depth=0 at prog root; depth=1 under parameters/."""
    prefix = "../" * depth
    links = [
        ("Overview", f"{prefix}README.md"),
        ("Parameters", f"{prefix}parameters/README.md"),
        ("Program identity", f"{prefix}program-identity.md"),
        ("Preset inventory", f"{prefix}preset-inventory.md"),
        ("Preset sheet", f"{prefix}preset-sheet.md"),
        ("Byte map", f"{prefix}byte-map-overview.md"),
        ("Cross-series", f"{prefix}cross.md"),
        ("System dumps", f"{prefix}../system/README.md"),
    ]
    parts = []
    for label, href in links:
        if current == label:
            parts.append(f"**{label}**")
        else:
            parts.append(f"[{label}]({href})")
    return " | ".join(parts) + "\n\n"


def _system_page_nav(*, depth: int, current: str | None = None) -> str:
    sys_prefix = "../" * depth if depth else ""
    prog_prefix = "../" * (depth + 1)
    links = [
        ("Program dumps", f"{prog_prefix}prog/README.md"),
        ("System overview", f"{sys_prefix}README.md" if depth else "README.md"),
        ("Parameters", f"{sys_prefix}parameters/README.md"),
    ]
    parts = []
    for label, href in links:
        if current == label:
            parts.append(f"**{label}**")
        else:
            parts.append(f"[{label}]({href})")
    return " | ".join(parts) + "\n\n"


def write_export_index(
    output_root: Path,
    *,
    today: str,
    prog_byte_map: dict[str, Any] | None = None,
    system_byte_map: dict[str, Any] | None = None,
    prog_parameter_count: int = 0,
    system_parameter_count: int = 0,
    preset_count: int = 0,
) -> Path:
    """Index at specification/README.md linking prog/ and system/."""
    from .open_items import (
        PROG_OPEN_ITEMS,
        SYSTEM_OPEN_ITEMS,
        render_open_items_markdown,
    )

    root = resolve_export_dir(output_root)
    root.mkdir(parents=True, exist_ok=True)

    prog_cov = ""
    if prog_byte_map:
        c = prog_byte_map["counts"]
        prog_cov = (
            f"**{c['known_or_frame']}** known/frame/checksum · "
            f"**{c['secondary']}** secondary · **{c['unknown']}** unknown "
            f"(of {c['total']} bytes)"
        )
    sys_cov = ""
    if system_byte_map:
        c = system_byte_map["counts"]
        sys_cov = (
            f"**{c['known_or_frame']}** known/frame/checksum · "
            f"**{c['secondary']}** secondary · **{c['unknown']}** unknown "
            f"(of {c['total']} bytes)"
        )

    open_count = len(PROG_OPEN_ITEMS) + len(SYSTEM_OPEN_ITEMS)
    lines = [
        "# M7 SysEx specification",
        "",
        "Generated specification for **program (PROG)** and **system (SYSTEM)** "
        "SysEx dump families.",
        "",
        "> Auto-generated by `python run.py` (or `python -m m7_sysex export`). "
        "Re-run after adding dumps; do not hand-edit generated pages.",
        "",
        f"_Last exported: {today}_",
        "",
        "## Families",
        "",
        "- [Program dumps](prog/README.md) — 157-byte program dumps, "
        f"{prog_parameter_count or 18} sound parameters, "
        f"{preset_count or 222} factory presets, byte map, Kaitai spec",
        "- [System dumps](system/README.md) — 77-byte system / I/O dumps, "
        f"{system_parameter_count or 8} captured settings",
        "- [Open questions](open-items.md) — tracked unknowns and follow-ups "
        f"({open_count} items)",
        "",
    ]
    if prog_cov or sys_cov:
        lines.extend(["## Coverage", ""])
        if prog_cov:
            lines.append(f"- **PROG:** {prog_cov}")
        if sys_cov:
            lines.append(f"- **SYSTEM:** {sys_cov}")
        lines.append("")

    lines.extend(
        [
            "## Companion docs",
            "",
            "- [Capture guide](../docs/capture-guide.md)",
            "- [Encoding sources](../docs/encoding-sources.md)",
            "- [Parameter catalog](../docs/parameter-catalog.md)",
            "- [Manual notes](../docs/manual-notes.md)",
            "",
        ]
    )
    path = root / "README.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    (root / "open-items.md").write_text(
        render_open_items_markdown(), encoding="utf-8"
    )
    return path
