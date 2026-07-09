# Domain QA - Rival Information Monitor Evidence

## Status

pass

## Reviewed Inputs

- User request to implement the approved continuation plan.
- `docs/playtest-findings-v0.10.37.md`
- `_workspace/experiments/v0.10.37-rival-info-monitor-evidence/results.json`
- `_workspace/experiments/v0.10.37-rival-info-monitor-evidence/diagnostics.md`
- `docs/playtest-findings-v0.10.36.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `SPEC.md`
- `CHANGELOG.md`
- `docs/mcp-playtesting-guide.md`

## Findings

- The artifact stays within Phase 7 evidence work and does not promote runtime
  mechanics, scenario schemas, MCP interfaces, replay formats, state hashes,
  scoring, AP budgets, command costs, or balance changes.
- The paired runs correctly separate observation value from endpoint metrics:
  monitored and unmonitored pairs have identical final hashes, while monitored
  runs include monitor-intel lines unavailable in the unmonitored observations.
- The findings preserve actor-visible observation boundaries. They discuss
  public rival lines, monitor intel, and private activity gaps rather than
  treating hidden true state as player knowledge.
- Expert completion is framed narrowly as one conservative simulated-agent
  policy completing seed `42`, not as a general Expert winnability claim.

## Required Fixes

- None.

## Residual Risks

- The evidence uses deterministic simulated-agent policies, not human classroom
  observation or calibrated learner behavior.
- The paired policy does not test whether players change later choices after
  seeing monitor intel.
- A future runtime slice must still identify a concrete gap before changing
  information delay, monitor value, public disclosure, difficulty values, AP
  budgets, command costs, scoring, or balance.

## Verification Evidence

- `python3 -m py_compile scripts/diagnose_runs.py _workspace/experiments/v0.10.37-rival-info-monitor-evidence/run_sessions.py`
- `python3 _workspace/experiments/v0.10.37-rival-info-monitor-evidence/run_sessions.py`
- `python3 -m json.tool _workspace/experiments/v0.10.37-rival-info-monitor-evidence/results.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.37-rival-info-monitor-evidence/results.json --output _workspace/experiments/v0.10.37-rival-info-monitor-evidence/diagnostics.md`
- `git diff --check`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test -- --test-threads=1`
