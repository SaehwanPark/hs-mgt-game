# Implementation Plan — Durable regional-affiliation host checkpoint v0.13.65

## Target slice

Close the remaining Phase 11/12 persistence boundary: an explicitly saved
`regional-affiliation-v1` GUI checkpoint survives a stopped/restarted loopback
host and recovers through the existing opaque browser session handle.

## Risk and scope

- Risk: medium. The slice adds one host wrapper and session reconstruction while
  reusing the existing `AffiliationReplayArtifact` serializer/verifier.
- In scope: host-only affiliation wrapper, explicit-save persistence, fresh-host
  replay/hash validation and hydration, collision protection, GUI transport
  restart coverage, synchronized evidence/docs/version metadata.
- Out of scope: autosave, browser serialization, replay playback/regeneration,
  new browser route/schema, simulation changes, assets/audio, screenshots,
  human review, and public release.

## Design contract

1. The existing `AffiliationReplayArtifact` remains canonical; a host-only
   `gui-affiliation-save-v1` wrapper adds the opaque session ID and never
   reaches JavaScript.
2. The configured GUI path stores one latest explicit checkpoint. Affiliation
   Save replaces the prior file through the existing temporary-sibling host
   operation; no archive or autosave is introduced.
3. A fresh host verifies the affiliation replay artifact with the existing
   deterministic verifier before hydrating the matching opaque ID. It restores
   history/current stage/done state without entering a transition.
4. Live sessions win over durable hydration, and terminal cleanup removes only
   a checkpoint claimed by the recovered session. Collision protection and
   repeated replacement remain shared with the previous slices.
5. The browser reuses the existing unknown-session `loadSession` retry and
   stores only the opaque session ID; no new client state path is added.

## Implementation steps

1. Add affiliation wrapper serialization, generic schema dispatch, replay
   validation, and terminal cleanup to host persistence.
2. Extend `GameSessionStore` to save/load affiliation sessions while preserving
   competitive/stabilization behavior and existing GUI path semantics.
3. Add focused persistence/session collision/restart tests and GUI transport
   coverage; preserve the browser authority boundary tests.
4. Update the Phase 11.1/12 ledgers, roadmap, guide/README, SPEC, CHANGELOG,
   LESSONS, request/contract/QA/handoff records, and release metadata to
   v0.13.65.

## Verification and handoff

- `cargo fmt --check`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
- focused affiliation persistence/restart/hash/collision and transport tests
- full Python suite plus release metadata, docs links, assets/security/
  generation/credits, device/offline/browser/audio/raster/visual-audio, and
  diff checks
- exactly one medium-effort read-only code reviewer
- commit, push, draft-to-ready PR, hosted checks, merge to `main`, and delete
  the temporary branch locally and remotely

## Exit evidence

The slice is complete only when a fresh host recovers the same saved
`regional-affiliation-v1` session ID, transition count, latest hash, visible
stage, and deterministic continuation from the host file without exposing the
serialized artifact to the browser.
