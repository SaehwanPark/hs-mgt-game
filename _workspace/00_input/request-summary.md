# Request Summary - Difficulty Depth Evidence Review v0.12.4

## Scope

- Continue from merged PR #156 and the v0.12.3 teachability review.
- Audit the existing post-change all-tier difficulty artifact and standalone
  Expert validation artifact without launching new sessions.
- Ask whether a visible pressure dimension is expressed across difficulty tiers
  and whether Expert completion remains a bounded clearability proxy.
- Report one candidate signal, if present, while keeping runtime promotion,
  balance, and winnability claims deferred.

## Non-goals

- No new capture, state, transition, ruleset, threshold, scoring, balance,
  difficulty value, command, scenario, replay/hash, or GUI changes.
- No causal comparison across source versions; endpoint outcomes are descriptive
  only because the sources were produced at different code versions.
- No general Expert winnability, human-learning, calibration, legal-validity,
  policy-forecasting, or optimal-strategy claim.

## Sources

- `SPEC.md`, `docs/roadmap.md`, `docs/design_principles.md`, and
  `docs/proposal.md`.
- `_workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/results.json`
  and its diagnostics.
- `_workspace/experiments/v0.11.9-expert-difficulty-validation/results.json`
  and its diagnostics.
- `docs/playtest-findings-v0.11.10.md`, `docs/playtest-findings-v0.11.11.md`,
  and the existing source audit contracts.

## Expected files

- `_workspace/experiments/v0.12.4-difficulty-depth-evidence/` audit script,
  results, and diagnostics.
- `tests/test_difficulty_depth_evidence.py` for source contracts, pressure
  summaries, malformed-input rejection, and deterministic rendering.
- `docs/playtest-findings-v0.12.4.md`, `SPEC.md`, `CHANGELOG.md`, README,
  architecture/roadmap/lesson notes, and workspace handoffs.
- `Cargo.toml` and `Cargo.lock` for version `0.12.4`.

## Validation target

- The two named artifacts contain 75 complete runs and 1,800 committed
  transitions in total: 60 all-tier plus 15 Expert.
- The all-tier matrix covers five profiles × three seeds × four difficulty
  tiers, with complete trace/hash/debrief contracts and zero validation
  failures.
- The Expert artifact covers the same five profiles × three seeds at Expert,
  with 15/15 complete runs and zero validation failures.
- The audit reports per-tier workforce-capacity signals, action trajectories,
  final tradeoff ranges, and the overlap/source-version limitation.
- Domain QA returns `Pass`; full Rust/Python, formatting, clippy, golden, CLI,
  and diff checks pass under default parallel CI tests.
