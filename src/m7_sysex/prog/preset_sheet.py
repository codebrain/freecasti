"""Compare decoded ``sysex/prog/presets/`` dumps to Bricasti's published preset sheet.

Source PDF: https://www.bricasti.com/images/preset_sheet.pdf

Parsed rows live in ``docs/reference/preset_sheet.json`` (committed). Normal
runs load that JSON — no PDF / pymupdf needed. Refresh with
``python run.py sheet --refresh`` (requires pymupdf).
"""

from __future__ import annotations

import json
import re
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..paths import PROG_PRESETS_DIR

PRESET_SHEET_URL = "https://www.bricasti.com/images/preset_sheet.pdf"
DEFAULT_CACHE_NAME = "preset_sheet.pdf"
DEFAULT_SHEET_JSON = Path("docs/reference/preset_sheet.json")
PRESETS_CORPUS_HINT = f"sysex/prog/{PROG_PRESETS_DIR}/"
PRESETS_ANALYSIS_HINT = f"{PRESETS_CORPUS_HINT}analysis.json"

# Left → right after the preset name on each sheet row.
SHEET_COLS = (
    "predelay",
    "reverb time",
    "size",
    "diffusion",
    "density",
    "hf rt multiply",
    "hf rt crossover",
    "lf rt multiply",
    "lf rt crossover",
    "vlf cut",
    "modulation",
    "early to reverb mix",
    "early rolloff",
    "early select",
    "rolloff",
)

# Parameters we decode from SysEx (series captures and/or preset-sheet inference).
COMPARABLE = SHEET_COLS

DISCRETE = frozenset(
    {
        "size",
        "diffusion",
        "density",
        "early select",
        "vlf cut",
        "early to reverb mix",
        "modulation",
        "hf rt multiply",
        "lf rt multiply",
    }
)

BANK_HEADERS = frozenset(
    {"Halls", "Rooms", "Chambers", "Plates", "Spaces", "Ambience"}
)

# Sheet abbreviations → dump preset names.
NAME_ALIASES = {
    "med hall": "medium hall",
    "med and near": "medium and near",
    "med and deep": "medium and deep",
    "med and dark": "medium and dark",
    "meduim and bright": "medium and bright",
}

_HEADER_SKIP = frozenset(
    {
        "Size",
        "Diffusion",
        "Density",
        "VLF Cut",
        "Modulation",
        "Early/reverb",
        "Reverb Rolloff",
        "y",
        "",
    }
)


def normalize_name(s: str) -> str:
    s = s.lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def default_cache_path(sysex_root: Path) -> Path:
    return Path(sysex_root).resolve().parent / ".cache" / DEFAULT_CACHE_NAME


def default_sheet_json_path(sysex_root: Path | None = None) -> Path:
    """Committed parsed-sheet JSON next to the repo's docs/ tree."""
    if sysex_root is not None:
        root = Path(sysex_root).resolve().parent
        return root / DEFAULT_SHEET_JSON
    return Path(DEFAULT_SHEET_JSON)


def ensure_preset_sheet(
    pdf_path: Path | None = None,
    *,
    sysex_root: Path | None = None,
    url: str = PRESET_SHEET_URL,
    force_download: bool = False,
) -> Path:
    """Return a local path to the preset sheet PDF, downloading if needed."""
    if pdf_path is not None:
        path = Path(pdf_path)
        if not path.is_file():
            raise FileNotFoundError(f"preset sheet not found: {path}")
        return path.resolve()

    cache = default_cache_path(sysex_root or Path("sysex"))
    if cache.is_file() and not force_download:
        return cache

    cache.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, cache)
    return cache


def load_sheet_json(path: Path) -> list[dict[str, Any]]:
    """Load parsed preset rows from ``docs/reference/preset_sheet.json``."""
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("presets")
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"no presets in sheet JSON: {path}")
    for row in rows:
        if not isinstance(row, dict) or "bank" not in row or "preset" not in row:
            raise ValueError(f"invalid preset row in {path}")
        if "sheet" not in row or not isinstance(row["sheet"], dict):
            raise ValueError(f"preset row missing sheet values in {path}")
    return rows


