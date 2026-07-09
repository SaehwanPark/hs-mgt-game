# Domain QA - Rival Information Pressure Design

## Status

pass

## Reviewed Inputs

- User request to implement the approved PR handoff plan.
- `docs/playtest-findings-v0.10.36.md`
- `docs/playtest-findings-v0.10.35.md`
- `docs/expansion-proposal-review.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `SPEC.md`
- `CHANGELOG.md`
- `docs/mcp-playtesting-guide.md`

## Findings

- The artifact stays within Phase 7 difficulty design and does not promote
  runtime mechanics, scenario schemas, MCP interfaces, replay formats, state
  hashes, scoring, AP budgets, command costs, or balance changes.
- The design separates observable rival information surfaces from hidden true
  state. It frames information delay, monitor value, and public disclosure as
  actor-visible design hypotheses rather than omniscient rival advantages.
- The note preserves the distinction between design intent, evidence limits,
  and future promotion criteria. Expert clearability is explicitly unvalidated.
- The design keeps monitoring pressure contextual and reviewable. It does not
  present monitoring frequency as proof of learning, endpoint quality, or
  calibrated strategy value.

## Required Fixes

- None.

## Residual Risks

- The tier table is still a design hypothesis based on simulated-agent,
  deterministic-policy, reviewer-policy, and operator-authored evidence rather
  than classroom observation.
- A future runtime slice must still prove that one information-pressure surface
  cannot be handled by existing observations, histories, diagnostics, or
  debriefs before changing mechanics.

## Verification Evidence

- `python3 -m json.tool _workspace/experiments/v0.9.8-difficulty-sweep/results.json`
- `python3 -m json.tool _workspace/experiments/v0.9.9-difficulty-adaptive/results.json`
- `python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
- `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- `git diff --check`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test -- --test-threads=1`
