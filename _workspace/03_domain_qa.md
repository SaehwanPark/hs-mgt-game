# Domain QA: AI-Agent Playtest Documentation Pivot

## Status

Pass with residual verification caveat.

## Reviewed Inputs

- User request to implement the approved plan.
- `_workspace/00_input/request-summary.md`
- `README.md`
- `SPEC.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/agent-playtest-protocol.md`
- `docs/decision-records/0009-ai-agent-playtest-validation-path.md`
- `docs/mcp-playtesting-guide.md`
- `docs/glossary.md`
- `docs/evidence-registry.md`
- `docs/phase5-scope-register.md`
- `docs/phase1-implications-memo.md`

## Findings

- Scope is bounded to documentation, planning, ADR, glossary, and version
  bookkeeping; no Rust runtime, ruleset, scenario, replay, MCP DTO, or golden
  hash behavior changed.
- The new protocol and roadmap language separate AI-agent playtest evidence
  from measured human learning, empirical calibration, and policy-forecasting
  claims.
- In-game AI players remain distinct from AI-agent playtesters through glossary
  and protocol language.
- Deterministic boundaries are preserved because the protocol requires campaign,
  seed, difficulty, observations, commands, histories, and debrief capture
  through the MCP adapter.

## Required Fixes

None for the documentation pivot.

## Residual Risks

- `scripts/run_automated_playtests.py` hung during verification on the first
  stabilization batch `submit_turn`, despite a one-turn MCP smoke test passing.
  Script debugging is a follow-up outside this docs-only change.
- Agent-playtest evidence remains simulated-player evidence. Any future claim
  about actual learner outcomes needs a separate human evaluation plan.

## Verification Evidence

- `python3` MCP one-turn smoke test passed for `start_session` and
  `submit_turn`.
- `python3 scripts/run_automated_playtests.py` attempted twice and interrupted
  after hanging on the first stabilization batch.
- `cargo fmt --check` passed.
- `cargo test` passed: 228 tests total across library and integration targets.
- `git diff --check` passed.
- Stale-language scan leaves active external-human wording only in historical,
  superseded, or explicit evidence-limit contexts.
