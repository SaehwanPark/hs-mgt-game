# Mechanism Design — Visual and Audio Phase 3 Contextual Action Submission v0.12.19

## Goal and Roadmap Phase

Allow one executive player to complete a competitive month graphically using
canonical commands, host validation, and a single existing transition boundary.
This is roadmap Phase 3 and precedes resolution animation/causal feedback.

## Slice Boundary

The host returns an action catalog for seven existing competitive command
families. The browser renders generic parameter forms, builds a local draft
batch, asks the host to validate the canonical batch, displays exact returned
costs/constraints/delay/uncertainty, and submits only a validated batch through
`submit_turn`. A rejected batch is visibly recoverable and non-mutating.

## Actors and Authority

The Rust engine/MCP host owns command vocabulary, parsing, validation, action
costs, resource checks, transition evaluation, stochastic inputs, history,
hashes, and committed outcomes. The browser owns only draft action values,
selection, form focus, local batch ordering, and status presentation.

## State, Beliefs, and Observations

Action metadata is visible command affordance, not true outcome state. The
client sees only current resources and host-returned validation/preview data.
It does not infer available resources, rival state, future staffing, capacity,
or stochastic result from form fields. Rejected validation preserves the prior
read-only envelope.

## Commands, Events, and Effects

`get_action_catalog` returns templates and parameter metadata. `validate_turn`
parses and validates the complete canonical batch without transition and returns
host-derived aggregate cost plus action previews/errors. `submit_turn` remains
the only mutation path; its response supplies committed events/effects/history
for the next observation. No browser action creates a new command verb.

## Strategic Interaction

The player chooses whether to spend scarce attention/resources on workforce,
capacity, information, payer/policy posture, or projects. The interface may
show tradeoffs and uncertainty but may not recommend an optimal action or imply
that a valid command guarantees a favorable result.

## Assumptions and Parameters

- Contract schemas: `competitive-actions-v1` and `competitive-validation-v1`.
- First supported campaign: `competitive-regional-v1`.
- Existing command parser accepts semicolon-separated batches; the builder
  emits the same canonical representation.
- Host action previews label delay and uncertainty without replacing Phase 4
  committed resolution.

## Educational Debrief Hooks

The draft/validated/submitted distinction makes decision quality inspectable
without collapsing it into outcome quality. Committed history and debrief
remain host-owned, and Phase 3 does not claim that the action workflow teaches
or improves strategic reasoning.

## Determinism and Replay Notes

Validation reads do not change turn, resources, history, or hashes. A rejected
submission must preserve the same envelope and replay trajectory. A successful
submission delegates to the existing deterministic/stochastic host transition;
the client records no parallel history.

## Open Questions

- Which default action grouping best supports first-time taskplay without
  suggesting a universal strategy?
- Which Phase 4 resolution sequence can explain multiple committed actions
  without implying that presentation order caused the outcome?
- What evidence is required before expanding the action workflow to other
  campaigns or adding richer contextual entity filters?
