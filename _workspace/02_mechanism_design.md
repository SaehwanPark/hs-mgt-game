# Mechanism Design — Affiliation Runtime Boundary Proposal v0.12.7

## Existing mechanism boundary

The runtime has one human-led Riverside system and one localized nonprofit
partner across six stages: assess, posture, commitments, review submission,
review resolution, and integrate-or-decline.

The design is already separated into:

1. true state in `AffiliationWorldState`;
2. actor-visible projection in `AffiliationObservation` and MCP formatting;
3. explicit stochastic outcomes in `AffiliationResolvedInputs`;
4. deterministic evaluation in `transition_affiliation`;
5. immutable transition/history/replay records; and
6. retrospective organizational, actor, and social-welfare debrief lines.

## Boundary decision

The implementation satisfies the minimum proposal. No new mechanism should be
added in v0.12.7. Direct acquisition and broader consolidation remain future
work gated by concrete evidence.
