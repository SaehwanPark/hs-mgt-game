# Implementation Plan — Visual/audio Phase 11.1 campaign-coverage evidence v0.12.88

## Task restatement

Create a machine-checkable coverage ledger for the current
`competitive-regional-v1` presentation catalog and bounded continuity path.
Use it to close only the technical Phase 11.1 items that are directly
evidenced; keep full-campaign screenshot, performance, and human-quality gates
open.

## Target slice

- Inventory the live facility, operational-overlay, actor-family, event-marker,
  event-cue, and music-state catalogs.
- Verify each catalog has unique IDs, visible source/equivalent text, and the
  documented generic/unknown fallback where the adapter provides one.
- Verify the existing first-month/history/debrief/replay continuity surfaces
  remain the bounded campaign evidence path.
- Record exact evidence scope and known limits in a JSON ledger, regression
  test, roadmap subsection, and project records.

## Assumptions

- “Coverage” means the committed presentation catalogs and current bounded
  first-month path, not an assertion that every future campaign entity or
  screenshot has been exercised.
- The test may import pure browser modules under Node, but must not start a
  server, fetch a resource, read host state, or mutate simulation/history.
- Existing asset validators remain the source of truth for registry/release
  coverage; this slice does not add or promote assets.

## Minimal implementation plan

1. Add `docs/evaluation/phase11.1-campaign-coverage-ledger.json` with exact
   catalog IDs, evidence references, fallback boundaries, and open limits.
2. Add `tests/test_phase11_campaign_coverage.py` with a Node probe that compares
   the live module exports to the ledger and exercises unknown/fallback paths.
3. Update only the Phase 11.1 checklist entries supported by this evidence;
   leave full facility/overlay/event/history/debrief/save-load/replay and
   screenshot completion open where the ledger is bounded.
4. Update contracts, QA, architecture, SPEC, README, changelog, LESSONS,
   version projections, and CI; do not change runtime behavior.
5. Run the full verification matrix and use the same single code reviewer.

## Acceptance criteria

- Ledger IDs exactly match the current live catalog exports.
- Catalog items have visible source/equivalent semantics and stable unique IDs.
- Unknown facility, actor, overlay, event-marker, and asset outcomes remain
  explicit generic fallbacks; unknown audio/music remains non-authoritative.
- The bounded continuity evidence names first-month, history, debrief, replay,
  and fallback surfaces without claiming full-campaign or screenshot coverage.
- No runtime, host, simulation, stochastic, history, replay, asset, or
  participant-data change is introduced.

## Non-goals and stop conditions

- Do not generate screenshots, benchmark devices, add assets, or claim full
  competitive-campaign visual/audio completion.
- Do not expose hidden state, actor intent, severity, future outcomes, or client
  authority through the ledger or test.
- Stop if validating the current catalog requires a new runtime path or
  external service.

## Review checklist

- Exact ledger/test parity and duplicate detection.
- Fallback and information-boundary assertions.
- Roadmap statuses do not overclaim full campaign coverage.
- Exactly one existing code reviewer inspects the final diff.

## Risk label

Risk: low

Reason: this is evidence and documentation over existing pure presentation
contracts; it does not change the client, host, simulation, or assets.
