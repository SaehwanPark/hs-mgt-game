# Mechanism Design - Instructor Run Summary & Decision Quality Review

## 1. Stabilization Campaign Instructor Summary
We will add `instructor_run_summary(history: &History) -> Vec<String>` to generate a dedicated post-run report for the stabilization campaign.
For each transition in the committed history, it will output:
- **Turn index**: e.g., "Turn 0 → 1"
- **Reported (Observed) Access Index**: `transition.observation.reported_access_index`
- **True Prior Access Index**: `transition.prior.access_index`
- **Measurement Gap**: `reported_access_index - true_prior_access_index` (indicating how much the player's perception was distorted by noise/delay).
- **Player Action**: Descriptive summary of the command chosen by the player (e.g. access commitment, nursing coalition rate).
- **True Next Access Index**: `transition.next.access_index` (the actual resulting state).

## 2. Competitive Campaign Instructor Summary
We will add `competitive_instructor_summary(history: &CompetitiveHistory, human_system_id: u32) -> Vec<String>` (or implement it directly as part of `competitive_debrief`).
For each month:
- **Month name**: e.g., "Month 1"
- **Player Batch**: The commands submitted by the player system.
- **Rivals True Actions**: List each rival system's commands and explicitly show their visibility:
  - Public commands: labeled as "(publicly disclosed)"
  - Private commands target-monitored by the player: labeled as "(observed via monitor)"
  - Private commands NOT monitored: labeled as "(unobserved by you - REVEALED FOR INSTRUCTOR REVIEW)"
- **Rival Rationales**: Expose the private rationales of each rival system for that month, labeled as "(unobserved during play - REVEALED FOR INSTRUCTOR REVIEW)".

## 3. CLI Display
- In the stabilization campaign, the summary is printed immediately after the standard educational debrief.
- In the competitive campaign, the competitive debrief is printed when the three-month preview completes.

## 4. MCP Display
- The MCP session end endpoint will return the enhanced debrief lines.
