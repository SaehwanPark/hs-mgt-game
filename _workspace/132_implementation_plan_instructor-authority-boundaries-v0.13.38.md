# Implementation Plan — Phase 12.3 instructor-only authority boundaries v0.13.38

## Task restatement

Begin Phase 12.3 with a bounded authority-boundary record for instructor and
true-state debrief surfaces. Document which existing CLI/host contracts may
contain post-run detail, which player-visible contracts remain observational,
and why the current live GUI does not claim a new instructor view.

## Current understanding

- Stabilization has an existing CLI instructor appendix that distinguishes
  reported player metrics from true underlying states; it is not a new route.
- Competitive debrief can reveal unobserved rival actions for post-run
  instructor evaluation through the existing host/core report.
- Regional affiliation has typed/CLI terminal debrief and replay detail but no
  separate instructor authority surface; browser campaign rendering remains
  text-first and the live launcher remains competitive-only.

## Target slice

Add `docs/evaluation/phase12-instructor-authority-boundaries.json` and a parity
test that record:

- existing instructor-only/privileged debrief sources by campaign;
- player-observation versus post-run detail boundary;
- host ownership, read-only browser rendering, live-GUI limitation, and
  written fallback; and
- no-new-surface, no-authority-expansion, no-counterfactual, and human-review
  limits.

## Assumptions

- “Documented” means source-linked current authority boundaries, not a claim
  that a new instructor product surface exists.
- Post-run CLI/typed detail may remain available to the existing contract, but
  it must not be presented as a live player observation or browser control.
- Human educational usability, visual design, and classroom effectiveness
  remain separate review gates.

## Minimal implementation plan

1. Add the instructor-authority boundary ledger and source-parity test.
2. Check the first Phase 12.3 item and synchronize canonical docs, lessons,
   version metadata, generated credits, and additive request/contract/QA/handoff
   records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next Phase 12.3 item.

## Non-goals

- Do not add instructor routes, true-state fields, counterfactuals,
  distributional views, persistence, screenshots, assets, audio files,
  authority paths, or educational claims.
- Do not expose resolved inputs or private actor rationale in live player
  observations or controls.

## Stop conditions

Stop if existing debrief sources cannot be separated into player-visible,
post-run CLI/typed, and not-yet-built instructor boundaries without expanding
authority or making a human-learning claim.

## Risk label

Risk: low

Reason: The slice documents existing source boundaries and explicitly records
the absence of a new instructor surface.
