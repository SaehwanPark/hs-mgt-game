# Implementation Plan — Phase 12 stabilization tutorial presentation v0.13.25

## Task restatement

Continue Phase 12 with a bounded record of the current stabilization tutorial
presentation. Bind the existing CLI beginner menu and guide to explicit
visible tutorial fields, while distinguishing that current evidence from a
future browser-native stabilization tutorial.

## Current understanding

- `src/cli/beginner.rs` already presents five-turn guided choices with labels,
  pros, cons, trade-offs, recommendability, and host-owned commands.
- `docs/guides/how-to-play.md` explains the stabilization flow and beginner
  entry path.
- The GUI campaign-coverage surface can render stabilization data through the
  shared adapter contract, but the live GUI launcher remains competitive-only;
  no stabilization tutorial rail is currently integrated there.

## Target slice

Add `docs/evaluation/phase12-stabilization-tutorial-presentation.json` and a
parity test that records:

- the current five-turn beginner presentation fields and source markers;
- guide and beginner-test evidence;
- the shared GUI coverage boundary and current live-launch limitation;
- the written-equivalent and host-authority boundary; and
- open work for a browser-native stabilization tutorial, direct audio, richer
  campaign-specific content, quality, and human review.

## Assumptions

- This is current tutorial evidence, not a new tutorial implementation.
- Beginner recommendations are presentation metadata, not an optimal policy
  claim; commands and outcomes remain core/host-owned.
- No new tutorial copy, runtime route, asset, audio, or authority path is
  required for this evidence slice.

## Minimal implementation plan

1. Add the tutorial presentation ledger and source-parity test.
2. Check only current stabilization tutorial-presentation evidence in Phase
   12.1 and synchronize canonical docs, lessons, version metadata, generated
   credits, and additive request/contract/QA/handoff records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next roadmap item.

## Non-goals

- Do not add a browser stabilization launcher/tutorial rail, new tutorial
  content, audio mapping, animation, assets, screenshots, persistence,
  instructor views, or human evaluation.
- Do not call the existing CLI beginner flow a complete visual/audio tutorial
  or a human learning result.

## Stop conditions

Stop if evidence requires new campaign content, live GUI integration, a new
authority path, asset promotion, direct audio mapping, quality judgment, or
human review.

## Risk label

Risk: low

Reason: The slice records existing guided-presentation sources and their
browser boundary with machine-checked parity and no runtime changes.
