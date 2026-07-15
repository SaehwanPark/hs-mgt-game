# Visual/audio Phase 13 — First-month continuity

**Status:** Implemented, verified, reviewed once, and merged in PR #180
**Scope:** Presentation-only first-month handoff rail and integration evidence
**Version target:** 0.12.29

## Purpose

Phases 0–12 provide separate technical surfaces for session launch/load,
actor-visible presentation, regional-world detail, contextual actions, monthly
resolution, generated audio, campaign coverage, accessibility, and visual
identity. The proposal's first polished month still needs one inspectable
continuity contract showing how those surfaces connect.

## User contract

The competitive regional desktop shows a seven-step, text-first path:

1. Start or load;
2. Inspect the visible market and briefing;
3. Draft host-catalogued actions;
4. Review at least two draft commands and host metadata;
5. Submit only after unchanged host validation;
6. Read or skip the committed resolution and refreshed presentation;
7. Continue to the next visible observation.

The rail is orientation, not a progress claim about strategy, policy, or
simulation outcome. Existing source, uncertainty, pending, status, and audio
equivalent text remain authoritative.

## Boundary

`first-month.mjs` owns a small local state projection and semantic rendering.
`app.mjs` updates it only after existing adapter calls succeed. The host remains
authoritative for session identity, action legality, transition, stochastic
resolution, committed effects, observations, history, hashes, replay, and
debrief.

## Verification and limits

Focused tests cover pure stage derivation, complete adapter sequencing,
rejection/recovery non-advancement, read-only submit exclusion, semantic text,
reduced-motion compatibility, and boundary exclusions. Full repository checks
pass before handoff.

These are technical and interface-task proxies only. They do not establish
human usability, lived accessibility, learning, engagement, calibration,
balance, policy validity, or domain-expert agreement.

## Explicit non-goals and next gate

No new host schema, simulation mechanism, browser transport, asset, audio
source, campaign-wide onboarding system, or browser-owned simulation state is
introduced. The next gate after this slice is a post-merge audit of whether the
remaining first-month product contract needs another narrow technical item or
should pause for separately authorized human evaluation.
