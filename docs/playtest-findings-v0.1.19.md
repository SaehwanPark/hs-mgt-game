# Internal Playtest Findings (v0.1.19)

**Date:** 2026-06-24  
**Slice:** Four-turn regional-market stabilization demo at v0.1.19  
**Codebase:** Library modules under `src/lib.rs`; 78 tests; GitHub Actions CI

## Sessions

| Session | Play mode | Seed | Result |
| --- | --- | --- | --- |
| Preset path 1 | Access stabilization | 42 | Completed four turns; replay verified |
| Interactive defaults | Interactive (default commands) | 42 | Completed four turns; identical final state to preset path 1 |
| Preset path 2 | Fiscal caution | 42 | Verified via strategy/replay tests at seed 42 |
| Preset path 3 | Aggressive bargaining | 42 | Verified via strategy/replay tests at seed 42 |

Golden final state hash at seed 42 (preset path 1 / interactive defaults):
`bce02dff9b4b4ac6` — unchanged since module refactor and test colocation.

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
- Module boundaries (`model`, `sim`, `actors`, `cli`, etc.) do not affect player
  CLI flow; behavior matches pre-refactor v0.1.15 sessions.

## Strategic Tension

- Access stabilization at seed `42` trades cash (100 → 46) for access gains
  (70 → 83) while preserving mixed stakeholder outcomes.
- Payer negotiation can reject aggressive rate requests despite adequate reported
  access, creating a finance/access tension without invalidating the command.
- Workforce and coalition turns reward credible commitments but still consume
  scarce cash.
- Observation revisions on later turns reinforce that decisions were made under
  incomplete and revisable information.
- Fiscal caution and aggressive bargaining preset paths produce distinct insurer
  and policy outcomes, supporting multiple defensible strategy discussions.

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
- No dedicated forecast display; uncertainty is conveyed through observations and
  revisions rather than explicit probability forecasts.
- No dominant exploit observed in the bounded four-turn slice at seed `42`.

## Infrastructure notes (v0.1.16–v0.1.18)

- Simulation logic lives in library modules; `main.rs` is a thin entry point.
- 77 colocated unit tests plus one golden integration test in
  `tests/golden_seed42.rs`.
- CI runs `cargo fmt --check` and `cargo test` on pushes to `main` and PRs.

## Recommended Next Slice

Per README contributor priorities:

1. Phase 1 research-to-design implications memo.
2. Competitor actor card and bounded fifth-turn competitive interaction runtime
   slice.
3. Phase 0 governance docs: glossary, decision-record conventions, versioning
   policy.
