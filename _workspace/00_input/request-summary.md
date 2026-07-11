# Request Summary - Adversarial Resource-Probe Evidence

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation gate.
- Task type: development continuation and bounded read-only evidence capture.
- Selected slice: probe visible cash, action-point, and concurrent-project
  validation limits with deterministic retries, then route runtime promotion
  only from a concrete unexplained gap.
- Version: 0.10.51.

## Sources

- Canonical project documents and the harness team specification.
- `SPEC.md` promotion rules and competitive teachability queue.
- Existing v0.10.45–v0.10.50 competitive teachability artifacts.
- `docs/agent-playtest-protocol.md` and `docs/mcp-playtesting-guide.md`.

## Expected Files

- `_workspace/experiments/v0.10.51-adversarial-resource-probe/`
- `tests/test_adversarial_resource_probe.py`
- `docs/playtest-findings-v0.10.51.md`
- Project state, lessons, playtesting guidance, and handoff files.

## Validation Target

- Run one deterministic adversarial resource-probe policy across seeds 42, 43,
  and 44 at Hard.
- Capture actor-visible observations, legal hints, commands, expected and
  unexpected failures, safe retries, transitions, hashes, history, and
  debriefs for all three runs.
- Regenerate JSON and diagnostics deterministically.
- Confirm rejected commands do not advance the turn and safe `hold` retries
  advance exactly once.
- Confirm no runtime, scenario, replay, MCP schema, state-hash, scoring,
  balance, difficulty, or debrief behavior changes.

## Non-Goals

- No runtime tuning, new win condition, balance pass, scoring redesign, advisor,
  monitor, command, actor, scenario, replay, or MCP change.
- No causal strategy comparison, dominance, optimality, decision-quality,
  human-learning, calibration, or policy-validity claim.
