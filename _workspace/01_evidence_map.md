# Evidence Map — Visual and Audio Phase 4 Resolution/Causal Feedback v0.12.20

## Scope

Phase 4 presents one committed competitive transition as a sequence of visible
decision, response, process, operating, resource, information, and pending-work
states. It does not alter how the transition is resolved.

## Sources Reviewed

- `docs/visual_audio_upgrade_proposal.md` Phase 4 and first-vertical-slice
  requirements.
- Phase 0 alignment, Phase 1 static desktop, Phase 2 read-only projection, and
  Phase 3 contextual action contract.
- `src/model/competitive_history.rs`, `src/model/events.rs`,
  `src/sim/observe_competitive.rs`, `src/mcp/presentation.rs`, and
  `src/mcp/session.rs`.
- README, SPEC, architecture, design principles, and project harness spec.

## Mechanisms and Institutions

The player is the executive of the human health system. A committed monthly
transition already contains player/rival responses, process changes, operating
effects, resource changes, and actor-visible information. Phase 4 gives those
existing institutional consequences separate presentation homes without adding
an actor or a new decision rule.

## Actor Incentives and Information

The browser may show the player's submitted batch, the host's committed event
and effect summaries, before/after player-visible operations/resources, updated
observations, and pending processes. It must not expose true world state,
unresolved stochastic inputs, private rival actions, or a causal story inferred
from hidden fields. Replay uses the same actor-visible envelope for the selected
committed transition.

## Assumptions

- `CompetitiveTransition.prior`, `next`, `events`, `effects`, and history are
  sufficient to build the first typed resolution envelope after safe actor-
  visible projection.
- `observe_for_human` remains the authoritative projection for decision-time and
  post-transition observations; no browser snapshot becomes simulation state.
- A before/after value comparison is presentation logic, not a causal formula.
- Existing `TransitionSummary` event/effect text is already an accepted player-
  visible source and can be reused without exposing new private fields.
- CSS/DOM reveal pacing is sufficient for Phase 4; audio and asset work remain
  gated to Phase 5.

## Unresolved Questions

- Which event/effect labels deserve grouping before a later structured causal
  DTO is justified?
- How should a later replay browser expose multiple months without making the
  first one-month surface a general replay editor?
- Which visible bottleneck cues are understandable to first-time users rather
  than merely traceable to source strings?

## Design Implications

- Add one versioned `competitive-resolution-v1` read-only contract with safe
  before/after snapshots, ordered presentation steps, direct committed effects,
  operating/resource breakdowns, and state-hash metadata.
- Store no presentation timeline in the simulation history; resolve the
  selected transition from immutable session history on each read.
- Keep textual results in the DOM before any animated reveal. Pause and reduced
  motion must change pacing, not content.
- Make replay lookup explicit and non-mutating so a later review cannot call
  `submit_turn` or alter the current session.

## Risks

The phrase “causal” can overclaim if the UI turns correlated effects or
before/after differences into an inferred graph. Render only host-attributed
effects and label simple comparisons as changes, not explanations. A technically
complete sequence is not evidence of human comprehension, learning, or domain
validity.
