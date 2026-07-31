# Implementation Plan — Correct full-campaign terminal raster state evidence v0.13.82

## Task restatement

Correct the v0.13.81 evaluation evidence so the three terminal JPEGs are
captured after the final host transition, with `session.done`, terminal
history/debrief, and disabled mutation controls visibly aligned.

## Current finding

Visual inspection of the committed v0.13.81 terminal frames shows the
competitive frame at turn 24 with the normal action rail, and the stabilization
and regional-affiliation frames at their last decision stage with placeholder
debrief text. The captures are therefore pre-terminal observations despite
their terminal filenames and manifest labels.

## Target slice

1. Re-run the existing loopback GUI at the fixed 1024×768 evaluation canvas.
2. Submit the final host-shaped decision for competitive (24/24),
   stabilization (5/5), and regional affiliation (6/6), then capture the
   actual terminal envelope for each campaign.
3. Replace only the three terminal JPEGs and their raw capture metadata; keep
   active evidence unchanged unless the route requires a new session.
4. Extend the manifest and fail-closed validator with terminal `done`, exact
   history count, non-empty debrief, and no-further-decision assertions.
5. Update the ledger, roadmap, SPEC, changelog, lessons, version, and
   operational handoffs to record the correction and preserve the human-review
   boundary.

## Non-goals

- No new route, schema, simulation rule, stochastic input, browser authority,
  asset, audio file, release asset, or production screenshot runner.
- No claim of pixel-level quality, human accessibility/educational usefulness,
  cross-browser/device certification, provenance/legal approval, or public
  release.

## Acceptance criteria

- Each terminal record is captured after the final host transition and records
  `session_done: true`, the campaign endpoint turn, matching history count,
  non-empty host debrief, and disabled/no further decision behavior.
- Each replacement JPEG matches its manifest byte size, SHA-256, MIME type, and
  exact 1024×768 dimensions; native raw capture metadata remains bound to the
  normalized artifact.
- The validator rejects a pre-terminal terminal record, count drift, empty
  debrief, enabled terminal decision, missing artifact, or metadata drift.
- Existing active records, host authority, written fallbacks, and release
  exclusion remain intact.

## Verification and handoff

- Use the in-app browser only for the local capture, then close its session.
- Run focused/full Python tests, Rust formatting/Clippy/tests, repository
  contract audits, and `git diff --check`.
- Complete exactly one medium-effort code review, then commit, push, open,
  merge, and clean the temporary branch locally and remotely.

## Evidence limits

This closes a technical terminal-state capture correction only. It does not
replace the separately required human visual, accessibility, educational,
audio-listening, cross-browser/device, provenance/legal, or public-release
reviews.
