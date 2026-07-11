# Final Handoff - Consultant Advice Validation Evidence

## Summary

Implemented the v0.10.40 Phase 7 evidence slice. A wrapper-boundary runner
captured four existing deterministic policies across seeds 42-44 at Normal and
Hard difficulty. All 24 sessions completed 24 months with zero validation
failures. Every month exposed four consultant options, and every debrief
retained the corresponding option titles and advisory comparison line.

No Rust runtime, MCP DTO, command, scenario, ruleset, balance, state-hash,
advisor-market, or learning behavior changed.

## Changed Files

- Added the v0.10.40 capture runner, raw JSON artifact, and diagnostics report.
- Added the v0.10.40 findings document and updated Phase 7 playtest, roadmap,
  specification, changelog, version, README, and lessons records.
- Updated the repository workspace input, evidence map, mechanism design, domain
  QA, and final handoff artifacts.

## Verification

- 24-run capture: 24/24 complete; 24/24 advice months; 24/24 debrief option
  records; 24/24 comparison lines; zero validation failures.
- `python3 -m unittest tests/test_playtest_wrapper.py`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1`
- `cargo test --test golden_competitive_seed42 -- --test-threads=1`
- `python3 scripts/run_automated_playtests.py`
- `git diff --check`

## Domain QA

Pass. The evidence is limited to visibility, deterministic variation, accepted
month coverage, and debrief traceability. It makes no advice-quality, learning,
calibration, difficulty, balance, or advisor-market claim.

## PR Handoff

- Base branch: `main`
- Working branch: `feat/consultant-advice-validation-v0.10.40`
- PR: pending creation after final local verification
- Review loop: pending three independent code-reviewer passes
- Merge-ready: no, until PR creation, CI, review findings, and comment replies
  are complete
