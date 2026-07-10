# Final Handoff - Consultant Advice Traceability Evidence

## Summary

Implemented the `v0.10.40` Phase 7 evidence slice. A deterministic 24-run MCP
matrix verifies four rendered consultant options per month against the exact
options retained in committed competitive history and the monthly debrief
record. The MCP transition summary now includes those already-stored options so
the wrapper can audit the same history the debrief uses.

The advisor market remains deferred: no roster, payroll, hiring, firing,
candidate pool, AI advice behavior, scenario schema, balance, or transition
semantics were added.

## Changed Files

- Added the consultant-advice evidence runner, stable result artifact, and
  diagnostic report for four existing profiles, three seeds, and two tiers.
- Added an additive `consultant_options` field to MCP competitive transition
  summaries plus focused coverage for submitted and fetched history.
- Updated Phase 7 findings, playtesting guidance, SDD artifacts, lessons,
  changelog, specification, and package metadata for `v0.10.40`.

## Verification

- `python3 -m py_compile _workspace/experiments/v0.10.40-consultant-advice-evidence/run_sessions.py`
- Generated the 24-run matrix twice; `results.json` was byte-for-byte stable.
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1` (285 tests pass)
- `python3 scripts/run_automated_playtests.py`
- `git diff --check`
- Seed-42 competitive golden hashes remain unchanged.

## Domain QA

Pass. The additive MCP audit field preserves actor-visible observation
boundaries, deterministic transitions, immutable history, debrief traceability,
and explicit deferral of the advisor market.

## Known Limits

- Advice wording is a design abstraction, not evidence of advice quality,
  measured learning, policy validity, or calibrated outcomes.
- The new MCP summary field is additive; strict downstream schemas must accept
  it. Legacy competitive history payloads still deserialize with an empty
  advisory list and cannot reconstruct advice never recorded.

## PR Handoff

- Base branch: `main`
- Working branch: `feat/consultant-advice-evidence-v0.10.40`
- PR: pending creation
- CI and review-loop results: pending PR handoff
- Next dependency: retain the generic advice baseline unless a later,
  separately justified teachability need identifies a limitation.
