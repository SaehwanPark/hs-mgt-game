# Mechanism Design - Competitive Campaign Length & Autosave

## State Boundary & Serialization
Create `CompetitiveSessionSave` representing the persistent state of a competitive campaign:
- `ruleset_version: String`
- `seed: u64`
- `difficulty: Difficulty`
- `history: CompetitiveHistory`
- `next_month: u32`

Define custom serialization and deserialization in a new file `src/artifact/competitive_session_save.rs` with:
- Header: `competitive-session-save-0.3.3`
- Serialized representation of `Difficulty` and `CompetitiveWorldState` / `CompetitiveHistory`.
- Integration into `src/artifact/mod.rs`.

## Persistence Layer
Expose functions in `src/cli/persistence.rs` for:
- Path: `.config/hs-mgt-game/competitive_session.save`
- `competitive_session_save_path() -> PathBuf`
- `load_competitive_session_save(ruleset: &CompetitiveRuleset) -> Result<CompetitiveSessionSave, SessionSaveError>`
- `write_competitive_session_save(save: &CompetitiveSessionSave) -> Result<(), SessionSaveError>`
- `delete_competitive_session_save() -> Result<(), SessionSaveError>`

## Loop Control & UX
1. Extend default campaigns: In `src/cli/campaign.rs`, set `COMPETITIVE_CAMPAIGN_MONTHS = 24`.
2. Update `run_competitive_month_loop` to run for `COMPETITIVE_CAMPAIGN_MONTHS`.
3. Detect early-quit (`q` or `quit` inputs) and serialize history/state to `competitive_session.save`.
4. Relaunch menu: Update `select_campaign` or the startup logic in `src/cli/session.rs` to detect both `session.save` (stabilization) and `competitive_session.save` (competitive) and present appropriate options to resume or start fresh.
5. Replay Export: Add options to output `competitive-replay-*.json` on completion.
