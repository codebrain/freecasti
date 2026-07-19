"""Sync specification/ assets into web-ui/public/ (downstream mirror)."""

from __future__ import annotations

import base64
import json
import shutil
from pathlib import Path

from m7_sysex.prog.algorithms import PROG_ALGORITHM_CONSTRAINTS
from m7_sysex.prog.menus import hardware_menu_order
from m7_sysex.prog.register_blob import runtime_reg_blob

_RUNTIME_FIELD_KEYS = (
    "id",
    "label",
    "parameter",
    "offsets",
    "start",
    "end",
    "encoding",
    "kind",
    "size",
)
_IDENTITY_FIELD_IDS = frozenset(
    {
        "program_name",
        "program_name_pad",
        "register_basis_blob",
        "bank_index",
        "program_slot",
        "bank_index_mirror",
        "register_bank",
        "register",
    }
)

# Preset catalog column order (differs from hardware menu order).
PROG_PARAM_ORDER = (
    "reverb time",
    "size",
    "predelay",
    "diffusion",
    "density",
    "modulation",
    "early select",
    "early to reverb mix",
    "delay time",
    "delay level",
    "delay modulation",
    "rolloff",
    "early rolloff",
    "vlf cut",
    "lf rt crossover",
    "lf rt multiply",
    "hf rt crossover",
    "hf rt multiply",
)

_ENCODING_SHORT = {
    "nibble_hilo": "nh",
    "raw_u8": "u8",
    "nibble_lohi": "nl",
    "ascii_space_padded": "as",
    "raw_bytes": "rb",
}


def _compact_json(data: object) -> str:
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False) + "\n"


def _runtime_spec(spec: dict) -> dict:
    """Fields required at runtime: controls (value_map) + program identity."""
    fields: list[dict] = []
    for field in spec["fields"]:
        if field["id"] not in _IDENTITY_FIELD_IDS and not field.get("value_map"):
            continue
        slim = {k: field[k] for k in _RUNTIME_FIELD_KEYS if k in field}
        if field.get("value_map"):
            slim["value_map"] = field["value_map"]
        fields.append(slim)
    return {
        "format": spec["format"],
        "version": spec["version"],
        "message_length": spec["message_length"],
        "fields": fields,
    }


def _compact_value_map(value_map: dict) -> list[list]:
    return [[entry["encoded"], entry["label"]] for entry in value_map["entries"]]


def _compact_field(field: dict) -> dict:
    compact: dict = {"id": field["id"], "s": field["start"]}
    encoding = field.get("encoding")
    if encoding:
        short = _ENCODING_SHORT.get(encoding)
        if short:
            compact["e"] = short
    if field.get("parameter"):
        compact["p"] = field["parameter"]
    if field.get("size"):
        compact["z"] = field["size"]
    if field.get("value_map"):
        compact["m"] = _compact_value_map(field["value_map"])
    return compact


def _compact_runtime_spec(spec: dict) -> dict:
    runtime = _runtime_spec(spec)
    return {
        "n": runtime["message_length"],
        "f": [_compact_field(field) for field in runtime["fields"]],
    }


def _bank_names(presets: list[dict]) -> list[str]:
    by_index: dict[int, str] = {}
    for entry in presets:
        by_index[entry["bank_index"]] = entry["bank"]
    return [by_index[i] for i in sorted(by_index)]


def _compact_preset_catalog(presets: dict) -> dict:
    """Minimal preset table: banks + param columns + tuple rows."""
    rows: list[list] = []
    for entry in presets["presets"]:
        encoded = [
            entry["parameters"][name]["encoded"] for name in PROG_PARAM_ORDER
        ]
        rows.append(
            [
                entry["bank_index"],
                entry["program_slot"],
                entry["name_field"],
                *encoded,
            ]
        )
    return {
        "banks": _bank_names(presets["presets"]),
        "params": list(PROG_PARAM_ORDER),
        "presets": rows,
        "algorithms": PROG_ALGORITHM_CONSTRAINTS,
    }


