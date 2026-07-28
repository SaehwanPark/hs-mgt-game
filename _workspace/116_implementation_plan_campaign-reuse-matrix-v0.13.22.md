# Implementation Plan — Phase 12 campaign presentation reuse matrix v0.13.22

## Task restatement

Continue Phase 12 with the next bounded item: document which existing visual,
audio, facility, and fallback primitives can be reused by the stabilization and
regional-affiliation campaign surfaces. Do not claim that campaign-specific
art, audio mapping, or quality review is complete.

## Current understanding

- `gui/visual-catalog.json` provides approved project-generated identity,
  marker, and status tokens with written equivalents.
- `gui/audio-catalog.json` provides approved runtime-generated music, UI cue,
  event cue, and ambience entries without file-backed release assets.
- `gui/facility-components.mjs` provides reusable facility descriptors and a
  generic fallback, while the current Phase 12 campaign contract requires no
  new map/facility asset.
- Phase 12 now has a current campaign presentation inventory, but the roadmap
  does not yet record the exact reuse decision per campaign and surface family.

## Target slice

Add `docs/evaluation/phase12-campaign-reuse-matrix.json` and parity tests that
record:

- shared identity, semantic-marker, status, UI-cue, facility-fallback, and
  written-equivalent reuse decisions;
- stabilization reuse of existing visible executive/status/pressure,
  regulatory, debrief, and ambience primitives;
- regional-affiliation reuse of existing stage/partner/status, affiliation,
  debrief, and boardroom/city ambience primitives;
- catalog source paths, exact IDs, approval/provenance source, and explicit
  `current-contract-eligible` versus `fallback-only` decisions; and
- campaign-specific work that remains open, including new pressure taxonomy,
  stage-specific treatment, audio quality, and human review.

## Assumptions

- A reuse decision documents an existing eligible primitive; it does not claim
  that every listed cue or ambience is already mapped into the campaign
  coverage envelope.
- The browser remains non-authoritative and uses written equivalents when
  optional audio or visual tokens are unavailable.
- No new asset, registry entry, runtime field, or campaign transition is
  required for this evidence slice.

## Minimal implementation plan

1. Add the reuse matrix with exact catalog IDs and campaign boundaries.
2. Add a focused parity test for catalog IDs, source markers, approval status,
   written equivalents, and the no-new-asset boundary.
3. Check only the Phase 12.1/12.2 reusable-assets roadmap items and synchronize
   canonical docs, lessons, version metadata, generated credits, and additive
   request/contract/QA/handoff records.
4. Run full Python/Rust/lint/release/documentation/generation/asset/offline/
   browser/device/visual-audio checks.
5. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the remaining campaign gates.

## Non-goals

- Do not create or promote map, facility, portrait, stage-art, or audio-file
  assets.
- Do not add audio-state mapping, tutorial copy, pressure mechanics, stage
  animation, instructor views, screenshots, persistence, or human evaluation.
- Do not treat reuse eligibility as campaign completion or quality approval.

## Stop conditions

Stop if evidence requires new campaign content, a visual/audio quality
decision, a new authority path, asset promotion, or human review.

## Risk label

Risk: low

Reason: The slice records existing catalog and fallback decisions in a
machine-checked ledger without changing runtime behavior or asset bytes.
