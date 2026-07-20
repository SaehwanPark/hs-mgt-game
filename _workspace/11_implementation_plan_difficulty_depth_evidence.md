# Operational Coding Plan - Difficulty Depth Evidence Review v0.12.4

## Task restatement

Audit the committed v0.11.11 all-tier and v0.11.9 Expert artifacts for a
visible difficulty pressure signal and bounded Expert clearability, without
launching sessions or changing runtime behavior.

## Current understanding

- The all-tier source covers 60 complete runs, five profiles, three seeds, four
  difficulty tiers, and 1,440 committed operating months.
- The Expert source covers 15 complete runs, the same five profiles and seeds,
  and 360 committed months.
- Existing diagnostics suggest workforce-capacity bottlenecks rise by tier and
  that Normal/Hard/Expert scripted action counts are identical; these claims
  must be recomputed from source history.
- Source versions differ (`0.11.11` versus `0.11.9`), so endpoint values are
  not a causal comparison.

## Assumptions

- Both JSON artifacts are immutable historical records.
- Existing event/effect wording is the source contract for the operating
  bottleneck classification.
- A complete run is only a bounded clearability proxy for its profile, seed,
  and difficulty coordinate.

If either source cannot satisfy its matrix, trace, hash, or debrief contract,
stop and report the limitation instead of launching a replacement capture.

## Minimal implementation plan

1. Add a deterministic audit script with explicit contracts for both source
   artifacts and source-version provenance.
2. Validate matrix identity, 24-transition histories, trace fields, hashes,
   zero validation failures, and debrief coverage.
3. Recompute per-tier action families, trajectory counts, bottleneck counts,
   final outcome ranges, and the Expert overlap/clearability summary.
4. Classify `workforce_capacity` as a candidate pressure signal only if its
   all-tier counts are nondecreasing; keep the classification descriptive.
5. Add focused Python tests for success, malformed input, non-monotonic signal
   rejection, and deterministic Markdown rendering.
6. Update findings, SPEC, changelog, README, architecture, roadmap, lessons,
   version metadata, and final handoff; run all repository checks.

## Files and functions likely to change

- `_workspace/experiments/v0.12.4-difficulty-depth-evidence/run_audit.py`.
- `_workspace/experiments/v0.12.4-difficulty-depth-evidence/results.json` and
  `diagnostics.md`.
- `tests/test_difficulty_depth_evidence.py`.
- `docs/history/playtests/v0.12/playtest-findings-v0.12.4.md`, `SPEC.md`, `CHANGELOG.md`, `README.md`,
  `ARCHITECTURE.md`, `docs/roadmap.md`, `LESSONS.md`, and workspace handoff.
- `Cargo.toml` and `Cargo.lock` for package version `0.12.4`.

Avoid editing `src/`; this slice is evidence-only. Do not alter either source
artifact.

## Tests and checks

- `python3 _workspace/experiments/v0.12.4-difficulty-depth-evidence/run_audit.py`.
- `python3 -m unittest tests/test_difficulty_depth_evidence.py`.
- `cargo test --all -- --test-threads=1`.
- `cargo test` (default parallel CI command).
- `cargo test --test golden_competitive_seed42 -- --test-threads=1`.
- `python3 -m unittest discover -s tests -p 'test_*.py'`.
- `cargo fmt --check`.
- `cargo clippy --all-targets -- -D warnings`.
- `cargo run --quiet -- --help`.
- `git diff --check`.

## Acceptance criteria

- Both source contracts pass with 75/75 complete runs and 1,800/1,800
  committed transitions.
- The all-tier matrix reports per-tier bottleneck/action/trajectory/outcome
  summaries, and Expert clearability is reported only for its 15 coordinates.
- The candidate pressure classification is deterministic and descriptive;
  runtime promotion remains deferred.
- No new session, source mutation, hidden-state inference, causal comparison,
  or general winnability claim occurs.
- Package/docs identify v0.12.4 and all checks pass.

## Non-goals

- No difficulty value, resource, rival AI, scoring, balance, transition,
  command, scenario, replay/hash, GUI, legal, calibration, or human-learning
  changes.
- No general Expert winnability or optimal strategy claim.
- No new evidence framework beyond this bounded source audit.

## Stop conditions

- Stop if the all-tier or Expert artifact is malformed or incomplete.
- Stop if source-version differences would require causal inference.
- Stop if the candidate signal is not source-supported or would require a
  runtime change to make it visible.

## Review checklist

- Source versions, matrices, and overlap are explicit.
- History/state-hash and debrief contracts are independently validated.
- Bottleneck classification uses committed event/effect text only.
- Monotonic pressure is labeled a candidate signal, never a causal effect.
- Expert completion is labeled a bounded clearability proxy.
- The report preserves evidence limits and runtime deferral.

## Risk label

Risk: Low.

Reason: This is a read-only deterministic audit over existing JSON artifacts;
it changes no simulation, persistence, command, or public interface behavior.
