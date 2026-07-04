# Domain QA - Month-Summary Clarity (Pass 3)

## Status
- **Review**: `fix`
- **Details**: The formatting changes introduce two notable issues: a display bug that duplicates the system name in public action entries, and a logical/information-leak bug that prints a flat, un-attributed list of effects containing both the player's and all rivals' effects (including private actions).

## Reviewed Inputs
- `src/competitive/resolution.rs` (working branch changes)
- `_workspace/02_mechanism_design.md`

## Findings

### Finding 1: Duplicated System Name in Public Action Entries (Logical/Formatting Bug)
In `resolution_summary_lines`, the public actions log entries are printed as:
```rust
lines.push(format!("  • {}: {}", name, entry.summary));
```
However, in `src/sim/transition_competitive.rs`, all public action logs are already formatted with the system name prefixed inside `entry.summary` (e.g., `"{system_name}: recruiting {headcount} {role:?} staff"`). This results in redundant CLI output:
```
  • Northlake Health: Northlake Health: recruiting 2 Nurse staff
```
This is a minor cosmetic and formatting bug.

### Finding 2: Information Leak and Confusion in Flat "Resolved Effects" (High Severity Logical Bug)
In the competitive campaign, `transition.effects` collects `AttributedEffect` entries for **all** systems (human + AI rivals) in a single shared vector. 
Because `AttributedEffect` does not store `system_id` or system name, displaying these in a flat list:
```rust
for effect in &transition.effects {
  let sign = if effect.delta >= 0 { "+" } else { "" };
  lines.push(format!("  • {} → {} {}{}", effect.source, effect.metric, sign, effect.delta));
}
```
leads to two critical issues:
1. **Information Leak**: It prints cash/resource and metric changes caused by rivals' *private* actions (e.g., investment below the public threshold, private recruitment), violating the design boundary that rivals' private actions must remain hidden.
2. **Player Confusion**: Since the list is un-attributed, a player who chose `Hold` (cost 0) might see `action cost → cash -25` (from a rival's investment) and mistakenly believe their own cash was deducted.

## Required Fixes

1. **Remove Duplicated Prefix**: Change the public actions loop in `resolution_summary_lines` to format only `entry.summary`:
   ```rust
   lines.push(format!("  • {}", entry.summary));
   ```
2. **Handle Resolved Effects Properly**: 
   - **Option A (Recommended)**: Remove the raw `transition.effects` print loop entirely from `resolution_summary_lines` for competitive campaigns. The player already gets their own resolved commands list, their starting resources for next month, and public events. Displaying un-attributed global effects is confusing and leaks private data.
   - **Option B**: If metric deltas are needed, compute them explicitly and securely for the human system by comparing `transition.prior.human_system()` and `transition.next.human_system()`.

## Residual Risks
- Ensure that removing/updating `transition.effects` printing in `resolution_summary_lines` does not affect any existing test assertions.

## Verification Evidence
- `cargo test` passes successfully (242 tests).
- `cargo clippy --all-targets -- -D warnings` compiles without warnings.
