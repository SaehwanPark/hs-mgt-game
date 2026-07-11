# Evidence Map - Information-to-Action Comparison

## Scope

Synthesize existing Phase 7 evidence about two actor-visible decision-support
surfaces: generic consultant advice and delayed rival-monitor intelligence.
The output is an instructor/reviewer comparison aid, not a new simulation
mechanic or causal evaluation.

## Sources Reviewed

- Canonical project and harness documents.
- `docs/playtest-findings-v0.10.37.md` and its monitor artifact.
- `docs/playtest-findings-v0.10.40.md`, `v0.10.41.md`, and `v0.10.42.md` and
  their consultant-advice artifacts.
- `docs/playtest-findings-v0.10.43.md` and its follow-through artifact.
- Existing comparison and facilitation surfaces in v0.10.29 and v0.10.34.

## Mechanisms and Institutions

- The human-led health system receives non-binding consultant suggestions and
  delayed partial information about rival activity.
- Consultant advice is a state-conditioned observation retained for history and
  debrief review; monitor intelligence is an observation-only rival signal.
- The comparison mechanism is a documentation abstraction over visibility,
  response, operational follow-through, outcomes, and explanation.

## Actor Incentives and Information

- Simulated policies use actor-visible observations and visible resource hints.
- Advice-aware and monitor-reactive policies intentionally differ from controls,
  so their endpoint differences are not causal treatment estimates.
- Final debriefs can reveal additional history and outcomes that were not known
  at decision time; instructor review must keep those contexts separate.

## Assumptions

- Existing JSON artifacts are deterministic and sufficient for the synthesis.
- Strategy labels remain interpretive discussion handles, not learner classes.
- Advice selection, monitor response, and fallback records demonstrate
  traceability only.

## Unresolved Questions

- Whether instructors or human players find the comparison sequence clear has
  not been tested with human or classroom evidence.
- Whether a future runtime information or difficulty change is needed remains
  unresolved.

## Design Implications

- Compare information visibility and response before judging endpoint quality.
- Treat operational follow-through as distinct from public commitments.
- Preserve current observation, history, replay, and debrief boundaries.
- Keep runtime, advisor-market, difficulty, balance, and scoring changes gated
  on a concrete future gap.

## Risks

- Different policy command streams may be misread as causal evidence.
- Instructor prompts may be mistaken for a validated assessment instrument.
- The comparison surface could duplicate prior facilitation notes unless it
  remains focused on the information-to-action chain.
