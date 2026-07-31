# Implementation Plan — Persisted full-campaign raster evidence v0.13.81

## Task restatement

Persist one active and one terminal 1024×768 screenshot for each launchable
campaign as non-release evaluation evidence, with hashes and dimensions bound
to the existing host-owned campaign-coverage surface.

## Current understanding

- `campaign-coverage-v1` already exposes active and terminal coverage for
  competitive, stabilization, and regional affiliation.
- v0.13.80 recorded the same six states through local-browser inspection, but
  the captures were intentionally ephemeral and therefore did not close the
  technical raster-artifact evidence gap.
- The connected local browser can return raw JPEG bytes, while no Chromium,
  Playwright, or production screenshot runner is part of the repository.

## Assumptions

- The existing loopback route and shared renderer remain the only source for
  captured content.
- Evaluation screenshots are documentation/evidence artifacts, not release
  assets, and must remain outside the asset registry and release directories.
- A persisted raster artifact proves capture reproducibility and geometry only;
  it does not establish pixel-level quality, accessibility, educational value,
  legal clearance, cross-browser compatibility, or public-release approval.

If any assumption is false, stop and report the mismatch before editing.

## Target slice

1. Capture active and terminal states for the three launchable campaigns at
   1024×768 using the existing loopback GUI and host campaign-coverage route.
2. Persist six JPEG artifacts under `docs/evaluation/` with stable names,
   SHA-256 hashes, byte sizes, MIME type, and exact 1024×768 dimensions; retain
   a separate capture-generated metadata record for each pre-padding frame.
3. Add a raster-evidence manifest and ledger entry that bind every artifact to
   its campaign/state, source markers, host-visible fields, and non-release
   boundary.
4. Add a standard-library-only validator that fails closed on missing files,
   hash/size/dimension drift, unknown state pairs, release-path placement, or
   missing authority and written-fallback limits.
5. Update the roadmap, SPEC, changelog, version, lessons, and handoff records.
6. Run focused/full validation and complete exactly one medium-effort review.

## Likely files

- `docs/evaluation/phase11.1-full-campaign-raster-evidence.json`: persisted
  six-state manifest and explicit technical limits.
- `docs/evaluation/phase11.1-full-campaign-raster-capture-metadata.json`:
  capture-generated native dimensions, raw byte sizes, and raw hashes before
  canvas padding.
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`: additive ledger
  projection for the persisted raster evidence.
- `docs/evaluation/phase11.1-campaign-raster/`: six non-release JPEG files.
- `tests/test_phase11_full_campaign_raster_evidence.py`: artifact, hash,
  geometry, source, authority, and boundary regression test.
- `tests/test_phase11_campaign_coverage.py` and
  `tests/test_release_metadata.py`: expected ledger/version assertions.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `README.md`,
  `CHANGELOG.md`, `Cargo.toml`, `Cargo.lock`, and `LESSONS.md`: synchronized
  project state and version `0.13.81`.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`, `_workspace/03_presentation_qa.md`,
  and `_workspace/final/handoff.md`: additive operational handoffs.

Avoid editing files outside this list unless the plan is incomplete; if that
happens, stop and explain why.

## Tests and checks

- `python3 -m unittest tests/test_phase11_full_campaign_raster_evidence.py`
- `python3 tests/test_phase11_full_campaign_raster_evidence.py`
- Full repository validation used by the contributor documentation, including
  Rust tests, Clippy, formatting, release metadata, documentation links, asset
  gates, GUI/Python tests, Node syntax, and offline/browser contracts.

Expected result: exactly six persisted JPEGs exist, each is a valid 1024×768
artifact whose manifest hash and byte size match, and the evidence still
states that the captures are not release assets or human review.

## Acceptance criteria

- The six exact campaign/state pairs are present and source-bound to the
  existing `campaign-coverage-v1` route and shared GUI renderer.
- Exactly six expected JPEG artifacts are present under the evidence directory;
  each has a verified SHA-256 and 1024×768 geometry, and is explicitly
  `release_eligible: false`.
- The capture-generated metadata binds each normalized artifact to its native
  pre-padding dimensions and raw capture hash/size.
- The validator rejects missing/changed artifacts, wrong dimensions, unknown
  state values, release-path placement, and omitted authority/fallback limits.
- No route, schema, simulation rule, stochastic input, browser authority,
  release asset, audio file, or hidden-state field is added.

## Non-goals

- Do not add browser automation dependencies or a production screenshot runner.
- Do not register evaluation JPEGs as visual/audio release assets.
- Do not claim pixel-level visual quality, accessibility, educational,
  provenance/legal, cross-browser/device, or public-release approval.
- Do not change simulation, persistence, replay, campaign controls, or asset
  registries.

## Stop conditions

- Stop if capturing requires a new route, schema, simulation field, or browser
  authority path.
- Stop if any artifact cannot be tied to the six-state matrix or exact source
  route without fabricating host/player content.
- Stop if the artifacts prove to be release assets or require human judgment
  to establish their technical validity.

## Handoff instruction

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising.

## Risk

Risk: low

Reason: the slice adds immutable evaluation evidence and a fail-closed
validator over existing host/browser behavior without changing runtime rules.
