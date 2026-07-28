# Implementation Plan — Phase 12.3 causal attribution boundary v0.13.41

## Task restatement

Close the current Phase 12.3 evidence item for causal attribution by recording
the existing host-sourced direct-effect and before/after presentation contract.
Keep inferred causal graphs, causal certainty, and human comprehension as
separately open work.

## Current understanding

- The host exposes typed `ResolutionEffect` source, metric, delta, and text
  fields from committed transition effects.
- The resolution envelope orders decision-time snapshots, visible responses,
  process/operation/resource changes, direct effects, new information, and
  pending processes.
- The browser renders direct effects and consequence links with source text and
  state hashes; it does not author effects or infer a causal graph.
- The debrief labels attributed mechanisms as items to inspect, not proof of
  causality or policy validity.

## Target slice

Add `docs/evaluation/phase12-causal-attribution-boundary.json` and a parity
test that record:

- typed direct-effect source/metric/delta/text fields;
- ordered before/after and direct-effect resolution stages;
- source-linked browser consequence rendering and written fallback;
- host/read-only/live-GUI boundaries; and
- explicit limits against inferred causal graphs, hidden inputs, forecasts,
  causal certainty, and human educational conclusions.

## Assumptions

- “Visualized” means the current technical direct-effect/consequence layer is
  source-linked and text-readable; it is not a claim of causal inference.
- Before/after comparison remains descriptive and host-supplied; the browser
  cannot author effect magnitude, source, or outcome.
- Existing direct effects are sufficient evidence for this current checklist
  item; a broader causal graph requires a separate source-backed design gate.

## Minimal implementation plan

1. Add the causal-attribution boundary ledger and source-parity test.
2. Check the Phase 12.3 item and synchronize canonical docs, lessons, version
   metadata, generated credits, and additive request/contract/QA/handoff
   records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next Phase 12.3 item.

## Non-goals

- Do not add causal inference, hidden-state fields, probability/calibration,
  counterfactuals, distributional views, exports, assets, audio files,
  persistence, routes, or educational claims.
- Do not convert before/after comparisons into causal certainty or future
  outcome forecasts.

## Stop conditions

Stop if the direct host effect source cannot remain distinct from inferred
causality, hidden inputs, or human learning claims.

## Risk label

Risk: low

Reason: The slice records existing host-sourced attribution boundaries only; it
adds no runtime behavior or inference authority.
