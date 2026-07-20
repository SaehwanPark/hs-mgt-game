# Presentation Contract — Phase 6.1 motion specification v0.12.68

## Goal and authorization

Specify restrained motion that can make visible consequence order easier to
follow without allowing client timing to become a second transition authority.

## Motion source ledger

| Category | Visible trigger/source | Allowed presentation |
| --- | --- | --- |
| Focus transition | Local selected visible target | Focus emphasis only; no state change |
| Report arrival | Actor-visible report insertion | Attention cue plus written report/source/status |
| Month transition | Host-committed month marker | Local orientation after committed text is available |
| Project progress | Host-reported progress field | Emphasize reported progress; no interpolation/promise |
| Project completion | Host-reported completion | Emphasize conclusion; do not predict completion |
| New visible rival action | Public observed action/timing | Emphasize public signal; retain private-detail boundary |
| Status change | Visible status label/pattern | Emphasize label; add no severity |
| Metric delta reveal | Explicit before/after/delta text | Emphasize exact values; do not recompute |
| Relationship-line change | Explicit visible line/pattern update | Emphasize visible pattern; infer no direction/cause |

## Motion contract

- `gui/motion-catalog.mjs` is the single catalog. Every entry defines semantic
  purpose, duration, easing, reduced-motion replacement, interruption,
  replay, input, deterministic order, and a declared frame budget.
- `MOTION_POLICY` caps simultaneous effects at three, sets a 16 ms declared
  frame budget, requires deterministic batch/sequence/category/target order,
  and states that motion never owns focus or blocks host input.
- `replayMotionSequence` returns immutable local plans. Reduced motion sets
  duration to zero and supplies the same-information static replacement.
- `interruptMotion` reports a local replacement while explicitly retaining
  written information and leaving host state unchanged.
- `gui/motion-proof.html` demonstrates the policy without timers, animation,
  network, host calls, or simulation state.

## Accessibility and fallback requirements

- Motion is supplementary; visible text, source/status, exact values, focus
  semantics, and keyboard input remain available without it.
- Reduced-motion replacement is immediate and static. Interrupting an effect
  never removes its report, metric, status, or consequence text.
- The proof’s print and responsive layout retains the complete catalog and
  evidence limits; no animation is required for comprehension.

## Authority, history, and replay boundaries

The catalog accepts explicit local motion events only. It does not call a host,
submit a command, mutate simulation state, resolve stochastic inputs, rewrite
history, change a state hash, reveal hidden information, or create audio or
debrief facts. Replay order is a presentation plan, not replay authority.

## Asset provenance and verification

`visual.runtime-motion-catalog` is a project-generated registry-approved
semantic asset with source hash, visible-source description, accessible
equivalent, and no release image. Focused catalog/proof tests include a local
performance-budget smoke check; full Python/Rust, formatting,
registry/credits/metadata, documentation, presentation-contract, and diff
checks are required before merge.

## Non-goals and next gate

This slice does not add CSS/JS runtime animation, host sequencing, audio
synchronization, metric transitions, browser performance measurement, or a
first-month resolution sequence. Later Phase 6.2 owns the first-month sequence.
