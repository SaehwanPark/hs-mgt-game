# Evidence Map - Instructor Run Summary & Decision Quality Review

## Inputs
- `docs/design_principles.md` Principle 3 (Separate Actor Rationality), Principle 20 (Design for Debriefing).
- `src/sim/observe.rs`: shows how reported access index contains noise and delay.
- `src/sim/observe_competitive.rs` and `src/mcp/session.rs`: shows how rival commands are observed or unobserved.

## Evidence-Backed Claims
- True access index matches `WorldState.access_index`, but the player only observes `Observation.reported_access_index`. The difference is driven by `delayed_access_report` and `measurement_noise` inputs.
- During active play in the competitive campaign, players only see public rival actions or actions from targets they specifically monitored. Unmonitored private actions remain unobserved.
- Exposing the true-vs-observed state and the unobserved rival actions at debrief time allows retroactively analyzing the quality of decisions made under imperfect information without exposing omniscient state during active play.

## Design Abstractions
- For competitive preview, noise and delay are currently simplified (true state matches observed), but the infrastructure should support future noise.
- Rival rationales are unobserved during active play, but exposing them at debrief time is acceptable for instructor/debrief review.

## Unresolved Questions
- How to display the comparisons cleanly in a text-based terminal table or block without exceeding terminal width.
- How to handle cases where no transitions have been committed yet.
