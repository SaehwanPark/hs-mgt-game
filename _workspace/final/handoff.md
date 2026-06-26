# Handoff

## Changed Files

- Added MCP server and in-memory session adapter in `src/mcp/`.
- Added stdio binary `src/bin/hs-mgt-game-mcp.rs`.
- Updated package version and dependencies in `Cargo.toml` / `Cargo.lock`.
- Updated `README.md`, `ARCHITECTURE.md`, `SPEC.md`, `CHANGELOG.md`.
- Added `docs/mcp-agent-interface.md` and ADR-0008.
- Updated workspace request, mechanism, QA, and handoff artifacts.

## Verification

- `cargo check --bin hs-mgt-game-mcp`
- `cargo test`
- `cargo fmt --check`

## Known Limits

- MCP supports stdio only.
- Sessions are in memory only.
- Competitive support remains the bounded three-month preview.
- No replay artifact format changes.

## Next Dependencies

Use external agent playtests before adding HTTP transport, auth, durable MCP
session persistence, full competitive campaign length, or replay/export
integration.
