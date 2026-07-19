import sys
from pathlib import Path

sys.path.insert(0, r"C:\m7\src")
sys.path.insert(0, r"C:\m7")
from tests.kaitai_support import ensure_kaitai_compiler, compile_ksy_to_python, PROG_KSY
from m7_sysex.frame import iter_sysex_messages
from m7_sysex.prog.register_blob import decode_register_blob, frame_blob, REGISTER_BLOB_FIELDS, register_name_codes

out = Path(r"C:\m7\.pytest_cache\tmp_blob_kaitai")
compile_ksy_to_python(PROG_KSY, out, ensure_kaitai_compiler())
sys.path.insert(0, str(out))
from m7_program_dump import M7ProgramDump  # noqa: E402
from enum import Enum  # noqa: E402

root = Path(r"C:\m7\sysex\prog\edit\registers")
n = 0
for p in sorted(root.rglob("*.syx")):
    for raw in iter_sysex_messages(p.read_bytes()):
        parsed = M7ProgramDump.from_bytes(raw)
        blob = parsed.register_basis_blob
        assert blob.is_register_basis, p
        basis = decode_register_blob(frame_blob(raw))
        codes = register_name_codes(frame_blob(raw))
        for i, code in enumerate(codes):
            v = getattr(blob, f"name_code_{i:02d}")
            v = v.value if isinstance(v, Enum) else v
            assert v == code, (p.name, i, v, code)
        for f in REGISTER_BLOB_FIELDS:
            if f.id in ("name", "tail"):
                continue
            v = getattr(blob, f.id)
            v = v.value if isinstance(v, Enum) else v
            assert v == basis.values[f.id], (p.name, f.id, v, basis.values[f.id])
        assert blob.tail_is_zero
        n += 1
# factory dump: guard false
fac = (Path(r"C:\m7\sysex\prog\presets") / "Halls.Large Hall.syx").read_bytes()
parsed = M7ProgramDump.from_bytes(fac)
assert not parsed.register_basis_blob.is_register_basis
# enum label check: stored capture reverb time 76 resolves to enum member
stored = (root / "samples" / "charset-b1s1-rt5s-stored.syx").read_bytes()
parsed = M7ProgramDump.from_bytes(stored)
rt = parsed.register_basis_blob.reverb_time
print("reverb_time instance:", rt, type(rt).__name__)
print("OK frames:", n)
