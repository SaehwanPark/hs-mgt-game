# Mechanism Design — Visual/audio Phase 13 first-month continuity v0.12.29

## Goal and roadmap gate

Close the technical continuity gap in the proposal's exact one-month
`competitive-regional-v1` experience without adding a new game mechanism.
Phase 13 is a presentation/action-boundary slice following the merged Phase 12
visual vocabulary.

## Local flow vocabulary

The rail has seven ordered stages:

1. `start` — start or load a host session;
2. `inspect` — read the current actor-visible briefing and regional world;
3. `draft` — choose and revise host-catalogued actions;
4. `validate` — review at least two draft commands and host-returned metadata;
5. `submit` — submit the unchanged host-validated batch;
6. `resolution` — read, skip, pause, or review the committed resolution and
   refreshed presentation;
7. `continue` — the next actor-visible observation is available.

The stage is derived from local booleans and a draft count. It describes client
handoff progress, not a simulation state or player success state.

## Actors and authority

- Executive: uses the rail to orient to the next presentation step.
- Browser: owns the rail, local draft count, stage display, and local selection.
- Host/core: owns session existence, command catalog, legality, costs, delays,
  stochastic resolution, committed effects, observations, history, hashes, and
  debriefs.

The browser never marks a step complete from a guessed result. A failed start,
load, validation, submit, resolution read, or refresh leaves the stage at the
last confirmed handoff and keeps existing recovery behavior.

## State and transition rules

The local flow state contains only:

```text
session_loaded: bool
action_catalog_loaded: bool
draft_count: non-negative integer
validated: bool
submitted: bool
resolution_visible: bool
refreshed: bool
```

The pure stage function applies these rules in order:

- no session → `start`;
- session without action catalog → `inspect`;
- submitted without both resolution and refreshed presentation → `resolution`;
- submitted with both resolution and refreshed presentation → `continue`;
- fewer than two drafts → `draft`;
- drafts without valid host validation → `validate`;
- valid validation without submit → `submit`;
- otherwise → `continue`.

Changing or clearing drafts clears local validation and cannot advance the
simulation. Resolution playback controls remain local and do not change the
stage or host state.

## Presentation contract

`gui/first-month.mjs` provides a frozen `competitive-first-month-v1` stage
catalog, a pure `firstMonthStageFor` function, and a DOM-only flow client. The
rail renders visible stage labels, current/upcoming/completed text, and a
plain-language boundary note. It uses no external assets and no adapter data.

## Educational and replay boundaries

The rail adds no causal claim and no debrief content. It must not be recorded as
simulation history, state hash input, replay content, audio classification, or
an outcome. A replay of the same local envelope may render the same stage only
when the same local handoff state is supplied.

## Risks and controls

- Risk: the rail could imply a host operation succeeded before its response.
  Control: update only after the existing client receives the expected result.
- Risk: two drafts could be read as two valid actions. Control: label this as a
  local review threshold; host validation remains authoritative.
- Risk: a generic progress bar could flatten campaign semantics. Control: keep
  the stage vocabulary competitive-first-month-specific and do not wire it into
  campaign coverage clients.
