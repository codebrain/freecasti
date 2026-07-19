"""Bricasti M7 program-parameter catalog (hint only).

Printed manual ranges help plan captures. They are not authoritative
per unit - firmware variance is expected (e.g. Early Select 0...31 vs printed
0...20). Dump-derived extremes and encodings always win.
"""

from __future__ import annotations

from typing import Any

# Official PDF sources for ``description`` fields below.
M7_MANUAL_URL = "https://www.bricasti.com/images/M7.pdf"
V2_ADDENDUM_URL = (
    "https://www.bricasti.com/images/M7_V2_Manual_Addendum_Upgrade.pdf"
)
M7_MANUAL_CITE = "Bricasti M7 Owner's Manual — Reverb Parameters"
V2_ADDENDUM_CITE = "Bricasti M7 V2 Manual Addendum"


# Menu order as listed in the Bricasti M7 owner's manual.
PROGRAM_PARAMETERS: list[dict[str, Any]] = [
    {
        "id": "reverb_time",
        "name": "Reverb Time",
        "aliases": ("reverb time", "rt", "time", "decay"),
        "unit": "s",
        "min": 0.1,
        "max": 30.0,
        "display": "mid_band_rt",
        "description": (
            "Mid-frequency reverb time. Sets the reverb time of the mid "
            "frequencies when the signal stops."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": (
            "This unit: non-linear table @ 100-101; "
            "captured 0.2...30 s (printed floor 0.1 s not yet dumped)."
        ),
        "observed_min": 0.2,
        "folder_hint": "reverb time",
    },
    {
        "id": "size",
        "name": "Size",
        "aliases": ("size", "reverb size"),
        "unit": None,
        "min": 1,
        "max": 24,
        "observed_min": 0,
        "observed_max": 30,
        "display": "integer",
        "description": (
            "Adjusts the apparent size of the late reverberant field."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": (
            "Manual UI: Small 1 - 24 Large. "
            "This unit uses Small / numbered / Large endpoints (may exceed 24)."
        ),
        "folder_hint": "size",
    },
    {
        "id": "predelay",
        "name": "Pre Delay",
        "aliases": ("predelay", "pre delay", "pre-delay"),
        "unit": "ms",
        "min": 0,
        "max": 500,
        "display": "ms",
        "description": (
            "Sets the amount of time which elapses between the input signal "
            "and the onset of reverberation."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": "Sparse capture series uses a non-linear table @ 104-105.",
        "folder_hint": "predelay",
    },
    {
        "id": "diffusion",
        "name": "Diffusion",
        "aliases": ("diffusion",),
        "unit": None,
        "min": 1,
        "max": 9,
        "observed_min": 0,
        "observed_max": 10,
        "display": "integer",
        "description": (
            "Sets initial diffusion of the reverb. Displayed and controlled as "
            "a percentage change from the initial value defined by the preset."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": (
            "Manual UI: Low 1 - 9 High. Captured hardware series also show "
            "0...10. SysEx stores an absolute encoded value @ 107."
        ),
        "folder_hint": "diffusion",
    },
    {
        "id": "density",
        "name": "Density",
        "aliases": ("density",),
        "unit": None,
        "min": 1,
        "max": 9,
        "observed_min": 0,
        "observed_max": 10,
        "display": "integer",
        "description": "Sets how the echo density builds up over time.",
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": (
            "Manual UI: Low 1 - 9 High. Captured hardware series also show 0...10."
        ),
        "folder_hint": "density",
    },
    {
        "id": "modulation",
        "name": "Modulation",
        "aliases": ("modulation", "mod"),
        "unit": None,
        "min": 1,
        "max": 9,
        "has_off": True,
        "observed_min": 0,
        "observed_max": 10,
        "display": "off_plus_integer",
        "description": (
            "Controls the amount of modulation and pitch variation in the "
            "later part of the reverberant field."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": (
            "Manual UI: Off, Low 1 - 9 High. Captures may use encoded off + 0...10."
        ),
        "folder_hint": "modulation",
    },
    {
        "id": "rolloff",
        "name": "Rolloff",
        "aliases": ("rolloff", "roll off", "roll-off"),
        "unit": "hz",
        "min": 80,
        "max": 28000,
        "display": "hz_table",
        "description": (
            "Low pass filter applied to the overall output of the reverb."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": (
            "Manual max 28 kHz; FULL may sit above the last numbered Hz. "
            "Filter order (dB/octave) analysis: "
            "[rolloff-slopes.md](../../../docs/rolloff-slopes.md)."
        ),
        "folder_hint": "rolloff",
    },
    {
        "id": "hf_rt_multiply",
        "name": "HF RT Multiply",
        "aliases": ("hf rt multiply", "hf rt mpy", "hf multiply"),
        "unit": None,
        "min": 0.2,
        "max": 1.0,
        "display": "multiply",
        "description": (
            "Sets the high-frequency reverb time above the crossover "
            "frequency set by HF RT Crossover. Displayed and controlled as a "
            "scaling of Reverb Time."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": "Closed-form scale @ 114-115: label = 0.05×encoded + 0.2.",
        "folder_hint": "hf rt multiply",
    },
    {
        "id": "hf_rt_crossover",
        "name": "HF RT Crossover",
        "aliases": ("hf rt crossover", "hf crossover", "hf xover"),
        "unit": "hz",
        "min": 200,
        "max": 16000,
        "display": "hz_table",
        "description": (
            "Sets the crossover frequency used by HF RT Multiply."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": "Non-linear Hz table @ 116-117.",
        "folder_hint": "hf rt crossover",
    },
    {
        "id": "lf_rt_multiply",
        "name": "LF RT Multiply",
        "aliases": ("lf rt multiply", "lf rt mpy", "lf multiply"),
        "unit": None,
        "min": 0.2,
        "max": 4.0,
        "display": "multiply",
        "description": (
            "Sets the low-frequency reverb time below the crossover "
            "frequency set by LF RT Crossover. Displayed and controlled as a "
            "scaling of Reverb Time."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": (
            "Captured @ 118-119: 0.05 steps up to 2.0×, then 0.1 steps to "
            "4.0× (non-uniform table, unlike HF)."
        ),
        "folder_hint": "lf rt multiply",
    },
    {
        "id": "lf_rt_crossover",
        "name": "LF RT Crossover",
        "aliases": ("lf rt crossover", "lf crossover", "lf xover"),
        "unit": "hz",
        "min": 80,
        "max": 4800,
        "display": "hz_table",
        "description": (
            "Sets the crossover frequency used by LF RT Multiply."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": "Own Hz table @ 120-121 (not HF's).",
        "folder_hint": "lf rt crossover",
    },
    {
        "id": "vlf_cut",
        "name": "VLF Cut",
        "aliases": ("vlf cut", "vlf"),
        "unit": "db",
        "min": -18,
        "max": 0,
        "observed_min": -20,
        "display": "db_cut",
        "description": (
            "Cuts the very low frequency content of the initial part of both "
            "the early and late reverberant fields."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": (
            "Printed 0 to -18 dB. Some units/UI paths may show -20; "
            "record hardware truth, do not force the printed floor."
        ),
        "folder_hint": "vlf cut",
    },
    {
        "id": "early_to_reverb_mix",
        "name": "Early/Reverb Mix",
        "aliases": (
            "early to reverb mix",
            "early/reverb mix",
            "early reverb mix",
            "early rev mix",
        ),
        "unit": None,
        "min": 0,
        "max": 40,
        "balance_side_max": 20,
        "display": "balance_pair",
        "description": (
            "Sets the balance between the early and later parts of the "
            "reverberant fields."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": (
            "Official 0/20 ... 20/20 ... 20/0 balance path (positions 0...40 "
            "at 124-125). Capture filenames use A.B (0.20, 20.6, 20.0) because "
            "'/' is illegal in filenames — same values as UI/sheet A/B."
        ),
        "folder_hint": "early to reverb mix",
    },
    {
        "id": "early_rolloff",
        "name": "Early Rolloff",
        "aliases": ("early rolloff", "early roll off"),
        "unit": "hz",
        "min": 80,
        "max": 20000,
        "display": "hz_table",
        "description": (
            "Sets the rolloff frequency point of the low pass filter for the "
            "early part of the reverberant field."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "notes": (
            "Non-linear Hz table @ 126-127. "
            "Filter order (dB/octave) analysis: "
            "[rolloff-slopes.md](../../../docs/rolloff-slopes.md)."
        ),
        "folder_hint": "early rolloff",
    },
    {
        "id": "early_select",
        "name": "Early Select",
        "aliases": ("early select",),
        "unit": None,
        "min": 0,
        "max": 20,
        "observed_max": 31,
        "display": "integer",
        "description": (
            "Controls the build up and decay characteristics of the early "
            "part of the reverberant field. The V2 addendum expands the "
            "selection beyond the printed 0–20 to 0–31 with larger, more "
            "spread-out early variants for a slower early reverb build-up "
            "(available on both V1 and V2 algorithm presets)."
        ),
        "description_source": M7_MANUAL_CITE,
        "description_url": M7_MANUAL_URL,
        "description_sources": (
            (M7_MANUAL_CITE, M7_MANUAL_URL),
            (V2_ADDENDUM_CITE, V2_ADDENDUM_URL),
        ),
        "notes": (
            "Manual prints 0 - 20; this project's M7 reaches 0 - 31. "
            "Treat the printed range as a hint only."
        ),
        "folder_hint": "early select",
    },
    {
        "id": "delay_level",
        "name": "Delay Level",
        "aliases": ("delay level", "delay lvl", "reverb delay level"),
        "unit": "db",
        "min": -20,
        "max": -6,
        "has_off": True,
        "display": "db_cut",
        "description": (
            "Level of the delayed input injected into the start of the late "
            "reverb (not the early reverb). The delayed sound is the original "
            "input signal, delayed, diffused, and band-limited by Rolloff."
        ),
        "description_source": V2_ADDENDUM_CITE,
        "description_url": V2_ADDENDUM_URL,
        "notes": (
            "This M7: discrete Off, or -20 dB ... -6 dB. "
            "V2 addendum parameter; not in older printed tables."
        ),
        "folder_hint": "delay level",
    },
    {
        "id": "delay_time",
        "name": "Delay Time",
        "aliases": ("delay time", "reverb delay time"),
        "unit": "ms",
        "min": 100,
        "max": 1000,
        "display": "ms",
        "description": (
            "Delay time for a diffused set of eight voices spread in time "
            "(controlled as a single delay). Adds coloration and a late swell "
            "to the late reverb."
        ),
        "description_source": V2_ADDENDUM_CITE,
        "description_url": V2_ADDENDUM_URL,
        "notes": (
            "Printed 100 ms ... 1 s. "
            "This unit: label = 8*encoded + 100; captured high 996 ms "
            "(8 ms grid; 1000 would not land on a step)."
        ),
        "observed_max": 996,
        "folder_hint": "delay time",
    },
    {
        "id": "delay_modulation",
        "name": "Delay Modulation",
        "aliases": ("delay modulation", "delay mod"),
        "unit": None,
        "min": 1,
        "max": 9,
        "has_off": True,
        "observed_min": 0,
        "observed_max": 10,
        "display": "off_plus_integer",
        "description": (
            "Modulates the delay voices only (not the reverb), similar in "
            "character to reverb Modulation: low settings are slower and more "
            "shallow; higher settings are more random and deeper."
        ),
        "description_source": V2_ADDENDUM_CITE,
        "description_url": V2_ADDENDUM_URL,
        "notes": (
            "Off, Low 1 - 9 High (same shape as reverb Modulation). "
            "V2 addendum parameter."
        ),
        "folder_hint": "delay modulation",
    },
]


_ALIAS_INDEX: dict[str, dict[str, Any]] = {}
for _entry in PROGRAM_PARAMETERS:
    for _alias in _entry["aliases"]:
        _ALIAS_INDEX[_alias.casefold()] = _entry
    _ALIAS_INDEX[_entry["folder_hint"].casefold()] = _entry
    _ALIAS_INDEX[_entry["name"].casefold()] = _entry


CATALOG_META = {
    "sources": [
        "Bricasti M7 Owner's Manual (program parameter control ranges)",
        "Bricasti MIDI App Notes / V2 addendum (dump types only)",
    ],
    "disclaimer": (
        "Hint only from published manuals / controllers - not authoritative. "
        "Firmware and unit variation are common (e.g. Early Select may be 0...31 "
        "on some M7s while the manual prints 0...20). Dump-derived extremes and "
        "encodings always win; catalog checks are soft guidance for capture planning."
    ),
}


def lookup_parameter(folder_name: str) -> dict[str, Any] | None:
    """Match a sysex/<folder>/ name to an official catalog entry."""
    key = folder_name.strip().casefold()
    if key in _ALIAS_INDEX:
        return dict(_ALIAS_INDEX[key])
    # Loose contains match for slight naming drift.
    for alias, entry in _ALIAS_INDEX.items():
        if alias in key or key in alias:
            return dict(entry)
    return None


def expected_range(entry: dict[str, Any]) -> dict[str, Any]:
    """Published range, preferring wider observed bounds when noted."""
    lo = entry.get("observed_min", entry.get("min"))
    hi = entry.get("observed_max", entry.get("max"))
    return {
        "manual_min": entry.get("min"),
        "manual_max": entry.get("max"),
        "compare_min": lo,
        "compare_max": hi,
        "unit": entry.get("unit"),
        "has_off": bool(entry.get("has_off")),
        "display": entry.get("display"),
        "balance_side_max": entry.get("balance_side_max"),
    }


def annotate_series(
    folder_name: str,
    value_range: dict[str, Any] | None,
    *,
    unit: str | None = None,
) -> dict[str, Any]:
    """
    Attach catalog hint metadata and soft range checks to one series.

    Dumps always win. Printed manual ranges are hints only - exceeding them
    is recorded as a note (firmware/unit variance), not an error to "fix".
    """
    entry = lookup_parameter(folder_name)
    if entry is None:
        return {
            "matched": False,
            "role": "hint",
            "warning": (
                f"No catalog hint for '{folder_name}'. "
                "See docs/parameter-catalog.md for the published list."
            ),
            **CATALOG_META,
        }

    expected = expected_range(entry)
    out: dict[str, Any] = {
        "matched": True,
        "role": "hint",
        "id": entry["id"],
        "name": entry["name"],
        "folder_hint": entry["folder_hint"],
        "notes": entry.get("notes"),
        "description": entry.get("description"),
        "description_source": entry.get("description_source"),
        "description_url": entry.get("description_url"),
        "description_sources": entry.get("description_sources"),
        "expected": expected,
        "warnings": [],
        "notes_from_check": [],
        **CATALOG_META,
    }

    if value_range is None:
        return out

    obs_min = value_range.get("min")
    obs_max = value_range.get("max")
    exp_min = expected["compare_min"]
    exp_max = expected["compare_max"]
    manual_min = expected["manual_min"]
    manual_max = expected["manual_max"]

    # Balance series: compare path positions / side max.
    if entry.get("display") == "balance_pair":
        side = entry.get("balance_side_max")
        bal = value_range.get("balance") or {}
        if side is not None and bal.get("side_max") not in (None, side):
            out["notes_from_check"].append(
                f"Balance side max observed {bal.get('side_max')} "
                f"(manual hint {side})"
            )
        if obs_min is not None and exp_min is not None and float(obs_min) != float(exp_min):
            out["notes_from_check"].append(
                f"Balance path low position {obs_min} (hint {exp_min})"
            )
        if obs_max is not None and exp_max is not None and float(obs_max) != float(exp_max):
            out["notes_from_check"].append(
                f"Balance path high position {obs_max} "
                f"(hint 0-{side}/{side}-0 -> 0...{2 * side})"
            )
        out["agreement"] = "match" if not out["notes_from_check"] else "differs_from_hint"
        return out

    if obs_min is None or obs_max is None or exp_min is None or exp_max is None:
        out["agreement"] = "incomplete"
        return out

    cat_unit = expected.get("unit")
    series_unit = unit or value_range.get("unit")
    if cat_unit and series_unit and cat_unit.casefold() != str(series_unit).casefold():
        out["notes_from_check"].append(
            f"Series unit '{series_unit}' differs from catalog hint '{cat_unit}'"
        )

    tol = _tolerance_for(entry)

    # Outside the *compare* window (includes known observed_* expansions).
    if float(obs_min) < float(exp_min) - tol:
        out["notes_from_check"].append(
            f"Observed min {obs_min} is below catalog hint floor {exp_min}"
            + (f" {cat_unit}" if cat_unit else "")
            + " (hardware wins)"
        )
    if float(obs_max) > float(exp_max) + tol:
        out["notes_from_check"].append(
            f"Observed max {obs_max} is above catalog hint ceiling {exp_max}"
            + (f" {cat_unit}" if cat_unit else "")
            + " (hardware wins)"
        )

    # Outside printed manual but inside expanded observed_* — informative only.
    if manual_min is not None and float(obs_min) < float(manual_min) - tol:
        if float(obs_min) >= float(exp_min) - tol:
            out["notes_from_check"].append(
                f"Observed min {obs_min} is below printed manual {manual_min} "
                "(unit/firmware variance; dump is authoritative)"
            )
    if manual_max is not None and float(obs_max) > float(manual_max) + tol:
        if float(obs_max) <= float(exp_max) + tol:
            out["notes_from_check"].append(
                f"Observed max {obs_max} is above printed manual {manual_max} "
                "(unit/firmware variance; dump is authoritative)"
            )

    # Incomplete span vs expanded hint (sparse extremes).
    if float(obs_min) > float(exp_min) + tol:
        out["warnings"].append(
            f"Capture low {obs_min} is above catalog hint min {exp_min} "
            "(extremes may be incomplete)"
        )
    if float(obs_max) < float(exp_max) - tol:
        if not (
            entry.get("display") == "hz_table"
            and value_range.get("high", {}).get("bound") == "above_max_numbered"
        ):
            out["warnings"].append(
                f"Capture high {obs_max} is below catalog hint max {exp_max} "
                "(extremes may be incomplete)"
            )

    if out["warnings"]:
        out["agreement"] = "partial"
    elif out["notes_from_check"]:
        out["agreement"] = "differs_from_hint"
    else:
        out["agreement"] = "match"
    return out


def missing_parameters(captured_folders: list[str]) -> list[dict[str, Any]]:
    """Catalog entries with no matching capture folder yet."""
    captured_ids: set[str] = set()
    for name in captured_folders:
        entry = lookup_parameter(name)
        if entry:
            captured_ids.add(entry["id"])
    return [
        {
            "id": e["id"],
            "name": e["name"],
            "folder_hint": e["folder_hint"],
            "range": _format_range(e),
            "notes": e.get("notes"),
        }
        for e in PROGRAM_PARAMETERS
        if e["id"] not in captured_ids
    ]


def catalog_overview(captured_folders: list[str]) -> dict[str, Any]:
    """Summary for export / cross docs."""
    matched = []
    for name in sorted(captured_folders):
        entry = lookup_parameter(name)
        if entry:
            matched.append(
                {
                    "folder": name,
                    "id": entry["id"],
                    "name": entry["name"],
                    "range": _format_range(entry),
                }
            )
    return {
        **CATALOG_META,
        "program_parameter_count": len(PROGRAM_PARAMETERS),
        "captured": matched,
        "missing": missing_parameters(captured_folders),
    }


def _format_range(entry: dict[str, Any]) -> str:
    if entry.get("display") == "balance_pair":
        side = entry.get("balance_side_max", 20)
        return f"0-{side} / 0-{side} (positions 0...{2 * side})"
    unit = entry.get("unit") or ""
    lo = entry.get("min")
    hi = entry.get("max")
    suffix = f" {unit}" if unit else ""
    extra = ""
    if entry.get("has_off"):
        extra = "; plus Off"
    if entry.get("observed_min") is not None or entry.get("observed_max") is not None:
        olo = entry.get("observed_min", lo)
        ohi = entry.get("observed_max", hi)
        extra += f"; hardware also seen {olo}...{ohi}{suffix}"
    return f"{lo} ... {hi}{suffix}{extra}"


def _tolerance_for(entry: dict[str, Any]) -> float:
    display = entry.get("display")
    if display in {"multiply"}:
        return 1e-6
    if display in {"ms", "integer", "off_plus_integer", "db_cut"}:
        return 0.0
    if display in {"hz_table"}:
        return 0.0
    if entry.get("unit") == "s":
        return 1e-6
    return 1e-6
