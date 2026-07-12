# Mechanism Design - Regional Affiliation Runtime Proposal v0.11.14

## Goal and Roadmap Phase

Phase 7.7 expansion proposal gate, preparing one Phase 9 opt-in
`regional-affiliation-v1` scenario without changing the current competitive
runtime.

## Slice Boundary

- Setting: Riverside Community Health evaluates a relationship with one
  fictional neighboring nonprofit system.
- Runtime target: six monthly stages using existing competitive transition,
  observation, history, replay, and debrief surfaces.
- Primary choices: remain independent, defer while gathering information, or
  pursue the affiliation.
- Direct acquisition, multi-transaction portfolios, AI rivals, and a new
  campaign engine remain outside the slice.

## Actors and Authority

- Riverside CEO: assesses, chooses a posture, proposes commitments, submits
  review, and chooses whether to begin early integration.
- Partner nonprofit: accepts, rejects, or conditions the package based on its
  own solvency, mission, continuity, autonomy, and outside options.
- Review institution: approves, conditions, delays, or rejects; it is not
  controlled by Riverside.
- Labor representatives, commercial payer, and community coalition: respond to
  commitments and perceived service or concentration risk.

## State, Beliefs, and Observations

Future affiliation-specific true state must be limited to:

- partner condition and fit signals;
- affiliation status and stage;
- community, workforce, and service-continuity commitments;
- review status and conditions;
- integration progress and drag; and
- existing Riverside cash, access, quality, workforce, community, and market
  outcomes reused from the current world model.

Riverside observation may expose reported or delayed partner condition bands,
public labor/community/payer signals, review status and uncertainty, current
commitments, resource obligations, and available alternatives. It must not
expose hidden partner condition, hidden actor utility, or realized outcomes
before they occur.

## Commands, Events, and Effects

The future command vocabulary is staged and bounded:

1. assess partner;
2. choose independence, deferral, or affiliation pursuit;
3. set community, workforce, and service-continuity commitments;
4. submit the package for review; and
5. begin or decline early integration after approval.

Invalid operations include exceeding commitment authority, submitting duplicate
review, integrating without approval, or acting after a terminal decision.
Modeled outcomes include partner rejection, review delay, conditional approval,
labor opposition, payer response, service disruption, and integration drag.

## Strategic Interaction

The partner and Riverside negotiate a credible package. The review institution,
labor, payer, and community actors respond from their own information and
authority. Responses are localized to this scenario; no global equilibrium or
general actor framework is required. Independence, deferral, and affiliation
must each remain defensible under different observations.

## Assumptions and Parameters

- Mechanism direction is evidence-informed; all prototype numbers are game
  abstractions until separately validated.
- Partner, review, labor, payer, community, and integration outcomes are named
  resolved inputs with stable stage/seed identity.
- Regulatory outcomes are educational abstractions and must not imply legal
  prediction.
- Commitment cost, review timing, and integration effects remain numeric
  implementation decisions for a later PR.

## Educational Debrief Hooks

- What did Riverside know before choosing its posture?
- Which commitments preserved continuity or legitimacy, and what did they cost?
- Did an unfavorable outcome reflect poor choice, hidden realization, or an
  actor response outside Riverside's authority?
- How did organizational outcome differ from community welfare and access?
- What would independence or deferral have preserved?

## Determinism and Replay Notes

All uncertainty must be resolved before deterministic transition evaluation.
Future transition/history records must retain the resolved affiliation inputs,
decision-time observation, commands, events, attributed effects, and state hash.
Later observations may revise earlier estimates but must not rewrite committed
history. Any wire-shape change requires explicit replay and state-hash versioning.

## Open Questions

- A later implementation PR must choose concrete Rust types, scenario fields,
  command spelling, numeric ruleset bounds, and replay/hash compatibility.
- Domain QA must approve those choices before runtime promotion.
