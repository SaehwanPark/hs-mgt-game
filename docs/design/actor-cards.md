# Actor Card Template

**Status:** Phase 3 design artifact  
**Audience:** Contributors designing strategic actors and scenario content

Actor cards define what an institution can do, what it wants, what it knows,
and how its choices should be explained. They are design artifacts, not a
runtime schema. Add a strategic actor to code only after its card is specific
enough to support deterministic tests and an educational debrief.

## Required Fields

Each actor card should include:

- Actor name and class.
- Scenario role.
- Objectives.
- Authority.
- Constraints.
- Resources.
- Observations.
- Private information or beliefs.
- Outside options.
- Risk posture.
- Time horizon.
- Feasible actions.
- Decision procedure.
- Rationale output.
- Debrief use.
- Evidence status.

## Field Guidance

### Actor Name and Class

Name the specific actor in the scenario and its broader class. Use concrete
scenario language such as `Northstar Health CEO`, `commercial insurer`, or
`state Medicaid agency` rather than generic labels alone.

### Scenario Role

State why the actor is present in the scenario. The role should connect to a
player decision, strategic interaction, observation difference, or debrief
question.

### Objectives

List the actor's own goals. Keep these separate from player success, social
welfare, and educational assessment.

### Authority

State what the actor can decide or commit. Authority should be institutional,
legal, contractual, political, or operational. Do not imply that influence is
the same as control.

### Constraints

Record limits on the actor's feasible actions, such as budgets, regulation,
labor contracts, network adequacy, political exposure, staffing capacity, or
organizational legitimacy.

### Resources

List resources the actor can use in the scenario: cash, capacity, staff,
contracts, information, political capital, community trust, or implementation
capacity.

### Observations

Define what the actor can observe at decision time. Observations may differ
from true state through delay, noise, missingness, bias, or later revisions.

### Private Information or Beliefs

Record beliefs, estimates, thresholds, or outside facts not visible to the
player. If the actor has no private information in the slice, say so.

### Outside Options

Describe credible alternatives if the interaction fails. Examples include
narrow-network threats, oversight escalation, work action, nonparticipation, or
delayed implementation.

### Risk Posture

State how the actor treats uncertainty and downside risk. Keep this qualitative
until evidence or playtesting justifies parameters.

### Time Horizon

State whether the actor emphasizes immediate financial pressure, quarterly
operational stability, election-cycle pressure, contract cycles, or long-term
legitimacy.

### Feasible Actions

List the actor's possible decisions in this slice. Separate invalid actions
from valid but unfavorable modeled outcomes.

### Decision Procedure

Describe the local, inspectable procedure that selects an action. This may be a
threshold rule, bounded best response, satisficing rule, bargaining heuristic,
or coalition heuristic. Do not introduce a global equilibrium requirement.

### Rationale Output

Specify the explanation the actor should leave in committed history. The
rationale should make the decision understandable for debugging and teaching
without exposing omniscient state.

### Debrief Use

Explain which debrief question the actor supports: decision quality under
uncertainty, strategic response, implementation limits, stakeholder legitimacy,
or social-welfare tradeoffs.

### Evidence Status

Classify the actor card's support as one of:

- Project requirement.
- Literature-informed abstraction.
- Official-data bounded.
- Expert-review candidate.
- Prototype abstraction.

Prototype abstractions must not be presented as calibrated claims.

## Minimum Readiness Check

Before a card can drive runtime work, confirm:

- The actor has a clear reason to exist in the first scenario.
- Authority, observations, and outside options are explicit.
- The decision procedure can be tested deterministically.
- The rationale output supports debriefing.
- Actor utility remains distinct from social welfare and player success.
- Any stochasticity or measurement uncertainty can be resolved before the core
  transition.

## Current Actor Cards

The current executable already contains compact actor behavior for:

- Commercial insurer.
- State policy officials.
- Nursing workforce representative.
- Regional provider coalition liaison.

These are sufficient for the five-turn architecture proof. Future slices should
use this template before adding Medicare, Medicaid, employers,
patient groups, regulators, elected officials, or advocacy coalitions as
strategic actors.

For **AI health-system players** in the competitive campaign, use the AI player
card template below (distinct from NPC institution cards).

### AI health-system player (competitive campaign)

| Field | Value |
| --- | --- |
| Actor name and class | AI-controlled regional health system CEO; peer player |
| Scenario role | Compete with human and other AI systems for access, margin, and trust |
| Objectives | Style-weighted: growth, margin, access leadership, or political legitimacy |
| Authority | Monthly command batch within AP, cash, and political capital limits |
| Constraints | Same ruleset as human; no omniscient rival state |
| Resources | Action points, cash, political capital, in-flight project slots |
| Observations | Own reported metrics; lagged public rival actions; policy briefings |
| Private information | Internal cash runway estimate (noisy); rival private negotiations hidden |
| Outside options | `hold`, reduced investment, defensive monitoring |
| Risk posture | Profile-defined; higher tiers take calculated competitive risks |
| Time horizon | Monthly with 1-month bounded lookahead for decision scoring |
| Feasible actions | Competitive verb catalog: `recruit`, `invest`, `monitor`, etc. |
| Decision procedure | Satisficing → level-1 best response to observed rival moves → stream tie-break |
| Rationale output | Text comparing top candidates and chosen batch |
| Debrief use | Contrast AI reasoning with human and consultant recommendations |
| Evidence status | Bounded game-theory abstraction per [`design_principles.md`](../design_principles.md) §5; not calibrated to real hospital competition |

### Rival regional health system (competitor, stabilization only)

| Field | Value |
| --- | --- |
| Actor name and class | Rival regional health system; competitor health system |
| Scenario role | Fifth-turn competitive capacity pressure after coalition turn |
| Objectives | Protect market share and growth option value in the region |
| Authority | Can accelerate outpatient/capacity expansion or pause plans |
| Constraints | Capital limits, community scrutiny, payer network reactions |
| Resources | Expansion capital, existing capacity, market intelligence |
| Observations | Player access posture signals, reported access, regional trust |
| Private information | Expansion cost estimates and margin thresholds (abstracted as market signal input) |
| Outside options | Delay expansion, target different submarket |
| Risk posture | Accelerate when rival response looks weak under market pressure |
| Time horizon | Current planning cycle |
| Feasible actions | Accelerate expansion, hold position, partial retreat |
| Decision procedure | Threshold evaluation on defensive capital and access posture vs market signal |
| Rationale output | Text explaining expansion, hold, or retreat given player credibility |
| Debrief use | Contrast defensive investment with competitive access and trust outcomes |
| Evidence status | Abstraction inspired by hospital market-capacity literature; not calibrated |
