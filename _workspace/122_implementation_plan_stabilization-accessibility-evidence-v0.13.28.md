# Implementation Plan — Phase 12 stabilization accessibility evidence v0.13.28

## Task restatement

Continue Phase 12 with a bounded record of current technical accessibility
contract checks relevant to stabilization presentation. Join existing keyboard,
focus, status-language, text-scale, reduced-motion, written-equivalent, audio-
fallback, and semantic-list tests without claiming lived accessibility.

## Current understanding

- `tests/test_gui_accessibility.py` checks landmarks, stable targets, text and
  non-color status language, text scale, cue explanations, focus/live-region
  semantics, boundary exclusions, JavaScript syntax, and local setting state.
- `tests/test_gui_first_month.py`, `tests/test_audio_fallback.py`, and the
  existing semantic/campaign tests cover written resolution/debrief retention,
  reduced-motion pacing, and optional-audio fallback.
- The live GUI launcher remains `competitive-regional-v1` only, so this is a
  shared technical presentation contract for possible stabilization data, not
  a live stabilization accessibility certification.

## Target slice

Add `docs/evaluation/phase12-stabilization-accessibility-evidence.json` and a
parity test that records:

- current technical accessibility checks and source markers;
- keyboard/focus, text/non-color status, text-scale, reduced-motion,
  written-equivalent, audio-fallback, and semantic-container coverage;
- local presentation-only settings and host/authority boundaries; and
- open work for browser-native stabilization integration, contrast/screen
  readers/devices, lived accessibility, and human review.

## Assumptions

- This is technical test evidence, not an accessibility-quality judgment.
- Current tests cover shared GUI contracts; they do not certify an unlaunched
  stabilization browser flow or a particular assistive technology.
- Written text remains the meaning-bearing fallback when audio, motion, storage,
  or browser capabilities are unavailable.

## Minimal implementation plan

1. Add the accessibility evidence ledger and source-parity test.
2. Check only current stabilization-relevant technical accessibility evidence
   in Phase 12.1 and synchronize canonical docs, lessons, version metadata,
   generated credits, and additive request/contract/QA/handoff records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next roadmap item.

## Non-goals

- Do not add a browser stabilization launcher, new accessibility behavior,
  route, runtime field, asset, audio file, screenshot, persistence, instructor
  view, screen-reader certification, device certification, or human study.
- Do not call technical proxies lived accessibility, contrast certification,
  assistive-technology compatibility, or educational usability.

## Stop conditions

Stop if the current technical checks cannot be source-linked without adding a
runtime authority path, a new stabilization flow, a quality judgment, or human
accessibility evidence.

## Risk label

Risk: low

Reason: The slice records existing shared GUI tests and their explicit limits;
it changes no client behavior, host contract, or simulation state.
