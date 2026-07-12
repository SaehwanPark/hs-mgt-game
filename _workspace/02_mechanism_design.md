# Mechanism Design - Workforce Capacity Difficulty Design Gate v0.12.5

## Goal and Roadmap Phase

Phase 7/9 difficulty-depth design gate following the v0.12.4 candidate signal.
This is an observation-contract proposal, not a new difficulty mechanism.

## Slice Boundary

- Inputs: v0.12.4 evidence plus current typed observation, MCP projection,
  transition, and debrief source.
- Output: a deterministic design contract for a possible MCP presentation
  follow-up.
- Proposed next slice: render only safe typed Riverside staffing/capacity
  context, add boundary tests, and rerun the unchanged v0.12.4 matrix.
- Excluded: difficulty values, balance, scoring, transition formulas, hidden
  targets, effective staffing calculations, rival state, GUI, and human
  evaluation.

## Actors and Authority

Riverside may observe its own current staffing counts and physical capacities.
The player does not observe hidden staffing targets, allocation priorities,
future pending effects, rival private workforce state, or realized future
responses before transition resolution.

## Current observation contract

The typed `PlayerObservation` already carries:

- workforce trust summary and nursing-vacancy wording;
- nurses, physicians, and admins;
- staffed beds, outpatient, emergency, ICU, obstetrics, psychiatric,
  cardiology, oncology, infusion, neurology, and ASC capacities;
- prior demand, treated volume, unmet demand, revenue, cost, and margin; and
- labor-market delay/cost guidance and state-conditioned consultant options.

The current MCP formatter renders the trust summary, prior operations, labor
guidance, and consultant options but omits the numeric staffing/capacity fields.

## Proposed projection contract

If promoted into the next implementation slice, render exactly two compact
lines from `PlayerObservation`:

1. `Staffing: nurses <n>, physicians <n>, admins <n>`.
2. `Physical capacity: staffed beds <n>, outpatient <n>, emergency <n>, ICU <n>, obstetrics <n>, psychiatric <n>, cardiology <n>, oncology <n>, infusion <n>, neurology <n>, ASC <n>`.

The projection must not calculate or expose effective capacity, role targets,
allocation queues, hidden pending hires, or future outcomes. Existing typed
fields are the only source.

## Transition and debrief boundaries

No command, event, effect, transition, resolved input, state hash, replay
artifact, or debrief causal wording changes. Existing staffing deficit and
staffing capacity constraint events remain the realized follow-through. The
next evidence run must prove that history/state hashes and the v0.12.4 golden
boundary are unchanged.

## Decision and educational hooks

The proposed lines let a player inspect the current staffing/capacity context
before choosing recruit, invest, monitor, pledge, or hold. They make the
existing labor-market and consultant tradeoffs more interpretable without
claiming that the line improves learning or that any action is optimal.

## Routing decision

The candidate signal warrants a bounded observation-context implementation
follow-up, not a difficulty-value or balance change. Keep runtime promotion for
mechanics deferred until a later evidence gate establishes a concrete need.

## Open questions

- Whether the compact line is understandable to humans remains unmeasured.
- Whether all service-line capacities belong in one line or need a later
  presentation review is an interface question, not a simulation question.
- Expert clearability remains limited to the named scripted profiles and seeds.
