# Operational Coding Plan - Difficulty Expansion v0.11.7

## Task restatement

Implement an institutionally expressive difficulty system (difficulty expansion) by introducing AI risk postures that affect action selection and rationales, while preserving backwards compatibility, existing state-hash schemas, and public observation boundaries.

## Current understanding

- AI decision-making lives in `src/actors/ai_player.rs` within `compute_ai_batch` and `score_command`.
- AI configurations are represented by `AiProfile` and `AiStyleWeights` in `src/model/competitive_world.rs`.
- `PlayerController` serialization/deserialization helper `RawPlayerController` handles JSON persistence and can be extended backward-compatibly.
- State hashes are defined in `src/model/competitive_hash.rs` and do not include the AI players' profile structures, so state hash invariance is preserved if JSON serializations remain compatible.
- The `Difficulty` enum lives in `src/model/campaign.rs` and currently sets rival counts (K) and AP budgets, but doesn't influence strategic weights or decision postures directly.

## Assumptions

- Hashing of `PlayerController` or its fields is not used in `competitive_state_hash_record`.
- The current seed-42 Normal baseline remains stable if we default to the current `Moderate` behavior.
- Scenario loading (`src/scenario/mod.rs`) initializes controllers and can map difficulty to the corresponding risk posture.

If any assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1. **Define Risk Posture Enum**:
   - In `src/model/campaign.rs`, add `RiskPosture` enum:
     ```rust
     #[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
     pub enum RiskPosture {
       Conservative,
       Moderate,
       Aggressive,
     }
     ```
2. **Update AiProfile and Serialization**:
   - In `src/model/competitive_world.rs`, add `pub risk_posture: RiskPosture` to `AiProfile`.
   - Update `PlayerController` serialization/deserialization to support `risk_posture`. In the deserialize helper `RawPlayerController::Ai`, make `risk_posture` optional (e.g. `#[serde(default)]`) and default to `RiskPosture::Moderate` to maintain full backwards compatibility with existing JSON saves.
3. **Genesis & Template Setup**:
   - In `src/competitive/genesis.rs`, add `pub risk_posture: RiskPosture` to `RivalTemplate`. Initialize the template constants (e.g. `NORTHLAKE`, `SUMMIT`, etc.) with default/logical risk postures (e.g. `Moderate` or specific styles).
   - Update `genesis_competitive_world_with_ruleset` to initialize `AiProfile::risk_posture` dynamically based on the active `difficulty`:
     - `Difficulty::Easy` -> `RiskPosture::Conservative`
     - `Difficulty::Normal` -> `RiskPosture::Moderate`
     - `Difficulty::Hard` | `Difficulty::Expert` -> `RiskPosture::Aggressive`
4. **Scenario Loading Integration**:
   - In `src/scenario/mod.rs`, update scenario AI system setup to initialize `risk_posture` from the active difficulty (mapping Easy -> Conservative, Normal -> Moderate, Hard/Expert -> Aggressive).
5. **AI Scoring and Decision Logic**:
   - In `src/actors/ai_player.rs`, pass `risk_posture` into `score_command` and adjust scoring weights:
     - **Conservative**:
       - Penalize `RatePosture::Aggressive` by `-10`.
       - Penalize `Invest` commands with `amount > 20` by `-5`.
       - Boost `Hold` command by `+3`.
     - **Aggressive**:
       - Boost `RatePosture::Aggressive` by `+5`.
       - Boost `Invest` commands with `amount > 20` by `+5`.
       - Reduce the `cash_pressure` penalty by `+4` (reducing it from `-8` to `-4`).
     - **Moderate**: No adjustments (default baseline behavior).
   - Update `compute_ai_batch` to format the risk posture into the generated AI rationale string (e.g., `"{} ({}, {:?}) — ..."`).
6. **Verification and Package Bump**:
   - Add focused unit tests in `src/actors/ai_player.rs` to verify that scoring behaves correctly under all three risk postures.
   - Bump project version to `0.11.7` in `Cargo.toml`.
   - Update `CHANGELOG.md` and `SPEC.md`.

## Files and functions likely to change

- `src/model/campaign.rs`: Define `RiskPosture` enum.
- `src/model/competitive_world.rs`: Add `risk_posture` to `AiProfile`, update `PlayerController` serialization.
- `src/competitive/genesis.rs`: Add `risk_posture` to `RivalTemplate`, update `genesis_competitive_world_with_ruleset`.
- `src/scenario/mod.rs`: Update `PlayerController::Ai` initialization from scenario.
- `src/actors/ai_player.rs`: Pass `risk_posture` to `score_command`, implement scoring offsets, update rationales, add unit tests.
- `Cargo.toml`: Bump version to `0.11.7`.

Avoid editing files outside this list unless the plan is found to be incomplete. If that happens, stop and explain why.

## Tests and checks

Run the complete test suite:
- `cargo test --all`
- `python3 -m unittest discover -s tests -p "test_*.py"`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`

Expected result:
- All 291 Rust tests and 138 Python tests pass.
- Formatting and clippy checks pass.
- Seed-42 Normal golden hashes and tests match exactly.

If tests fail:
1. Fix failures directly related to this change.
2. Do not fix unrelated failures unless required to unblock validation.
3. Report unrelated failures separately.

## Acceptance criteria

- `RiskPosture` is introduced and configured correctly based on difficulty.
- AI players under different difficulty levels use different risk postures, modifying their choice scores.
- Rationale strings contain the selected risk posture.
- State-hash values for `Difficulty::Normal` remain invariant compared to the baseline.
- Backward compatibility with prior session save files is maintained (deserialization succeeds).

## Non-goals

- Do not change public API signatures outside `AiProfile`.
- Do not modify state-hash calculation logic.
- Do not introduce non-deterministic factors or external inputs.
- Do not balance the game parameters globally outside the specified risk posture offsets.

## Stop conditions

Stop and ask for review if:
- Adding `risk_posture` to `AiProfile` causes serialization mismatches in existing playtests or validation runs.
- The state hash changes for `Difficulty::Normal` seed-42, indicating a regression.
- The implementation requires editing more than 6 files.

## Review checklist

Before finalizing, verify:
- The diff implements only the requested risk-posture behavior.
- The change is covered by focused unit tests.
- Backward compatibility for session serialization is preserved.
- No unrelated formatting, renaming, or cleanup was introduced.
- Rationale strings are updated correctly.

## Risk label

Risk: Low

Reason: The changes are isolated to AI scoring weight offsets and setup logic, and they maintain full backwards compatibility for serialization with state hashes remaining invariant.
