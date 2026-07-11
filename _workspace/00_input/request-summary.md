# Request Summary - Project-Recovery Use Evidence

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation gate.
- Task type: development continuation and bounded evidence capture.
- Working branch: `feat/project-recovery-use-v0.10.56`.
- Version: `0.10.56`.
- Selected slice: test response-conditioned recovery from the existing
  two-project limit without changing runtime or MCP behavior.

## Sources

- Canonical project documents and the harness team specification.
- `SPEC.md` Phase 7 queue and the v0.10.55 ASC observation handoff.
- `_workspace/experiments/v0.10.55-asc-project-observation/results.json`.
- Existing MCP wrapper, project-limit runner, and focused evidence tests.

## Expected Files

- `_workspace/experiments/v0.10.56-project-recovery-use/`.
- `tests/test_project_recovery_use.py`.
- `docs/playtest-findings-v0.10.56.md` and `docs/mcp-playtesting-guide.md`.
- Version, changelog, specification, README, lessons, and required handoff
  artifacts.

## Validation Target

- Run `competitive-regional-v1` at Hard difficulty for seeds 42, 43, and 44.
- Accept clinic and ASC projects before probing a third project.
- On rejection, use only the plain error and unchanged actor-visible
  observation to select `hold`.
- Require one expected rejection, one safe retry, 24 transitions, debrief
  coverage, and v0.10.55 state-hash continuity per run.
- Regenerate JSON and Markdown deterministically.

## Non-Goals

- No project-limit hint, resource payload, transition, command, scenario,
  replay, MCP schema, state-hash, scoring, balance, or difficulty change.
- No human-comprehension, learning, calibration, winnability, or policy-
  validity claim.
