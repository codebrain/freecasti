"""Relative links in committed markdown resolve to real files and anchors."""

from pathlib import Path

from m7_sysex.markdown_links import (
    extract_markdown_links,
    find_broken_markdown_links,
    repo_markdown_files,
    validate_markdown_link,
)

ROOT = Path(__file__).resolve().parents[1]


def test_repo_markdown_files_include_documentation_tree():
    paths = {p.relative_to(ROOT) for p in repo_markdown_files(ROOT)}
    assert Path("README.md") in paths
    assert Path("docs/README.md") in paths
    assert Path("specification/README.md") in paths
    assert Path("web-ui/README.md") in paths
    assert not any("node_modules" in p.parts for p in paths)


def test_all_markdown_links_resolve():
    broken = find_broken_markdown_links(ROOT)
    if not broken:
        return
    lines = [
        f"{item.link.source.relative_to(ROOT)}:{item.link.line} {item.link.url!r} — {item.reason}"
        for item in broken[:40]
    ]
    if len(broken) > 40:
        lines.append(f"... and {len(broken) - 40} more")
    raise AssertionError(
        f"{len(broken)} broken markdown link(s):\n" + "\n".join(lines)
    )


def test_anchor_links_resolve(tmp_path: Path):
    page = tmp_path / "page.md"
    page.write_text(
        "## Open questions\n\nSee [overview](README.md#open-questions).\n",
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text("## Open questions\n", encoding="utf-8")
    broken = [
        validate_markdown_link(link, repo_root=tmp_path)
        for link in extract_markdown_links(page.read_text(encoding="utf-8"), page)
    ]
    assert all(item is None for item in broken)
