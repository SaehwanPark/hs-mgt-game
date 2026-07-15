# Mechanism Design — Visual and Audio Phase 6 Regional World v0.12.22

## Goal and Roadmap Phase

Make one competitive regional situation navigable as an evolving institutional
system rather than a set of disconnected reports. This is roadmap Phase 6 after
the merged action, resolution, and optional-audio slices.

## Slice Boundary

The host exposes `competitive-regional-world-v1` as a non-mutating read for
`competitive-regional-v1`. It contains a schematic layout, public entity
identity, owned player facilities/processes, actor-visible demand/access and
operating overlays, public rival signals at the existing lag, and source/lag
metadata. It does not contain true coordinates, rival private metrics, or map
simulation.

## Actors and Authority

Rust/MCP owns projection, identity filtering, public-signal timing, observations,
history, and hashes. The browser owns selected entity, active overlay, panel
navigation, viewport, and display geometry. Audio remains the existing optional
client layer; map selection does not trigger simulation or hidden audio state.

## State, Beliefs, and Observations

The human entity may expose owned facility names, visible capacity metrics,
operations, access, demand, unmet demand, and in-flight projects. Rival entities
expose name, public role, public signal text, observed month, and explicit detail
unavailability. Overlay values use actor-visible player observations and are
labeled as reported/observed; missing or lagged information remains visible.

## Commands, Events, and Effects

The read returns:

1. a schema/session/replay envelope;
2. schematic `entities` with stable IDs, role, label, layout position, status,
   source, facilities, and public signals;
3. `overlays` for visible demand, access, unmet demand, capacity pressure, and
   process categories with value/label/source/equivalent;
4. `navigation` targets for briefing, map, detail, and pending timeline; and
5. explicit `missing`/`unavailable` notes.

`get_regional_world(session_id)` is read-only and never calls `submit_turn`.
Entity selection and overlay changes are client-only presentation state.

## Strategic Interaction

The map supports executive questions: where is the player's visible bottleneck,
which owned facility/process explains it, and what public rival signal deserves
attention? It does not optimize routes, rank institutions, imply social welfare,
or reveal a rival's hidden strategy.

## Assumptions and Parameters

- Schema: `competitive-regional-world-v1`.
- First supported campaign: `competitive-regional-v1`.
- Schematic positions are deterministic layout slots, not geographic data.
- Public signals use the existing one-month lag and source text; no new lag
  formula is introduced.
- Empty public signals, no active process, unsupported campaign, and unavailable
  historical projection are explicit read errors/states.

## Educational Debrief Hooks

The map links visible overlays to facility, briefing, and pending-process source
labels. A learner can distinguish owned detail from public rival identity and
reported signal timing. This phase does not claim comprehension, learning,
calibration, or domain validity.

## Determinism and Replay Notes

The host derives the envelope from current actor-visible observation and public
history without changing session state. Repeated reads preserve turn, history,
hash, and audio state; historical reads are bounded to committed presentation
sources if enabled. Layout slot selection is deterministic and presentation-only.

## Open Questions

- Is the identity/signal map enough to justify a later relationship layer?
- Which overlay combinations remain legible at smaller viewports?
- What evidence would authorize asset-backed map identity or true geography?
