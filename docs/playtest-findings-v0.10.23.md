# Access Follow-Through Debrief Note v0.10.23

- **Status:** Phase 7 explanatory debrief wording
- **Date:** 2026-07-08
- **Code version:** 0.10.23
- **Campaign:** `competitive-regional-v1`
- **Prior routing:** `docs/playtest-findings-v0.10.22.md`

This slice implements the bounded follow-up selected in `v0.10.22`: add a
concise competitive debrief explanation for access-heavy runs that separates
public access pledges from durable operational follow-through under cash
pressure.

## Implemented Change

The competitive end-of-run debrief now adds an `Access follow-through note:`
when committed history shows all of the following:

- at least two human access pledges;
- final human cash below the existing cash-risk threshold of `20`;
- fewer durable follow-through actions than access pledges.

Durable follow-through uses committed player commands already visible in
history: recruitment, direct investment, monitoring, payer negotiation, or
capital projects. The note is explanatory and does not use warning language.

## Boundaries

This change does not alter runtime mechanics, access-pledge effects, command
costs, validation rules, difficulty values, scenario schemas, stochastic inputs,
MCP DTOs, replay formats, state hashes, diagnostics, or balance values.

The existing instructor-facing repeated-pledge warning remains unchanged. The
new note is a student-facing debrief explanation for low-cash access-heavy runs,
not a new failure state or calibration claim.

## Evidence Limits

- This wording is supported by simulated-agent and operator-authored evidence,
  not human play or classroom evidence.
- The trigger is a product explanation heuristic over committed history.
- The change helps players interpret public commitments versus operational
  follow-through, but it does not prove balance quality or policy validity.

## Verification

```bash
cargo test debrief::report_tests -- --test-threads=1
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
git diff --check
```
