# Implementation Plan — v0.13.105 host save-artifact download

## Goal

Close the bounded technical gap between host-owned checkpoint persistence and
user-requested file download without moving serialization or authority into
the browser.

## Contract

1. Add a host route for an opaque checkpoint artifact download. It accepts a
   validated session ID and optional `storage=archive|legacy` selector.
2. The host resolves the configured checkpoint path, rejects unsafe IDs,
   symlinks, missing files, unsupported schemas, mismatched IDs, and invalid
   save contents, then serves the exact validated file bytes with a safe
   attachment filename.
3. The local adapter exposes the host download operation. The GUI adds an
   explicit **Download host save** action for discovered entries and keeps
   the archive/legacy source in the request.
4. Browser code treats the response as an opaque download payload only. It
   does not inspect save bytes, deserialize them, write browser storage, load
   a session, or mutate game state. Errors remain written and recoverable.
5. Existing Save/Restore, reference import/export, checkpoint discovery,
   autosave, replay, and host/core transitions remain unchanged.

## Files expected to change

- `src/mcp/persistence.rs`, `src/mcp/session.rs`, `src/gui_server.rs`
- `gui/host-adapter.mjs`, `gui/app.mjs`, `gui/index.html`
- focused Rust/Node/Python tests and phase ledgers/audit
- release metadata and v0.13.105 roadmap/changelog/spec/handoff docs

## Verification

- Rust formatter, tests, and Clippy
- full Python suite and focused browser/transport/persistence tests
- loading/offline/browser compatibility and documentation validators
- explicit assertions that download is host-validated, opaque, manual, and
  non-mutating
- update the low-power source-byte proxy only if the measured source changes

## Open boundaries after this slice

Automatic resume policy, replay regeneration, screenshots, human usability,
accessibility/educational/listening review, browser/device certification,
asset provenance/legal review, revision/expansion decisions, and public
release approval remain outside this technical slice.