def _load_serialize_skeletons(spec_root: Path) -> dict[str, str]:
    path = spec_root / "web_serialize_skeletons.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    prog = raw["prog"]
    system = raw["system"]
    for key, entry in ("prog", prog), ("system", system):
        b64 = entry.get("b64")
        length = entry.get("message_length")
        if not isinstance(b64, str) or not isinstance(length, int):
            raise ValueError(f"web_serialize_skeletons.json: invalid {key} entry")
        if len(base64.standard_b64decode(b64)) != length:
            raise ValueError(
                f"web_serialize_skeletons.json: {key} b64 length != message_length"
            )
    return {"p": prog["b64"], "s": system["b64"]}


def _load_prog_ui_state(repo_root: Path) -> dict | None:
    path = repo_root / "sysex" / "prog" / "menus" / "prog_ui_state.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _runtime_bundle(
    prog_spec: dict,
    system_spec: dict,
    presets_full: dict,
    *,
    serialize_skeletons: dict[str, str],
    prog_ui: dict | None = None,
) -> dict:
    """Single browser runtime payload: compact prog/system specs + preset catalog."""
    bundle = {
        "prog": _compact_runtime_spec(prog_spec),
        "system": _compact_runtime_spec(system_spec),
        "presets": _compact_preset_catalog(presets_full),
        "tpl": serialize_skeletons,
        "reg_blob": runtime_reg_blob(),
    }
    if prog_ui is not None:
        bundle["prog_ui"] = prog_ui
        bundle["menu_order"] = hardware_menu_order()
    return bundle


_LEGACY_PUBLIC_DIRS = ("spec", "presets", "templates")
_LEGACY_PUBLIC_FILES = ("sync-manifest.json",)


def _prune_legacy_public(public: Path) -> None:
    """Drop obsolete public/ trees and files superseded by m7-runtime.json."""
    for name in _LEGACY_PUBLIC_DIRS:
        tree = public / name
        if tree.exists():
            shutil.rmtree(tree)
    for name in _LEGACY_PUBLIC_FILES:
        stale = public / name
        if stale.is_file():
            stale.unlink()


def sync_web_ui_assets(repo_root: Path) -> list[Path]:
    """Copy machine specs and presets into web-ui/public/m7-runtime.json."""
    repo_root = repo_root.resolve()
    web_root = repo_root / "web-ui"
    public = web_root / "public"
    spec_root = repo_root / "specification"
    serialize_skeletons = _load_serialize_skeletons(spec_root)

    prog_spec = json.loads(
        (spec_root / "prog" / "m7_program_dump.spec.json").read_text(encoding="utf-8")
    )
    system_spec = json.loads(
        (spec_root / "system" / "m7_system_dump.spec.json").read_text(encoding="utf-8")
    )
    presets_full = json.loads(
        (spec_root / "prog" / "presets" / "presets.json").read_text(encoding="utf-8")
    )
    prog_ui = _load_prog_ui_state(repo_root)

    written: list[Path] = []

    def write_json(path: Path, data: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_compact_json(data), encoding="utf-8")
        written.append(path)

    write_json(
        public / "m7-runtime.json",
        _runtime_bundle(
            prog_spec,
            system_spec,
            presets_full,
            serialize_skeletons=serialize_skeletons,
            prog_ui=prog_ui,
        ),
    )

    param_manifest = _build_param_manifest(prog_spec, system_spec)
    gen_dir = web_root / "src" / "generated"
    gen_dir.mkdir(parents=True, exist_ok=True)
    param_manifest_path = gen_dir / "param-manifest.json"
    param_manifest_path.write_text(_compact_json(param_manifest), encoding="utf-8")
    written.append(param_manifest_path)

    _prune_legacy_public(public)

    return written


def _build_param_manifest(prog_spec: dict, system_spec: dict) -> dict:
    def summarize(fields: list[dict]) -> list[dict]:
        out: list[dict] = []
        for field in fields:
            if not field.get("value_map") and field.get("kind") not in ("string", "meta"):
                if field["id"] not in ("bank_index", "program_slot", "bank_index_mirror"):
                    continue
            entry = {
                "id": field["id"],
                "label": field.get("label") or field["id"],
                "parameter": field.get("parameter"),
                "kind": field.get("kind"),
                "encoding": field.get("encoding"),
            }
            if field.get("description"):
                entry["description"] = field["description"]
            if field.get("value_map"):
                entry["enum_id"] = field["value_map"]["enum_id"]
            out.append(entry)
        return out

    return {
        "prog": summarize(prog_spec["fields"]),
        "system": summarize(system_spec["fields"]),
    }
