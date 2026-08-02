# Implementation Plan — Committed effect delta legibility v0.14.7

## Target slice

Make existing committed resolution-effect deltas explicit in the shared
consequence-link renderer. Keep the change browser-local and presentation-only;
the host remains authoritative for effects, metrics, replay, and history.

## Boundaries

- In scope: a strict formatter for committed-effect `delta`, a text node in
  consequence-link cards, focused malformed-input tests, current docs, and
  synchronized provenance/device evidence.
- Out of scope: Rust/MCP routes or DTOs, simulation/effect generation,
  persistence/replay formats, action legality, assets/audio, campaign rules,
  and additional browser engines.

## Acceptance criteria

1. Positive, negative, and zero numeric deltas render with unambiguous signs.
2. Missing, non-integer, boolean, array, object, and non-finite values render
   `Delta unavailable` only for committed effects.
3. Regional signal/process links do not claim a delta they do not carry.
4. Source, timing/hash context, focus controls, and information-boundary text
   remain unchanged; no private or resolved input is exposed.
5. Focused tests, full suites, documentation currentness, and presentation
   audits pass; the sole medium-effort reviewer reports no actionable issue.

## Verification plan

- `python3 -m unittest tests.test_consequence_links`
- Full Python discovery, Rust format/clippy/tests, Node syntax, documentation
  currentness/links, release metadata, asset/provenance/security/release,
  browser/offline/loading/audio/raster/contract, and device-proxy checks.
- Refresh only current device/provenance measurements after source changes;
  preserve historical evidence records.
