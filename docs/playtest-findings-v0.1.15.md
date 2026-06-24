# Internal Playtest Findings (v0.1.15)

**Date:** 2026-06-24  
**Slice:** Four-turn regional-market stabilization demo with replay artifact export

## Sessions

| Session | Play mode | Seed | Result |
| --- | --- | --- | --- |
| Preset path 1 | Access stabilization | 42 | Completed four turns; replay verified |
| Interactive defaults | Interactive (default commands) | 42 | Completed four turns; identical final state to preset path 1 |

## Comprehensibility

- The starting executive dashboard gives enough context to understand cash,
  capacity, access, trust, and policy pressure before choosing a play mode.
- Strategy previews help compare preset commitments without revealing future
  actor outcomes.
- Interactive turn briefings separate reported access, policy briefing, and prior
  measurement revisions clearly.
- Turn-resolution summaries are short enough to scan while preserving actor
  rationale and state hash per turn.
- The export prompt is unobtrusive when skipped and confirms the written path
  when used.

## Strategic Tension

- Access stabilization at seed `42` trades cash (100 → 46) for access gains
  (70 → 83) while preserving mixed stakeholder outcomes.
- Payer negotiation rejects the aggressive rate request despite adequate reported
  access, creating a finance/access tension without invalidating the command.
- Workforce and coalition turns reward credible commitments but still consume
  scarce cash.
- Observation revisions on later turns reinforce that decisions were made under
  incomplete and revisable information.

## Debrief Usefulness

- The debrief distinguishes actor rationales, attributed mechanisms, and the
  decision-quality versus outcome-quality prompt.
- Revision notes explain why later briefings differ without rewriting committed
  history.
- Exported replay artifacts preserve enough committed transition detail to
  reproduce and verify the run outside the interactive session.

## Confusion Points and Exploits

- Numeric command entry requires reading the default hint line; posture menus
  remain deferred.
- The additional export prompt adds one more CLI step after every run, though
  empty input preserves the prior skip behavior.
- No dominant exploit observed in the bounded four-turn slice at seed `42`.

## Recommended Next Slice

- Add Phase 0 CI (`cargo fmt --check` and `cargo test`) before broader
  contributor onboarding.
- Split the simulation core out of `src/main.rs` now that replay artifacts
  create a second consumer of committed history.
