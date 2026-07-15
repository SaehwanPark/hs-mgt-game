# Visual and Audio Phase 2 — Live Read-Only Integration

Status: Implemented and merged for the `competitive-regional-v1` campaign in PR #169.

Date: 2026-07-15

Phase 2 promotes the minimum typed host projection needed to render a live or
recorded actor-visible session through the Phase 1 executive desktop. It does
not enable graphical actions or change the simulation.

## Typed read-only contract

The MCP `get_presentation` read is non-mutating and returns
`schema_version: "competitive-read-only-v1"` with these top-level fields:

| Field | Purpose | Authority/source |
| --- | --- | --- |
| `session` | Session id, campaign, seed metadata, difficulty, year/month, turn, limit, done | MCP session metadata and current competitive session |
| `resources` | Cash, action points, political capital | Player-owned visible resources |
| `observation` | Access/quality, trust, staffing, capacity, operations, market/policy bullets, gaps, and advisory options | `PlayerObservation` |
| `institutions` | Player institution and observed capacity/facility lines | Player-owned fields already used by the observation |
| `pending_effects` | Visible in-flight projects and policy review text when present | Observation fields, not client timers |
| `history` | Committed transition command summaries, events, effects, and state hashes | Immutable `CompetitiveHistory` summaries |
| `latest_transition` | Most recent committed transition when available | Immutable committed history |
| `replay` | Seed metadata, transition count, and latest committed hash | Immutable history metadata |

The projection intentionally contains no legal-command list, true world-state
object, effect queue, event metadata, resolved stochastic inputs, private rival
action, or non-observation event flag. It supports only
`competitive-regional-v1`; other campaigns receive an explicit unsupported
presentation error until their semantics have a separate projection.

## Source and authority map

The host continues to compute observations and transitions. The typed projection
selects fields and labels their source; it does not calculate margin, capacity,
trust, delay, rival behavior, outcomes, or causal explanations. The browser
maps typed values to the existing executive surfaces and owns only selection,
loading, error, focus, and recorded/live presentation state.

`get_presentation` does not advance a session. Repeated reads preserve turn,
history length, resources, and state hashes. The existing `submit_turn` path is
not used by the Phase 2 client and remains reserved for the legacy thin-client
compatibility export until Phase 3 defines graphical action submission.

## Browser adapter behavior

`gui/app.mjs` exports `createReadOnlyClient`, `validateReadOnlyEnvelope`, and
`renderReadOnlyEnvelope`. A host or recorded provider supplies:

```js
window.HsMgtGameReadOnlyAdapter = {
  sessionId: "session-1",
  async getPresentation(sessionId) {
    // Return the versioned get_presentation envelope.
  },
};
```

The client renders typed session resources, observation lines, player capacity
detail, public market signals, explicit information gaps, pending processes,
monthly operating values, transition summaries, and state hashes. It exposes
loading, empty, adapter-error, unsupported-schema, missing-observation, and
unsupported-campaign text states. It omits action submission from the read-only
path. Without an adapter, the page shows the bounded Phase 1 fixture and labels
it as static display data.

## Static review checklist

1. Load a live or recorded envelope and observe the loading-to-loaded status.
2. Locate cash, AP, political capital, workforce trust, session, and turn.
3. Inspect current access/quality, staffing, capacity, operations, and the
   observed player facility card.
4. Find public market/policy signals and an explicit information gap.
5. Follow pending process text to its observation source.
6. Inspect committed history, transition effects, and the latest state hash.
7. Exercise empty data, missing observation, adapter error, and unsupported
   schema/campaign behavior.
8. Confirm that selection and loading do not change the turn or call
   `submitTurn`.

Automated checks cover JSON shape/exclusions, no-transition behavior, typed
adapter markers, mapping, syntax, and no external assets/network calls. These
are technical and interface-task proxies; they do not establish human usability,
engagement, lived accessibility, learning, classroom effectiveness, domain
validity, calibration, or policy validity.

## Explicit non-goals and next gate

This phase does not implement action forms, command validation or submission,
batch revision, monthly resolution, animation, causal overlays, audio, assets,
replay playback controls, mobile support, instructor true-state views, or other
campaigns. It does not change transitions, randomness, replay verification,
history semantics, hashes, or debrief generation.

Phase 3 is the next candidate: contextual action submission through canonical
commands, host validation, batch revision/removal, rejection atomicity, and one
graphical competitive month. Phase 3 must reuse the typed observation/command
authority boundary and must not imply stochastic certainty.
