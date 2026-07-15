# GUI executive desktop and contextual action builder

This is a dependency-free Phase 2/3/4 browser surface over typed actor-visible
MCP presentation, action, and resolution contracts. Open `index.html` through a
static file server and provide a live or recorded read-only adapter:

```js
window.HsMgtGameReadOnlyAdapter = {
  sessionId: "session-1",
  async getPresentation(sessionId) {
    // Call get_presentation or return a recorded envelope with the same schema.
  },
};
```

The read-only client expects `schema_version: "competitive-read-only-v1"` and
renders the typed `session`, `resources`, `observation`, `institutions`,
`pending_effects`, `history`, `latest_transition`, and `replay` fields. It can
consume live MCP output or a recorded envelope without knowing which source
provided it. The demo envelope is display fixture data, not a second simulation
state, and remains available when no read-only adapter is configured.

For the Phase 3/4 action and resolution path, inject a separate host adapter with
`getPresentation`, `getActionCatalog`, `validateTurn`, and `submitTurn`. The
page then renders forms from the host action catalog, keeps draft rows locally,
and submits only an unchanged batch that the host marked valid:

```js
window.HsMgtGameActionAdapter = {
  sessionId: "session-1",
  async getPresentation(sessionId) {},
  async getActionCatalog(sessionId) {},
  async validateTurn(sessionId, commandText) {},
  async getResolution(sessionId, turn) {},
  async submitTurn(commandText) {},
};
```

`createReadOnlyClient` never calls `submitTurn`. The action-builder path is
enabled only when `HsMgtGameActionAdapter` is supplied; it submits only an
unchanged host-validated batch. The legacy `createThinClient` and
`HsMgtGameAdapter.submitTurn` export remain available for compatibility with
the earlier thin-client proof, but are not wired into the Phase 3/4 page.
Host/core code remains authoritative for commands, transitions, randomness,
history, hashes, and debriefs.

After a successful action submission, `getResolution(sessionId, turn)` may
return `schema_version: "competitive-resolution-v1"`. The page renders the
eight host-sourced resolution steps, before/after operating/resource values,
direct committed effects, and state hash. Play, pause, skip, review, and a
historical-turn read are local presentation controls; `getResolution` never
advances the session. Text remains in the DOM when paused or reduced motion is
enabled.

Phase 2/3/4 review checklist:

- load a live or recorded envelope and observe the loading-to-loaded state;
- locate typed cash, AP, political capital, trust, and session metadata;
- inspect current observation, observed player capacity/facility metrics, and
  public market/information-gap signals;
- follow a pending process and monthly result back to its typed source;
- inspect committed transitions and state hashes without changing the turn;
- exercise empty, missing, unsupported-schema, and adapter-error states; and
- verify that the read-only path does not expose or call command submission.
- with the action adapter, add/revise/remove drafts, validate through the host,
  and confirm submit is unavailable until validation passes.
- after a committed submit, locate all eight resolution steps and compare the
  before/after snapshots without treating differences as inferred causality;
- pause, skip, review a historical committed turn, and enable reduced motion;
  confirm text remains complete and no session transition occurs.

This checklist is a technical/interface-task proxy, not human usability or
lived-accessibility evidence.

Asset audit: zero downloaded assets, external fonts, network calls, or image
files. CSS, HTML, and JavaScript are the complete surface. The typed projection
contains no true-world state, resolved stochastic inputs, private rival actions,
or client-side cost formula. Resolution animation, causal overlays, audio,
assets, and campaign expansion remain later phases. Phase 4 resolution pacing is
presentation-only and has no audio playback or downloaded assets.
