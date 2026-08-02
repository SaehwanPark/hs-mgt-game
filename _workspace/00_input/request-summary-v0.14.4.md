# Request Summary — Progressive workspace navigation gating v0.14.4

## Authorized outcome

Continue the GUI-first workspace-task-quality queue with one bounded interaction
improvement: keep Setup/Brief/Decide/Resolve/Review navigation aligned with the
host-backed task progression so users can revisit completed workspaces but cannot
jump into a future workspace before its visible handoff is ready.

## Target slice

- Track unlocked workspace stages in the existing browser-local workspace
  controller and unlock them from the existing host/session events.
- Keep Setup and completed/current workspaces available for review; gate only
  future workspace navigation and expose its disabled state with native button
  semantics and an explanatory label.
- Preserve programmatic event routing, primary handoff buttons, all three
  campaigns, refresh/retry behavior, keyboard focus, reduced motion, and the
  browser's presentation-only authority boundary.

## Non-goals

- No new route, DTO/schema, simulation rule, persistence format, browser storage,
  asset/audio file, campaign, action protocol, or host authority.
- No client-side legality, outcome, true-state, replay, or debrief inference.
- No claim of human usability, learning, lived accessibility, browser/device
  certification, provenance/legal approval, or public-release readiness.

## Validation target

Focused Node/Python workspace-controller and source-contract tests; full Rust,
Python, documentation, asset, browser-default, and presentation checks; exactly
one medium-effort code review; authorized PR/merge and temporary-branch cleanup.

## Evidence limits

Passing checks establish only that navigation follows the declared event-driven
task boundary and preserves presentation fallbacks. They do not establish human
comprehension or accessibility in lived use.
