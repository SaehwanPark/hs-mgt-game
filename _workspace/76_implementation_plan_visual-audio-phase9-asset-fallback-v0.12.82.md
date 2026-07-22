# Implementation Plan — Visual/audio Phase 9.2 graceful asset fallback v0.12.82

## Target slice

Complete the next bounded Phase 9.2 release-hardening item by making optional
visual asset availability explicit and recoverable at the presentation
boundary.

## Scope

- Add `gui/asset-availability.mjs` with pure, deterministic projections for
  caller-supplied load outcomes: loaded, missing, failed, and malformed.
- Preserve the visible requested identity/category label and written
  equivalent in every outcome; use a generic marker/fallback presentation when
  the release asset cannot be used and never expose a stale release path as
  loaded.
- Add `facilityPresentationFor` and `identityPresentationFor` adapters that
  consume the existing component/identity contracts without reading host
  state or deriving severity, intent, causality, or outcomes.
- Add an accessible `gui/asset-fallback-proof.html` fixture with loaded and
  fallback examples, plus focused Python/Node tests for status normalization,
  missing/failure recovery, text-equivalent preservation, and unknown IDs.
- Update CI, roadmap, specification, architecture, changelog, README, lessons,
  contributor guidance, and presentation QA.

## Non-goals

- No network fetches, dynamic imports, asset downloads, image/audio decoding,
  sanitization, re-encoding, deletion, or release-manifest changes.
- No portrait approval, model/seed inference, asset promotion, legal/ownership
  claim, or new external asset.
- No host command, session, simulation, stochastic, observation, history,
  replay, state-hash, debrief, or runtime authority changes.

## Acceptance checks

- Successful local availability preserves the requested asset identity and
  release path; missing, failed, malformed, and unknown outcomes render an
  explicit generic fallback with a written equivalent and no release path.
- The proof remains keyboard-visible and communicates fallback state without
  color or audio; it has no network, host, command, or hidden-state access.
- Focused Node/Python tests cover all normalized outcomes and authority
  boundaries; all existing asset/release/security checks remain green.
- Full Python/Rust/JavaScript, formatting, Clippy, documentation, and diff
  checks pass.

## Evidence limits

This slice proves only deterministic presentation recovery for caller-supplied
availability results. It does not prove browser decoder safety, human
accessibility, asset quality, legal clearance, ownership, or educational
benefit. Actual browser loading/decoder integration remains outside this
fixture-only contract.

## Review contract

Use exactly one read-only code reviewer for the PR handoff. Resolve every
actionable finding before merge, then delete the temporary branch locally and
remotely.

## Review disposition

The one designated code reviewer approved the final worktree with no actionable
findings after fixes for contradictory availability result handling and roadmap
evidence/deduplication. No runtime or host-authority issue was found.
