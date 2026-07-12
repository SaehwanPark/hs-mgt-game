# Operational Coding Plan - Workforce Capacity Difficulty Design Gate v0.12.5

## Task restatement

Turn the v0.12.4 candidate workforce-capacity signal into a bounded observation
contract decision: determine whether the current MCP surface is sufficient and,
if not, specify the smallest typed-field projection follow-up.

## Current understanding

- v0.12.4 reports workforce-capacity bottlenecks rising 0/15/30/160 across
  Easy/Normal/Hard/Expert in deterministic simulated-policy evidence.
- `PlayerObservation` contains Riverside staffing counts and physical capacity
  fields, but `format_competitive_observation` does not render them.
- Workforce trust, nursing-vacancy wording, prior operations, labor guidance,
  consultant options, and debrief attribution are already visible.

## Assumptions

- The typed observation is the authoritative safe source.
- The smallest useful follow-up is two presentation lines, not a derived
  effective-capacity or role-target model.
- The next implementation must rerun the unchanged v0.12.4 matrix and compare
  history/state hashes exactly.

## Minimal implementation plan for the next gate

1. Render `Staffing:` and `Physical capacity:` lines from `PlayerObservation` in
   the MCP competitive observation.
2. Add a session-boundary Rust test for the exact safe labels and values.
3. Rerun the v0.12.4 all-tier/Expert-compatible observation matrix and require
   no transition, history, state-hash, replay, command, or golden changes.
4. Keep runtime difficulty/balance promotion deferred and record whether the
   projection gap closes.

## This v0.12.5 design-gate implementation

- Add a deterministic JSON design contract and Markdown diagnostics.
- Add focused Python validation for safe fields, excluded fields, and stable
  routing.
- Update SPEC, changelog, README, architecture, roadmap, lessons, findings,
  and final handoff; bump package metadata to `0.12.5`.

## Files and functions likely to change in the next implementation

- `src/mcp/session.rs`: `format_competitive_observation` and session tests.
- A new v0.12.6 post-fix evidence artifact and focused Python tests.

Files for this design gate:

- `_workspace/experiments/v0.12.5-workforce-capacity-design/`.
- `tests/test_workforce_capacity_design.py`.
- `docs/workforce-capacity-design-v0.12.5.md` and related governance docs.

## Acceptance criteria

- The design artifact says `observation_context_follow_up_required: true`.
- It names exactly the safe typed fields to render and the hidden fields to
  exclude.
- It states that no difficulty, transition, balance, scoring, or winnability
  change is authorized by this gate.
- Domain QA passes and all repository checks pass.

## Stop conditions

- Stop if the proposed field requires true state not present in
  `PlayerObservation`.
- Stop if the projection would reveal hidden targets, future outcomes, or rival
  private state.
- Stop if the implementation would require changing transition or hash code.

## Risk label

Risk: Low.

Reason: This gate produces a bounded, testable observation contract and no
runtime behavior change.
