# Request Summary - Active Projects Display Hardening

## Phase / Gate
Phase 6.0/6.1/7: Competitive Campaign Hardening (Track 1)

## Scope
Enhance the active projects display in the competitive campaign's executive report dashboard.
- Instead of the generic `In-flight: 1 active project(s)`, show details of each project: project kind, remaining months to completion, and monthly cash draw.
- E.g., `In-flight: ClinicNetwork (8 mos left, $2k/mo draw)`.
- If multiple, display separated by commas (e.g. `ClinicNetwork (8 mos left, $2k/mo draw), Tower (11 mos left, $10k/mo draw)`).
- If none, display `none`.
- Update `observe_for_human` in `src/sim/observe_competitive.rs` to extract these details from the `effect_queue`.
- Keep existing game rules, stabilization campaigns, and other CLI aspects unchanged.

## Non-Goals
- No changes to stabilization campaign loop rules.
- No changes to competitive transition engine rules.
- No changes to database/serialization format for saved sessions or replays.

## Sources
- `docs/roadmap.md` §6.0, 6.1
- `src/sim/observe_competitive.rs`
- `src/cli/display/executive_report.rs`

## Expected Files to Change
- `src/sim/observe_competitive.rs`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
