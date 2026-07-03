# Request Summary - Instructor Run Summary & Decision Quality Review

## Scope
Implement an instructor-visible run summary and decision-quality review capability for both stabilization and competitive campaigns.
1. In the stabilization campaign, display a comparison between observed reported access index and the true access index per turn, highlighting the delta caused by measurement noise and delay.
2. In the competitive campaign, list true rival actions, labeling them as observed (if monitored or public) or unobserved by the player.
3. Ensure this detailed analysis is only displayed at the end of the campaign (debrief time).
4. Integrate the new summary into both CLI and MCP end-of-session outputs.

## Non-Goals
- No changes to transition rules or state/observation calculations during active play.
- No grading system or automated LMS scoring.

## Sources
- `SPEC.md` Track 1
- `docs/design_principles.md` Principle 20 (Design for Debriefing)
- `docs/harness/health-policy-strategy-game/team-spec.md`

## Expected Files
- `src/debrief/report.rs`
- `src/debrief/report_tests.rs`
- `src/cli/output.rs`
- `src/cli/campaign.rs`
- `src/mcp/session.rs`

## Validation Target
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
