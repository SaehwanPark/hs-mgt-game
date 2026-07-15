# Evidence Map — Visual and Audio Phase 6 Regional World v0.12.22

## Scope

Phase 6 turns the existing report/map panel into a persistent, navigable
schematic regional view backed by a host projection. It does not add geography
or new simulation state.

## Sources Reviewed

- Phase 6 and first-vertical-slice requirements in
  `docs/visual_audio_upgrade_proposal.md`.
- Phase 0 source/hidden-state/map policy and Phase 1–5 GUI/MCP contracts.
- `PlayerObservation`, `CompetitiveWorldState.public_action_log`,
  `ReadOnlyPresentationEnvelope`, and existing pending-process sources.
- README, SPEC, architecture, design principles, and harness spec.

## Mechanisms and Institutions

The map presents the regional institution set as an executive information
surface. The human system gets owned facility/process detail and visible
operating overlays. Rival markers communicate identity and public signals only;
their private operating state remains unavailable.

## Actor Incentives and Information

Player demand, access, unmet demand, capacity, and projects are shown with
source labels. Rival public actions appear only through the existing one-month
observation lag and are labeled observed/reported. No map marker is a proxy for
unobserved rival utility, hidden capacity, geographic influence, or outcome.

## Assumptions

- Existing player observation plus public action log are sufficient for a first
  regional-world DTO; no true-state serialization is required.
- A stable schematic position derived from public entity ordering is display
  layout, not a geography claim or simulation coordinate.
- The host can classify the human system and public rival identities while
  filtering rival private metrics and projects.
- Existing `get_presentation` can remain unchanged; an additive
  `competitive-regional-world-v1` read is safer than widening unrelated DTOs.

## Unresolved Questions

- Which visual relationship signals are truly public enough to deserve a map
  edge rather than a linked briefing item?
- When should public rival signals age out of the map versus remain in history?
- What evidence would justify real geography, distance, or richer asset work?

## Design Implications

- Add a typed regional-world envelope with entities, owned facilities, public
  signals, visible overlays, active player processes, source labels, and layout
  metadata.
- Keep map selection, active overlay, and panel navigation local; reload the
  projection for current/historical presentation without mutation.
- Build rival signals from the same lagged visible public source used by human
  observation, not from rival `HealthSystemState` fields.
- Make missing public signal, unavailable rival detail, and absent player
  process explicit in the UI.

## Risks

Map polish can imply false geography, hidden rival knowledge, or a city-builder
scope. Use a schematic legend, source/lag labels, minimal markers, and a QA gate
that rejects any client-side metric reconstruction or private rival field.
