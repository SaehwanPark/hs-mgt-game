# Implementation Plan — Visual/audio Phase 9.2 release reproducibility v0.12.81

## Target slice

Complete the next bounded Phase 9.2 release-hardening slice by adding a
dependency-free metadata audit and deterministic manifest projection for
approved release assets.

## Scope

- Extend `scripts/validate_asset_security.py` with explicit metadata checks:
  reject unexpected PNG text/EXIF chunks, JPEG APP1/COM metadata, GIF comment
  extensions, and metadata-bearing audio tags in release files; preserve the
  existing source-preview exception and document it.
- Add `scripts/verify_asset_release.py` to read canonical registry release
  paths, validate path/hash/approval binding through the existing registry
  gate, and emit a stable sorted manifest containing each release file's
  relative path, byte size, SHA-256, and canonical digest.
- Commit the generated `assets/ASSET_RELEASE_MANIFEST.json` projection and
  fail CI when regeneration differs from the committed output.
- Add temporary-fixture tests for metadata classes, stale manifest output,
  path ordering, missing release files, and deterministic repeated generation.
- Update contributor/release guidance, CI, roadmap evidence, specification,
  architecture, changelog, README, lessons, and presentation QA.

## Non-goals

- No asset sanitization, stripping, re-encoding, deletion, download, or
  replacement; the audit fails closed and leaves the source unchanged.
- No portrait approval, model/seed inference, release promotion, legal
  clearance, or third-party asset addition.
- No host command, session, simulation, stochastic, observation, history,
  replay, state-hash, debrief, or runtime presentation authority changes.

## Acceptance checks

- Current repository assets pass the metadata audit and the committed release
  manifest check without network access or file mutation.
- Release metadata fixtures fail closed for each supported image/audio class,
  while source-only preview metadata follows the documented scope.
- Manifest output is byte-for-byte stable across repeated generation and
  rejects stale, reordered, missing, or hash-mismatched release inputs.
- CI runs registry validation, security/metadata validation, and manifest
  parity; contributor guidance explains the non-mutating audit boundary.
- Full Python/Rust/JavaScript, asset, release, documentation, formatting,
  Clippy, and diff checks pass.

## Evidence limits

The slice establishes bounded metadata and release-inventory reproducibility
evidence. It does not prove decoder safety, legal clearance, ownership,
accessibility, audio quality, human review, educational benefit, or policy
validity. Asset loading fallback remains a separate Phase 9.2 target.

## Review contract

Use exactly one read-only code reviewer for the PR handoff. Resolve every
actionable finding before merge, then delete the temporary branch locally and
remotely.

## Review disposition

The one designated code reviewer approved the final worktree with no
actionable findings after fixes for canonical release-root enforcement,
`..` traversal and symlink rejection across all three release gates, and
FLAC APPLICATION plus MP3 ID3v1/APE metadata fixtures.
