# Implementation Plan — Visual/audio Phase 11.2 raster scope and bounds v0.13.0

## Target slice

Define and machine-check the raster boundary for the current repository: no
raster files may be shipped under `assets/release`, while the seven
non-release portrait preview PNGs remain bounded by explicit dimensions and
byte totals and remain ineligible for release promotion.

## Selection rationale

Phase 11.2 now has release byte budgets, normalized release SVGs, and current
catalog fallback coverage. Raster derivatives are the next packaging item;
the repository currently has no tracked release raster derivative but does
have generated, unverified portrait previews. A scope-and-bounds contract makes
that distinction machine-visible without inventing a release raster pipeline.

## Design

1. Add `assets/raster-scope.json` with release-raster prohibition and explicit
   preview width/height/file/total-byte limits.
2. Add dependency-free `scripts/check_raster_scope.py` that reports release
   raster count, preview count/bytes/dimensions, and fail-closed path/type/
   promotion violations.
3. Add Python tests for the current report, CLI JSON, release-raster failure,
   dimension/byte failure, and preview release-ineligibility boundary.
4. Update Phase 11.2 evidence, canonical records, lessons, QA, handoff,
   changelog, and version projections to v0.13.0.

## Explicit boundary

This slice does not resize or promote images, add release raster derivatives,
change portrait provenance, alter browser loading, or claim raster quality,
decode/render/memory performance, offline operation, device suitability, or
compatibility.

## Verification gate

Run focused raster-scope tests/checker, `cargo fmt`, `cargo test`, Clippy with
warnings denied, full Python discovery, release/documentation/asset/security/
generation checks, and the visual/audio contract audit before one
code-reviewer handoff. Merge the temporary branch to `main`, delete it locally
and remotely, then re-audit the next unmet roadmap item.
