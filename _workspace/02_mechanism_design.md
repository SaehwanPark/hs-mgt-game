# Mechanism Design - Month-Summary Clarity

## Interface & Data Boundary
- **Input**: `CompetitiveTransition` containing prior state, next state, events, effects, and aggregated actions.
- **Output**: `Vec<String>` returned by `resolution_summary_lines` to be printed in the CLI loop.

## Vocabulary & Formatting Rules
- **Player commands resolved**: Detailed format string per command variant mapping to CLI input grammar (e.g. `recruit role=nurse headcount=2`, `hold`).
- **Public actions logged**: List of rival/player actions categorized as public (e.g., access pledges, bed/clinic expansion projects over threshold). Prints `{system_name}: {summary}`.
- **Resolved effects**: Attributed changes from the current month resolution: `{source} → {metric} {delta}` (e.g. `recruit → staffed_beds +2`).
- **Starting resources**: Pre-turn overview of Cash, Political Capital, and Project monthly draws for the upcoming month.
