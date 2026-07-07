# Evidence Map - Live Difficulty-Pressure Capture

## Evidence Question

Can the existing live MCP capture path support pressure-seeking Normal/Hard
competitive comparison using existing automated playtest policies without
changing the MCP interface or runtime simulation behavior?

## Inputs

- `docs/agent-playtest-protocol.md` requires captured evidence to retain
  actor-visible observations, legal commands, submitted commands, validation
  failures, histories, and debriefs.
- `docs/playtest-findings-v0.10.9.md` establishes that the current MCP wrapper
  can capture observation-by-observation evidence.
- `docs/playtest-findings-v0.10.10.md` establishes that the current diagnostic
  script can summarize live-capture artifact shape.
- `docs/playtest-findings-v0.10.11.md` shows that conservative policies under-
  sample pressure paths and do not strongly distinguish difficulty tiers.
- `scripts/run_automated_playtests.py` already contains pressure-seeking and
  difficulty-adaptive policies.

## Mechanism Mapping

- The live-capture artifact shape already contains profile metadata, submitted
  commands, validation failures, transition counts, final hashes, and debrief
  text.
- Seed, difficulty, and policy profile can be recorded per run while preserving
  the existing batch-level diagnostic format by including the matrix coordinates
  in profile labels.
- Existing automated policies avoid new command vocabulary and preserve the
  legal command surface already validated by earlier playtest slices.
- Because this is post-run analysis, no hidden active-play state, Rust MCP DTO,
  transition logic, stochastic boundary, or state hash change is needed.

## Evidence Produced

- `_workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
  records 24 completed competitive runs.
- `_workspace/experiments/v0.10.12-live-difficulty-pressure/diagnostics.md`
  summarizes profile outcomes, action frequencies, validation failures, access
  pledges, and final hashes.
- The matrix produced zero validation failures and 42 total access pledges.
- Capacity Growth and Balanced Strategy show differentiated Normal/Hard
  endpoints, while Fiscal Caution and Naive First-Time remain relatively stable
  for the tested metrics.

## Interpretation Limits

- This is simulated-agent strategy-space diagnostics, not human play or live LLM
  play.
- Three seeds, one campaign, two difficulty labels, and four deterministic
  scripted policies cannot justify balance tuning.
- The Hard/Normal comparison includes effects from the existing adaptive policy
  wrapper, so it is pressure evidence rather than an isolated measurement of
  difficulty settings alone.
- The diagnostic parses final metrics from debrief text; it does not add a new
  runtime export surface.

## Follow-Up Routing

- Use this matrix as workflow evidence for pressure-policy live capture and
  Normal/Hard comparison.
- Keep runtime cooldowns, pledge-effect tuning, and broader analytics tooling
  gated on stronger repeated evidence.
