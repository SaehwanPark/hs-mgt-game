# Request Summary - Debrief-Coherence Audit

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation gate.
- Task type: development continuation and bounded evidence audit.
- Base branch: `main`.
- Working branch: `feat/debrief-coherence-audit-v0.10.58`.
- Version: `0.10.58`.
- Selected slice: audit decision-time context, commands, transitions, delayed or
  partial context, outcomes, and retrospective debrief framing.

## Sources

- Canonical project documents and the harness team specification.
- The v0.10.57 debrief-use audit and its six source artifacts.
- v0.10.43 rival-information follow-through evidence.
- v0.10.50 observation-driven teachability evidence.
- v0.10.51 adversarial resource-probe evidence.
- v0.10.54–v0.10.56 project-recovery evidence.

## Expected Files

- `_workspace/experiments/v0.10.58-debrief-coherence-audit/`.
- `tests/test_debrief_coherence_audit.py`.
- `docs/playtest-findings-v0.10.58.md` and `docs/mcp-playtesting-guide.md`.
- Version, changelog, specification, README, lessons, and required handoffs.

## Validation Target

- Review six existing artifacts and 39 completed source runs.
- Verify decision context, action/retry response, transition follow-through,
  delayed or partial context where applicable, outcome context, and debrief
  explanation markers.
- Verify v0.10.54→v0.10.55→v0.10.56 state-hash continuity across seeds 42–44.
- Regenerate JSON and Markdown deterministically.
- Keep runtime promotion deferred unless separate player-facing, instructor-
  facing, or domain-review evidence identifies an unexplained problem.

## Non-Goals

- No new MCP sessions, runtime mechanics, MCP schema, scenario, replay, state
  hash, scoring, balance, difficulty, or debrief wording change.
- No generalized evidence schema or human/classroom learning claim.
