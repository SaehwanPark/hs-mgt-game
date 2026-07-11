# Request Summary - Consultant Advice Validation Evidence

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation loop.
- Task type: development continuation and bounded simulated-agent evidence.
- Selected slice: validate the v0.10.39 consultant baseline at the MCP wrapper
  boundary across four existing policies, seeds 42-44, and Normal/Hard.

## Sources

- `README.md`, `docs/proposal.md`, `docs/roadmap.md`, and
  `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `SPEC.md` and the v0.10.39 consultant-advice handoff
- Existing `scripts/play_game.py` and
  `scripts/run_automated_playtests.py` policies

## Expected Files

- `_workspace/experiments/v0.10.40-consultant-advice-validation/`
- `docs/playtest-findings-v0.10.40.md`
- `SPEC.md`, `CHANGELOG.md`, package metadata, playtest documentation, and
  `_workspace/03_domain_qa.md` / `_workspace/final/handoff.md`

## Validation Target

- 24 runs complete 24 months with zero validation failures.
- Every accepted month exposes exactly four A-D options with non-empty
  tradeoffs and visible state-conditioned variation.
- Every debrief retains the exact option titles and advisory comparison line for
  every committed month.
- Runtime transitions, AI behavior, commands, rulesets, and state hashes remain
  unchanged.

## Non-Goals

- No advisor market, roster, payroll, candidate pool, hire/fire command, AI
  advice policy, scenario schema, balance change, difficulty claim, or
  human-learning claim.
