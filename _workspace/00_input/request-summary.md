# Request Summary - Competitive Campaign Length & Autosave

## Scope
Extend the competitive regional campaign loop to 24 months, implement autosave/resume logic via `competitive_session.save`, and add competitive replay export on completion.

Specifically:
- Extend campaign loop length: change default preview to a 24-month horizon.
- Autosave/resume:
  - Add path and load/write/delete helpers for `competitive_session.save` in `src/cli/persistence.rs`.
  - Create serializable `CompetitiveSessionSave` structure.
  - Intercept early quit in `run_competitive_month_loop` and save active campaign.
  - Check for competitive autosave on CLI REPL startup and offer resume menu option.
- Replay export:
  - Support exporting competitive replay JSON artifact upon successful completion.

## Non-Goals
- No changes to stabilization campaign rules, loop, or save file.
- No network multiplayer capabilities.
- No database integration.

## Sources
- `src/cli/campaign.rs`
- `src/cli/persistence.rs`
- `src/cli/session.rs`
- `src/model/session_save.rs`

## Expected Files
- `src/model/competitive_session_save.rs` (or added to `session_save.rs`)
- `src/artifact/competitive_session_save.rs`
- `src/cli/persistence.rs`
- `src/cli/campaign.rs`
- `src/cli/session.rs`
- `Cargo.toml`
- `CHANGELOG.md`
- `SPEC.md`
