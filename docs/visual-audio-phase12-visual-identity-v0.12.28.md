# Visual/audio Phase 12 — Visual identity and marker provenance

**Status:** Implemented and verified; exactly one general code-review pass complete
**Scope:** Presentation-only identity, marker, and generated-asset provenance
**Version:** 0.12.28

## Purpose

Phase 11 makes the first competitive session reachable. The next bounded gap is
recognition: the existing regional desktop renders generic symbols, so a first
time executive must repeatedly decode which system, facility, pressure, or
process a row represents. This phase adds a small, explicit vocabulary without
adding geography, simulation state, or third-party assets.

## User contract

- Riverside, Northlake, and Summit show stable identity labels and symbols.
- Facility, demand, capacity, project, staffing, payer/policy, and timeline
  surfaces show category markers with visible text.
- Existing status text, symbol/pattern, source labels, and missingness remain
  available; color is never the only distinction.
- Unknown systems or categories show a generic token rather than a guessed
  identity.

## Boundary

`visual.mjs` will expose a frozen `visual-catalog-v1` and pure lookup helpers.
`app.mjs` will use those helpers at existing map, selected-detail, facility,
overlay, and process render points. `visual-catalog.json` and
`ASSET_CREDITS.md` will record project-generated glyph/CSS primitives and no
third-party files.

## Authority and limits

The host remains authoritative for every displayed fact and status. The browser
uses only visible IDs, names, kinds, labels, and categories. Visual lookup does
not calculate severity, add actor knowledge, issue commands, modify state, or
enter replay/history/hash/debrief data. No human usability or lived-accessibility
claim follows from the technical checks.

## Verification

- Registry and lookup tests cover all required entries plus unknown/empty
  fallback.
- GUI tests verify tokens retain semantic labels and existing source/status
  text, with no host/simulation/network/asset boundary break.
- Node syntax, Python discovery, Rust tests/lint/format, release metadata, and
  diff checks pass.

Focused visual identity plus existing GUI/audio/accessibility/regional/static/
release tests: 32 passed; full Python discovery: 299 passed. Serial Rust tests,
formatting, Clippy, Node syntax, release metadata, and domain QA pass. The one
general review found and fixed exact visible-ID fallback and status-catalog
duplication issues; no second review pass is run.

## Explicit non-goals and next gate

This phase does not acquire images or audio, redesign map geometry, animate
transitions, add campaign-specific identity, change a host DTO, or evaluate
human recognition. Later visual asset production requires separate provenance
and release approval; broader first-month polish remains gated by the product
contract and AI-agent evidence.
