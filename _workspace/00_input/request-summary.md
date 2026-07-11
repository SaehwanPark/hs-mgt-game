# Request Summary - Teachability Observation Capture

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation gate.
- Task type: development continuation and bounded read-only evidence capture.
- Selected slice: capture observation-driven Hard competitive traces and route
  runtime promotion only from a concrete unexplained gap.
- Version: 0.10.50.

## Sources

- Canonical project documents and the harness team specification.
- `SPEC.md` promotion rules and competitive teachability queue.
- Existing v0.10.45–v0.10.49 competitive teachability artifacts.
- `docs/agent-playtest-protocol.md` and `docs/mcp-playtesting-guide.md`.

## Expected Files

- `_workspace/experiments/v0.10.50-teachability-observation-capture/`
- `tests/test_teachability_observation_capture.py`
- `docs/playtest-findings-v0.10.50.md`
- Project state, lessons, playtesting guidance, and handoff files.

## Validation Target

- Run three observation-driven profiles across seeds 42, 43, and 44 at Hard.
- Capture actor-visible observations, legal hints, commands, failures/retries,
  transitions, hashes, history, and debriefs for all nine runs.
- Regenerate JSON and diagnostics deterministically.
- Confirm no runtime, scenario, replay, MCP schema, state-hash, scoring,
  balance, difficulty, or debrief behavior changes.

## Non-Goals

- No runtime tuning, new win condition, balance pass, scoring redesign, advisor,
  monitor, command, actor, scenario, replay, or MCP change.
- No causal strategy comparison, dominance, optimality, decision-quality,
  human-learning, calibration, or policy-validity claim.
