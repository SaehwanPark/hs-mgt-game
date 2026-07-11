# Request Summary - Phase 7 Evidence Chain Synthesis

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation gate.
- Task type: development continuation and bounded read-only evidence synthesis.
- Selected slice: connect the v0.10.50, v0.10.51, and v0.10.52 evidence artifacts
  through source, control, and matrix continuity checks.
- Version: 0.10.53.

## Sources

- Canonical project documents and the harness team specification.
- `SPEC.md` promotion rules and competitive teachability queue.
- `_workspace/experiments/v0.10.50-teachability-observation-capture/results.json`.
- `_workspace/experiments/v0.10.51-adversarial-resource-probe/results.json`.
- `_workspace/experiments/v0.10.52-decision-load-evidence/results.json`.
- `docs/agent-playtest-protocol.md` and `docs/mcp-playtesting-guide.md`.

## Expected Files

- `_workspace/experiments/v0.10.53-evidence-synthesis/`
- `tests/test_phase7_evidence_synthesis.py`
- `docs/playtest-findings-v0.10.53.md`
- Project state, lessons, playtesting guidance, and handoff files.

## Validation Target

- Validate all three source identities and declared evidence dimensions.
- Confirm v0.10.51 First-Time Executive control hashes match v0.10.50.
- Confirm the shared nine-member profile/seed matrix remains continuous through
  v0.10.52.
- Regenerate JSON and Markdown deterministically without new sessions.
- Confirm no runtime, scenario, replay, MCP schema, state-hash, scoring,
  balance, difficulty, or debrief behavior changes.

## Non-Goals

- No new MCP sessions, runtime tuning, new win condition, balance pass, scoring
  redesign, advisor, monitor, command, actor, scenario, replay, or MCP change.
- No generalized evidence schema, causal strategy comparison, dominance,
  optimality, decision-quality, human-learning, calibration, or policy-validity
  claim.
