# Request Summary - Exemplary Scenario Authoring Plan (Phase 6.2)

## Scope
Draft an exemplary scenario brief at `docs/exemplary-scenario-brief.md` that models a mid-sized regional healthcare market containing:
1. **Financial Pressure:** Declining margins or cash flow squeeze due to shifting payer rates or high fixed operating costs.
2. **Workforce Conflict:** Nurses bargaining or strike threat over staffing ratios and burnout.
3. **Payer provider rate negotiations:** Negotiation with a dominant commercial payer.
4. **Competitive Response:** Simultaneous capacity expansion or service line poaching by a rival health system.
5. **Policy / Regulatory process:** Certificate of Need (CON) review for facility expansion, or health department policy intervention.
6. **Delayed consequences:** Long-term reputation effects, lagged effects of EHR rollout, or worker strike consequences.
7. **Debrief hooks:** Educational reflection prompts distinguishing decision quality from luck and rival behavior.
8. **Defensible strategic directions:** At least two viable, contrasting strategies for Riverside Community Health (e.g., Access Safety Net Defense vs. Fiscal Preservation/Market Consolidation).

## Non-Goals
- No changes to simulation code or Rust codebase.
- No scenario loader or TOML parser modifications.
- No changes to existing scenario fixtures (e.g. `scenarios/stabilization-v1.toml`).
- No drive-by refactoring of unrelated documents.

## Sources
- `SPEC.md` Track 2 (Exemplary scenario authoring plan)
- `docs/first-scenario-brief.md`
- `docs/competitive-scenario-brief.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`

## Expected Files
- `docs/exemplary-scenario-brief.md`

## Validation Target
- Domain review confirms scenario elements, observations, learning purpose, and non-goals.
- Existing codebase compiles and all tests pass (`cargo test`).
