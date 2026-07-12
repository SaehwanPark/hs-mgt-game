# Operational Coding Plan - Phase 7 Teachability Evidence Review v0.12.3

## Task restatement

Audit the two current Phase 7 evidence lanes for decision-to-debrief trace
coherence and source-specific context, then record whether a concrete gap
justifies another bounded change. Read committed artifacts only.

## Current understanding

- The v0.12.2 affiliation artifact contains 9 complete six-stage runs with
  post-fix commitments, alternatives, assumptions, hashes, and debrief lines.
- The v0.11.12 competitive artifact contains 9 complete hard-difficulty
  24-month runs with observation, command, transition, hash, consultant,
  advisory, and debrief records.
- The competitive campaign was not changed by v0.12.2; its source version and
  golden control hash must remain pinned in the report.

## Assumptions

- The two JSON artifacts are immutable historical sources.
- Source-specific marker checks are the correct contract; the report will not
  force identical terminology across campaigns.
- A supported trace is evidence of inspectable continuity only, not evidence of
  human learning, balance, winnability, or strategy quality.

If a source cannot satisfy its declared contract without inference or a new
capture, stop and report the limitation rather than broadening the task.

## Minimal implementation plan

1. Add a deterministic audit script with explicit contracts for both artifacts.
2. Validate source identity, matrix, completeness, trace fields, history/hash
   alignment, source-specific context, and debrief markers.
3. Emit a compact JSON report and diagnostics table with per-source and
   aggregate counts, missing steps, gaps, and evidence limits.
4. Add focused Python tests for success, malformed source rejection, missing
   marker detection, and deterministic report rendering.
5. Update findings, SPEC, changelog, README, architecture, roadmap, lessons,
  version metadata, and final handoff; run all repository checks.
6. If CI exposes a pre-existing shared-test filesystem race, add only a
   test-scoped synchronization guard and rerun the default parallel suite.

## Files and functions likely to change

- `_workspace/experiments/v0.12.3-phase7-teachability-review/run_audit.py`.
- `_workspace/experiments/v0.12.3-phase7-teachability-review/results.json` and
  `diagnostics.md`.
- `tests/test_phase7_teachability_review.py`.
- `src/cli/persistence.rs` only for a test-scoped shared-path isolation guard
  if CI requires it.
- `docs/playtest-findings-v0.12.3.md`, `SPEC.md`, `CHANGELOG.md`, `README.md`,
  `ARCHITECTURE.md`, `docs/roadmap.md`, `LESSONS.md`, and workspace handoff.
- `Cargo.toml` and `Cargo.lock` for package version `0.12.3`.

Avoid editing production `src/` behavior; the planned slice is evidence-only.
Do not alter either source artifact. A test-only synchronization guard is an
allowed CI follow-up if the shared persistence path races under parallel tests.

## Tests and checks

- `python3 _workspace/experiments/v0.12.3-phase7-teachability-review/run_audit.py`.
- `python3 -m unittest tests/test_phase7_teachability_review.py`.
- `cargo test --all -- --test-threads=1`.
- `cargo test` (default parallel CI command; required after any test-isolation
  follow-up).
- `cargo test --test golden_competitive_seed42 -- --test-threads=1`.
- `python3 -m unittest discover -s tests -p 'test_*.py'`.
- `cargo fmt --check`.
- `cargo clippy --all-targets -- -D warnings`.
- `git diff --check`.

## Acceptance criteria

- Both named artifacts pass their pinned identity and source-specific contracts.
- 18/18 runs are complete and 270/270 committed transitions are represented.
- All review dimensions are supported for every eligible run; missing markers
  and trace/hash mismatches are reported as failures.
- No new runtime capture, state mutation, or hidden-state inference occurs.
- Any CI follow-up changes tests only and leaves production semantics intact.
- The report explicitly says whether a concrete gap exists and keeps runtime
  promotion deferred when none is found.
- Package/docs identify v0.12.3 and all repository checks pass.

## Non-goals

- No transition, ruleset, command, scenario, replay/hash, balance, difficulty,
  scoring, GUI, legal, calibration, or human-learning changes.
- No new generalized evidence framework or external dependency.
- No claim that source markers prove comprehension, teaching effectiveness,
  optimality, winnability, or causal attribution.

## Stop conditions

- Stop if either artifact is missing, malformed, or cannot be validated without
  inventing information.
- Stop if source-specific context requires exposing hidden actor state.
- Stop if the audit suggests a runtime or interface change without a concrete
  unexplained gap and a separately bounded design gate.

## Review checklist

- Historical source versions and provenance are visible.
- Affiliation post-fix context is checked without reopening v0.12.1.
- Competitive consultant/advisory context is checked without relabeling the
  old capture as v0.12.3.
- Every accepted trace transition aligns to its history/state hash.
- Debrief markers are source-specific and evidence limits are explicit.
- The artifact renderer is deterministic and malformed input is rejected.

## Risk label

Risk: Low.

Reason: This is a read-only deterministic audit over committed JSON artifacts;
it has no simulation, persistence, or public command behavior change.
