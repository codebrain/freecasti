#!/usr/bin/env python3
"""Kick off M7 SysEx analysis + docs export from the repo root.

Usage:

    python run.py                 # full pipeline (analyze + regenerate docs)
    python run.py export          # same as above
    python run.py analyze sysex/predelay
    python run.py cross
    python run.py sheet           # compare _presets to sheet JSON
    python run.py sheet --refresh # re-parse PDF into sheet JSON
    python run.py inventory       # preset inventory summary
    python run.py -h

Adds ``src/`` to ``sys.path`` and chdirs to the repo root so default
``sysex/`` and ``specification/`` paths work without ``pip install -e .``.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"


def main(argv: list[str] | None = None) -> int:
    src = str(SRC)
    if src not in sys.path:
        sys.path.insert(0, src)
    os.chdir(ROOT)

    from m7_sysex.cli import main as cli_main

    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        args = ["export"]
    return cli_main(args)


if __name__ == "__main__":
    raise SystemExit(main())
