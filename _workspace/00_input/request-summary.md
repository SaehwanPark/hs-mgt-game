# Request Summary - Regional Affiliation Playtest Validation v0.12.1

## Scope

- Continue from merged PR #153 and the completed v0.12.0 runtime slice.
- Capture deterministic MCP playtest traces for the opt-in
  `regional-affiliation-v1` campaign across independent, deferred, and pursuit
  postures at seeds 42, 43, and 44.
- Audit decision-time observations, legal commands, committed history/state
  hashes, resolved actor responses, and affiliation debrief continuity.
- Identify at most one concrete player-facing or educational evidence gap for a
  later bounded slice; keep this change read-only with respect to simulation
  transitions.

## Non-goals

- No changes to competitive or affiliation transition semantics, rulesets,
  state-hash schemas, replay formats, command parsing, or balance.
- No direct acquisition, national deal market, private-equity rollup, detailed
  transaction finance, calibrated legal outcome, or policy forecast.
- No human-learning, classroom-effectiveness, general winnability, calibration,
  or policy-validity claim.
- No GUI, AI-rival affiliation behavior, autosave expansion, or broad evidence
  framework.

## Sources

- `README.md`, `docs/proposal.md`, `docs/roadmap.md`, and
  `docs/design_principles.md`.
- `SPEC.md`, `docs/system-boundary.md`, `docs/scenario-format-draft.md`,
  `docs/decision-records/0010-regional-affiliation-runtime-slice.md`, and the
  v0.12.0 workspace artifacts.
- Current affiliation Rust state, observation, MCP, replay, and debrief code.
- No new external evidence is introduced; this is a validation artifact.

## Expected files

- `_workspace/experiments/v0.12.1-affiliation-playtest-validation/` capture,
  deterministic audit, and diagnostics.
- `tests/test_affiliation_playtest_validation.py` for artifact contracts.
- `docs/playtest-findings-v0.12.1.md`, `SPEC.md`, `CHANGELOG.md`, README, and
  synchronized roadmap/handoff notes.
- `Cargo.toml` and `Cargo.lock` for the patch-level `0.12.1` increment.

## Validation target

- The 3-profile × 3-seed matrix contains 9 complete six-stage runs with no
  unexpected validation failures.
- Every accepted command links to one actor-visible observation, one transition
  summary/state hash, and one debrief stage line.
- The audit distinguishes Riverside outcomes from partner, review, labor,
  payer, and community responses and records a concrete observation-context gap
  if the MCP surface omits fields exposed by the typed observation.
- Domain QA returns `Pass` for the evidence-only artifact.
- Existing Rust, Python, formatting, clippy, golden, and diff checks pass.
