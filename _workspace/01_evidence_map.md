# Evidence Map

## Inputs

- Scripted seed-variation findings from `docs/playtest-findings-v0.1.51.md`.
- Scripted naive-profile findings from `docs/playtest-findings-v0.1.52.md`.
- Free-form first-time findings from `docs/playtest-findings-v0.1.54.md`.
- Free-form profile synthesis findings from
  `docs/playtest-findings-v0.1.55.md`.
- Active MCP playtest protocol and guide.

## Evidence-Backed Claims

- Scripted and free-form simulated-agent profiles can complete both current
  campaigns without validation failures.
- Stabilization outcomes are strongly profile-driven: fiscal caution preserves
  cash, access/capacity growth improves access and trust, and naive low-
  complexity play weakens community trust.
- Competitive outcomes show meaningful cash, bed, access, and workforce-trust
  tradeoffs, but the short preview produces a narrower access range than cash
  and capacity ranges.
- Monitoring is consistently understood by tested profiles; project commands
  have not yet appeared in the captured three-month competitive profiles.
- Free-form profiles can use committed history and debrief output for causal
  explanation without relying on hidden implementation details.

## Design Abstractions

- Profiles are simulated-agent personas, not measured human user segments.
- The diagnostic report is an analysis artifact, not an analytics platform or
  equilibrium model.
- Seed 42 free-form evidence and seeds 42-44 scripted evidence are bounded
  validation samples, not stochastic characterization.
- The three-month competitive preview is a hardening and validation surface, not
  the full 24-month campaign target.

## Unresolved Questions

- Whether passive competitive play reflects command-help/report guidance
  weakness, short preview horizon, or reasonable cash-preservation strategy.
- Whether project commands need clearer guidance, longer horizon evidence, or
  no change in the bounded preview.
- Whether larger profile/seed matrices justify dedicated diagnostics tooling.
- Whether competitive stochastic sensitivity should become a focused design
  target after the bounded preview.
