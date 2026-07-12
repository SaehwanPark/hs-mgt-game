# Final Handoff - Affiliation Runtime Boundary Proposal v0.12.7

## Result

- Reconciled the affiliation-first design gate with the existing opt-in
  `regional-affiliation-v1` runtime.
- Confirmed six minimum contracts: true state, actor observation, resolved
  inputs, deterministic transition evaluation, history/replay, and debrief.
- Audited source markers across the ADR, model, observation, input resolution,
  transition, replay, MCP, scenario, and debrief boundaries.
- Validated the committed v0.12.2 artifact: 9/9 complete runs, 54/54 stages,
  and commitments/alternatives/assumptions present in all 54 observations.
- Authorized no new runtime change. Broader acquisition and consolidation
  remain evidence-gated.

## Version boundaries

- Package: `0.12.7`
- Change surface: proposal artifact, source-boundary audit, focused Python
  tests, and canonical documentation
- Rust runtime behavior, commands, scenario fields, state hashes, replay
  formats, and competitive campaign behavior: unchanged

## Branch and PR handoff

- Base branch: `main`
- Working branch: `feat/affiliation-runtime-boundary-v0.12.7`
- PR: to be opened after final local verification
- Domain QA: Pass.
- Review passes: pending PR opening and post-open review.
- Merge state: pending PR review and merge.

## Verification

- Proposal source markers: supported across all required boundaries.
- Existing affiliation artifact: 9/9 complete runs, 54/54 stages, zero
  validation failures, and 54/54 observations with typed context.
- Focused proposal tests, 308 Rust tests, 199 Python tests, formatting, clippy,
  CLI smoke, golden, proposal audit, and diff checks: passed locally.

## Stop condition

After this proposal merges, no Present item remains authorized. A new runtime
slice requires concrete playtest, instructor, scenario, domain, or release
evidence identifying an unexplained gap and a new bounded proposal.
