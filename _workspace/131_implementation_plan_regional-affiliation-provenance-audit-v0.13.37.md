# Implementation Plan — Phase 12 regional-affiliation provenance audit v0.13.37

## Task restatement

Complete the Phase 12.2 provenance-audit item with a bounded current
regional-affiliation asset/provenance record. Join reusable catalog sources,
registry validation, generated credits, release manifests, audio packaging,
portrait-preview gates, and the no-new-asset decision without claiming legal
clearance or human quality approval.

## Current understanding

- Regional affiliation currently reuses repository-authored/project-generated
  identity, marker, status, facility-fallback, and optional runtime-generated
  audio contracts.
- The current campaign asset-need decision requires no new asset under the
  abstract/stage contract; future geography, placement, stage art, recorded
  audio, licensed assets, or portrait promotion reopen provenance work.
- Machine checks already cover registry schema/hashes/provenance fields,
  security, release manifests, generated metadata, runtime credits, catalog
  reuse, and audio packaging; portrait previews remain unreleased.

## Target slice

Add `docs/evaluation/phase12-regional-affiliation-provenance-audit.json` and a
parity test that record:

- current regional-affiliation reusable visual/audio/fallback source contracts;
- machine audit commands, source markers, pass status, and coverage;
- third-party release count, no-new-asset decision, generated credits,
  file-backed audio boundary, and unreleased portrait-preview gate; and
- legal, training-data, human quality, educational, and public-release limits.

## Assumptions

- A green machine audit establishes technical provenance evidence only, not
  legal clearance, model/training-data provenance, output quality, or approval.
- Existing catalog eligibility does not prove direct affiliation campaign
  mapping, partner-specific identity treatment, stage art, or audio quality.
- Unverified portrait previews remain outside the release surface until the
  documented human/provenance/release gates are satisfied.

## Minimal implementation plan

1. Add the regional-affiliation provenance ledger and source-parity test.
2. Check the final Phase 12.2 provenance item and synchronize canonical docs,
   lessons, version metadata, generated credits, and additive request/contract/
   QA/handoff records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the remaining roadmap items.

## Non-goals

- Do not add assets, portrait releases, recorded audio, routes, runtime fields,
  persistence, screenshots, instructor views, authority paths, legal claims,
  human review claims, or public-release approval.
- Do not treat registry/catalog presence as direct campaign use or audio/visual
  quality evidence.

## Stop conditions

Stop if the current regional-affiliation provenance boundary cannot be tied to
machine checks, catalogs, credits, release/security gates, portrait status,
and future reopen triggers without promoting an asset or making a human/legal
claim.

## Risk label

Risk: low

Reason: The slice records existing technical provenance checks and keeps
unverified/future asset decisions outside the current release boundary.
