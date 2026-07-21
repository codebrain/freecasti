[Program dumps](../../prog/README.md) | **System overview** | [Bytes](../bytes/README.md) | [Byte map](../byte-map-overview.md)


# Audio Format

_Generated 2026-07-22. Source folder: `sysex/system/audio format/`._

## SysEx summary

- **Offsets:** 15
- **Encoding:** `raw_u8`
- **Confidence:** high
- **Layout:** [byte map overview](../byte-map-overview.md) · [full map](../byte-map.md)

## Description

Selects whether the M7 uses its analog or AES digital audio I/O. Analog mode always routes through the analog converters at the optimal internal sample rate for analog performance, regardless of what is connected. Digital mode uses a valid AES input when present, locks to the incoming sample rate and clock, mutes if the digital stream is lost, and switches back seamlessly when it returns.

_Source: [Bricasti M7 Owner's Manual — System Menu](https://www.bricasti.com/images/M7.pdf)._

> **Capture note:** No hardware UI walk in `docs/reference/provided_labels.json` yet for this system setting — encoding map is built from sparse labeled dumps.

## Encoding map

Witness sources: [encoding sources](../../../docs/encoding-sources.md) (`dump`, `provided`, `inferred`, preset links).

| Encoded | Offset 15 | Label | Source |
| --- | --- | --- | --- |
| 0 | `00` | analog | dump |
| 1 | `01` | digital | dump |

### Captured dumps

Sparse series used as anchors (plus secondary/checksum bytes that moved with this capture stream):

| Label | Offset 15 | Encoded | Checksum 72-75 | Source |
| --- | --- | --- | --- | --- |
| Analog | `00` | 0 | `0A` `0A` `02` `07` | dump |
| Digital | `01` | 1 | `0E` `09` `01` `08` | dump |

## Interpretation

- **Primary field:** offsets **15**, encoding `raw_u8` (enum table: 2 distinct labels each map to a unique encoded value).
- **Confidence:** high (2/2 dumps matched, 100%).
- **Sampling:** 2 sample mid(s) (not every step).
- **How to set:**
  1. encoded = lookup desired label in the capture encoding map (enum table)
  2. byte[offset0] = encoded & 0x0F  # M7 payload nibbles are 0x00-0x0F
  3. recompute trailing checksum: CRC-16/ARC over bytes[8:72], pack as four high-nibble-first SysEx bytes at offsets 72-75
- **Checksum nibbles:** 72-75 (CRC-16/ARC over offsets 8-71, packed high-nibble-first).

## Other system series

- **Audio Format** (this page)
- [Audio Routing](audio-routing.md)
- [Display Level](display-level.md)
- [Dry Gain](dry-gain.md)
- [MIDI Bank](midi-bank.md)
- [MIDI Channel](midi-channel.md)
- [Output Level](output-level.md)
- [Wet Gain](wet-gain.md)
