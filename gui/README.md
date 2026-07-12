# GUI thin-client proof

This is a dependency-free browser surface over existing MCP-shaped data. Open
`index.html` through a static file server and provide an adapter when wiring it
to a live session:

```js
window.HsMgtGameAdapter = {
  async submitTurn(commandText) {
    // Call the existing MCP submit_turn boundary and return a SessionEnvelope.
  },
};
```

The page renders only `observation`, `legal_commands`, `history`, and `debrief`
values supplied by the adapter. It performs only empty-input checking; command
legality and state transitions remain server/core responsibilities. The demo
envelope is display fixture data, not a second simulation state.

Asset audit: zero downloaded assets, external fonts, network calls, or image
files. CSS, HTML, and JavaScript are the complete surface.
