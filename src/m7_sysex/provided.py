"""Backward-compatible shim — see m7_sysex.prog.provided."""
from .prog import provided as _impl


def __getattr__(name):
    return getattr(_impl, name)


def __dir__():
    return sorted(set(dir(_impl)))
