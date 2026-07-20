# Phase 1 Research-to-Design Implications Memo

**Status:** Phase 1 closure artifact  
**Version:** v0.1.20  
**Date:** 2026-06-24  
**Audience:** Contributors, domain reviewers, and playtest designers

This memo converts Phase 1 research ([`phase1-lit-review.md`](phase1-lit-review.md),
[`evidence-registry.md`](../../research/evidence-registry.md), [`_workspace/01_evidence_map.md`](../../../_workspace/01_evidence_map.md))
into actionable design implications for the stabilization vertical slice. It is
not a bibliography and does not calibrate prototype parameters.

## Purpose

Phase 1 asked which prior approaches the project should adopt, modify, or
reject, and which evidence infrastructure must exist before broader calibration
or agent-playtest validation. The bounded five-turn prototype at v0.1.27 already
implements several adopted patterns. This memo records what literature and
precedent imply for **future** mechanism work, documentation, and validation.

## Adopted Patterns

| Pattern | Literature / precedent basis | Current implementation |
| --- | --- | --- |
| Narrow vertical slice before frameworks | Roadmap, serious-games pedagogy reviews | Five-turn CLI demo with replay and debrief |
| Deterministic transition core with explicit stochastic boundary | Simulation method literature, ODD/STRESS targets | `sim/transition.rs` plus `inputs/resolve.rs` |
| True state vs actor observations | Health simulation reporting guidance | `sim/observe.rs`, briefing tests |
| Local strategic actors with inspectable rationales | Bargaining and institutional IO abstractions | `actors/` modules, history records |
| Invalid commands separate from unfavorable outcomes | Educational debrief literature | `sim/validate.rs`, debrief prompts |
| Immutable history and replay verification | Project architecture requirement | `replay/`, state hashes, replay artifact |
| Educational debrief distinguishing decision from outcome | INACSL-style debrief guidance | `debrief/report.rs` |
| Actor cards before runtime actor expansion | Mechanism design control | [`actor-cards.md`](../../design/actor-cards.md) |
| Parameter ledger before calibration | Phase 1 evidence spine recommendation | [`evidence-registry.md`](../../research/evidence-registry.md) §Parameter-Source Ledger |

## Modified Patterns

| Pattern | What we keep | What we simplify for the slice |
| --- | --- | --- |
| Dynamic health-system simulation | Feedback among finance, access, workforce, policy | Integer metrics, no service-line portfolio |
| Payer-provider bargaining | Rate request vs network access tension | Single commercial insurer, three outcomes |
| Policy lifecycle | Stakeholder response to access mandate | One state-policy decision, no legislative process |
| Labor relations under pressure | Credible retention and schedule relief | One nursing representative, no strike calendar |
| Cooperative coalition action | Shared commitment and legitimacy tradeoff | One liaison actor, no coalition formation search |
| Serious-game pedagogy | Objectives, feedback, debrief alignment | CLI-only; no facilitator tooling yet |
| Official data grounding | CMS, MedPAC, MACPAC, KFF, BLS as candidates | Ledger names sources; prototype integers stay abstract |

## Rejected Patterns (for current scope)

| Pattern | Reason to defer |
| --- | --- |
| Global multi-actor equilibrium each turn | Roadmap and design principles forbid solving one game containing all actors |
| Authoritative policy forecasting | Non-goal; educational abstraction only |
| Comprehensive US reimbursement rules | Scope control; first scenario is regional stabilization |
| Graphical client first | CLI-first project direction |
| Empirical calibration before mechanism register | Phase 1 gap analysis; ledger precedes numeric replacement |
| Universal serious-game efficacy claim | Literature shows heterogeneous effects; debrief and alignment matter |
| End-user co-design without documented protocol | Literature supports participatory design; formal protocol is Phase 7 scope |

## Mechanism Implications by Interaction

### Payer negotiation (Turn 1)

- **Design implication:** Insurer decisions should use reported access and
  requested rate, not player omniscience. Rejection must remain a valid modeled
  outcome when inputs are valid.
