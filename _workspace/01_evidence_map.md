# Evidence Map - Independent Reviewer-Agent Live Capture

## Evidence Question

Can the existing live MCP capture path evaluate independent
observation-conditioned reviewer policies without changing runtime simulation
behavior, MCP DTOs, or shared diagnostics?

## Inputs

- `docs/agent-playtest-protocol.md` requires captured evidence to retain
  actor-visible observations, legal commands, submitted commands, validation
  failures, histories, and debriefs.
- `docs/playtest-findings-v0.10.9.md` establishes that the current MCP wrapper
  can capture observation-by-observation evidence.
- `docs/playtest-findings-v0.10.10.md` establishes that the current diagnostic
  script can summarize live-capture artifact shape.
- `docs/playtest-findings-v0.10.13.md` recommends a stronger next gate using a
  bounded agent or reviewer policy not authored from the same deterministic
  profile scripts.
- `scripts/play_game.py` and `scripts/diagnose_runs.py` already expose the
  capture and diagnostic boundary needed for this slice.

## Mechanism Mapping

- The new runner records actor-visible observations, legal command hints,
  submitted commands, validation failures, transition hashes, final
  observations, and debriefs through the existing Python wrapper.
- Three reviewer policies choose commands from observation cues and month
  position, not from the existing automated month-table policies.
- Access-pledge repetition is bounded to at most one pledge per run so the slice
  tests reviewer follow-through rather than restaging the prior access-loop
  diagnostic.
- Because this is post-run analysis, no hidden active-play state, Rust MCP DTO,
  transition logic, stochastic boundary, or state hash change is needed.

## Evidence Produced

- `_workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json`
  records 18 completed competitive runs.
- `_workspace/experiments/v0.10.14-independent-reviewer-agent-capture/diagnostics.md`
  summarizes profile outcomes, action frequencies, validation failures, access
  pledges, and final hashes.
- The matrix produced zero validation failures and 6 total access pledges.
- Normal and Hard endpoint metrics were identical for each profile because the
  policies are not difficulty-adaptive.

## Interpretation Limits

- This is simulated-agent strategy-space diagnostics, not human play or live LLM
  play.
- Three seeds, one campaign, two difficulty labels, and three deterministic
  reviewer policies cannot justify balance tuning.
- The reviewer policies are operator-authored and observation-conditioned; they
  are not independent human samples.
- The diagnostic parses final metrics from debrief text; it does not add a new
  runtime export surface.

## Follow-Up Routing

- Use this matrix as evidence that new bounded reviewer policies can be tested
  with the current capture/diagnostic workflow before runtime tuning.
- Keep runtime cooldowns, pledge-effect tuning, difficulty tuning, and broader
  analytics tooling gated on stronger repeated evidence.
