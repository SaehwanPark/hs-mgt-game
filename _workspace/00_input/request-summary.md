# Request Summary - Competitive Autocomplete Hardening (Phase 6 - Track 2)

## Scope
Extend the CLI autocompletion capabilities in the competitive campaign (`competitive-regional-v1`) to support argument keys and enum values, fulfilling the requirements in `docs/cli-command-grammar-draft.md`.
Specifically, we will:
1. Parse the command segment at the cursor (handling multi-command semicolon separators).
2. If the cursor is at an argument key position (e.g. after a verb or a space), autocomplete matching argument keys that have not yet been specified in the current command segment.
3. If the cursor is after an argument key followed by `=` (e.g. `domain=`), autocomplete or cycle through matching enum values.
4. Ensure no filesystem completion is triggered.
5. Colocate unit tests in `src/cli/repl.rs` to verify autocompletion behavior for verbs, keys, and values.

## Non-Goals
- No changes to stabilization campaign prompts (which are numeric-only).
- No changes to transition rules or gameplay balance.
- No changes to simulation state hash validation or scenarios.

## Sources
- `docs/cli-command-grammar-draft.md` § Autocomplete
- `src/cli/repl.rs`
- `src/cli/competitive_parse.rs`

## Expected Files
- `src/cli/repl.rs` (Modified)
- `_workspace/00_input/request-summary.md` (Modified)

## Validation Target
- All unit tests in `src/cli/repl.rs` pass cleanly.
- `cargo test` passes cleanly (233+ tests).
