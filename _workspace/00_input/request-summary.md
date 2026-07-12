# Request Summary - Current-Code Teachability Capture v0.11.12

## Scope

- Continue Phase 7 validation after the merged v0.11.11 all-tier matrix.
- Reuse the existing observation-driven Fiscal Steward, Access Expansion
  Advocate, and First-Time Executive profiles.
- Capture `competitive-regional-v1` at Hard difficulty for seeds 42, 43, and
  44 through the local MCP boundary.
- Preserve actor-visible observations, legal commands, submitted commands,
  validation failures, retries, committed histories, state hashes, final
  observations, and debriefs.
- Audit action cadence, trace/hash alignment, player/rival operating-event
  boundaries, and debrief continuity.
- Bump the package to `0.11.12` and complete the branch, PR, and review
  handoff.

## Non-goals

- No runtime mechanics, difficulty values, AI scoring, commands, scenarios,
  rulesets, replay formats, MCP schemas, or state-hash changes.
- No new evidence framework, dependency, external LLM integration, or broad
  all-tier rerun.
- No causal strategy, balance, general winnability, human-learning,
  cognitive-load, calibration, or policy-validity claim.
- No runtime promotion from descriptive pacing or retry signals alone.

## Sources

- `SPEC.md`, the Phase 7 ranked queue, and the v0.11.11 checkpoint.
- `docs/roadmap.md`, `docs/design_principles.md`, and
  `docs/agent-playtest-protocol.md`.
- Historical observation-driven policies in
  `_workspace/experiments/v0.10.50-teachability-observation-capture/`.
- Historical pacing audit in
  `_workspace/experiments/v0.10.52-decision-load-evidence/`.
- Current-code all-tier baseline in
  `_workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/`.

## Expected files

- `_workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/`.
- `tests/test_phase7_current_code_teachability_capture.py`.
- `docs/playtest-findings-v0.11.12.md`, `CHANGELOG.md`, `README.md`, `SPEC.md`,
  `docs/roadmap.md`, `docs/mcp-playtesting-guide.md`, and `LESSONS.md`.
- `Cargo.toml`, `Cargo.lock`, and active `_workspace` handoffs.

## Validation target

- Exactly 9 unique profile/seed coordinates and 216 committed months.
- Every run completes 24 transitions; any rejected command or safe retry is
  preserved rather than discarded.
- The Normal seed-42 hold-control hash remains `61357596d8800592`.
- Focused artifact tests, full Python/Rust suites, formatting, clippy,
  playtest generation, JSON validation, and diff checks pass.
