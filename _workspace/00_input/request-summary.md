# Request Summary - Workforce Parameter/Evidence Ledger (Phase 1/7 - Track 3)

## Scope
Create or extend a parameter/evidence ledger for one bounded mechanism. We select the **Nursing Workforce & Retention** mechanism (comprising nurse staffing ratios, recruitment delays, AP/cash costs, and workforce trust).
We will:
1. Identify all workforce-related parameters and formulas in both stabilization and competitive campaign models.
2. Link code variables and transitions to primary literature and precedents (e.g., California AB 394 safe staffing, Linda Aiken JAMA 2002 nurse burnout study, NSI 2026 RN Staffing Report).
3. Assign confidence labels based on the project ontology: `Empirically calibrated`, `Literature-grounded`, `Expert-informed`, `Stylized abstraction`, `Gameplay-driven`.
4. Document the ledger in `docs/workforce-ledger.md` and update `docs/evidence-registry.md` to reference it.
5. Bump the package version to `0.2.4`.

## Non-Goals
- No changes to simulation rules or parameter values in the codebase.
- No database or telemetry changes.
- No changes to existing scenario TOML files.

## Sources
- `SPEC.md` Track 3 (Evidence, parameters, and model-confidence ledger)
- `docs/evidence-registry.md`
- `src/actors/labor.rs`
- `src/sim/transition.rs`
- `src/sim/transition_competitive.rs`
- `src/model/competitive_command.rs`

## Expected Files
- `docs/workforce-ledger.md` (Created)
- `docs/evidence-registry.md` (Modified)
- `Cargo.toml` (Modified)
- `Cargo.lock` (Modified)
- `CHANGELOG.md` (Modified)
- `SPEC.md` (Modified)

## Validation Target
- All cargo tests pass successfully (`cargo test`).
- Formatting and clippy checks pass cleanly.