def write_sheet_json(
    rows: list[dict[str, Any]],
    path: Path,
    *,
    source_pdf: str | None = None,
    source_url: str = PRESET_SHEET_URL,
) -> Path:
    """Write parsed sheet rows to JSON for offline compare."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    banks = dict(sorted(Counter(r["bank"] for r in rows).items()))
    pdf_ref = source_pdf
    if pdf_ref:
        # Keep committed JSON portable — don't embed machine-local absolute paths.
        name = Path(pdf_ref).name
        if name == DEFAULT_CACHE_NAME:
            pdf_ref = f".cache/{DEFAULT_CACHE_NAME}"
    payload = {
        "kind": "bricasti_preset_sheet",
        "source_url": source_url,
        "source_pdf": pdf_ref,
        "parsed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "columns": list(SHEET_COLS),
        "preset_count": len(rows),
        "banks": banks,
        "presets": [
            {
                "bank": r["bank"],
                "preset": r["preset"],
                "sheet": {col: r["sheet"][col] for col in SHEET_COLS},
            }
            for r in rows
        ],
        "notes": [
            "Parsed from the published PDF. Blank Modulation / Early Rolloff "
            "cells are filled as 'off' / '?' during parse.",
            "Refresh with: python run.py sheet --refresh",
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def refresh_sheet_json(
    *,
    sysex_root: Path = Path("sysex"),
    pdf_path: Path | None = None,
    json_path: Path | None = None,
    force_download: bool = False,
) -> tuple[Path, list[dict[str, Any]]]:
    """Re-parse the PDF and overwrite the committed sheet JSON."""
    pdf = ensure_preset_sheet(
        pdf_path, sysex_root=sysex_root, force_download=force_download
    )
    rows = parse_preset_sheet(pdf)
    out = Path(json_path) if json_path else default_sheet_json_path(sysex_root)
    write_sheet_json(rows, out, source_pdf=str(pdf))
    return out, rows


def load_sheet_rows(
    *,
    sysex_root: Path = Path("sysex"),
    json_path: Path | None = None,
    pdf_path: Path | None = None,
    refresh: bool = False,
    force_download: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return sheet rows plus load metadata.

    Prefers the committed JSON. With ``refresh=True``, re-parses the PDF and
    rewrites that JSON (requires pymupdf).
    """
    out_json = Path(json_path) if json_path else default_sheet_json_path(sysex_root)
    meta: dict[str, Any] = {"sheet_json": str(out_json)}

    if refresh:
        pdf = ensure_preset_sheet(
            pdf_path, sysex_root=sysex_root, force_download=force_download
        )
        rows = parse_preset_sheet(pdf)
        write_sheet_json(rows, out_json, source_pdf=str(pdf))
        meta["source"] = "pdf"
        meta["pdf_path"] = str(pdf)
        return rows, meta

    if out_json.is_file():
        rows = load_sheet_json(out_json)
        meta["source"] = "json"
        return rows, meta

    # First-time fallback: parse PDF and write JSON.
    pdf = ensure_preset_sheet(
        pdf_path, sysex_root=sysex_root, force_download=force_download
    )
    rows = parse_preset_sheet(pdf)
    write_sheet_json(rows, out_json, source_pdf=str(pdf))
    meta["source"] = "pdf"
    meta["pdf_path"] = str(pdf)
    return rows, meta


def parse_preset_sheet(pdf_path: Path) -> list[dict[str, Any]]:
    """Parse factory preset rows from the Bricasti PDF.

    Each row is ``{bank, preset, sheet: {param: token}}``.

    Some printed rows omit a blank cell (commonly Modulation, occasionally
    Early Rolloff). Those 14-token rows are normalized back to 15 columns.
    """
    try:
        import fitz  # pymupdf
    except ImportError as exc:
        raise ImportError(
            "preset sheet comparison requires pymupdf - run: pip install pymupdf"
        ) from exc

    lines: list[str] = []
    for page in fitz.open(Path(pdf_path)):
        lines.extend(ln.strip() for ln in page.get_text("text").splitlines())

    rows: list[dict[str, Any]] = []
    current_bank: str | None = None
    i = 0
    nval = len(SHEET_COLS)

    while i < len(lines):
        ln = lines[i]
        if ln in BANK_HEADERS:
            current_bank = ln
            i += 1
            continue
        if current_bank and _looks_like_preset_name(ln):
            j = i + 1
            raw_vals: list[str] = []
            while j < len(lines) and _looks_like_value(lines[j]):
                raw_vals.append(lines[j])
                j += 1
            vals = _normalize_sheet_values(raw_vals)
            if vals is not None and len(vals) == nval:
                rows.append(
                    {
                        "bank": current_bank,
                        "preset": ln,
                        "sheet": dict(zip(SHEET_COLS, vals)),
                    }
                )
                i = j
                continue
        i += 1

    return rows


