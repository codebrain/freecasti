"""Backward-compatible shim — see m7_sysex.prog.byte_map."""
from .prog import byte_map as _impl


def __getattr__(name):
    return getattr(_impl, name)


def __dir__():
    return sorted(set(dir(_impl)))
