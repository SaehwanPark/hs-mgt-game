# Mechanism Design — Visual and Audio Phase 4 Resolution/Causal Feedback v0.12.20

## Goal and Roadmap Phase

Make one already committed competitive month legible and reviewable through a
host-owned resolution presentation. This is roadmap Phase 4 and follows the
Phase 3 graphical action path; it precedes audio, assets, and broader replay.

## Slice Boundary

The host exposes the latest or a selected historical competitive transition as
`competitive-resolution-v1`. The envelope contains actor-visible before/after
snapshots, ordered presentation steps, existing committed event/effect text,
operating/resource breakdowns, pending processes, and state-hash metadata. The
browser renders the full textual result immediately and may reveal steps with
local play/pause/skip/review controls. There is no new transition call.

## Actors and Authority

The Rust simulation and MCP host own transition evaluation, explicit stochastic
inputs, actor observations, committed events/effects, resources, pending
processes, history, hashes, and debriefs. The browser owns only step index,
paused/skipped/review mode, reduced-motion preference, selection, and DOM/CSS
pacing. A replay read is host-derived and non-mutating.

## State, Beliefs, and Observations

The true `CompetitiveWorldState` remains behind the host boundary. The host
projects `CompetitiveTransition.prior` and `.next` through the same human
observation path used by the read-only viewer. Decision-time and post-transition
snapshots are labeled separately. Existing events/effects are rendered as
committed source text; no hidden rival action, resolved input, or inferred
causal edge is reconstructed in the client.

## Commands, Events, and Effects

`get_resolution(session_id, turn?)` reads a committed transition from history;
omitting `turn` selects the latest. The ordered presentation steps are:

1. submitted batch;
2. visible institutional responses;
3. process advancement;
4. operating result;
5. resource changes;
6. direct committed effects;
7. newly visible information; and
8. updated pending processes.

Each step has a stable ID, label, source, and text/items. Invalid session,
unsupported campaign, unavailable turn, and no-history cases are recoverable
read errors. `submit_turn` remains the sole mutation.

## Strategic Interaction

The resolution presentation shows that the player's action is one institutional
input among rival and environmental responses. It may show public responses and
player-owned consequences already present in the accepted transition summary,
but it does not reveal private rival choices or imply that sequence order caused
the outcome. A valid command can still produce an unfavorable result.

## Assumptions and Parameters

- Schema: `competitive-resolution-v1`.
- First supported campaign: `competitive-regional-v1`.
- The envelope uses current host observation/resource types and existing
  `TransitionSummary` source strings before any richer structured effect schema.
- Comparison display may show `before → after` values for visible metrics; it
  must not call that comparison a causal explanation.
- CSS reveal timing is intentionally short, skippable, and reduced-motion safe.

## Educational Debrief Hooks

The sequence separates what was submitted, what became visible, and what the
host attributes directly to committed effects. Review mode preserves the full
textual record and state hash so a learner or instructor can ask which facts
were available before the decision and which appeared afterward. This phase
does not claim comprehension or learning.

## Determinism and Replay Notes

Resolution reads derive only from immutable committed history and the same
actor-visible projection used by the live viewer. They do not resolve random
inputs, write presentation state into the simulation, advance turns, rewrite
history, or change hashes. Replaying a selected month calls only the read-only
resolution path.

## Open Questions

- Is a future structured causal-effect DTO needed after the first sequence is
  inspected, or are accepted source strings sufficient?
- Which direct effect groups should be promoted into visual overlay categories?
- What evidence is required before expanding the action workflow to other
  campaigns or adding richer contextual entity filters?
