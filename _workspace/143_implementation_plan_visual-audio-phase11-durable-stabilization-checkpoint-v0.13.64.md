# Implementation Plan — Durable stabilization host checkpoint v0.13.64

## Target slice

Close the next narrow Phase 11.1 technical boundary: an explicitly saved
`stabilization-v1` GUI checkpoint survives a stopped/restarted loopback host and
can be recovered through the existing opaque browser session handle.

## Risk and scope

- Risk: medium. The slice adds a second host-owned persistence artifact and
  campaign reconstruction, but reuses the existing stabilization save/replay
  verifier and existing browser load retry.
- In scope: host-only stabilization wrapper beside the existing competitive
  checkpoint format, explicit-save persistence, fresh-store hydration with
  replay/hash validation, live-session collision protection, loopback restart
  transport coverage, synchronized evidence/docs/version metadata.
- Out of scope: regional-affiliation durability, autosave, browser
  serialization, replay playback/regeneration, new browser route/schema,
  simulation changes, assets/audio, screenshots, human review, and public
  release.

## Design contract

1. The existing stabilization `SessionSave` replay artifact remains canonical;
   a host-only wrapper adds the opaque session ID and
   `gui-stabilization-save-v1` schema marker. The wrapper never reaches the
   browser.
2. The existing configured GUI host checkpoint path stores one latest explicit
   checkpoint. Stabilization Save replaces the prior file through a
   temporary-sibling host operation, just as competitive Save does; no archive
   or autosave is introduced.
3. A restarted host hydrates only a matching opaque ID, verifies the saved
   stabilization history through the existing deterministic replay verifier,
   reconstructs the current world, and does not enter a transition.
4. A live session always wins. A durable file cannot overwrite a newly created
   session with a colliding ID; an unclaimed checkpoint remains recoverable
   after the colliding live session ends.
5. The existing browser action-client retry remains the only browser change:
   after an unknown live read it tries host `loadSession` once, then repeats
   actor-visible reads. Browser storage remains an opaque ID only.

## Implementation steps

1. Add stabilization wrapper serialization, validation, matching-ID load, and
   terminal cleanup to the host persistence module.
2. Extend `GameSessionStore` and the real GUI host path to save/load
   stabilization sessions while preserving competitive and affiliation
   behavior.
3. Add focused malformed/save-restart/hash/collision tests and GUI transport
   restart coverage; retain the browser authority boundary tests.
4. Update the Phase 11.1 ledger, roadmap, GUI guide/README, SPEC, CHANGELOG,
   LESSONS, request/contract/QA/handoff records, and release metadata to
   v0.13.64.

## Verification and handoff

- `cargo fmt --check`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
- focused stabilization persistence/transport and browser recovery tests
- full Python suite plus release metadata, docs links, assets/security/
  generation/credits, offline/browser/device, audio/raster/visual-audio, and
  diff checks
- exactly one medium-effort read-only code reviewer
- commit, push, draft-to-ready PR, hosted checks, merge to `main`, and delete
  the temporary branch locally and remotely

## Exit evidence

The slice is complete only when a fresh host recovers the same saved
`stabilization-v1` session ID, transition count, latest hash, visible campaign
state, and deterministic continuation from the host file, while a malformed or
colliding checkpoint cannot overwrite the live session or create browser state.
