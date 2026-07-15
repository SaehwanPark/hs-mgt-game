# Mechanism Design — Visual and Audio Phase 2 Live Read-Only Integration v0.12.18

## Goal and Roadmap Phase

Render one real or recorded `competitive-regional-v1` session through a typed
actor-visible projection. This is roadmap Phase 2 and deliberately precedes
graphical action submission.

## Slice Boundary

The host exposes a versioned read-only presentation envelope containing session
summary/resources, current player observation, observed player capacity/facility
detail, public market signals and information gaps, pending processes, committed
transition summaries, state hashes, and replay metadata. The browser renders
the envelope through the Phase 1 surfaces and supports loading/error/empty and
unsupported-campaign states. No transition is run by this path.

## Actors and Authority

The Rust engine and MCP store remain authoritative for observation generation,
legal commands, resolved stochastic inputs, transitions, pending effects,
immutable history, replay hashes, and debriefs. The typed projection is a
read-only host boundary. The browser owns only rendering, selection, loading,
error, focus, and recorded/live source state; it has no command authority.

## State, Beliefs, and Observations

DTO fields are selected from `PlayerObservation`, player-owned visible resource
fields, public market signals, and committed `CompetitiveTransition` summaries.
The projection omits `CompetitiveWorldState`, `effect_queue`, `event_metadata`,
resolved inputs, legal commands, private rival actions, and non-observation
flags. Missing values remain `null`/empty with an explicit UI label.

## Commands, Events, and Effects

`get_presentation` is a non-mutating MCP read. It returns committed transition
events/effects and hashes for the replay prototype but cannot parse, validate,
or submit commands. `submit_turn` remains a separate legacy tool and is not
called by the Phase 2 read-only browser client.

## Strategic Interaction

The player can inspect visible capacity/workforce pressure and public market
signals in context, then review the committed history that produced the current
observation. The slice intentionally does not offer an action response; that
choice is reserved for Phase 3 where canonical command equivalence and
rejection atomicity can be tested.

## Assumptions and Parameters

- Contract schema version: `competitive-read-only-v1`.
- First supported campaign: `competitive-regional-v1`.
- Recorded providers return the same envelope as live providers.
- A player facility is represented by observed capacity/staffing metrics, not
  an inferred hidden facility object.
- No client-side numeric formula, status classifier, timer, or stochastic
  forecast is introduced.

## Educational Debrief Hooks

Committed command summaries, visible events/effects, and hashes remain
reviewable without claiming that the browser has established causal learning.
Debrief generation remains host-owned; no instructor true-state view is added.

## Determinism and Replay Notes

`get_presentation` must not change turn, history length, state hash, or session
resources. Repeated reads of the same live/recorded session must serialize
equivalent visible facts. Replay metadata is a view over committed history, not
new simulation history.

## Open Questions

- Whether public rival identities need a separate structured source in Phase 3+
  rather than current market bullets.
- Whether the Phase 3 action catalog can be promoted without extending the
  presentation projection beyond visible command metadata.
- Which replay navigation controls are justified after a static history view.
