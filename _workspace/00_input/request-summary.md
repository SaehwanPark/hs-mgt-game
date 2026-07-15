# Request Summary — Visual/audio Phase 13 first-month continuity v0.12.29

## User objective

Continue the SPEC/proposal visual and audio upgrade through bounded, evidence-
gated slices. After Phase 12, select and implement the next smallest gap in the
first polished `competitive-regional-v1` month while preserving the existing
host, simulation, observation, history, replay, and audio boundaries.

## Selected slice

Add a presentation-only first-month path rail that makes the existing launch,
inspection, action drafting, host validation, submission, resolution, and
refreshed-observation handoffs legible as one continuous workflow.

## Required behavior

- Start or load remains host-authoritative.
- The rail uses local client progress only; it does not infer a policy outcome,
  action legality, stochastic result, or hidden state.
- The action client must show the draft/validation/submission handoff without
  limiting the existing ability to add, revise, or remove actions.
- Resolution and refreshed presentation remain separate host reads; both must
  be available before the rail says the month is ready to continue.
- Rejected or failed host operations keep the current session and path state
  recoverable rather than fabricating progress.
- Every step has visible text and semantic state; color or motion is optional.

## Explicit non-goals

- No Rust/MCP DTO, command, transition, stochastic, history/hash/replay,
  debrief, campaign, browser transport, dependency, or asset change.
- No browser-owned simulation state and no client-side cost or outcome formula.
- No claim of human usability, lived accessibility, learning, engagement,
  calibration, balance, policy validity, or domain-expert agreement.
