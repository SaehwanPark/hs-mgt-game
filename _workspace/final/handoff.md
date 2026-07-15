# Final Handoff — Live competitive GUI repair v0.12.31

## Result

The competitive GUI is playable from a normal checkout with:

```bash
cargo run --bin hs-mgt-game-gui
```

The binary prints a loopback URL, serves the existing browser client, injects a
same-origin adapter, and delegates start/read/validate/submit/resolution work to
the existing authoritative session store.

## Changed areas

- Rust: loopback-only Axum server, embedded GUI assets, narrow competitive start
  DTO, binary entry point, and real transport tests.
- Browser: same-origin action adapter, live-without-session demo bootstrap,
  transactional active-session replacement, and competitive coverage fix.
- Player docs: README quickstart, shared How to Play routing, canonical GUI
  guide/troubleshooting, and developer adapter reference.
- Project records: ADR-0012, proposal/roadmap/spec/architecture/changelog,
  lessons, handoffs, and v0.12.31 metadata.

## Verification

- 316 Python tests passed; 81 are GUI-focused.
- 328 Rust library tests and all binary/integration/golden/scenario/doctest
  targets passed.
- Release metadata, Node syntax, Rust formatting, Clippy, and diff checks pass.
- A real `127.0.0.1:8787` process served the injected page and started a seed-42
  Normal competitive session.

## Review and deviations

- Code review found one initial security/scope issue: the HTTP start request
  reused MCP `scenario_path`. The final implementation uses a narrow DTO,
  rejects unknown fields and noncompetitive campaigns, and never accepts a
  scenario path.
- No implementation deviations from the approved functional scope remain.

## Known limits

- Competitive GUI only; use the CLI for other or custom scenarios.
- Sessions are process-local and nonpersistent.
- No remote hosting, authentication, multiplayer, packaging, or production
  deployment.
- Viewport, screen-reader, and hardware-audio verification remains unclaimed
  because the configured in-app browser controller was unavailable.
