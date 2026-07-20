# Implementation Plan — Visual and Audio Phase 2 Live Read-Only Integration v0.12.18

Status: Design approved for implementation.

Branch: `feat/visual-audio-phase2-live-read-only-v0.12.18`

## User request and context

Continue the visual/audio Future track from `SPEC.md` and
`docs/history/initiatives/visual-audio/visual-audio-upgrade-proposal.md` using the preferred workflow. Phase 0
accepted the host-authoritative browser boundary and Phase 1 validated the
fixture-driven executive information architecture. Phase 2 should render a
real or recorded competitive session through a typed read-only presentation
contract without enabling graphical actions.

## Goal

Promote only the minimum structured projection needed for a one-month
`competitive-regional-v1` viewer:

- current actor-visible session and observation fields;
- player-system capacity/facility detail derived from the existing observation;
- public market signals and explicit information gaps;
- pending visible processes;
- committed transition summaries, state hashes, and replay metadata; and
- loading, error, empty, and unsupported-campaign states in the browser client.

The viewer must render facts supplied by the host/MCP adapter. It must not
submit commands, calculate outcomes, inspect `CompetitiveWorldState` in the
browser, expose resolved stochastic inputs, or create a second simulation.

## Assumptions

- Phase 2 targets `competitive-regional-v1` only; stabilization and affiliation
  remain later campaign-specific work.
- The current Rust host already computes `PlayerObservation` and committed
  `CompetitiveTransition` summaries. The new projection will select and
  serialize safe fields from those sources instead of reimplementing formulas.
- A read-only adapter can be live or recorded as long as it returns the same
  versioned envelope. The browser does not need to know which source supplied
  it.
- The existing legacy `SessionEnvelope`, `submit_turn`, and thin-client export
  remain available for compatibility, but the Phase 2 viewer path uses a
  separate `get_presentation`/`getPresentation` read-only contract.
- No browser binary is assumed; DOM contracts and Rust serialization tests are
  the available automated evidence.

## Exact implementation targets

1. `src/mcp/presentation.rs`
   - Add serializable, schema-described read-only DTOs for session summary,
     resources, observation, player institution/facility metrics, pending
     processes, replay metadata, and committed transition summaries.
   - Construct them only from actor-visible observation data, player-owned
     resources, public market signals, and immutable committed history.
   - Omit legal commands, true world state, effect queues, event metadata,
     resolved inputs, private rival actions, and the strike/private flags that
     are not part of the standard player observation.

2. `src/mcp/session.rs`, `src/mcp/server.rs`, `src/mcp/mod.rs`
   - Add `GetPresentationRequest`, `GameSessionStore::get_presentation`, and a
     `get_presentation` MCP tool with an explicit no-transition description.
   - Support only `competitive-regional-v1` in this bounded slice and return a
     typed unsupported-campaign error for other sessions.
   - Keep `start_session`, `get_observation`, `get_history`, `submit_turn`, and
     `end_session` behavior unchanged.

3. `gui/app.mjs`, `gui/index.html`, `gui/README.md`
   - Add a version-checked `createReadOnlyClient` consuming
     `HsMgtGameReadOnlyAdapter.getPresentation(sessionId)` or a recorded
     equivalent.
   - Render typed live/recorded data through the Phase 1 presentation surfaces;
     render history/hash metadata as a first replay-view prototype.
   - Add explicit loading, adapter error, empty observation, unsupported
     campaign, and missing-field states.
   - Keep Phase 1 demo rendering and legacy thin-client exports compatible, but
     do not wire the read-only client to `submitTurn` or any command form.

4. Tests and evidence
   - Add Rust unit coverage for projection shape, no-transition behavior,
     committed history/hash propagation, unsupported campaigns, and hidden-field
     exclusion after JSON serialization.
   - Add Python/Node contract coverage for the typed browser adapter, mapping,
     loading/error/empty states, read-only non-submission, and no-network/no-
     asset behavior.
   - Add `docs/history/initiatives/visual-audio/visual-audio-phase2-live-read-only-v0.12.18.md` with the contract,
     source map, boundary, checklist, limitations, and Phase 3 gate.

5. Project records
   - Promote Phase 2 in `SPEC.md`, refresh `ARCHITECTURE.md`, `README.md`,
     `CHANGELOG.md`, `LESSONS.md`, workspace evidence/mechanism notes, and
     version metadata to `0.12.18`.

## Acceptance criteria

- A live or recorded typed envelope renders current player-visible facts and
  committed history without requiring CLI syntax.
- Rust projection JSON contains no legal-command submission surface, hidden
  world state, resolved-input field, or private rival action.
- Calling `get_presentation` leaves session turn/history/hash unchanged.
- The browser renders explicit loading, error, empty, missing, and unsupported
  states and never calls `submitTurn` from the read-only client.
- Existing legacy MCP and thin-client tests remain green.
- `cargo fmt`, `cargo test`, `cargo clippy -- -D warnings`, full Python tests,
  Node syntax checks, release metadata, and whitespace checks pass.
- The diff changes no simulation transitions, randomness, replay verification,
  scenario files, audio, assets, or network-dependent core behavior.

## Non-goals

- No graphical action builder, validation, submit, batch revision, or command
  form; those belong to Phase 3.
- No monthly resolution animation, causal overlays, audio, assets, replay
  playback, mobile support, polished artwork, or campaign expansion.
- No direct `CompetitiveWorldState` serialization, private rival observation,
  resolved stochastic inputs, client formulas, or client-owned history.
- No claim of human usability, lived accessibility, learning, balance, or
  policy validity.

## Stop conditions

Stop and narrow the slice if implementation requires exposing true world state,
duplicating simulation formulas, changing transition/randomness/replay logic,
creating a browser-only command, inventing rival private data, or adding a
network/service/deployment convention not required by the existing adapter.

## Review and handoff checks

- Use one code-reviewer pass only, per the user’s workflow instruction.
- Treat serialized DTO inspection and fixture/DOM checks as technical evidence,
  not human-usability evidence.
- Merge the Phase 2 PR into `main` only after focused checks, full checks, one
  review, and CI pass; then return to Phase 3 design.
