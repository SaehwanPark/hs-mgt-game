# Request Summary - Phase 7 Difficulty Evidence Synthesis v0.11.10

## Scope

- Synthesize the committed v0.11.6 all-tier strategy-comparison audit with the
  v0.11.9 Expert difficulty validation artifact.
- Validate source-specific metadata, profile/seed coverage, trace contracts,
  and deterministic evidence continuity for `competitive-regional-v1`.
- Record the evidence result and preserve runtime promotion deferral.
- Update the package version to `0.11.10` and complete PR handoff and review.

## Non-goals

- No new game sessions, runtime mechanics, difficulty values, scoring, balance,
  command, scenario, ruleset, replay, MCP schema, or state-hash changes.
- No generalized evidence schema or normalization of heterogeneous source
  artifacts.
- No causal strategy, general Expert winnability, human-learning,
  empirical-calibration, or policy-validity claim.

## Sources

- `SPEC.md` ranked next-development queue, Phase 7 validation track.
- `docs/roadmap.md` Phase 7 validation and evidence limits.
- `_workspace/experiments/v0.11.6-strategy-comparison-use-audit/results.json`.
- `_workspace/experiments/v0.11.9-expert-difficulty-validation/results.json`.
- `docs/playtest-findings-v0.11.6.md` and `docs/playtest-findings-v0.11.9.md`.

## Expected Files

- `_workspace/experiments/v0.11.10-phase7-difficulty-synthesis/`.
- `tests/test_phase7_difficulty_synthesis.py`.
- `docs/playtest-findings-v0.11.10.md`, `SPEC.md`, `CHANGELOG.md`,
  `LESSONS.md`, `README.md`, `Cargo.toml`, and `Cargo.lock`.
- `_workspace/03_domain_qa.md` and `_workspace/final/handoff.md`.

## Validation Target

- Accept 60 all-tier source runs, 15 Expert source runs, and 15 overlapping
  profile/seed coordinates with no structural evidence gap.
- Preserve the Normal seed-42 golden hash and the existing runtime boundaries.
- Pass focused artifact tests, full Python/Rust suites, formatting, clippy,
  automated playtests, JSON validation, and diff checks.
