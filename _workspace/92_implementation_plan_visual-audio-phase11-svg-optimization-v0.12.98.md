# Implementation Plan — Visual/audio Phase 11.2 SVG optimization v0.12.98

## Target slice

Enable a conservative, dependency-free release-SVG normalization pass for the
15 tracked `assets/release/visual/svg/*.svg` files, then add a fail-closed
check that every release SVG is idempotently normalized and that registry and
manifest hashes match the optimized bytes.

## Selection rationale

The v0.12.97 asset-size budget closed the first Phase 11.2 checklist item.
SVG optimization is the next explicit item, and the release derivatives use
safe inter-tag formatting whitespace that can be removed without changing
text-node content, attributes, styles, dimensions, or accessible title/desc
content.

## Design

1. Add `scripts/optimize_release_svg.py` with a pure normalization function
   that strips outer whitespace and collapses whitespace between XML tags only.
2. Run the optimizer on the tracked release SVG class, update only the
   corresponding registry `release_hash` fields, regenerate the deterministic
   release manifest, and preserve source files and original hashes.
3. Add `--check`/report behavior and tests for idempotence, text preservation,
   registry/manifest alignment, and fail-closed malformed/path boundaries.
4. Update Phase 11.2 evidence, canonical records, lessons, asset guidance,
   QA, handoff, changelog, and version projections.

## Explicit boundary

The pass is a byte-level formatting normalization, not a semantic SVG rewrite.
It does not remove accessible text, alter geometry, change styles or URLs,
convert raster assets, measure render time, or claim runtime performance.

## Verification gate

Run focused SVG tests and the optimizer check, `cargo fmt`, `cargo test`,
Clippy with warnings denied, full Python discovery, release/documentation/
asset/security/generation checks, and the visual/audio contract audit before
one code-reviewer handoff. Merge the temporary branch to `main`, delete it
locally and remotely, then re-audit the next unmet roadmap item.
