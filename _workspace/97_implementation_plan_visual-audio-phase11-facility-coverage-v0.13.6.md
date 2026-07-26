# Implementation Plan — Visual/audio Phase 11.1 facility asset coverage v0.13.6

## Target slice

Close the Phase 11.1 `Facility asset coverage complete` checklist item by
proving that every file-backed facility in the live `FACILITY_COMPONENTS`
catalog has a source SVG, a release SVG, and an approved matching visual
registry entry. Keep the generic facility descriptor as an explicit fallback,
not as a release asset.

## Selection rationale

The campaign ledger already names all current facility IDs, but its evidence
does not join those IDs to the release registry. This is the smallest useful
next slice: it converts catalog presence into a fail-closed coverage check and
directly supports the Phase 11.1 asset-registry gate without changing runtime
rendering or campaign semantics.

## Design

1. Add a machine-readable facility-asset coverage section to the existing
   campaign ledger, with the file-backed IDs, registry ID prefix, and explicit
   generic fallback boundary.
2. Extend the Phase 11.1 coverage test to compare the live catalog, source and
   release files, and `visual-assets.json` entries, including semantic role,
   hashes, and approved status through the existing asset validator.
3. Close only the facility asset coverage checklist item; retain overlay,
   screenshot, placement, continuity, performance, device, compatibility, and
   human-evaluation limits as open.
4. Record the contract, SDD status, roadmap evidence, QA, changelog, and
   version projections for v0.13.6.

## Explicit boundary

This slice audits repository assets and catalog wiring. It does not add new
art, claim that every campaign placement has been screenshot-reviewed, alter
the GUI, consume hidden state, change host authority, or establish human
visual quality/accessibility evidence.

## Verification gate

Run the focused campaign-coverage and asset-registry tests, then the full
Python suite, `cargo fmt --check`, Clippy with warnings denied, and all release,
documentation, security, and visual/audio contract checks before one
code-reviewer handoff. Merge the branch to `main`, then re-audit the next
unchecked roadmap item.

## Acceptance criteria

- Every file-backed facility catalog entry has existing source and release
  paths.
- Each file-backed facility maps exactly once to `visual.facility.<id>`.
- Registry source/release paths match the live catalog and approved hashes.
- `generic-facility` has no asset paths and remains the unknown fallback.
- Only the Phase 11.1 facility asset coverage item is checked.

## Risk label

Risk: low

Reason: the change adds deterministic governance evidence and tests only; no
runtime, simulation, host DTO, audio, replay, or asset bytes change.
