"""Analyze sysex/_presets/ dumps named <bank>.<preset>.

These are not single-parameter series. They confirm the program-name field and
locate bank / program-slot identity bytes in the payload.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from ..frame import (
    CHECKSUM_NIBBLE_COUNT,
    NAME_LENGTH,
    NAME_OFFSET,
    parse_sysex,
)

# Meta capture folder (preferred name). Legacy ``_names`` still accepted.
from ..paths import LEGACY_PRESETS_DIR, prog_presets_root

# Soft bank-index hints from the V2 addendum bank list (0-based).
# Dump-derived indices always win when they disagree.
HINT_BANK_INDEX: dict[str, int] = {
    "Halls": 0,
    "Plates": 1,
    "Rooms": 2,
    "Chambers": 3,
    "Ambience": 4,
    "Spaces": 5,
    "Halls 2": 6,
    "Plates 2": 7,
    "Rooms 2": 8,
    "Spaces 2": 9,
    "NonLin": 10,
}

# Non-factory bank indices.
# Hold **EDIT** sends a 157-byte program-dump frame with bank word 88-89 = 11;
# offset 137 still mirrors the *source* factory/user bank (not 11).
# Indices 118-120 are from the Bricasti MIDI app notes (program-change /
# receive targets); 118 is the ephemeral Edit bank created on *receive*.
EDIT_DUMP_BANK_INDEX = 11
EDIT_RECEIVE_BANK_INDEX = 118
FAVORITES_BANK_INDEX = 119
REGISTERS_BANK_INDEX = 120

SPECIAL_BANK_LABELS: dict[int, str] = {
    EDIT_DUMP_BANK_INDEX: "Edit",
    EDIT_RECEIVE_BANK_INDEX: "Edit (receive)",
    FAVORITES_BANK_INDEX: "Favorites",
    REGISTERS_BANK_INDEX: "Registers",
}

# Factory spellings that differ from common export filenames (V2 addendum).
NAME_FIELD_ALIASES: dict[str, str] = {
    "NonLin A": "Nonlin A",
    "NonLin B": "Nonlin B",
    "NonLin C": "Nonlin C",
    "NonLin D": "Nonlin D",
}

BANK_WORD_OFFSETS = (88, 89)
PROGRAM_WORD_OFFSETS = (90, 91)
BANK_MIRROR_OFFSET = 137


def bank_map_sorted_by_index(
    bank_map: dict[str, int],
) -> list[tuple[str, int]]:
    """Return ``(bank name, index)`` pairs sorted by encoded bank index."""
    return sorted(bank_map.items(), key=lambda kv: kv[1])


def format_bank_map_by_index(bank_map: dict[str, int]) -> str:
    """Format ``Bank=index`` pairs for docs, sorted by index value."""
    return ", ".join(f"{name}={idx}" for name, idx in bank_map_sorted_by_index(bank_map))


class PresetDumpError(ValueError):
    """Filename preset/bank does not match SysEx program-identity fields."""


def bank_index_from_raw(raw: bytes) -> int:
    """Decode bank index from offsets 88-89 (nibble_hilo)."""
    from ..encodings import nibble_hilo

    return nibble_hilo(raw[BANK_WORD_OFFSETS[0]], raw[BANK_WORD_OFFSETS[1]])


def program_slot_from_raw(raw: bytes) -> int:
    """Decode program slot within bank from offsets 90-91 (nibble_hilo)."""
    from ..encodings import nibble_hilo

    return nibble_hilo(raw[PROGRAM_WORD_OFFSETS[0]], raw[PROGRAM_WORD_OFFSETS[1]])


def expected_bank_index(bank: str) -> int:
    """Return the factory bank index for a filename bank name."""
    try:
        return HINT_BANK_INDEX[bank]
    except KeyError as exc:
        known = ", ".join(sorted(HINT_BANK_INDEX))
        raise PresetDumpError(
            f"unknown bank name {bank!r} in preset filename "
            f"(expected one of: {known})"
        ) from exc


def bank_name_for_index(index: int) -> str | None:
    """Best-effort bank label for a dump bank index (for error messages)."""
    for name, idx in HINT_BANK_INDEX.items():
        if idx == index:
            return name
    return SPECIAL_BANK_LABELS.get(index)


def is_edit_buffer_dump(raw: bytes) -> bool:
    """True when offsets 88-89 encode the hold-EDIT send bank index (11)."""
    return bank_index_from_raw(raw) == EDIT_DUMP_BANK_INDEX


def edit_source_bank_index(raw: bytes) -> int:
    """Source bank from mirror offset 137 on an EDIT dump (banks 0-15).

    On hold-EDIT sends the bank word (88-89) is 11, but offset 137 still
    carries the low nibble of the program's original factory/user bank.
    """
    if not is_edit_buffer_dump(raw):
        raise ValueError(
            f"not an EDIT dump (bank index {bank_index_from_raw(raw)}, "
            f"expected {EDIT_DUMP_BANK_INDEX})"
        )
    return raw[BANK_MIRROR_OFFSET] & 0x0F


def validate_preset_dump(
    path: Path | str,
    raw: bytes | None = None,
) -> dict[str, Any]:
    """Validate ``<bank>.<preset>.syx`` against name and bank identity bytes.

    Raises ``PresetDumpError`` when the filename stem disagrees with offsets
    8-87 (program name), 88-89 (bank index), or 137 (bank mirror). Returns an
    identity dict on success (same fields used in ``analyze_names_folder``).
    """
    path = Path(path)
    if raw is None:
        raw = path.read_bytes()

    bank, preset = parse_preset_stem(path.stem)
    parse_sysex(raw)

    name_check = check_name_bytes(raw, preset)
    if not name_check.get("name_bytes_match"):
        detail = name_check.get("error")
        if detail is None:
            mismatch = name_check.get("name_mismatch") or {}
            detail = (
                f"name field {name_check.get('name_field')!r} does not match "
                f"filename preset {preset!r}"
            )
            if mismatch.get("offset") is not None:
                detail += (
                    f" (first mismatch at offset {mismatch['offset']}: "
                    f"expected {mismatch.get('expected_byte')}, "
                    f"got {mismatch.get('actual_byte')})"
                )
        raise PresetDumpError(f"{path.name}: {detail}")

    expected_index = expected_bank_index(bank)
    bank_index = bank_index_from_raw(raw)
    if bank_index != expected_index:
        dump_bank = bank_name_for_index(bank_index)
        dump_label = (
            f"{dump_bank} (index {bank_index})"
            if dump_bank
            else f"index {bank_index}"
        )
        raise PresetDumpError(
            f"{path.name}: dump bank index is {dump_label} but filename bank "
            f"{bank!r} expects index {expected_index}"
        )

    bank_lo = raw[BANK_WORD_OFFSETS[1]]
    mirror = raw[BANK_MIRROR_OFFSET]
    if mirror != bank_lo:
        raise PresetDumpError(
            f"{path.name}: bank mirror offset {BANK_MIRROR_OFFSET} "
            f"({mirror:02X}) != bank low nibble offset {BANK_WORD_OFFSETS[1]} "
            f"({bank_lo:02X})"
        )

    return {
        "file": path.name,
        "stem": path.stem,
        "bank": bank,
        "preset": preset,
        "name_field": name_check.get("name_field") or preset,
        "name_matches_preset": bool(name_check.get("name_matches_preset")),
        "name_bytes_match": True,
        "bank_index": bank_index,
        "program_slot": program_slot_from_raw(raw),
        "bytes": {
            "88": f"{raw[BANK_WORD_OFFSETS[0]]:02X}",
            "89": f"{raw[BANK_WORD_OFFSETS[1]]:02X}",
            "90": f"{raw[PROGRAM_WORD_OFFSETS[0]]:02X}",
            "91": f"{raw[PROGRAM_WORD_OFFSETS[1]]:02X}",
            str(BANK_MIRROR_OFFSET): f"{mirror:02X}",
        },
        "bank_mirror": mirror,
        "bank_mirror_matches": True,
    }


def is_meta_folder(name: str) -> bool:
    """Folders starting with '_' are meta captures, not parameter series."""
    return name.startswith("_")


def parse_preset_stem(stem: str) -> tuple[str, str]:
    """Split `<bank name>.<preset name>` on the first dot."""
    bank, sep, preset = stem.partition(".")
    if not sep or not bank.strip() or not preset.strip():
        raise ValueError(
            f"expected '<bank>.<preset>' filename stem, got {stem!r}"
        )
    return bank.strip(), preset.strip()


def expected_name_bytes(preset: str) -> bytes:
    """ASCII program-name field for a preset: space-padded to NAME_LENGTH."""
    encoded = preset.encode("ascii")
    if len(encoded) > NAME_LENGTH:
        raise ValueError(
            f"preset name longer than {NAME_LENGTH} bytes: {preset!r}"
        )
    return encoded.ljust(NAME_LENGTH, b" ")


def check_name_bytes(raw: bytes, preset: str) -> dict[str, Any]:
    """Compare SysEx offsets 8-87 to the space-padded filename preset.

    Returns a dict with match flags and, on failure, the first differing offset.
    """
    if len(raw) < NAME_OFFSET + NAME_LENGTH:
        return {
            "name_bytes_match": False,
            "name_field": None,
            "error": f"SysEx shorter than name field ({len(raw)} bytes)",
        }
    actual = raw[NAME_OFFSET : NAME_OFFSET + NAME_LENGTH]
    expected_candidates = [expected_name_bytes(preset)]
    alias = NAME_FIELD_ALIASES.get(preset)
    if alias:
        expected_candidates.append(expected_name_bytes(alias))
    name_field = actual.decode("ascii", errors="replace").rstrip(" ")
    if any(actual == exp for exp in expected_candidates):
        return {
            "name_bytes_match": True,
            "name_field": name_field,
            "name_matches_preset": name_field == preset,
        }
    # Find first mismatch for diagnostics (primary filename spelling).
    expected = expected_candidates[0]
    mismatch_at = next(
        (i for i, (a, b) in enumerate(zip(actual, expected)) if a != b),
        min(len(actual), len(expected)),
    )
    mismatch: dict[str, Any] = {
        "offset": NAME_OFFSET + mismatch_at,
        "expected_byte": f"{expected[mismatch_at]:02X}"
        if mismatch_at < len(expected)
        else None,
        "actual_byte": f"{actual[mismatch_at]:02X}"
        if mismatch_at < len(actual)
        else None,
        "expected_name": preset,
        "actual_name": name_field,
        "expected_prefix_hex": expected[:32].hex(" "),
        "actual_prefix_hex": actual[:32].hex(" "),
    }
    if alias:
        mismatch["known_alias"] = alias
        mismatch["note"] = (
            "Factory name uses known alias spelling; see docs/manual-notes.md"
        )
    return {
        "name_bytes_match": False,
        "name_field": name_field,
        "name_matches_preset": name_field == preset,
        "name_mismatch": mismatch,
    }


def find_names_folder(sysex_root: Path) -> Path | None:
    """Return ``sysex/prog/presets`` (or legacy ``_presets``) if it contains dumps."""
    root = Path(sysex_root)
    from ..paths import LEGACY_PRESETS_DIR, prog_presets_root

    for folder in (
        prog_presets_root(root),
        root / LEGACY_PRESETS_DIR,
    ):
        if not folder.is_dir():
            continue
        syx = list(folder.glob("*.syx")) + list(folder.glob("*.SYX"))
        if syx:
            return folder
    return None


def analyze_names_folder(folder: Path) -> dict[str, Any]:
    """Diff factory/user preset dumps to locate name / bank / program fields."""
    folder = Path(folder).resolve()
    paths = sorted(
        {p.resolve() for p in list(folder.glob("*.syx")) + list(folder.glob("*.SYX"))},
        key=lambda p: p.name.lower(),
    )
    if len(paths) < 2:
        raise ValueError(f"need at least 2 .syx dumps in {folder}")

    dumps: list[dict[str, Any]] = []
    for path in paths:
        raw = path.read_bytes()
        row = validate_preset_dump(path, raw)
        dumps.append(row)

    blobs = [p.read_bytes() for p in paths]
    length = len(blobs[0])
    changing = _changing_offsets(blobs)

    checksum_start = length - 1 - CHECKSUM_NIBBLE_COUNT
    checksum_offsets = list(range(checksum_start, length - 1))
    name_offsets = list(range(NAME_OFFSET, NAME_OFFSET + NAME_LENGTH))

    name_ok = all(d.get("name_bytes_match") for d in dumps)
    name_mismatches = [d for d in dumps if not d.get("name_bytes_match")]
    mirror_ok = all(d["bank_mirror_matches"] for d in dumps)

    bank_map = _fit_bank_index(dumps)
    program_map = _fit_program_slots(dumps)
    hint_notes = _bank_hint_notes(bank_map)

    identity_offsets = sorted(
        set(BANK_WORD_OFFSETS)
        | set(PROGRAM_WORD_OFFSETS)
        | {BANK_MIRROR_OFFSET}
    )
    sound_offsets = [
        off
        for off in changing
        if off not in identity_offsets
        and off not in checksum_offsets
        and off not in name_offsets
        and off not in (146, 147)
    ]

    confidence = "high" if name_ok and mirror_ok and bank_map["consistent"] else "medium"
    if not program_map["has_multi_slot_bank"]:
        if confidence == "high" and not program_map["consistent"]:
            confidence = "medium"
    if name_mismatches:
        confidence = "low"

    matched = sum(1 for d in dumps if d.get("name_bytes_match"))
    summary_parts = [
        f"Program name bytes at offsets {NAME_OFFSET}-{NAME_OFFSET + NAME_LENGTH - 1} "
        f"match filename preset (ASCII space-padded) in {matched}/{len(dumps)} dumps.",
        f"Bank index at {BANK_WORD_OFFSETS[0]}-{BANK_WORD_OFFSETS[1]} "
        f"(nibble_hilo); mirrored at {BANK_MIRROR_OFFSET}.",
        f"Program slot within bank at {PROGRAM_WORD_OFFSETS[0]}-{PROGRAM_WORD_OFFSETS[1]} "
        f"(nibble_hilo).",
    ]
    if name_mismatches:
        files = ", ".join(d["file"] for d in name_mismatches[:5])
        extra = f" (+{len(name_mismatches) - 5} more)" if len(name_mismatches) > 5 else ""
        summary_parts.append(
            f"NAME BYTE MISMATCH in {len(name_mismatches)} dump(s): {files}{extra}."
        )
    if hint_notes:
        summary_parts.append(" ".join(hint_notes))

    result: dict[str, Any] = {
        "kind": "presets",
        "parameter": LEGACY_PRESETS_DIR,
        "folder": str(folder),
        "dump_count": len(dumps),
        "message_length": length,
        "naming_convention": "<bank name>.<preset name>.syx",
        "fields": {
            "program_name": {
                "offsets": name_offsets[:1] + [name_offsets[-1]],
                "offset_range": f"{NAME_OFFSET}-{NAME_OFFSET + NAME_LENGTH - 1}",
                "encoding": "ascii_space_padded",
                "length": NAME_LENGTH,
                "matches_filename_preset": name_ok,
                "bytes_match_count": matched,
                "bytes_mismatch_count": len(name_mismatches),
                "notes": (
                    "ASCII program name only - bank name is not stored in this field. "
                    "Each dump's bytes[8:88] are checked against the filename preset "
                    "half, encoded as ASCII and space-padded to 80 bytes."
                ),
            },
            "bank_index": {
                "offsets": list(BANK_WORD_OFFSETS),
                "encoding": "nibble_hilo",
                "mirror_offset": BANK_MIRROR_OFFSET,
                "mirror_matches": mirror_ok,
                "map": bank_map["map"],
                "consistent": bank_map["consistent"],
                "notes": (
                    "Factory/user bank select. Low nibble at offset 89 carries the "
                    f"index in this corpus (offset 88 stayed 00). Offset "
                    f"{BANK_MIRROR_OFFSET} always equals offset 89."
                ),
            },
            "program_slot": {
                "offsets": list(PROGRAM_WORD_OFFSETS),
                "encoding": "nibble_hilo",
                "by_bank": program_map["by_bank"],
                "consistent": program_map["consistent"],
                "has_multi_slot_bank": program_map["has_multi_slot_bank"],
                "notes": (
                    "Slot within the current bank (not a global program number). "
                    "Halls samples: Large Hall=0, Medium Hall=1, Small Hall=2, "
                    "Large & Near=3 (factory list order). Rooms uses contiguous "
                    "slots 0–35 (Long Wood Room at 35)."
                ),
            },
        },
        "changing_offsets": changing,
        "classification": {
            "identity_offsets": identity_offsets,
            "name_offsets_touched": [o for o in changing if o in name_offsets],
            "checksum_offsets": checksum_offsets,
            "secondary_offsets": [o for o in (146, 147) if o in changing],
            "sound_parameter_offsets": sound_offsets,
        },
        "bank_hint_notes": hint_notes,
        "name_mismatches": [
            {
                "file": d["file"],
                "preset": d["preset"],
                "name_field": d.get("name_field"),
                "mismatch": d.get("name_mismatch"),
            }
            for d in name_mismatches
        ],
        "hypothesis": {
            "confidence": confidence,
            "summary": " ".join(summary_parts),
        },
        "dumps": dumps,
    }
    return result


def write_names_analysis(result: dict[str, Any], path: Path | None = None) -> Path:
    if path is None:
        path = Path(result["folder"]) / "analysis.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return path


def _fit_bank_index(dumps: list[dict[str, Any]]) -> dict[str, Any]:
    """Each bank name should map to exactly one encoded bank index."""
    by_bank: dict[str, set[int]] = defaultdict(set)
    for d in dumps:
        by_bank[d["bank"]].add(d["bank_index"])
    mapping = {bank: sorted(vals)[0] for bank, vals in by_bank.items()}
    consistent = all(len(vals) == 1 for vals in by_bank.values())
    if len(set(mapping.values())) != len(mapping):
        consistent = False
    return {
        "map": dict(bank_map_sorted_by_index(mapping)),
        "consistent": consistent,
    }


def _fit_program_slots(dumps: list[dict[str, Any]]) -> dict[str, Any]:
    """Within each bank, preset names should map 1:1 to program slots."""
    by_bank: dict[str, dict[str, int]] = defaultdict(dict)
    consistent = True
    has_multi = False
    for d in dumps:
        bank = d["bank"]
        preset = d["preset"]
        slot = d["program_slot"]
        if preset in by_bank[bank] and by_bank[bank][preset] != slot:
            consistent = False
        by_bank[bank][preset] = slot
    for _bank, presets in by_bank.items():
        if len(presets) >= 2:
            has_multi = True
        if len(set(presets.values())) != len(presets):
            consistent = False
    return {
        "by_bank": {
            bank: dict(sorted(presets.items(), key=lambda kv: kv[1]))
            for bank, presets in sorted(by_bank.items())
        },
        "consistent": consistent,
        "has_multi_slot_bank": has_multi,
    }


def _bank_hint_notes(bank_map: dict[str, Any]) -> list[str]:
    notes: list[str] = []
    for bank, idx in (bank_map.get("map") or {}).items():
        hinted = HINT_BANK_INDEX.get(bank)
        if hinted is None:
            notes.append(f"Bank {bank!r} index {idx} has no catalog hint.")
        elif hinted != idx:
            notes.append(
                f"Bank {bank!r}: dump index {idx} differs from hint {hinted}."
            )
    return notes


def _changing_offsets(blobs: list[bytes]) -> list[int]:
    length = len(blobs[0])
    changing = []
    for i in range(length):
        if len({b[i] for b in blobs}) > 1:
            changing.append(i)
    return changing
