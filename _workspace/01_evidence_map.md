# Evidence Map - Live-Capture Matrix Evidence

## Evidence Question

Can the existing live MCP capture path support a small seed/difficulty matrix
without changing the MCP interface or runtime simulation behavior?

## Inputs

- `docs/agent-playtest-protocol.md` requires captured evidence to retain
  actor-visible observations, legal commands, submitted commands, validation
  failures, histories, and debriefs.
- `docs/playtest-findings-v0.10.9.md` establishes that the current MCP wrapper
  can capture observation-by-observation evidence.
- `docs/playtest-findings-v0.10.10.md` establishes that the current diagnostic
  script can summarize live-capture artifact shape.
- The next evidence need is matrix coverage, not a new runtime export surface.

## Mechanism Mapping

- The live-capture artifact shape already contains profile metadata, submitted
  commands, validation failures, transition counts, final hashes, and debrief
  text.
- Seed and difficulty can be recorded per run while preserving the existing
  batch-level diagnostic format by including the matrix coordinates in profile
  labels.
- Because this is post-run analysis, no hidden active-play state, Rust MCP DTO,
  transition logic, stochastic boundary, or state hash change is needed.

## Evidence Produced

- `_workspace/experiments/v0.10.11-live-capture-matrix/results.json` records 18
  completed competitive runs.
- `_workspace/experiments/v0.10.11-live-capture-matrix/diagnostics.md`
  summarizes profile outcomes, action frequencies, validation failures, access
  pledges, and final hashes.
- The matrix produced zero validation failures and six total access pledges, all
  from the Access Operations persona.

## Interpretation Limits

- This is simulated-agent strategy-space diagnostics, not human play or live LLM
  play.
- Three seeds, one campaign, two difficulty labels, and three deterministic
  conservative policies cannot justify balance tuning.
- The diagnostic parses final metrics from debrief text; it does not add a new
  runtime export surface.

## Follow-Up Routing

- Use this matrix as workflow evidence for seed/difficulty live capture.
- Keep runtime cooldowns, pledge-effect tuning, and broader analytics tooling
  gated on stronger repeated evidence.