def _normalize_sheet_values(vals: list[str]) -> list[str] | None:
    """Pad blank omitted cells so each row has one token per SHEET_COLS entry."""
    nval = len(SHEET_COLS)
    if len(vals) == nval:
        return list(vals)
    if len(vals) != nval - 1:
        return None

    # Missing Modulation: after VLF the next token is Early/reverb (N/M).
    mod_i = SHEET_COLS.index("modulation")
    if "/" in vals[mod_i]:
        fixed = list(vals)
        fixed.insert(mod_i, "off")
        return fixed

    # Missing Early Rolloff: after Early/reverb comes Early Select (small int).
    eroll_i = SHEET_COLS.index("early rolloff")
    if (
        eroll_i < len(vals)
        and "/" in vals[eroll_i - 1]
        and re.fullmatch(r"\d{1,2}", vals[eroll_i] or "")
    ):
        fixed = list(vals)
        fixed.insert(eroll_i, "?")
        return fixed

    return None


def _looks_like_preset_name(ln: str) -> bool:
    if not ln or ln[0].isdigit() or ln in _HEADER_SKIP:
        return False
    if ln in BANK_HEADERS:
        return False
    lowered = ln.lower()
    if "reverb" in lowered or "hf rt" in lowered or "early rolloff" in lowered:
        return False
    if "lf rt" in lowered or "xover" in lowered:
        return False
    return True


def _looks_like_value(v: str) -> bool:
    vl = v.lower()
    if vl in {
        "off",
        "full",
        "low",
        "high",
        "h",
        "l",
        "hi",
        "sm",
        "ms",
        "large",
        "small",
        "?",
    }:
        return True
    if "/" in v:
        return True
    return bool(re.match(r"^[+-]?\d", v))


def load_preset_dumps(analysis_path: Path) -> list[dict[str, Any]]:
    data = json.loads(Path(analysis_path).read_text(encoding="utf-8"))
    dumps = data.get("dumps") or []
    if not dumps:
        raise ValueError(f"no dumps in {analysis_path}")
    if not any(d.get("parameters") for d in dumps):
        raise ValueError(
            f"{analysis_path} has no decoded parameters — run `python run.py` first"
        )
    return dumps


def find_presets_analysis(sysex_root: Path) -> Path:
    from .names import find_names_folder

    folder = find_names_folder(sysex_root)
    if folder is None:
        raise FileNotFoundError(
            f"no {PRESETS_CORPUS_HINT} (or legacy _presets) folder under {sysex_root}"
        )
    path = folder / "analysis.json"
    if not path.is_file():
        raise FileNotFoundError(
            f"missing {path} — run `python run.py` to decode presets first"
        )
    return path


def parse_sheet_value(param: str, token: str) -> tuple[str, float | str | None]:
    """Return ``(kind, value)`` where kind is ``num``, ``tok``, or ``skip``."""
    t = token.strip()
    tl = t.lower()
    if tl in {"?", ""}:
        return "skip", None
    # Size extremes: sheet prints L / Large / Sm / Small (not Low/High).
    if param == "size":
        if tl in {"l", "large"}:
            return "tok", "large"
        if tl in {"s", "sm", "ms", "small"}:
            return "tok", "small"
    if tl in {"off", "full", "low", "high", "h", "l", "hi"}:
        mapped = {"h": "high", "l": "low", "hi": "high"}.get(tl, tl)
        # Sheet often prints H/Low for density/diffusion extremes.
        if param in {"density", "diffusion"}:
            if mapped == "high":
                return "num", 10.0
            if mapped == "low":
                return "num", 0.0
        # Sheet often prints ``1`` for minimum modulation; ``low`` is the same.
        if param == "modulation" and mapped == "low":
            return "num", 1.0
        return "tok", mapped
    if tl in {"large", "small", "sm", "ms"}:
        return "tok", {"sm": "small", "ms": "small"}.get(tl, tl)
    if param == "early to reverb mix":
        from ..labels import balance_path_position, parse_balance_pair_token

        pair = parse_balance_pair_token(t)
        if pair is not None:
            pos = balance_path_position(pair[0], pair[1], 20)
            if pos is not None:
                return "num", float(pos)
            return "skip", None
        # Bare path position (0..40) if the sheet ever prints that way.
        try:
            v = float(t)
            return ("num", v) if 0 <= v <= 40 else ("skip", None)
        except ValueError:
            return "skip", None
    if param == "modulation" and tl.isdigit():
        return "num", float(tl)
    try:
        return "num", float(re.sub(r"(?i)(ms|hz|db|s)$", "", t))
    except ValueError:
        return "tok", tl


