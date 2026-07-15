# Visual and Audio Phase 6 — Regional Map and Persistent World

Status: Implemented and reviewed on the Phase 6 branch; ready for PR handoff.

Phase 6 makes the `competitive-regional-v1` situation navigable as a schematic
institutional world. The host supplies actor-visible identities, owned detail,
public rival signals, overlays, and process links; the browser supplies map
layout, selection, and navigation. This is not geographic simulation.

## Typed regional-world contract

The planned `competitive-regional-world-v1` envelope contains:

- session/replay metadata and schema version;
- stable schematic entities with identity, role, status, layout slot, source,
  owned/public visibility, facilities, and public signal lines;
- player-visible demand, access, unmet-demand, capacity-pressure, and pending
  process overlays with values, labels, sources, and equivalents;
- navigation targets for briefing, map, selected detail, and pending timeline;
  and
- explicit unavailable/missing notes for rival private detail, absent public
  signal, or absent player process.

The host exposes this envelope through the non-mutating
`get_regional_world(session_id)` read.

Schematic layout slots are presentation geometry only. No coordinate represents
distance, travel, catchment, patient movement, or an unmodeled relationship.

## Source and authority map

Rival public signals use the existing one-month observation lag and retain
their observed/reported month in the envelope.

| Surface | Source | Visibility rule |
| --- | --- | --- |
| Player identity/facilities | human system plus `PlayerObservation` | owned detail |
| Player demand/access overlays | `PlayerObservation` | reported/observed labels |
| Player projects/processes | `PlayerObservation.in_flight_projects` | visible commitment, not outcome promise |
| Rival identity | public system identity | public name/role only |
| Rival signal | lagged `public_action_log` through human observation | observed/reported month and source text |
| Map layout | deterministic display slot | no geography claim |

## Browser behavior

The page adds map view, overlay chooser, entity selection, and links between
briefing, map, selected detail, and pending timeline. Selection changes only DOM
and local client state. Source, lag, unavailable-detail, and missing-signal text
remain visible without hover. Existing action, resolution, audio, history, and
debrief paths remain available.

An adapter error, unsupported schema, empty world, or unavailable public signal
is rendered as recoverable presentation state. The browser never calls
`submit_turn` from map navigation and never reconstructs a regional metric from
private fields.

## Static review checklist

1. Load a current world envelope and identify the player, public rivals, owned
   facilities, current overlays, and pending processes.
2. Select each entity and overlay; follow links to briefing/detail/timeline.
3. Confirm rival signals carry observed/reported timing and private detail says
   unavailable.
4. Exercise missing signal/process, empty, unsupported, and adapter-error states.
5. Repeat the read and confirm session turn, history, hash, and audio state are
   unchanged.
6. Use keyboard navigation and reduced motion; confirm no content depends on
   hover or animation.
7. Confirm no geography, route, patient movement, private rival metric, map
   formula, asset, or network behavior appears.

These are technical/interface-task checks only. They do not establish human
comprehension, usability, lived accessibility, learning, engagement,
calibration, balance, domain validity, or policy validity.

## Explicit non-goals and next gate

This phase does not add true geography, distances, routes, patient movement,
city-builder mechanics, rival private state, broad map assets, relationships,
other campaigns, an instructor true-state view, or human evaluation.

Phase 7 is the next candidate: campaign coverage for stabilization and
affiliation only after shared primitives preserve campaign-specific semantics.
