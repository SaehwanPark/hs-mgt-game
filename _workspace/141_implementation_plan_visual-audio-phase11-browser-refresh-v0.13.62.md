# Implementation Plan — Browser-refresh session continuity v0.13.62

## Task restatement

Recover a currently live GUI host session after a browser refresh by retaining
only the host-issued session ID in browser storage and reusing the existing
host-owned load path. Keep written presentation complete, clear stale IDs when
the host confirms the session is unavailable, and preserve all simulation,
history, replay, asset, audio, and authority boundaries.

## Current understanding

- `gui/app.mjs` owns the presentation-only session launcher and action client.
- `gui/host-adapter.mjs` keeps the host session ID in memory and the Rust host
  keeps sessions/checkpoints in memory for the current process.
- The page currently starts with the demo fixture unless the adapter already
  has an in-memory session ID; a browser refresh loses that adapter state.
- Existing `getSession`, `getPresentation`, and campaign-coverage reads are
  the correct host-owned recovery path.
- Existing `endSession` is the confirmed terminal boundary and should clear
  the stored ID after success.

## Assumptions and stop conditions

- Browser storage is an optional capability and may throw or be unavailable;
  the client must continue without it.
- A stored value is only an opaque non-empty session ID. No command, outcome,
  observation, hash, true state, or private information is stored.
- `createActionClient.load(sessionId)` remains the single recovery path for
  competitive and campaign-coverage sessions.
- An unknown-session response is the only automatic stale-ID cleanup signal;
  transient adapter failures must preserve the stored ID for retry.

Stop and report if recovery requires a new host route, a new DTO/schema,
browser serialization of simulation state, a cross-process store, or changes to
transition/history/replay authority.

## Minimal implementation plan

1. Inspect the existing launcher, action-client initialization/end path, host
   adapter, session-launch markup, and GUI tests; confirm no second session
   persistence implementation exists.
2. Add a small safe storage helper with read/write/clear operations and a stable
   key. Persist IDs only after successful host-backed load/start; prefill the
   existing-session input and invoke the existing action-client load on page
   initialization when a stored ID exists. Clear it after confirmed end or
   unknown-session recovery, while preserving it for other failures.
3. Add focused Node/Python coverage for storage exceptions, successful start/
   load persistence, refresh recovery, stale-ID cleanup, end cleanup, demo
   fallback, written status, and forbidden authority fields.
4. Update the GUI guide and README limitation wording, Phase 11.1 evidence
   ledger/test, roadmap/SPEC/changelog/lessons, version projections and device
   measurement, then record presentation QA and final handoff.
5. Run focused checks and the full repository validation. Perform exactly one
   medium-effort code review; fix relevant findings and rerun affected checks.

## Likely files

- `gui/app.mjs`: safe storage helper, launcher persistence, initial recovery,
  stale/end cleanup, and optional dependency injection.
- `gui/index.html`, `gui/README.md`, `docs/guides/gui-how-to-play.md`: visible
  recovery wording and same-host limitation.
- `tests/test_gui_session_launch.py`, `tests/test_gui_live_host.py`, and a
  focused `tests/test_phase11_browser_refresh_recovery.py`.
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json` and its test.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `CHANGELOG.md`,
  `LESSONS.md`, `README.md`, `Cargo.toml`, `Cargo.lock`,
  `tests/test_release_metadata.py`, and generated metadata as required by
  existing release checks.

## Public/API effects

No Rust API, route, schema, simulation state, persistence artifact, or replay
format changes. Browser storage adds one presentation-only opaque ID key and is
best-effort; older browsers and blocked storage retain the existing launcher and
demo behavior.

## Tests and acceptance criteria

- A successful host start or existing-session load stores the exact non-empty
  host session ID; failed loads do not overwrite it.
- A fresh page with a stored ID prefills the load control and calls the existing
  host load path; a valid response restores the presentation.
- A confirmed unknown session clears the stale ID and reports written recovery;
  other adapter failures leave it available for retry.
- A confirmed end clears the ID; storage exceptions never throw through UI
  actions or block the host session.
- No stored field or browser code references true state, resolved inputs,
  private rationale, transition authority, or replay regeneration.
- Focused tests, full Rust/Python checks, release/asset/documentation/device/
  browser/offline/visual-audio checks, and `git diff --check` pass at v0.13.62.

## Non-goals

- No durable file or cross-process persistence, browser-state serialization,
  service worker/cache, replay playback/regeneration, new route/schema, asset,
  audio change, simulation change, or human evaluation claim.

## Handoff requirements

Commit and push the coherent slice, perform one medium-effort code review,
prepare the PR handoff, merge into `main`, then delete this temporary branch
locally and remotely. Record the merge and remaining roadmap gates before
starting the next plan.

## Risk label

Risk: medium

Reason: the slice changes browser startup and recovery behavior across the
shared session launcher while depending on optional storage and preserving a
host process boundary, but it does not change simulation or public host APIs.

## Execution record

- Added shared best-effort session-ID storage to the action and read-only
  clients, including confirmed terminal cleanup in both paths after review.
- Focused tests and full repository checks passed; the emulated device source
  measurement was refreshed to 383,148 bytes after the final GUI change.
- The sole medium-effort code review found one Medium read-only terminal-cleanup
  issue. It was fixed by sharing the session store with the read-only launcher
  and clearing it after a confirmed end; focused read-only source coverage was
  added and affected checks were rerun.
- No plan deviation or new dependency was introduced.
