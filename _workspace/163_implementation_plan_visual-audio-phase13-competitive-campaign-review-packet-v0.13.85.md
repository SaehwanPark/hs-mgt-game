# Implementation Plan — Phase 13.1 Competitive Campaign Review Packet v0.13.85

## Target slice

Prepare a source-bound technical packet for the open `Competitive campaign
coverage complete` roadmap item. The packet will make a bounded full-campaign
review actionable across the existing 24-month competitive host path without
claiming that participants understood the campaign or approving expansion.

## Audience and job to be done

- Primary audience: strategy-game players and health-policy/management
  reviewers inspecting the competitive campaign.
- Supporting audience: accessibility-oriented reviewers and facilitators.
- Job: play or inspect early, middle, and terminal competitive states; identify
  facility and pressure changes; trace visible committed consequences; use
  history/replay/checkpoint views; and report quality, comprehension, and
  friction without inferring hidden state.

## In scope

1. Bind the host-owned 24-month competitive campaign and every named current
   presentation surface.
2. Bind the four player facility groups, eleven capacity labels, operational
   overlays, event cues, music states, history, replay, checkpoint, and
   terminal debrief evidence already in the repository.
3. Define early/mid/terminal participant tasks, success observations, review
   questions, accessibility/fallback checks, and a pending-human decision
   record.
4. Add a fail-closed validator and update roadmap, SPEC, request, contract,
   QA, domain QA, handoff, lessons, changelog, and version metadata.
5. Bump the project patch version to 0.13.85 and regenerate deterministic
   credits/notices/runtime metadata.

## Explicitly out of scope

- Runtime, simulation, route, browser-authority, persistence, asset, audio,
  screenshot, or release-manifest changes.
- A 24-frame screenshot golden set, cross-browser/device certification,
  participant data, educational findings, legal clearance, or expansion/go-no-
  go approval.
- Repeating the v0.13.84 first-session packet or closing its separate human
  gate.

## Planned artifacts

- `docs/evaluation/phase13.1-competitive-campaign-review-packet.json`
- `tests/test_phase13_1_competitive_campaign_review_packet.py`
- A v0.13.85 roadmap evidence section and changelog entry.

## Verification and handoff gate

- Full Python and Rust suites, formatting, clippy, documentation links,
  release metadata, asset/security/offline/browser checks, and focused packet
  tests pass.
- The validator proves exact campaign limits/surfaces, ledger parity,
  source-marker bindings, terminal evidence, authority/fallback boundaries,
  release exclusion, and pending-human fields.
- Obtain exactly one medium-effort code review, resolve actionable findings,
  then commit, push, open/ready the PR, wait for CI, merge to `main`, and
  delete the temporary branch locally and remotely.
