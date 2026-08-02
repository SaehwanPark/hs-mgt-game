# Implementation Plan — Playtest history evidence closure v0.14.11

## Target slice

Close the concrete `command_without_history` finding in the GUI playtest
matrix. A committed decision capture must retain the host-reported transition
turn, state hash, and transition count from the visible envelope; the analyzer
must continue to flag captures that omit that evidence.

## Scope

- expose the existing visible-envelope recorder helper for deterministic
  regression coverage;
- add the missing committed history observation to the stabilization matrix
  fixture;
- preserve the analyzer's missing-history finding through a synthetic regression
  case;
- update current project, release, contract, QA, handoff, and lesson documents.

## Non-goals

- no simulation, stochastic input, host route, DTO/schema, persistence, replay,
  browser-authority, campaign, asset, audio, or browser-support change;
- no inference of commit status from a local command event;
- no human learning, usability, accessibility, legal, policy, calibration, or
  public-release claim.

## Verification target

Focused playtest/analysis tests, JavaScript syntax, full Python and Rust suites,
documentation currentness and links, release metadata, asset/security/release
checks, Chromium-default/offline/loading/device checks, presentation contracts,
one medium-reasoning code review, and the authorized PR/merge cleanup loop.
