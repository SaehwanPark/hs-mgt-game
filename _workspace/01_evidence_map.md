# Evidence Map: MCP Playtest Evidence Slice

## Scope

Map the v0.1.49 automated MCP playtest results into bounded validation
implications. This artifact supports evidence documentation and follow-up
selection only; it does not approve formula tuning or broader runtime expansion.

## Sources Reviewed

- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.1.49.md`
- `scripts/run_automated_playtests.py`
- `scripts/play_game.py`
- MCP transition histories and debriefs captured by the automated batch

## Evidence Observed

- Six scripted-policy sessions completed at seed `42`: three profiles across
  `stabilization-v1` and three profiles across `competitive-regional-v1`.
- Stabilization profiles produced distinct cash/access/trust tradeoffs and
  debriefs with actor rationales, attributed effects, and observation revision
  notes.
- Competitive profiles produced distinct command clusters and final hashes, but
  current MCP debrief output does not expose final player tradeoff metrics.
- No scripted validation failures occurred after the harness policy-selection
  bug was fixed.

## Assumptions

- Scripted-policy completion is useful command-surface evidence but weaker than
  free-form agent or human play.
- One seed can flag obvious harness, command, or debrief issues but cannot
  justify balance tuning.
- Competitive final-metric reporting should be derived from committed history or
  debrief output, not from hidden active-play state.

## Design Implications

- Treat the next Phase 7 slice as evidence-surface improvement before broader
  diagnostics: competitive final tradeoff reporting is the clearest gap.
- Keep strategy-space diagnostics lightweight until seed variation and
  competitive metric evidence exist.
- Add naive/free-form agent profiles only after the evidence surface can support
  interpreting their outcomes.

## Risks

- **False precision:** final hashes show different trajectories but are not
  outcome distributions.
- **Educational overclaim:** scripted policy success does not measure human
  comprehension or classroom learning.
- **Automation brittleness:** policy routing should use stable campaign/session
  information or command-surface shape, not one turn-specific hint.
