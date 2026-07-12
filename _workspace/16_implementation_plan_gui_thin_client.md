# Implementation Plan — GUI Thin-Client Proof v0.12.11

## Target slice

Prototype one dependency-free browser surface that consumes existing MCP-shaped
observation, legal-command, history/replay, and debrief outputs.

## Files

- `gui/index.html`, `gui/app.mjs`, `gui/README.md`: thin client and adapter
  contract.
- `tests/test_gui_thin_client.py`: static and JavaScript contract tests.
- `docs/gui-thin-client-v0.12.11.md`: scope, asset audit, and verification.
- `SPEC.md`, canonical docs, and `LESSONS.md`: close the GUI Future item.

## Non-goals

No simulation state, parser, transition, network service, authentication,
production hosting, downloaded assets, GUI-only scenario behavior, or CLI/MCP
replacement.

## Acceptance criteria

- Observation, command hints, history/state hashes, and debrief render targets
  exist in the surface.
- Submission delegates to an injected adapter and does not duplicate rules.
- No external assets or network calls are bundled.
- JavaScript syntax, static contract tests, and local HTTP serving pass.
- Browser visual limitation is recorded if the configured browser is unavailable.
