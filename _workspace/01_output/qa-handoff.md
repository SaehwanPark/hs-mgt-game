# QA Handoff Checklist - Exemplary Competitive Scenario & Timeline Events

This document details the implementation of the `competitive-exemplary-v1` scenario, including its timeline events, delayed consequences, and the RNA strike / CON challenge mechanics.

## Verified Scope
- **Scenario File Created:** [scenarios/competitive-exemplary-v1.toml](file:///Users/saehwan/repos/hs-mgt-game/scenarios/competitive-exemplary-v1.toml) defines the starting parameters for:
  - Riverside Community Health (Human, cash=500, political_capital=4, staffed_beds=118)
  - Northlake Health (AI, growth style, cash=1200, political_capital=2, staffed_beds=132)
  - Summit Care (AI, margin style, cash=900, political_capital=2, staffed_beds=104)
- **Workforce Wage Commit Verb:** Players can run `commit pledge_type=workforce level=1` to accept the nurse wage increase and settle the labor dispute, setting the metadata flag `rna_wage_increase_accepted` to true.
- **Burnout & Strike Warning (Month 8):** If Riverside's staffing ratio falls below 80% (fewer than 24 nurses for 118 beds), trust drops by 15% and a strike warning triggers.
- **Active Strike & CON Legal Objection (Month 10):** If wages were not increased, an active strike starts. Riverside capacity is halved, travel nurse costs of $30/month are deducted, and capital projects are delayed. Additionally, if clinic builds are in progress, Northlake files a CON objection which requires 3 PC or $100 cash to bypass, or delays the project by 3 months.
- **Blue Shield Contract Renewal (Month 12):** If the player does not execute `negotiate payer=carrier_a`, Riverside goes out-of-network with Blue Shield, decreasing commercial patient volume by 40% (reflected in `market_share_index` drop).
- **Delayed EHR & Strike Consequences (Month 18):** If the strike occurred, community trust drops by 20% and market share by 10%. If EHR migration was underfunded (not started by Month 15), operational efficiency drops, costing $20/month.

## Verification Checklist
- [x] Scenario file parses and validates successfully: `test_load_exemplary_competitive_scenario` passes.
- [x] Month 8 burnout and strike warning triggers: `test_exemplary_scenario_timeline_month8_burnout_and_strike_warning` passes.
- [x] Workforce wage commitment settles dispute: `test_exemplary_scenario_timeline_workforce_wage_commitment` passes.
- [x] Month 10 strike active limits and CON legal challenge: `test_exemplary_scenario_timeline_month10_strike_and_con_objection` passes.
- [x] Month 12 Blue Shield and Month 18 EHR lag consequences: `test_exemplary_scenario_timeline_month12_blue_shield_renewal_and_month18_ehr_lag` passes.
- [x] Entire game test suite runs and compiles successfully: `cargo test` passes all 260 tests.

## Version Bump
- Package version bumped to `0.5.6` in `Cargo.toml`.
- Added release notes for `0.5.6` in `CHANGELOG.md` and `SPEC.md`.
