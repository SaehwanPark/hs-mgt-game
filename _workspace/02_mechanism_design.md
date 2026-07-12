# Mechanism Design - Difficulty Depth Evidence Review v0.12.4

## Goal and Roadmap Phase

Phase 7/9 difficulty-depth evidence gate after the v0.12.3 teachability review.
This is a read-only audit, not a new difficulty mechanism.

## Slice Boundary

- Inputs: exactly the v0.11.11 all-tier and v0.11.9 Expert JSON artifacts.
- Output: deterministic source validation, per-tier pressure summaries,
  clearability coverage, candidate-signal classification, and evidence limits.
- Unit: 24 committed operating months per run; 60 all-tier runs plus 15
  standalone Expert runs.
- Excluded: new sessions, parameter tuning, ruleset changes, scoring, hidden
  rival omniscience, player-resource cuts, GUI, and human evaluation.

## Actors and Authority

The audit treats each source's actor-visible observation and submitted command
as the player-facing boundary. Rival private actions and instructor-revealed
outcomes remain source records; the report does not infer them as player
knowledge or utility.

## State, Beliefs, and Observations

Pressure is represented only by committed operating records and source-provided
trace fields: workforce-capacity markers, capacity/demand markers, operating
loss, action-family trajectories, final tradeoff summaries, and debrief
explanation markers. No hidden state is added.

## Commands, Events, and Effects

No command, event, effect, transition, resolved input, state-hash, or replay
behavior changes. Existing events/effects are parsed to classify descriptive
operating bottlenecks.

## Strategic Interaction

The all-tier source preserves five scripted profiles over four difficulty tiers;
the Expert source preserves the same five profile names over three seeds. The
audit reports profile/seed/tier coverage and action trajectories but assigns no
utility, quality, or optimality judgment.

## Candidate Pressure Dimension

`workforce_capacity` is a candidate only if the recomputed all-tier counts are
nondecreasing across Easy, Normal, Hard, and Expert. If supported, the finding
means the current artifacts expose an operating-pressure signal worth a later
design gate. It does not mean the signal is correctly calibrated or that
runtime tuning is authorized.

## Educational and Debrief Hooks

- Each run must retain the decision-time observation/command surface.
- Each accepted month must link to a committed transition and state hash.
- Each run must retain month-level debrief coverage and decision-quality
  framing.
- The report must distinguish bounded clearability evidence from winnability
  and human learning.

## Determinism and Replay Notes

The audit reads committed JSON only and emits stable JSON/Markdown summaries. It
does not regenerate a transition, alter a hash, or rewrite a source artifact.

## Open Questions

- Whether workforce-capacity pressure is legible or appropriately paced to a
  human player remains unmeasured.
- Whether Expert is generally winnable remains untested beyond the named
  profiles and seeds.
- A later runtime change requires a separate design gate with focused tests and
  an explicit decision about balance and difficulty semantics.
