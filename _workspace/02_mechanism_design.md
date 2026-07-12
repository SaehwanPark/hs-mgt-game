# Mechanism Design

## Goal and Roadmap Phase

Phase 7 debrief traceability follow-up for the competitive campaign. This is a
reporting-surface correction, not a new simulation mechanism.

## Output Contract

For each committed competitive transition, `competitive_debrief` renders one
player-owned line inside the matching month section:

`Operating result: treated X/Y demand units (Z unmet); operating revenue R,
operating cost C, operating margin M.`

The values come from the human system in `transition.next`. The line is a
realized post-run outcome link and is kept separate from decision-time
observations, player commands, rival visibility, and global effect summaries.

## Boundaries

- Use the existing typed `CompetitiveTransition` and `HealthSystemState` fields.
- Keep the change inside the debrief layer; CLI and MCP consume the shared
  output without separate formatting logic.
- Do not derive or render rival operating values.
- Do not change transitions, stochastic inputs, hashes, replay formats, or
  public MCP DTOs.

## Validation

- Focused Rust coverage asserts exact player values and excludes rival sentinel
  values.
- MCP end-session coverage confirms the shared debrief contains the line.
- Full Rust/Python verification and the seed-42 golden test remain required.
