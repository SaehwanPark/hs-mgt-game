# GUI live read-only executive desktop

This is a dependency-free Phase 2 browser surface over a typed actor-visible
MCP presentation contract. Open `index.html` through a static file server and
provide a live or recorded read-only adapter:

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

`createReadOnlyClient` never calls `submitTurn`; action submission is deferred to
Phase 3. The legacy `createThinClient` and `HsMgtGameAdapter.submitTurn` export
remain available for compatibility with the earlier thin-client proof, but are
not wired into the Phase 2 page. Host/core code remains authoritative for
commands, transitions, randomness, history, hashes, and debriefs.

Phase 2 review checklist:

- load a live or recorded envelope and observe the loading-to-loaded state;
- locate typed cash, AP, political capital, trust, and session metadata;
- inspect current observation, observed player capacity/facility metrics, and
  public market/information-gap signals;
- follow a pending process and monthly result back to its typed source;
- inspect committed transitions and state hashes without changing the turn;
- exercise empty, missing, unsupported-schema, and adapter-error states; and
- verify that the read-only path does not expose or call command submission.

This checklist is a technical/interface-task proxy, not human usability or
lived-accessibility evidence.

Asset audit: zero downloaded assets, external fonts, network calls, or image
files. CSS, HTML, and JavaScript are the complete surface. The typed projection
contains no true-world state, resolved stochastic inputs, private rival actions,
or legal-command submission fields. Graphical actions, animation, audio, assets,
replay playback, and campaign expansion remain later phases.
