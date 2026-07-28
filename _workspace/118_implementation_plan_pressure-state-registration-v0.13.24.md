# Implementation Plan — Phase 12 current pressure-state registration v0.13.24

## Task restatement

Continue Phase 12 with a bounded registration of the current actor-visible
pressure-state taxonomy. Bind existing operational overlays, statuses, event
cue candidates, and music states without inventing hidden severity or claiming
that campaign-specific pressure presentation is complete.

## Current understanding

- `gui/operational-overlays.mjs` already defines twelve actor-visible
  operational categories with direct visible fields, text equivalents, and
  non-color patterns.
- `gui/visual-catalog.json` provides approved status tokens, while the event
  cue and music contracts provide optional visible-only audio vocabulary.
- Phase 12.1 still has “new pressure states registered” open, but the current
  shared taxonomy has not been recorded as one cross-catalog evidence item.

## Target slice

Add `docs/evaluation/phase12-pressure-state-registration.json` and a parity
test that records:

- the current shared pressure-state IDs and visible trigger fields;
- exact overlay, status, event-cue, and music source IDs where applicable;
- written equivalents, non-color/reduced-motion behavior, and optional-audio
  boundaries;
- the empty campaign-specific pressure-state registration set; and
- explicit limits for future taxonomy, tutorial, direct audio mapping,
  screenshots, quality, and human review.

## Assumptions

- Registration is a catalog/evidence decision, not a new runtime vocabulary;
  no hidden severity, intent, probability, or future outcome is inferred.
- Event cues and music states are eligible presentation channels, not proof
  that every campaign-coverage envelope maps them directly.
- Existing unknown/fallback behavior remains the safe path for any future ID.

## Minimal implementation plan

1. Add the pressure-state registration ledger and source-parity test.
2. Check only the current shared pressure-state registration evidence in the
  Phase 12.1 roadmap and synchronize canonical docs, lessons, version metadata,
  generated credits, and additive request/contract/QA/handoff records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
  offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
  branch locally/remotely, and reassess the next roadmap item.

## Non-goals

- Do not add new pressure mechanics, hidden-state fields, campaign-specific
  states, audio mapping, tutorial copy, animation, assets, screenshots,
  instructor views, persistence, or human evaluation.
- Do not call the current shared taxonomy a complete Phase 12 pressure design.

## Stop conditions

Stop if a new state requires simulation semantics, a hidden-state projection,
new campaign content, direct audio mapping, asset promotion, quality judgment,
or human review.

## Risk label

Risk: low

Reason: The slice binds existing actor-visible presentation catalogs with
machine-checked source parity and no runtime changes.
