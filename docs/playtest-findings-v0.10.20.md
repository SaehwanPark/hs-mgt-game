# Live Retry Visibility Checkpoint v0.10.20

- **Status:** Phase 7 evidence-routing checkpoint
- **Date:** 2026-07-08
- **Code version:** 0.10.20
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/playtest-findings-v0.10.16.md`
  - `docs/playtest-findings-v0.10.17.md`
  - `docs/playtest-findings-v0.10.18.md`
  - `docs/playtest-findings-v0.10.19.md`
- **Exemplar artifact:** `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- **Diagnostic report:** `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`

This checkpoint closes the current live retry visibility gate selected in
`v0.10.16`. The project now has enough structured retry metadata to distinguish
accepted command streams from rejected cash-overrun attempts in current
live-capture artifacts without changing runtime mechanics.

## What Is Now Complete

- `v0.10.17` added diagnostic reporting for optional
  `live_validation_retries`, separating live command-selection friction from
  final replay validation failures.
- `v0.10.18` added additive structured MCP validation fields for competitive
  resource-limit errors while preserving the plain `error` string.
- `v0.10.19` preserved those structured fields in Python live-capture artifacts
  and updated diagnostics to prefer structured cash-retry classification with
  legacy fallback.

## Current Interpretation

The retry signal is now a visible tooling and evidence-quality signal, not a
runtime balance conclusion. The `v0.10.15` exemplar still shows that the Live
Access Operator encountered cash-pressure retries under Normal and Hard
difficulty, but the accepted command streams completed cleanly and replayed
without final validation failures.

Structured metadata reduces ambiguity in future evidence review by making these
cases explicit:

- cash-overrun retries can be counted from `resource_limit.resource == "cash"`
  or `code == "insufficient_cash"`;
- non-cash validator errors can remain visible through `code` and `error`;
- wrapper-only failures can remain string-only when no MCP validation payload is
  available.

## Follow-Up Routing

- Continue preserving structured retry fields in live-capture artifacts.
- Use retry counts as evidence for guidance, debrief, or command-surface review,
  not as standalone proof that balance formulas are wrong.
- Defer runtime tuning, command-cost changes, access-pledge cooldowns, and
  difficulty adjustments until a later evidence slice identifies a concrete
  mechanic problem beyond retry classification.
- If development continues immediately, prefer a new bounded evidence question
  from `SPEC.md` Future rather than expanding the retry metadata path again.

## Evidence Limits

- This checkpoint uses simulated-agent and operator-authored evidence, not human
  play, classroom learning evidence, empirical calibration, or policy-validity
  evidence.
- The strongest live retry signal still comes from one campaign, a small set of
  profiles, and the `v0.10.15` seed `42` exemplar.
- Diagnostic classification depends on captured metadata and debrief-derived
  summaries; it does not expose hidden active-play state.

## Verification

```bash
python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.20-diagnostics.md
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```
