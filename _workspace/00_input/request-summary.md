# Request Summary

## Scope

Hardening competitive campaign guidance, command help, and debriefing to resolve the gaps identified in the v0.1.56 playtest diagnostics. Specifically:
1. Expand the help text for `PromptContext::CompetitiveCommand` in `src/cli/guidance.rs` to display detailed descriptions of each competitive command's effects, Action Point (AP) costs, cash costs, and political capital costs.
2. Update the monthly command prompt printing in `src/cli/campaign.rs` to clearly notify the user that typing `?` or `help` displays the detailed command manual.
3. Update the `competitive_debrief` function in `src/mcp/session.rs` to add a strategic lesson about capital projects (AP costs, monthly cash draws, duration, and concurrency limits).

## Non-Goals

- No changes to core simulation transition logic, model structures, or validation thresholds.
- No changes to scenario TOML files or the campaign selection flow.
- No changes to the stabilization campaign's guidance, help, or debrief.
- No changes to golden hashes (the golden hashes for seed 42 must remain identical to main).
- No new MCP endpoints or DTO changes.

## Sources

- `SPEC.md`
- `docs/playtest-findings-v0.1.56.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `src/cli/guidance.rs`
- `src/cli/campaign.rs`
- `src/mcp/session.rs`

## Expected Files

- `src/cli/guidance.rs`
- `src/cli/campaign.rs`
- `src/mcp/session.rs`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`

## Validation Target

- Extended competitive help text passes the existing `help_text_avoids_actor_outcome_spoilers` test.
- All 230+ cargo tests run and pass.
- Stabilization and competitive campaign simulation outcomes (e.g. golden hashes) remain stable.
- `cargo fmt --check` passes.

## Global Skills Needed

- `preferred-workflow` for PR, branch, and code-review loop.
- `plan-designer` for defining the operational coding plan.
- `simple-code-writer` for editing the Rust files.
- `spec-driven-developer` for SDD index and changelog updates.
- `code-reviewer` for three independent review passes.
