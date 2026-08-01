# Implementation plan: v0.13.109 Firefox competitive full-campaign smoke

## Target slice

Extend the existing loopback-only Firefox/Marionette probe from launch/read
continuity to one complete competitive regional campaign using only the
visible GUI controls and host-backed responses.

## Design

1. Add a probe helper that uses the visible `hold` action form, host validation,
   and host submission controls for exactly 24 months. Wait for each committed
   history row and autosave status before recording the next month.
2. End that same session through the visible end-session control and record the
   host terminal history/debrief counts and final state hash. Keep the existing
   all-campaign launch smoke after this path.
3. Extend packet validation and regression tests with an explicit
   `firefox_competitive_full_campaign_smoke_complete` field while keeping
   `firefox_full_campaign_certification_complete` and all external gates false.
4. Add the packet as a separate technical check in the consolidated audit,
   bump the patch version to 0.13.109, and update the roadmap, guide, changelog,
   and lessons with the evidence boundary.

## Public contracts and compatibility

No runtime, simulation, browser-support-policy, asset, audio, or save-format
contract changes are expected. The probe and JSON packets gain source-bound
technical evidence fields only. Firefox remains `not-certified` under the
canonical browser policy.

## Verification

- Run the rebuilt GUI host and the live Firefox probe; require 24 committed
  turns, 24 history/replay rows, 24 autosave observations, and a non-empty
  host debrief.
- Run the focused Firefox packet/audit tests and all Python tests.
- Run `cargo fmt`, Clippy, serial Rust tests, audit/device/release checks, and
  `git diff --check`.
- Obtain exactly one Archimedes code review at medium reasoning effort before
  merging.

## Non-goals and stop conditions

- Do not automate other campaigns, change the browser matrix, or infer human
  review from the automated run.
- Stop and report if the host changes the visible action or terminal contract,
  if any transition is not host-backed, or if required runtime/permission
  evidence cannot be recorded honestly.

## Risk

Medium: the probe spans browser DOM events, asynchronous host transport,
autosave, replay/history refresh, and terminal rendering, so a false positive
could overstate continuity if counts are not tied to host-visible updates.

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising.
