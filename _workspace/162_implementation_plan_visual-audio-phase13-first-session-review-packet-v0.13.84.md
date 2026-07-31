# Implementation Plan — Phase 13.1 First-Session Review Packet v0.13.84

## Target slice

Prepare a source-bound, participant-ready technical packet for the open
`First-session workflow complete` roadmap item. The packet will make a bounded
first-time-user evaluation actionable without claiming that a participant has
completed the flow or that accessibility, educational, or release decisions
have been made.

## Audience and job to be done

- Primary audience: a first-time local GUI player completing the competitive
  first-month path.
- Supporting audience: a facilitator who can provide setup, consent, stop, and
  recovery guidance without teaching hidden state.
- Job: launch or load a session, identify the next visible action, complete the
  host-mediated first-month handoffs, recover from a rejected or unavailable
  operation, and report comprehension and friction.

## In scope

1. Bind the seven source-defined competitive first-month stages.
2. Bind the five source-defined campaign-coverage orientation stages as a
   secondary recognition task.
3. Bind existing settings, written-equivalent, reduced-motion, audio-off, and
   recovery guidance.
4. Define participant tasks, success observations, review questions, and a
   structured pending-human decision record.
5. Add a fail-closed validator and update the roadmap, release notes, SPEC,
   handoff, request summary, presentation contract/QA, and lessons.
6. Bump the project patch version to 0.13.84 and regenerate deterministic
   credits/notices/runtime metadata.

## Explicitly out of scope

- Runtime, simulation, route, browser-authority, persistence, asset, audio,
  or screenshot changes.
- Participant data, interview findings, ratings, accessibility certification,
  educational conclusions, or public-release approval.
- Closing the separate competitive full-campaign coverage, provenance/legal,
  AI-generation, or debrief-visual human gates.

## Planned artifacts

- `docs/evaluation/phase13.1-first-session-review-packet.json`
- `tests/test_phase13_1_first_session_review_packet.py`
- A v0.13.84 roadmap evidence section and changelog entry.

## Verification and handoff gate

- Full Python and Rust suites, formatting, clippy, documentation links,
  release metadata, asset/security/offline/browser checks, and focused packet
  tests pass.
- The packet validator proves source markers, exact stage lists, recovery and
  accessibility boundaries, host authority, and pending-human fields.
- Obtain exactly one medium-effort code review, resolve actionable findings,
  then commit, push, open/ready the PR, wait for CI, merge to `main`, and
  delete the temporary branch locally and remotely.
