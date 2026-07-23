# Implementation Plan — Visual/audio Phase 11.2 asset-size budget v0.12.97

## Target slice

Define and machine-check a bounded asset-size budget for the tracked release
package. The checker will report per-class file count, total bytes, largest
file, and pass/fail status for the existing release SVG class and the complete
release package.

## Selection rationale

Phase 11.1 remains open for full campaign coverage, durable save/load/replay
continuity, screenshots, and human-quality evidence. Phase 11.2 is the next
unstarted roadmap milestone; its first explicit checklist item is an asset-size
budget. Existing release assets are small, deterministic, and already listed
in `assets/ASSET_RELEASE_MANIFEST.json`, so a registry-adjacent budget contract
is a bounded slice with inspectable evidence.

## Design

1. Add `assets/asset-budget.json` with `asset-budget-v1`, two named classes,
   explicit root/include patterns, file-count limits, per-file byte limits,
   and total-byte limits.
2. Add dependency-free `scripts/check_asset_budget.py` that validates the
   budget schema, resolves only in-repository files, emits a deterministic JSON
   report, and exits nonzero when a class exceeds a limit or has no files.
3. Add Python tests for schema/report shape, observed release counts and bytes,
   script execution, path-boundary validation, and limit failure behavior.
4. Update Phase 11.2 roadmap evidence, canonical records, asset guidance,
   lessons, QA, handoff, changelog, and version projections.

## Explicit boundary

The budget covers tracked `assets/release` files only. Source references,
generated portrait previews, Rust binaries, JavaScript bundles, browser cache,
decode time, render time, memory, offline operation, low-power devices, and
browser compatibility remain outside this slice and must not be claimed as
verified performance.

## Verification gate

Run the focused asset-budget tests, the checker, `cargo fmt`, `cargo test`,
Clippy with warnings denied, full Python discovery, release/documentation/
asset/security/generation checks, and the visual/audio contract audit before
one code-reviewer handoff. Merge the temporary branch to `main`, delete it
locally and remotely, then re-audit the next unmet roadmap item.
