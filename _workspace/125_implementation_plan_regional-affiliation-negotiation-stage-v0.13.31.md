# Implementation Plan — Phase 12 regional-affiliation negotiation-stage visualization v0.13.31

## Task restatement

Continue Phase 12.2 with a bounded current negotiation-stage visualization
record for `regional-affiliation-v1`. Bind the host stage label, commitment
decision form, visible commitment vector, uncertainty, process renderer, and
existing optional affiliation/negotiation audio contract without claiming a
new browser route or stage-specific art.

## Current understanding

- The host campaign-coverage projection exposes the typed
  `NegotiateCommitments` stage as `Negotiate commitments`, an active
  `Institutional stage` process, and a host-owned commitment decision with
  community, workforce, and continuity parameters.
- Existing source contracts expose visible commitment values, partner and
  stakeholder status, written uncertainty, and a reusable
  `affiliation_negotiation` audio state whose meaning remains optional.
- The shared browser renderer already renders supplied processes and decisions,
  while the live GUI launcher remains competitive-regional-v1 only.

## Target slice

Add `docs/evaluation/phase12-regional-affiliation-negotiation-stage.json` and a
parity test that records:

- the typed negotiation stage and stage-label/process projection;
- host-authoritative commitment fields, command parameters, bounds, and
  visible uncertainty;
- shared process/decision renderer and written fallback boundaries;
- reusable optional affiliation/negotiation audio eligibility; and
- no-new-asset, no-browser-route, no-hidden-state, and no-human-review limits.

## Assumptions

- This is current negotiation-stage presentation evidence, not a new visual
  implementation or a claim that the full affiliation campaign is browser
  complete.
- Commitment values and partner/stakeholder responses remain actor-visible
  only when supplied by the host; private intent, hidden thresholds, and true
  outcomes remain outside the presentation contract.
- Existing semantic markers, status language, written equivalents, and
  optional audio are reusable; no stage-specific map, facility, portrait, or
  audio asset is required by the current contract.

## Minimal implementation plan

1. Add the negotiation-stage ledger and source-parity test.
2. Check only current negotiation-stage evidence in Phase 12.2 and synchronize
   canonical docs, lessons, version metadata, generated credits, and additive
   request/contract/QA/handoff records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next roadmap item.

## Non-goals

- Do not add a browser-native affiliation route, stage art, map/facility art,
  portrait, audio file, registry entry, runtime field, persistence, screenshot,
  instructor view, or human study.
- Do not expose hidden partner intent, commitment thresholds, private review
  state, true response, causal outcome, or future agreement probability.

## Stop conditions

Stop if the negotiation stage cannot be source-linked to a host-owned process,
decision, visible commitment fields, and written/optional-audio fallbacks
without changing runtime authority or adding an asset.

## Risk label

Risk: low

Reason: The slice records existing stage, decision, process, fallback, and
audio-contract boundaries without changing assets, runtime behavior, or the
authority model.
