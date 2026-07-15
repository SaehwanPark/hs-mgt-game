# Mechanism Design — Visual and Audio Phase 7 Campaign Coverage v0.12.23

## Goal and Roadmap Phase

Implement roadmap Phase 7: extend the validated presentation system to
stabilization and affiliation while preserving their incompatible campaign
semantics and canonical command boundaries.

## Slice Boundary

The host exposes `campaign-coverage-v1` through a non-mutating
`get_campaign_coverage` read for `stabilization-v1` and
`regional-affiliation-v1`. The envelope includes shared session/stage/briefing/
metric/history/replay/debrief primitives plus campaign-specific actors,
processes, and decisions. Competitive presentation remains on its existing
contracts.

## Actors and Authority

Rust/MCP owns campaign state, actor-visible observations, stage legality,
canonical command parsing/validation, resolved inputs, transitions, history,
hashes, and educational debriefs. The browser owns panel visibility, local form
drafts, selected campaign decision, navigation, and audio playback. The browser
does not own campaign state or infer outcome meaning.

## State, Beliefs, and Observations

Stabilization presents reported access/quality, current cash/staffed beds,
policy/market briefing, stage-specific decision metadata, and explicit
uncertainty. Affiliation presents partner identity/condition when reported,
Riverside visible metrics, commitments, stage/status, stakeholder response
signals, assumptions, and integration/review obligations. True states and
resolved stochastic inputs remain unavailable.

## Commands, Events, and Effects

The envelope returns host-shaped decisions with command templates and parameter
metadata. The browser substitutes only entered values into the host-provided
template and sends the resulting canonical text to the existing `submit_turn`
adapter. Host rejection leaves the current coverage envelope and session intact;
success reloads the read and committed history. Existing transition events,
attributed effects, hashes, and debrief lines are reused as source-labeled
history rather than recomputed.

## Strategic Interaction

Stabilization keeps the player focused on sequencing short-term capacity,
policy, workforce, coalition, and competitive commitments. Affiliation keeps
partner fit, review authority, labor, payer, community, and integration as
separate interacting institutions. The UI may clarify the next stage and visible
tradeoffs but may not rank a universally optimal posture or merge actor utility
with Riverside outcomes.

## Assumptions and Parameters

- Schema: `campaign-coverage-v1`.
- Stabilization: five turns, one stage-specific command form, existing ruleset
  constraints, and existing observation/debrief sources.
- Affiliation: six stages, existing posture/commitment/review/integration
  commands, `AffiliationRuleset` commitment/cost bounds, and existing response
  observations.
- `get_campaign_coverage` and browser navigation are non-mutating.
- Existing generated audio maps done state to debrief, visible pressure text to
  pressure music, and committed affiliation-stage refreshes to the existing
  affiliation milestone cue; muting preserves all text.

## Educational Debrief Hooks

The shared surface links current decisions to source labels, committed history,
state hashes, and the existing campaign-specific debrief. Stabilization retains
actor rationales and attributed mechanisms. Affiliation retains alternatives,
actor response separation, obligations, and the independence/deferral question.
No score-only summary or human learning claim is added.

## Determinism and Replay Notes

The host derives coverage from current actor-visible observation and immutable
history. Repeated reads preserve turn, transition count, latest hash, and audio
state. Parameter metadata is descriptive; it does not resolve commands or
randomness. Existing replay verification remains untouched.

## Open Questions

- Which campaign-specific form errors need additional host guidance after
  adapter traces are available?
- Should later coverage add historical stage review, or is committed history
  sufficient for the first campaign-complete presentation slice?
- What evidence would authorize campaign-specific visual identity assets or
  richer audio beyond generated cues?
