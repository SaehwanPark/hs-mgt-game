# Implementation Plan — Phase 12 regional-affiliation replay/debrief views v0.13.36

## Task restatement

Continue Phase 12.2 with a bounded current replay/debrief surface record for
`regional-affiliation-v1`. Join immutable replay artifact verification, host
history/replay metadata, terminal debrief content, and shared text renderers
without claiming a browser-native affiliation view or an educational result.

## Current understanding

- The affiliation model has a versioned replay artifact containing the seed,
  ruleset version, genesis, and typed transition history.
- Serialization validates the artifact version and ruleset; replay rechecks
  prior state, actor observation, and state hashes.
- The host campaign-coverage and end-session envelopes expose summarized
  history, replay count/hash metadata, and a terminal affiliation debrief.
- The CLI debrief supplies stylized outcomes, decision-quality prompts,
  alternatives, and stage response detail; the shared browser renderer is
  text-first and the live launcher remains competitive-regional-v1 only.

## Target slice

Add `docs/evaluation/phase12-regional-affiliation-replay-debrief.json` and a
parity test that record:

- replay artifact versioning, serialization, ruleset checks, replay integrity,
  transition history, and state-hash alignment;
- host campaign-coverage/end-session history, replay, and debrief fields;
- terminal debrief outcomes, decision-quality language, alternatives, and
  written rendering; and
- CLI/shared-renderer boundaries, live-GUI limitation, no-hidden-state claim,
  no-new-asset boundary, and human-review limits.

## Assumptions

- This is current technical replay/debrief evidence, not a new replay route,
  persistence implementation, browser affiliation view, or instructor surface.
- Typed replay artifacts and terminal debriefs may retain post-resolution
  detail for their existing CLI/host contract; no browser actor-visible claim
  promotes resolved inputs into a live decision view.
- Written history, hashes, debrief lines, source attribution, and uncertainty
  remain the fallback when visual/audio presentation is absent.

## Minimal implementation plan

1. Add the replay/debrief ledger and source-parity test.
2. Check the Phase 12.2 replay/debrief item and synchronize canonical docs,
   lessons, version metadata, generated credits, and additive request/contract/
   QA/handoff records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next roadmap item.

## Non-goals

- Do not add browser-native affiliation replay/debrief routes, animation,
  persistence, screenshots, instructor views, assets, audio files, runtime
  fields, authority paths, or public-release claims.
- Do not turn resolved inputs, private rationale, hidden thresholds, legal
  validity, causal certainty, or future outcomes into actor-visible controls or
  predictions.

## Stop conditions

Stop if replay/debrief evidence cannot be source-linked to versioned artifact
integrity, host history/replay metadata, terminal debrief content, and written
fallback while preserving the live-GUI and actor-observation boundaries.

## Risk label

Risk: low

Reason: The slice records existing replay/debrief contracts and presentation
limits without changing runtime behavior, persistence, or authority.
