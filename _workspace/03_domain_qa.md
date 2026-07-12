# Domain QA - Difficulty Depth Evidence Review v0.12.4

## Status

Pass.

## Reviewed Inputs

- v0.12.4 request summary, evidence map, mechanism design, and implementation
  plan.
- v0.11.11 post-change all-tier validation artifact/diagnostics.
- v0.11.9 Expert validation artifact/diagnostics.
- `docs/playtest-findings-v0.11.10.md`,
  `docs/playtest-findings-v0.11.11.md`, `SPEC.md`, `docs/roadmap.md`, and
  `docs/design_principles.md`.

## Findings

- The evidence question is appropriately bounded to existing deterministic
  simulated-policy artifacts.
- The source contracts retain five profiles, three seeds, four tiers for the
  all-tier lane, and the same five profiles/seeds for the Expert lane.
- Workforce capacity is a plausible visible pressure category because it is
  represented in accepted operating records and can be summarized by tier.
- The source-version mismatch and scripted-policy limits prevent causal,
  calibration, general winnability, or human-learning conclusions.
- Any candidate signal must route to a later design gate; this slice does not
  authorize difficulty or balance changes.

## Required Fixes

None for the planned evidence-only slice.

## Residual Risks

- Monotonic bottleneck counts can reflect policy composition or ruleset
  interactions rather than a valid player-facing difficulty gradient.
- Expert completion across 15 scripted coordinates is not general winnability.
- Existing debrief markers show traceability, not comprehension or pedagogical
  effectiveness.

## Verification Evidence

- Planned focused Python tests cover source identity, exact matrices, trace/hash
  alignment, candidate-signal calculation, malformed input, and deterministic
  rendering.
- Planned report coverage: 75 complete runs, 1,800 transitions, and explicit
  per-tier pressure/outcome summaries.
- No runtime or source artifact is mutated by the audit.
