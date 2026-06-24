# Phase 5 Scope and Risk Register

**Status:** Phase 5 closure artifact (refreshed)  
**Version:** v0.1.23  
**Date:** 2026-06-24  
**Audience:** Contributors, domain reviewers, and playtest designers

This register records what the first vertical slice achieved against
[`docs/roadmap.md`](roadmap.md) Phase 5, what remains intentionally deferred,
known risks, exit-criteria evidence, and recommended next slices.

## Scope Statement

The current executable is a five-turn regional-market stabilization demo at
v0.1.21+. It demonstrates deterministic transitions, seeded stochastic inputs,
strategic non-player actors, observation separation, replay verification, replay
artifact export, interactive CLI play, and educational debrief. It is a bounded
architecture and gameplay proof, not an MVP campaign or calibrated policy model.

## Achieved (roadmap §5.2–5.5)

### Interaction slice (§5.2)

| Requirement | Implementation | Evidence |
| --- | --- | --- |
| One payer negotiation | Turn 1 `StabilizeAccess` with commercial insurer accept/counter/reject | `src/actors/insurer.rs`, transition tests |
| One workforce or capacity pressure | Turn 3 `RespondToWorkforcePressure` with labor response | `src/actors/labor.rs` |
| One policy proposal with stakeholder response | Turn 2 `RespondToStateAccessMandate` with state policy decision | `src/actors/state_policy.rs` |
| One cooperative or coalition opportunity | Turn 4 `JoinRegionalAccessCoalition` with liaison decision | `src/actors/coalition.rs` |
| Competitive capacity interaction | Turn 5 `RespondToCompetitorCapacityMove` with rival system decision | `src/actors/competitor.rs`, transition tests |
| Delayed consequences across several turns | Cash, access, trust, and policy pressure carry across five turns | Golden seed-42 integration test, replay tests |

### Observation slice (§5.3)

| Requirement | Implementation | Evidence |
| --- | --- | --- |
| True versus reported measures | `observe` derives actor-visible reports from true state plus resolved inputs | `src/sim/observe.rs`, observation tests |
| Actor-specific information | Per-turn briefings use observation data, not future outcomes | `src/cli/display/briefing.rs`, briefing tests |
| Measurement delay or uncertainty | Named random streams perturb reported access | `src/inputs/resolve.rs`, resolver tests |
| Later revisions | Revision stream adds new briefing notes without rewriting history | `src/cli/strategy_tests.rs`, `src/debrief/report_tests.rs` |

### Playable CLI slice (§5.4)

| Requirement | Implementation | Evidence |
| --- | --- | --- |
| Concise executive dashboard | Starting dashboard before play-mode selection | `src/cli/display/dashboard.rs`, dashboard tests |
| Event and policy briefings | Per-turn executive briefings in interactive mode | `src/cli/display/briefing.rs` |
| Command selection | Interactive default plus preset strategy paths 1–3 | `src/cli/session.rs`, interactive tests |
| Turn-resolution summaries | Post-turn actor rationale and state hash display | `src/cli/display/briefing.rs`, briefing tests |
| End-of-run causal explanation | Deterministic debrief from committed history | `src/debrief/report.rs`, debrief tests |

Partially achieved:

| Requirement | Status | Notes |
| --- | --- | --- |
| Forecasts and uncertainty | Mostly achieved | Interactive uncertainty preview before each turn; observation note on dashboard; no probabilistic forecast objects |

### Internal playtesting (§5.5)

| Requirement | Evidence |
| --- | --- |
| Comprehensibility | [`playtest-findings-v0.1.25.md`](playtest-findings-v0.1.25.md) |
| Strategic tension | Finance/access/workforce/policy/competition tradeoffs at seed 42 |
| Causal transparency | Actor rationales, attributed effects, debrief prompts |
| Pacing | Five-turn bounded slice; no action overload observed |
| Action overload | Not observed in five-turn slice at seed 42 |
| Obvious exploits | None dominant at seed 42 in internal sessions |

### Phase 5 deliverables

| Deliverable | Status | Location |
| --- | --- | --- |
| Playable vertical slice | Complete | `cargo run` interactive and preset modes |
| One short scenario | Complete (design) | [`first-scenario-brief.md`](first-scenario-brief.md) |
| Deterministic replay file | Complete | `replay-artifact-0.1.15` format in `src/artifact/` |
| End-of-run analysis report | Complete | Debrief output plus replay artifact export |
| Internal playtest findings | Complete | [`playtest-findings-v0.1.25.md`](playtest-findings-v0.1.25.md) |
| Revised scope and risk register | Complete | This document |

## Deferred (with rationale)

### World slice (§5.1) — achieved within narrowed scope

