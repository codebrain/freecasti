"""Stub catalog hints for SYSTEM dump parameters (hint only)."""

from __future__ import annotations

from typing import Any

from ..prog.catalog import M7_MANUAL_URL

M7_MANUAL_SYSTEM_CITE = "Bricasti M7 Owner's Manual — System Menu"
MIDI_APP_URL = "https://www.bricasti.com/images/Midi_app_note.pdf"
MIDI_APP_CITE = "Bricasti M7 MIDI Application Notes"

SYSTEM_PARAMETERS: list[dict[str, Any]] = [
    {
        "id": "audio_format",
        "name": "Audio Format",
        "folder_hint": "audio format",
        "encoding": "raw_u8",
        "offsets": [15],
        "description": (
            "Selects whether the M7 uses its analog or AES digital audio I/O. "
            "Analog mode always routes through the analog converters at the "
            "optimal internal sample rate for analog performance, regardless of "
            "what is connected. Digital mode uses a valid AES input when present, "
            "locks to the incoming sample rate and clock, mutes if the digital "
            "stream is lost, and switches back seamlessly when it returns."
        ),
        "description_source": M7_MANUAL_SYSTEM_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": "Primary nibble at offset 15; Analog=0, Digital=1 in this capture set.",
    },
    {
        "id": "audio_routing",
        "name": "Audio Routing",
        "folder_hint": "audio routing",
        "encoding": "raw_u8",
        "offsets": [13],
        "description": (
            "Sets the routing of the processed (wet) audio. Useful for mono-in, "
            "stereo-out reverb work where a single input feeds both processing "
            "channels. This affects the wet path only — the dry path stays "
            "stereo (use a Y cable for mono internal dry mixing). Choices are "
            "Mono L, Mono R, or Stereo."
        ),
        "description_source": M7_MANUAL_SYSTEM_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": "Primary nibble at offset 13; Stereo=0, Mono L=1, Mono R=2.",
    },
    {
        "id": "midi_channel",
        "name": "MIDI Channel",
        "folder_hint": "midi channel",
        "encoding": "nibble_hilo",
        "offsets": [22, 23],
        "description": (
            "Selects the MIDI channel the M7 listens on for program change and "
            "other control messages (channels 1–16, or Omni for all channels). "
            "SysEx dumps are channel-less and are not filtered by this setting."
        ),
        "description_source": MIDI_APP_CITE,
        "description_url": MIDI_APP_URL,
        "notes": "Encoded 0–15 maps to channels 1–16; omni uses encoded 16.",
    },
    {
        "id": "midi_bank",
        "name": "MIDI Bank",
        "folder_hint": "midi bank",
        "encoding": "raw_u8",
        "offsets": [25],
        "description": (
            "Selects which program bank the M7 uses when receiving MIDI program "
            "changes — factory banks (Halls, Plates, Rooms, and so on), the "
            "V2 “2” banks, NonLin, and user register/favorite banks."
        ),
        "description_source": MIDI_APP_CITE,
        "description_url": MIDI_APP_URL,
        "notes": (
            "Primary nibble at offset 25; each bank name maps to a distinct "
            "value 0x00–0x0D in this capture set."
        ),
    },
    {
        "id": "display_level",
        "name": "Display Level",
        "folder_hint": "display level",
        "encoding": "raw_u8",
        "offsets": [21],
        "description": (
            "Sets the brightness of the front-panel display in five steps: "
            "Dim, 1, 2, 3, and Bright."
        ),
        "description_source": M7_MANUAL_SYSTEM_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": (
            "UI dim/1/2/3/bright; display-level captures also move offset 25 "
            "(secondary) alongside the primary field at offset 21."
        ),
    },
    {
        "id": "dry_gain",
        "name": "Dry Gain",
        "folder_hint": "dry gain",
        "encoding": "nibble_hilo",
        "offsets": [10, 11],
        "description": (
            "Part of the M7’s internal mixing: sets the level of the dry "
            "(direct) source path. Used with Wet Gain to balance dry and "
            "processed audio. Normally Off when the M7 is used as a full-wet "
            "sidechain with an external mixer; set to 0 dB (Full) with Wet "
            "Gain Off for unity dry pass-through (mastering or I/O test). "
            "Allow headroom — combining dry and wet can increase level. When "
            "using an external mixer, keep Dry Off to avoid out-of-phase dry "
            "from converter and signal-path delay."
        ),
        "description_source": M7_MANUAL_SYSTEM_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": (
            "Off and Full are discrete endpoints; numbered settings use 0.5 dB "
            "steps (label = encoded × 0.5 − 60.5 dB for encoded 1…121)."
        ),
    },
    {
        "id": "wet_gain",
        "name": "Wet Gain",
        "folder_hint": "wet gain",
        "encoding": "nibble_hilo",
        "offsets": [8, 9],
        "description": (
            "Part of the M7’s internal mixing: sets the level of the processed "
            "(reverb) signal. Off, then −60 dB to 0 dB (Full) in 0.5 dB steps. "
            "Normally 0 dB (Full) with Dry Gain Off for a full-wet sidechain "
            "setup. Set Off to bypass processing for I/O test and measurement. "
            "Allow headroom when balancing with Dry Gain — the mix can add gain "
            "and the reverb process itself can add up to about 10 dB."
        ),
        "description_source": M7_MANUAL_SYSTEM_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": (
            "Off and Full are discrete endpoints; numbered settings use 0.5 dB "
            "steps (label = encoded × 0.5 − 60.5 dB for encoded 1…121)."
        ),
    },
    {
        "id": "output_level",
        "name": "Output Level",
        "folder_hint": "output level",
        "encoding": "raw_u8",
        "offsets": [17],
        "description": (
            "Sets the analog output level trim in three steps (−8 dB, −16 dB, "
            "and −24 dB) to match the input sensitivity of your mixer return "
            "or the next device in the chain. Return to factory defaults after "
            "level-matching tests — high settings can distort on hot signals."
        ),
        "description_source": M7_MANUAL_SYSTEM_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": "Primary byte at offset 17 (raw_u8 values 0, 1, 2 for UI 8/16/24).",
    },
]


def lookup_system_parameter(name: str) -> dict[str, Any] | None:
    key = name.strip().casefold()
    for row in SYSTEM_PARAMETERS:
        if row["id"] == key or row["folder_hint"].casefold() == key:
            return row
        if row["name"].casefold() == key:
            return row
    return None
