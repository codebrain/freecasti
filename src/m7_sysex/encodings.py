"""Encoding hypotheses for mapping SysEx bytes to human parameter values."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Sequence


@dataclass(frozen=True)
class EncodedField:
    """A decoded integer extracted from one or more SysEx offsets."""

    name: str
    offsets: tuple[int, ...]
    raw_bytes: tuple[int, ...]
    value: int
    description: str


@dataclass(frozen=True)
class EncodingFit:
    """How well an encoding explains labeled dump values."""

    encoding: str
    offsets: tuple[int, ...]
    score: float  # 0..1 exact match rate under the chosen scale
    matched: int
    total: int
    scale: float | None = None
    offset: float | None = None
    mapping: list[dict[str, Any]] | None = None
    notes: str | None = None
    r_squared: float | None = None
    exact: bool = False  # True when score comes from an exact linear scale
    monotonic_score: float = 0.0  # 0..1 order agreement (for table/index fields)


def nibble_hilo(b0: int, b1: int) -> int:
    """High nibble in first byte, low nibble in second: (b0<<4)|b1."""
    return ((b0 & 0x0F) << 4) | (b1 & 0x0F)


def nibble_lohi(b0: int, b1: int) -> int:
    """Low nibble in first byte, high nibble in second: b0|(b1<<4)."""
    return (b0 & 0x0F) | ((b1 & 0x0F) << 4)


def midi14_be(b0: int, b1: int) -> int:
    return ((b0 & 0x7F) << 7) | (b1 & 0x7F)


def midi14_le(b0: int, b1: int) -> int:
    return (b0 & 0x7F) | ((b1 & 0x7F) << 7)


_PAIR_DECODERS: dict[str, Callable[[int, int], int]] = {
    "nibble_hilo": nibble_hilo,
    "nibble_lohi": nibble_lohi,
    "midi14_be": midi14_be,
    "midi14_le": midi14_le,
}

# Prefer these when scores tie (nibble payload devices).
_ENCODING_RANK = {
    "raw_u8": 0,
    "nibble_hilo": 1,
    "nibble_lohi": 2,
    "midi14_le": 3,
    "midi14_be": 4,
    "raw_bytes": 5,
}


def encode_at_offsets(encoded: int, encoding: str, n_offsets: int = 1) -> tuple[int, ...]:
    """Pack an encoded integer into on-wire SysEx data bytes (inverse of decode)."""
    enc = int(encoded)
    if encoding == "raw_u8":
        if n_offsets != 1:
            raise ValueError("raw_u8 expects 1 offset")
        return (enc & 0xFF,)
    if encoding == "nibble_hilo":
        if n_offsets != 2:
            raise ValueError("nibble_hilo expects 2 offsets")
        return ((enc >> 4) & 0x0F, enc & 0x0F)
    if encoding == "nibble_lohi":
        if n_offsets != 2:
            raise ValueError("nibble_lohi expects 2 offsets")
        return (enc & 0x0F, (enc >> 4) & 0x0F)
    if encoding == "midi14_be":
        if n_offsets != 2:
            raise ValueError("midi14_be expects 2 offsets")
        return ((enc >> 7) & 0x7F, enc & 0x7F)
    if encoding == "midi14_le":
        if n_offsets != 2:
            raise ValueError("midi14_le expects 2 offsets")
        return (enc & 0x7F, (enc >> 7) & 0x7F)
    if encoding == "raw_bytes":
        width = max(1, n_offsets)
        raw = enc.to_bytes(width, "big", signed=False)
        return tuple(raw[-width:])
    raise ValueError(f"unknown encoding: {encoding}")


def decode_at_offsets(data: bytes, offsets: Sequence[int], encoding: str) -> EncodedField:
    raw = tuple(data[i] for i in offsets)
    if encoding == "raw_u8":
        if len(raw) != 1:
            raise ValueError("raw_u8 expects 1 offset")
        value = raw[0]
        desc = "unsigned value from a single SysEx byte"
    elif encoding in _PAIR_DECODERS:
        if len(raw) != 2:
            raise ValueError(f"{encoding} expects 2 offsets")
        value = _PAIR_DECODERS[encoding](raw[0], raw[1])
        desc = {
            "nibble_hilo": "two nibbles, high then low -> one byte",
            "nibble_lohi": "two nibbles, low then high -> one byte",
            "midi14_be": "14-bit big-endian MIDI (7+7)",
            "midi14_le": "14-bit little-endian MIDI (7+7)",
        }[encoding]
    elif encoding == "raw_bytes":
        value = int.from_bytes(bytes(raw), "big")
        desc = f"{len(raw)} raw bytes big-endian"
    else:
        raise ValueError(f"unknown encoding: {encoding}")

    return EncodedField(
        name=encoding,
        offsets=tuple(offsets),
        raw_bytes=raw,
        value=value,
        description=desc,
    )


def fit_numeric_encoding(
    dumps: Sequence[tuple[Any, bytes]],
    offsets: Sequence[int],
    encoding: str,
) -> EncodingFit:
    """
    Score how well `encoding` at `offsets` matches numeric labels.

    Primary score is the fraction of dumps matched by an exact linear/affine
    map. Monotonic order agreement is used to rank table/index fields when no
    closed-form scale fits.
    """
    decoded: list[tuple[float, int, tuple[int, ...]]] = []
    for label, data in dumps:
        field = decode_at_offsets(data, offsets, encoding)
        decoded.append((float(label), field.value, field.raw_bytes))

    total = len(decoded)
    mapping = [
        {
            "label": label,
            "encoded": enc,
            "raw_bytes": [f"{b:02X}" for b in raw],
        }
        for label, enc, raw in decoded
    ]
    mono = _monotonic_score(
        [label for label, _enc, _raw in decoded],
        [enc for _label, enc, _raw in decoded],
    )

    best: EncodingFit | None = None
    scales = [1, 2, 4, 5, 8, 10, 0.5, 0.25, 0.1, 0.05]

    # Edge-affine from capture convention: extremes + adjacent-to-extremes.
    # When low and high edge slopes agree, that scale+offset is authoritative.
    for scale, add, edge_note in _edge_affine_hypotheses(decoded):
        matched = sum(
            1
            for label, enc, _raw in decoded
            if _nearly_equal(enc * scale + add, label)
        )
        if _nearly_equal(add, 0.0):
            notes = f"label = encoded * {scale:g}"
        elif _nearly_equal(scale, 1.0):
            notes = f"label = encoded + ({add:g})"
        else:
            notes = f"label = encoded * {scale:g} + ({add:g})"
        notes = f"{notes}; {edge_note}"
        fit = EncodingFit(
            encoding=encoding,
            offsets=tuple(offsets),
            score=matched / total if total else 0.0,
            matched=matched,
            total=total,
            scale=float(scale),
            offset=float(add),
            mapping=mapping,
            notes=notes,
            exact=True,
            monotonic_score=mono,
        )
        best = _prefer(best, fit)

    # Exact affine maps derived from the data (handles large dB offsets like
    # label = encoded - 20 for VLF cut, not just the small ±8 UI offsets).
    for scale in scales:
        diffs = []
        ok = True
        for label, enc, _raw in decoded:
            predicted_base = enc * float(scale)
            diff = label - predicted_base
            if diffs and not _nearly_equal(diff, diffs[0]):
                ok = False
                break
            diffs.append(diff)
        if ok and diffs:
            add = diffs[0]
            if _nearly_equal(add, round(add)):
                add = float(int(round(add)))
            if _nearly_equal(add, 0.0):
                notes = f"label = encoded * {scale}"
            elif _nearly_equal(scale, 1.0):
                notes = f"label = encoded + ({add:g})"
            else:
                notes = f"label = encoded * {scale} + ({add:g})"
            fit = EncodingFit(
                encoding=encoding,
                offsets=tuple(offsets),
                score=1.0,
                matched=total,
                total=total,
                scale=float(scale),
                offset=float(add),
                mapping=mapping,
                notes=notes,
                exact=True,
                monotonic_score=mono,
            )
            best = _prefer(best, fit)

    for scale in scales:
        for notes, predicted_fn, out_scale, out_offset in (
            (
                f"label = encoded * {scale}",
                lambda enc, s=scale: enc * s,
                float(scale),
                0.0,
            ),
            (
                f"label = encoded / {scale}",
                lambda enc, s=scale: enc / s,
                1.0 / float(scale),
                0.0,
            ),
        ):
            matched = sum(
                1
                for label, enc, _raw in decoded
                if _nearly_equal(predicted_fn(enc), label)
            )
            fit = EncodingFit(
                encoding=encoding,
                offsets=tuple(offsets),
                score=matched / total if total else 0.0,
                matched=matched,
                total=total,
                scale=out_scale,
                offset=out_offset,
                mapping=mapping,
                notes=notes,
                exact=True,
                monotonic_score=mono,
            )
            best = _prefer(best, fit)

    # Common small UI offsets: display = encoded + k (e.g. modulation).
    for add in range(-8, 9):
        if add == 0:
            continue
        matched = sum(
            1
            for label, enc, _raw in decoded
            if _nearly_equal(enc + add, label)
        )
        fit = EncodingFit(
            encoding=encoding,
            offsets=tuple(offsets),
            score=matched / total if total else 0.0,
            matched=matched,
            total=total,
            scale=1.0,
            offset=float(add),
            mapping=mapping,
            notes=f"label = encoded + ({add})",
            exact=True,
            monotonic_score=mono,
        )
        best = _prefer(best, fit)

    # Least-squares / monotonic fallback when exact fit is incomplete.
    if total >= 2:
        xs = [enc for _label, enc, _raw in decoded]
        ys = [label for label, _enc, _raw in decoded]
        scale_ls, offset_ls, r2 = _linear_regression(xs, ys)
        ls_notes = (
            f"least-squares hint only (not used for endpoint unit conversion): "
            f"label ~= {scale_ls:.6g}*encoded + {offset_ls:.6g} (r^2={r2:.4f})"
        )
        edge_note = _edge_disagreement_note(decoded)
        table_notes = (
            f"table/index candidate (monotonic {mono:.0%})"
            + (f"; {edge_note}" if edge_note else "")
            + f"; {ls_notes}"
        )
        if best is None or best.score < 1.0:
            # Always consider a table candidate so partial exact scales
            # (e.g. predelay *2 at the low end only) lose to monotonic tables
            # when edge slopes disagree.
            table_fit = EncodingFit(
                encoding=encoding,
                offsets=tuple(offsets),
                score=mono if mono >= 0.9 else 0.0,
                matched=0,
                total=total,
                scale=None,
                offset=None,
                mapping=mapping,
                notes=table_notes if mono >= 0.9 else ls_notes,
                r_squared=r2,
                exact=False,
                monotonic_score=mono,
            )
            best = _prefer(best, table_fit)
            if best is not None and best.exact and best.score < 1.0:
                extra = ls_notes
                if edge_note:
                    extra = f"{edge_note}; {extra}"
                best = EncodingFit(
                    encoding=best.encoding,
                    offsets=best.offsets,
                    score=best.score,
                    matched=best.matched,
                    total=best.total,
                    scale=best.scale,
                    offset=best.offset,
                    mapping=best.mapping,
                    notes=f"{best.notes}; {extra}",
                    r_squared=r2,
                    exact=best.exact,
                    monotonic_score=mono,
                )

    assert best is not None
    return best


def is_enum_table_fit(fit: EncodingFit | dict[str, Any]) -> bool:
    """True when the fit is a bijective enum label → encoded lookup table."""
    notes = fit.notes if isinstance(fit, EncodingFit) else fit.get("notes")
    return bool(notes) and str(notes).startswith("enum table")


def fit_enum_encoding(
    dumps: Sequence[tuple[Any, bytes]],
    offsets: Sequence[int],
    encoding: str,
) -> EncodingFit:
    """
    Score how well `encoding` at `offsets` explains enum-named capture labels.

    A perfect fit requires each label to map to exactly one encoded value and
    no two labels to share an encoded value (bijection within the capture set).
    """
    decoded: list[tuple[Any, int, tuple[int, ...]]] = []
    for label, data in dumps:
        field = decode_at_offsets(data, offsets, encoding)
        decoded.append((label, field.value, field.raw_bytes))

    total = len(decoded)
    mapping = [
        {
            "label": label,
            "encoded": enc,
            "raw_bytes": [f"{b:02X}" for b in raw],
        }
        for label, enc, raw in decoded
    ]

    label_to_enc: dict[Any, int] = {}
    enc_to_label: dict[int, Any] = {}
    matched = 0
    for label, enc, _raw in decoded:
        label_ok = label not in label_to_enc or label_to_enc[label] == enc
        enc_ok = enc not in enc_to_label or enc_to_label[enc] == label
        if label_ok and enc_ok:
            label_to_enc[label] = enc
            enc_to_label[enc] = label
            matched += 1

    bijective = matched == total and len(label_to_enc) == total
    if bijective:
        notes = (
            f"enum table: {total} distinct labels each map to a unique encoded value"
        )
    else:
        notes = "enum table (partial or inconsistent label/encoded mapping)"

    return EncodingFit(
        encoding=encoding,
        offsets=tuple(offsets),
        score=1.0 if bijective else (matched / total if total else 0.0),
        matched=matched if bijective else matched,
        total=total,
        scale=None,
        offset=None,
        mapping=mapping,
        notes=notes,
        exact=False,
        monotonic_score=1.0 if bijective else 0.0,
    )


def rank_key(fit: EncodingFit | dict[str, Any]) -> tuple:
    """Sort key: perfect exact fits, then full monotonic tables, then weak exact."""
    if isinstance(fit, EncodingFit):
        encoding = fit.encoding
        score = fit.score
        exact = fit.exact
        offsets = fit.offsets
        scale = fit.scale
        mono = fit.monotonic_score
    else:
        encoding = fit["encoding"]
        score = fit["score"]
        exact = fit.get("exact", False)
        offsets = tuple(fit["offsets"])
        scale = fit.get("scale")
        mono = float(fit.get("monotonic_score") or 0.0)

    # Habitual edit-state nibbles - demote unless nothing else fits.
    secondary_zone = {146, 147}
    secondary_penalty = 1 if any(o in secondary_zone for o in offsets) else 0

    strong_exact = score if exact and score >= 0.999 else 0.0
    # Complete monotonic table beats a partial closed-form that only fits
    # some dumps (typical when extreme->adjacent slopes disagree).
    strong_table = score if (not exact and score >= 0.999) else 0.0
    weak_exact = score if exact else 0.0
    scale_penalty = 0 if scale == 1 or scale is None else 1
    return (
        -strong_exact,
        -strong_table,
        -mono,
        -weak_exact,
        secondary_penalty,
        -len(offsets),
        scale_penalty,
        _ENCODING_RANK.get(encoding, 99),
        offsets,
    )


def _prefer(current: EncodingFit | None, candidate: EncodingFit) -> EncodingFit:
    if current is None:
        return candidate
    return candidate if rank_key(candidate) < rank_key(current) else current


def _edge_affine_hypotheses(
    decoded: Sequence[tuple[float, int, tuple[int, ...]]],
) -> list[tuple[float, float, str]]:
    """
    Derive affine candidates from extreme<->adjacent pairs.

    Capture series include extremes and adjacent-to-extreme settings; when both
    edges share the same dlabel/dencoded, that slope is a global scale.
    """
    if len(decoded) < 2:
        return []
    ordered = sorted(decoded, key=lambda t: t[0])
    low, low_adj = ordered[0], ordered[1]
    high, high_adj = ordered[-1], ordered[-2]

    def slope(
        a: tuple[float, int, tuple[int, ...]],
        b: tuple[float, int, tuple[int, ...]],
    ) -> float | None:
        d_enc = b[1] - a[1]
        if d_enc == 0:
            return None
        return (b[0] - a[0]) / d_enc

    low_s = slope(low, low_adj)
    high_s = slope(high_adj, high)

    out: list[tuple[float, float, str]] = []
    if (
        low_s is not None
        and high_s is not None
        and _nearly_equal(low_s, high_s, rel=1e-4, abs_tol=1e-6)
    ):
        scale = (low_s + high_s) / 2.0
        scale = float(f"{scale:.12g}")
        add = low[0] - scale * low[1]
        if _nearly_equal(add, round(add)):
            add = float(int(round(add)))
        else:
            add = float(f"{add:.12g}")
        out.append(
            (
                scale,
                add,
                "from agreeing extreme<->adjacent edge slopes",
            )
        )
    elif low_s is not None and high_s is not None:
        # Still try each edge locally - useful diagnostics via scoring.
        for scale, anchor, which in (
            (low_s, low, "low-edge"),
            (high_s, high, "high-edge"),
        ):
            add = anchor[0] - scale * anchor[1]
            out.append(
                (
                    float(f"{scale:.12g}"),
                    float(f"{add:.12g}"),
                    f"from {which} slope only (edges disagree)",
                )
            )
    return out


def _edge_disagreement_note(
    decoded: Sequence[tuple[float, int, tuple[int, ...]]],
) -> str | None:
    if len(decoded) < 4:
        # Need two distinct pairs.
        if len(decoded) < 2:
            return None
    ordered = sorted(decoded, key=lambda t: t[0])
    if len(ordered) < 2:
        return None
    low_s = None
    high_s = None
    d_enc = ordered[1][1] - ordered[0][1]
    if d_enc:
        low_s = (ordered[1][0] - ordered[0][0]) / d_enc
    d_enc = ordered[-1][1] - ordered[-2][1]
    if d_enc:
        high_s = (ordered[-1][0] - ordered[-2][0]) / d_enc
    if low_s is None or high_s is None:
        return None
    if _nearly_equal(low_s, high_s, rel=1e-4, abs_tol=1e-6):
        return None
    return (
        f"extreme<->adjacent slopes disagree "
        f"(low dlabel/denc={low_s:.6g}, high={high_s:.6g})"
    )


def _monotonic_score(labels: Sequence[float], encoded: Sequence[int]) -> float:
    """Fraction of label pairs whose encoded order agrees (Spearman-style)."""
    n = len(labels)
    if n < 2:
        return 1.0
    agree = 0
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            d_label = labels[j] - labels[i]
            d_enc = encoded[j] - encoded[i]
            if d_label == 0:
                continue
            total += 1
            if d_enc == 0:
                continue
            if (d_label > 0 and d_enc > 0) or (d_label < 0 and d_enc < 0):
                agree += 1
    return agree / total if total else 0.0


def _nearly_equal(a: float, b: float, rel: float = 1e-6, abs_tol: float = 1e-6) -> bool:
    return abs(a - b) <= max(abs_tol, rel * max(abs(a), abs(b)))


def _linear_regression(xs: Sequence[float], ys: Sequence[float]) -> tuple[float, float, float]:
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    var_x = sum((x - mean_x) ** 2 for x in xs)
    if var_x == 0:
        return 0.0, mean_y, 0.0
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    slope = cov / var_x
    intercept = mean_y - slope * mean_x
    ss_tot = sum((y - mean_y) ** 2 for y in ys)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot else 1.0
    return slope, intercept, r2
