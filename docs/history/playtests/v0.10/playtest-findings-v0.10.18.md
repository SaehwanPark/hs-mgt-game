# MCP Structured Validation Errors v0.10.18

- **Status:** Phase 7 MCP interface hardening slice
- **Date:** 2026-07-08
- **Code version:** 0.10.18
- **Campaign:** `competitive-regional-v1`
- **Evidence input:** `docs/history/playtests/v0.10/playtest-findings-v0.10.17.md`

This slice implements the follow-up from the live retry cash-pressure
diagnostics: make competitive MCP validation failures machine-classifiable
without requiring live-capture wrappers to parse human-readable error text.

## Interface Change

MCP errors preserve the existing `error` string and may now include optional
structured fields:

- `code`: stable snake_case validation category;
- `resource_limit`: resource name, required amount, and available amount;
- `hint`: short resubmission guidance for resource-limit failures.

Resource-limit payloads are emitted for insufficient cash, AP budget overrun,
and insufficient political capital. Other competitive validation failures get a
stable `code` when they come from the competitive validator. Parser, session,
scenario, and generic errors remain plain unless the server can classify them.

## Interpretation

- The change helps diagnostics and agent wrappers classify rejected live
  decisions before an accepted command stream.
- It does not alter command legality, resources, action costs, transitions,
  replay hashes, scenario formats, or balance values.
- Structured retry metadata remains simulated-agent/operator evidence, not
  human-learning, calibration, or balance proof.

## Follow-Up Routing

- Future live-capture wrappers should prefer `code` and `resource_limit` over
  matching error strings when recording retry metadata.
- Runtime tuning remains deferred until a later evidence slice identifies a
  concrete mechanic problem across stronger evidence than retry friction alone.

## Verification

```bash
cargo test mcp::session::tests::competitive_ --lib
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```
