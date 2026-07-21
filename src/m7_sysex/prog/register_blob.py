"""Decode/encode the register basis blob (program-dump offsets 24-87).

Reg-backed hold-EDIT dumps reuse the factory space-pad region 24-87 as a
**bit-packed snapshot of the stored register**: the low nibble of each byte
(4 bits per byte, MSB first) forms a 256-bit stream holding the register
name (14 x 6-bit chars), a per-slot store-generation counter, and every
stored parameter value including the V2 delay block.

This table is the single source of truth for the blob layout: the generated
documentation page (``specification/prog/bytes/register-basis-blob.md``),
the Kaitai ``register_basis_blob`` type instances, the ``m7-runtime.json``
``reg_blob`` key, and the web-ui TypeScript decoder are all derived from it.

Witness captures (all under ``sysex/prog/edit/registers/``):

* ``fullsweep-rooms-studio-a.syx`` - 50 registers, layout + store counter
* ``samples/rooms-studio-a-b1s1-delay-edit.syx`` - counter bump, delay in
  payload only (stored before the delay was dialed in)
* ``samples/charset-b1s1-renamed.syx`` - name ``&123456789ABCD`` pins the
  6-bit charset codes 1-11
* ``samples/charset-b1s1-rt5s-unstored-edit.syx`` - payload shows a 5.0 s
  reverb-time edit while the blob keeps the stored value (blob != live edit)
* ``samples/charset-b1s1-rt5s-stored.syx`` - after storing, the blob updates
  and carries the delay block at bits 197-211 (level 15 / time 11 / mod 6)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..frame import (
    REGISTER_BASIS_BLOB_LENGTH,
    REGISTER_BASIS_BLOB_OFFSET,
)

BLOB_BIT_LENGTH = REGISTER_BASIS_BLOB_LENGTH * 4  # 256
REGISTER_NAME_LENGTH = 14
REGISTER_NAME_CHAR_BITS = 6

# Complete 6-bit charset: 0=space, 1='&', 2-11='0'-'9', 12-37='A'-'Z',
# 38-63='a'-'z'. Witnessed by samples/charset-b1s1-renamed.syx
# (register renamed to `&123456789ABCD`); only digit '0' = code 2 is
# inferred by continuity rather than directly witnessed.
REGISTER_NAME_CHARSET = (
    " &0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
)
INFERRED_CHARSET_CODES = frozenset({2})  # digit '0'

assert len(REGISTER_NAME_CHARSET) == 64


@dataclass(frozen=True)
class RegisterBlobField:
    """One field of the 256-bit register basis bitstream."""

    id: str
    label: str
    bit_offset: int
    bit_width: int
    # Spec field id of the live payload twin (None for blob-only fields).
    payload_field: str | None = None
    # Wire offsets of the payload twin in the 157-byte frame.
    payload_offsets: tuple[int, ...] = ()
    doc: str = ""

    @property
    def bit_end(self) -> int:
        return self.bit_offset + self.bit_width - 1


REGISTER_BLOB_FIELDS: tuple[RegisterBlobField, ...] = (
    RegisterBlobField(
        "name",
        "register name",
        0,
        84,
        "program_name",
        tuple(range(8, 22)),
        "14 characters x 6-bit code (see charset table); matches the ASCII "
        "name at offsets 8-21 on every corpus capture",
    ),
    RegisterBlobField(
        "pad",
        "zero pad",
        84,
        12,
        None,
        (),
        "Always 0 in witnessed captures",
    ),
    RegisterBlobField(
        "store_counter",
        "store-generation counter",
        96,
        5,
        None,
        (),
        "Increments each time the register slot is overwritten (wire offsets "
        "48-49). Fullsweep history: 3 for B0 R0-R2, 2 for B0 R3-B1 R1, 1 "
        "elsewhere; delay-edit re-store bumped B1 R1 to 3; the rename "
        "capture reads 5 (renaming stores twice); the rt5s store to B1 R0 "
        "reads 3",
    ),
    RegisterBlobField(
        "store_marker",
        "constant 001",
        101,
        3,
        None,
        (),
        "Constant 1 in every witnessed register capture",
    ),
    RegisterBlobField(
        "predelay", "predelay", 104, 8, "predelay", (104, 105)
    ),
    RegisterBlobField(
        "reverb_time", "reverb time", 112, 8, "reverb_time", (100, 101)
    ),
    RegisterBlobField(
        "diffusion", "diffusion", 120, 4, "diffusion", (106, 107)
    ),
    RegisterBlobField("density", "density", 124, 4, "density", (108, 109)),
    RegisterBlobField(
        "hf_rt_crossover",
        "hf rt crossover",
        128,
        6,
        "hf_rt_crossover",
        (116, 117),
    ),
    RegisterBlobField(
        "lf_rt_multiply",
        "lf rt multiply",
        134,
        6,
        "lf_rt_multiply",
        (118, 119),
    ),
    RegisterBlobField(
        "modulation", "modulation", 140, 4, "modulation", (110, 111)
    ),
    RegisterBlobField(
        "early_to_reverb_mix",
        "early to reverb mix",
        144,
        6,
        "early_to_reverb_mix",
        (124, 125),
    ),
    RegisterBlobField("vlf_cut", "vlf cut", 150, 5, "vlf_cut", (122, 123)),
    RegisterBlobField(
        "early_select", "early select", 155, 5, "early_select", (128, 129)
    ),
    RegisterBlobField(
        "engine_class",
        "engine/bank-class flag",
        160,
        2,
        "engine_bank_class_flag",
        (130,),
        "0 classic banks, 1 on `* 2` banks, 2 NonLin (same as payload 130)",
    ),
    RegisterBlobField(
        "early_rolloff",
        "early rolloff",
        162,
        7,
        "early_rolloff",
        (126, 127),
    ),
    RegisterBlobField("rolloff", "rolloff", 169, 7, "rolloff", (112, 113)),
    RegisterBlobField("size", "size", 176, 6, "size", (102, 103)),
    RegisterBlobField(
        "hf_rt_multiply",
        "hf rt multiply",
        182,
        5,
        "hf_rt_multiply",
        (114, 115),
    ),
    RegisterBlobField(
        "lf_rt_crossover",
        "lf rt crossover",
        187,
        5,
        "lf_rt_crossover",
        (120, 121),
    ),
    RegisterBlobField(
        "source_bank",
        "source factory bank",
        192,
        5,
        "bank_index_mirror",
        (136, 137),
        "Factory bank the register was stored from (same as payload 136–137)",
    ),
    RegisterBlobField(
        "delay_level",
        "delay level",
        197,
        4,
        "delay_level",
        (132, 133),
        "V2 delay block; located by samples/charset-b1s1-rt5s-stored.syx "
        "(reads 15). Zero when the register was stored without delay",
    ),
    RegisterBlobField(
        "delay_time",
        "delay time",
        201,
        7,
        "delay_time",
        (134, 135),
        "V2 delay block; stored capture reads 11",
    ),
    RegisterBlobField(
        "delay_modulation",
        "delay modulation",
        208,
        4,
        "delay_modulation",
        (138, 139),
        "V2 delay block; stored capture reads 6",
    ),
    RegisterBlobField(
        "tail",
        "zero tail",
        212,
        44,
        None,
        (),
        "Always 0 in witnessed captures",
    ),
)

# Fields carried in RegisterBasis.values (everything except the name).
SCALAR_FIELD_IDS: tuple[str, ...] = tuple(
    f.id for f in REGISTER_BLOB_FIELDS if f.id != "name"
)


def _check_field_table() -> None:
    covered = 0
    for field in REGISTER_BLOB_FIELDS:
        if field.bit_offset != covered:
            raise AssertionError(
                f"blob field gap/overlap at bit {covered} "
                f"({field.id} starts at {field.bit_offset})"
            )
        covered = field.bit_offset + field.bit_width
    if covered != BLOB_BIT_LENGTH:
        raise AssertionError(
            f"blob fields cover {covered} bits, expected {BLOB_BIT_LENGTH}"
        )


_check_field_table()

_FIELDS_BY_ID = {f.id: f for f in REGISTER_BLOB_FIELDS}


@dataclass(frozen=True)
class RegisterBasis:
    """Decoded register basis blob (stored register snapshot)."""

    name: str
    # Encoded integer per scalar field id (see REGISTER_BLOB_FIELDS).
    values: dict[str, int]

    @property
    def store_counter(self) -> int:
        return self.values["store_counter"]


def blob_kind(blob: bytes) -> str:
    """Classify a 64-byte 24-87 region.

    ``"factory_pad"``: all ``0x20`` spaces (factory / parameter-series
    dumps). ``"register_basis"``: nibble-packed stored-register snapshot.
    ``"unknown"``: anything else.
    """
    if len(blob) != REGISTER_BASIS_BLOB_LENGTH:
        raise ValueError(
            f"blob length {len(blob)} != {REGISTER_BASIS_BLOB_LENGTH}"
        )
    if all(b == 0x20 for b in blob):
        return "factory_pad"
    if all(b <= 0x0F for b in blob):
        return "register_basis"
    return "unknown"


def _blob_int(blob: bytes) -> int:
    value = 0
    for byte in blob:
        value = (value << 4) | (byte & 0x0F)
    return value


def extract_bits(blob: bytes, bit_offset: int, bit_width: int) -> int:
    """Read ``bit_width`` bits at ``bit_offset`` from the 256-bit stream."""
    total = _blob_int(blob)
    shift = BLOB_BIT_LENGTH - (bit_offset + bit_width)
    return (total >> shift) & ((1 << bit_width) - 1)


def register_name_codes(blob: bytes) -> tuple[int, ...]:
    """The 14 raw 6-bit character codes of the blob name field."""
    return tuple(
        extract_bits(
            blob, i * REGISTER_NAME_CHAR_BITS, REGISTER_NAME_CHAR_BITS
        )
        for i in range(REGISTER_NAME_LENGTH)
    )


def decode_register_name(blob: bytes) -> str:
    """Decode the blob name field to text (trailing spaces stripped)."""
    chars = [REGISTER_NAME_CHARSET[code] for code in register_name_codes(blob)]
    return "".join(chars).rstrip(" ")


def encode_register_name(name: str) -> tuple[int, ...]:
    """Encode text to 14 6-bit codes (space-padded). Raises on bad chars."""
    if len(name) > REGISTER_NAME_LENGTH:
        raise ValueError(
            f"name longer than {REGISTER_NAME_LENGTH} chars: {name!r}"
        )
    codes = []
    for ch in name.ljust(REGISTER_NAME_LENGTH, " "):
        idx = REGISTER_NAME_CHARSET.find(ch)
        if idx < 0:
            raise ValueError(f"character {ch!r} not in register name charset")
        codes.append(idx)
    return tuple(codes)


def decode_register_blob(blob: bytes) -> RegisterBasis:
    """Decode a nibble-packed 24-87 region into a :class:`RegisterBasis`."""
    kind = blob_kind(blob)
    if kind != "register_basis":
        raise ValueError(
            f"not a nibble-packed register basis blob (kind={kind!r})"
        )
    values = {
        f.id: extract_bits(blob, f.bit_offset, f.bit_width)
        for f in REGISTER_BLOB_FIELDS
        if f.id != "name"
    }
    return RegisterBasis(name=decode_register_name(blob), values=values)


def encode_register_blob(basis: RegisterBasis) -> bytes:
    """Inverse of :func:`decode_register_blob` (byte-identical round trip)."""
    total = 0
    codes = encode_register_name(basis.name)
    for code in codes:
        total = (total << REGISTER_NAME_CHAR_BITS) | code
    bits_done = REGISTER_NAME_LENGTH * REGISTER_NAME_CHAR_BITS
    for field in REGISTER_BLOB_FIELDS:
        if field.id == "name":
            continue
        if field.bit_offset != bits_done:
            raise AssertionError("field table out of order")
        value = int(basis.values[field.id])
        if value < 0 or value >= (1 << field.bit_width):
            raise ValueError(
                f"{field.id}={value} does not fit in {field.bit_width} bits"
            )
        total = (total << field.bit_width) | value
        bits_done += field.bit_width
    out = bytearray()
    for i in range(REGISTER_BASIS_BLOB_LENGTH):
        shift = BLOB_BIT_LENGTH - 4 * (i + 1)
        out.append((total >> shift) & 0x0F)
    return bytes(out)


def frame_blob(raw_frame: bytes) -> bytes:
    """Slice the 24-87 blob region out of a 157-byte program dump."""
    return raw_frame[
        REGISTER_BASIS_BLOB_OFFSET : REGISTER_BASIS_BLOB_OFFSET
        + REGISTER_BASIS_BLOB_LENGTH
    ]


def payload_value(raw_frame: bytes, field: RegisterBlobField) -> int | None:
    """Live edit-buffer value of a blob field's payload twin, if any."""
    offs = field.payload_offsets
    if not offs or field.id == "name":
        return None
    if len(offs) == 1:
        return raw_frame[offs[0]]
    if len(offs) == 2:
        return (raw_frame[offs[0]] << 4) | raw_frame[offs[1]]
    raise ValueError(f"unsupported payload width for {field.id}")


