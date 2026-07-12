# Request Summary - Expert Difficulty Validation v0.11.9

## Scope

- Validate Expert difficulty after the v0.11.7 AI risk-posture and v0.11.8
  rival resource-scaling changes.
- Run a deterministic Expert-only evidence matrix for `competitive-regional-v1`
  across five policy lanes: Access First, Commercial Focus, Workforce
  Resilience, Capital Modernization, and Coalition/Legitimacy.
- Use seeds 42, 43, and 44, capturing actor-visible observations, legal command
  hints, submitted commands, validation failures, histories, hashes, final
  observations, and debriefs.
- Preserve the Normal seed-42 hold-control hash.
- Update the package version to `0.11.9`.
- Complete feature branch setup, verification, PR handoff, and review loop.

## Non-goals

- No runtime mechanics, difficulty values, scoring, balance, command, scenario,
  ruleset, replay, MCP schema, or state-hash changes.
- No general Expert winnability, human-learning, empirical-calibration, causal,
  or policy-validity claim.
- No broad Phase 7 synthesis beyond this Expert clearability gate.

## Sources

- `SPEC.md` (Ranked next-development queue - Track 2: Difficulty depth and winnability)
- `docs/roadmap.md` (Phase 7 validation and Expert severity/winnability gate)
- `docs/expansion-proposal-review.md` (Difficulty expansion proposal)
- `docs/playtest-findings-v0.10.46.md` (prior Expert clearability evidence shape)

## Expected files

- `_workspace/experiments/v0.11.9-expert-difficulty-validation/run_sessions.py`
- `_workspace/experiments/v0.11.9-expert-difficulty-validation/results.json`
- `_workspace/experiments/v0.11.9-expert-difficulty-validation/diagnostics.md`
- `tests/test_expert_difficulty_validation.py`
- `docs/playtest-findings-v0.11.9.md`
- `SPEC.md`, `CHANGELOG.md`, `LESSONS.md`, `README.md`, and MCP guidance docs.

## Validation target

- 15/15 Expert runs complete the 24-month campaign with zero validation failures
  or failures are explicitly recorded and routed.
- Normal seed-42 hold-control hash remains `61357596d8800592`.
- Focused artifact tests, full Python/Rust tests, formatting, clippy, automated
  playtests, JSON validation, and diff checks pass.
