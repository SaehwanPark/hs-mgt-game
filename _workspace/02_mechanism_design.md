# Mechanism Design — Visual and Audio Phase 1 Static Desktop v0.12.17

## Goal and Roadmap Phase

Validate the Phase 0 information architecture with a static executive desktop
before adding live read-only DTOs. This is roadmap Phase 1.

## Slice Boundary

One actor-visible `competitive-regional-v1` month with Riverside Community
Health and public rival summaries. The screen includes header metrics, briefing,
schematic regional cards, selected system/facility detail, action previews,
pending processes, monthly result, history, and debrief. No transition is run.

## Actors and Authority

The browser owns only fixture rendering, entity selection, focus/navigation, and
local presentation state. Existing MCP/host code remains authoritative for
observation, legal commands, command submission, stochastic inputs, transitions,
history, hashes, and debriefs.

## State, Beliefs, and Observations

Fixture fields are limited to actor-visible values: finance, workforce,
capacity, access/quality, public market/rival signals, visible timing, direct
monthly results, and source labels. Private rival actions, true state, resolved
inputs, private utility, and hidden outcomes are unavailable or excluded.

## Commands, Events, and Effects

Action cards preview existing `recruit`, `invest`, and `monitor` command families
with canonical text, cost, delay, visible constraint, and uncertainty. They are
not submit controls. The existing command field continues to call
`HsMgtGameAdapter.submitTurn`; no new command or GUI-only resolution exists.

## Strategic Interaction

The player compares visible workforce/capacity pressure with public rival
signals and pending commitments. Entity selection supports inspection, not a
strategic action. The prototype preserves the distinction between a visible
signal and a private rival response.

## Assumptions and Parameters

The browser-native stack from ADR-0011 is retained. CSS custom properties define
design tokens. Statuses use text plus a diamond marker and color-independent
wording. Grid breakpoints support typical desktop/laptop widths; reduced motion
removes transitions.

## Educational Debrief Hooks

The desktop makes decision context, pending effects, direct monthly drivers,
observation gaps, history, and debrief links visible. It does not claim that a
reviewer learned, understood, or preferred the interface.

## Determinism and Replay Notes

No transition, RNG, history, replay artifact, or hash is touched. Selecting an
entity rerenders fixture detail only. Existing adapter submission behavior is
unchanged, and future replay visualization remains a separate phase.

## Open Questions

- Which fixture fields are actually needed for a typed Phase 2 adapter?
- Which loading/error/empty states need structured host responses?
- What evidence would justify live projection or a richer visual component?
