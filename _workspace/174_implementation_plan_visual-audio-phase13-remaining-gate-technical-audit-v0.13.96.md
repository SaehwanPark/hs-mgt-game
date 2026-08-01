# Implementation Plan — Remaining-gate technical audit v0.13.96

## Task restatement

Consolidate the existing source-bound technical evidence for every substantive
unchecked visual/audio roadmap gate into one fail-closed audit. Preserve the
distinction between technical preparation and authorized human evidence; do
not mark a human, legal, accessibility, educational, or expansion decision as
complete.

## Target slice

- Add `docs/evaluation/phase13-remaining-gate-technical-audit.json` with a
  source-bound inventory of the remaining roadmap gates, their technical
  evidence, human status, required authority, and blocking effect.
- Add a standard-library validator and focused tests that reject roadmap/source
  drift, missing evidence sources, unsupported status promotion, and accidental
  human or release approval.
- Synchronize the roadmap, `SPEC.md`, `CHANGELOG.md`, release metadata, and
  `_workspace` handoffs with v0.13.96 and the explicit human-evidence blocker.

## Acceptance criteria

- Every substantive unchecked roadmap item is represented by a stable gate ID,
  source marker, technical status, human status, and next authorized action.
- Existing technical evidence is reported only as source-bound preparation;
  human statuses remain `pending-authorized-human-evidence` or
  `pending-authorized-human-review`.
- The validator rejects missing source files/markers, unknown gates, boolean or
  numeric coercion, human/release status promotion, and changed roadmap markers.
- No runtime, simulation, browser authority, asset, audio, persistence, or
  release behavior changes.
- The audit explicitly states that the next meaningful actions require
  authorized human evidence or decisions, so no implementation gap is hidden.

## Non-goals

- Do not run or fabricate a participant, audio-listening, accessibility,
  provenance/legal, resemblance, clinical, debrief, or expansion review.
- Do not add participant records, raw notes/media, identity, browser/session
  locations, private game state, asset metadata, or release assets.
- Do not promote portraits, expand campaigns, or claim public-release readiness.

## Validation target

- `python3 -m unittest tests.test_phase13_remaining_gate_technical_audit`
- `python3 scripts/validate_remaining_gate_technical_audit.py`
- Full Python suite, serial Rust tests, formatting/clippy, asset/release,
  documentation, version, and diff checks.
- Exactly one medium-effort code reviewer before PR handoff.

## Handoff boundary

After merge and branch cleanup, re-audit the roadmap. If only the explicitly
listed human-evidence gates remain, stop and report the exact required inputs
instead of manufacturing closure.
