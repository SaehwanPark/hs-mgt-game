# Implementation Plan — Phase 12 stabilization provenance audit v0.13.29

## Task restatement

Complete the current stabilization campaign's provenance audit by joining the
existing visual/audio catalogs, asset registries, generated credits/notices,
release checks, and no-new-asset decision. Keep unreleased portrait previews,
future campaign content, legal clearance, and human review explicitly open.

## Current understanding

- The reusable-asset matrix and map/facility decision already identify the
  current stabilization reuse boundary and no-new-asset requirement.
- `gui/visual-catalog.json` and `gui/audio-catalog.json` use repository-authored
  or project-generated presentation records with written equivalents and
  provenance/approval fields.
- `scripts/validate_assets.py`, `scripts/verify_asset_release.py`, generated
  credits/notices, and registry tests provide current technical provenance
  checks; portrait previews remain intentionally unverified and unreleased.

## Target slice

Add `docs/evaluation/phase12-stabilization-provenance-audit.json` and a parity
test that records:

- current campaign-reusable visual/audio/facility provenance sources;
- passing registry, release-manifest, credits/notices, and generation-boundary
  checks;
- the no-new-map/facility/audio/visual decision and unreleased-preview boundary;
  and
- open work for future campaign assets, legal review, portrait provenance,
  human quality, and public release.

## Assumptions

- This is a current technical provenance audit, not legal clearance or a human
  quality approval.
- Generated audio has no shipped file path; its source/provenance is the local
  runtime recipe and current catalog/credits boundary.
- Unverified portrait previews are excluded from the current campaign release
  surface and must remain unreleased.

## Minimal implementation plan

1. Add the provenance audit ledger and source-parity test.
2. Check only current stabilization provenance evidence in Phase 12.1 and
   synchronize canonical docs, lessons, version metadata, generated credits,
   and additive request/contract/QA/handoff records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next roadmap item.

## Non-goals

- Do not promote portrait previews, add new campaign assets/audio files/routes,
  change registry entries, add persistence, create screenshots, or make legal,
  human-quality, public-release, or educational claims.
- Do not treat machine provenance fields as proof of output quality, training-
  data provenance, or human approval.

## Stop conditions

Stop if the current provenance checks cannot be source-linked without promoting
an unverified preview, adding an asset/runtime authority path, or making a
legal or human judgment.

## Risk label

Risk: low

Reason: The slice records existing technical registry/release provenance and
explicit exclusions without changing assets, catalogs, runtime, or simulation.
