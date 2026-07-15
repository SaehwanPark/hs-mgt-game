# Request Summary — Visual/audio first-month contract audit v0.12.30

## User objective

Continue the SPEC/proposal visual and audio upgrade through bounded,
evidence-gated slices. After the merged Phase 13 rail, verify the complete
technical first-month contract against the proposal and close the bounded
visual/audio sequence only if current source and focused tests prove every
required handoff.

## Selected slice

Add a dependency-free, deterministic contract audit for the existing
`competitive-regional-v1` first-month experience. Use it to record source/test
evidence for launch, inspection, bottleneck and rival/payer context, two-action
review, canonical submission, resolution metrics/causal effects, optional audio,
and continuation. Align `SPEC.md` and release documentation with the result.

## Required behavior

- The audit must emit stable machine-readable JSON with one result per
  first-month contract obligation and explicit evidence paths.
- A passing result must prove source markers and focused test markers for every
  required handoff; missing source, test, or boundary evidence must fail closed.
- The audit must report technical/interface-task evidence separately from
  human usability, lived accessibility, learning, engagement, calibration,
  balance, policy-validity, and domain-expert questions.
- The audit must verify the browser boundary remains presentation-only and does
  not add simulation, network, hidden-state, or GUI-only outcome logic.
- `SPEC.md`, the changelog, version projections, and a durable audit document
  must describe the bounded sequence as closed while retaining explicit
  deferred work.

## Explicit non-goals

- No Rust/MCP DTO, command, transition, stochastic, history/hash/replay,
  debrief, campaign, browser transport, dependency, or runtime behavior change.
- No browser-owned simulation state, client-side cost/outcome formula,
  downloaded asset, audio-source change, network call, or new phase beyond the
  bounded audit/closure artifact.
- No claim of human usability, lived accessibility, learning, engagement,
  calibration, balance, policy validity, or domain-expert agreement.
