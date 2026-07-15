# Evidence Map — Visual/audio Phase 13 first-month continuity v0.12.29

## Sources reviewed

- `SPEC.md` product contract, intended experience, presentation/action
  boundary, evidence-gated sequence, first competitive vertical slice, and
  promotion rules.
- `docs/visual_audio_upgrade_proposal.md` sections 4, 7, 8, 9, 14, 15, and
  16, especially the exact one-month experience and integration test gate.
- Phase 0–12 alignment/protocol documents and their focused test contracts.
- `gui/app.mjs`, `gui/index.html`, `gui/README.md`, `gui/audio.mjs`,
  `gui/playtest.mjs`, and existing GUI launch/action/resolution tests.
- Canonical README, proposal, roadmap, design principles, architecture, and
  harness team spec.

## Observed gap

The browser already has separate working boundaries for session launch/load,
read-only presentation, regional-world reads, campaign coverage, action
catalog/validation, resolution, refreshed presentation, and optional audio.
The client does not expose one explicit, testable presentation contract that
connects those handoffs into the planned first-month path. Existing behavior
is therefore available but difficult to audit as a complete vertical slice.

## Evidence classification

- Technical correctness: a deterministic stage vocabulary and adapter-sequence
  test can verify the handoff order and failure behavior.
- Interface-task proxy: the visible rail can expose where the client is in the
  host-shaped workflow and preserve text when actions or resolution are not
  available.
- Unresolved human question: whether the rail improves comprehension, reduces
  friction, or feels inviting requires later human evaluation and is not
  promoted by this slice.

## Boundary evidence

- `createSessionLauncher` owns only host start/load requests and delegates the
  presentation read to the existing client loader.
- `createActionClient` already keeps draft actions local, requires unchanged
  host validation, submits only through `submitTurn`, reads resolution without
  advancing it, and refreshes actor-visible presentation afterward.
- `createReadOnlyClient` remains submit-free.
- `createFirstMonthFlow` will own only local stage rendering and a small
  serializable state projection; it will not receive adapter payloads or enter
  replay/history/hash data.

## Unresolved questions

- Whether a later browser host needs a richer flow event contract remains
  separate; this slice uses the current local client boundary.
- Whether a first-month rail should become campaign-specific is deferred until
  a later campaign coverage gate.
