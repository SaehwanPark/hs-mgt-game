# Request Summary - Command-to-Effect Explainability Evidence

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation gate.
- Task type: development continuation and bounded read-only evidence audit.
- Selected slice: check command-to-effect and command-to-debrief trace coverage
  in the existing v0.10.46 Expert artifact.
- Version: 0.10.47.

## Sources

- Canonical project documents and the harness team specification.
- `SPEC.md` Future difficulty-depth queue and promotion rules.
- `docs/playtest-findings-v0.10.35.md`, `docs/playtest-findings-v0.10.36.md`,
  `docs/playtest-findings-v0.10.37.md`, and recent teachability findings.
- Existing v0.10.46 MCP capture artifact and the competitive debrief contract.

## Expected Files

- `_workspace/experiments/v0.10.47-command-effect-explainability/`
- `tests/test_command_effect_explainability.py`
- `docs/playtest-findings-v0.10.47.md`
- Project state, lessons, playtesting guidance, and handoff files.

## Validation Target

- Review all 12 existing runs without launching new MCP sessions.
- Require every command to be supported, explicitly neutral, or retained as an
  unmatched record with a reason.
- Confirm monthly player command records remain present in the debrief.
- Regenerate JSON and Markdown output deterministically.
- Confirm no runtime, scenario, replay, MCP schema, state-hash, scoring, or
  balance files change.

## Non-Goals

- No new sessions, difficulty tuning, new win condition, balance pass, scoring
  redesign, advisor, monitor, command, actor, scenario, replay, or MCP changes.
- No causal, decision-quality, human-learning, calibration, or policy-validity
  claim.
