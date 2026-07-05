# Mechanism Design - Active Projects Detailed Observation

## Mechanism Summary
Provide the player with explicit, detailed information about their currently active (in-flight) capital projects during the competitive campaign.

## State to Observation Mapping
1. During observation derivation (`observe_for_human` in `src/sim/observe_competitive.rs`), query `world.effect_queue`.
2. Find all `PendingEffect` entries where:
   - `effect.system_id == human.system_id`
   - `effect.kind` is one of `BedsCapacity`, `OutpatientCapacity`, or `TechnologyQuality`.
   - `effect.kind` has a `project_draw` value of `Some(draw)`.
3. Map each qualifying `PendingEffect` to a descriptive string:
   - Identify the project label:
     - `BedsCapacity` -> `"Tower"`
     - `OutpatientCapacity` -> `"ClinicNetwork"`
     - `TechnologyQuality` -> Look at the `effect.summary` string. If it contains `"EhrCerner"`, label it `"EhrCerner"`. Otherwise, label it `"EhrEpic"`.
   - Compute remaining months: `remaining_months = effect.resolve_month.saturating_sub(observation_month)`.
   - Format: `"{label} ({remaining_months} mos left, ${draw}k/mo draw)"`.
4. Combine the descriptions:
   - If empty, return `"none"`.
   - Otherwise, join with `", "` (e.g. `"ClinicNetwork (8 mos left, $2k/mo draw), Tower (11 mos left, $10k/mo draw)"`).
5. Populate the `in_flight_projects` field of `PlayerObservation` with this detailed string.

## Acceptance Criteria
- Starting a project (e.g. `ClinicNetwork` budget 18) results in `In-flight: ClinicNetwork (8 mos left, $2k/mo draw)` being shown in subsequent turns of the campaign.
- Multiple active projects are listed simultaneously.
- Completed projects disappear from the list.
- All unit and campaign integration tests continue to compile and pass.
