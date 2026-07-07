# Evidence Map - Static-vs-Adaptive Live Capture

## Evidence Question

Can the existing live MCP capture path compare static and adaptive deterministic
policies side by side without changing the MCP interface or runtime simulation
behavior?

## Inputs

- `docs/agent-playtest-protocol.md` requires captured evidence to retain
  actor-visible observations, legal commands, submitted commands, validation
  failures, histories, and debriefs.
- `docs/playtest-findings-v0.10.9.md` establishes that the current MCP wrapper
  can capture observation-by-observation evidence.
- `docs/playtest-findings-v0.10.10.md` establishes that the current diagnostic
  script can summarize live-capture artifact shape.
- `docs/playtest-findings-v0.10.12.md` recommends comparing static and adaptive
  policies side by side before changing balance values.
- `scripts/run_automated_playtests.py` already contains the base policies and
  the difficulty-adaptive wrapper.

## Mechanism Mapping

- The live-capture artifact shape already contains profile metadata, submitted
  commands, validation failures, transition counts, final hashes, and debrief
  text.
- Seed, difficulty, profile, and policy variant can be recorded per run while
  preserving existing diagnostics by including the matrix coordinates in profile
  labels.
- The `static` variant uses base deterministic policies; the `adaptive` variant
  uses the existing `TARGET_DIFFICULTY_ADAPTIVE` wrapper.
- Because this is post-run analysis, no hidden active-play state, Rust MCP DTO,
  transition logic, stochastic boundary, or state hash change is needed.

## Evidence Produced

- `_workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
  records 48 completed competitive runs.
- `_workspace/experiments/v0.10.13-live-static-adaptive-capture/diagnostics.md`
  summarizes profile outcomes, action frequencies, validation failures, access
  pledges, and final hashes.
- The matrix produced zero validation failures and 84 total access pledges.
- Normal static and adaptive runs are identical; Hard adaptive runs increase
  monitoring and preserve more cash/workforce trust for Capacity Growth and
  Balanced Strategy, with slightly lower access and staffed beds.

## Interpretation Limits

- This is simulated-agent strategy-space diagnostics, not human play or live LLM
  play.
- Three seeds, one campaign, two difficulty labels, two policy variants, and
  four deterministic scripted policies cannot justify balance tuning.
- Static/adaptive differences reflect the policy wrapper's behavior, not an
  isolated measurement of difficulty settings alone.
- The diagnostic parses final metrics from debrief text; it does not add a new
  runtime export surface.

## Follow-Up Routing

- Use this matrix as workflow evidence for comparing policy variants in live
  capture before runtime tuning.
- Keep runtime cooldowns, pledge-effect tuning, and broader analytics tooling
  gated on stronger repeated evidence.
