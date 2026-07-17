"""Backward-compatible shim — see m7_sysex.prog.preset_sheet."""
from .prog import preset_sheet as _impl


def __getattr__(name):
    return getattr(_impl, name)


def __dir__():
    return sorted(set(dir(_impl)))
