# Implementation Plan — Phase 8.2 current portrait metadata gates v0.13.19

## Task restatement

Continue Phase 8.2 with the three current portrait checklist gates already
supported by repository evidence: every canonical role is defined, every
preserved preview source exists and is hash-bound, and every preview has a
written accessible equivalent. Close only those technical metadata gates.

## Current understanding

- `portrait-set.json` defines seven role IDs, labels, families,
  `alt_text_guidance`, and generic fallbacks.
- `portrait-previews.json` binds seven role IDs to preserved repository-local
  PNGs with SHA-256 hashes, and every entry carries an
  `accessible_equivalent` field.
- `portrait-preview-coverage.json` records the current inventory and existing
  workflow tests, but it does not expose these three checklist gates as
  explicit parity fields.
- Prompt/seed provenance is incomplete because the preview tool did not expose
  an approved local model revision or actual seed; no release derivative,
  registry entry, runtime consumer, human review, or quality approval exists.

## Target slice

Extend the portrait-preview coverage ledger and focused test with:

- `role_definition` closure for all seven canonical role IDs/labels/families;
- `source_preservation` closure for all seven repository-relative preview
  paths, dimensions, and recorded source hashes; and
- `accessible_equivalent` closure for all seven preview entries and role
  guidance/fallbacks.

Update the Phase 8.2 checklist to check only “Role defined,” “Source image
preserved,” and “Alt text written,” with evidence and explicit limits.

## Assumptions

- These three gates are technical metadata/path/text closures, not a claim
  that a human recognizes a portrait, approves identity consistency, or finds
  the image accessible in lived use.
- Existing `test_portrait_workflow.py` hash and fail-closed tests remain
  authoritative; add only parity assertions needed to expose the three
  roadmap states.
- `accessible_equivalent` is the repository's written text-equivalent field;
  it does not replace human accessibility evaluation.

## Minimal implementation plan

1. Add explicit technical-gate statuses and evidence to
   `docs/evaluation/portrait-preview-coverage.json`.
2. Extend `tests/test_portrait_workflow.py` to require role label/family,
   preserved source/hash, accessible-equivalent, and fallback parity.
3. Update the Phase 8.2 checklist/status and v0.13.19 evidence; synchronize
   canonical docs, lessons, version metadata, generated credits, and additive
   request/contract/QA/handoff records.
4. Run full Python/Rust/lint/release/documentation/generation/asset/offline/
   browser/device/visual-audio checks.
5. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next roadmap gap.

## Non-goals

- Do not alter portrait bytes or generation records, add model/seed claims,
  complete crops/derivatives, perform human review, approve registry/release,
  wire portraits into the GUI, or claim lived accessibility or quality.

## Stop conditions

Stop if evidence requires a human judgment, approved model identity/seed,
release derivative, registry promotion, runtime consumer, or external review.

## Risk label

Risk: low

Reason: The slice makes existing role/text/path/hash evidence explicit without
changing assets, generation state, release eligibility, or runtime behavior.
