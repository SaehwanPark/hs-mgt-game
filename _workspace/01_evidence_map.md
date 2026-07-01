# Evidence Map: Naive-Profile Playtest Evidence Slice

## Scope

Map the v0.1.51 scripted MCP seed-variation results into the next bounded
validation step: adding one deterministic naive profile. This artifact supports
evidence documentation and follow-up selection only; it does not approve formula
tuning or broader runtime expansion.

## Sources Reviewed

- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.1.51.md`
- `scripts/run_automated_playtests.py`
- `scripts/play_game.py`
- MCP transition histories and debriefs captured by the automated batch

## Evidence Observed

- v0.1.51 completed 18 scripted-policy sessions: three optimized profiles across
  seeds 42, 43, and 44 for both current campaigns.
- The v0.1.51 findings still left first-time command comprehension untested
  because all profiles were pre-authored around strategic intent.
- v0.1.52 completed 24 scripted-policy sessions after adding a deterministic
  `Naive First-Time` profile.
- The naive profile completed both campaigns across seeds 42, 43, and 44 without
  validation failures.
- Naive stabilization play preserved cash but produced weaker access and
  community-trust outcomes. Naive competitive play preserved resources but
  underused the action space.

## Assumptions

- Scripted-policy completion is useful command-surface evidence but weaker than
  free-form agent or human play.
- A deterministic naive profile can test whether legal low-complexity commands
  can complete the current MCP flow, but it cannot prove that first-time players
  understand the command grammar.
- Competitive final-metric reporting should remain derived from committed
  history or end-session debrief output, not from hidden active-play state.

## Design Implications

- The next validation step should be a free-form agent profile that chooses
  commands from actor-visible observations, legal-command hints, and
  player-facing docs.
- If free-form runs repeat passive or low-benefit competitive play, evaluate
  command help and monthly report guidance before considering balance changes.
- Keep strategy-space diagnostics lightweight until repeated scripted or
  free-form findings show a concrete tooling need.

## Risks

- **False precision:** deterministic scripted profiles are not outcome
  distributions or equilibrium evidence.
- **Educational overclaim:** scripted policy success does not measure human
  comprehension or classroom learning.
- **Automation brittleness:** policy routing should use stable campaign/session
  information or command-surface shape, not one turn-specific hint.
