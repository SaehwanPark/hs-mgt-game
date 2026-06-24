# Initial System Boundary and Ontology Draft

**Status:** Draft for Phase 2 conceptual design  
**Audience:** Contributors and domain reviewers

## Geographic and Institutional Setting

- Fictional regional US health market.
- Player leads one nonprofit health system.
- Initial slice includes commercial insurer, state policy officials, nursing
  workforce representative, and regional provider coalition liaison.

## Player Role and Authority

- Player acts as health system CEO.
- Authority covers capacity investment, payer negotiation posture, state mandate
  response, workforce retention offers, and coalition participation.
- Player does not directly set reimbursement rules, legislate, or control
  competitor systems.

## Campaign Scope (Current Prototype)

- Four-turn deterministic demo with compiled strategy paths.
- Seeded stochastic inputs resolved before each transition.
- Append-only history with replay and educational debrief.

## Included Actor Classes

| Actor | Role in prototype |
| --- | --- |
| Health system CEO | Player command selection via strategy path |
| Commercial insurer | Rate negotiation on capacity turn |
| State policy officials | Access mandate response |
| Nursing workforce representative | Labor pressure response |
| Regional provider coalition liaison | Coalition access opportunity |

## Excluded (Initial Version)

- Medicare and Medicaid as strategic actors.
- Competing health systems.
- Employers and patients as decision agents.
- Federal legislative process.
- Full service-line portfolio.
- Graphical interface and multiplayer roles.

## Core State Variables

- Financial: cash, commercial rate.
- Capacity and access: staffed beds, access index.
- Quality and trust: quality index, workforce trust, community trust.
- Policy: policy pressure.

## Observation Model

- Player sees reported access (delayed, noisy) and current quality.
- Later turns may include prior-period access measurement revisions in the
  briefing without rewriting committed history.
- NPC decisions use actor-visible observations and resolved inputs.

## Command Vocabulary (Prototype)

1. `StabilizeAccess` — capacity and payer rate posture.
2. `RespondToStateAccessMandate` — advocacy and access commitment.
3. `RespondToWorkforcePressure` — retention and schedule relief.
4. `JoinRegionalAccessCoalition` — coalition investment and shared access
   commitment.

## Deferred Ontology Work

- Typed scenario and ruleset file formats.
- Patient cohort segmentation.
- Service-line and capital-allocation ontology.
- Formal belief-state representation beyond observation snapshots.
