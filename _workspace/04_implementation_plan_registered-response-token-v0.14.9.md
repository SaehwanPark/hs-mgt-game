# Implementation Plan — Registered response status token v0.14.9

## Target slice

Reuse the approved `status-reported` runtime visual token in visible response
link headings. Keep the change presentation-only; the existing catalog,
provenance, fallback, and host response projection remain authoritative.

## Boundaries

- In scope: response-card token wiring, focused token/rendering regression
  coverage, current docs, and synchronized device evidence.
- Out of scope: new asset files or registry entries, audio, Rust/MCP routes or
  DTOs, simulation/effect generation, persistence/replay formats, action
  legality, campaign rules, and additional browser engines.

## Acceptance criteria

1. Only `visible-response` links receive the registered `status-reported`
   token; effects and regional signals/processes retain their current cards.
2. The token carries its existing label, symbol, source, tooltip, and written
   equivalent; color is not required for meaning.
3. Response text, source/replay context, target-free information boundary,
   keyboard focus, mute/reduced-motion behavior, and missing-data fallbacks are
   unchanged.
4. Focused tests, full suites, documentation currentness, asset/security,
   browser/offline/loading, visual/audio, and device checks pass; the sole
   medium-effort reviewer reports no actionable issue.
