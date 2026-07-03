# Domain QA Review

## Status

pass

## Reviewed Inputs

- `_workspace/00_input/request-summary.md`
- `src/cli/guidance.rs`
- `src/cli/campaign.rs`
- `src/cli/repl.rs`
- `src/mcp/session.rs`

## Findings

- **Guidance Hardening:** The expanded help text in `src/cli/guidance.rs` for `PromptContext::CompetitiveCommand` correctly lists resource costs (Action Points, cash, political capital) and delay/concurrency constraints for all 7 verbs (`hold`, `invest`, `recruit`, `monitor`, `negotiate`, `commit`, `project`).
- **Prompt Cueing:** The prompt message in `src/cli/campaign.rs` and the interactive input in `src/cli/repl.rs` now explicitly cues the player that typing `?` or `help` shows detailed command descriptions.
- **Debrief Quality:** A strategic lesson about capital projects has been added to the competitive end-session debrief in `src/mcp/session.rs` to address the `project` command underuse identified during diagnostics.
- **Determinism and State Boundaries:** No changes were made to core simulation transition logic, model structures, or state hashes. Simulation determinism and replay stability are fully preserved.

## Required Fixes

None.

## Residual Risks

- **Playtest Validation:** Although guidance has been hardened to encourage better utilization of commands like `project` and `recruit`, follow-up automated playtests are required to verify if the new info-rich interface actually changes agent command distributions and reduces `hold` overuse.

## Verification Evidence

- Run `cargo test` and `cargo fmt --check` successful. All 230+ tests passed cleanly.
- Existing tests (such as `help_text_avoids_actor_outcome_spoilers`) verify that no outcome spoilers were leaked in the expanded help text.
