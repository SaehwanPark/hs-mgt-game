# Mechanism Design — Visual and Audio Phase 0 Alignment v0.12.16

## Goal and Roadmap Phase

Close the visual/audio proposal's Phase 0 product and architecture alignment
gate. The smallest useful slice is one actor-controlled competitive month,
without a new simulation mechanism.

## Slice Boundary

The setting is `competitive-regional-v1`; Riverside is the human system, the
duration is one month, and the player acts as an executive allocating attention,
resources, workforce, payer/policy posture, commitments, and strategy. The
presentation surface includes briefing, schematic region, institution/facility
detail, action draft/preview, pending processes, resolution, replay, and debrief.
Stabilization and affiliation remain future campaign-specific work.

## Actors and Authority

The Rust host and existing MCP adapter own simulation authority. The player sees
the actor-visible projection. Rival systems remain strategic actors, but private
rival actions are excluded from the standard client. Client navigation,
selection, drafts, animation, and preferences are non-authoritative.

## State, Beliefs, and Observations

True state includes fields in `CompetitiveWorldState`, resolved inputs, and
private actor actions. The player observation includes organization identity,
reported access/quality, trust summaries, staffing, capacity, demand, treated and
unmet volume, revenue/cost/margin, project status, runway, market/policy bullets,
consultant options, and information gaps. The client must never infer omitted
values, private utility, or future outcomes.

## Commands, Events, and Effects

The first slice uses existing `CompetitiveCommand` variants: hold, recruit,
invest, monitor, negotiate, commit, and project. A form preview shows canonical
command, costs, delays, visible constraints, validation result, and uncertainty;
it does not promise the outcome. Committed `TransitionSummary` events/effects
and the next observation supply resolution and cue sources. Validation failure
does not advance history.

## Strategic Interaction

The player responds to visible workforce/capacity pressure and public payer,
policy, market, and rival signals. Private rival actions and resolved stochastic
inputs remain hidden until an authorized visible report or committed effect
reveals them. No new payoff or actor rule is introduced by the presentation.

## Assumptions and Parameters

Browser-native HTML/CSS/ES modules plus native SVG are the initial stack. A
future client may use Web Audio API playback, but cue classification is a pure
visible-event mapping. Music states are menu, stable operations, pressure, and
debrief; UI and event cue counts remain bounded by the proposal.

## Educational Debrief Hooks

The surface keeps decision quality separate from outcome quality, links visible
causes to committed effects, preserves observation-time information, and asks
the player to inspect tradeoffs, pending processes, and revisions. It does not
claim that an agent or static checker learned or understood the material.

## Determinism and Replay Notes

The client does not resolve randomness or mutate history. Replaying visible
history may regenerate animation/audio cues, but playback is not recorded in
simulation history. Presentation changes must leave commands, transitions,
replay artifacts, state hashes, and deterministic outcomes unchanged.

## Open Questions

- Which structured adapter projections are needed after Phase 1 fixture review?
- What host mode and asset storage are justified by evidence?
- What recording sink and browser fallback are appropriate for Phase 5 audio?

The Phase 0 artifact never imports the Rust crate, runs a simulation, adds a
browser dependency, downloads assets, or publishes an artifact. The static
contract test checks that the boundary and source inventory remain explicit.
