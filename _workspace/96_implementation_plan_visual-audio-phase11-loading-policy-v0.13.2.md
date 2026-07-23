# Implementation Plan — Visual/audio Phase 11.2 loading-policy audit v0.13.2

## Task restatement

Add a deterministic, dependency-free audit of the live GUI loading surface.
Record that the current inline/generated board and runtime-generated audio need
neither lazy-loading nor preload directives, and fail closed if future
file-backed assets appear without explicit loading-policy metadata.

## Current understanding

- The live entrypoint is `gui/index.html` with local module scripts and no
  file-backed image/audio/video tags or preload links.
- `gui/scene.mjs` serializes the visible regional board as inline SVG; audio is
  generated from local Web Audio recipes after user gesture.
- Phase 11.2 has audio packaging evidence but leaves lazy loading and preload
  policy unchecked.
- The target is static governance evidence, not a browser-loader rewrite.

## Assumptions

- The files named in the policy are the current live GUI entrypoint/modules.
- A known marker scan is sufficient for this bounded static contract; it is not
  a substitute for browser timing or device measurement.
- Future file-backed assets must be declared before they are connected to the
  live entrypoint.

If any assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1. Add `assets/loading-policy.json` with the current no-lazy/no-preload
   decisions, live files, forbidden file-backed markers, and future policy
   metadata requirements.
2. Add `scripts/check_loading_policy.py` to validate repository-relative files,
   scan the live source set for preload/media/loading markers, verify the
   current decisions, and emit `loading-policy-report-v1`.
3. Add focused tests for the current green report/CLI, preload and media
   marker rejection, unlisted source/policy metadata, path escapes, and
   malformed definitions.
4. Update roadmap, `README.md`, `SPEC.md`, `ARCHITECTURE.md`, `LESSONS.md`,
   `CHANGELOG.md`, version projections, request/contract/QA, and handoff to
   v0.13.2. Correct the prior handoff status to record PR #250 as merged.
5. Run focused and full checks; stop if implementation reaches browser loading,
   asset promotion, host authority, or runtime performance claims.

## Files and functions likely to change

- `assets/loading-policy.json`: current loading decisions and live scope.
- `scripts/check_loading_policy.py`: path/marker/policy validation and report.
- `tests/test_loading_policy.py`: focused green and fail-closed cases.
- `_workspace` request/contract/QA/plan/handoff records.
- Roadmap, canonical docs, lessons, changelog, asset guidance, and version
  projections.

## Tests and checks

- `python3 -m unittest tests.test_loading_policy`
- `python3 -m unittest discover -s tests`
- `cargo fmt --check`
- `cargo test`
- `cargo clippy --all-targets --all-features -- -D warnings`
- documentation, release metadata, asset, security, and visual/audio audits.

Expected result: the report passes with no current preload/media markers and
all declared live policy files present.

## Acceptance criteria

- Current report is deterministic and records no lazy-loading/preload need for
  the inline/generated live surface.
- A preload tag, media file reference, or unlisted live source fails closed.
- Future policy metadata names fallback, equivalent, trigger, budget, and
  provenance requirements without promoting an asset.
- No browser runtime, simulation, host DTO, history/hash/replay, debrief, or
  audio behavior changes.
- Only the Phase 11.2 lazy-loading and preload checklist items are closed;
  runtime/offline/device/compatibility and human gates remain open.

## Non-goals

- Do not add lazy loading, preload directives, media files, or dependencies.
- Do not claim browser, cache, decode, memory, offline, device, compatibility,
  screenshot, asset-quality, or human evidence.
- Do not perform unrelated refactoring or formatting.

## Stop conditions

Stop and report if a live file-backed asset reference already exists, the live
file set is broader than the bounded list, policy requires changing browser
behavior, or more than the planned governance/docs/test files need production
edits.

## Review checklist

- Static marker and path checks are fail-closed and scoped to live files.
- Tests cover current green and representative future-risk cases.
- Inline/generated and actor-visible boundaries remain explicit.
- No loading decision is presented as runtime performance evidence.
- Version, roadmap, canonical docs, QA, and handoff agree.

## Risk label

Risk: low

Reason: This is a read-only static audit over a local module graph with no
browser, simulation, asset, or public API behavior change.
