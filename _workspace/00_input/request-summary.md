# Request Summary - AI Rationale Visibility Hardening (Phase 6 - Track 1)

## Scope
Refactor the competitive debriefing and instructor summaries to track and label visibility sources for rival AI rationales.
Specifically, we will:
1. Dynamically identify whether a rival's actions were monitored by the player or contained publicly disclosed commands during play.
2. In the student-facing `competitive_debrief`, if a rival's actions were observed, append the visibility source to the rationale string: `(observed via monitor)` or `(observed via public disclosure)`.
3. In the instructor-visible summary, dynamically label rationale visibility based on monitored/public status during play, leaving the `(unobserved during play - REVEALED FOR INSTRUCTOR REVIEW)` label strictly for private unobserved actions.
4. Colocate unit tests in `src/debrief/report_tests.rs` to verify correct behavior across private, monitored, and public disclosure states.

## Non-Goals
- No changes to stabilization campaign debrief structures.
- No changes to simulation transition rules or scenario loaders.

## Sources
- `src/debrief/report.rs`
- `src/debrief/report_tests.rs`

## Expected Files
- `src/debrief/report.rs` (Modified)
- `src/debrief/report_tests.rs` (Modified)

## Validation Target
- All cargo tests pass cleanly (241+ tests).
- `cargo clippy --all-targets -- -D warnings` compiles without warnings.
