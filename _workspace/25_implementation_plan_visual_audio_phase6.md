# Implementation Plan — Visual and Audio Phase 6 Regional World v0.12.22

Status: Implemented and fully verified; pending exactly one review pass and PR
handoff.

## Task restatement

Add one actor-visible, host-derived schematic regional-world projection and
render it in the existing browser surface. Keep map identity, player facilities,
visible overlays, public rival signals, and pending processes useful for
executive navigation without introducing geography, a browser world model, or
private rival state.

## Current understanding

- `ReadOnlyPresentationEnvelope` currently contains one player institution,
  player-visible operations/capacity, pending processes, history, and public
  market bullets.
- `CompetitiveWorldState` also contains public action log entries and system
  identities, but rival `HealthSystemState` metrics and effect queues must not
  cross the standard player boundary.
- Phase 1 already has a fixture map/entity card and Phase 2–5 have host/action/
  resolution/audio patterns that can be extended with an additive DTO.
- The existing observation helper applies the public rival lag and must remain
  the source of all map signals.

## Assumptions

- An additive read-only `get_regional_world` projection can safely filter
  public system identities/signals and player-owned detail.
- Stable layout slots are sufficient; no geographic coordinates or map asset
  pipeline is needed for this gate.
- Existing history can provide the current observation; historical map review
  is deferred unless source timing remains unambiguous.

If rival visibility cannot be filtered without leaking true state, or if map
behavior needs new simulation semantics, stop before editing the core.

## Minimal implementation plan

1. Add `competitive-regional-world-v1` DTOs in `src/mcp/regional_world.rs` for
   session/replay, entities, owned facilities, public signals, overlays,
   navigation, and missingness/source metadata.
2. Add a non-mutating `GetRegionalWorldRequest`, store method, and MCP tool;
   derive the human entity from `observe_for_human`, public rival names/signals
   from the lagged public log, and never serialize rival health-system metrics.
3. Add Rust tests for normal projection, public lag, hidden-field exclusion,
   unsupported campaign, no mutation/hash stability, and missing signal/process.
4. Add browser map renderer/navigation/overlay/detail links over the typed DTO;
   keep selection and active overlay local and preserve action/resolution/audio
   clients. Add empty/unsupported/adapter-error states.
5. Add GUI/static tests for source labels, no private fields/formulas, identity,
   overlay, timeline, keyboard navigation, and no asset/network behavior.
6. Update Phase 6 contract, SPEC/architecture/README/changelog/lessons, version
   metadata to `0.12.22`, evidence/domain QA/handoff records.
7. Run focused/full checks, perform exactly one code-review pass, push, PR, CI,
   merge into `main`, and record Phase 7 as the next gate.

## Files and functions likely to change

- `src/mcp/regional_world.rs`, `src/mcp/session.rs`, `src/mcp/server.rs`, and
  `src/mcp/mod.rs`: typed host projection, request, tool, and tests.
- `gui/app.mjs`, `gui/index.html`, `gui/README.md`: schematic map, overlays,
  navigation, detail/timeline links, and adapter guidance.
- `tests/test_gui_regional_world.py`: static browser/source-boundary tests.
- Phase 6 contract/project records, metadata, lessons, QA, and handoff.

Avoid editing transition, resolver, randomness, scenario, audio, or replay
verification files. Do not add map assets, fetches, coordinates that imply
geography, or a browser-owned regional state model.

## Tests and checks

Run:

- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1`
- `python3 -m unittest tests/test_gui_regional_world.py tests/test_gui_audio.py tests/test_gui_resolution.py`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `node --check gui/app.mjs`
- `python3 scripts/check_release_metadata.py`
- `git diff --check`

Expected result: host projection tests prove actor-visible filtering and
non-mutating reads; browser tests prove map/navigation/overlay rendering without
formulas, assets, network, or transition calls; all existing tests remain green.

## Acceptance criteria

- `get_regional_world` returns a typed current actor-visible map/world envelope
  for competitive sessions with stable entity IDs, source labels, overlays,
  facilities/processes, navigation, and explicit missingness.
- Player-owned facility/operating detail is visible; rival identity and
  lagged public signals are visible; rival private metrics, projects, true
  coordinates, effect queues, and hidden state are absent.
- Browser navigation/selection/overlay changes do not submit commands, mutate
  session/history/hash, or change audio settings/state.
- Map elements support a decision or explanation and remain legible without
  hover-only content; keyboard and reduced-motion paths preserve content.
- No transition formula, new command, other campaign, downloaded asset, network
  behavior, or human comprehension/domain-validity claim is added.

## Non-goals

- No true geography, distances, routes, patient movement, city-builder, or
  facility simulation.
- No rival private operations/capacity/workforce/resources/project queues.
- No map asset library, general relationship/equilibrium model, mobile redesign,
  campaign expansion, or instructor true-state view.

## Stop conditions

Stop and request direction if the public observation lag cannot be preserved,
the host must expose rival private fields, the browser needs to calculate map
metrics, any marker implies unsupported geography/relationship, or the map needs
simulation mutation to become useful.

## Review checklist

- DTO fields have explicit source/visibility labels and hidden-field tests.
- Public rival signals match existing lagged observation text and do not use
  rival `HealthSystemState` metrics.
- Player facilities/processes and demand/access overlays are actor-visible.
- Map selection/navigation is local, keyboard-reachable, and not hover-only.
- Empty/missing/unsupported/adapter-error states are explicit.
- No assets/network/formulas/core changes appear; exact one review pass occurs.

## Risk label

Risk: high. This is an additive host projection with a new identity/visibility
surface; the main risks are rival information leakage, false geography claims,
and map polish expanding beyond decision-support scope.
