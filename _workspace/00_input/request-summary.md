# Request Summary - Expert Clearability Evidence

## Scope

- Roadmap phase: Phase 7 competitive difficulty and winnability evidence gate.
- Task type: development continuation and bounded MCP evidence capture.
- Selected slice: test completion of the current Expert campaign with existing
  simulated-policy profiles across named seeds.
- Version: 0.10.46.

## Sources

- Canonical project documents and the harness team specification.
- `SPEC.md` Future difficulty-depth queue and promotion rules.
- `docs/playtest-findings-v0.10.35.md`, `docs/playtest-findings-v0.10.36.md`,
  `docs/playtest-findings-v0.10.37.md`, and recent teachability findings.
- Existing MCP wrapper and policy functions in `scripts/`.

## Expected Files

- `_workspace/experiments/v0.10.46-expert-clearability-evidence/`
- `tests/test_expert_clearability_evidence.py`
- `docs/playtest-findings-v0.10.46.md`
- Project state, lessons, playtesting guidance, and handoff files.

## Validation Target

- Capture four profiles across seeds `42`, `43`, and `44` at Expert difficulty.
- Require 12 represented runs with actor-visible traces, commands, validation
  failures, histories, hashes, and debriefs.
- Preserve failed or incomplete runs for diagnosis rather than dropping them.
- Regenerate JSON and Markdown output deterministically.
- Confirm no runtime, scenario, replay, MCP schema, state-hash, scoring, or
  balance files change.

## Non-Goals

- No difficulty tuning, new win condition, balance pass, scoring redesign,
  advisor, monitor, command, actor, scenario, replay, or MCP changes.
- No general Expert winnability, causal, human-learning, calibration, or
  policy-validity claim.
