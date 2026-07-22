# Implementation Plan — Visual/audio Phase 9.2 asset security v0.12.80

## Target slice

Implement the first bounded Phase 9.2 security/integrity gate as a dependency-
free scanner for untrusted visual/audio file content and bounded dimensions.

## Scope

- Add `scripts/validate_asset_security.py` with explicit file-size and
  dimension ceilings, safe repository-root traversal, and deterministic error
  messages.
- Scan registered source/release paths and preserved generation preview files
  that are within the asset roots; do not scan build artifacts or rewrite
  contributor files.
- Reject SVG scripts, inline event handlers, external URLs/references,
  embedded raster images, foreign objects, external font declarations, XML
  entities, malformed XML-like structure, and unsafe/oversized view boxes.
- Validate PNG/JPEG/GIF dimensions and WAV/OGG/MP3/FLAC magic signatures when
  those formats are present; reject unsupported audio extensions/signatures.
- Add malicious temporary fixtures and repository-scan tests; run the scanner
  in CI and contributor release guidance.

## Non-goals

- No asset sanitization/re-encoding, deletion, or mutation.
- No network fetches, model downloads, external assets, portrait approvals,
  release promotion, or legal/ownership claims.
- No host command, session, simulation, stochastic, observation, history,
  hash, replay, debrief, or runtime presentation authority changes.

## Acceptance checks

- Current repository assets pass without network access or file mutation.
- Malicious SVG fixtures fail for every prohibited content class; malformed,
  oversized, and excessive-dimension binary/audio fixtures fail closed.
- Supported codec signatures pass and unsupported/mismatched formats fail.
- CI runs both asset metadata and security checks; docs identify evidence
  limits and the remaining human/legal review gate.
- Full Python/Rust/JavaScript, asset, release, documentation, formatting,
  Clippy, and diff checks pass.

## Evidence limits

This scanner detects bounded classes of unsafe file content and malformed
signatures. It does not prove that an asset is legally distributable, safe for
all decoders, accessible, high quality, owned, or educationally beneficial.

## Review disposition

The one designated code reviewer approved the final implementation with no
actionable findings after targeted fixes for decoded SVG references, CSS and
XML stylesheet URLs, oversized-file early return, binary payload/frame
structure, strict SVG dimensions, registry-derived scope, and malformed or
unsupported registry handling.

## Verification evidence

- `python3 -m unittest discover -s tests -p 'test_*.py'` — 502 passing tests.
- `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, and
  `cargo test -- --test-threads=1` — passing.
- Asset registry, asset security, generated credits, release metadata,
  documentation links, JavaScript syntax, and diff checks — passing.
