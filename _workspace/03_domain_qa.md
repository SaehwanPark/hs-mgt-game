# Domain QA - Instructor Debrief Facilitation Note

## Status

Pass.

## Reviewed Inputs

- User request to implement the approved continuation and PR handoff plan.
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `SPEC.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.10.29.md`
- `docs/playtest-findings-v0.10.30.md`
- `docs/playtest-findings-v0.10.33.md`
- `docs/playtest-findings-v0.10.34.md`
- `_workspace/00_input/request-summary.md`

## Findings

- The slice stays within the Phase 7 competitive teachability and validation
  loop. It sequences existing comparison evidence for instructor use rather
  than promoting a runtime change.
- The facilitation sequence keeps decision context separate from outcome
  context, preserving the project's distinction between actor-visible
  observations, true state consequences, and debrief interpretation.
- Workforce-protective and growth/capacity prompts are framed as interpretive
  review postures, not hidden strategy classes, validated learner archetypes,
  assessment instruments, or balance proof.
- The routing guidance defers access-pledge cooldowns, project-cost,
  capacity-effect, staffing-allocation, action-availability, difficulty,
  scoring, and balance changes until a future artifact identifies a concrete
  mechanics defect.
- The review preserves deterministic replay, actor-observation separation,
  append-only history, visible assumptions, and educational debriefing
  boundaries.

## Required Fixes

None.

## Residual Risks

- Existing evidence is simulated-agent, deterministic-policy, reviewer-policy,
  and operator-authored evidence, not human classroom observation.
- The facilitation sequence remains a discussion aid rather than a validated
  classroom assessment instrument.
- Future runtime tuning still requires a separate evidence artifact naming a
  concrete command-cost, project timing, cash runway, staffing, difficulty, or
  balance defect.

## Verification Evidence

- `python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
- `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- `python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.34-live-diagnostics.md`
- `git diff --check`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test -- --test-threads=1`
