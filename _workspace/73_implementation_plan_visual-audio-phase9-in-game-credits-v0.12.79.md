# Implementation Plan — Visual/audio Phase 9.1 in-game credits v0.12.79

## Target slice

Close the Phase 9.1 “in-game credits accessible” technical item with a
read-only asset credits/provenance panel in the static executive desktop,
backed by a generated ES module derived from the canonical visual/audio
registries.

## Scope

- Extend `scripts/generate_asset_credits.py` to generate and check
  `gui/asset-credits.mjs` alongside the Markdown credits and notice files.
- Include stable IDs, type, source/generation, license, attribution, approval,
  provenance, written equivalent, release status, and registry reference in
  the generated runtime projection.
- Add a keyboard-accessible, text-first credits/provenance disclosure to
  `gui/index.html`, with a pure renderer that uses `textContent` and explicit
  empty/fallback state.
- Keep the panel independent of host/session data and preserve large text,
  reduced motion, no-color meaning, no-network, and no-audio requirements.
- Add focused projection-parity, HTML, JavaScript, and boundary tests plus
  update the GUI guide, roadmap evidence, release docs, and QA handoff.

## Non-goals

- No portrait approval, model/seed claim, generated image, release derivative,
  external asset, network retrieval, or legal clearance.
- No host command, session state, actor observation, simulation transition,
  stochastic input, history, state hash, replay, debrief, or causal signal.
- No claim that a static credits panel is human usability or lived-accessibility
  evidence.

## Acceptance checks

- The generated runtime module is byte-stable with the canonical registries and
  stale output fails the existing credits check.
- The credits panel is present before and after host/session loading, exposes
  text equivalents and provenance/approval/release status, and has no network
  or command-submission path.
- Focused GUI tests and all existing Python/Rust/JavaScript, asset, release,
  documentation, formatting, Clippy, and diff checks pass.

## Evidence limits

The panel makes project provenance visible and reproducible. Automated tests do
not establish human accessibility, legal clearance, ownership, learning,
policy validity, or educational benefit.
