# Implementation Plan — Visual/audio Phase 11.1 live checkpoint continuity v0.12.96

## Target slice

Add a bounded host-owned save/restore checkpoint handoff for the live
`competitive-regional-v1` GUI. A checkpoint is an in-memory clone of the
current host session; restoring it must refresh the visible presentation,
history, replay metadata, and action catalog from the host.

## Evidence and constraints

- The CLI already has durable `CompetitiveSessionSave` artifacts and replay
  verification, but the loopback `GameSessionStore` is currently ephemeral and
  has no live checkpoint operation.
- The host session types and committed histories can be cloned without
  changing transition rules or hashes.
- Save/restore is an explicit host mutation boundary; the browser may request
  it but may not serialize, infer, or restore state locally.
- Durable filesystem persistence, cross-process recovery, browser refresh
  persistence, full campaign continuity, and human evaluation remain open.

## Host/core changes

1. Add `SAVE_SCHEMA_VERSION = "competitive-save-v1"`, typed save/load requests,
   and a `SaveEnvelope` with operation, identity, seed, transition count, and
   latest visible state hash.
2. Add an in-memory checkpoint map to `GameSessionStore`; clone the current
   session on save and replace it from the checkpoint on restore.
3. Expose `save_session` and `load_session` through MCP and loopback
   `POST /api/v1/sessions/{session_id}/save|load` routes.

## Browser changes

1. Add `saveSession` and `loadSession` adapter methods.
2. Add strict save-envelope validation and a small checkpoint client with
   explicit capability, schema, unknown-session, missing-checkpoint, and
   failure states.
3. Add accessible save/restore controls to the live session launch surface.
   Successful restore calls the existing host read path to refresh visible
   presentation, action catalog, history, replay, and regional world; failed
   restore preserves the current session/view.

## Tests and records

- Rust checkpoint clone/restore/hash continuity and MCP/transport assertions.
- Node/Python validation, controls, refresh/failure preservation, syntax, and
  authority-boundary tests in `tests/test_phase11_live_checkpoint.py`.
- Update roadmap, coverage ledger, SPEC, architecture, README, GUI adapter
  contract, lessons, QA, handoff, changelog, version projections, and credits.

## Explicit non-goals

- No durable save file, cross-process/session import, replay regeneration,
  browser serialization, client-side simulation, new hashes, new assets/audio,
  or full-campaign continuity claim.

## Verification gate

Run `cargo fmt`, `cargo test`, Python discovery, Clippy with warnings denied,
release/documentation/asset/security/generation checks, and the visual/audio
contract audit before one code-reviewer handoff. Merge the temporary branch to
`main`, delete it locally and remotely, then re-audit the next roadmap gap.
