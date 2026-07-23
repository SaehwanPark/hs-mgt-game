# Implementation Plan — Visual/audio Phase 11.2 missing-asset fallback v0.12.99

## Target slice

Prove the existing GUI missing-asset fallback contract across every tracked
facility and fictional institution release descriptor. The test will enumerate
the live JavaScript catalogs, align their release paths to the visual registry,
and exercise missing/failed/malformed availability through the existing generic
fallback presentation boundary.

## Selection rationale

Phase 11.2 now has the asset-size budget and conservative SVG normalization
checked. Its remaining checklist includes missing-asset fallback; the GUI
already has a pure availability/presentation boundary and facility/identity
fallbacks, but coverage currently exercises only selected examples.

## Design

1. Extend `tests/test_asset_fallback.py` with a Node contract that enumerates
   all `FACILITY_COMPONENTS` and `IDENTITY_KITS` and reads the canonical visual
   registry release paths.
2. For every descriptor, pass missing, failed, and malformed availability to
   the existing presentation helpers and require fallback mode, null release
   path, non-empty written equivalent, and no hidden-state/network markers.
3. Require the catalog release paths to equal the registry release-path set,
   preventing an untested or unregistered release asset from entering the
   fallback surface.
4. Update Phase 11.2 evidence, canonical records, lessons, QA, handoff,
   changelog, and version projections.

## Explicit boundary

This slice adds test coverage only. It does not add or remove assets, change
fallback behavior, alter simulation/host state, introduce network access, or
claim full campaign coverage, human accessibility, browser compatibility, or
runtime performance.

## Verification gate

Run focused fallback tests, `cargo fmt`, `cargo test`, Clippy with warnings
denied, full Python discovery, release/documentation/asset/security/generation
checks, and the visual/audio contract audit before one code-reviewer handoff.
Merge the temporary branch to `main`, delete it locally and remotely, then
re-audit the next unmet roadmap item.
