"""Program algorithm constraints (manual + capture knowledge)."""

from __future__ import annotations

# Bank index for the NonLin factory bank (see specification/prog/program-identity.md).
NONLIN_BANK_INDEX = 10

# V2 addendum + UI: only these parameters affect NonLin sound on the unit.
NONLIN_ACTIVE_PARAMETERS: list[str] = [
    "size",
    "predelay",
    "rolloff",
    "early select",
    "early to reverb mix",
    "early rolloff",
]

PROG_ALGORITHM_CONSTRAINTS: dict[str, dict[str, object]] = {
    "nonlin": {
        "bank_index": NONLIN_BANK_INDEX,
        "params": NONLIN_ACTIVE_PARAMETERS,
    },
}
