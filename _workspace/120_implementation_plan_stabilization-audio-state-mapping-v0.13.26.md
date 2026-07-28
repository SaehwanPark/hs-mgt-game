# Implementation Plan — Phase 12 stabilization audio-state mapping v0.13.26

## Task restatement

Continue Phase 12 with a bounded mapping of the current stabilization
campaign's actor-visible pressure/recovery vocabulary to existing optional
music and event-cue contracts. Keep the CLI-only tutorial and current live GUI
launcher boundary explicit while recording the next integration gate.

## Current understanding

- `docs/evaluation/phase12-pressure-state-registration.json` already registers
  eight shared actor-visible pressure/recovery categories and their eligible
  overlay, event-cue, music-state, text, and reduced-motion vocabulary.
- `gui/audio-cue-contract.mjs` and `gui/music-stem-contract.mjs` provide
  source-linked optional channels with written equivalents and visible-only
  triggers.
- `gui/audio-direction.mjs` documents bounded prototype direction, but the
  stabilization CLI has no audio surface and the live GUI launcher remains
  competitive-regional-v1 only.

## Target slice

Add `docs/evaluation/phase12-stabilization-audio-state-mapping.json` and a
parity test that records:

- the eight current shared pressure/recovery mappings reused by
  `stabilization-v1`;
- existing music-state and event-cue IDs, visible trigger boundaries, and
  written equivalents;
- the optional-audio, audio-direction, and no-direct-campaign-envelope
  boundaries; and
- open work for browser-native stabilization integration, direct tutorial or
  campaign audio, quality, and human review.

## Assumptions

- This is a current contract mapping, not a new audio implementation.
- Audio remains optional atmospheric/cue support; visible text and status are
  meaning-bearing and complete without playback.
- Mapping a visible category to an eligible existing ID does not infer hidden
  severity, probability, intent, causality, or future outcome.

## Minimal implementation plan

1. Add the mapping ledger and source-parity test.
2. Check only current stabilization audio-state mapping in Phase 12.1 and
   synchronize canonical docs, lessons, version metadata, generated credits,
   and additive request/contract/QA/handoff records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next roadmap item.

## Non-goals

- Do not add campaign-specific audio files, audio routes, tutorial audio,
  playback behavior, new cue or music IDs, animation, assets, screenshots,
  persistence, instructor views, or human evaluation.
- Do not call an eligible mapping direct campaign-envelope audio integration.

## Stop conditions

Stop if current mapping cannot be source-linked to existing visible fields and
catalog IDs without adding a runtime authority path, campaign content, an
asset, direct audio integration, or a quality/human judgment.

## Risk label

Risk: low

Reason: The slice joins already-tested current pressure, cue, music, and
written-equivalent contracts without changing runtime behavior or adding
audio assets.
