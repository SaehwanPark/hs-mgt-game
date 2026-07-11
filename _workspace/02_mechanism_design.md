# Mechanism Design - Project-Recovery Use Evidence

## Goal and Roadmap Phase

Phase 7 validation: test actor-visible recovery use while preserving the
deterministic competitive transition boundary.

## Slice Boundary

- Included: existing project-limit rejection, plain error text, unchanged
  observation, response-conditioned `hold`, history, hashes, and debrief.
- Excluded: new commands, actors, rules, scenario fields, runtime hints, or
  MCP schema changes.

## Capture Design

- Seeds: 42, 43, and 44; difficulty: Hard; campaign: competitive-regional-v1.
- Month 4: accept `clinic_network` project.
- Month 6: accept `asc_unit` project.
- Month 7: submit `neurology_unit` project and expect
  `too_many_concurrent_projects`.
- After rejection: verify the same turn and observation, then select `hold`
  using only the plain error and visible `ClinicNetwork`/`AscUnit` state.

## Determinism and Replay Notes

The runner must build the local MCP binary, preserve the accepted command
stream, and match v0.10.55 state hashes for every seed. Generated artifacts
must be stable across regeneration.

## Educational and Domain Limits

The capture supports response-surface traceability only. It must not claim
human comprehension, learning, advice value, balance, winnability, calibration,
or policy validity.
