"""Build a full SysEx byte map from frame knowledge + independent parameter analyses.

Each sysex/prog/parameters/<parameter>/ folder is an independent capture
stream (only that parameter intentionally varied). Analyses are never
cross-compared at the dump-byte level - we only merge per-folder conclusions
into a layout map.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..frame import (
    BRICASTI_MFR_ID,
    CHECKSUM_NIBBLE_COUNT,
    DATA_OFFSET,
    NAME_OFFSET,
    PROGRAM_DUMP_HEADER,
    PROGRAM_NAME_EDITABLE_LENGTH,
    PROGRAM_NAME_LENGTH,
    REGISTER_BASIS_BLOB_LENGTH,
    REGISTER_BASIS_BLOB_OFFSET,
)


def pick_series_example(folder: Path) -> Path | None:
    """Pick one dump from a single parameter folder (prefer low.syx)."""
    folder = Path(folder)
    for name in ("low.syx", "LOW.SYX", "off.syx", "OFF.SYX"):
        candidate = folder / name
        if candidate.is_file():
            return candidate
    dumps = sorted(folder.glob("*.syx")) + sorted(folder.glob("*.SYX"))
    seen: set[str] = set()
    for path in dumps:
        key = str(path).lower()
        if key in seen:
            continue
        seen.add(key)
        return path
    return None


def build_byte_map(
    results: list[dict[str, Any]],
    names: dict[str, Any] | None = None,
    *,
    sysex_root: Path | None = None,
) -> dict[str, Any]:
    """
    Annotate every byte offset using the fixed frame plus each folder's own findings.

    Example hex for a known parameter comes only from that parameter's folder.
    Unknown payload bytes have no cross-series example hex (folders are independent).

    Optional ``names`` is the ``_presets`` preset-identity analysis (bank / program /
    name confirmation) and claims those identity offsets.

    Optional ``sysex_root`` enables corpus-wide constant checks when applying
    reserved/meta layout claims from ``corpus_layout``.
    """
    if not results and not names:
        raise ValueError("no analysis results for byte map")

    length_source = results[0] if results else names
    length = int(length_source["message_length"])
    for result in results[1:]:
        if int(result["message_length"]) != length:
            raise ValueError(
                "parameter folders have different SysEx lengths; "
                "cannot merge independent layouts"
            )
    if names and int(names["message_length"]) != length and results:
        raise ValueError("_presets dumps have a different SysEx length")
    if names and not results:
        length = int(names["message_length"])

    if sysex_root is None:
        if names and names.get("folder"):
            sysex_root = Path(names["folder"]).parent
        elif results:
            sysex_root = Path(results[0]["folder"]).parent

    annotations: list[dict[str, Any]] = [
        {
            "offset": i,
            "hex": None,
            "hex_source": None,
            "status": "unknown",
            "role": "unknown payload nibble (no cross-folder dump comparison)",
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
            rank = {"known": 3, "frame": 3, "checksum": 2, "secondary": 1, "unknown": 0}
            if rank.get(status, 0) < rank.get(cell["status"], 0):
                if parameter and parameter not in cell["parameters"]:
                    cell["parameters"].append(parameter)
                continue
            if status == "secondary" and cell["status"] == "known":
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
                # Only attach hex from the owning series (or frame template dump).
                cell["hex"] = f"{example[off]:02X}"
                cell["hex_source"] = example_source

    # Frame illustration: use constants where fixed; one folder dump only for name ASCII.
    frame_example_path = None
    frame_example = None
    search_folders = [Path(r["folder"]) for r in results]
    if names:
        search_folders.insert(0, Path(names["folder"]))
    for folder in search_folders:
        path = pick_series_example(folder)
        if path is not None:
            frame_example_path = path
            frame_example = path.read_bytes()
            if len(frame_example) != length:
                frame_example = None
                frame_example_path = None
                continue
            break

    claim([0], status="frame", role="SysEx start (F0)")
    annotations[0]["hex"] = "F0"
    annotations[0]["hex_source"] = "frame constant"

    for i, b in enumerate(BRICASTI_MFR_ID, start=1):
        claim([i], status="frame", role=f"Manufacturer ID ({BRICASTI_MFR_ID.hex(' ')})")
        annotations[i]["hex"] = f"{b:02X}"
        annotations[i]["hex_source"] = "frame constant"

    for i, b in enumerate(PROGRAM_DUMP_HEADER, start=4):
        claim(
            [i],
            status="frame",
            role=f"Program-dump header ({PROGRAM_DUMP_HEADER.hex(' ')})",
        )
        annotations[i]["hex"] = f"{b:02X}"
        annotations[i]["hex_source"] = "frame constant"

    name_role = (
        "Program name (ASCII, 14-character editable label per manual; "
        "space-padded within this field)"
    )
    if names and (names.get("fields") or {}).get("program_name", {}).get(
        "matches_filename_preset"
    ):
        name_role += (
            " - confirmed against sysex/prog/presets/ filename preset "
            "(bank name is not stored here)"
        )
    claim(
        list(range(NAME_OFFSET, NAME_OFFSET + PROGRAM_NAME_EDITABLE_LENGTH)),
        status="frame",
        role=name_role,
        example=frame_example,
        example_source=str(frame_example_path) if frame_example_path else None,
    )
    claim(
        list(
            range(
                NAME_OFFSET + PROGRAM_NAME_EDITABLE_LENGTH,
                NAME_OFFSET + PROGRAM_NAME_LENGTH,
            )
        ),
        status="frame",
        role=(
            "Program name trailing pad (always `0x20` in this corpus; "
            f"offsets {NAME_OFFSET + PROGRAM_NAME_EDITABLE_LENGTH}–"
            f"{NAME_OFFSET + PROGRAM_NAME_LENGTH - 1} complete the "
            f"{PROGRAM_NAME_LENGTH}-byte wire name window)"
        ),
        example=frame_example,
        example_source=str(frame_example_path) if frame_example_path else None,
    )
    if frame_example is not None:
        for i in range(NAME_OFFSET, NAME_OFFSET + PROGRAM_NAME_LENGTH):
            b = frame_example[i]
            annotations[i]["ascii"] = chr(b) if 32 <= b < 127 else None

    claim(
        list(
            range(
                REGISTER_BASIS_BLOB_OFFSET,
                REGISTER_BASIS_BLOB_OFFSET + REGISTER_BASIS_BLOB_LENGTH,
            )
        ),
        status="frame",
        role=(
            "Register basis blob: factory dumps space-pad with `0x20`; "
            "Reg-backed hold-EDIT dumps store a bit-packed snapshot of the "
            "**stored register** (low nibbles as a 256-bit stream: 14-char "
            "6-bit name, store-generation counter, all 18 parameters incl. "
            "the V2 delay block) — fully decoded in "
            "bytes/register-basis-blob.md (see `sysex/prog/edit/registers/`)"
        ),
        example=frame_example,
        example_source=str(frame_example_path) if frame_example_path else None,
    )

    checksum_start = length - 1 - CHECKSUM_NIBBLE_COUNT
    claim(
        list(range(checksum_start, length - 1)),
        status="checksum",
        role=(
            "Checksum: CRC-16/ARC over offsets 8-151 (name + payload), "
            "packed as four high-nibble-first SysEx bytes (per-dump; "
            "recompute after edits - do not copy across parameter series)"
        ),
    )
    claim([length - 1], status="frame", role="SysEx end (F7)")
    annotations[length - 1]["hex"] = "F7"
    annotations[length - 1]["hex_source"] = "frame constant"

    if names:
        _claim_names_identity(claim, names, length)
        _claim_preset_sheet(claim, names, length)

    # Each parameter folder contributes only its own conclusions + its own example bytes.
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
            notes = (best.get("notes") or "").split(";", 1)[0].strip()
            role = (
                f"Parameter `{name}` (from independent series "
                f"sysex/prog/parameters/{name}/)"
            )
            if enc:
                role += f" ({enc}"
                if notes:
                    role += f", {notes}"
                role += ")"
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
                role=(
                    "Secondary field that also moved in this parameter's "
                    "independent series (edit/UI/state - not cross-checked "
                    "against other folders)"
                ),
                parameter=name,
                confidence=confidence,
                # Do not attach hex from this series onto a shared map cell that
                # multiple series may report - keep secondary hex empty.
            )

    corpus_claims: list[dict[str, Any]] = []
    from .corpus_layout import claim_corpus_layout

    example = None
    example_source = None
    if names:
        folder = Path(names["folder"])
        example_path = pick_series_example(folder)
        if example_path is not None:
            example = example_path.read_bytes()
            example_source = str(example_path)
            if len(example) != length:
                example = None
                example_source = None
    corpus_claims = claim_corpus_layout(
        claim,
        length=length,
        sysex_root=sysex_root,
        example=example,
        example_source=example_source,
    )
    _normalize_display_region(annotations, sysex_root=sysex_root)

    regions = _collapse_regions(annotations)
    known = sum(1 for a in annotations if a["status"] in {"frame", "known", "checksum"})
    secondary = sum(1 for a in annotations if a["status"] == "secondary")
    unknown = sum(1 for a in annotations if a["status"] == "unknown")

    return {
        "message_length": length,
        "independence_note": (
            "Each sysex/prog/parameters/<parameter>/ folder is an independent "
            "dump stream. Byte values are never compared across folders; only "
            "per-folder conclusions are merged into this layout map. "
            "sysex/prog/presets/ is a separate preset-identity series "
            "(bank/program/name). Additional reserved/meta roles come from a "
            "corpus scan of all dumps."
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
        "names": {
            "present": bool(names),
            "confidence": (names or {}).get("hypothesis", {}).get("confidence"),
            "bank_map": ((names or {}).get("fields") or {})
            .get("bank_index", {})
            .get("map"),
        }
        if names
        else {"present": False},
    }


def _claim_names_identity(claim, names: dict[str, Any], length: int) -> None:
    """Claim bank / program identity offsets from the _presets analysis."""
    folder = Path(names["folder"])
    example_path = pick_series_example(folder)
    example = example_path.read_bytes() if example_path else None
    if example is not None and len(example) != length:
        example = None
        example_path = None

    fields = names.get("fields") or {}
    conf = (names.get("hypothesis") or {}).get("confidence")
    bank = fields.get("bank_index") or {}
    program = fields.get("program_slot") or {}

    bank_map = bank.get("map") or {}
    from .names import EDIT_DUMP_BANK_INDEX, format_bank_map_by_index

    bank_summary = format_bank_map_by_index(bank_map)
    claim(
        list(bank.get("offsets") or [88, 89]),
        status="known",
        role=(
            "Bank index (`nibble_hilo`) from sysex/prog/presets/ "
            f"[{bank_summary}]"
            + (
                f"; mirrored at offset {bank.get('mirror_offset', 137)}"
                if bank.get("mirror_matches")
                else ""
            )
            + (
                f"; hold EDIT sends use index {EDIT_DUMP_BANK_INDEX} here "
                "while mirror 137 keeps the source bank "
                "(see sysex/prog/edit/)"
            )
        ),
        parameter="_presets",
        confidence=conf,
        encoding=bank.get("encoding") or "nibble_hilo",
        example=example,
        example_source=str(example_path) if example_path else None,
    )
    claim(
        list(program.get("offsets") or [90, 91]),
        status="known",
        role=(
            "Program slot within bank (`nibble_hilo`) from sysex/prog/presets/ "
            "(not a global program number)"
        ),
        parameter="_presets",
        confidence=conf,
        encoding=program.get("encoding") or "nibble_hilo",
        example=example,
        example_source=str(example_path) if example_path else None,
    )
    if bank.get("mirror_offset") is not None and bank.get("mirror_matches"):
        claim(
            [int(bank["mirror_offset"])],
            status="known",
            role=(
                f"Bank index mirror (equals offset {bank['offsets'][1]}) "
                "from sysex/prog/presets/; on hold-EDIT dumps this stays the "
                "source bank while 88-89 are Edit index 11"
            ),
            parameter="_presets",
            confidence=conf,
            encoding="raw_u8",
            example=example,
            example_source=str(example_path) if example_path else None,
        )


def _claim_preset_sheet(claim, names: dict[str, Any], length: int) -> None:
    """Claim sound-parameter offsets located from presets × published sheet."""
    folder = Path(names["folder"])
    example_path = pick_series_example(folder)
    example = example_path.read_bytes() if example_path else None
    if example is not None and len(example) != length:
        example = None
        example_path = None

    for dec in names.get("parameter_decoders") or []:
        if dec.get("source") != "preset_sheet":
            continue
        offsets = list(dec.get("offsets") or [])
        if not offsets:
            continue
        name = dec["parameter"]
        enc = dec.get("encoding")
        kind = dec.get("kind")
        role = (
            f"Parameter `{name}` (from sysex/prog/presets/ × preset sheet"
        )
        if enc and kind:
            role += f"; {enc}, {kind}"
        elif enc:
            role += f"; {enc}"
        role += " — confirm with a dedicated capture series)"
        claim(
            offsets,
            status="known",
            role=role,
            parameter=name,
            confidence=dec.get("confidence") or "medium",
            encoding=enc,
            example=example,
            example_source=str(example_path) if example_path else None,
        )


def _series_parameter_names(byte_map: dict[str, Any]) -> set[str]:
    """Capture-series parameter names claimed on any byte (excludes meta tags)."""
    names: set[str] = set()
    for cell in byte_map.get("bytes") or []:
        for p in cell.get("parameters") or []:
            if p not in {"_presets", "_corpus", "_menus"}:
                names.add(p)
    for region in byte_map.get("regions") or []:
        for p in region.get("parameters") or []:
            if p not in {"_presets", "_corpus", "_menus"}:
                names.add(p)
    return names


_IDENTITY_FIELD_HREFS = {
    "bank index": "bytes/bank-index.md",
    "bank index mirror": "bytes/bank-index.md",
    "program slot": "bytes/program-slot.md",
    "program name": "bytes/program-name.md",
    "program name (ASCII)": "bytes/program-name.md",
    "program name pad": "bytes/program-name-pad.md",
    "register bank": "bytes/register-bank.md",
    "register": "bytes/register.md",
    "register basis blob": "bytes/register-basis-blob.md",
    "favorite slot (8 = none)": "bytes/favorite-slot.md",
    "panel mode flag": "bytes/panel-mode-flag.md",
    "selected menu index": "bytes/selected-menu-index.md",
    "algorithm/family flag": "bytes/algorithm-family-flag.md",
    "family-flag mirror": "bytes/algorithm-family-flag.md",
    "engine/bank-class flag": "bytes/engine-bank-class-flag.md",
    "display": "bytes/display.md",
}


def _parameter_page_href(name: str) -> str:
    from ..export import parameter_slug

    return f"bytes/{parameter_slug(name)}.md"


def _link_parameter_name(name: str, *, backticks: bool = False) -> str:
    href = _parameter_page_href(name)
    if backticks:
        return f"[`{name}`]({href})"
    return f"[{name}]({href})"


def _link_field_label(label: str, series_params: set[str]) -> str:
    """Link overview Field/Parameter cells to a page when one exists."""
    if label in series_params:
        return _link_parameter_name(label)
    href = _IDENTITY_FIELD_HREFS.get(label)
    if href:
        return f"[{label}]({href})"
    return label


def _link_source_cell(source: str) -> str:
    if source == "_presets":
        return "[_presets](program-identity.md)"
    if source == "_menus":
        return "[_menus](bytes/display.md)"
    if source == "preset×sheet":
        return "[preset×sheet](preset-sheet.md)"
    return source


def _linkify_meaning(text: str, series_params: set[str]) -> str:
    """Add markdown links for parameter names and identity paths in Meaning cells."""
    import re

    # Longest names first so "hf rt multiply" wins over shorter prefixes.
    ordered = sorted(series_params, key=len, reverse=True)

    def repl_param_tick(match: re.Match[str]) -> str:
        name = match.group(1)
        if name in series_params:
            return f"Parameter {_link_parameter_name(name, backticks=True)}"
        return match.group(0)

    text = re.sub(r"Parameter `([^`]+)`", repl_param_tick, text)

    for name in ordered:
        path = f"sysex/prog/parameters/{name}/"
        if path in text:
            text = text.replace(
                path, f"[{path}]({_parameter_page_href(name)})"
            )

    if "sysex/prog/presets/" in text:
        text = text.replace(
            "sysex/prog/presets/",
            "[sysex/prog/presets/](program-identity.md)",
        )

    marker = "moved in independent series: "
    if marker in text:
        head, tail = text.split(marker, 1)
        # Strip trailing ")" that closes the parenthetical, if present.
        closing = ""
        body = tail
        if body.endswith(")"):
            body, closing = body[:-1], ")"
        parts = [p.strip() for p in body.split(",")]
        linked = []
        for part in parts:
            if part in series_params:
                linked.append(_link_parameter_name(part))
            else:
                linked.append(part)
        text = head + marker + ", ".join(linked) + closing

    # Bank index legend: Halls=0, Plates=1, … (longest names first).
    # Linked form is [Halls](…)=0, so Bank=digit only matches the plain legend.
    from ..export import bank_md_link

    for bank in (
        "Halls 2",
        "Plates 2",
        "Rooms 2",
        "Spaces 2",
        "Halls",
        "Plates",
        "Rooms",
        "Chambers",
        "Ambience",
        "Spaces",
        "NonLin",
    ):
        text = re.sub(
            rf"{re.escape(bank)}(=\d+)",
            lambda m, b=bank: f"{bank_md_link(b)}{m.group(1)}",
            text,
        )

    # Legend was wrapped as [Halls=0, …]; linking names yields [[Halls](…)=0, …];
    # drop the outer list brackets so markdown links render cleanly.
    text = re.sub(r"\[(\[[^\]]+\]\(presets/[^)]+\)=\d+)", r"\1", text)
    text = re.sub(r"(\]\([^)]+\)=\d+)\];", r"\1;", text)

    return text


def render_byte_map_markdown(byte_map: dict[str, Any]) -> str:
    """Markdown region summary for the full program-dump layout."""
    counts = byte_map["counts"]
    series_params = _series_parameter_names(byte_map)
    lines: list[str] = [
        "## Full byte map",
        "",
        f"Every offset in the {byte_map['message_length']}-byte program-dump layout.",
        "",
        "Short consolidated view: [byte-map-overview.md](byte-map-overview.md).",
        "",
        "Codegen layout: [m7_program_dump.ksy](m7_program_dump.ksy) "
        "([Kaitai Struct](https://kaitai.io/)) · "
        "[m7_program_dump.spec.json](m7_program_dump.spec.json).",
        "",
        byte_map.get("independence_note")
        or "Parameter folders are analyzed independently.",
        "",
        f"Coverage: **{counts['known_or_frame']}** known/frame/checksum, "
        f"**{counts['secondary']}** secondary, "
        f"**{counts['unknown']}** unknown "
        f"(of {counts['total']}).",
        "",
        "Example hex for a known parameter comes only from that parameter’s own "
        "folder. Unknown payload bytes show `-` (no shared cross-folder snapshot).",
        "",
        "### Regions",
        "",
        "| Offsets | Len | Example hex | Status | Meaning |",
        "|---------|-----|-------------|--------|---------|",
    ]
    for region in byte_map["regions"]:
        example = region.get("example_hex") or "-"
        if example != "-":
            example = f"`{example}`"
        meaning = _linkify_meaning(region["role"], series_params)
        label, _encoding = _overview_label(region, byte_map)
        href = _IDENTITY_FIELD_HREFS.get(label)
        if href and f"]({href})" not in meaning:
            if href in meaning:
                # Role text mentions the page as plain text; make it a link.
                meaning = meaning.replace(href, f"[{href}]({href})")
            else:
                meaning += f" — see [{label}]({href})"
        lines.append(
            f"| {region['offsets']} | {region['length']} | "
            f"{example} | {region['status']} | {meaning} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_byte_map_overview_markdown(byte_map: dict[str, Any]) -> str:
    """Short consolidated layout: frame + parameters + gaps (no per-byte table)."""
    counts = byte_map["counts"]
    length = byte_map["message_length"]
    regions = byte_map.get("regions") or []
    series_params = _series_parameter_names(byte_map)

    lines: list[str] = [
        "## Byte map overview",
        "",
        f"**{length}**-byte program dump. "
        f"Known/frame/checksum **{counts['known_or_frame']}** · "
        f"secondary **{counts['secondary']}** · "
        f"unknown **{counts['unknown']}**.",
        "",
        "Full regions table: [byte-map.md](byte-map.md).",
        "",
        "Codegen layout: [m7_program_dump.ksy](m7_program_dump.ksy) "
        "([Kaitai Struct](https://kaitai.io/)) · "
        "[m7_program_dump.spec.json](m7_program_dump.spec.json).",
        "",
        "Reserved/meta roles (padding, family flag, display @ 146–147, engine/bank class) come "
        "from a corpus scan of all `.syx` dumps — medium confidence.",
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

    # Compact parameter index (sound + identity), sorted by first offset.
    param_rows = _overview_parameter_rows(byte_map)
    if param_rows:
        lines.extend(
            [
                "",
                "### Parameters (by offset)",
                "",
                "| Offsets | Parameter | Encoding | Source |",
                "|---------|-----------|----------|--------|",
            ]
        )
        for row in param_rows:
            param = _link_field_label(row["parameter"], series_params)
            source = _link_source_cell(row["source"])
            lines.append(
                f"| {row['offsets']} | {param} | "
                f"`{row['encoding']}` | {source} |"
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
                f"Edit/UI state (not a sound parameter): {offs}",
                "",
                "See [panel mode flag](bytes/panel-mode-flag.md), "
                "[selected menu index](bytes/selected-menu-index.md), "
                "[ui-state.md](ui-state.md), and "
                "[bytes/display.md](bytes/display.md) for menu captures.",
                "",
            ]
        )

    return "\n".join(lines)


def _overview_label(
    region: dict[str, Any],
    byte_map: dict[str, Any],
) -> tuple[str, str | None]:
    """Return (short field name, encoding) for the overview table."""
    from .corpus_layout import overview_label_for_offsets

    status = region.get("status")
    role = region.get("role") or ""
    params = [
        p
        for p in (region.get("parameters") or [])
        if p not in {"_presets", "_corpus", "_menus"}
    ]
    encoding = _region_encoding(region, byte_map)
    start = region.get("start")
    end = region.get("end")
    params_all = region.get("parameters") or []

    # Corpus short labels only when this region was claimed by corpus_layout.
    if (
        "_corpus" in params_all
        and start is not None
        and end is not None
        and status in {"known", "secondary"}
    ):
        corpus_label = overview_label_for_offsets(list(range(int(start), int(end) + 1)))
        if corpus_label and not params:
            return corpus_label, encoding

    if status == "frame":
        return _short_frame_label(role), None
    if status == "checksum":
        return "checksum (CRC-16/ARC)", encoding
    if status == "secondary":
        if role.lower().startswith("display"):
            return "display", encoding or "nibble_hilo"
        if "_corpus" in params_all and start is not None and end is not None:
            # Region may also list series that moved it as a secondary byte;
            # the corpus claim still owns the short label (e.g. offset 92).
            corpus_label = overview_label_for_offsets(
                list(range(int(start), int(end) + 1))
            )
            if corpus_label:
                return corpus_label, encoding
        return "secondary (edit/UI)", encoding
    if status == "unknown":
        return "UNKNOWN", None

    # known
    if params:
        return params[0], encoding
    params_all = region.get("parameters") or []
    if "_menus" in params_all:
        corpus_label = overview_label_for_offsets(
            list(range(int(start), int(end) + 1))
            if start is not None and end is not None
            else []
        )
        if corpus_label:
            return corpus_label, encoding
        if role.lower().startswith("display"):
            return "display", encoding or "nibble_hilo"
    if "_corpus" in params_all:
        corpus_label = overview_label_for_offsets(
            list(range(int(start), int(end) + 1))
            if start is not None and end is not None
            else []
        )
        if corpus_label:
            return corpus_label, encoding
        if "algorithm/family" in role.lower() or "family-flag" in role.lower():
            if "mirror" in role.lower():
                return "family-flag mirror", encoding
            return "algorithm/family flag", encoding
        if (
            "engine/bank-class" in role.lower()
            or "secondary-bank" in role.lower()
            or "bank-6 related" in role.lower()
        ):
            return "engine/bank-class flag", encoding
        if "* 2" in role.lower() and "flag" in role.lower():
            return "engine/bank-class flag", encoding
        if "reserved" in role.lower() and "padding" in role.lower():
            return "reserved padding", encoding
        if "reserved" in role.lower():
            return "reserved (always 0)", encoding
        if "favorite-source slot" in role.lower() or "favorite slot" in role.lower():
            return "favorite slot (8 = none)", encoding or "raw_u8"
        if "register bank" in role.lower() or role.lower().startswith("register page"):
            return "register bank", encoding or "raw_u8"
        if role.lower() == "register" or "register within bank" in role.lower() or "register slot" in role.lower():
            return "register", encoding or "raw_u8"
        if "fixed field" in role.lower() or "always `00 08`" in role:
            return "favorite slot (8 = none)", encoding
        if "fixed companion" in role.lower() or "always `02 00`" in role:
            return "fixed (always 02 00)", encoding
    lowered = role.lower()
    if "bank index mirror" in lowered:
        return "bank index mirror", encoding or "raw_u8"
    if "bank index" in lowered:
        return "bank index", encoding or "nibble_hilo"
    if "program slot" in lowered:
        return "program slot", encoding or "nibble_hilo"
    if "register basis" in lowered:
        return "register basis blob", encoding or "raw_bytes"
    if "trailing pad" in lowered or "name trailing" in lowered:
        return "program name pad", None
    if "program name" in lowered:
        return "program name", None
    return role.split("(")[0].strip() or "known", encoding


def _short_frame_label(role: str) -> str:
    lowered = role.lower()
    if "sysEx start" in role or "sysex start" in lowered:
        return "SysEx start (F0)"
    if "manufacturer" in lowered:
        return "manufacturer ID"
    if "header" in lowered:
        return "program-dump header"
    if "register basis" in lowered:
        return "register basis blob"
    if "trailing pad" in lowered or "name trailing" in lowered:
        return "program name pad"
    if "program name" in lowered or "space-padded" in lowered:
        return "program name (ASCII)"
    if "sysEx end" in role or "sysex end" in lowered:
        return "SysEx end (F7)"
    return role.split("(")[0].strip() or "frame"


def _region_encoding(
    region: dict[str, Any],
    byte_map: dict[str, Any],
) -> str | None:
    start = region.get("start")
    if start is None:
        return None
    bytes_ = byte_map.get("bytes") or []
    if 0 <= start < len(bytes_):
        return bytes_[start].get("encoding")
    return None


def _overview_parameter_rows(byte_map: dict[str, Any]) -> list[dict[str, str]]:
    """One row per claimed sound/identity field, ordered by offset."""
    rows: list[dict[str, str]] = []
    for region in byte_map.get("regions") or []:
        if region.get("status") != "known":
            continue
        label, encoding = _overview_label(region, byte_map)
        if label in {"unknown", "UNKNOWN", "secondary (edit/UI)"}:
            continue
        if label.startswith("reserved") or label.startswith("fixed"):
            continue
        role = (region.get("role") or "").lower()
        source = "series"
        if "preset sheet" in role:
            source = "preset×sheet"
        elif "_menus" in (region.get("parameters") or []) or label == "display":
            source = "_menus"
        elif "_corpus" in (region.get("parameters") or []) or label in {
            "algorithm/family flag",
            "family-flag mirror",
            "engine/bank-class flag",
            "secondary-bank (* 2) flag",
        }:
            source = "corpus"
        elif "_presets" in (region.get("parameters") or []) or label in {
            "bank index",
            "bank index mirror",
            "program slot",
        }:
            source = "_presets"
        # Skip pure reserved corpus padding from the parameter index.
        if source == "corpus" and label.startswith("reserved"):
            continue
        rows.append(
            {
                "offsets": region["offsets"],
                "parameter": label,
                "encoding": encoding or "?",
                "source": source,
            }
        )
    return rows


def _normalize_display_region(
    annotations: list[dict[str, Any]],
    *,
    sysex_root: Path | None = None,
) -> None:
    """Unify offsets 146-147 as one known `nibble_hilo` display field."""
    if len(annotations) <= 147:
        return
    from .display_corpus import DISPLAY_ROLE

    role = DISPLAY_ROLE
    example_bytes: bytes | None = None
    example_source: str | None = None
    if sysex_root is not None:
        from ..paths import prog_menus_root

        idle_path = prog_menus_root(sysex_root) / "no menu.syx"
        if idle_path.is_file():
            try:
                from ..frame import parse_sysex

                example_bytes = parse_sysex(idle_path.read_bytes()).raw
                example_source = str(idle_path)
            except ValueError:
                pass
    for off in (146, 147):
        cell = annotations[off]
        cell["status"] = "known"
        cell["role"] = role
        cell["encoding"] = "nibble_hilo"
        cell["confidence"] = "high"
        cell["parameters"] = ["_menus"]
        if example_bytes is not None and example_source and off < len(example_bytes):
            cell["hex"] = f"{example_bytes[off]:02X}"
            cell["hex_source"] = example_source


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
        role = first["role"]
        if first.get("parameters") and first["status"] == "secondary":
            role += (
                f" (moved in independent series: {', '.join(first['parameters'])})"
            )
        regions.append(
            {
                "start": first_off,
                "end": last_off,
                "offsets": offsets,
                "length": len(chunk),
                "example_hex": example,
                "status": first["status"],
                "role": role,
                "parameters": list(first.get("parameters") or []),
            }
        )
        if i < len(annotations):
            start = i
            prev = cur
    return regions
