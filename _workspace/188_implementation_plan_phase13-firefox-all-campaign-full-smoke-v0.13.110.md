# Implementation plan: v0.13.110 Firefox all-campaign full-transition smoke

## Target slice

Extend the existing loopback-only Firefox/Marionette probe from competitive
full-campaign smoke to the five-stage stabilization and six-stage regional
affiliation host-shaped decision sequences.

## Design

1. Add one probe helper for the visible campaign coverage form. For each
   stage, fill only the rendered numeric fields with their visible minimum or
   zero/default, click the existing submit control, and wait for the exact
   host autosave count and committed history count.
2. After each campaign reaches its terminal coverage state, use the visible
   end-session control and record the host terminal history/debrief count and
   final state hash. Keep competitive smoke unchanged.
3. Extend packet validation and regression tests with explicit stabilization
   and regional-affiliation full-transition observations. Keep browser support
   certification, audio decoder review, WebKit, device, human, and release
   boundaries false.
4. Add one source-bound all-campaign technical check to the consolidated audit,
   bump the patch version to 0.13.110, and update the roadmap, guide, changelog,
   lessons, generated credits, and handoff.

## Public contracts and compatibility

No runtime, simulation, browser-support-policy, asset, audio, or save-format
contract changes are expected. The probe and JSON packets gain source-bound
technical evidence fields only. Firefox remains `not-certified` under the
canonical browser policy.

## Verification

- Run the rebuilt GUI host and the Firefox probe; require competitive 24,
  stabilization 5, and regional affiliation 6 host-backed transitions.
- Run focused packet/audit/release tests and the full Python suite.
- Run `cargo fmt`, Clippy, serial Rust tests, audit/device/release checks, and
  `git diff --check`.
- Obtain exactly one Archimedes code review at medium reasoning effort before
  merging.

## Non-goals and stop conditions

- Do not automate unsupported controls, change the browser matrix, or infer
  human review from the automated run.
- Stop and report if a rendered campaign form changes, a transition is not
  host-backed, or required runtime/permission evidence cannot be recorded
  honestly.

## Risk

Medium: two campaign-specific asynchronous coverage contracts must be driven
without confusing a rendered terminal debrief or stale form with a committed
host transition.

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising.
