# ADR-0009: AI-Agent Playtest Validation Path

**Status:** Accepted  
**Date:** 2026-06-30  
**Deciders:** Project maintainer and implementation agent

## Context

The roadmap previously expected structured external human playtests during
Phase 7. Recruiting external players is difficult for the current project and
is not feasible within the current personal-project budget. The repository has
a local stdio MCP server plus Python automation for bounded agent play of both
implemented campaign slices.

The project still needs reproducible evidence for command comprehension,
strategic diversity, pacing risks, exploit discovery, causal transparency, and
debrief coherence before expanding campaign scope.

## Decision

Use AI-agent and sub-agent playtests as the active validation path for the
current roadmap. External human recruitment is not a Phase 7 dependency, and
no project budget is reserved for recruitment, incentives, or human-subject
study administration.

Agent playtests must use the MCP interface or an equivalent documented adapter
that preserves actor-visible observations, validated commands, transition
history, state hashes, and debrief outputs. Findings must label which evidence
comes from simulated players and must not claim measured human learning,
classroom effectiveness, empirical calibration, or policy forecasting validity.

## Consequences

- Phase 7 planning can proceed without human participant recruitment.
- Playtest findings become more reproducible because seeds, profiles, prompts,
  observations, commands, and histories can be captured.
- The project can run more strategy profiles and stress cases than small human
  sessions would allow.
- Educational claims are narrower: agent evidence can inspect debrief coherence
  and decision traces, but cannot prove actual learner outcomes.
- Human-subjects governance is not part of routine validation unless a future
  separately funded and approved human evaluation plan is created.

## Alternatives Considered

| Alternative | Reason not chosen |
| --- | --- |
| Keep external human playtests as the active Phase 7 gate | Recruitment burden blocks near-term validation and iteration |
| Treat agent playtests only as a temporary proxy | The project has an implemented MCP interface and can make agent runs the reproducible default |
| Use terminal scraping instead of MCP | Less structured, harder to preserve observations and errors, and duplicates the MCP adapter |
| Claim agent runs validate educational outcomes | Overstates the evidence and conflicts with the project's assumption-visibility principle |

## Validation

- `docs/validation/playtesting.md` defines required run artifacts, profiles,
  rubric dimensions, synthesis format, and evidence limits.
- `docs/guides/mcp-playtesting-guide.md` remains the operational runbook for the
  existing MCP automation.
- Future playtest findings should cite campaign, seed, difficulty, agent
  profile, and evidence artifacts.
