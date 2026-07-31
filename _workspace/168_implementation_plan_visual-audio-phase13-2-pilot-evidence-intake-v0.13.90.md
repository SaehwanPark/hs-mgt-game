# Implementation Plan: Pilot Evidence-Intake Packet v0.13.90

## Target slice

Make the open `Run structured first-time-user evaluation` roadmap item
operationally ready for an authorized human pilot by adding a source-bound,
machine-checkable evidence-intake packet. The slice records an empty intake
state only; it does not perform evaluation or infer human comprehension.

## Current repository understanding

- `docs/evaluation/phase13.1-first-session-review-packet.json` already binds
  the first-session tasks, technical observations, accommodations, recovery
  paths, and pending human decision fields.
- `docs/evaluation/phase13.2-pilot-feedback-instrument.json` already defines
  the authorized pilot tasks, bounded ratings, consent status, finding
  categories, and pending go/no-go decision.
- The remaining gap is a safe, checked-in intake boundary that makes accepted
  record fields and forbidden participant/media/hidden-state fields explicit
  without adding participant data.

## Authorized changes

- Add `docs/evaluation/phase13.2-pilot-evidence-intake-packet.json` with an
  empty records array, allowed response vocabulary, privacy boundary, and
  pending human decision.
- Add `scripts/validate_pilot_evidence_intake.py`, using only the Python
  standard library, to validate the packet and reject unsafe or malformed
  record shapes when exercised by tests.
- Add `tests/test_phase13_2_pilot_evidence_intake.py` covering source parity,
  empty/pending status, allowed record structure, and rejection of identity,
  raw media, URLs/session IDs, hidden-state, and unbounded free-text fields.
- Update the roadmap, SPEC, CHANGELOG, README/package version, lessons,
  request summary, presentation contract/QA, domain QA, and final handoff;
  regenerate deterministic credits/notices/runtime metadata after the version
  bump.

## Public and compatibility effects

No Rust, GUI runtime, simulation, persistence, asset, audio, browser-policy,
release-manifest, or public API behavior changes are expected. The new JSON
packet and validator define a repository-local evaluation evidence contract;
the packet must remain `pending-human-evidence` and contain no participant
results.

## Explicit non-goals and stop conditions

- Do not run or claim a first-time-user study.
- Do not add names, contact information, health information, raw transcripts,
  screenshots, recordings, browser URLs, session IDs, or hidden game state.
- Do not mark accessibility, educational usability, audio usefulness,
  debrief comprehension, expansion approval, or public release complete.
- Stop and report if existing pilot fields conflict with the proposed bounded
  vocabulary or if source records require storing unrestricted text.

## Verification and acceptance criteria

- The packet validator passes its empty, pending-human baseline.
- Focused tests prove source markers, task/rating/consent parity, and unsafe
  field rejection.
- Existing pilot-preparation, first-session, privacy, asset, release, and
  documentation checks remain green.
- Full Python/Rust validation, formatting, clippy, and `git diff --check`
  pass before handoff.
- Exactly one medium-effort code reviewer performs the final review; findings
  are resolved before the PR is merged and the temporary branch is deleted.

## Risk label

**Medium:** the packet handles evaluation and privacy boundaries, but it does
not alter runtime behavior or collect external data.

## Execution instruction

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising. Report
files changed, tests run, deviations, and unresolved risks.
