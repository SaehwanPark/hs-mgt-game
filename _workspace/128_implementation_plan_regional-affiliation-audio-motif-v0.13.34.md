# Implementation Plan — Phase 12 regional-affiliation audio motif v0.13.34

## Task restatement

Continue Phase 12.2 with a bounded current affiliation-audio motif record for
`regional-affiliation-v1`. Bind the existing `affiliation_negotiation` music
state, explicit `event.affiliation-milestone` cue, visible trigger sources,
written equivalents, and audio-off fallback without adding audio content or
claiming direct campaign-envelope integration.

## Current understanding

- The reusable music contract already defines an affiliation/negotiation state
  with a visible partner, coalition, commitment, or negotiation trigger,
  restrained generated stems, and complete written fallback.
- The event-cue contract already defines a committed visible affiliation
  milestone cue with a stage/status marker and written equivalent.
- Host resolution and browser audio routing classify only visible text/events;
  audio remains optional and the live GUI launcher remains
  competitive-regional-v1 only.

## Target slice

Add `docs/evaluation/phase12-regional-affiliation-audio-motif.json` and a parity
test that records:

- the shared music state and event-cue motif metadata;
- visible trigger sources, classifier/cue routing, and text equivalents;
- generated-audio, normalization, crossfade, and audio-off fallback boundaries;
- current shared campaign eligibility versus direct affiliation integration; and
- no-new-file, no-audio-asset, no-hidden-state, and human-quality limits.

## Assumptions

- This is current reusable affiliation-audio evidence, not a new audio-content
  implementation or a claim that the affiliation campaign directly plays the
  motif in a browser route.
- Audio may reflect only explicit visible partner/negotiation/stage context or
  committed affiliation events; it cannot encode agreement, severity, success,
  private intent, or future outcome.
- Existing generated Web Audio, text equivalents, mute controls, and fallback
  contracts are reusable; no release audio asset is required.

## Minimal implementation plan

1. Add the affiliation-audio motif ledger and source-parity test.
2. Check only current affiliation-audio evidence in Phase 12.2 and synchronize
   canonical docs, lessons, version metadata, generated credits, and additive
   request/contract/QA/handoff records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next roadmap item.

## Non-goals

- Do not add recorded audio, release audio files, new stems, new cue IDs,
  browser routes, runtime fields, persistence, screenshots, instructor views,
  or human listening studies.
- Do not infer agreement, severity, quality, private intent, legal clearance,
  educational effect, or future campaign outcome from audio.

## Stop conditions

Stop if the affiliation motif cannot be source-linked to explicit visible
triggers, text equivalents, and audio-off fallback without adding content,
changing authority, or making audio necessary.

## Risk label

Risk: low

Reason: The slice records existing reusable music/cue contracts and visible
fallback boundaries without changing audio content, runtime behavior, or
authority.
