# Evidence Map - Consultant Advice Synthesis

## Scope

Synthesize the existing generic consultant evidence chain before considering a
future differentiated advisor market.

## Sources Reviewed

- `docs/expansion-proposal-review.md`
- `docs/playtest-findings-v0.10.40.md`
- `docs/playtest-findings-v0.10.41.md`
- `_workspace/experiments/v0.10.40-consultant-advice-evidence/results.json`
- `_workspace/experiments/v0.10.41-consultant-advice-usage/results.json`
- `docs/mcp-playtesting-guide.md`
- Canonical project and harness documents listed in the request summary

## Mechanisms and Institutions

- Generic consultant options are a non-binding decision-support surface derived
  from the player's actor-visible observation.
- Advisory history preserves what was shown at the time of a committed
  transition so later debriefs can distinguish available advice from submitted
  action.
- Advice-aware wrapper behavior is an evidence harness, not a new game actor or
  a model of an advisor labor market.

## Actor Incentives and Information

- Human and simulated policies receive only their visible observations and
  resource hints.
- Advice-aware policies use visible cues and safe fallback; controls ignore the
  advice and provide regression hashes.
- No artifact establishes human preference, comprehension, advice quality, or
  causal benefit.

## Assumptions

- Four options remain a gameplay abstraction rather than a calibrated advisory
  recommendation.
- Repeated deterministic controls are regression evidence, not independent
  human samples.
- Endpoint differences caused by different policy commands are not causal
  evidence.

## Unresolved Questions

- Whether a human-facing generic advice surface is sufficiently useful remains
  untested by human or classroom evidence.
- Whether a future advisor roster would add educational value remains unresolved
  because no concrete generic-baseline limitation has been observed.

## Design Implications

- Retain the generic baseline and its observation/history/debrief continuity.
- Keep advisor-market runtime promotion gated on a concrete future need,
  recurring-cost sensitivity, and symmetric human/AI information rules.
- Route new development through evidence that identifies a specific
  comprehension, strategy, pacing, or debrief limitation.

## Risks

- Selection, fallback, and alignment counts can be misread as advice uptake or
  quality.
- A polished evidence artifact can be mistaken for human-learning validation.
- Expanding the advisor proposal before a concrete need would add speculative
  actors, payroll, and balance semantics.
