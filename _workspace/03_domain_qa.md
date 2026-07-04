# Domain QA - Clinical Service Lines and Staffing (Phase 6 - Track 5)

## Review Status: PENDING IMPLEMENTATION

## Project-Specific Checks
- **Determinism Check:** The staffing calculation, effective capacity, and burnout formulas are completely deterministic, satisfying the core engine design boundary.
- **State vs. Observation Separation:** Physical capacities and headcounts are true state variables. The executive report will present reported access/quality (which can be noisy or lagged) alongside current headcounts and capacity indicators.
- **Strategic Tradeoffs:** Ensures high capital spend on expansion projects must be balanced with appropriate timing of recruitment (and its associated delay & cash costs) to avoid understaffing penalties.
- **Simple Code Writing:** Avoids adding a general staffing framework. Implements simple formulas directly in `effects_competitive.rs` and `transition_competitive.rs`.

## Validation Targets for Implementer
- Verify that standard recruitment delays (1 month for nurses, 3 months for physicians) are preserved.
- Verify that the game loop resolves recruitments correctly and updates `nurses` and `physicians` fields.
- Ensure that the CLI dashboard and executive reports display the new staffing headcounts and capacity constraints clearly.
