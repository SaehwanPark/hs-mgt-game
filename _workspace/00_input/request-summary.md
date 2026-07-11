# Request Summary - Project-Limit Recovery Evidence Gate

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation gate.
- Task type: development continuation and bounded MCP evidence capture.
- Selected slice: test the actor-visible recovery surface for the existing
  two-project concurrency limit across Hard seeds 42, 43, and 44.
- Working branch: `feat/project-limit-recovery-evidence-v0.10.54`.
- Version: 0.10.54.

## Sources

- Canonical project documents and the harness team specification.
- `SPEC.md` promotion rules and competitive teachability queue.
- `_workspace/experiments/v0.10.51-adversarial-resource-probe/results.json`.
- `src/mcp/session.rs`, `src/model/resources.rs`, `src/cli/guidance.rs`, and
  `src/debrief/report.rs` as inspect-only descriptions of current behavior.
- `docs/agent-playtest-protocol.md` and `docs/mcp-playtesting-guide.md`.

## Expected Files

- `_workspace/experiments/v0.10.54-project-limit-recovery/`
- `tests/test_project_limit_recovery.py`
- `docs/playtest-findings-v0.10.54.md`
- Project state, evidence map, lessons, playtesting guidance, and handoff files.

## Validation Target

- Confirm two project commands are accepted before a third project receives
  `too_many_concurrent_projects` on the same turn.
- Preserve the pre-failure observation, legal command hints, structured error
  fields, post-failure observation, `hold` retry, transition hashes, and debrief.
- Complete all three 24-month runs without unexpected validation failures.
- Regenerate JSON and Markdown deterministically.
- Confirm no runtime, scenario, replay, MCP schema, state-hash, scoring,
  balance, difficulty, or debrief behavior changes.

## Non-Goals

- No validation-hint implementation, runtime tuning, new win condition, balance
  pass, scoring redesign, command, actor, scenario, replay, or MCP change.
- No generalized evidence schema, causal strategy comparison, dominance,
  optimality, decision-quality, human-learning, calibration, or policy-validity
  claim.
