[Program dumps](../../prog/README.md) | [System overview](../README.md) | **Bytes** | [Byte map](../byte-map-overview.md)


# System dump bytes

**System / I/O settings** captured while holding **SYSTEM** on the M7 — not program sound parameters. Each row links to a capture-series page with dump tables and encoding fits.

| Parameter | SysEx (offsets · encoding · confidence) | Description |
|-----------|----------------------------------------|-------------|
| [Audio Format](audio-format.md) | `15` · `raw_u8` · high | Selects whether the M7 uses its analog or AES digital audio I/O. Analog mode always routes through the analog converters at the optimal internal sample rate for analog performance, regardless of what is connected. Digital mode uses a valid AES input when present, locks to the incoming sample rate and clock, mutes if the digital stream is lost, and switches back seamlessly when it returns. |
| [Audio Routing](audio-routing.md) | `13` · `raw_u8` · high | Sets the routing of the processed (wet) audio. Useful for mono-in, stereo-out reverb work where a single input feeds both processing channels. This affects the wet path only — the dry path stays stereo (use a Y cable for mono internal dry mixing). Choices are Mono L, Mono R, or Stereo. |
| [MIDI Channel](midi-channel.md) | `22-23` · `nibble_hilo` · high | Selects the MIDI channel the M7 listens on for program change and other control messages (channels 1–16, or Omni for all channels). SysEx dumps are channel-less and are not filtered by this setting. |
| [MIDI Bank](midi-bank.md) | `25` · `raw_u8` · high | Selects which program bank the M7 uses when receiving MIDI program changes — factory banks (Halls, Plates, Rooms, and so on), the V2 “2” banks, NonLin, and user register/favorite banks. |
| [Display Level](display-level.md) | `21` · `raw_u8` · high | Sets the brightness of the front-panel display in five steps: Dim, 1, 2, 3, and Bright. |
| [Dry Gain](dry-gain.md) | `10-11` · `nibble_hilo` · high | Part of the M7’s internal mixing: sets the level of the dry (direct) source path. Used with Wet Gain to balance dry and processed audio. Normally Off when the M7 is used as a full-wet sidechain with an external mixer; set to 0 dB (Full) with Wet Gain Off for unity dry pass-through (mastering or I/O test). Allow headroom — combining dry and wet can increase level. When using an external mixer, keep Dry Off to avoid out-of-phase dry from converter and signal-path delay. |
| [Wet Gain](wet-gain.md) | `8-9` · `nibble_hilo` · high | Part of the M7’s internal mixing: sets the level of the processed (reverb) signal. Off, then −60 dB to 0 dB (Full) in 0.5 dB steps. Normally 0 dB (Full) with Dry Gain Off for a full-wet sidechain setup. Set Off to bypass processing for I/O test and measurement. Allow headroom when balancing with Dry Gain — the mix can add gain and the reverb process itself can add up to about 10 dB. |
| [Output Level](output-level.md) | `17` · `raw_u8` · high | Sets the analog output level trim in three steps (−8 dB, −16 dB, and −24 dB) to match the input sensitivity of your mixer return or the next device in the chain. Return to factory defaults after level-matching tests — high settings can distort on hot signals. |

_Last exported: 2026-07-21_

See [../README.md](../README.md) for frame layout and byte-map coverage.
