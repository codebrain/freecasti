"""Tests for program algorithm constraints."""

from m7_sysex.prog.algorithms import (
    NONLIN_ACTIVE_PARAMETERS,
    NONLIN_BANK_INDEX,
    PROG_ALGORITHM_CONSTRAINTS,
)


def test_nonlin_constraint_lists_user_controls() -> None:
    assert NONLIN_BANK_INDEX == 10
    assert set(NONLIN_ACTIVE_PARAMETERS) == {
        "size",
        "predelay",
        "rolloff",
        "early select",
        "early to reverb mix",
        "early rolloff",
    }
    assert PROG_ALGORITHM_CONSTRAINTS["nonlin"]["bank_index"] == 10
