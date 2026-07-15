# Implementation Plan — Live competitive GUI repair v0.12.31

1. Add a loopback-only Axum binary around the existing `GameSessionStore` and
   serve embedded GUI assets with conditional host-adapter injection.
2. Add the same-origin action adapter, preserve static demo bootstrap, and make
   replacement-session activation transactional from the browser's view.
3. Remove unsupported campaign-coverage reads from competitive live flows.
4. Add real transport, adapter, documentation, and regression tests.
5. Add exact README/How-to/GUI instructions, ADR, architecture/spec/changelog,
   lesson, release metadata, domain QA, and final handoff.

Acceptance: `cargo run --bin hs-mgt-game-gui` prints a loopback URL and a player
can start, validate, submit, resolve, and refresh one competitive month without
manual adapter injection or a false recovery state.
