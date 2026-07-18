"""Build a full SYSTEM dump byte map from series analyses + corpus scan."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..frame import (
    BRICASTI_MFR_ID,
    CHECKSUM_NIBBLE_COUNT,
    SYSTEM_CHECKSUM_COVER_END,
    SYSTEM_DUMP_HEADER,
    SYSTEM_MESSAGE_LENGTH,
    SYSTEM_PAYLOAD_OFFSET,
)
from ..prog.byte_map import pick_series_example
from .corpus_layout import claim_corpus_layout, overview_label_for_offsets


def build_system_byte_map(
    results: list[dict[str, Any]],
    *,
    sysex_root: Path | None = None,
) -> dict[str, Any]:
    """Annotate every byte in the 77-byte system dump layout."""
    if not results:
        raise ValueError("no system analysis results for byte map")

    length = int(results[0]["message_length"])
    for result in results[1:]:
        if int(result["message_length"]) != length:
            raise ValueError("system series have different SysEx lengths")

    if sysex_root is None and results:
        sysex_root = Path(results[0]["folder"]).parent.parent

    annotations: list[dict[str, Any]] = [
        {
            "offset": i,
            "hex": None,
            "hex_source": None,
            "status": "unknown",
            "role": "unknown system payload nibble",
            "parameters": [],
        }
        for i in range(length)
    ]

    def claim(
        offsets: list[int],
        *,
        status: str,
        role: str,
        parameter: str | None = None,
        confidence: str | None = None,
        encoding: str | None = None,
        example: bytes | None = None,
        example_source: str | None = None,
    ) -> None:
        for off in offsets:
            if off < 0 or off >= length:
                continue
            cell = annotations[off]
            if parameter == "_corpus":
                existing = [
                    p for p in (cell.get("parameters") or []) if p != "_corpus"
                ]
                if existing:
                    continue
            rank = {"known": 3, "frame": 3, "checksum": 2, "secondary": 1, "unknown": 0}
            if rank.get(status, 0) < rank.get(cell["status"], 0):
                if parameter and parameter not in cell["parameters"]:
                    cell["parameters"].append(parameter)
                continue
            cell["status"] = status
            cell["role"] = role
            if confidence:
                cell["confidence"] = confidence
            if encoding:
                cell["encoding"] = encoding
            if parameter and parameter not in cell["parameters"]:
                cell["parameters"].append(parameter)
            if example is not None and 0 <= off < len(example):
                cell["hex"] = f"{example[off]:02X}"
                cell["hex_source"] = example_source

    frame_example = None
    frame_example_path = None
    for result in results:
        folder = Path(result["folder"])
        path = pick_series_example(folder)
        if path is not None:
            raw = path.read_bytes()
            if len(raw) == length:
                frame_example = raw
                frame_example_path = path
                break

    claim([0], status="frame", role="SysEx start (F0)")
    annotations[0]["hex"] = "F0"
    annotations[0]["hex_source"] = "frame constant"

    for i, b in enumerate(BRICASTI_MFR_ID, start=1):
        claim([i], status="frame", role=f"Manufacturer ID ({BRICASTI_MFR_ID.hex(' ')})")
        annotations[i]["hex"] = f"{b:02X}"
        annotations[i]["hex_source"] = "frame constant"

    for i, b in enumerate(SYSTEM_DUMP_HEADER, start=4):
        claim(
            [i],
            status="frame",
            role=f"System-dump header ({SYSTEM_DUMP_HEADER.hex(' ')})",
        )
        annotations[i]["hex"] = f"{b:02X}"
        annotations[i]["hex_source"] = "frame constant"

    checksum_start = length - 1 - CHECKSUM_NIBBLE_COUNT
    claim(
        list(range(checksum_start, length - 1)),
        status="checksum",
        role=(
            "Checksum: CRC-16/ARC over offsets 8-71, "
            "packed as four high-nibble-first SysEx bytes"
        ),
    )
    claim([length - 1], status="frame", role="SysEx end (F7)")
    annotations[length - 1]["hex"] = "F7"
    annotations[length - 1]["hex_source"] = "frame constant"

    for result in results:
        name = result["parameter"]
        folder = Path(result["folder"])
        series_path = pick_series_example(folder)
        series_bytes = series_path.read_bytes() if series_path else None
        if series_bytes is not None and len(series_bytes) != length:
            series_bytes = None
            series_path = None

        hyp = result.get("hypothesis") or {}
        confidence = hyp.get("confidence")
        best = result.get("best_encoding")
        if best and best.get("offsets"):
            enc = best.get("encoding")
            role = f"Parameter `{name}` (from sysex/system/{name}/)"
            if enc:
                role += f" ({enc})"
            claim(
                list(best["offsets"]),
                status="known",
                role=role,
                parameter=name,
                confidence=confidence,
                encoding=enc,
                example=series_bytes,
                example_source=str(series_path) if series_path else None,
            )
        for off in result.get("classification", {}).get("secondary_offsets") or []:
            claim(
                [off],
                status="secondary",
                role=f"Secondary field in system series `{name}`",
                parameter=name,
                confidence=confidence,
            )

    coupling: dict[int, list[str]] = {}
    for result in results:
        name = result["parameter"]
        for off in result.get("classification", {}).get("secondary_offsets") or []:
            coupling.setdefault(off, []).append(name)
    for off, names in sorted(coupling.items()):
        cell = annotations[off]
        if cell["status"] in {"known", "secondary"} and names:
            extra = ", ".join(f"`{n}`" for n in sorted(names))
            cell["role"] += f" (also secondary in: {extra})"

    corpus_claims = claim_corpus_layout(
        claim,
        length=length,
        sysex_root=sysex_root,
        example=frame_example,
        example_source=str(frame_example_path) if frame_example_path else None,
    )

    # Fill any remaining payload gaps as unknown regions (contiguous coverage).
    for off in range(SYSTEM_PAYLOAD_OFFSET, checksum_start):
        if annotations[off]["status"] == "unknown":
            annotations[off]["role"] = (
                "Unknown system payload nibble (no series claim in this corpus)"
            )
            if frame_example is not None:
                annotations[off]["hex"] = f"{frame_example[off]:02X}"
                annotations[off]["hex_source"] = str(frame_example_path)

    regions = _collapse_regions(annotations)
    known = sum(1 for a in annotations if a["status"] in {"frame", "known", "checksum"})
    secondary = sum(1 for a in annotations if a["status"] == "secondary")
    unknown = sum(1 for a in annotations if a["status"] == "unknown")

    return {
        "kind": "system",
        "message_length": length,
        "independence_note": (
            "Each sysex/system/<series>/ folder is an independent capture stream. "
            "Reserved/meta roles come from a corpus scan of all system dumps."
        ),
        "counts": {
            "known_or_frame": known,
            "secondary": secondary,
            "unknown": unknown,
            "total": length,
        },
        "bytes": annotations,
        "regions": regions,
        "corpus_layout_claims": [
            {
                "offsets": c["offsets"],
                "status": c["status"],
                "label": c.get("label"),
                "confidence": c.get("confidence"),
            }
            for c in corpus_claims
        ],
    }


def render_system_byte_map_markdown(byte_map: dict[str, Any]) -> str:
    """Markdown byte-map page for system dumps."""
    counts = byte_map["counts"]
    lines: list[str] = [
        "## System byte map",
        "",
        f"Every offset in the {byte_map['message_length']}-byte system-dump layout.",
        "",
        "Short consolidated view: [byte-map-overview.md](byte-map-overview.md).",
        "",
        "Codegen layout: [m7_system_dump.ksy](m7_system_dump.ksy) · "
        "[m7_system_dump.spec.json](m7_system_dump.spec.json).",
        "",
        byte_map.get("independence_note") or "",
        "",
        f"Coverage: **{counts['known_or_frame']}** known/frame/checksum, "
        f"**{counts['secondary']}** secondary, "
        f"**{counts['unknown']}** unknown "
        f"(of {counts['total']}).",
        "",
        "### Regions",
        "",
        "| Offsets | Len | Example hex | Status | Meaning |",
        "|---------|-----|-------------|--------|---------|",
    ]
    series_params = _series_parameter_names(byte_map)
    for region in byte_map["regions"]:
        example = region.get("example_hex") or "-"
        if example != "-":
            example = f"`{example}`"
        meaning = _linkify_meaning(region["role"], series_params)
        lines.append(
            f"| {region['offsets']} | {region['length']} | "
            f"{example} | {region['status']} | {meaning} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_system_byte_map_overview_markdown(byte_map: dict[str, Any]) -> str:
    """Short consolidated system layout (no per-byte table)."""
    counts = byte_map["counts"]
    length = byte_map["message_length"]
    regions = byte_map.get("regions") or []
    series_params = _series_parameter_names(byte_map)

    lines: list[str] = [
        "## Byte map overview",
        "",
        f"**{length}**-byte system dump. "
        f"Known/frame/checksum **{counts['known_or_frame']}** · "
        f"secondary **{counts['secondary']}** · "
        f"unknown **{counts['unknown']}**.",
        "",
        "Full regions table: [byte-map.md](byte-map.md).",
        "",
        "Codegen layout: [m7_system_dump.ksy](m7_system_dump.ksy) "
        "([Kaitai Struct](https://kaitai.io/)) · "
        "[m7_system_dump.spec.json](m7_system_dump.spec.json).",
        "",
        "Reserved/meta roles (fixed prefix, padding) come from a corpus scan "
        "of all system `.syx` dumps — medium confidence.",
        "",
        "### Layout",
        "",
        "| Offsets | Len | Status | Field |",
        "|---------|----:|--------|-------|",
    ]

    for region in regions:
        label, encoding = _overview_label(region, byte_map)
        status = region["status"]
        if status == "unknown":
            status = "UNKNOWN"
            field = "UNKNOWN"
        else:
            linked = _link_field_label(label, series_params)
            field = linked
            if encoding:
                field = f"{linked} (`{encoding}`)"
        lines.append(
            f"| {region['offsets']} | {region['length']} | "
            f"{status} | {field} |"
        )

    param_rows = _overview_parameter_rows(byte_map)
    if param_rows:
        lines.extend(
            [
                "",
                "### Settings (by offset)",
                "",
                "| Offsets | Setting | Encoding | Source |",
                "|---------|---------|----------|--------|",
            ]
        )
        for row in param_rows:
            param = _link_field_label(row["parameter"], series_params)
            lines.append(
                f"| {row['offsets']} | {param} | "
                f"`{row['encoding']}` | {row['source']} |"
            )

    unknown = [r for r in regions if r.get("status") == "unknown"]
    secondary = [r for r in regions if r.get("status") == "secondary"]
    if unknown:
        total = sum(int(r["length"]) for r in unknown)
        lines.extend(
            [
                "",
                "### Unknown",
                "",
                f"**{total}** bytes still unmapped "
                f"({len(unknown)} region{'s' if len(unknown) != 1 else ''}):",
                "",
                "| Offsets | Len |",
                "|---------|----:|",
            ]
        )
        for r in unknown:
            lines.append(f"| {r['offsets']} | {r['length']} |")
        lines.append("")
    if secondary:
        offs = ", ".join(f"`{r['offsets']}`" for r in secondary)
        lines.extend(
            [
                "",
                "### Secondary",
                "",
                f"Bytes that also move in other capture series: {offs}",
                "",
            ]
        )

    coupled = _coupled_offset_notes(byte_map)
    if coupled:
        lines.extend(["", "### Coupled offsets", ""] + coupled + [""])

    return "\n".join(lines)


def _series_parameter_names(byte_map: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for cell in byte_map.get("bytes") or []:
        for p in cell.get("parameters") or []:
            if p not in {"_corpus"}:
                names.add(p)
    for region in byte_map.get("regions") or []:
        for p in region.get("parameters") or []:
            if p not in {"_corpus"}:
                names.add(p)
    return names


def _parameter_page_href(name: str) -> str:
    from ..export.nav import parameter_slug

    return f"bytes/{parameter_slug(name)}.md"


def _link_parameter_name(name: str) -> str:
    return f"[{name}]({_parameter_page_href(name)})"


def _link_field_label(label: str, series_params: set[str]) -> str:
    if label in series_params:
        return _link_parameter_name(label)
    return label


def _linkify_meaning(text: str, series_params: set[str]) -> str:
    import re

    ordered = sorted(series_params, key=len, reverse=True)

    def repl_param_tick(match: re.Match[str]) -> str:
        name = match.group(1)
        if name in series_params:
            return f"Parameter {_link_parameter_name(name)}"
        return match.group(0)

    text = re.sub(r"Parameter `([^`]+)`", repl_param_tick, text)

    for name in ordered:
        path = f"sysex/system/{name}/"
        if path in text:
            text = text.replace(path, f"[sysex/system/{name}/]({_parameter_page_href(name)})")

    marker = "also secondary in: "
    if marker in text:
        head, tail = text.split(marker, 1)
        closing = ""
        body = tail
        if body.endswith(")"):
            body, closing = body[:-1], ")"
        parts = [p.strip().strip("`") for p in body.split(",")]
        linked = []
        for part in parts:
            if part in series_params:
                linked.append(_link_parameter_name(part))
            else:
                linked.append(part)
        text = head + marker + ", ".join(linked) + closing

    return text


def _overview_parameter_rows(byte_map: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for region in byte_map.get("regions") or []:
        if region.get("status") != "known":
            continue
        label, encoding = _overview_label(region, byte_map)
        if label in {"unknown", "UNKNOWN"}:
            continue
        if label.startswith("reserved") or label.startswith("fixed"):
            continue
        params = [p for p in (region.get("parameters") or []) if p != "_corpus"]
        if not params:
            continue
        primary = _primary_parameter_for_region(region) or params[0]
        rows.append(
            {
                "offsets": region["offsets"],
                "parameter": primary,
                "encoding": encoding or "?",
                "source": "series",
            }
        )
    return rows


def _coupled_offset_notes(byte_map: dict[str, Any]) -> list[str]:
    """Human notes for bytes claimed by one series but secondary in another."""
    notes: list[str] = []
    for cell in byte_map.get("bytes") or []:
        if cell.get("status") != "known":
            continue
        role = cell.get("role") or ""
        marker = "also secondary in: "
        if marker not in role:
            continue
        primary = _primary_parameter_from_role(role)
        if not primary:
            continue
        tail = role.split(marker, 1)[1].rstrip(")")
        others = [p.strip().strip("`") for p in tail.split(",")]
        for other in others:
            if other and other != primary:
                notes.append(
                    f"- Offset **{cell['offset']}** "
                    f"([{primary}]({_parameter_page_href(primary)})) also moves "
                    f"when capturing [{other}]({_parameter_page_href(other)})."
                )
    return notes


def _primary_parameter_from_role(role: str) -> str | None:
    import re

    match = re.search(r"Parameter `([^`]+)`", role)
    return match.group(1) if match else None


def _primary_parameter_for_region(region: dict[str, Any]) -> str | None:
    params = [p for p in (region.get("parameters") or []) if p != "_corpus"]
    if not params:
        return None
    role = region.get("role") or ""
    named = _primary_parameter_from_role(role)
    if named in params:
        return named
    return params[-1]


def _overview_label(region: dict[str, Any], byte_map: dict[str, Any]) -> tuple[str, str | None]:
    status = region.get("status")
    role = region.get("role") or ""
    params = [
        p for p in (region.get("parameters") or []) if p not in {"_corpus"}
    ]
    encoding = _region_encoding(region, byte_map)
    start = region.get("start")
    end = region.get("end")

    if (
        "_corpus" in (region.get("parameters") or [])
        and start is not None
        and end is not None
        and status in {"known", "secondary"}
        and not params
    ):
        corpus_label = overview_label_for_offsets(list(range(int(start), int(end) + 1)))
        if corpus_label:
            return corpus_label, encoding

    if status == "frame":
        lowered = role.lower()
        if "start" in lowered:
            return "SysEx start (F0)", None
        if "manufacturer" in lowered:
            return "manufacturer ID", None
        if "header" in lowered:
            return "system-dump header", None
        if "end" in lowered:
            return "SysEx end (F7)", None
        return "frame", None
    if status == "checksum":
        return "checksum (CRC-16/ARC)", encoding
    if status == "secondary":
        return "secondary", encoding
    if status == "unknown":
        return "UNKNOWN", None
    if params:
        return _primary_parameter_for_region(region) or params[0], encoding
    return role.split("(")[0].strip() or "known", encoding


def _region_encoding(region: dict[str, Any], byte_map: dict[str, Any]) -> str | None:
    start = region.get("start")
    if start is None:
        return None
    bytes_ = byte_map.get("bytes") or []
    if 0 <= start < len(bytes_):
        return bytes_[start].get("encoding")
    return None


def _collapse_regions(annotations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not annotations:
        return []

    def key(cell: dict[str, Any]) -> tuple:
        return (cell["status"], cell["role"], tuple(cell.get("parameters") or []))

    regions: list[dict[str, Any]] = []
    start = 0
    prev = key(annotations[0])
    for i in range(1, len(annotations) + 1):
        cur = key(annotations[i]) if i < len(annotations) else None
        if cur == prev:
            continue
        chunk = annotations[start:i]
        first = chunk[0]
        last_off = chunk[-1]["offset"]
        first_off = chunk[0]["offset"]
        offsets = (
            str(first_off) if first_off == last_off else f"{first_off}-{last_off}"
        )
        hexes = [c["hex"] for c in chunk if c.get("hex")]
        if hexes and len(hexes) == len(chunk):
            example = " ".join(hexes[:8])
            if len(hexes) > 8:
                example += " ..."
        elif hexes:
            example = " ".join(hexes[:8]) + (" ..." if len(chunk) > 8 else "")
        else:
            example = None
        regions.append(
            {
                "start": first_off,
                "end": last_off,
                "offsets": offsets,
                "length": len(chunk),
                "example_hex": example,
                "status": first["status"],
                "role": first["role"],
                "parameters": list(first.get("parameters") or []),
            }
        )
        if i < len(annotations):
            start = i
            prev = cur
    return regions
