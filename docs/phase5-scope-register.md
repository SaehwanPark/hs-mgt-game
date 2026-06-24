# Phase 5 Scope and Risk Register

**Status:** Phase 5 closure artifact  
**Version:** v0.1.19  
**Date:** 2026-06-24  
**Audience:** Contributors, domain reviewers, and playtest designers

This register records what the first vertical slice achieved against
[`docs/roadmap.md`](roadmap.md) Phase 5, what remains intentionally deferred,
known risks, exit-criteria evidence, and the recommended next runtime slice.

## Scope Statement

The current executable is a four-turn regional-market stabilization demo at
v0.1.19. It demonstrates deterministic transitions, seeded stochastic inputs,
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
| Delayed consequences across several turns | Cash, access, trust, and policy pressure carry across four turns | Golden seed-42 integration test, replay tests |

### Observation slice (§5.3)

| Requirement | Implementation | Evidence |
| --- | --- | --- |
| True versus reported measures | `observe` derives actor-visible reports from true state plus resolved inputs | `src/sim/observe.rs`, observation tests |
| Actor-specific information | Per-turn briefings use observation data, not future outcomes | `src/cli/display/briefing.rs`, briefing tests |
| Measurement delay or uncertainty | Named random streams perturb reported access | `src/inputs/resolve.rs`, resolver tests |
| Later revisions | Revision stream adds new briefing notes without rewriting history | Observation revision tests, debrief revision notes |

### Playable CLI slice (§5.4)

| Requirement | Implementation | Evidence |
| --- | --- | --- |
| Concise executive dashboard | Starting dashboard before play-mode selection | `src/cli/display/dashboard.rs`, dashboard tests |
| Event and policy briefings | Per-turn executive briefings in interactive mode | `src/cli/display/briefing.rs` |
| Command selection | Interactive default plus preset strategy paths 1–3 | `src/cli/session.rs`, interactive tests |
| Turn-resolution summaries | Post-turn actor rationale and state hash display | `src/cli/display/interactive.rs` |
| End-of-run causal explanation | Deterministic debrief from committed history | `src/debrief/report.rs`, debrief tests |

Partially achieved:

| Requirement | Status | Notes |
| --- | --- | --- |
| Forecasts and uncertainty | Partial | Uncertainty appears through noisy/revised observations and strategy previews; no dedicated forecast UI or probabilistic forecast objects |

### Internal playtesting (§5.5)

| Requirement | Evidence |
| --- | --- |
| Comprehensibility | [`playtest-findings-v0.1.19.md`](playtest-findings-v0.1.19.md) |
| Strategic tension | Finance/access/workforce/policy tradeoffs at seed 42 |
| Causal transparency | Actor rationales, attributed effects, debrief prompts |
| Pacing | Four-turn bounded slice; no action overload observed |
| Obvious exploits | None dominant at seed 42 in internal sessions |

### Phase 5 deliverables

| Deliverable | Status | Location |
| --- | --- | --- |
| Playable vertical slice | Complete | `cargo run` interactive and preset modes |
| One short scenario | Complete (design) | [`first-scenario-brief.md`](first-scenario-brief.md) |
| Deterministic replay file | Complete | `replay-artifact-0.1.15` format in `src/artifact/` |
| End-of-run analysis report | Complete | Debrief output plus replay artifact export |
| Internal playtest findings | Complete | [`playtest-findings-v0.1.19.md`](playtest-findings-v0.1.19.md) |
| Revised scope and risk register | Complete | This document |

## Deferred (with rationale)

### World slice (§5.1) — intentionally narrowed

| Roadmap item | Status | Rationale |
| --- | --- | --- |
| One competitor | Deferred | Next recommended runtime slice; requires actor card first per [`first-scenario-brief.md`](first-scenario-brief.md) |
| Medicare | Deferred | Out of first-scenario scope; adds federal payment complexity before competitive interaction is modeled |
| Medicaid | Deferred | Same as Medicare; state Medicaid agency needs distinct authority and information boundaries |
| Patient cohorts | Deferred | First scenario uses aggregate access and trust indices, not cohort simulation |
| Service-line portfolio | Deferred | Beyond stabilization scenario learning objectives |

