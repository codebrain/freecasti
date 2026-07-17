# Security policy

## Supported versions

| Version | Supported |
|---------|-----------|
| `main`  | Yes       |

Releases are not tagged separately yet; security fixes land on `main`.

## Reporting a vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Report them privately via [GitHub Security Advisories](https://github.com/codebrain/freecasti/security/advisories/new).

Include:

- A description of the issue and affected components (Python tooling, web UI,
  GitHub Actions workflow, etc.)
- Steps to reproduce, if applicable
- Impact assessment (e.g. remote code execution, data exposure, supply-chain risk)
- Any suggested fix or mitigation

We aim to acknowledge reports within a few business days and will coordinate
disclosure timing with you.

## Out of scope

The following are generally **not** treated as security vulnerabilities for this
project:

- Issues that require physical access to an M7 unit or a user's MIDI setup
- Browser Web MIDI permission prompts behaving as designed
- User-controlled `.syx` files causing unexpected editor state in the browser
  (the editor is a local-first tool; only load SysEx from sources you trust)
- Unofficial reverse-engineered protocol accuracy vs. official Bricasti firmware

## Secure development

Contributors should:

- Avoid committing secrets (API keys, tokens, `.env` files)
- Keep GitHub Actions workflows pinned to major versions where practical
- Run `python -m pytest tests -q` and `cd web-ui && npm test` before merging
  security-sensitive changes
