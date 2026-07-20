# Operational Coding Plan - Regional Affiliation Playtest Validation v0.12.1

## Task restatement

Capture and audit nine deterministic `regional-affiliation-v1` MCP sessions—
three observation-driven policies across seeds 42, 43, and 44—while preserving
all runtime transitions, replay contracts, and the competitive seed-42 golden
path.

## Current understanding

- `scripts/play_game.py` already provides an MCP client and trace wrapper.
- Affiliation observations and six-stage transitions are implemented in
  `src/model/affiliation.rs`, `src/affiliation/`, and `src/mcp/session.rs`.
- The typed observation contains more context than the MCP formatter currently
  renders; the audit should identify this only as a player-facing evidence gap.
- Existing Phase 7 artifacts use committed JSON, a deterministic audit module,
  a Markdown renderer, and focused Python contract tests.

## Assumptions

- The local MCP binary can run all nine sessions using the existing command
  parser and deterministic seed streams.
- The existing six-stage schedule is the authoritative completion contract.
- No state transition or ruleset change is needed to answer the evidence
  question.

If any assumption is false, stop and report the mismatch before editing runtime
code or broadening the artifact.

## Minimal implementation plan

1. Add a capture runner for the exact 3-profile × 3-seed matrix. Use only
   actor-visible observations and legal command hints; omit process-specific
   session IDs from persisted output.
2. Add deterministic validation and Markdown rendering for matrix identity,
   six-stage history/hash alignment, accepted-command trace linkage, validation
   failure separation, actor-response coverage, and debrief continuity.
3. Record the repeated omission of typed observation context from the MCP
   surface as one concrete gap, while keeping runtime promotion deferred for
   balance and ruleset changes.
4. Add focused Python tests using the committed artifact and malformed/partial
   fixtures; update `SPEC.md`, `CHANGELOG.md`, README, roadmap, and handoff.
5. Run the focused artifact tests, the capture/audit, the complete Rust and
   Python suites, formatting, clippy, golden replay, and diff checks.

## Files and functions likely to change

- `_workspace/00_input/request-summary.md`: current slice contract.
- `_workspace/01_evidence_map.md`: evidence and limits.
- `_workspace/02_mechanism_design.md`: capture boundary and debrief hooks.
- `_workspace/experiments/v0.12.1-affiliation-playtest-validation/run_sessions.py`:
  matrix capture, validation, audit, and rendering.
- `_workspace/experiments/v0.12.1-affiliation-playtest-validation/results.json`:
  deterministic committed capture.
- `_workspace/experiments/v0.12.1-affiliation-playtest-validation/diagnostics.md`:
  rendered audit.
- `tests/test_affiliation_playtest_validation.py`: focused artifact contract
  tests.
- `docs/history/playtests/v0.12/playtest-findings-v0.12.1.md`, `SPEC.md`, `CHANGELOG.md`, `README.md`,
  `docs/roadmap.md`, and `_workspace/final/handoff.md`: synchronized project
  state.
- `Cargo.toml` and `Cargo.lock`: patch version `0.12.1`.

Avoid editing Rust runtime files unless the capture exposes an existing defect
that prevents the planned matrix from running. If that happens, stop and report
the conflict rather than silently expanding this slice.

## Tests and checks

- `python3 -m unittest tests/test_affiliation_playtest_validation.py`
- `python3 _workspace/experiments/v0.12.1-affiliation-playtest-validation/run_sessions.py --output ... --diagnostics ...`
- `cargo test --all -- --test-threads=1`
- `cargo test --test golden_competitive_seed42 -- --test-threads=1`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `git diff --check`

Expected result: nine complete six-stage runs, deterministic audit output, no
unexpected validation failures, and no change to competitive golden hashes.

## Acceptance criteria

- The artifact contains exactly each profile/seed coordinate once.
- Every run has six ordered transitions, six pre-command observations, aligned
  state hashes, and a complete affiliation debrief.
- The audit reports Riverside outcomes separately from partner/review/labor/
  payer/community response labels.
- The audit records one concrete repeated decision-time observation-context gap
  and explicitly avoids a human-learning or winnability claim.
- No Rust transition, scenario, command, replay, or state-hash behavior changes.
- Package metadata and project docs identify version `0.12.1`.

## Non-goals

- Do not tune thresholds, commitment costs, balance, or difficulty.
- Do not add a generalized analytics framework or GUI.
- Do not claim human comprehension, educational effectiveness, winnability,
  legal validity, calibration, or policy forecasting.
- Do not modify the competitive campaign or its golden state hash.

## Stop conditions

- Stop if the MCP client cannot complete a profile without an implementation
  change to the affiliation runtime.
- Stop if the artifact requires storing true state or hidden actor utility that
  the player would not observe.
- Stop if more than the named artifact/docs/test files require production-code
  edits or if the output cannot be made deterministic without a new dependency.
- Stop before promoting any runtime tuning from this evidence-only slice.

## Review checklist

- The matrix is exact and reproducible across all nine coordinates.
- Observations are captured before commands and never replaced by post-turn
  state.
- History/state-hash/debrief links are complete and deterministic.
- Actor responses are not mislabeled as Riverside outcomes or social welfare.
- The concrete observation-context gap is grounded in typed-vs-rendered fields.
- Evidence limits and deferred work are explicit.
- No runtime semantics or competitive golden contract changed.

## Risk label

Risk: Medium

Reason: The slice is read-only with respect to simulation semantics, but it adds
an evidence contract and can influence the next interface decision if source
boundaries are not kept explicit.
