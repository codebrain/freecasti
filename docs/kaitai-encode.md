# Kaitai encode / serialize

Kaitai Struct generates **decoders** from `specification/**/*.ksy`. It does not emit
serializers for the Python target. To build or edit M7 SysEx messages from parsed
objects, use the helpers in `m7_sysex` described here.

## Overview

| Layer | Module | Role |
|-------|--------|------|
| Frame + checksum | [`frame.py`](../src/m7_sysex/frame.py) | CRC-16/ARC, cover ranges, read/write checksum nibbles |
| Parameter bytes | [`encodings.py`](../src/m7_sysex/encodings.py) | `encode_at_offsets` / `decode_at_offsets` for one field |
| Full message | [`kaitai_encode.py`](../src/m7_sysex/kaitai_encode.py) | `serialize_parsed_dump` from a Kaitai root object + `.spec.json` fields |
| Spec | `specification/prog/m7_program_dump.{ksy,spec.json}` | Field offsets, encodings, enum tables |
| Spec | `specification/system/m7_system_dump.{ksy,spec.json}` | Shorter 77-byte system layout |

Typical workflow:

1. Compile the `.ksy` (tests do this ephemerally; see [development.md](development.md)).
2. `parsed = M7ProgramDump.from_bytes(raw)` (generated class name).
3. Edit fields on `parsed` if needed (enum members, nibble wrappers, name string).
4. `encoded = serialize_parsed_dump(parsed, fields)` — checksum is **always** recomputed.

## Checksums

Program and system dumps share **CRC-16/ARC** over a fixed byte range, packed as
four high-nibble-first SysEx data bytes before `F7`.

```python
from m7_sysex.frame import (
    program_dump_checksum,      # compute only
    write_program_dump_checksum,  # write into bytearray in place
    verify_program_dump_checksum,
    system_dump_checksum,
    write_system_dump_checksum,
    verify_system_dump_checksum,
)
```

- **Program dump:** cover is offsets `8 .. checksum_start` (16-byte name +
  64-byte register basis blob + payload). Checksum cover is unchanged.
- **System dump:** cover is offsets `8 .. 71` (64 payload nibbles).

After changing any covered byte, call `write_program_dump_checksum(buf)` or
`write_system_dump_checksum(buf)` before sending the message.

## Single-parameter encode

For docs and patch tools that only touch one parameter’s offsets:

```python
from m7_sysex.encodings import decode_at_offsets, encode_at_offsets

# nibble_hilo at offsets 100-101 (e.g. reverb time)
wire = encode_at_offsets(70, "nibble_hilo", n_offsets=2)  # -> (4, 6)
buf[100], buf[101] = wire
write_program_dump_checksum(buf)
```

`encode_at_offsets` is the inverse of `decode_at_offsets` for `raw_u8`,
`nibble_hilo`, `nibble_lohi`, `midi14_be`, `midi14_le`, and `raw_bytes`.

## Full-message serialize (with Kaitai parsed objects)

```python
import json
from pathlib import Path

from m7_sysex.kaitai_encode import serialize_parsed_dump

# fields list from the committed machine spec (same layout Kaitai compiled)
fields = json.loads(
    Path("specification/prog/m7_program_dump.spec.json").read_text()
)["fields"]

# parsed = <your compiled M7ProgramDump instance>
encoded = serialize_parsed_dump(parsed, fields, system=False)
```

`field_wire_bytes(parsed, field)` (same module) maps one Kaitai field back to
on-wire bytes: fixed `contents`, ASCII name, `u1` enums, and `*_encoded` nibble
wrappers.

The checksum field in the spec is skipped during field copy; `serialize_parsed_dump`
fills it via `write_*_dump_checksum`.

## Tests

| File | What it checks |
|------|----------------|
| `tests/test_encodings.py` | `encode_at_offsets` ↔ `decode_at_offsets` |
| `tests/test_frame.py` | CRC vectors, `write_program_dump_checksum` |
| `tests/test_kaitai_encode.py` | Parse → serialize → byte-identical; corrupt checksum repair |
| `tests/test_kaitai_roundtrip.py` | Per-field wire extract vs raw (decode-side layout) |

**Encode corpus tests** (`test_prog_serialize_roundtrip_corpus`,
`test_system_serialize_roundtrip_corpus`) are marked `slow` and skipped in the
default pytest run. Run them with:

```bash
python -m pytest tests/test_kaitai_encode.py -q -m slow
# or full suite including slow:
python -m pytest tests -q -o addopts=
```

## Limitations

- Serialization follows the committed `.spec.json` layout. Fields marked unknown
  in the byte map are not magically inferred; copy them from a template dump or
  parse an existing message first.
- Kaitai Python returns bare `int` for out-of-enum `u1` values on read; on write,
  `field_wire_bytes` emits that integer as a single byte.
- Building a message **from scratch** without parsing a template still requires
  valid values for structural/meta fields (bank index, slot, display, etc.).

## Web UI (TypeScript)

The browser editor in [`web-ui/`](../web-ui/) mirrors the Python encode path in
`web-ui/src/sysex/` (`serialize.ts`, `encodings.ts`, `frame.ts`). It loads
compact specs from `public/m7-runtime.json` (synced by `python run.py`) and uses
Kaitai-generated parsers under `src/generated/sysex-parsers/` for the debug panel decode
view only — live editing patches bytes via the spec field tables, not by
re-serializing Kaitai objects.
