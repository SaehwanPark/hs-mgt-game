# Operational Coding Plan - Regional Affiliation Observation Context v0.12.2

## Task restatement

Close the v0.12.1 MCP observation-context gap by rendering the existing typed
affiliation commitments, alternatives, and assumptions in the player-facing
`regional-affiliation-v1` observation, while preserving all simulation and
replay semantics.

## Current understanding

- `src/affiliation/observe.rs` already supplies the three safe context fields.
- `src/mcp/session.rs::format_affiliation_observation` is the only current MCP
  projection path and omits those fields.
- Existing v0.12.1 evidence proves the omission across 9 runs; its artifact must
  remain immutable while a new post-fix artifact records v0.12.2.

## Assumptions

- The typed observation fields are safe to expose because they contain player
  commitments, scenario alternatives, and explicit abstraction assumptions.
- No transition or state-hash code must change.
- Existing `scripts/play_game.py` and the v0.12.1 runner can be reused for the
  same matrix without a new dependency.

If any assumption is false, stop and report the mismatch before broadening the
slice.

## Minimal implementation plan

1. Add `Commitments:`, `Alternative:`, and `Assumption:` lines to the MCP
   affiliation observation formatter using only `AffiliationObservation`.
2. Add a Rust session-boundary test for initial, choose-posture, and post-
   commitment observations; assert the exact safe labels and values.
3. Add a small v0.12.2 post-fix capture wrapper that reuses the v0.12.1 policy
   matrix, validates the same 9 coordinates/54 stages, and requires zero
   missing typed context fields.
4. Update SPEC, changelog, README, architecture, roadmap, lessons, findings,
   and handoff; bump package metadata to `0.12.2`.
5. Run focused tests, regenerate the post-fix artifact, then run all repository
   checks and three review passes before PR merge.

## Files and functions likely to change

- `src/mcp/session.rs`: `format_affiliation_observation` and focused tests.
- `_workspace/experiments/v0.12.2-affiliation-observation-context/run_sessions.py`:
  post-fix capture/audit wrapper.
- `_workspace/experiments/v0.12.2-affiliation-observation-context/results.json`
  and `diagnostics.md`: committed post-fix evidence.
- `tests/test_affiliation_observation_context.py`: artifact contract tests.
- `SPEC.md`, `CHANGELOG.md`, `README.md`, `ARCHITECTURE.md`, `docs/roadmap.md`,
  `docs/playtest-findings-v0.12.2.md`, `LESSONS.md`, and workspace handoffs.
- `Cargo.toml` and `Cargo.lock`: version `0.12.2`.

Avoid editing transition, model, input, scenario, replay, or hash modules. If
the projection cannot be fixed at the MCP formatter boundary, stop and report
the structural conflict.

## Tests and checks

- `cargo test mcp::session::tests::affiliation_observation_includes_context`
- `python3 -m unittest tests/test_affiliation_observation_context.py`
- `python3 _workspace/experiments/v0.12.2-affiliation-observation-context/run_sessions.py`
- `cargo test --all -- --test-threads=1`
- `cargo test --test golden_competitive_seed42 -- --test-threads=1`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `git diff --check`

## Acceptance criteria

- Every affiliation MCP observation includes the three explicit context labels
  sourced from the typed observation.
- The v0.12.2 matrix has 9/9 complete runs, 54 stages, zero validation
  failures, and zero missing typed context fields.
- Competitive golden hashes and affiliation transition/state hashes are
  unchanged by the presentation-only change.
- No hidden partner state, actor utility, or future outcome is rendered.
- Package/docs identify v0.12.2 and the v0.12.1 gap is recorded as closed.

## Non-goals

- Do not change commands, transitions, rulesets, numeric thresholds, balance,
  actor responses, replay/hash schemas, GUI, or scenario data.
- Do not add a generic observation renderer or new dependency.
- Do not claim human comprehension, educational effectiveness, winnability,
  legal validity, or calibration.

## Stop conditions

- Stop if exposing a requested field requires reading true state or hidden actor
  utility rather than the typed observation.
- Stop if any state hash, replay contract, or competitive golden path changes.
- Stop if more than the named MCP/test/artifact/doc files require production
  edits or if a broader abstraction appears necessary.

## Review checklist

- All three labels come only from `AffiliationObservation`.
- Alternatives are stage-appropriate and assumptions remain visibly stylized.
- Commitments show player state and total without hidden partner data.
- Rust tests exercise the actual `SessionEnvelope` observation surface.
- v0.12.1 remains immutable; v0.12.2 post-fix evidence is separate.
- Full checks pass and docs do not overclaim educational or policy evidence.

## Risk label

Risk: Low

Reason: This is a localized read-only MCP presentation change with focused
boundary tests and no transition, persistence, or public command semantics.
