# Evidence Map - Live MCP Capture Evidence

## Evidence Question

Can the current local MCP wrapper capture observation-by-observation simulated
play evidence without changing the Rust MCP API or runtime simulation behavior?

## Inputs

- `docs/agent-playtest-protocol.md` requires artifacts to record actor-visible
  observations, legal command hints, submitted commands, validation failures,
  histories, and final debriefs.
- `docs/playtest-findings-v0.10.7.md` identified a limit: sub-agent command
  plans were replayed through MCP, but they were not captured as live
  month-by-month decisions.

## Mechanism Mapping

- `scripts/play_game.py` already drives the MCP server over stdio and receives
  the actor-visible session envelope before each command.
- Optional trace capture records the evidence already crossing the boundary:
  observations, legal command hints, submitted command text, validation
  failures, transition summaries, done state, final observation, and debrief.
- Because the capture occurs in the Python wrapper, no Rust MCP DTO, hidden
  state, transition logic, stochastic boundary, or state hash change is needed.

## Evidence Produced

- Three Hard competitive persona-policy runs at seed `42`.
- All three completed 24 months with zero validation failures.
- Access-pledge counts were `0`, `1`, and `0`.
- The artifact is stored at
  `_workspace/experiments/v0.10.9-live-mcp-capture/results.json`.

## Interpretation Limits

- Deterministic persona policies are simulated-agent evidence, not autonomous
  live LLM play or human play.
- One seed and one difficulty tier cannot justify balance tuning.
- Conservative command policies reduce validation noise and are primarily useful
  for validating the capture workflow.

## Follow-Up Routing

- Use this trace path for future free-form or LLM-assisted MCP evidence when
  observation-by-observation context matters.
- Keep access-pledge follow-up in guidance, debrief, and evidence review unless
  later live LLM or human play repeats the issue.
