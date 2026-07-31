# Implementation Plan: Debrief Visual Evidence-Intake Packet v0.13.91

## Target slice

Make the open `Debrief visuals reviewed` roadmap item operationally ready for
authorized human review by adding a strict, source-bound, empty evidence
intake packet for the three existing terminal debrief cases. The slice does
not perform or imply human visual, accessibility, educational, classroom, or
audio-listening review.

## Current repository understanding

- `docs/evaluation/phase13.2-debrief-visual-review-packet.json` already binds
  the competitive, stabilization, and regional-affiliation terminal cases,
  corrected raster/transcript evidence, review questions, fallbacks, and
  pending human-review fields.
- `docs/evaluation/phase13.2-debrief-visual-boundary.json` defines the
  host-owned, written-equivalent, read-only, causality, replay, and optional
  audio boundaries.
- `docs/evaluation/phase13.2-pilot-evidence-intake-packet.json` establishes
  the project pattern for an empty, privacy-bounded, source-derived evidence
  intake; this slice applies that pattern to debrief review cases.

## Authorized changes

- Add `docs/evaluation/phase13.2-debrief-visual-evidence-intake-packet.json`
  with the three canonical case IDs, bounded review dimensions, zero records,
  and pending human/release decisions.
- Add `scripts/validate_debrief_visual_evidence_intake.py` using only the
  standard library to enforce exact packet envelopes, canonical source parity,
  bounded records, and privacy/release exclusions.
- Add `tests/test_phase13_2_debrief_visual_evidence_intake.py` covering source
  parity, case/rating/finding vocabulary, empty/pending status, unknown-field
  rejection, source redirection, and numeric type rejection.
- Update the roadmap, SPEC, CHANGELOG, README/package version, lessons,
  request summary, presentation contract/QA, domain QA, and final handoff;
  regenerate deterministic credits/notices/runtime metadata after the version
  bump.

## Public and compatibility effects

No Rust, GUI runtime, simulation, persistence, asset, audio, browser-policy,
release-manifest, or public API behavior changes are expected. The new JSON
packet and validator define a repository-local human-review evidence contract;
the packet must remain empty and pending authorized review.

## Explicit non-goals and stop conditions

- Do not claim visual quality, accessibility, educational, classroom,
  audio-listening, legal/provenance, or public-release results.
- Do not add names, contact information, raw transcripts, unrestricted notes,
  private state, browser URLs, session IDs, or new screenshots/recordings.
- Do not change the existing terminal debrief renderer, rasters, transcript,
  host authority, release manifest, or review packet’s source cases.
- Stop and report if the existing three-case packet or review questions cannot
  be represented by a bounded vocabulary without inventing a new criterion.

## Verification and acceptance criteria

- The validator passes its empty, pending-human baseline.
- Focused tests prove exact case/source parity, bounded review values, privacy
  exclusions, unknown-field rejection, source redirection rejection, and
  numeric type safety.
- Existing debrief visual packet, pilot preparation, asset, release,
  documentation, full Python/Rust, formatting, and clippy checks remain green.
- Exactly one medium-effort code reviewer performs the final review; findings
  are resolved before the PR is merged and the temporary branch is deleted.

## Risk label

**Medium:** the packet governs human-review evidence and release boundaries,
but does not alter runtime behavior or collect external data.

## Execution instruction

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising. Report
files changed, tests run, deviations, and unresolved risks.
