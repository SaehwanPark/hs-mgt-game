# Implementation plan — v0.13.104 browser-safe checkpoint reference transfer

## Task restatement

Implement deterministic browser export/import for a validated checkpoint
reference, not a save artifact. Preserve host authority, opaque-ID-only
browser persistence, the existing manual load/restore flow, and explicit
written fallbacks.

## Target contract

Add the browser-only schema `gui-checkpoint-reference-v1` with exactly these
fields:

- `schema_version`
- `session_id`
- `campaign`
- `seed`
- `transition_count`
- `storage` (`archive` or `legacy`)

Export serializes fields in this stable order. Import rejects malformed JSON,
unsupported schemas, unsafe IDs, unsupported campaigns, invalid seeds or
transition counts, invalid storage values, and extra keys. A valid import only
fills the existing session-ID control and reports that the host must still
validate the current checkpoint.

## Minimal implementation plan

1. Add pure browser validation, stable serialization, parsing, and safe
   download helpers in `gui/app.mjs`, reusing the existing discovery field
   contract and rejecting extra keys or save-shaped fields.
2. Add an export action beside each discovered checkpoint and an import file
   control in the existing saved-checkpoint panel. Keep the action explicit,
   keyboard reachable, written, recoverable, and free of automatic loading or
   browser-storage writes.
3. Add Node/Python contract tests for deterministic round trips, malformed and
   extra-field rejection, no-load/no-storage behavior, UI wiring, written
   empty/error states, and a valid reference’s exact fields. Add no Rust route
   or persistence code unless an existing contract unexpectedly requires it.
4. Update GUI guide/README, `SPEC.md`, `README.md`, `CHANGELOG.md`, `LESSONS.md`,
   the v0.13.104 roadmap entry, Phase 11.1 ledger, and the remaining-gate
   boundary so the new browser reference boundary and remaining host-only
   artifact limit are explicit. Bump the package patch version to `0.13.104`
   and refresh only existing version-bound generated projections.
5. Run focused browser tests, full Rust/Python suites, clippy, formatting,
   documentation/release/asset/audio/offline/loading/security/audit checks,
   then perform the one-reviewer PR handoff.

## Files likely to change

- `gui/app.mjs`, `gui/index.html`
- `tests/test_phase11_browser_refresh_recovery.py`
- `docs/guides/gui-how-to-play.md`, `gui/README.md`, `SPEC.md`, `README.md`,
  `CHANGELOG.md`, `LESSONS.md`
- `docs/visual_audio_enhancement_roadmap.md`
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`
- `Cargo.toml`, `Cargo.lock`, release metadata and generated projections as
  required by the repository’s existing version checks
- `_workspace/00_input/request-summary-v0.13.104.md` and this plan

## Acceptance criteria

- `gui-checkpoint-reference-v1` validates only the six metadata fields and
  rejects extra keys or save-shaped content.
- Export produces deterministic reference JSON; no browser save artifact,
  true state, history, resolved inputs, or new hash is present.
- Import accepts a valid reference, fills the existing opaque ID, leaves the
  current view and browser storage unchanged, and does not call load/restore.
- Invalid JSON/schema/fields and unavailable file APIs produce written,
  recoverable status without mutating the current session.
- Existing checkpoint discovery, manual loading, host restore, autosave,
  refresh recovery, and all three campaign paths remain unchanged.
- Documentation and evidence state that host validation remains authoritative
  and actual browser save-artifact serialization is still out of scope.

## Non-goals and risks

This does not implement actual browser save-artifact serialization, automatic
resume, replay regeneration, screenshots, device certification, human review,
or release approval. Risk is low-to-medium: the main concern is accidentally
letting a convenience reference become a client authority or a container for
private host state.

## Handoff requirement

Use exactly one medium-effort code reviewer, address actionable findings, merge
the PR into `main`, delete the temporary branch locally and remotely, verify a
clean `main`, and re-audit the roadmap.
