# Implementation Plan — Phase 12.3 true-state language boundary v0.13.39

## Task restatement

Close the current Phase 12.3 evidence item for distinct true-state and
player-visible language by recording the existing textual labels and authority
boundary. Keep any browser-native true-state visual language as separately open
work.

## Current understanding

- The existing CLI debrief uses explicit `Observed`, `True Prior`, and `True
  Outcome` labels when the instructor appendix is available.
- Unobserved competitive details are marked `REVEALED FOR INSTRUCTOR REVIEW`.
- The host/core report owns the distinction; shared GUI renderers display
  supplied text and the live launcher remains competitive-only.
- Existing evidence distinguishes decision quality from outcome quality, but it
  does not establish a browser-native visual language or a human usability
  result.

## Target slice

Add `docs/evaluation/phase12-true-state-language-boundary.json` and a parity
test that record:

- source-linked observed, true-state, instructor-only, and decision-quality
  labels;
- campaign/host/browser/written fallback boundaries;
- the absence of a new true-state field, route, control, asset, or authority
  path; and
- the remaining browser, causal, counterfactual, distributional, export, and
  human educational review work.

## Assumptions

- “Distinct language” means the current technical textual boundary is explicit
  and source-verifiable; it is not a claim that a complete visual design exists.
- True-state labels remain post-run/instructor-only where the current contract
  permits them and are not promoted into live actor observation or controls.
- Written labels remain the fallback when audio or visual decoration is absent.

## Minimal implementation plan

1. Add the true-state language-boundary ledger and source-parity test.
2. Check the Phase 12.3 item and synchronize canonical docs, lessons, version
   metadata, generated credits, and additive request/contract/QA/handoff
   records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next Phase 12.3 item.

## Non-goals

- Do not add browser-native true-state views, routes, fields, controls,
  persistence, screenshots, assets, audio files, counterfactuals,
  distributional charts, export formats, or educational claims.
- Do not expose resolved inputs or private actor rationale in live player
  observations.

## Stop conditions

Stop if the existing labels cannot be separated into player-visible, true-state
post-run, and instructor-only language without expanding authority or implying
human comprehension.

## Risk label

Risk: low

Reason: The slice records and tests existing source boundaries only; it adds no
runtime state or presentation authority.
