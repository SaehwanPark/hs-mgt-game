# Implementation Plan — Phase 8.2 current portrait-preview inventory integrity v0.13.18

## Task restatement

Continue the visual/audio roadmap with the smallest supported Phase 8.2
portrait slice: record the current seven preserved portrait previews and prove
their role/path/hash/review-queue alignment. Keep the candidates unverified,
unreleased, and outside the runtime asset registry until the required human and
provenance gates are actually completed.

## Current understanding

- `assets/generation/portrait-set.json` defines exactly seven canonical role
  IDs, shared editorial style constraints, accessible-equivalent guidance,
  generic fallbacks, and prohibited-content boundaries.
- `assets/generation/portrait-previews.json` preserves one source PNG for each
  role with repository-relative paths, source hashes, prompts, settings,
  dimensions, written equivalents, and generic fallbacks.
- `assets/generation/portrait-review-queue.json` binds the same seven entries
  to pending human gates. `assets/generation/generation-manifest.json` remains
  empty, and the preview entries have no approved local model revision, seed,
  release path, or registry ID.
- `tests/test_portrait_workflow.py` already validates most of this boundary but
  does not expose a single ledger for the current inventory.

## Target slice

Add `docs/evaluation/portrait-preview-coverage.json` with a
`fictional-portrait-preview-coverage-v1` contract that records:

- exact seven role and preview counts and ordered IDs;
- source, preview, review-queue, and generation-manifest document paths;
- source PNG hash/dimension and one-to-one role/path binding evidence;
- the seven pending review-queue entries and zero release-manifest entries;
- the empty registry/release boundary; and
- explicit limits for human review, model/seed provenance, quality,
  accessibility, legal clearance, release derivatives, and runtime use.

## Assumptions

- “Coverage” means every current preserved candidate is inventory-complete and
  hash/path bound; it does not mean any portrait is approved, high quality,
  accessible in lived use, legally cleared, deterministic to regenerate, or
  ready for release/runtime use.
- Existing generation validators and portrait workflow tests remain
  authoritative for detailed field validation and fail-closed promotion.
- No image bytes, model metadata, release derivative, registry entry, GUI
  consumer, or human-review decision is needed for this evidence slice.

If the existing documents do not support an exact ledger field, record the
unknown or pending state instead of inferring it.

## Minimal implementation plan

1. Add the portrait-preview coverage ledger with exact current source paths,
   counts, IDs, hash/dimension boundary, review queue, and release limits.
2. Extend `tests/test_portrait_workflow.py` to require ledger/source parity and
   preserve the existing hash, pending-review, and release-block assertions.
3. Update the Phase 8.2 roadmap status/checklist and add v0.13.18 evidence;
   synchronize `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `LESSONS.md`,
   `README.md`, `docs/roadmap.md`, version metadata, generated credits, and
   additive request/contract/QA/handoff records.
4. Run full Python/Rust/lint/release/documentation/asset/generation/offline/
   browser/device/visual-audio checks.
5. Review with one reviewer in three independent passes, open a PR, merge into
   `main`, remove the temporary branch locally/remotely, and reassess the next
   roadmap gap.

## Files and functions likely to change

- `docs/evaluation/portrait-preview-coverage.json`.
- `tests/test_portrait_workflow.py`.
- `assets/generation/portrait-set.json`,
  `assets/generation/portrait-previews.json`,
  `assets/generation/portrait-review-queue.json`, and
  `assets/generation/generation-manifest.json` are read-only sources for this
  slice and should not change.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`, `_workspace/03_presentation_qa.md`,
  this plan, and `_workspace/final/handoff.md`.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `ARCHITECTURE.md`,
  `CHANGELOG.md`, `LESSONS.md`, `README.md`, `docs/roadmap.md`, `Cargo.toml`,
  `Cargo.lock`, and generated package-version projections.

## Acceptance criteria

- The ledger records exactly seven current portrait roles/previews and seven
  pending review-queue entries, with one-to-one role/path/hash evidence and an
  empty generation manifest.
- The focused test proves ledger paths and counts match the source documents
  and retains existing fail-closed release/pending-review behavior.
- The roadmap records current preview inventory integrity only; human review,
  model/seed provenance, legal/quality/accessibility review, release
  derivatives, registry bridge, and runtime use remain open.
- Package version increments to v0.13.18 and metadata is consistent.

## Non-goals

- Do not generate or modify portraits, add model/seed claims, approve review
  gates, create release derivatives, add registry entries, wire portraits into
  the GUI, or claim human quality/legal/accessibility approval.

## Stop conditions

Stop if evidence requires a human decision, approved model identity/seed,
additional image generation, release promotion, or a runtime consumer.

## Risk label

Risk: low

Reason: The slice adds a read-only integrity ledger over existing preserved
preview documents and tests without changing image bytes, generation metadata,
runtime behavior, or release eligibility.
