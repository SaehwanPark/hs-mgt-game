# QA Handoff Checklist - Exemplary Competitive Scenario & Timeline Events

This document details the implementation of the `competitive-exemplary-v1` scenario, including its timeline events, delayed consequences, and the RNA strike / CON challenge mechanics.

## Verified Scope
- **Scenario File Created:** [scenarios/competitive-exemplary-v1.toml](../../scenarios/competitive-exemplary-v1.toml) defines the starting parameters for:
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

---

# QA Handoff — GUI task workspace redesign v0.14.1

## Changed files

`gui/index.html`, `gui/app.mjs`, `gui/first-month.mjs`, new
`gui/workspace.mjs`, `src/gui_server.rs`, loading/offline manifests, focused
GUI tests, canonical docs, version metadata, and append-only presentation
artifacts.

## Verification target

Run Node syntax, focused/full Python tests, loading/offline/documentation and
release checks, `cargo fmt --check`, `cargo clippy --all-targets -- -D
warnings`, and `cargo test`. Host-backed campaign workflows must retain the
existing command, envelope, transition, history, replay, checkpoint, and
debrief behavior.

## Residual risk

No authorized human pilot or real browser/device layout matrix has been run in
this handoff. Treat the redesign as technically verified and pending human
cognitive-load/accessibility/usability validation. PR3 asset generation remains
conditional on recorded repeated findings and provenance/licensing approval.

## Final verification addendum — v0.14.1

- Full Python suite: 939 passed; Rust `cargo test`, `cargo fmt --check`, and
  `cargo clippy --all-targets -- -D warnings` passed.
- Embedded smoke served the shell, `/workspace.mjs`, and host session creation;
  release, documentation, loading/offline, device-proxy, syntax, and diff
  checks passed.
- Residual risk is unchanged: no browser layout certification or authorized
  human cognitive-load/usability result is claimed.

### Word-sized wrapping correction

The follow-up screenshot defect is addressed with stable timeline grid tracks,
word-boundary label wrapping, and a narrow-screen status row. The correction is
presentation-only and adds no host or asset contract.

### Actor and overlay follow-up

Long actor summaries now render as readable text below the actor heading, and
overlay/process marker labels cannot collapse to character-per-line pills.

### Overlay track sizing correction

Browser reproduction found the long intelligence value could still consume the
entire `auto` grid track and leave the marker/title track at zero width. The
regional overlay list now uses two flexible columns, preserving readable
word-sized heading and value wrapping. Device source remains within the
`445000`-byte proxy limit (`444994` bytes measured).

The refreshed verification run passes all 941 Python tests plus Node syntax,
release/documentation, loading/offline, device-proxy, formatting, clippy, and
Rust test checks.

## Unified draft contextual actions v0.14.2

The QA target is one host-ordered `Actions` surface for all three campaign
types, with competitive `Monthly plan` validation and direct-card submission.
Review must preserve canonical batches, host authority, rejection recovery,
Details accessibility, focus/live-region behavior, live technical-control
visibility, and the 445,000-byte source proxy. Human usability/accessibility
and browser/device certification remain open gates.
