"""Backward-compatible shim — see m7_sysex.prog.decode_preset."""
from .prog import decode_preset as _impl


def __getattr__(name):
    return getattr(_impl, name)


def __dir__():
    return sorted(set(dir(_impl)))
