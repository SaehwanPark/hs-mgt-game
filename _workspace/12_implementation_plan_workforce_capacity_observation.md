# Implementation Plan — Workforce Capacity Observation Context v0.12.6

## Target slice

Close the v0.12.5 typed-vs-rendered observation gap by projecting the existing
staffing and physical-capacity fields into competitive MCP observations.

## Files

- `src/mcp/session.rs`: add the two safe observation lines and a focused
  session-boundary regression test.
- `Cargo.toml`, `Cargo.lock`, and `README.md`: bump the package milestone to
  `0.12.6`.
- `_workspace/experiments/v0.12.6-workforce-capacity-observation/`: capture and
  audit the compatible matrix against immutable prior source artifacts.
- `tests/test_workforce_capacity_observation.py`: enforce artifact identity,
  projection coverage, hidden-field exclusion, and exact source matches.
- Canonical docs and `LESSONS.md`: record the bounded observation-only result.

## Non-goals

No staffing rules, effective-capacity model, difficulty values, balance,
scoring, transition semantics, command grammar, scenario scope, hidden-state
exposure, or winnability claim.

## Acceptance criteria

- The MCP competitive observation contains the exact `Staffing:` and
  `Physical capacity:` lines from `PlayerObservation`.
- Focused Rust and Python tests pass.
- The compatible 75-run/1,800-transition matrix completes without validation
  failures.
- Histories and state-hash sequences match the immutable v0.11.11 all-tier and
  v0.11.9 Expert controls exactly.
- Full repository checks pass before PR handoff.
