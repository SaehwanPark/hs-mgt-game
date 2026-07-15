# Evidence Map — Live competitive GUI repair v0.12.31

## Repository evidence

- `gui/app.mjs` required `HsMgtGameActionAdapter` or
  `HsMgtGameReadOnlyAdapter`; without one it rendered a fixture and rejected
  session start.
- `src/bin/hs-mgt-game-mcp.rs` exposed only stdio transport.
- `src/mcp/session.rs` already owned all required competitive operations and
  typed actor-visible envelopes.
- Existing session-launch tests injected fake adapters; the v0.12.30 audit
  explicitly excluded browser transport correctness.
- Competitive `get_campaign_coverage` is intentionally unsupported, while the
  live action/read path called it unconditionally.

## Design conclusions

- The gap belongs at the I/O adapter boundary, not in simulation or scenario
  mechanics.
- A same-origin loopback host can reuse `GameSessionStore` without exposing
  private state or duplicating formulas.
- Static demo mode remains useful and must remain distinct from live serving.
- Audio is gesture-gated by design and needs live verification/documentation,
  not core changes.

## Evidence limits

Automated transport and browser-contract checks prove technical integration.
They do not establish human usability, lived accessibility, learning,
calibration, balance, or policy validity.