### Runtime and platform

| Item | Rationale |
| --- | --- |
| Scenario or ruleset file loader | Conceptual model and action vocabulary not yet stable enough for a schema |
| Mid-run save/load | Replay artifact export covers post-run reproducibility for now |
| Forecast UI | Observation uncertainty is modeled; dedicated forecast objects deferred |
| Empirical calibration | Prototype integers remain design abstractions per [`evidence-registry.md`](evidence-registry.md) |
| Graphical interface | CLI-first scope per project proposal |
| Clippy CI or release automation | Phase 0 CI covers fmt and test only |

### Educational and validation

| Item | Rationale |
| --- | --- |
| External classroom playtesting | Awaiting governance docs, implications memo, and competitor slice |
| Learning-outcome measurement | Phase 7 educational evaluation scope |
| Parameter-source ledger | Phase 1 implications memo slice |

## Exit criteria assessment (roadmap §5)

| Exit criterion | Assessment | Evidence |
| --- | --- | --- |
| Player can complete the slice without developer intervention | Met | Interactive default completes four turns from `cargo run`; preset paths 1–3 available |
| Meaningful conflict among finance, access, workforce, and policy | Met | Seed 42 access-stabilization path trades cash for access; payer rejection and policy escalation paths exist |
| Non-player behavior understandable but not entirely predictable | Met | Actor rationales in history and debrief; seeded inputs vary outcomes by seed |
| Players can explain why major outcomes occurred | Met | Debrief uses rationales, attributed effects, and decision-vs-outcome prompt |
| Recognizably a strategy game, not a static model demo | Met | Multiple defensible preset paths, interactive parameter choices, strategic actor responses |

Phase 5 is **closed for the current bounded slice**. Remaining roadmap §5.1 world elements are deferred to later slices with explicit design gates, not treated as incomplete Phase 5 blockers.

## Risk register

| Risk | Severity | Mitigation |
| --- | --- | --- |
| False precision | Medium | Label prototype formulas as abstractions in [`system-boundary.md`](system-boundary.md) and [`evidence-registry.md`](evidence-registry.md); defer calibration until parameter ledger exists |
| Scope drift | Medium | Use this register and [`first-scenario-brief.md`](first-scenario-brief.md) readiness checklist before runtime expansion; actor cards required before new strategic actors |
| Cognitive load | Low–Medium | Four-turn bound; dashboard and previews reduce pre-run confusion; posture menus remain deferred |
| Golden-test fragility | Low | `tests/golden_seed42.rs` documents canonical hash; breaking changes require explicit CHANGELOG note and hash update |
| Export prompt friction | Low | Empty input skips export; TTY-gated in non-interactive contexts |
| Documentation staleness | Medium | Version playtest findings with releases; keep SPEC Present/Done accurate |
| Normative opacity | Low | Debrief separates decision quality from outcome quality; social welfare not collapsed into player score |

## Recommended next slice

**Competitor strategic actor runtime slice** (`feat/competitor-capacity-slice`):

1. Write competitor actor card using [`actor-cards.md`](actor-cards.md).
2. Add a bounded fifth-turn competitive capacity or market-entry interaction.
3. Extend replay, debrief, preset paths, and golden tests consistently.
4. Run mechanism design and domain QA handoffs before implementation.

Intervening documentation slices (per README priorities):

1. Phase 0 governance docs (glossary, decision records, versioning policy).
2. Phase 1 research-to-design implications memo.

## Related documents

- [`first-scenario-brief.md`](first-scenario-brief.md) — scenario concept and expansion gates
- [`system-boundary.md`](system-boundary.md) — actor and command boundaries
- [`playtest-findings-v0.1.19.md`](playtest-findings-v0.1.19.md) — internal playtest record
- [`evidence-registry.md`](evidence-registry.md) — mechanism evidence status
