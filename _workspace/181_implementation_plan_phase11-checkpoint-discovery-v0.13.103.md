# Implementation plan — v0.13.103 checkpoint discovery

## Task restatement

Implement a host-owned durable checkpoint discovery read and an accessible GUI
picker while preserving the existing opaque-ID manual load/restore flow,
host-only persistence, and actor-visible data boundary.

## Current understanding

- `src/mcp/persistence.rs` owns the `.checkpoints` archive and legacy fallback,
  but currently exposes only per-session read/write/remove operations.
- `src/mcp/session.rs` owns typed MCP/session envelopes and can map validated
  persistence records to discovery metadata.
- `src/gui_server.rs` owns loopback routes and can add one read-only route.
- `gui/host-adapter.mjs` and `gui/app.mjs` already own fetch and session-launch
  behavior; `gui/index.html` owns the start/load form.
- The open roadmap item is checkpoint discovery, not browser serialization or
  replay redesign.

## Assumptions

- The configured persistence path is available to the host when discovery is
  requested; a host without persistence returns a structured recoverable error.
- Only validated wrapper files are discoverable. Invalid or unsupported files
  are skipped and counted without returning their contents or paths.
- Archive entries are ordered by opaque session ID for deterministic output;
  the valid legacy fallback is included only when its session ID is not already
  represented by an archive entry.
- Metadata is limited to `session_id`, `campaign`, `seed`,
  `transition_count`, and `storage` (`archive` or `legacy`).

If any assumption is false, stop and report the mismatch before broadening the
implementation.

## Minimal implementation plan

1. Inspect the existing wrapper schemas and load validators in
   `src/mcp/persistence.rs`; add a deterministic discovery helper that scans
   the sibling archive and legacy file, validates each candidate through the
   existing host validators, skips invalid candidates, and returns metadata plus
   an invalid-entry count.
2. Add `CheckpointDiscoveryEnvelope` and `CheckpointDescriptor` to
   `src/mcp/session.rs` with schema version `gui-checkpoint-discovery-v1`, and
   add a read-only `GameSessionStore` method that maps validated persistence
   records without mutating live sessions.
3. Add `GET /api/v1/checkpoints` in `src/gui_server.rs` and
   `listCheckpoints()` in `gui/host-adapter.mjs`. Preserve the loopback host,
   status/error conventions, and no-client-authority boundary.
4. Add an accessible “Find saved checkpoints” control and metadata list to
   `gui/index.html`/`gui/app.mjs`. Validate the envelope before rendering,
   render an empty/error state, and make an entry’s action fill the existing
   opaque session-ID field without submitting a load request. Keep the manual
   input and existing restore controls unchanged.
5. Add Rust persistence/session/transport tests for valid archive entries,
   valid legacy fallback, invalid-file skipping, deterministic ordering,
   duplicate archive-over-legacy behavior, and no mutation. Add Node/Python
   contract tests for envelope validation, picker behavior, route/adapter
   wiring, written fallback, and browser-storage privacy.
6. Bump the package from `0.13.102` to `0.13.103`, update `CHANGELOG.md`,
   `README.md`, `SPEC.md`, `LESSONS.md`, GUI guidance, the Phase 11.1 ledger,
   the roadmap, and the consolidated technical audit. Regenerate only the
   repository’s version-bound asset credit projections when required by their
   existing generator.
7. Run focused tests, then the full Rust/Python suites and existing release,
   browser/offline/loading/device/asset/audio/documentation/audit checks.
   Report files changed, tests run, deviations, and unresolved risks.

## Files and functions likely to change

- `src/mcp/persistence.rs`: deterministic validated archive/legacy discovery
  records and focused persistence tests.
- `src/mcp/session.rs`: discovery envelope, store read method, and session
  contract tests.
- `src/gui_server.rs`: loopback discovery route and transport tests.
- `gui/host-adapter.mjs`: typed discovery request.
- `gui/app.mjs`: discovery-envelope validation, rendering, and picker behavior.
- `gui/index.html`: accessible discovery control and list/status region.
- `tests/test_phase11_browser_refresh_recovery.py`: browser storage/privacy,
  picker, route, adapter, and documentation contract assertions.
- `docs/guides/gui-how-to-play.md`, `gui/README.md`,
  `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `LESSONS.md`,
  `CHANGELOG.md`, `README.md`, and evaluation packets: synchronized scope and
  limits.
- `Cargo.toml`, `Cargo.lock`, release metadata tests, generated asset credits,
  and technical-audit validator expectations: v0.13.103 synchronization.

Avoid editing files outside this list unless the plan is incomplete; if that
happens, stop and explain why.

## Public contract and compatibility effects

- Adds one loopback-only read route and the `gui-checkpoint-discovery-v1`
  envelope; existing session routes and save/load envelopes remain unchanged.
- Adds no browser persistence artifact and no simulation or replay schema
  change.
- Legacy single-file checkpoints remain readable and discoverable when valid;
  archive entries take precedence for duplicate session IDs.

## Tests and checks

- `cargo test mcp::persistence::tests::`
- `cargo test mcp::session::tests::...checkpoint...`
- focused GUI transport and Node/Python browser contract tests
- `cargo fmt`
- `cargo test`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- existing audit, release, asset/audio, browser, offline/loading/device,
  documentation-link, and CLI checks

Expected result: all focused and full checks pass; discovery returns only
validated metadata, preserves legacy compatibility, and introduces no browser
save artifact.

## Acceptance criteria

- `GET /api/v1/checkpoints` returns a typed discovery envelope with stable
  ordering and only validated metadata for all three campaign families.
- A malformed/unsupported/mismatched checkpoint is omitted and counted while
  valid archive entries remain available; a valid legacy entry is included only
  when not shadowed by an archive entry.
- The GUI’s discovery control renders campaign, opaque ID, storage source, and
  transition count with a written empty/error fallback.
- Choosing a discovered entry fills the existing session-ID input and leaves
  loading to the user; manual ID entry and restore behavior remain unchanged.
- Browser storage and client code contain no checkpoint save artifact, true
  state, resolved input, or new transition authority.
- Version, docs, ledger, audit, generated projections, and lessons identify
  v0.13.103 and preserve all remaining human/runtime/release limits.

## Non-goals

- Do not add browser serialization, automatic load, replay regeneration,
  autosave policy changes, simulation rules, new dependencies, or broad API
  refactors.
- Do not expose raw checkpoint paths, save wrappers, private state, or
  unresolved errors to the browser.
- Do not claim human usability, accessibility, audio quality, browser/device
  certification, educational effectiveness, or release readiness.

## Stop conditions

Stop and request review if the route needs a public network bind, save contents,
new browser authority, a migration of existing files, more than one new route,
or a broader persistence/replay redesign.

## Handoff requirement

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising. Report files
changed, tests run, deviations, and unresolved risks. Use exactly one
medium-effort code reviewer during PR handoff.

## Risk label

Risk: medium

Reason: This adds a public loopback read contract over persistence metadata and
must preserve malformed-file handling, legacy compatibility, and the browser
authority/privacy boundary.
