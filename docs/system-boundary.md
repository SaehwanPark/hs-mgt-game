# Initial System Boundary and Ontology Draft

**Status:** Phase 2 conceptual design draft  
**Audience:** Contributors and domain reviewers

This document defines the current conceptual boundary for the first regional
market slice. It describes what the prototype represents, what it deliberately
leaves outside the model, and which terms should stay stable until a narrower
scenario or ruleset format is approved.

## Setting and Time Horizon

- The setting is a fictional regional US health market centered on one
  nonprofit health system.
- The current executable is a four-turn deterministic demo with compiled
  strategy paths, explicit run seed, append-only history, replay, and educational
  debrief.
- Each turn represents an executive decision point, not a fixed calendar unit.
  A later campaign design may assign quarters or months after the scenario
  learning objectives are settled.
- The scope is regional and institutional. National policy, federal budgets,
  and macroeconomic conditions may appear only as resolved external inputs until
  the roadmap calls for broader modeling.

## Player Role and Authority

- The player is the health system CEO.
- Current authority covers capacity investment, payer negotiation posture, state
  access-mandate response, workforce retention and schedule relief offers, and
  regional access coalition participation.
- The player can allocate organizational resources and make public or
  institutional commitments.
- The player cannot directly set reimbursement law, legislate, control
  competitor systems, compel workforce acceptance, or directly alter observed
  measurements.

## Actor Classes

| Actor class | Current role | Authority boundary | Information boundary |
| --- | --- | --- | --- |
| Health system CEO | Player command selection | May commit health-system resources within ruleset limits | Sees reported access, quality, briefings, and later revisions |
| Commercial insurer | Turn 1 rate negotiation | May accept, counter, or reject a requested rate path | Responds to observed access, requested rate, and network concerns |
| State policy officials | Turn 2 access mandate response | May grant flexibility, continue mandate, or escalate oversight | Responds to reported access, commitments, and policy signal |
| Nursing workforce representative | Turn 3 labor pressure response | May cooperate, offer limited support, or signal work action | Responds to retention, schedule relief, trust, and labor pressure |
| Regional provider coalition liaison | Turn 4 access coalition | May join fully, participate narrowly, or withdraw | Responds to shared access commitment, community trust, and leverage |

Future actor classes may include Medicare, Medicaid, competitors, employers,
patient groups, regulators, elected officials, and advocacy coalitions. They
should not be added as strategic actors until a slice needs their authority,
information, and decision procedure.

## State and Observation Boundary

- True state currently tracks cash, staffed beds, access index, quality index,
  workforce trust, community trust, commercial rate, and policy pressure.
- Observations are actor-visible reports derived from true state plus explicit
  resolved inputs. They may be delayed, noisy, or revised later.
- Later measurement revisions are new observations about prior periods. They do
  not mutate committed transition records or prior observations.
- Actor decisions must use the state, observation, command, and resolved inputs
  available to that turn. They must not depend on hidden randomness, wall-clock
  time, filesystem state, network state, or global mutable state.

## Command Vocabulary

| Command | Player decision represented | Current validation boundary |
| --- | --- | --- |
| `StabilizeAccess` | Capacity investment and payer rate posture | Positive staffed-bed change, non-negative bounded capital spend |
| `RespondToStateAccessMandate` | Advocacy and access commitment | Non-negative bounded advocacy spend, positive access commitment |
| `RespondToWorkforcePressure` | Retention and schedule-relief response | Non-negative bounded retention spend, positive bounded schedule relief |
| `JoinRegionalAccessCoalition` | Regional access coalition posture | Non-negative bounded coalition investment, positive bounded shared access commitment |

Validation failures represent invalid operations. Rejected negotiations,
oversight escalation, work actions, and coalition withdrawal are valid modeled
outcomes.

## Causal Categories

- Financial capacity: cash spending constrains later strategic flexibility.
- Access capacity: staffed beds, shared commitments, and labor pressure affect
  access.
- Workforce legitimacy: retention and schedule relief influence workforce trust,
  quality, and potential work actions.
- Community legitimacy: public bargaining friction, access commitments, policy
  response, and coalition behavior influence community trust.
- Policy pressure: state signals and actor responses can increase or reduce
  oversight pressure.
- Measurement and revision: reported access may differ from true access, and
  later revisions create new briefing information without rewriting history.

All current causal formulas are integer prototype abstractions. They are
inspectable mechanics, not empirical calibration.

## Included and Excluded Processes

Included in the current conceptual boundary:

- Local payer-provider bargaining.
- State access-policy response.
- Workforce pressure and labor response.
- Regional access coalition opportunity.
- Actor-specific observation, rationale records, attributed effects, replay, and
  educational debrief.

Excluded from the current conceptual boundary:

- Full Medicare, Medicaid, employer, patient, or competitor strategic behavior.
- Service-line portfolio modeling.
- Individual patient simulation.
- Federal legislative process.
- Scenario or ruleset file loading.
- Save files, persistence, multiplayer roles, graphical interface, or release
  packaging.

## Deferred Ontology Work

- Formal actor-card template covering objectives, authority, constraints,
  information, outside options, risk posture, time horizon, and decision
  procedure.
- Scenario and ruleset versioning format.
- Patient cohort and distributional outcome vocabulary.
- Service-line, capital-allocation, and market-area vocabulary.
- Formal belief-state representation beyond observation snapshots.
- Parameter ledger separating empirical ranges, design abstractions, balancing
  choices, and normative scoring.
