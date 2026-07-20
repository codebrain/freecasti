"""Favorites capture session under sysex/prog/favorites/.

Witnesses for the favorite-slot field (offset 94), the panel-mode flag
(offset 92, including the favorites-screen value 8), and the favorites
auto-commit behavior of the register basis blob. See
sysex/prog/favorites/README.md for the session narrative.
"""

from pathlib import Path

import pytest

from m7_sysex.frame import (
    BRICASTI_MFR_ID,
    PROGRAM_DUMP_HEADER,
    PROGRAM_MESSAGE_LENGTH,
    parse_sysex,
    verify_program_dump_checksum,
)
from m7_sysex.names import (
    EDIT_DUMP_BANK_INDEX,
    HINT_BANK_INDEX,
    bank_index_from_raw,
    is_edit_buffer_dump,
    program_slot_from_raw,
)
from m7_sysex.prog.names import FAVORITE_SLOT_NONE, FAVORITE_SLOT_OFFSET
from m7_sysex.prog.register_blob import (
    blob_kind,
    decode_register_blob,
    frame_blob,
)
from m7_sysex.types import is_prog_corpus_dump

ROOT = Path(__file__).resolve().parents[1]
SYSEX = ROOT / "sysex"
FAVORITES = SYSEX / "prog" / "favorites"

PANEL_MODE_OFFSET = 92
FAVORITES_SCREEN_FLAG = 8

ALL_CAPTURES = sorted(FAVORITES.rglob("*.syx"))


def _raw(rel: str) -> bytes:
    return (FAVORITES / rel).read_bytes()


def test_corpus_has_all_session_captures():
    assert len(ALL_CAPTURES) == 22


@pytest.mark.parametrize(
    "path", ALL_CAPTURES, ids=lambda p: f"{p.parent.name}/{p.stem}"
)
def test_frames_parse_with_valid_crc(path: Path):
    raw = path.read_bytes()
    assert len(raw) == PROGRAM_MESSAGE_LENGTH
    frame = parse_sysex(raw)
    assert frame.manufacturer_id == BRICASTI_MFR_ID
    assert frame.header == PROGRAM_DUMP_HEADER
    assert verify_program_dump_checksum(raw)


@pytest.mark.parametrize(
    "path", ALL_CAPTURES, ids=lambda p: f"{p.parent.name}/{p.stem}"
)
def test_excluded_from_prog_corpus_scan(path: Path):
    assert not is_prog_corpus_dump(path, SYSEX)


@pytest.mark.parametrize(
    "path", ALL_CAPTURES, ids=lambda p: f"{p.parent.name}/{p.stem}"
)
def test_session_frame_invariants(path: Path):
    raw = path.read_bytes()
    # Panel mode: idle, parameter menu, or favorites screen.
    assert raw[PANEL_MODE_OFFSET] in (0, 2, FAVORITES_SCREEN_FLAG)
    if is_edit_buffer_dump(raw):
        # Hold-EDIT frames always read "not from a favorite".
        assert raw[FAVORITE_SLOT_OFFSET] == FAVORITE_SLOT_NONE
        assert bank_index_from_raw(raw) == EDIT_DUMP_BANK_INDEX
    else:
        # PROG frames carry the favorite slot code and the source identity.
        assert raw[FAVORITE_SLOT_OFFSET] in (0, 2, 4, 6)
        assert bank_index_from_raw(raw) in HINT_BANK_INDEX.values()
    # Whole session ran with register B1 R0 as the last-loaded register
    # basis; favorite operations never touch offsets 93/95.
    assert raw[93] == 1
    assert raw[95] == 0
    # Every frame in this session carries a register basis blob. Favorite
    # saves keep the store counter at 0 (favorites bypass the per-slot
    # counter); capture 01 is the initial *register* store to B1 R0, so it
    # carries that slot's real counter instead.
    blob = frame_blob(raw)
    assert blob_kind(blob) == "register_basis"
    counter = decode_register_blob(blob).store_counter
    if path.name == "01-store-b1r0-hold-edit.syx":
        assert counter > 0
    else:
        assert counter == 0


def test_prog_frames_carry_source_identity_never_bank_119():
    """Favorite-loaded PROG dumps report the source program's bank/slot."""
    cases = {
        "deep-ambience/06-load-fav1-hold-prog.syx": ("Ambience", 9, 0),
        "deep-ambience/07-load-fav2-hold-prog.syx": ("Ambience", 9, 2),
        "deep-ambience/08-load-fav3-hold-prog.syx": ("Ambience", 9, 4),
        "deep-ambience/09-load-fav4-hold-prog.syx": ("Ambience", 9, 6),
        "nonlin-c/13-rt075-favscreen-hold-prog-commit.syx": ("NonLin", 2, 0),
        "nonlin-c/18-rt1s-progscreen-hold-prog-nocommit.syx": ("NonLin", 2, 0),
        "nonlin-c/21-rt2s-menuopen-hold-prog-nocommit.syx": ("NonLin", 2, 0),
    }
    for rel, (bank, slot, fav_code) in cases.items():
        raw = _raw(rel)
        assert bank_index_from_raw(raw) == HINT_BANK_INDEX[bank], rel
        assert program_slot_from_raw(raw) == slot, rel
        assert raw[FAVORITE_SLOT_OFFSET] == fav_code, rel


