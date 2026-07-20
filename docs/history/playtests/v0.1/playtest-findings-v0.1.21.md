# Internal Playtest Findings (v0.1.21)

**Date:** 2026-06-24  
**Slice:** Five-turn regional-market stabilization demo at v0.1.21  
**Codebase:** Library modules; 82 tests; GitHub Actions CI

## Sessions

| Session | Play mode | Seed | Result |
| --- | --- | --- | --- |
| Preset path 1 | Access stabilization | 42 | Completed five turns; replay verified |
| Interactive defaults | Interactive (default commands) | 42 | Completed five turns; identical final state to preset path 1 |
| Preset path 2 | Fiscal caution | 42 | Verified via strategy/replay tests at seed 42 |
| Preset path 3 | Aggressive bargaining | 42 | Verified via strategy/replay tests at seed 42 |

Golden final state hash at seed 42 (preset path 1 / interactive defaults):
`6fb1ebbea564274f` — turn 4 hash unchanged at `bce02dff9b4b4ac6`.

## Competitor Turn

- Turn 5 briefing surfaces market competition context without revealing
  competitor decision outcomes.
- Access stabilization at seed 42 triggers competitor partial retreat after
  strong defensive capital and access posture.
- Aggressive bargaining path triggers competitor accelerate expansion on turn 5.

## Recommended Next Slice

**Superseded at v0.1.22.** Phase 0 governance docs (glossary, decision-record
conventions, versioning policy) shipped in `feat/phase0-governance-docs`.

See [`phase5-scope-register.md`](../../foundations/phase5-scope-register.md) for current deferred
items and hardening priorities (forecast preview, scenario format design).