| Roadmap item | Status | Evidence |
| --- | --- | --- |
| One player-controlled health system | Achieved | Player CEO commands in `src/model/command.rs` |
| One competitor | Achieved | Turn 5 rival system in `src/actors/competitor.rs` |
| One commercial insurer | Achieved | Turn 1 insurer actor in `src/actors/insurer.rs` |
| Small labor market | Achieved | Turn 3 nursing workforce representative in `src/actors/labor.rs` |
| Selected financial, capacity, access, quality, and trust measures | Achieved | `src/model/metrics.rs`, `src/model/state.rs` |
| One state-policy process | Achieved | Turn 2 state policy actor in `src/actors/state_policy.rs` |

### World slice (§5.1) — intentionally deferred

| Roadmap item | Status | Rationale |
| --- | --- | --- |
| Medicare | Deferred | Out of first-scenario scope; adds federal payment complexity |
| Medicaid | Deferred | State Medicaid agency needs distinct authority and information boundaries |
| Patient cohorts | Deferred | First scenario uses aggregate access and trust indices, not cohort simulation |
| Service-line portfolio | Deferred | Beyond stabilization scenario learning objectives |
| Employer or patient-group strategy | Deferred | Per [`first-scenario-brief.md`](first-scenario-brief.md) excluded interactions |
| Federal legislative process | Deferred | Per [`system-boundary.md`](system-boundary.md) excluded processes |

### Runtime and platform

| Item | Rationale |
| --- | --- |
| Scenario or ruleset file loader | Format design draft planned; runtime loader after approval |
| Mid-run save/load | Replay artifact export covers post-run reproducibility for now |
| Empirical calibration | Prototype integers remain design abstractions per [`evidence-registry.md`](evidence-registry.md) |
| Graphical interface | CLI-first scope per project proposal |
| Clippy CI or release automation | Phase 0 CI covers fmt and test only |

### Educational and validation

| Item | Rationale |
| --- | --- |
| External classroom playtesting | Phase 7 scope; after hardening and governance docs |
| Learning-outcome measurement | Phase 7 educational evaluation scope |
| Parameter-source ledger | Added in Phase 1 implications memo (v0.1.20) |

## Exit criteria assessment (roadmap §5)

| Exit criterion | Assessment | Evidence |
| --- | --- | --- |
| Player can complete the slice without developer intervention | Met | Interactive default completes five turns from `cargo run`; preset paths 1–3 available |
| Meaningful conflict among finance, access, workforce, and policy | Met | Path 1 at seed 42 trades cash for access with insurer rejection; path 3 triggers policy escalation; turn 5 adds competition tension |
| Non-player behavior understandable but not entirely predictable | Met | Actor rationales in history and debrief; resolved inputs vary by seed |
| Players can explain why major outcomes occurred | Met | Debrief uses rationales, attributed effects, and decision-vs-outcome prompt |
| Recognizably a strategy game, not a static model demo | Met | Multiple defensible preset paths, interactive parameter choices, strategic actor responses |

Phase 5 is **closed for the first-scenario bounded slice**. Remaining roadmap
§5.1 world elements (Medicare, Medicaid, cohorts) and Phase 6 expansion are
deferred with explicit design gates.

Golden final state hash at seed 42: `6fb1ebbea564274f` (86 tests at v0.1.25).

## Risk register

| Risk | Severity | Mitigation |
| --- | --- | --- |
| False precision | Medium | Label prototype formulas as abstractions in [`system-boundary.md`](system-boundary.md) and [`evidence-registry.md`](evidence-registry.md); defer calibration until parameter ledger exists |
| Scope drift | Medium | Use this register and [`first-scenario-brief.md`](first-scenario-brief.md) readiness checklist before runtime expansion; actor cards required before new strategic actors |
| Cognitive load | Low–Medium | Five-turn bound; dashboard and previews reduce pre-run confusion |
| Golden-test fragility | Low | `tests/golden_seed42.rs` documents canonical hash; breaking changes require explicit CHANGELOG note and hash update |
| Export prompt friction | Low | Empty input skips export; TTY-gated in non-interactive contexts |
| Documentation staleness | Medium | Version playtest findings with releases; keep SPEC Present/Done accurate |
| Normative opacity | Low | Debrief separates decision quality from outcome quality; social welfare not collapsed into player score |

## Recommended next slices

Per [`SPEC.md`](../SPEC.md) Future backlog and README contributor priorities:

1. **External playtest protocol refresh** — Phase 7 prep after v0.1.25 hardening.
2. **Scenario data loading runtime** — after [`scenario-format-draft.md`](scenario-format-draft.md) review.
3. **Medicare/Medicaid strategic actors** — gated; excluded from first scenario.

## Related documents

- [`first-scenario-brief.md`](first-scenario-brief.md) — scenario concept and expansion gates
- [`system-boundary.md`](system-boundary.md) — actor and command boundaries
- [`playtest-findings-v0.1.25.md`](playtest-findings-v0.1.25.md) — internal playtest record
- [`evidence-registry.md`](evidence-registry.md) — mechanism evidence status