def stored_vs_payload(raw_frame: bytes) -> dict[str, tuple[int, int]]:
    """Blob (stored) vs payload (live) mismatches: id -> (stored, live).

    Empty when the register has no unstored edits. The blob snapshots the
    stored register; the payload reflects the live edit buffer, so entries
    here flag unstored edits (witness:
    ``samples/charset-b1s1-rt5s-unstored-edit.syx``).
    """
    blob = frame_blob(raw_frame)
    basis = decode_register_blob(blob)
    out: dict[str, tuple[int, int]] = {}
    for field in REGISTER_BLOB_FIELDS:
        live = payload_value(raw_frame, field)
        if live is None:
            continue
        stored = basis.values[field.id]
        if stored != live:
            out[field.id] = (stored, live)
    return out


def register_name_char_enum_entries() -> list[dict[str, Any]]:
    """Kaitai enum entries for the 6-bit name charset."""
    entries: list[dict[str, Any]] = []
    for code, ch in enumerate(REGISTER_NAME_CHARSET):
        if ch == " ":
            name = "space"
        elif ch == "&":
            name = "ampersand"
        elif ch.isdigit():
            name = f"digit_{ch}"
        elif ch.isupper():
            name = f"upper_{ch.lower()}"
        else:
            name = f"lower_{ch}"
        label = repr(ch)
        if code in INFERRED_CHARSET_CODES:
            label += " (inferred by continuity)"
        entries.append({"encoded": code, "name": name, "label": label})
    return entries


def runtime_reg_blob() -> dict[str, Any]:
    """Compact layout for the web-ui runtime bundle (``reg_blob`` key)."""
    return {
        "charset": REGISTER_NAME_CHARSET,
        "name_length": REGISTER_NAME_LENGTH,
        "char_bits": REGISTER_NAME_CHAR_BITS,
        "blob_offset": REGISTER_BASIS_BLOB_OFFSET,
        "blob_length": REGISTER_BASIS_BLOB_LENGTH,
        "fields": [
            {
                "id": f.id,
                "label": f.label,
                "bit": f.bit_offset,
                "width": f.bit_width,
                **(
                    {
                        "payloadField": f.payload_field,
                        "payloadOffsets": list(f.payload_offsets),
                    }
                    if f.payload_field
                    else {}
                ),
            }
            for f in REGISTER_BLOB_FIELDS
        ],
    }
