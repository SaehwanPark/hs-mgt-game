# Request Summary - Phase 7 Teachability Evidence Review v0.12.3

## Scope

- Continue from merged PR #155 and the v0.12.2 post-fix artifact.
- Run a deterministic, read-only Phase 7 audit across the existing
  `regional-affiliation-v1` post-fix artifact and the approved competitive
  teachability capture.
- Check the common decision-context → action/response → transition → outcome →
  debrief chain, then check each campaign's declared context markers.
- Preserve both source artifacts as historical evidence and keep runtime
  promotion deferred unless the audit identifies a concrete unexplained gap.

## Non-goals

- No new session capture, state, transition, ruleset, threshold, balance,
  command-parser, or replay/hash-schema changes.
- A CI follow-up may isolate shared filesystem tests, but must not change
  production runtime semantics.
- No cross-campaign normalization that erases source-specific observation
  boundaries or treats different debrief vocabulary as missing evidence.
- No GUI, generalized observation framework, legal forecast, calibration,
  winnability, or human-learning claim.

## Sources

- `SPEC.md`, `docs/roadmap.md`, `docs/design_principles.md`, and
  `docs/proposal.md`.
- `_workspace/experiments/v0.12.2-affiliation-observation-context/results.json`
  and its diagnostics.
- `_workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/results.json`
  and its diagnostics.
- `docs/playtest-findings-v0.12.1.md`, `docs/playtest-findings-v0.12.2.md`,
  and the current MCP/session contracts.

## Expected files

- `_workspace/experiments/v0.12.3-phase7-teachability-review/` audit script,
  results, and diagnostics.
- `tests/test_phase7_teachability_review.py` for source contracts, coverage,
  malformed-input rejection, and deterministic rendering.
- `src/cli/persistence.rs` only if CI exposes a test-isolation defect; no
  production persistence behavior is in scope.
- `docs/playtest-findings-v0.12.3.md`, `SPEC.md`, `CHANGELOG.md`, README,
  architecture/roadmap/lesson notes, and workspace handoffs.
- `Cargo.toml` and `Cargo.lock` for version `0.12.3`.

## Validation target

- The two named artifacts contain 18 complete runs and 270 committed
  transitions in total.
- Every eligible run has actor-visible observation, legal command, submitted
  command, accepted transition/state-hash, final outcome, and debrief evidence.
- Affiliation-specific commitment/alternative/assumption context and
  competitive-specific consultant/advisory context are present without
  hidden-state inference.
- The audit reports no structural gap, preserves the competitive control hash,
  and keeps runtime promotion deferred.
- Domain QA returns `Pass`; full Rust/Python, formatting, clippy, golden, and
  diff checks pass under the repository's default parallel test command.
