# Internal Playtest Findings (v0.1.25)

**Date:** 2026-06-24  
**Slice:** Five-turn demo with forecast/uncertainty preview at v0.1.25  
**Codebase:** Library modules; 86 tests; GitHub Actions CI

## Sessions

| Session | Play mode | Seed | Result |
| --- | --- | --- | --- |
| Preset path 1 | Access stabilization | 42 | Completed five turns; replay verified; trajectory unchanged |
| Interactive defaults | Interactive (default commands) | 42 | Uncertainty preview shown each turn; identical final state to preset path 1 |

Golden final state hash at seed 42 (preset path 1 / interactive defaults):
`6fb1ebbea564274f` — unchanged from v0.1.21.

## Forecast Preview

- Interactive mode prints uncertainty preview before each executive briefing.
- Preview surfaces reported access, cash/spend bounds, policy pressure, and market
  context without rival or payer decision outcomes.
- Starting dashboard adds observation uncertainty note for pre-run context.

## Recommended Next Slice

External playtest protocol refresh or scenario loader after format draft review.