def parse_ours_value(param: str, display: str) -> tuple[str, float | str | None]:
    d = (display or "").strip()
    if d.startswith("~"):
        d = d[1:].strip()
    if param == "size" and d.lower() in {"l", "large", "s", "sm", "ms", "small"}:
        return "tok", (
            "large" if d.lower() in {"l", "large"} else "small"
        )
    if param == "modulation" and d.lower() == "low":
        return "num", 1.0
    if d.lower() in {"off", "low", "high", "full"}:
        return "tok", d.lower()
    if param == "early to reverb mix":
        from ..labels import balance_path_position, parse_balance_pair_token

        pair = parse_balance_pair_token(d)
        if pair is not None:
            pos = balance_path_position(pair[0], pair[1], 20)
            if pos is not None:
                return "num", float(pos)
    if d.startswith("idx "):
        return "skip", None
    m = re.match(r"^([+-]?\d+(?:\.\d+)?)", d)
    if not m:
        return "tok", d.lower()
    return "num", float(m.group(1))


def _tolerance(param: str, sheet_v: float, ours_v: float) -> float:
    if param in DISCRETE:
        return 0.51
    if param == "predelay":
        return 3.0
    if param == "reverb time":
        return 0.08
    if param in {"hf rt multiply", "lf rt multiply"}:
        return 0.03
    if param in {"hf rt crossover", "lf rt crossover", "rolloff", "early rolloff"}:
        return max(400.0, 0.12 * max(abs(sheet_v), abs(ours_v)))
    return 1e-9


def _soft_tolerance(param: str, sheet_v: float, ours_v: float) -> float:
    """Wider band for known table-interpolation / print-rounding drift."""
    if param == "predelay":
        return max(20.0, 0.5 * max(abs(sheet_v), abs(ours_v)))
    if param == "reverb time":
        return 0.2
    if param in {"rolloff", "early rolloff"}:
        return max(1500.0, 0.25 * max(abs(sheet_v), abs(ours_v)))
    # Crossover tables: allow modest drift; large sheet/dump gaps stay hard.
    if param in {"hf rt crossover", "lf rt crossover"}:
        return max(500.0, 0.1 * max(abs(sheet_v), abs(ours_v)))
    return _tolerance(param, sheet_v, ours_v)


def _canonical_preset_key(bank: str, preset: str) -> tuple[str, str]:
    n = normalize_name(preset)
    return bank, NAME_ALIASES.get(n, n)


def build_sheet_index(
    sheet_rows: list[dict[str, Any]],
) -> dict[tuple[str, str], dict[str, Any]]:
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for row in sheet_rows:
        key = _canonical_preset_key(row["bank"], row["preset"])
        index[key] = row
        # Also index under the raw normalized sheet name.
        index[(row["bank"], normalize_name(row["preset"]))] = row
    return index


def match_sheet_row(
    dump: dict[str, Any],
    sheet_index: dict[tuple[str, str], dict[str, Any]],
    sheet_rows: list[dict[str, Any]],
) -> dict[str, Any] | None:
    bank = dump["bank"]
    preset = dump["preset"]
    if bank == "Halls 2":
        # Separate bank; not listed as such on the classic sheet.
        return None
    key = _canonical_preset_key(bank, preset)
    hit = sheet_index.get(key)
    if hit is not None:
        return hit
    # Same preset name, unique across sheet.
    n = normalize_name(preset)
    n = NAME_ALIASES.get(n, n)
    cands = [
        r
        for r in sheet_rows
        if NAME_ALIASES.get(normalize_name(r["preset"]), normalize_name(r["preset"]))
        == n
        and r["bank"] == bank
    ]
    if len(cands) == 1:
        return cands[0]
    return None


