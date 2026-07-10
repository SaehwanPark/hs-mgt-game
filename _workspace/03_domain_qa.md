# Domain QA - Live Consultant Advice and Advisory History

## Status

pass

## Reviewed Inputs

- `SPEC.md` v0.10.39 completion entry and Future promotion rules.
- `_workspace/00_input/request-summary.md` and
  `_workspace/02_mechanism_design.md`.
- `src/sim/observe_competitive.rs`, `src/competitive/month_loop.rs`,
  `src/model/competitive_history.rs`, `src/mcp/session.rs`, and
  `src/debrief/report.rs`.
- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, and the harness team specification.

## Findings

- The slice is bounded to decision support and history; it does not promote the
  deferred advisor market, payroll, hiring, or a new strategic actor.
- Consultant options are generated from `PlayerObservation` only and retain
  visible uncertainty and tradeoffs without hidden rival state or outcome
  guarantees.
- The exact options shown are stored on committed competitive transitions,
  preserving append-only debrief traceability and serialized session recovery.
- The deterministic transition core and state hash remain unchanged; advice is
  captured before the month-start working-state mutation.
- CLI and MCP observations use the same generator, while AI decision behavior
  remains unchanged and symmetric future advisor-market requirements remain
  deferred.

## Required Fixes

- None.

## Residual Risks

- Advice wording is a gameplay abstraction and has not been validated as an
  educational intervention or calibrated policy guidance.
- Competitive history JSON now contains an optional advisory field; legacy
  payloads default to an empty list and therefore cannot reconstruct advice
  that was never recorded.

## Verification Evidence

- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1` (285 tests pass)
- `cargo test --lib competitive_session_save_round_trip_fields`
- `python3 scripts/run_automated_playtests.py`
- `git diff --check`