def test_favorite_slot_codes_cover_all_four_slots():
    """Offset 94 = (slot - 1) * 2 across the deep-ambience PROG walk."""
    for slot in (1, 2, 3, 4):
        raw = _raw(f"deep-ambience/{5 + slot:02d}-load-fav{slot}-hold-prog.syx")
        assert raw[FAVORITE_SLOT_OFFSET] == (slot - 1) * 2


def test_panel_mode_flag_values():
    """92 = 8 on favorites screen, 2 with a menu open, 0 otherwise."""
    favscreen = (
        "deep-ambience/06-load-fav1-hold-prog.syx",
        "nonlin-c/13-rt075-favscreen-hold-prog-commit.syx",
    )
    for rel in favscreen:
        assert _raw(rel)[PANEL_MODE_OFFSET] == FAVORITES_SCREEN_FLAG, rel
    assert (
        _raw("nonlin-c/18-rt1s-progscreen-hold-prog-nocommit.syx")[
            PANEL_MODE_OFFSET
        ]
        == 0
    )
    assert (
        _raw("nonlin-c/21-rt2s-menuopen-hold-prog-nocommit.syx")[
            PANEL_MODE_OFFSET
        ]
        == 2
    )


def _reverb_times(rel: str) -> tuple[int, int]:
    """(blob stored, live payload) encoded reverb time for one capture."""
    raw = _raw(rel)
    blob = decode_register_blob(frame_blob(raw))
    payload = (raw[100] << 4) | raw[101]
    return blob.values["reverb_time"], payload


def test_auto_commit_trajectory():
    """Blob RT follows the commit story: only hold-PROG on the favorites
    screen persists the edit buffer into the favorite slot."""
    # Saved with factory RT 0.2 s (encoded 0 — the encoding floor).
    assert _reverb_times("nonlin-c/11-save-fav1-hold-edit.syx") == (0, 0)
    # Unstored 0.75 s edit (encoded 11): payload diverges from blob.
    assert _reverb_times("nonlin-c/12-rt075-unstored-hold-edit.syx") == (0, 11)
    # Hold-PROG on the favorites screen commits: blob catches up.
    assert _reverb_times(
        "nonlin-c/13-rt075-favscreen-hold-prog-commit.syx"
    ) == (11, 11)
    assert _reverb_times("nonlin-c/14-rt075-committed-hold-edit.syx") == (
        11,
        11,
    )
    # 1.0 s edit (encoded 16) never commits: not on timer, not on a brief
    # PROG press, not on hold-PROG from the program screen.
    for rel in (
        "nonlin-c/15-rt1s-immediate-hold-edit.syx",
        "nonlin-c/16-rt1s-after-wait-hold-edit.syx",
        "nonlin-c/17-rt1s-after-prog-press-hold-edit.syx",
        "nonlin-c/18-rt1s-progscreen-hold-prog-nocommit.syx",
        "nonlin-c/19-rt1s-hold-edit.syx",
    ):
        assert _reverb_times(rel) == (11, 16), rel
    # Re-selecting the favorite discards the unsaved edit; committed 0.75 s
    # survived the reload.
    assert _reverb_times("nonlin-c/20-reselect-fav1-hold-edit.syx") == (
        11,
        11,
    )
    # 2.0 s edit (encoded 36) with a menu open: hold-PROG does not commit.
    assert _reverb_times(
        "nonlin-c/21-rt2s-menuopen-hold-prog-nocommit.syx"
    ) == (11, 36)
    assert _reverb_times("nonlin-c/22-rt2s-hold-edit.syx") == (11, 36)


def test_resave_keeps_store_counter_zero():
    """Favorite saves and re-saves never bump the blob store counter."""
    first = _raw("deep-ambience/02-save-fav1-hold-edit.syx")
    resave = _raw("deep-ambience/10-resave-fav1-hold-edit.syx")
    for raw in (first, resave):
        assert decode_register_blob(frame_blob(raw)).store_counter == 0
    # The re-save changes nothing but the LCD display bytes (and checksum).
    assert first[8:146] == resave[8:146]
    assert first[148:152] == resave[148:152]


def test_wait_and_brief_prog_press_change_nothing():
    """Captures 16 and 17 are byte-identical (no timed or brief-press save)."""
    a = _raw("nonlin-c/16-rt1s-after-wait-hold-edit.syx")
    b = _raw("nonlin-c/17-rt1s-after-prog-press-hold-edit.syx")
    assert a == b
