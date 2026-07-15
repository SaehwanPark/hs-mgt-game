# Request Summary — Visual and Audio Phase 6 Regional World v0.12.22

## Scope

- Continue the merged Phase 5 one-month competitive presentation with a bounded
  persistent regional-world surface.
- Add a host-owned actor-visible regional-world projection containing a
  schematic identity map, player facility/process detail, player-visible
  demand/access overlays, and public rival signals.
- Add browser navigation between briefing, map, selected detail, and pending
  timeline while preserving the existing action, resolution, audio, and
  read-only contracts.
- Respect the existing lagged public-rival observation boundary; do not expose
  rival private metrics, effect queues, true geography, or hidden projects.

## Sources

- `docs/visual_audio_upgrade_proposal.md` Phase 6 requirements and exit gate.
- Phase 0 map/identity/access policy and merged Phase 1–5 presentation docs.
- `src/sim/observe_competitive.rs`, `src/mcp/presentation.rs`, current public
  action log semantics, and `gui/app.mjs`/`gui/index.html`.
- Canonical product docs, architecture, design principles, versioning policy,
  lessons, and harness team spec.

## Expected files

- Typed actor-visible regional-world DTO and non-mutating MCP/session read.
- Browser schematic map/overlay/detail/navigation rendering over that DTO.
- Static host/browser tests for source mapping, observation lag, hidden-field
  exclusion, selection/navigation, empty/missing states, and no map simulation.
- Phase 6 contract document, SPEC/architecture/version records, tests, evidence,
  domain QA, lessons, and final handoff.

## Validation target

- Every map marker, facility, overlay, public signal, and process has a host or
  actor-visible source and an explicit missingness/lag label.
- Player detail can expose owned facilities, capacity, operations, and projects;
  rival identity is public while rival private operations remain unavailable.
- Map selection and navigation change presentation state only. Commands,
  transitions, audio, history, hashes, and replay remain unchanged.
- Decorative geometry is schematic and supports an actionable or explanatory
  question; no coordinate or relationship implies an unmodeled mechanic.

## Explicit non-goals

No true regional geography, routing, distance, travel, patient movement,
city-builder systems, rival private metrics/projects, new campaign support,
downloaded visual assets, simulation formulas, browser-owned world state, or
human usability/domain-validity claim.

## Global workflow

Use the repo orchestrator, evidence mapper, mechanism designer, domain QA, and
end-user experience workflow; use simple-code/spec-driven/plan-design skills and
the preferred workflow with exactly one code reviewer. Implement on this branch,
verify, open a PR, review once, merge into `main`, and then design Phase 7 only
after the Phase 6 gate closes.
