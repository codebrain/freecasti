# Contributing

Thank you for helping improve Freecasti and the M7 SysEx specification.
This repository combines Python analysis tooling, generated specification
artifacts, and a static web editor.

## Before you start

- Read the [README](README.md) for project scope and status.
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Check [open issues](https://github.com/codebrain/freecasti/issues) to avoid
  duplicate work.
- For security issues, see [SECURITY.md](SECURITY.md) — please do not file
  public issues for vulnerabilities.

## Ways to contribute

| Area | Examples |
|------|----------|
| **Hardware captures** | New `.syx` dumps for parameters, presets, or system settings |
| **Specification** | Fixes to generated docs after re-export, or analyzer/export code |
| **Web UI** | Editor UX, encode/serialize logic, accessibility, tests |
| **Tests** | Corpus validation, round-trips, regression coverage |
| **Docs** | Capture guides, clarifications, typo fixes in hand-maintained docs |

Hardware captures are especially valuable: the byte map is derived from real
dumps, and every committed `.syx` file is validated in CI.

## Development setup

See [docs/development.md](docs/development.md) for full commands. Quick path:

```bash
pip install -e ".[dev]"
python run.py
python -m pytest tests -q

cd web-ui
npm install
npm test
npm run build
```

Requirements: Python 3.11+, Node 20+ for the web UI, Java (or
`kaitai-struct-compiler`) when compiling Kaitai parsers.

## Pull request guidelines

1. **Open an issue first** for large changes (new subsystems, broad refactors,
   or controversial spec interpretations). Small fixes and capture PRs can
   skip this.
2. **Branch from `main`** and keep PRs focused. Prefer several small PRs over
   one large one.
3. **Run tests** before opening a PR:
   - `python -m pytest tests -q`
   - `cd web-ui && npm test` when touching the UI or encode paths
4. **Regenerate derived files** when your change affects analysis or export:
   ```bash
   python run.py
   ```
   Commit the updated `specification/`, `sysex/**/analysis.json`, and
   `web-ui/public/` / `web-ui/src/generated/` outputs together with your
   source changes.
5. **Do not hand-edit generated artifacts** unless the generator itself cannot
   express the fix. Typical generated paths:
   - `specification/` (except when fixing export code)
   - `sysex/**/analysis.json`
   - `web-ui/public/m7-runtime.json`
   - `web-ui/src/generated/`
6. **Write clear commit messages** — what changed and why, not just which
   files moved.
7. **License** — by contributing, you agree that your contributions are
   licensed under the [Apache License 2.0](LICENSE).

## Contributing SysEx captures

Follow [docs/capture-guide.md](docs/capture-guide.md) and the filename
conventions in the README.

**Program parameters** (`sysex/prog/parameters/<name>/`):

- Change **only one** parameter per series.
- Include extremes, adjacent-to-extreme settings, and a sparse sample of mids.
- Name files after the value (`off.syx`, `120hz.syx`, `high.syx`, etc.).

**Factory presets** (`sysex/prog/presets/`):

- Use `<bank>.<preset>.syx`.
- Offsets 8–87 must match the preset name (ASCII, space-padded to 80 bytes).
  The display name lives at 8–23; factory dumps space-pad 24–87. Reg-backed
  hold-EDIT dumps put a basis blob at 24–87 instead — capture those under
  `sysex/prog/edit/registers/`, not `presets/`.

**System settings** (`sysex/system/<setting>/`):

- One folder per setting; same labeling discipline as program parameters.

After adding dumps, run `python run.py` and include regenerated outputs in
your PR. The test suite validates every committed `.syx` file.

## Contributing to the web UI

- Do not edit `web-ui/src/generated/` or `web-ui/public/m7-runtime.json`
  by hand — run `python run.py` from the repo root.
- Match existing TypeScript/React style in surrounding files.
- Add or update Vitest tests for encode/serialize behavior you change.
- UI copy for the product is **Freecasti**; the hardware is **Bricasti M7**.

## Code review

Maintainers may request changes, ask for additional captures, or suggest
splitting a PR. Reviews focus on correctness against hardware dumps, test
coverage, and clarity of generated documentation.

## Trademark note

This is an **unofficial** community effort. Bricasti and M7 are trademarks of
their respective owners. Do not imply endorsement by Bricasti or Future
State Studios unless you are explicitly authorized to do so.
