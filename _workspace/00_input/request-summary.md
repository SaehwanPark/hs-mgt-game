# Request Summary - ASC Project Observation Coverage

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation gate.
- Task type: development continuation and bounded observability bugfix.
- Working branch: `fix/asc-project-observation-v0.10.55`.
- Version: `0.10.55`.
- Selected slice: expose accepted ASC projects in the existing actor-visible
  `In-flight projects` observation and verify unchanged project-limit recovery.

## Sources

- Canonical project documents and the harness team specification.
- `SPEC.md` Phase 7 queue and the v0.10.54 project-limit recovery handoff.
- `_workspace/experiments/v0.10.54-project-limit-recovery/results.json`.
- `src/sim/observe_competitive.rs` and its active-project observation tests.
- `docs/agent-playtest-protocol.md` and `docs/mcp-playtesting-guide.md`.

## Expected Files

- `src/sim/observe_competitive.rs` and its focused Rust regression test.
- `_workspace/experiments/v0.10.55-asc-project-observation/`.
- `tests/test_asc_project_observation.py`.
- Version, changelog, specification, findings, lessons, playtesting guidance,
  and required `_workspace` handoff files.

## Validation Target

- Run `competitive-regional-v1` at Hard difficulty for seeds 42, 43, and 44.
- Accept `clinic_network` and `asc_unit` projects before probing a third
  project.
- Require both `ClinicNetwork` and `AscUnit` details in the month-7
  actor-visible observation and after the rejected third-project command.
- Preserve `too_many_concurrent_projects`, same-turn state, one safe `hold`
  retry, 24 transitions, debrief explanation, and v0.10.54 state hashes.
- Regenerate JSON and Markdown deterministically.

## Non-Goals

- No project-limit hint, structured resource payload, transition, command,
  scenario, replay, MCP schema, state-hash, scoring, balance, or difficulty
  change.
- No new service-line mechanism, generalized evidence schema, human-learning,
  calibration, winnability, or policy-validity claim.
