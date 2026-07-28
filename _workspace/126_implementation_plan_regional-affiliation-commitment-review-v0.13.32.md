# Implementation Plan — Phase 12 regional-affiliation commitment and review states v0.13.32

## Task restatement

Continue Phase 12.2 with a bounded current commitment/review-state
presentation record for `regional-affiliation-v1`. Bind host-projected
commitment values and partner response states to the institutional-review
process, submit/await commands, reported review statuses, written equivalents,
and optional audio without claiming a complete browser campaign.

## Current understanding

- The host coverage projection exposes community, workforce, and continuity
  commitments as visible metrics and exposes partner/stakeholder responses as
  reported actor signals.
- The host exposes an `institutional-review` pending process during submit and
  resolve stages, with `submit-review` and `await-review` decisions and written
  uncertainty about timing and outcome.
- The shared browser renderer can display supplied process and decision fields;
  the live GUI launcher remains competitive-regional-v1 only.

## Target slice

Add `docs/evaluation/phase12-regional-affiliation-commitment-review.json` and a
parity test that records:

- visible commitment metrics and partner response states;
- pending institutional-review process and submit/await decision states;
- host-reported review response/status vocabulary and transition boundary;
- shared process/decision renderers, written fallback, and optional audio; and
- no-new-asset, no-browser-route, no-hidden-state, and no-human-review limits.

## Assumptions

- This is current commitment/review-state evidence, not a new visual
  implementation or a claim that review outcomes are forecastable.
- Review responses are stylized host-resolved observations; they are not legal,
  regulatory, partner, or educational predictions.
- Existing status language, written equivalents, and optional audio are
  reusable; no stage-specific map, facility, portrait, or audio asset is
  required by the current contract.

## Minimal implementation plan

1. Add the commitment/review-state ledger and source-parity test.
2. Check only current commitment/review evidence in Phase 12.2 and synchronize
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
- Do not expose private review deliberation, hidden thresholds, agreement
  probability, true response, legal validity, or future integration outcome.

## Stop conditions

Stop if commitment and review states cannot be source-linked to host-owned
metrics, process, decisions, response/status fields, and written/optional-audio
fallbacks without changing runtime authority or adding an asset.

## Risk label

Risk: low

Reason: The slice records existing host observation, process, command, status,
fallback, and audio-contract boundaries without changing assets, runtime
behavior, or authority.
