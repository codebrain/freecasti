"""Backward-compatible shim — see m7_sysex.prog.corpus_layout."""
from .prog import corpus_layout as _impl


def __getattr__(name):
    return getattr(_impl, name)


def __dir__():
    return sorted(set(dir(_impl)))
