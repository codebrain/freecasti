"""Backward-compatible shim — see m7_sysex.prog.analyze."""
from .prog import analyze as _impl


def __getattr__(name):
    return getattr(_impl, name)


def __dir__():
    return sorted(set(dir(_impl)))
