# Phase 10.2 structured visual/audio evaluation protocol

Status: optional external-feedback preparation; no participant result is recorded
by this protocol artifact and no technical promotion depends on it.

## Purpose and boundaries

Evaluate, if external feedback is later requested, whether the first-month
`competitive-regional-v1` presentation helps
people identify institutions, facilities, visible pressures, and consequence
chains without exposing hidden state or making audio necessary. The protocol
evaluates the existing technical slice; it does not approve assets, establish
legal clearance, or substitute for accessibility, educational, or domain
review.

Sessions must use fictional repository content, a seeded run, and the host’s
actor-visible presentation. Do not collect names, contact details, health
information, private game state, or identifying recordings in the repository.
Record only consented task outcomes, anonymized role/category, and bounded
feedback needed for revision.

## Participants and session shape

If a separately authorized study is chosen, recruit across the roadmap groups: project contributors, strategy-game players,
health-policy/management experts, accessibility-oriented reviewers, and
first-time users. A facilitator may stop a task for discomfort, fatigue,
accessibility barriers, privacy concerns, or information-boundary confusion.

Each session has:

1. orientation without teaching the intended answer;
2. first-month play from session start through committed resolution;
3. recognition and consequence-tracing tasks;
4. accessibility and audio preference tasks;
5. short quantitative ratings and optional qualitative comments;
6. facilitator coding and participant debrief.

## Task protocol

The canonical task IDs and prompts are in
`docs/evaluation/phase10.2-evaluation-protocol.json`. Facilitators must use the
same task order and record “not observed” when a task is skipped or a response
cannot be interpreted. Do not reveal private rival actions, future outcomes, or
an optimal strategy while facilitating.

### First-session tasks

- Start a seeded competitive session and identify what is visible before the
  first action.
- Draft at least two actions, inspect validation/cost/uncertainty, submit them,
  review resolution, and describe what refreshed.
- Use skip/review and locate committed history or replay context.

### Recognition tasks

- Identify Riverside, Northlake, and Summit from labels and visible identity
  tokens.
- Identify one facility, one project/capacity signal, one pressure signal, and
  one public rival observation.
- Point to the source/status or missingness text for each selected item.

### Consequence-tracing tasks

- Trace one drafted action through validation, submission, resolution, and a
  visible consequence without predicting hidden outcomes.
- Explain which information was public, stale, uncertain, missing, or committed.
- Reconstruct the first-month sequence from the written resolution stages.

### Accessibility and audio tasks

- Complete the recognition and tracing tasks with keyboard navigation and text
  scale increased.
- Repeat a task in reduced-motion mode and confirm that written content remains
  reviewable after skipping.
- Try full audio, cues-only, mute, reduced notifications, unavailable audio,
  and written equivalents; report preference, usefulness, fatigue, and whether
  any meaning was lost without sound.

## Measurement and coding

Use the bounded 1–5 ratings in the JSON protocol for recognition, legibility,
consequence comprehension, information density, cognitive load, animation
usefulness, audio usefulness, audio fatigue, game identity, accessibility, and
trust in information boundaries. Ratings are participant feedback, not policy
outcomes or model validation.

Classify each finding as exactly one of:

- defect: a reproducible failure, confusion, accessibility barrier, or
  information-boundary violation;
- preference: a subjective improvement request that does not violate the
  contract;
- scope expansion: a request for a new feature, campaign, asset, or authority
  outside the current slice.

Enter only anonymized findings in
`docs/evaluation/phase10.2-revision-log.md`. Leave the go/no-go decision blank
for external feedback; it does not gate the automated technical queue.

## Evidence limits

This protocol prepares optional human evaluation. No participant results are
included and no technical work waits for them.
Preparation does not establish legal clearance, universal accessibility,
clinical validity, policy forecasting accuracy, or educational effectiveness.
Any release or human-approval decision remains separately authorized and outside
the automated GUI progression policy.

## Phase 13.2 pilot-preparation addendum

**Status:** preparation complete for authorized human planning; no participant
result, recording, or go/no-go decision is included here.

### Facilitator preflight

- Use an exact repository checkout and build the live host before the session;
  the GUI binds to loopback and is not a network multiplayer service.
- Use the documented `competitive-regional-v1`, seed `42`, and Normal
  difficulty first unless the session plan records another bounded choice.
- Confirm that all examples remain fictional and that the facilitator will not
  teach hidden rival actions, future outcomes, or an intended optimal strategy.
- Obtain explicit consent before collecting any feedback, screenshot, or
  recording. A participant may skip a task or stop without explanation.

### Classroom hardware assumptions

- One facilitator-controlled local host and one learner-facing Chromium desktop
  browser on the **same computer** per active run; the loopback host cannot
  serve a browser on another computer. In a multi-device room, use one
  host/browser pair per learner or show one facilitator-controlled session;
  the GUI currently supports one competitive session flow, not classroom
  multiplayer.
- Keyboard and pointing-device access, a readable desktop display, and a
  current Chromium-based browser with JavaScript modules enabled.
- The repository's bounded browser proxy uses a 1024×768 viewport. This is a
  layout-planning baseline, not a real-device, battery, thermal, or frame-rate
  certification.
- Audio is optional. A muted session must remain fully playable; if audio is
  enabled, use headphones or a facilitator-controlled speaker and avoid
  assuming that every learner can hear it.
- Build/dependency resolution should be completed before class. The live host
  itself is local and does not require runtime asset or network downloads.

### Audio and accessibility guidance

- Begin with audio off and explain that every cue has a written equivalent.
  Offer cues-only, mute, reduced notifications, and independent channel
  volumes; stop or mute audio when it causes distraction or fatigue.
- Offer the existing **Reduced motion**, **Large** text, and optional cue
  explanation settings before the first task. Keep written results visible and
  allow keyboard navigation, skip, review, extra time, or a task retry as
  accommodations.
- A dedicated **Low-distraction mode** is available in the settings panel. It
  applies the existing recipe: Reduced motion on, Large text, cue explanations
  on, audio muted, and reduced notifications enabled. Turning it off restores
  prior local presentation/audio preferences. This is still not a claim of
  universal accessibility.
- Record only the accommodation offered or the observed barrier category; do
  not record a diagnosis, health information, or identifying detail.

### Screenshot, recording, and feedback handling

- Screenshots and recordings require separate explicit consent. Do not capture
  the browser URL, session IDs, participant names, private notes, or hidden
  state; crop or redact any accidental capture before local review.
- Do not commit participant media or raw responses to the repository. Use the
  structured instrument at
  `docs/evaluation/phase13.2-pilot-feedback-instrument.json` and record only
  anonymized task outcomes, bounded ratings, classified findings, and the
  separate feedback/screenshot/recording consent statuses. A declined or
  not-applicable media consent must not be followed by capture.
- Classify a finding as `defect`, `preference`, or `scope-expansion`. Keep the
  decision field pending until an authorized reviewer inspects the evidence.

This addendum prepares a pilot workflow. It does not establish measured
learning, classroom effectiveness, human accessibility, audio usefulness,
legal clearance, or public-release readiness.
