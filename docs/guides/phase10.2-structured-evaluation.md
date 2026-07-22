# Phase 10.2 structured visual/audio evaluation protocol

Status: ready for authorized human evaluation; no participant result is recorded
by this protocol artifact.

## Purpose and boundaries

Evaluate whether the first-month `competitive-regional-v1` presentation helps
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

Recruit across the roadmap groups: project contributors, strategy-game players,
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
until authorized reviewers inspect the findings and evidence.

## Evidence limits

This protocol prepares human evaluation. No participant results are included.
Preparation does not establish legal clearance, universal accessibility,
clinical validity, policy forecasting accuracy, or educational effectiveness.
Any release or human-approval decision remains separately authorized.
