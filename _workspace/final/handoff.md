# Final Handoff - Consultant Advice Usage Evidence

## Summary

Implemented the `v0.10.41` Phase 7 evidence slice. A deterministic 24-run
matrix compares advice-aware and advice-ignoring competitive policies across
Fiscal Caution and Naive First-Time profiles, seeds 42–44, and Normal/Hard
difficulty.

Advice-aware policies read only visible consultant options and resource hints,
record selection, fallback, safe-hold, and command-alignment signals, and never
inspect hidden state. Advice-ignoring controls match the v0.10.40 state hashes.

The advisor market remains deferred: no roster, payroll, hiring, firing,
candidate pool, AI advisor, scenario, balance, or transition semantics were
added.

## Changed Files

- Added the advice-usage runner, deterministic result artifact, diagnostics, and
  focused Python tests.
- Added v0.10.41 findings, playtesting-guide routing, SDD evidence handoffs,
  domain QA, lessons, changelog, specification, and package metadata.

## Verification

- `python3 -m unittest discover -s tests -p 'test_*.py'` (9 tests pass)
- `python3 -m py_compile _workspace/experiments/v0.10.41-consultant-advice-usage/run_sessions.py tests/test_consultant_advice_usage.py`
- Generated the 24-run matrix twice; `results.json` and `diagnostics.md` were
  byte-for-byte stable.
- All 24 runs completed 24 months with zero validation failures, exact option
  continuity, and 24 debrief records per run.
- Advice-ignoring controls matched v0.10.40 hashes.
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1` (285 tests pass)
- `python3 scripts/run_automated_playtests.py`
- `git diff --check`

## Domain QA

Pass. The slice preserves actor-visible observation boundaries, deterministic
transitions, immutable history, debrief traceability, and explicit deferral of
the advisor market. Policy differences are not interpreted as causal advice
evidence.

## Known Limits

- Advice wording and policy selection remain design abstractions, not evidence
  of advice quality, measured learning, policy validity, or calibrated outcomes.
- Advice-aware endpoint differences reflect intentionally different commands and
  are not a causal comparison.
- Safe-hold fallback uses visible resource guards and does not prove that the
  underlying policy would be valid under hidden state.

## PR Handoff

- Base branch: `main`
- Working branch: `feat/consultant-advice-usage-v0.10.41`
- PR: pending creation after the implementation commit
- Review loop: pending
- Merge-ready: no, until the PR is open and three independent review passes are
  complete.
- Next dependency: retain the generic advice baseline unless later evidence
  identifies a concrete teachability limitation.
