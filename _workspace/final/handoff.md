# Final Handoff - MCP Structured Validation Errors

## Summary

Implemented the `v0.10.18` Phase 7 MCP interface hardening slice. Competitive
MCP validation errors now preserve the existing plain `error` string and may add
optional structured fields for error code, resource-limit details, and
resubmission hints.

This is an additive MCP adapter change. It does not change transition logic,
command grammar, validation rules, scenario schemas, replay hashes, state hash
logic, action costs, ruleset values, or balance.

## Changed Files

- `src/mcp/session.rs`: optional structured validation error fields and focused
  session tests.
- `docs/mcp-agent-interface.md` and `docs/mcp-playtesting-guide.md`: additive
  error shape and live-capture routing notes.
- `docs/playtest-findings-v0.10.18.md`: slice findings and follow-up routing.
- `SPEC.md`, `CHANGELOG.md`, `Cargo.toml`, `Cargo.lock`: `v0.10.18` record and
  package metadata.
- `_workspace/00_input/request-summary.md`: harness request framing.

## Verification

- `cargo test mcp::session::tests::competitive_ --lib`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`

## PR Handoff

- Branch: `feat/mcp-structured-validation-errors`
- Base: `main`
- PR: https://github.com/SaehwanPark/hs-mgt-game/pull/99

## Review Summary

- Pass 1: No blocking MCP adapter, docs, versioning, or test issues.
- Pass 2: Low numeric hardening finding: resource-limit payloads used `i32`
  while AP and political-capital validator fields are `u32`. Fixed by using
  `i64` payload values with lossless conversions.
- Pass 3: No further code, documentation, or scope findings.
- Critical/High findings: none.
- Medium/Low disposition: one Low finding fixed before PR handoff.
- Follow-up review after Critical/High fixes: not required.
- CI/comment triage: GitHub Actions `check` passed on PR #99; no PR comments
  or reviews were present during triage.
- Merge-ready: yes.

## Known Limits

- Parser, session, scenario, and generic errors may still expose only `error`.
- Structured fields are additive and optional; clients must not require them for
  all error cases.
- Runtime tuning remains deferred until stronger evidence identifies a concrete
  mechanic problem.