def compare_preset_to_sheet(
    dump: dict[str, Any],
    sheet_row: dict[str, Any],
) -> dict[str, Any]:
    """Classify per-parameter differences for one dump vs one sheet row.

    Also returns ``details``: one row per ``COMPARABLE`` parameter with dump
    display, sheet token, status (``match`` / ``soft`` / ``hard`` / ``skipped``),
    and optional ``delta``.
    """
    ours = dump.get("parameters") or {}
    hard: list[dict[str, Any]] = []
    soft: list[dict[str, Any]] = []
    matched: list[str] = []
    skipped: list[str] = []
    details: list[dict[str, Any]] = []

    for param in COMPARABLE:
        dump_display = None
        dump_encoded = None
        if param in ours:
            dump_display = ours[param].get("display")
            dump_encoded = ours[param].get("encoded")
        sheet_tok = (sheet_row.get("sheet") or {}).get(param)

        if param not in ours:
            skipped.append(param)
            details.append(
                {
                    "param": param,
                    "dump": dump_display,
                    "encoded": dump_encoded,
                    "sheet": sheet_tok,
                    "status": "skipped",
                }
            )
            continue

        sk, sv = parse_sheet_value(param, sheet_tok)
        ok, ov = parse_ours_value(param, str(dump_display or ""))
        if sk == "skip" or ok == "skip" or sv is None or ov is None:
            skipped.append(param)
            details.append(
                {
                    "param": param,
                    "dump": dump_display,
                    "encoded": dump_encoded,
                    "sheet": sheet_tok,
                    "status": "skipped",
                }
            )
            continue

        if sk == "tok" or ok == "tok":
            if str(sv).lower() != str(ov).lower():
                issue = {
                    "param": param,
                    "sheet": sheet_tok,
                    "ours": dump_display,
                    "encoded": dump_encoded,
                    "delta": delta,
                    "kind": "token",
                }
                hard.append(issue)
                details.append(
                    {
                        "param": param,
                        "dump": dump_display,
                        "encoded": dump_encoded,
                        "sheet": sheet_tok,
                        "status": "hard",
                        "kind": "token",
                    }
                )
            else:
                matched.append(param)
                details.append(
                    {
                        "param": param,
                        "dump": dump_display,
                        "encoded": dump_encoded,
                        "sheet": sheet_tok,
                        "status": "match",
                    }
                )
            continue

        assert isinstance(sv, float) and isinstance(ov, float)
        delta = ov - sv
        if abs(delta) <= _tolerance(param, sv, ov):
            matched.append(param)
            details.append(
                {
                    "param": param,
                    "dump": dump_display,
                    "encoded": dump_encoded,
                    "sheet": sheet_tok,
                    "status": "match",
                    "delta": delta,
                }
            )
        elif abs(delta) <= _soft_tolerance(param, sv, ov):
            issue = {
                "param": param,
                "sheet": sheet_tok,
                "ours": dump_display,
                "encoded": dump_encoded,
                "delta": delta,
                "kind": "table",
            }
            soft.append(issue)
            details.append(
                {
                    "param": param,
                    "dump": dump_display,
                    "encoded": dump_encoded,
                    "sheet": sheet_tok,
                    "status": "soft",
                    "delta": delta,
                    "kind": "table",
                }
            )
        else:
            issue = {
                "param": param,
                "sheet": sheet_tok,
                "ours": dump_display,
                "encoded": dump_encoded,
                "delta": delta,
                "kind": "value",
            }
            hard.append(issue)
            details.append(
                {
                    "param": param,
                    "dump": dump_display,
                    "encoded": dump_encoded,
                    "sheet": sheet_tok,
                    "status": "hard",
                    "delta": delta,
                    "kind": "value",
                }
            )

    return {
        "bank": dump["bank"],
        "preset": dump["preset"],
        "sheet_bank": sheet_row["bank"],
        "sheet_preset": sheet_row["preset"],
        "hard": hard,
        "soft": soft,
        "matched": matched,
        "skipped": skipped,
        "details": details,
    }


