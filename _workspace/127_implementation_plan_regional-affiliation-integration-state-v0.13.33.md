# Implementation Plan — Phase 12 regional-affiliation integration-state visualization v0.13.33

## Task restatement

Continue Phase 12.2 with a bounded current integration-state presentation
record for `regional-affiliation-v1`. Bind the host `IntegrateOrDecline` stage,
integration-obligation process, begin/decline decision, visible outcome status,
written consequence language, and optional audio without exposing resolved
hidden inputs or claiming a browser-native affiliation route.

## Current understanding

- The host coverage projection exposes `Integrate or decline`, an
  `integration-obligation` process, and a `choose-integration` decision with
  begin/decline options and written uncertainty.
- The transition records actor-visible `Integrated` or `IntegrationDeclined`
  statuses and visible effects/events, while integration drag, continuity shock,
  and other resolved inputs remain outside the actor observation.
- Shared process/decision renderers and optional affiliation audio already exist;
  the live GUI launcher remains competitive-regional-v1 only.

## Target slice

Add `docs/evaluation/phase12-regional-affiliation-integration-state.json` and a
parity test that records:

- the typed integration stage and obligation process;
- begin/decline decision fields, written uncertainty, and host outcome statuses;
- visible consequence/status boundary versus hidden resolved integration inputs;
- shared process/decision renderers, written fallback, and optional audio; and
- no-new-asset, no-browser-route, persistence, instructor, and human-review
  limits.

## Assumptions

- This is current integration-state evidence, not a new visual implementation
  or a claim that integration drag is forecastable or directly visible.
- Status, metrics, effects, and written consequence text remain host-authored;
  true resolved inputs and future integration trajectory remain outside the
  player presentation.
- Existing status language, written equivalents, and optional audio are
  reusable; no stage-specific map, facility, portrait, or audio asset is
  required by the current contract.

## Minimal implementation plan

1. Add the integration-state ledger and source-parity test.
2. Check only current integration-state evidence in Phase 12.2 and synchronize
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
- Do not expose integration drag, continuity shock, private approval basis,
  hidden future obligations, legal validity, or future integration trajectory.

## Stop conditions

Stop if integration state cannot be source-linked to a host-owned process,
decision, status, visible consequence/effect boundary, and written/optional-
audio fallback without changing runtime authority or adding an asset.

## Risk label

Risk: low

Reason: The slice records existing host process, decision, status, effect,
fallback, and audio-contract boundaries without changing assets, runtime
behavior, or authority.
