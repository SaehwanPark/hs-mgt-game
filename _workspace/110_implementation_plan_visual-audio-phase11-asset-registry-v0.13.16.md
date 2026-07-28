# Implementation Plan — Visual/audio Phase 11.1 current asset-registry coverage v0.13.16

## Task restatement

Record and verify 100% coverage of the current tracked visual and audio asset
registries as a bounded Phase 11.1 registry-completeness item. Existing
validators already require schema, provenance, approval, path, hash, license,
accessible-equivalent, and release-boundary correctness. This slice adds an
explicit campaign ledger contract and parity evidence without claiming that
all future campaign assets exist, that every registry entry is file-backed, or
that asset quality and screenshots are complete.

## Current understanding

- `assets/registry/visual-assets.json` contains 38 approved visual entries;
  `assets/registry/audio-assets.json` contains 7 approved audio entries.
- Fifteen approved visual entries have release paths under
  `assets/release/visual/svg`; runtime-generated and catalog/documentation
  entries intentionally have null release paths.
- `scripts/validate_assets.py` checks registry schema, IDs, semantic roles,
  provenance, licenses, hashes, accessible equivalents, and denylisted terms.
- `scripts/verify_asset_release.py` checks every non-null release path and its
  generated manifest; `scripts/generate_asset_credits.py` checks the
  deterministic attribution projections.
- `tests/test_asset_registry.py`, the release/security tests, and the existing
  Phase 11 campaign tests provide focused registry and fallback evidence.

## Target slice

Define `asset_registry_coverage` for the current tracked registries:

- exact visual/audio entry counts and schema sources;
- approved-entry and unique-ID closure;
- release-path/file-backed versus runtime-generated boundary;
- validator, release-manifest, security, and credits evidence; and
- explicit limits for future assets, visual/audio quality, screenshots,
  accessibility, and human review.

## Assumptions

- “100%” means every current tracked registry entry is valid, approved, unique,
  provenance-complete, and correctly classified for its release path; it does
  not mean every future campaign need is represented or file-backed.
- The existing validators are authoritative for entry-level correctness, so
  the implementation should add only a ledger/parity contract over them.
- Runtime-generated audio and GUI module sources are valid registered assets
  with explicit null release paths, not missing release files.

If a stated registry boundary is not directly covered, add only the smallest
focused assertion required before closing the bounded item.

## Minimal implementation plan

1. Add `asset_registry_coverage` to the Phase 11.1 campaign ledger with exact
   visual/audio counts, release/runtime classification, source validators, and
   limits.
2. Extend `tests/test_phase11_campaign_coverage.py` to load both registries,
   validate the ledger counts/approval boundary, and link it to live registry,
   release, security, and credits sources.
3. Update the roadmap checklist/status and add v0.13.16 evidence; synchronize
   `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `LESSONS.md`, version metadata,
   and additive request/contract/QA/handoff records.
4. Run focused/full Python and Rust checks plus release/documentation, asset,
   security, offline, browser, device, and visual/audio contract checks.
5. Stop before adding unregistered assets, promoting runtime sources to files,
   creating screenshot tooling, or making quality/human-evaluation claims.

## Files and functions likely to change

- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`.
- `tests/test_phase11_campaign_coverage.py` and, only if a gap is found,
  `tests/test_asset_registry.py`.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`, `_workspace/03_presentation_qa.md`,
  this plan, and `_workspace/final/handoff.md`.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `ARCHITECTURE.md`,
  `CHANGELOG.md`, `LESSONS.md`, `README.md`, `Cargo.toml`, `Cargo.lock`, and
  generated package-version projections.

Avoid changing registry entries, asset bytes, Rust runtime, GUI behavior, or
audio behavior unless focused inspection proves the current registry is
incorrect.

## Tests and checks

- `python3 -m unittest tests.test_asset_registry tests.test_phase11_campaign_coverage`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `cargo fmt --check`
- `cargo test -- --test-threads=1`
- `cargo clippy --all-targets --all-features -- -D warnings`
- release, documentation, asset/security, credits, offline, browser-policy,
  device-policy, and visual/audio contract checks.

## Acceptance criteria

- The ledger records exact current visual/audio registry counts, approved-entry
  and unique-ID closure, release/runtime classification, and validator sources.
- Coverage tests prove the ledger counts match both live registry documents and
  require the existing validator/release/security/credits evidence.
- The roadmap closes only current asset-registry completeness; future campaign
  assets, placement/use, asset quality, screenshots, accessibility, and human
  review remain open.
- Package version increments to v0.13.16 and generated metadata is consistent.

## Non-goals

- Do not add or remove asset entries, file-backed audio, raster derivatives,
  screenshots, browser dependencies, telemetry, or human evaluation.
- Do not call current registry validity a complete campaign asset inventory or
  an asset-quality approval.

## Stop conditions

Stop if evidence requires a new asset, release derivative, screenshot suite,
quality judgment, human review, or a claim beyond current registry closure.

## Review checklist

- Visual/audio counts and registry source paths match exactly.
- All current entries are approved, unique, provenance-complete, and validated.
- File-backed release paths are distinct from runtime-generated null paths.
- Release manifest, security, and credits sources remain linked.
- Future campaign inventory, quality, screenshot, accessibility, and human
  limits are explicit in docs and ledger.
- No unrelated runtime, asset, audio, or simulation behavior changed.

## Risk label

Risk: low

Reason: The slice adds an evidence contract over already-valid registries and
existing deterministic checks; no registry contents or runtime behavior is
intended to change.
