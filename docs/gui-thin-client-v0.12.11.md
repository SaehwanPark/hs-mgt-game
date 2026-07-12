# GUI Thin-Client Proof — v0.12.11

## Decision

Add one dependency-free browser surface over existing MCP-shaped outputs. The
surface renders actor-visible observations, legal command hints, committed
history/state hashes, and debrief lines. It delegates command legality,
submission, transition, and state ownership to an injected MCP adapter.

## Contract

- Input: `observation`, `legal_commands`, `history`, and `debrief` values from
  existing session/history/debrief boundaries.
- Adapter: `window.HsMgtGameAdapter.submitTurn(commandText)` returns the next
  session envelope.
- Client validation: empty-input checking only; the server remains authoritative
  for command legality.
- State ownership: no simulation state, parser, transition, or network client
  is duplicated in the GUI.
- Assets: zero external assets, fonts, image files, or network calls.

## Verification

- `node --check gui/app.mjs`: passed.
- Adapter contract smoke test: passed.
- Static GUI contract tests: 5 passed.
- Local HTTP serving: `index.html` and `app.mjs` returned successfully.
- In-app browser visual verification: unavailable because the configured browser
  backend reported no available browser in this session; the limitation is
  recorded rather than substituted with an unrelated automation backend.

## Limits

This is a thin-client proof, not a production GUI, hosted application,
accessibility certification, user study, or visual usability claim. CLI/MCP
behavior and the deterministic core remain unchanged.
