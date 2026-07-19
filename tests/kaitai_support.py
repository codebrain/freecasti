"""Helpers for compiling Kaitai specs in tests (output stays in temp/cache)."""

from __future__ import annotations

import importlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from enum import Enum
from pathlib import Path
from typing import Any
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parents[1]
PROG_KSY = ROOT / "specification" / "prog" / "m7_program_dump.ksy"
SYSTEM_KSY = ROOT / "specification" / "system" / "m7_system_dump.ksy"
KAITAI_COMPILER_VERSION = "0.10"
KAITAI_COMPILER_URL = (
    "https://github.com/kaitai-io/kaitai_struct_compiler/releases/download/"
    f"{KAITAI_COMPILER_VERSION}/kaitai-struct-compiler-{KAITAI_COMPILER_VERSION}.zip"
)

_ENUM_LINE = re.compile(
    r"^\s+(?P<enc>-?\d+):\s+(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)(?:\s+#\s+(?P<label>.+))?$"
)


def ensure_kaitai_compiler() -> str:
    """Return a kaitai-struct-compiler executable, downloading 0.10 if needed."""
    found = shutil.which("kaitai-struct-compiler")
    if found:
        return found

    cache_root = (
        ROOT / ".pytest_cache" / f"kaitai-struct-compiler-{KAITAI_COMPILER_VERSION}"
    )
    if sys.platform == "win32":
        candidate = cache_root / "bin" / "kaitai-struct-compiler.bat"
    else:
        candidate = cache_root / "bin" / "kaitai-struct-compiler"
    if candidate.is_file():
        return str(candidate)

    zip_path = cache_root.with_suffix(".zip")
    cache_root.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(KAITAI_COMPILER_URL, zip_path)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(cache_root.parent)
    zip_path.unlink(missing_ok=True)

    if not candidate.is_file():
        raise RuntimeError(f"kaitai-struct-compiler not found at {candidate}")
    return str(candidate)


def kaitai_root_class_name(ksy_stem: str) -> str:
    """Map ``m7_program_dump`` → ``M7ProgramDump`` (Kaitai Python naming)."""
    return "".join(part[:1].upper() + part[1:] for part in ksy_stem.split("_"))


def enum_class_name(enum_id: str) -> str:
    """Map ``diffusion_values`` → ``DiffusionValues`` (generated Python name)."""
    stem = enum_id.removesuffix("_values") if enum_id.endswith("_values") else enum_id
    return "".join(part.capitalize() for part in stem.split("_")) + "Values"


def compile_ksy(ksy_path: Path, out_dir: Path, compiler: str, target: str = "python") -> Path:
    """Compile one ``.ksy`` file under ``out_dir``."""
    out_dir.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [compiler, "-t", target, "--outdir", str(out_dir), str(ksy_path)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"kaitai-struct-compiler failed for {ksy_path} ({target}):\n"
            f"{proc.stdout}\n{proc.stderr}"
        )
    if target == "python":
        py_path = out_dir / f"{ksy_path.stem}.py"
        if not py_path.is_file():
            raise RuntimeError(f"expected generated module at {py_path}")
        return py_path
    return out_dir


def compile_ksy_to_python(ksy_path: Path, out_dir: Path, compiler: str) -> Path:
    return compile_ksy(ksy_path, out_dir, compiler, target="python")


class KaitaiCompileCache:
    """Compile each ``.ksy`` path at most once per pytest session."""

    def __init__(self, compiler: str) -> None:
        self.compiler = compiler
        self.out_root: Path | None = None
        self._compiled: set[tuple[str, str]] = set()
        self._parsers: dict[str, type] = {}
        self._sys_paths: set[str] = set()

    @staticmethod
    def _key(ksy_path: Path, target: str) -> tuple[str, str]:
        return (str(ksy_path.resolve()), target)

    def compile_count(self, ksy_path: Path, target: str = "python") -> int:
        """Return 1 if ``ksy_path`` was compiled for ``target``, else 0."""
        return int(self._key(ksy_path, target) in self._compiled)

    def compile_target(self, ksy_path: Path, out_dir: Path, target: str) -> Path:
        """Compile ``ksy_path`` once for ``target``; return the output path/dir."""
        key = self._key(ksy_path, target)
        if key in self._compiled:
            if target == "python":
                return out_dir / f"{ksy_path.stem}.py"
            return out_dir
        result = compile_ksy(ksy_path, out_dir, self.compiler, target=target)
        self._compiled.add(key)
        return result

    def parser_for(self, ksy_path: Path, out_dir: Path) -> type:
        """Return the root parser class, compiling the ``.ksy`` at most once."""
        ksy_path = ksy_path.resolve()
        cache_key = str(ksy_path)
        if cache_key in self._parsers:
            return self._parsers[cache_key]

        self.compile_target(ksy_path, out_dir, "python")
        out_str = str(out_dir.resolve())
        if out_str not in self._sys_paths:
            sys.path.insert(0, out_str)
            self._sys_paths.add(out_str)

        module = importlib.import_module(ksy_path.stem)
        parser_cls = getattr(module, kaitai_root_class_name(ksy_path.stem))
        self._parsers[cache_key] = parser_cls
        return parser_cls


def load_spec(spec_json: Path) -> dict[str, Any]:
    return json.loads(spec_json.read_text(encoding="utf-8"))


def load_spec_fields(spec_json: Path) -> list[dict[str, Any]]:
    return list(load_spec(spec_json)["fields"])


