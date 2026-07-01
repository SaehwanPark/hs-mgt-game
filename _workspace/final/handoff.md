# Final Handoff: Seed-Variation Playtest Evidence Slice

## Changed Files

- Updated `scripts/run_automated_playtests.py` to run existing scripted profiles
  across seeds 42, 43, and 44 for both current MCP campaigns.
- Added `docs/playtest-findings-v0.1.51.md` with the 18-session scripted
  seed-variation findings.
- Updated `README.md`, `SPEC.md`, `CHANGELOG.md`, and
  `docs/mcp-playtesting-guide.md`.
- Bumped package version in `Cargo.toml` and `Cargo.lock`.
- Replaced current `_workspace/` request summary, domain QA, and handoff.

## Verification

- `cargo fmt --check` passed.
- `cargo test` passed: 222 unit tests, 8 integration tests, 0 doc tests.
- `python3 scripts/run_automated_playtests.py` completed 18 sessions without
  validation failures.
- `git diff --check` passed.

## Known Limits

- This is scripted-agent evidence, not human learning or classroom evaluation.
- Seeds 42, 43, and 44 provide first sensitivity evidence, not broad stochastic
  characterization.
- Competitive preview outcomes were identical across these seeds for the three
  scripted profiles; this is documented as a bounded finding, not a general
  determinism claim.
- No gameplay formulas, transition semantics, scenarios, replay formats, MCP DTO
  shapes, campaign length, or golden hashes changed.

## Next Dependency

Add one naive or free-form agent profile to test command comprehension, help
text, and debrief use beyond pre-authored scripted policies.