- **Evidence status:** Abstraction inspired by commercial contracting literature;
  not calibrated to contract data.
- **Next work:** Link ledger row to KFF employer survey and MedPAC hospital
  payment context when ranges are introduced.

### State access mandate (Turn 2)

- **Design implication:** Policy response should depend on credible access
  commitment and advocacy spend, with an inspectable oversight ladder.
- **Evidence status:** Simplified policy-process abstraction.
- **Next work:** Document state authority boundaries before adding Medicaid or
  federal actors.

### Workforce pressure (Turn 3)

- **Design implication:** Labor response should reward credible retention and
  schedule relief under explicit labor-pressure signal.
- **Evidence status:** Labor-market tension abstraction; BLS occupation data is a
  future anchor only.
- **Next work:** Avoid implying legal strike simulation without labor-law review.

### Regional coalition (Turn 4)

- **Design implication:** Cooperative outcomes should trade community legitimacy
  against cash and shared commitment credibility.
- **Evidence status:** Roadmap cooperative interaction form; not a general
  coalition-formation model.
- **Next work:** Keep distinct from future competitive interaction.

### Competitor capacity (planned Turn 5)

- **Design implication:** Roadmap §3.3 calls for one competitive capacity or
  market-entry interaction. Implement only after an actor card and mechanism
  design gate. Use local deterministic evaluation with rationale, not market
  equilibrium.
- **Evidence status:** Not yet implemented; hospital market-power literature
  informs plausibility only.
- **Next work:** See [`actor-cards.md`](../../design/actor-cards.md) competitor card and
  `_workspace/02_mechanism_design.md` after Slice 2 design.

## Documentation and Validation Standards

Adopt for ongoing slices:

| Standard | Application in this repo |
| --- | --- |
| ODD / STRESS transparency | Document actors, state variables, process overview, and design experiments in system-boundary and architecture docs |
| Mechanism register | [`evidence-registry.md`](../../research/evidence-registry.md) mechanism table |
| Parameter-source ledger | Same file; source candidates without fabricated values |
| Deterministic replay tests | Golden integration test, replay verification, artifact round-trip |
| Domain QA before runtime expansion | `_workspace/03_domain_qa.md` per slice |
| Playtest findings versioned with releases | `docs/history/playtests/v*/playtest-findings-v*.md` |
| Decision vs outcome debrief | Required debrief prompt in every end-of-run report |

Defer to a separate human evaluation study unless explicitly planned:
CONSORT-SPI, TIDieR-PHP, formal learning-outcome instruments, and external
expert panels at scale.

## Unresolved Empirical Questions

These remain open by design until a parameter ledger row moves to calibration:

1. Which official datasets anchor payer mix, hospital margin, workforce pressure,
   and access indices for the fictional region?
2. Which mechanism thresholds need expert review before future classroom use?
3. Which educational outcomes can agent-playtest traces inspect, and which
   require a separate human evaluation plan?
4. Which actor objectives should be scenario-configurable versus fixed?
5. Which distributional or disparity outcomes must be first-class before public
   release?
6. How should rulesets, scenarios, and replay artifacts version together?

## Risks Carried from Phase 1

| Risk | Mitigation already in place | Remaining action |
| --- | --- | --- |
| False precision | Abstraction labels in evidence registry | Do not replace integers without ledger citation |
| Scope drift | Phase 5 register, scenario brief gates | Actor card required before new actors |
| Educational opacity | Rationales, attributed effects, debrief | Extend to competitor slice |
| Thin health-policy-game precedent | Document assumptions explicitly | Implications memo and domain QA |

## Related Documents

- [`phase1-lit-review.md`](phase1-lit-review.md) — full literature framework
- [`evidence-registry.md`](../../research/evidence-registry.md) — mechanism and parameter ledger
- [`phase5-scope-register.md`](phase5-scope-register.md) — Phase 5 closure and next slice
- [`first-scenario-brief.md`](../../design/first-scenario-brief.md) — scenario expansion gates
