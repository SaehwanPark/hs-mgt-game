# Live MCP Capture Evidence v0.10.9

- **Status:** Phase 7 simulated-agent evidence
- **Date:** 2026-07-07
- **Code version:** 0.10.9
- **Campaign:** `competitive-regional-v1`
- **Difficulty:** `hard`
- **Seed:** `42`
- **Harness:** live observation-by-observation MCP capture with deterministic
  persona policies

This artifact tests whether the current MCP wrapper can capture the evidence
required by the agent-playtest protocol: actor-visible observations, legal
command hints, submitted commands, validation outcomes, transition hashes, and
final debriefs. It addresses a limitation in the v0.10.7 sub-agent slice, where
command plans were generated before replay rather than captured month by month.

The results remain simulated-agent evidence only. They do not measure human
learning, classroom effectiveness, empirical calibration, policy validity,
numerical balance, or equilibrium behavior.

## Run Matrix

| Profile | Completed months | Validation failures | Access pledges | Final hash |
| --- | ---: | ---: | ---: | --- |
| Solvency Monitor | 24 | 0 | 0 | `013adf62dc95a77c` |
| Access Operations | 24 | 0 | 1 | `114593ef75a3670f` |
| Workforce Quality | 24 | 0 | 0 | `577c2f27dc380d80` |

The replay artifact is
`_workspace/experiments/v0.10.9-live-mcp-capture/results.json`.
The capture script is
`_workspace/experiments/v0.10.9-live-mcp-capture/run_sessions.py`.

## Findings

1. **The existing MCP boundary supports live evidence capture.** The Python MCP
   wrapper now records each month’s actor-visible observation, legal command
   hints, submitted command, transition summary, state hash, and validation
   outcome without changing Rust MCP DTOs or runtime simulation behavior.
2. **No repeated access-pledge loop appeared in this live-capture slice.** The
   Access Operations profile made one access pledge in month 1 and then used
   workforce, Medicaid, Medicare, monitoring, and hold actions. The other two
   profiles made no access pledges.
3. **The policies were conservative under Hard pressure.** Solvency Monitor and
   Workforce Quality leaned on monitoring, holds, staffing, payer, quality, and
   workforce moves. This is useful capture evidence, not proof that the command
   space is balanced or strategically rich.
4. **The evidence supports workflow, not tuning.** The slice justifies using the
   live-capture artifact path for future free-form or LLM-assisted runs. It does
   not justify runtime access cooldowns, pledge-effect changes, or balance edits.

## Endpoint Notes

- Solvency Monitor ended with cash `60`, access `68`, quality `74`, workforce
  trust `60`, community trust `64`, market share `24`.
- Access Operations ended with cash `35`, access `73`, quality `75`, workforce
  trust `58`, community trust `65`, market share `24`.
- Workforce Quality ended with cash `60`, access `68`, quality `74`, workforce
  trust `60`, community trust `64`, market share `25`.

## Evidence Limits

- Three profiles, one seed, one campaign, and one difficulty tier.
- The policies are deterministic local heuristics, not autonomous live LLM play.
- Conservative command selection reduces validation noise but also limits
  conclusions about action-space pressure, risk-taking, and balance.
- The artifact captures what the scripted persona saw and submitted; it is not a
  human-playtest or classroom-learning artifact.

## Follow-Up Routing

- Use the live-capture workflow when future findings need observation-by-
  observation evidence.
- Keep access-pledge follow-up in guidance, debrief, and evidence review unless
  later live LLM or human play repeats access pledges after seeing current
  guidance.
- Do not add a general LLM runner until repeated live-capture work shows the
  current MCP wrapper cannot capture required prompts, observations, commands,
  validation errors, retries, histories, and debriefs.
