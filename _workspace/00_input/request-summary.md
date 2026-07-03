# Request Summary

## Scope

Execute follow-up playtest sessions under the new v0.1.57 command help and prompt cues to verify if the guidance successfully reduces Hold overuse and aids first-time play understanding. Document the findings in `docs/playtest-findings-v0.1.58.md`.

Specific tasks:
1. Run follow-up free-form playtest sessions for the `stabilization-v1` and `competitive-regional-v1` campaigns with seed 42.
2. Verify that the agent utilizes the expanded command help (typing `?` or `help`) and uses commands like `project`, `recruit`, and `negotiate` instead of defaulting to `hold` where appropriate.
3. Update `CHANGELOG.md` and `SPEC.md` to document the new playtest findings and present version bump.
4. Bump Cargo package version in `Cargo.toml` to `0.1.58`.
5. Prepare and push a temporary branch `feat/playtest-findings-v0.1.58` and open a PR (PR handoff).
6. Run the 3-pass review loop on the resulting PR.

## Non-Goals

- No changes to core simulation transition logic, model structures, or validation thresholds.
- No changes to scenario TOML files or the campaign selection flow.
- No changes to golden hashes (the golden hashes for seed 42 must remain identical to main).
- No new MCP endpoints or DTO changes.

## Sources

- `SPEC.md`
- `docs/playtest-findings-v0.1.56.md`
- `docs/playtest-findings-v0.1.55.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `scripts/play_game.py`
- `scripts/run_automated_playtests.py`

## Expected Files

- `docs/playtest-findings-v0.1.58.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`

## Validation Target

- All automated playtests pass successfully.
- All unit and integration tests (230+) run and pass.
- `cargo fmt --check` passes.
- Playtest report matches the structure in `docs/agent-playtest-protocol.md`.

## Global Skills Needed

- `preferred-workflow` for PR, branch, and code-review loop.
- `plan-designer` for defining the operational coding plan.
- `simple-code-writer` for editing project files.
- `spec-driven-developer` for SDD index and changelog updates.
- `code-reviewer` for three independent review passes.
