# GUI static executive desktop prototype

This is a dependency-free Phase 1 browser surface over existing MCP-shaped data.
Open `index.html` through a static file server and provide an adapter when wiring
it to a live session:

```js
window.HsMgtGameAdapter = {
  async submitTurn(commandText) {
    // Call the existing MCP submit_turn boundary and return a SessionEnvelope.
  },
};
```

The page renders the existing `observation`, `legal_commands`, `history`, and
`debrief` values supplied by the adapter, plus an optional
`presentation_fixture` for the Phase 1 information-architecture prototype. The
fixture contains only actor-visible display data for executive metrics, briefing,
regional systems, facilities, action previews, pending processes, and a monthly
result. Selecting a system changes presentation detail only.

The command field performs only empty-input checking; command legality and state
transitions remain server/core responsibilities. The demo envelope is display fixture data,
not a second simulation state. The static desktop is designed for
an executive or first-time reviewer who needs to find finance, workforce,
capacity, access, and public rival information without reading raw JSON or CLI output.

Phase 1 review checklist:

- locate cash, margin, AP, political capital, and trust in the header;
- identify a visible workforce/capacity bottleneck from the briefing and detail;
- inspect a selected system's facility cards and access/quality metrics;
- identify a public rival signal while noting unavailable private activity;
- find action cost/delay/constraint previews and the adapter-owned command path;
- follow a pending process and monthly result back to its visible source; and
- repeat the scan at a narrower desktop width with keyboard focus visible.

This checklist is a static interface-task proxy, not human usability evidence.

Asset audit: zero downloaded assets, external fonts, network calls, or image
files. CSS, HTML, and JavaScript are the complete surface. Live read-only DTOs,
action forms, animation, audio playback, replay visualization, and campaign
expansion remain later phases.
