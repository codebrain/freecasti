"""Backward-compatible shim — see m7_sysex.prog.kaitai_spec."""
from .prog import kaitai_spec as _impl


def __getattr__(name):
    return getattr(_impl, name)


def __dir__():
    return sorted(set(dir(_impl)))
