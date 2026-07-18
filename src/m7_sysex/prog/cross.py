"""Cross-series meta-analysis (separate from independent per-folder diffs).

Compares *messages as opaque samples* and *per-folder conclusions* - never
treats absolute payload values from folder A as the state of folder B.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from ..frame import CHECKSUM_NIBBLE_COUNT, DATA_OFFSET
from .display import DISPLAY_OFFSETS


def cross_analyze(
    results: list[dict[str, Any]],
    sysex_root: Path | None = None,
) -> dict[str, Any]:
    """
    Meta-analysis across independent parameter series.

    Safe uses of the corpus:
    - which offsets are identical in every captured message (stable in this set)
    - which offsets recur as secondary movers across series
    - whether two series claim the same primary offset (conflict)
    - payload offsets never touched by any series (coverage gaps)
    - checksum formula search treating each message independently
    """
    if not results:
        raise ValueError("no analysis results for cross analysis")

    length = int(results[0]["message_length"])
    messages: list[dict[str, Any]] = []
    for result in results:
        folder = Path(result["folder"])
        for dump in result.get("dumps") or []:
            path = folder / dump["file"]
            if not path.is_file():
                continue
            raw = path.read_bytes()
            if len(raw) != length:
                continue
            messages.append(
                {
                    "parameter": result["parameter"],
                    "file": dump["file"],
                    "path": str(path),
                    "raw": raw,
                }
            )

    if len(messages) < 2:
        raise ValueError("need at least 2 dumps across series for cross analysis")

    stable_offsets: list[int] = []
    variable_offsets: list[int] = []
    for i in range(length):
        values = {m["raw"][i] for m in messages}
        if len(values) == 1:
            stable_offsets.append(i)
        else:
            variable_offsets.append(i)

    # Per-series changing / primary / secondary from independent analyses.
    series_touch: dict[str, dict[str, Any]] = {}
    secondary_hits: Counter[int] = Counter()
    primary_claims: dict[int, list[dict[str, Any]]] = defaultdict(list)

    for result in results:
        name = result["parameter"]
        changing = list(result.get("changing_offsets") or [])
        primary = list((result.get("best_encoding") or {}).get("offsets") or [])
        secondary = list(
            (result.get("classification") or {}).get("secondary_offsets") or []
        )
        confidence = (result.get("hypothesis") or {}).get("confidence")
        series_touch[name] = {
            "changing_offsets": changing,
            "primary_offsets": primary,
            "secondary_offsets": secondary,
            "confidence": confidence,
            "dump_count": result.get("dump_count"),
        }
        for off in secondary:
            if off in DISPLAY_OFFSETS:
                continue
            secondary_hits[off] += 1
        for off in primary:
            primary_claims[off].append(
                {
                    "parameter": name,
                    "confidence": confidence,
                    "encoding": (result.get("best_encoding") or {}).get("encoding"),
                }
            )

    recurrent_secondary = [
        {
            "offset": off,
            "series_count": count,
            "series": sorted(
                name
                for name, info in series_touch.items()
                if off in info["secondary_offsets"]
            ),
        }
        for off, count in sorted(secondary_hits.items())
        if count >= 2
    ]

    conflicts = []
    for off, claims in sorted(primary_claims.items()):
        params = {c["parameter"] for c in claims}
        if len(params) > 1:
            conflicts.append({"offset": off, "claims": claims})

    touched = set()
    for info in series_touch.values():
        touched.update(info["changing_offsets"])
        touched.update(info["primary_offsets"])

    checksum_start = length - 1 - CHECKSUM_NIBBLE_COUNT
    coverage_gaps = sorted(
        i
        for i in range(DATA_OFFSET, checksum_start)
        if i not in touched
    )

    checksum = _search_checksum(messages, checksum_start)

    # Stable payload nibbles (inside data region, identical everywhere in corpus).
    stable_payload = [i for i in stable_offsets if DATA_OFFSET <= i < checksum_start]

    return {
        "kind": "cross_series_meta",
        "disclaimer": (
            "Cross analysis does not transfer absolute parameter values between "
            "folders. Each sysex/<parameter>/ stream remains independent; this "
            "pass only looks for stable bytes, recurrent movers, claim conflicts, "
            "untouched offsets, and checksum hypotheses across the message corpus."
        ),
        "message_length": length,
        "message_count": len(messages),
        "series_count": len(results),
        "series": sorted(series_touch.keys()),
        "stable_offsets": stable_offsets,
        "stable_payload_offsets": stable_payload,
        "variable_offset_count": len(variable_offsets),
        "recurrent_secondary": recurrent_secondary,
        "primary_conflicts": conflicts,
        "coverage_gaps": coverage_gaps,
        "series_touch": series_touch,
        "checksum": checksum,
    }


def render_cross_markdown(cross: dict[str, Any]) -> str:
    """Markdown body for specification/prog/cross.md."""
    lines: list[str] = [
        "## Cross-series analysis",
        "",
        cross["disclaimer"],
        "",
        f"Corpus: **{cross['message_count']}** messages from "
        f"**{cross['series_count']}** independent series "
        f"({', '.join(f'`{s}`' for s in cross['series'])}).",
        "",
        "Run standalone with `python -m m7_sysex cross` "
        "(also included in `python -m m7_sysex export`).",
        "",
        "### Stable bytes (identical in every captured message)",
        "",
        f"**{len(cross['stable_offsets'])}** offsets never change in this corpus "
        f"({len(cross['stable_payload_offsets'])} of those are in the payload "
        f"before the checksum).",
        "",
    ]
    if cross["stable_payload_offsets"]:
        lines.append(
            "Stable payload offsets: "
            + _fmt_offset_list(cross["stable_payload_offsets"])
        )
        lines.append("")
        lines.append(
            "_Stable-in-corpus ≠ immutable forever - only unused or fixed "
            "in these captures._"
        )
        lines.append("")

    lines.extend(
        [
            "### Recurrent secondary movers",
            "",
            "Offsets that moved as non-primary fields in **two or more** "
            "independent series (likely shared edit/UI/state, not a sound parameter):",
            "",
        ]
    )
    if cross["recurrent_secondary"]:
        from ..export import parameter_md_link

        lines.append("| Offset | Series count | Seen in |")
        lines.append("|--------|-------------:|---------|")
        for row in cross["recurrent_secondary"]:
            seen = ", ".join(
                parameter_md_link(s)
                if s not in {"_presets", "_corpus"}
                else f"`{s}`"
                for s in row["series"]
            )
            lines.append(
                f"| {row['offset']} | {row['series_count']} | {seen} |"
            )
        lines.append("")
    else:
        lines.append("_None yet._")
        lines.append("")

    lines.extend(["### Primary offset conflicts", ""])
    if cross["primary_conflicts"]:
        lines.append(
            "Two or more series claimed the same primary offset - investigate:"
        )
        lines.append("")
        for row in cross["primary_conflicts"]:
            claims = ", ".join(
                f"`{c['parameter']}` ({c.get('confidence')}, {c.get('encoding')})"
                for c in row["claims"]
            )
            lines.append(f"- offset **{row['offset']}**: {claims}")
        lines.append("")
    else:
        lines.append("No primary-offset conflicts between series.")
        lines.append("")

    gaps = cross["coverage_gaps"]
    lines.extend(
        [
            "### Untouched in parameter series",
            "",
            f"**{len(gaps)}** payload offsets never changed in any independent "
            "`sysex/prog/parameters/<name>/` capture series:",
            "",
            _fmt_offset_list(gaps) if gaps else "_Every payload offset moved in at least one series._",
            "",
            "Many of these are already documented elsewhere — program identity "
            "(offsets 88–91), fixed/reserved fields, and corpus-derived meta — "
            "see [byte-map-overview.md](byte-map-overview.md). This list means "
            "no dedicated single-parameter series has moved them yet, not that "
            "the byte map is unknown.",
            "",
            "### Checksum hypotheses",
            "",
        ]
    )
    cs = cross.get("checksum") or {}
    algo = cs.get("algorithm")
    if algo:
        lines.extend(
            [
                f"**Verified:** `{algo['name']}` "
                f"(also {', '.join(algo.get('also_known_as') or [])}).",
                "",
                f"- Cover: {algo['cover']}",
                f"- Exclude: {algo['exclude']}",
                f"- Poly/init: {algo['poly']}, init {algo['init']}, "
                f"refin={algo['refin']}, refout={algo['refout']}, "
                f"xorout={algo['xorout']}",
                f"- Pack: {algo['pack']}",
                "",
            ]
        )
    if cs.get("matches"):
        lines.append(
            f"Hypotheses that fit **all** messages "
            f"({cs.get('tried', 0)} tried):"
        )
        lines.append("")
        for m in cs["matches"][:12]:
            mark = " (verified cover)" if m.get("verified") else ""
            lines.append(f"- `{m['name']}` - {m['detail']}{mark}")
        if len(cs["matches"]) > 12:
            lines.append(f"- ...and {len(cs['matches']) - 12} more equivalents")
        lines.append("")
    elif not algo:
        lines.append(
            "No checksum matched all messages yet "
            f"(tried {cs.get('tried', 0)} hypotheses)."
        )
        lines.append("")

    return "\n".join(lines)


def write_cross_analysis(cross: dict[str, Any], path: Path) -> Path:
    import json

    path = Path(path)
    if path.exists():
        path.unlink()
    # raw bytes not present in cross dict - good, JSON-serializable
    path.write_text(json.dumps(cross, indent=2) + "\n", encoding="utf-8")
    return path


def _fmt_offset_list(offsets: list[int]) -> str:
    if not offsets:
        return "-"
    # Collapse contiguous runs.
    runs: list[str] = []
    start = prev = offsets[0]
    for off in offsets[1:]:
        if off == prev + 1:
            prev = off
            continue
        runs.append(str(start) if start == prev else f"{start}-{prev}")
        start = prev = off
    runs.append(str(start) if start == prev else f"{start}-{prev}")
    return ", ".join(f"`{r}`" for r in runs)


def _search_checksum(
    messages: list[dict[str, Any]], checksum_start: int
) -> dict[str, Any]:
    """Try sum/XOR/CRC checksum formulas; each message is an independent sample."""
    from ..frame import crc16_arc, pack_u16_be_nibbles

    def pack_lohi(val: int, n: int = 4) -> list[int]:
        out = []
        for i in range(n):
            out.append((val >> (4 * i)) & 0x0F)
        return out

    def pack_hilo_be(val: int, n: int = 4) -> list[int]:
        out = []
        for i in range(n - 1, -1, -1):
            out.append((val >> (4 * i)) & 0x0F)
        return out

    def pack_be_bytes(val: int) -> list[int]:
        return list(pack_u16_be_nibbles(val))

    def pack_hilo_bytes(raw: bytes, start: int, end: int) -> bytes:
        data = raw[start:end]
        return bytes(
            (data[i] << 4) | data[i + 1] for i in range(0, len(data) - 1, 2)
        )

    # (name, fn -> int over raw message)
    value_fns: list[tuple[str, Any]] = [
        ("sum[1:cs)", lambda raw: sum(raw[1:checksum_start])),
        ("sum[4:cs)", lambda raw: sum(raw[4:checksum_start])),
        ("sum[8:cs)", lambda raw: sum(raw[8:checksum_start])),
        ("sum[88:cs)", lambda raw: sum(raw[DATA_OFFSET:checksum_start])),
        ("xor[1:cs)", lambda raw: _xor(raw[1:checksum_start])),
        ("xor[8:cs)", lambda raw: _xor(raw[8:checksum_start])),
        ("xor[88:cs)", lambda raw: _xor(raw[DATA_OFFSET:checksum_start])),
        (
            "sum_pack_hilo[88:cs)",
            lambda raw: sum(pack_hilo_bytes(raw, DATA_OFFSET, checksum_start)),
        ),
        (
            "xor_pack_hilo[88:cs)",
            lambda raw: _xor(pack_hilo_bytes(raw, DATA_OFFSET, checksum_start)),
        ),
        ("fletcher16[8:cs)", lambda raw: _fletcher16(raw[8:checksum_start])),
        ("fletcher16[88:cs)", lambda raw: _fletcher16(raw[DATA_OFFSET:checksum_start])),
        (
            "crc16_arc[8:cs)",
            lambda raw: crc16_arc(raw[8:checksum_start]),
        ),
        (
            "crc16_arc[88:cs)",
            lambda raw: crc16_arc(raw[DATA_OFFSET:checksum_start]),
        ),
        (
            "crc16_arc[4:cs)",
            lambda raw: crc16_arc(raw[4:checksum_start]),
        ),
        (
            "crc16_arc[1:cs)",
            lambda raw: crc16_arc(raw[1:checksum_start]),
        ),
        (
            "crc16_arc[0:cs)",
            lambda raw: crc16_arc(raw[0:checksum_start]),
        ),
        (
            "crc16_ccitt_false[8:cs)",
            lambda raw: _crc16_ccitt_false(raw[8:checksum_start]),
        ),
        (
            "crc16_xmodem[8:cs)",
            lambda raw: _crc16_xmodem(raw[8:checksum_start]),
        ),
        (
            "crc16_modbus[8:cs)",
            lambda raw: _crc16_modbus(raw[8:checksum_start]),
        ),
        (
            "crc16_arc_pack_hilo[88:cs)",
            lambda raw: crc16_arc(pack_hilo_bytes(raw, DATA_OFFSET, checksum_start)),
        ),
        (
            "crc16_arc[8:88)+pack_hilo[88:cs)",
            lambda raw: crc16_arc(
                raw[8:DATA_OFFSET] + pack_hilo_bytes(raw, DATA_OFFSET, checksum_start)
            ),
        ),
    ]

    encodings = [
        ("nibs_le", pack_lohi),
        ("nibs_be", pack_hilo_be),
        ("u16_be_nibs", pack_be_bytes),
    ]
    transforms = [
        ("id16", lambda v: v & 0xFFFF),
        ("neg16", lambda v: (-v) & 0xFFFF),
        ("ones16", lambda v: (~v) & 0xFFFF),
        ("sum8", lambda v: v & 0xFF),
        ("neg8", lambda v: (-v) & 0xFF),
    ]

    matches: list[dict[str, Any]] = []
    tried = 0
    for range_name, range_fn in value_fns:
        for enc_name, enc_fn in encodings:
            for tr_name, tr_fn in transforms:
                # 8-bit transforms only need 2 nibbles; still pad to 4 for compare
                if tr_name in {"sum8", "neg8"} and enc_name == "u16_be_nibs":
                    continue
                tried += 1
                name = f"{tr_name}({range_name})/{enc_name}"
                ok = True
                for msg in messages:
                    raw = msg["raw"]
                    actual = list(raw[checksum_start : checksum_start + 4])
                    pred = enc_fn(tr_fn(range_fn(raw)))
                    pred = (pred + [0, 0, 0, 0])[:4]
                    if pred != actual:
                        ok = False
                        break
                if ok:
                    matches.append(
                        {
                            "name": name,
                            "detail": (
                                f"{tr_name} of {range_name}, packed as {enc_name}"
                            ),
                            "verified": range_name.startswith("crc16_arc[8:cs)"),
                        }
                    )

    # Prefer the known ARC match first in the list.
    matches.sort(key=lambda m: (0 if m.get("verified") else 1, m["name"]))
    verified = next((m for m in matches if m.get("verified")), None)
    return {
        "tried": tried,
        "matches": matches,
        "verified": verified,
        "algorithm": (
            {
                "name": "CRC-16/ARC",
                "also_known_as": ["CRC-16/IBM", "CRC-16/ANSI"],
                "poly": "0x8005 (reflected 0xA001)",
                "init": "0x0000",
                "refin": True,
                "refout": True,
                "xorout": "0x0000",
                "cover": "offsets 8..151 (80-byte name + payload nibbles as stored)",
                "exclude": "F0, manufacturer ID, header 70 08 01 00, checksum, F7",
                "pack": "16-bit CRC as four high-nibble-first SysEx bytes",
            }
            if verified
            else None
        ),
    }


def _xor(data: bytes) -> int:
    x = 0
    for b in data:
        x ^= b
    return x


def _fletcher16(data: bytes) -> int:
    s1 = 0
    s2 = 0
    for b in data:
        s1 = (s1 + b) % 255
        s2 = (s2 + s1) % 255
    return ((s2 & 0xFF) << 8) | (s1 & 0xFF)


def _crc16_ccitt_false(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def _crc16_xmodem(data: bytes) -> int:
    crc = 0x0000
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def _crc16_modbus(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF
