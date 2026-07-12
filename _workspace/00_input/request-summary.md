# Request Summary - Regional Affiliation Observation Context v0.12.2

## Scope

- Continue from merged PR #154 and the v0.12.1 Phase 7 finding.
- Render the existing typed affiliation `commitments`, `alternatives`, and
  `assumptions` fields in the `regional-affiliation-v1` MCP observation.
- Add focused session-boundary tests and rerun the exact independent/deferred/
  pursuit × seeds 42/43/44 capture to prove the context is present.
- Preserve the affiliation transition/replay/hash contracts and the competitive
  seed-42 golden path.

## Non-goals

- No state, transition, ruleset, threshold, balance, command-parser, or replay/
  hash-schema changes.
- No exposure of hidden partner condition, actor utility, resolved future
  responses, or realized outcomes before they occur.
- No GUI, generalized observation framework, AI-rival affiliation behavior,
  legal forecast, calibration, winnability, or human-learning claim.

## Sources

- `SPEC.md`, `docs/roadmap.md`, `docs/design_principles.md`, and
  `docs/proposal.md`.
- `docs/playtest-findings-v0.12.1.md` and the immutable v0.12.1 capture.
- `src/model/affiliation.rs`, `src/affiliation/observe.rs`,
  `src/mcp/session.rs`, and existing MCP session tests.

## Expected files

- `src/mcp/session.rs` and its focused test module.
- `_workspace/experiments/v0.12.2-affiliation-observation-context/` post-fix
  capture and diagnostics.
- `tests/test_affiliation_observation_context.py` for the post-fix artifact.
- `docs/playtest-findings-v0.12.2.md`, `SPEC.md`, `CHANGELOG.md`, README,
  architecture/roadmap/lesson notes, and workspace handoffs.
- `Cargo.toml` and `Cargo.lock` for version `0.12.2`.

## Validation target

- MCP observations contain explicit `Commitments:`, `Alternative:`, and
  `Assumption:` lines without exposing hidden state.
- The same 9-run matrix completes 54 stages with no validation failures, and
  the post-fix audit reports no missing typed context fields.
- Affiliation hashes/replay and the competitive seed-42 golden tests remain
  unchanged.
- Domain QA returns `Pass`; full Rust/Python, formatting, clippy, golden, and
  diff checks pass.