def compare_dumps_to_sheet(
    dumps: list[dict[str, Any]],
    sheet_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    index = build_sheet_index(sheet_rows)
    comparisons: list[dict[str, Any]] = []
    missing: list[dict[str, str]] = []
    skipped_banks: list[dict[str, str]] = []

    for dump in dumps:
        if dump.get("bank") == "Halls 2":
            skipped_banks.append(
                {
                    "bank": dump["bank"],
                    "preset": dump["preset"],
                    "reason": "not listed as a separate bank on the classic sheet",
                }
            )
            continue
        sheet = match_sheet_row(dump, index, sheet_rows)
        if sheet is None:
            missing.append({"bank": dump["bank"], "preset": dump["preset"]})
            continue
        comparisons.append(compare_preset_to_sheet(dump, sheet))

    hard = [c for c in comparisons if c["hard"]]
    soft_only = [c for c in comparisons if c["soft"] and not c["hard"]]
    exact = [c for c in comparisons if not c["hard"] and not c["soft"]]

    hard_by_param: Counter[str] = Counter()
    soft_by_param: Counter[str] = Counter()
    for c in comparisons:
        for row in c["hard"]:
            hard_by_param[row["param"]] += 1
        for row in c["soft"]:
            soft_by_param[row["param"]] += 1

    by_dump = {
        (c["bank"], c["preset"]): c for c in comparisons
    }

    return {
        "kind": "preset_sheet_compare",
        "source_url": PRESET_SHEET_URL,
        "sheet_preset_count": len(sheet_rows),
        "sheet_banks": dict(
            sorted(Counter(r["bank"] for r in sheet_rows).items())
        ),
        "dump_count": len(dumps),
        "matched_count": len(comparisons),
        "exact_count": len(exact),
        "soft_only_count": len(soft_only),
        "hard_count": len(hard),
        "missing_on_sheet": missing,
        "skipped_banks": skipped_banks,
        "hard_by_param": dict(hard_by_param),
        "soft_by_param": dict(soft_by_param),
        "comparisons": comparisons,
        "by_dump": by_dump,
        "notes": [
            "Table parameters densify with hardware UI walks (`provided`) when "
            "available; otherwise sheet-derived points fill gaps between capture "
            "anchors (series dumps always win on conflict).",
            "Soft diffs are usually print rounding or off-grid sheet values "
            "(especially predelay and Hz fields) once provided walks exist.",
            "Halls 2 is skipped - the classic PDF has no Halls 2 section.",
            "SysEx dumps are authoritative when they conflict with the PDF.",
        ],
    }


def sheet_status_for_dump(
    sheet_compare: dict[str, Any] | None,
    bank: str,
    preset: str,
) -> dict[str, Any]:
    """Lookup helper for per-preset page rendering.

    Returns ``{kind, comparison?}`` where kind is
    ``compared`` | ``missing`` | ``skipped`` | ``unavailable``.
    """
    if not sheet_compare:
        return {"kind": "unavailable"}
    key = (bank, preset)
    comparison = (sheet_compare.get("by_dump") or {}).get(key)
    if comparison is not None:
        return {"kind": "compared", "comparison": comparison}
    for row in sheet_compare.get("missing_on_sheet") or []:
        if row.get("bank") == bank and row.get("preset") == preset:
            return {"kind": "missing"}
    for row in sheet_compare.get("skipped_banks") or []:
        if row.get("bank") == bank and row.get("preset") == preset:
            return {
                "kind": "skipped",
                "reason": row.get("reason")
                or "not listed on the classic sheet",
            }
    return {"kind": "unavailable"}


def format_report(result: dict[str, Any], *, verbose: bool = False) -> str:
    lines: list[str] = [
        f"Bricasti preset sheet vs {PRESETS_CORPUS_HINT}",
        f"  sheet presets: {result['sheet_preset_count']} "
        f"({result['sheet_banks']})",
        f"  dumps: {result['dump_count']} / matched: {result['matched_count']} / "
        f"exact: {result['exact_count']} / soft-only: {result['soft_only_count']} / "
        f"hard: {result['hard_count']}",
        "",
    ]

    missing = result.get("missing_on_sheet") or []
    if missing:
        lines.append(f"Not on sheet ({len(missing)}):")
        for row in missing:
            lines.append(f"  - {row['bank']} / {row['preset']}")
        lines.append("")

    skipped = result.get("skipped_banks") or []
    if skipped:
        lines.append("Skipped:")
        for row in skipped:
            lines.append(
                f"  - {row['bank']} / {row['preset']} ({row['reason']})"
            )
        lines.append("")

    hard_comps = [c for c in result["comparisons"] if c["hard"]]
    if hard_comps:
        lines.append("Hard discrepancies:")
        for c in hard_comps:
            lines.append(
                f"  {c['bank']} / {c['preset']}  "
                f"[sheet: {c['sheet_bank']}/{c['sheet_preset']}]"
            )
            for iss in c["hard"]:
                extra = ""
                if "delta" in iss:
                    extra = f"  delta={iss['delta']:g}"
                lines.append(
                    f"    {iss['param']}: sheet={iss['sheet']!r} "
                    f"ours={iss['ours']!r}{extra}"
                )
            if verbose:
                for iss in c["soft"]:
                    lines.append(
                        f"    ~ {iss['param']}: sheet={iss['sheet']!r} "
                        f"ours={iss['ours']!r}"
                    )
        lines.append("")
    else:
        lines.append("Hard discrepancies: none")
        lines.append("")

    soft_only = [c for c in result["comparisons"] if c["soft"] and not c["hard"]]
    if soft_only:
        lines.append(
            f"Soft-only (table/rounding) presets: {len(soft_only)}"
            + (" - detail:" if verbose else " (pass --verbose for detail)")
        )
        if verbose:
            for c in soft_only:
                lines.append(f"  {c['bank']} / {c['preset']}")
                for iss in c["soft"]:
                    lines.append(
                        f"    ~ {iss['param']}: sheet={iss['sheet']!r} "
                        f"ours={iss['ours']!r}"
                    )
        else:
            for param, count in sorted(
                (result.get("soft_by_param") or {}).items(),
                key=lambda kv: (-kv[1], kv[0]),
            ):
                lines.append(f"  {param}: {count}")
        lines.append("")

    for note in result.get("notes") or []:
        lines.append(f"Note: {note}")

    return "\n".join(lines).rstrip() + "\n"


def _sheet_issue_row(c: dict[str, Any], iss: dict[str, Any]) -> str:
    """One hard/soft table row with bank, preset, and parameter links."""
    from ..export import bank_md_link, parameter_md_link, preset_md_link

    delta = iss.get("delta")
    delta_txt = f"{delta:g}" if isinstance(delta, float) else "-"
    enc = iss.get("encoded")
    enc_txt = str(enc) if enc is not None else "—"
    dump_txt = iss.get("ours") if iss.get("ours") is not None else "—"
    return (
        f"| {bank_md_link(c['bank'])} | "
        f"{preset_md_link(c['bank'], c['preset'])} | "
        f"{parameter_md_link(iss['param'])} | "
        f"{enc_txt} | {dump_txt} | {iss['sheet']} | {delta_txt} |"
    )


def _sheet_param_summary_table(
    title: str,
    counts: dict[str, int],
    *,
    link_params: bool = True,
) -> list[str]:
    """Markdown subsection: parameter → discrepancy count."""
    if not counts:
        return [f"## {title}", "", "None.", ""]
    from ..export import parameter_md_link

    lines = [f"## {title}", "", "| Parameter | Presets |", "|-----------|--------:|"]
    for param, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        name_cell = (
            parameter_md_link(param) if link_params else f"`{param}`"
        )
        lines.append(f"| {name_cell} | {count} |")
    lines.append("")
    return lines


def _sheet_preset_list_row(bank: str, preset: str, *, suffix: str = "") -> str:
    from ..export import bank_md_link, preset_md_link

    row = f"- {bank_md_link(bank)} / {preset_md_link(bank, preset)}"
    if suffix:
        row += f" — {suffix}"
    return row


def render_sheet_markdown(result: dict[str, Any], *, today: str) -> str:
    """Markdown errata page for specification/prog/preset-sheet.md."""
    lines: list[str] = [
        "# Preset sheet errata",
        "",
        f"_Generated {today}. Comparing decoded `{PRESETS_CORPUS_HINT}` dumps to "
        f"[Bricasti's published preset sheet]({PRESET_SHEET_URL}) "
        f"(parsed data: `docs/reference/preset_sheet.json`)._",
        "",
        "The classic PDF covers **V1-era banks only** (Ambience, Chambers, Halls, "
        "Plates, Rooms, Spaces). V2 banks (Halls 2, Plates 2, Rooms 2, Spaces 2), "
        "NonLin, and many later factory presets are **not on the sheet** — see "
        "[preset-inventory.md](preset-inventory.md) for the full capture list.",
        "",
        f"**Sheet presets:** {result['sheet_preset_count']} "
        f"({', '.join(f'{k}={v}' for k, v in (result.get('sheet_banks') or {}).items())})",
        "",
        f"**Dumps:** {result['dump_count']} matched "
        f"{result['matched_count']} "
        f"(exact {result['exact_count']}, "
        f"soft-only {result['soft_only_count']}, "
        f"hard {result['hard_count']})",
        "",
        "Hard = sheet value disagrees with the SysEx dump beyond tolerance. "
        "Soft = modest drift (often print rounding on Hz tables) once hardware "
        "UI walks densify the decode maps. SysEx dumps are treated as "
        "authoritative when they conflict with the PDF. "
        "Dump labels come from the densified encoding map (series captures, "
        "`provided` UI walks, and sheet anchors); `~` only when an encoding "
        "falls between labeled steps.",
        "",
        "See also [program-identity.md](program-identity.md), "
        "[presets/](presets/), and [parameters/README.md](parameters/README.md).",
        "",
    ]

    hard_by_param = result.get("hard_by_param") or {}
    soft_by_param = result.get("soft_by_param") or {}
    lines.extend(
        _sheet_param_summary_table("Hard discrepancies by parameter", hard_by_param)
    )
    lines.extend(
        _sheet_param_summary_table(
            "Soft discrepancies by parameter (table / rounding)",
            soft_by_param,
        )
    )

    hard_comps = [c for c in result["comparisons"] if c["hard"]]
    lines.extend(["## Hard discrepancies", ""])
    if not hard_comps:
        lines.extend(["None.", ""])
    else:
        lines.extend(
            [
                "| Bank | Preset | Parameter | Encoded | Dump | Sheet | Δ |",
                "|------|--------|-----------|--------:|------|------:|--:|",
            ]
        )
        for c in hard_comps:
            for iss in c["hard"]:
                lines.append(_sheet_issue_row(c, iss))
        lines.append("")

    soft_rows = [
        (c, iss)
        for c in result["comparisons"]
        for iss in c["soft"]
    ]
    lines.extend(["## Soft discrepancies (table / rounding)", ""])
    if not soft_rows:
        lines.extend(["None.", ""])
    else:
        lines.extend(
            [
                "| Bank | Preset | Parameter | Encoded | Dump | Sheet | Δ |",
                "|------|--------|-----------|--------:|------|------:|--:|",
            ]
        )
        for c, iss in soft_rows:
            lines.append(_sheet_issue_row(c, iss))
        lines.append("")

    missing = result.get("missing_on_sheet") or []
    lines.extend(["## Dumps not on the sheet", ""])
    if not missing:
        lines.extend(["None.", ""])
    else:
        lines.append(
            f"These factory dumps are in `{PRESETS_CORPUS_HINT}` but have no row "
            "on the classic PDF (likely later additions):"
        )
        lines.append("")
        for row in missing:
            lines.append(_sheet_preset_list_row(row["bank"], row["preset"]))
        lines.append("")

    skipped = result.get("skipped_banks") or []
    if skipped:
        lines.extend(["## Skipped (bank not on classic sheet)", ""])
        for row in skipped:
            lines.append(
                _sheet_preset_list_row(
                    row["bank"],
                    row["preset"],
                    suffix=row.get("reason") or "not listed on the classic sheet",
                )
            )
        lines.append("")

    lines.extend(["## Notes", ""])
    for note in result.get("notes") or []:
        lines.append(f"- {note}")
    if result.get("sheet_json"):
        sheet_path = _repo_relative_path(
            result["sheet_json"], "docs/reference/preset_sheet.json"
        )
        lines.append(
            f"- Sheet data: `{sheet_path}` ({result.get('sheet_source', '?')})"
        )
    if result.get("pdf_path"):
        lines.append(f"- Local PDF: `{_posix_path(result['pdf_path'])}`")
    if result.get("analysis_path"):
        analysis = _repo_relative_path(
            result["analysis_path"], PRESETS_ANALYSIS_HINT
        )
        lines.append(f"- Analysis: `{analysis}`")
    lines.extend(["", f"_Last exported: {today}_", ""])
    return "\n".join(lines)


def _posix_path(path: str | Path) -> str:
    return str(path).replace("\\", "/")


def _repo_relative_path(path: str | Path, preferred: str) -> str:
    text = _posix_path(path)
    if preferred in text:
        return preferred
    return text


def run_compare(
    *,
    sysex_root: Path = Path("sysex"),
    pdf_path: Path | None = None,
    analysis_path: Path | None = None,
    sheet_json: Path | None = None,
    refresh: bool = False,
    force_download: bool = False,
) -> dict[str, Any]:
    """Load sheet + dumps and return a comparison result dict."""
    sheet_rows, meta = load_sheet_rows(
        sysex_root=sysex_root,
        json_path=sheet_json,
        pdf_path=pdf_path,
        refresh=refresh,
        force_download=force_download,
    )
    if analysis_path is None:
        analysis_path = find_presets_analysis(sysex_root)
    dumps = load_preset_dumps(analysis_path)
    result = compare_dumps_to_sheet(dumps, sheet_rows)
    result["sheet_source"] = meta.get("source")
    result["sheet_json"] = meta.get("sheet_json")
    if meta.get("pdf_path"):
        result["pdf_path"] = meta["pdf_path"]
    result["analysis_path"] = str(analysis_path)
    return result


def write_sheet_markdown(
    result: dict[str, Any],
    output_path: Path,
    *,
    today: str | None = None,
    nav: str = "",
) -> Path:
    """Write the errata markdown page (optionally prepended with nav)."""
    from datetime import date

    if today is None:
        today = date.today().isoformat()
    body = render_sheet_markdown(result, today=today)
    text = (nav + body) if nav else body
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    return output_path
