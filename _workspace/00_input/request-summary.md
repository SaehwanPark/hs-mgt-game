# Request Summary - Difficulty Expansion v0.11.7

## Scope

- Implement a structured difficulty parameter system that makes difficulty levels institutionally expressive.
- Introduce an explicit `RiskPosture` enum (`Conservative`, `Moderate`, `Aggressive`) representing the AI's strategic risk-taking profile.
- Add `risk_posture` field to `AiProfile` and `RivalTemplate` to configure each AI system.
- Map the active game `Difficulty` to initial AI risk postures at genesis (Easy -> Conservative, Normal -> Moderate, Hard/Expert -> Aggressive).
- Update AI batch computation logic in `src/actors/ai_player.rs` to adjust scoring weights based on the active `RiskPosture` (e.g., conservative AI players penalize aggressive negotiations and large capital investments, while aggressive AI players boost aggressive rate posturing and large capital investments, and have higher cash thresholds).
- Preserve backwards compatibility for JSON serialization of saved sessions, keeping competitive state hashes invariant.
- Complete the feature branch setup, verification, PR handoff, and review loop.

## Non-goals

- No broad balance pass, hidden rival omniscience, or punitive player AP/resource cuts.
- No changes to the state-hash schema or serialization formats that break compatibility with existing save states.
- No changes to the core transition kernel or the public observation boundaries.
- No causal or policy-validity claims.

## Sources

- `docs/expansion-proposal-review.md` (Proposal 1: Difficulty Expansion)
- `SPEC.md` (Ranked next-development queue - Track 2: Difficulty depth and winnability)
- `docs/roadmap.md` (Phase 7 validation and educational gates)

## Expected files

- Updated `src/model/campaign.rs` (defining `RiskPosture`).
- Updated `src/model/competitive_world.rs` (adding `risk_posture` to `AiProfile` and updating serialization).
- Updated `src/competitive/genesis.rs` (initializing `risk_posture` based on `Difficulty`).
- Updated `src/scenario/mod.rs` (populating `risk_posture` from difficulty when loading AI systems).
- Updated `src/actors/ai_player.rs` (implementing risk-posture scoring modifiers in `score_command` and rationales).
- Updated `Cargo.toml`, `CHANGELOG.md`, `SPEC.md`, and workspace files.

## Validation target

- All 291 Rust tests and 138 Python tests pass.
- Focused unit tests verifying risk-posture behavior under Conservative, Moderate, and Aggressive profiles.
- Replay and golden seed-42 tests continue to pass (with state-hash invariance verified).
