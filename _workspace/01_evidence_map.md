# Evidence Map - Live-Capture Diagnostics

## Evidence Question

Can the existing strategy-space diagnostics script summarize live MCP capture
artifacts without changing the MCP interface or runtime simulation behavior?

## Inputs

- `docs/agent-playtest-protocol.md` requires captured evidence to retain
  actor-visible observations, legal commands, submitted commands, validation
  failures, histories, and debriefs.
- `docs/playtest-findings-v0.10.9.md` establishes that the current MCP wrapper
  can capture observation-by-observation evidence.
- The current diagnostic script supports replay JSON and automated playtest
  batch JSON, but not the live-capture artifact shape.

## Mechanism Mapping

- The live-capture artifact already contains profile metadata, submitted
  commands, validation failures, transition counts, final hashes, and debrief
  text.
- Diagnostic reporting can parse command verbs directly from submitted command
  text and parse final metrics from existing debrief lines.
- Because this is post-run analysis, no hidden active-play state, Rust MCP DTO,
  transition logic, stochastic boundary, or state hash change is needed.

## Evidence Produced

- `scripts/diagnose_runs.py` now accepts the live-capture artifact shape.
- `_workspace/experiments/v0.10.10-live-capture-diagnostics/diagnostics.md`
  summarizes the v0.10.9 captured runs.
- The compact report preserves the v0.10.9 limits: three deterministic
  persona-policy runs, Hard difficulty, seed `42`, and zero validation failures.

## Interpretation Limits

- This is simulated-agent strategy-space diagnostics, not human play or live LLM
  play.
- One seed, one campaign, and one difficulty tier cannot justify balance tuning.
- The diagnostic parses final metrics from debrief text; it does not add a new
  runtime export surface.

## Follow-Up Routing

- Use this diagnostic path when future live-capture artifacts need compact
  action-frequency and outcome tables.
- Keep runtime cooldowns, pledge-effect tuning, and broader analytics tooling
  gated on stronger repeated evidence.
