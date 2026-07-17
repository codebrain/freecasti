"""Unit tests for encoding primitives and numeric fitting."""

import pytest

from m7_sysex.encodings import (
    decode_at_offsets,
    encode_at_offsets,
    fit_numeric_encoding,
    midi14_be,
    midi14_le,
    nibble_hilo,
    nibble_lohi,
)


def test_nibble_pair_decoders():
    assert nibble_hilo(0x03, 0x0A) == 0x3A
    assert nibble_lohi(0x0A, 0x03) == 0x3A
    # High bits outside the nibble are masked away.
    assert nibble_hilo(0xF3, 0xFA) == 0x3A
    assert midi14_be(0x01, 0x00) == 128
    assert midi14_le(0x00, 0x01) == 128


def test_decode_at_offsets():
    data = bytes(range(16))
    raw = decode_at_offsets(data, [7], "raw_u8")
    assert raw.value == 7
    pair = decode_at_offsets(data, [2, 3], "nibble_hilo")
    assert pair.value == 0x23
    assert pair.raw_bytes == (2, 3)
    assert pair.offsets == (2, 3)

    with pytest.raises(ValueError, match="raw_u8 expects 1"):
        decode_at_offsets(data, [1, 2], "raw_u8")
    with pytest.raises(ValueError, match="expects 2"):
        decode_at_offsets(data, [1], "nibble_hilo")
    with pytest.raises(ValueError, match="unknown encoding"):
        decode_at_offsets(data, [1], "nope")


@pytest.mark.parametrize(
    ("encoding", "encoded", "n_offsets"),
    [
        ("raw_u8", 0x3A, 1),
        ("nibble_hilo", 0x3A, 2),
        ("nibble_lohi", 0x3A, 2),
        ("midi14_be", 128, 2),
        ("midi14_le", 128, 2),
    ],
)
def test_encode_decode_at_offsets_roundtrip(encoding, encoded, n_offsets):
    wire = encode_at_offsets(encoded, encoding, n_offsets)
    data = bytearray(16)
    for i, off in enumerate(range(n_offsets)):
        data[off] = wire[i]
    decoded = decode_at_offsets(bytes(data), list(range(n_offsets)), encoding)
    assert decoded.value == encoded
    assert decoded.raw_bytes == wire


def _dumps_from_pairs(pairs):
    """Build (label, data) samples with the encoded value at offset 0 (raw_u8)."""
    return [(label, bytes([enc])) for label, enc in pairs]


def test_fit_exact_affine():
    # label = 8*encoded + 100 (delay-time shape)
    dumps = _dumps_from_pairs([(100, 0), (108, 1), (500, 50), (988, 111), (996, 112)])
    fit = fit_numeric_encoding(dumps, (0,), "raw_u8")
    assert fit.exact is True
    assert fit.score == 1.0
    assert fit.scale == 8.0
    assert fit.offset == 100.0


def test_fit_monotonic_table_when_edges_disagree():
    # Low edge step 2, high edge step 8 - no single affine fits everything.
    dumps = _dumps_from_pairs([(0, 0), (2, 1), (50, 10), (92, 20), (100, 21)])
    fit = fit_numeric_encoding(dumps, (0,), "raw_u8")
    assert fit.exact is False
    assert fit.monotonic_score == 1.0
    assert "table/index" in (fit.notes or "")
