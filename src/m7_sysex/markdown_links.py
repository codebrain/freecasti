"""Validate relative links in committed markdown documentation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

FENCED_CODE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`]+`")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+)$")


class MarkdownLinksError(ValueError):
    """Raised when one or more relative markdown links do not resolve."""


@dataclass(frozen=True, slots=True)
class MarkdownLink:
    source: Path
    line: int
    url: str


@dataclass(frozen=True, slots=True)
class BrokenMarkdownLink:
    link: MarkdownLink
    reason: str


def repo_markdown_files(repo_root: Path) -> list[Path]:
    """Markdown pages tracked as project documentation (not node_modules)."""
    root = repo_root.resolve()
    candidates: list[Path] = []
    for path in (
        root / "README.md",
        root / "docs",
        root / "specification",
        root / "web-ui" / "README.md",
    ):
        if path.is_file():
            candidates.append(path)
        elif path.is_dir():
            candidates.extend(
                md
                for md in path.rglob("*.md")
                if "node_modules" not in md.parts
            )
    return sorted(set(candidates))


def strip_verbatim_markdown(text: str) -> str:
    """Remove fenced and inline code so example URLs are not validated."""
    text = FENCED_CODE.sub("", text)
    return INLINE_CODE.sub("", text)


def github_heading_anchor(heading: str) -> str:
    """GitHub-compatible slug for a markdown heading."""
    text = re.sub(r"<[^>]+>", "", heading).strip().casefold()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def markdown_heading_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    for line in text.splitlines():
        if match := HEADING.match(line):
            anchors.add(github_heading_anchor(match.group(1)))
    return anchors


def _parse_link_target(raw: str) -> tuple[str, str | None]:
    target = raw.strip().split()[0].strip("<>").strip('"').strip("'")
    if "#" in target:
        path_part, anchor = target.split("#", 1)
        return path_part, anchor or None
    return target, None


def extract_markdown_links(text: str, source: Path) -> list[MarkdownLink]:
    links: list[MarkdownLink] = []
    stripped = strip_verbatim_markdown(text)
    for line_no, line in enumerate(stripped.splitlines(), start=1):
        for match in MARKDOWN_LINK.finditer(line):
            links.append(MarkdownLink(source=source, line=line_no, url=match.group(1)))
    return links


def _skip_external_url(url: str) -> bool:
    lowered = url.casefold()
    return lowered.startswith(("http://", "https://", "mailto:", "tel:", "data:"))


def _rel(path: Path, repo_root: Path) -> str:
    return str(path.resolve().relative_to(repo_root.resolve()))


def validate_markdown_link(
    link: MarkdownLink,
    *,
    repo_root: Path,
) -> BrokenMarkdownLink | None:
    raw = link.url.strip()
    if _skip_external_url(raw):
        return None

    root = repo_root.resolve()
    path_part, anchor = _parse_link_target(raw)
    source_text = link.source.read_text(encoding="utf-8")
    source_anchors = markdown_heading_anchors(source_text)

    if not path_part:
        if anchor and anchor not in source_anchors:
            return BrokenMarkdownLink(
                link=link,
                reason=f"anchor #{anchor} not found in {_rel(link.source, root)}",
            )
        return None

    target = (link.source.parent / path_part).resolve()
    if not target.exists():
        return BrokenMarkdownLink(
            link=link,
            reason=(
                f"target {path_part!r} not found from "
                f"{_rel(link.source, root)}:{link.line}"
            ),
        )

    if anchor and target.is_file() and target.suffix.casefold() == ".md":
        target_anchors = markdown_heading_anchors(target.read_text(encoding="utf-8"))
        if anchor not in target_anchors:
            return BrokenMarkdownLink(
                link=link,
                reason=f"anchor #{anchor} not found in {_rel(target, root)}",
            )
    return None


def format_broken_markdown_links(
    broken: list[BrokenMarkdownLink],
    repo_root: Path,
    *,
    limit: int = 40,
) -> str:
    root = repo_root.resolve()
    lines = [
        (
            f"{_rel(item.link.source, root)}:{item.link.line} "
            f"{item.link.url!r} — {item.reason}"
        )
        for item in broken[:limit]
    ]
    if len(broken) > limit:
        lines.append(f"... and {len(broken) - limit} more")
    return f"{len(broken)} broken markdown link(s):\n" + "\n".join(lines)


def find_broken_markdown_links(repo_root: Path) -> list[BrokenMarkdownLink]:
    broken: list[BrokenMarkdownLink] = []
    for md_path in repo_markdown_files(repo_root):
        for link in extract_markdown_links(md_path.read_text(encoding="utf-8"), md_path):
            if issue := validate_markdown_link(link, repo_root=repo_root):
                broken.append(issue)
    return broken


def check_markdown_links(repo_root: Path) -> int:
    """Validate documentation links; return the number of markdown files checked."""
    root = repo_root.resolve()
    broken = find_broken_markdown_links(root)
    if broken:
        raise MarkdownLinksError(format_broken_markdown_links(broken, root))
    return len(repo_markdown_files(root))
