# Domain QA - Workforce Capacity Difficulty Design Gate v0.12.5

## Status

Pass.

## Reviewed Inputs

- v0.12.5 request summary, evidence map, mechanism design, and implementation
  plan.
- v0.12.4 difficulty-depth report and diagnostics.
- `PlayerObservation`, competitive observation construction, MCP formatter,
  staffing transition events, and debrief attribution.
- `SPEC.md`, `docs/roadmap.md`, `docs/design_principles.md`, and the v0.11.11/
  v0.11.12 findings.

## Findings

- The v0.12.4 pressure signal is grounded in accepted operating records, but
  its numeric staffing/capacity context is not fully rendered in MCP output.
- The omitted fields already belong to the typed actor observation, so a
  compact projection is a bounded interface follow-up rather than a new state
  or difficulty mechanism.
- Rendering current Riverside staffing and physical capacity is within actor
  authority; hidden targets, effective allocations, future hires, and rival
  private state remain excluded.
- The proposal preserves deterministic transitions, state hashes, replay,
  commands, debrief attribution, and the competitive golden contract.

## Required Fixes

None for the design gate.

## Residual Risks

- Numeric context may still be hard for humans to interpret; no learning claim
  is made.
- A compact capacity line may be verbose and should remain outside the
  deterministic core.
- The proposal does not establish balance, calibration, or winnability.

## Verification Evidence

- Planned design-contract test confirms the exact safe source fields, excluded
  hidden fields, next-slice tests, and unchanged-contract requirements.
- No runtime or source artifact is mutated by this design gate.
