# Request Summary - Debrief-Use Audit

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation gate.
- Task type: development continuation and bounded evidence audit.
- Base branch: `main`.
- Working branch: `feat/debrief-use-audit-v0.10.57`.
- Version: `0.10.57`.
- Selected slice: audit event-specific continuity from actor-visible evidence
  through response, accepted transition/hash, and debrief explanation.

## Sources

- Canonical project documents and the harness team specification.
- `SPEC.md` Phase 7 queue and v0.10.56 project-recovery handoff.
- v0.10.43 rival-information follow-through artifact.
- v0.10.50 observation-driven teachability artifact.
- v0.10.51 resource-probe artifact.
- v0.10.54–v0.10.56 project-recovery artifacts.

## Expected Files

- `_workspace/experiments/v0.10.57-debrief-use-audit/`.
- `tests/test_debrief_use_audit.py`.
- `docs/playtest-findings-v0.10.57.md` and `docs/mcp-playtesting-guide.md`.
- Version, changelog, specification, README, lessons, and required handoffs.

## Validation Target

- Review six existing artifacts and 39 completed source runs.
- Verify visibility, response, follow-through, outcome, and explanation coverage.
- Verify v0.10.54→v0.10.55→v0.10.56 state-hash continuity across seeds 42–44.
- Regenerate JSON and Markdown deterministically.
- Keep runtime promotion deferred unless a separate player-facing,
  instructor-facing, or domain-review gap is demonstrated.

## Non-Goals

- No new MCP sessions, runtime mechanics, MCP schema, scenario, replay, state
  hash, scoring, balance, difficulty, or debrief wording change.
- No generalized evidence schema or human/classroom learning claim.
