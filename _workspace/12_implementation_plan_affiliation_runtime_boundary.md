# Implementation Plan — Affiliation Runtime Boundary Proposal v0.12.7

## Target slice

Reconcile the affiliation-first design gate with the existing opt-in runtime.
Verify that the minimum state, observation, resolved-input, deterministic
transition, history/replay, and debrief contracts are implemented and visible
in the owning source boundaries.

## Files

- `docs/affiliation-runtime-boundary-v0.12.7.md`: durable proposal decision and
  limits.
- `_workspace/experiments/v0.12.7-affiliation-runtime-boundary-proposal/`:
  source-marker and evidence-contract artifact.
- `tests/test_affiliation_runtime_boundary.py`: focused structural and artifact
  tests.
- Canonical docs, `SPEC.md`, and `LESSONS.md`: close the stale proposal queue
  entry and record that no new runtime change is authorized.

## Non-goals

No new Rust types, commands, scenario fields, state-hash fields, replay format,
actor framework, deal financing, legal forecast, or change to
`competitive-regional-v1`.

## Acceptance criteria

- All minimum contract source markers are supported.
- The existing v0.12.2 affiliation artifact remains 9/9 complete and 54/54
  stages with typed observation context.
- The proposal explicitly authorizes no new runtime change and preserves
  deferred scope.
- Focused Python and full repository checks pass.
