# Domain QA - Difficulty Pressure Dimension Gate

## Status

Pass.

## Reviewed Inputs

- User request to implement the approved difficulty pressure gate plan.
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `SPEC.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.9.8.md`
- `docs/playtest-findings-v0.9.9.md`
- `docs/playtest-findings-v0.10.12.md`
- `docs/playtest-findings-v0.10.13.md`
- `docs/playtest-findings-v0.10.15.md`
- `docs/playtest-findings-v0.10.16.md`
- `docs/playtest-findings-v0.10.20.md`
- `docs/expansion-proposal-review.md`
- `docs/playtest-findings-v0.10.34.md`
- `docs/playtest-findings-v0.10.35.md`
- `_workspace/00_input/request-summary.md`

## Findings

- The slice stays within the Phase 7 competitive teachability and validation
  loop and the difficulty-depth promotion gate. It selects a future evidence
  surface rather than promoting a runtime change.
- Rival information and monitoring pressure visibility is a suitable next
  bounded difficulty dimension because it is actor-visible, inspectable, and
  compatible with the project's true-state versus observation boundary.
- The gate avoids hidden rival omniscience by requiring future difficulty work
  to remain visible through observations, monitor value, public disclosure, or
  debrief traceability.
- The routing guidance keeps Expert winnability, difficulty value changes,
  player-resource cuts, command-cost changes, scoring, GUI, M&A, and balance
  work deferred until a later artifact identifies a concrete need.
- The review preserves deterministic replay, actor-observation separation,
  append-only history, visible assumptions, and educational debriefing
  boundaries.

## Required Fixes

None.

## Residual Risks

- Existing evidence is simulated-agent, deterministic-policy, reviewer-policy,
  and operator-authored evidence, not human classroom observation.
- Monitoring frequency is a pressure signal, not proof that monitoring improves
  learning, endpoint metrics, or strategy quality.
- Future runtime tuning still requires a separate evidence artifact naming a
  concrete information-delay, monitor-value, rival-pressure, command-cost,
  cash-runway, staffing, difficulty, or balance defect.

## Verification Evidence

- `python3 -m json.tool _workspace/experiments/v0.9.8-difficulty-sweep/results.json`
- `python3 -m json.tool _workspace/experiments/v0.9.9-difficulty-adaptive/results.json`
- `python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
- `python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
- `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.35-diagnostics.md`
- `git diff --check`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test -- --test-threads=1`
