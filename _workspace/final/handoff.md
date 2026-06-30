# Final Handoff: AI-Agent Playtest Documentation Pivot

## Changed Files

- Added `docs/agent-playtest-protocol.md`.
- Added `docs/decision-records/0009-ai-agent-playtest-validation-path.md` and
  linked it from the ADR index.
- Updated `README.md`, `SPEC.md`, `docs/roadmap.md`,
  `docs/external-playtest-protocol.md`, `docs/mcp-playtesting-guide.md`,
  `docs/glossary.md`, `docs/evidence-registry.md`,
  `docs/phase5-scope-register.md`, and `docs/phase1-implications-memo.md`.
- Added request summary, domain QA, and handoff artifacts under `_workspace/`.
- Updated `CHANGELOG.md`, `Cargo.toml`, `Cargo.lock`, and `LESSONS.md`.

## Verification

- MCP one-turn smoke test passed.
- `cargo fmt --check` passed.
- `cargo test` passed.
- `git diff --check` passed.
- Stale-language scan reviewed active and historical playtest terminology.

## Known Limits

- Full `scripts/run_automated_playtests.py` hung twice on the first
  stabilization batch `submit_turn`; this was not fixed because the requested
  change was documentation-only.
- The docs now make AI-agent playtests the active validation path, but they do
  not claim human educational outcome measurement.

## Next Dependency

The next agent-playtest findings slice should either fix or replace the hanging
batch runner before relying on it for a versioned findings document.