def fields_with_value_map(fields: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [f for f in fields if f.get("value_map")]


def fields_by_parameter(fields: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for field in fields:
        param = field.get("parameter")
        if param:
            out.setdefault(param, []).append(field)
    return out


def parse_ksy_enums(ksy_text: str) -> dict[str, dict[int, tuple[str, str | None]]]:
    """Parse ``enums:`` blocks from a ``.ksy`` file."""
    enums: dict[str, dict[int, tuple[str, str | None]]] = {}
    in_enums = False
    current: str | None = None
    for line in ksy_text.splitlines():
        if line == "enums:":
            in_enums = True
            continue
        if not in_enums:
            continue
        if line and not line.startswith(" "):
            break
        if line.startswith("types:"):
            break
        if line.startswith("  ") and not line.startswith("    ") and line.strip().endswith(":"):
            current = line.strip()[:-1]
            enums[current] = {}
            continue
        if current is None:
            continue
        match = _ENUM_LINE.match(line)
        if match:
            label = match.group("label")
            enums[current][int(match.group("enc"))] = (match.group("name"), label)
    return enums


def value_maps_from_fields(
    fields: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """``enum_id`` → ``value_map`` dict from machine spec fields."""
    out: dict[str, dict[str, Any]] = {}
    for field in fields:
        value_map = field.get("value_map")
        if not value_map:
            continue
        enum_id = str(value_map["enum_id"])
        out[enum_id] = value_map
    return out


def assert_spec_json_ksy_value_maps_agree(
    spec_fields: list[dict[str, Any]],
    ksy_text: str,
) -> None:
    """``.spec.json`` value maps must match ``.ksy`` enum tables."""
    ksy_enums = parse_ksy_enums(ksy_text)
    for field in fields_with_value_map(spec_fields):
        value_map = field["value_map"]
        enum_id = value_map["enum_id"]
        assert enum_id in ksy_enums, f"missing enum {enum_id} in .ksy for {field['id']}"
        ksy_entries = ksy_enums[enum_id]
        for entry in value_map["entries"]:
            enc = int(entry["encoded"])
            name = str(entry["name"])
            label = str(entry.get("label") or name)
            assert enc in ksy_entries, f"{enum_id}: missing encoded {enc} in .ksy"
            ksy_name, ksy_label = ksy_entries[enc]
            assert ksy_name == name, f"{enum_id}[{enc}] name {ksy_name!r} != {name!r}"
            assert ksy_label == label, (
                f"{enum_id}[{enc}] label {ksy_label!r} != {label!r}"
            )


def assert_compiled_enums_match_value_maps(
    parser_cls: type,
    value_maps: dict[str, dict[str, Any]],
) -> None:
    """Generated Python ``Enum`` classes mirror ``value_map`` tables."""
    for enum_id, value_map in value_maps.items():
        cls = getattr(parser_cls, enum_class_name(enum_id), None)
        assert cls is not None, f"missing generated enum class for {enum_id}"
        by_value = {member.value: member for member in cls}
        for entry in value_map["entries"]:
            enc = int(entry["encoded"])
            assert enc in by_value, f"{enum_id}: encoded {enc} missing from Python enum"


from m7_sysex.kaitai_encode import field_wire_bytes
def encoded_int_from_field(parsed: Any, field: dict[str, Any]) -> int:
    """Return the decoded integer for a mapped parameter field."""
    val = getattr(parsed, field["id"])
    if isinstance(val, Enum):
        return int(val.value)
    if hasattr(val, "hi_nibble"):
        inner = val.value
        if isinstance(inner, Enum):
            return int(inner.value)
        return (int(val.hi_nibble) << 4) | int(val.lo_nibble)
    if hasattr(val, "value"):
        inner = val.value
        if isinstance(inner, Enum):
            return int(inner.value)
        return int(inner)
    return int(val)


def field_parsed_value(parsed: Any, field: dict[str, Any]) -> Any:
    """Return the parsed field value (enum member or nibble wrapper)."""
    return getattr(parsed, field["id"])


def assert_message_roundtrip(
    parsed: Any,
    raw: bytes,
    fields: list[dict[str, Any]],
    *,
    path: Path | str | None = None,
) -> None:
    """Every spec field must reproduce the source bytes at its offsets."""
    label = f" ({path})" if path else ""
    for field in fields:
        fid = field["id"]
        start = int(field["start"])
        end = int(field["end"])
        wire = field_wire_bytes(parsed, field)
        expected = raw[start : end + 1]
        assert wire == expected, (
            f"{fid}{label}: parsed {wire!r} != raw {expected!r} "
            f"at offsets [{start}, {end}]"
        )


def assert_checksum_matches_native(
    parsed: Any,
    raw: bytes,
    *,
    system: bool = False,
) -> None:
    """Kaitai checksum field must match the native CRC packer."""
    from m7_sysex.frame import program_dump_checksum, system_dump_checksum

    expected = (
        system_dump_checksum(raw) if system else program_dump_checksum(raw)
    )
    assert bytes(parsed.checksum) == expected


def split_sysex_messages(data: bytes) -> list[bytes]:
    """Split a file that may contain multiple F0…F7 messages."""
    msgs: list[bytes] = []
    i = 0
    while i < len(data):
        if data[i] == 0xF0:
            j = i + 1
            while j < len(data) and data[j] != 0xF7:
                j += 1
            if j < len(data):
                msgs.append(data[i : j + 1])
                i = j + 1
                continue
        i += 1
    return msgs
