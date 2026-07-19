#!/usr/bin/env python3
"""Build and preview the M7 web UI from the repo root.

Runs the web-ui pipeline end-to-end:

  1. Sync ``specification/`` into ``web-ui/public/m7-runtime.json`` (+ param manifest)
  2. ``npm install`` when ``node_modules/`` is missing
  3. ``npm run build`` (Kaitai compile + Vite production bundle)
  4. ``vite preview`` serving ``web-ui/dist/``
  5. Open the default browser

Usage::

    python web.py
    python web.py --port 8080
    python web.py --skip-build      # preview existing dist/
    python web.py --export          # run full ``python run.py`` first
    python web.py --no-open
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
WEB_UI = ROOT / "web-ui"
DEFAULT_PORT = 4173


def _setup_path() -> None:
    src = str(SRC)
    if src not in sys.path:
        sys.path.insert(0, src)
    os.chdir(ROOT)


def _npm() -> str:
    npm = shutil.which("npm")
    if not npm:
        raise SystemExit("npm not found on PATH — install Node.js 20+")
    return npm


def _run(cmd: list[str], *, cwd: Path) -> None:
    print(f"+ {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def _sync_public() -> None:
    from m7_sysex.export.web_ui import sync_web_ui_assets

    written = sync_web_ui_assets(ROOT)
    print(f"synced {len(written)} web-ui asset(s) into web-ui/public/")


def _ensure_node_modules() -> None:
    if (WEB_UI / "node_modules").is_dir():
        return
    _run([_npm(), "install"], cwd=WEB_UI)


def _build() -> None:
    _run([_npm(), "run", "build"], cwd=WEB_UI)


def _wait_for_http(url: str, *, timeout: float = 90) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, OSError, TimeoutError):
            time.sleep(0.25)
    raise TimeoutError(f"preview server did not respond at {url}")


def _preview(port: int, *, open_browser: bool) -> int:
    url = f"http://127.0.0.1:{port}/"
    cmd = [_npm(), "run", "preview", "--", "--host", "127.0.0.1", "--port", str(port)]
    print(f"+ {' '.join(cmd)}", flush=True)
    proc = subprocess.Popen(cmd, cwd=WEB_UI)
    try:
        _wait_for_http(url)
        print(f"\nM7 web UI: {url}\nPress Ctrl+C to stop.\n", flush=True)
        if open_browser:
            webbrowser.open(url)
        return proc.wait()
    except KeyboardInterrupt:
        print("\nStopping preview server…", flush=True)
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        return 0
    except Exception:
        proc.terminate()
        raise


def main(argv: list[str] | None = None) -> int:
    _setup_path()

    parser = argparse.ArgumentParser(description="Build and preview the M7 web UI.")
    parser.add_argument(
        "--export",
        action="store_true",
        help="Run full python run.py export before syncing web-ui assets",
    )
    parser.add_argument(
        "--skip-sync",
        action="store_true",
        help="Skip syncing specification assets into web-ui/public/",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip npm run build (serve existing dist/)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Preview server port (default {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not open a browser tab",
    )
    args = parser.parse_args(argv)

    if not WEB_UI.is_dir():
        raise SystemExit(f"missing web-ui directory: {WEB_UI}")

    if args.export:
        _run([sys.executable, str(ROOT / "run.py"), "export"], cwd=ROOT)
    elif not args.skip_sync:
        _sync_public()

    _ensure_node_modules()

    if not args.skip_build:
        _build()

    dist_index = WEB_UI / "dist" / "index.html"
    if not dist_index.is_file():
        raise SystemExit(
            f"missing {dist_index} — run without --skip-build or build web-ui manually"
        )

    return _preview(args.port, open_browser=not args.no_open)


if __name__ == "__main__":
    raise SystemExit(main())
