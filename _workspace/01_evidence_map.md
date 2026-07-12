# Evidence Map - Difficulty Depth Evidence Review v0.12.4

## Scope

Review existing all-tier and Expert simulated-policy artifacts for a visible
difficulty pressure signal before any runtime tuning. This is descriptive
evidence, not a balance or winnability claim.

## Sources Reviewed

- `_workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/results.json`
  and `diagnostics.md`.
- `_workspace/experiments/v0.11.9-expert-difficulty-validation/results.json`
  and `diagnostics.md`.
- `docs/playtest-findings-v0.11.10.md`,
  `docs/playtest-findings-v0.11.11.md`, `SPEC.md`, `docs/roadmap.md`, and
  `docs/design_principles.md`.

## Evidence lanes

| Lane | Source | Matrix | Code version | Purpose |
| --- | --- | --- | --- | --- |
| all-tier pressure | v0.11.11 post-change all-tier validation | 5 profiles × 3 seeds × Easy/Normal/Hard/Expert; 60 runs | 0.11.11 | per-tier operating pressure, action trajectories, outcomes |
| Expert clearability | v0.11.9 Expert difficulty validation | 5 profiles × 3 seeds × Expert; 15 runs | 0.11.9 | bounded completion/trace contract and overlap |

The source-version mismatch is retained as a limitation. The audit does not
pretend the two artifacts are a causal before/after experiment.

## Review dimensions

- Matrix identity: profiles, seeds, difficulty labels, and coordinates are
  complete and unique.
- Trace integrity: 24 transitions per run, observation/legal-command/
  submitted-command records, accepted history/state hashes, and debrief lines.
- Clearability proxy: complete run status and zero validation failures for the
  tested profiles and seeds.
- Visible pressure: per-tier operating bottleneck counts, especially
  `workforce_capacity`, plus action-family counts and trajectory diversity.
- Tradeoff surface: descriptive per-tier ranges for cash, access, quality,
  workforce trust, community trust, and market share.

## Candidate-signal rule

Report a candidate visible pressure dimension when its all-tier operating
signal is nondecreasing across Easy → Normal → Hard → Expert and the source
contract supports the signal for every tier. This is a routing signal only. It
does not establish that the dimension causes player behavior or that a tier is
balanced or winnable.

## Observed direction to verify

The prior diagnostics suggest `workforce_capacity` appears in 0 Easy, 15
Normal, 30 Hard, and 160 Expert operating months. The audit must recompute
these counts from committed history and record the result rather than trusting
the prose summary. Normal, Hard, and Expert also appear to reuse the same
aggregate scripted action counts; this may indicate that pressure is visible in
operating consequences rather than in the submitted action surface.

## Assumptions and limits

- Existing JSON artifacts are immutable historical sources.
- A scripted profile's completion is only a bounded clearability proxy for the
  named coordinates.
- Endpoint ranges and bottleneck counts are not causal marginal effects,
  equilibrium outcomes, or validated strategy classes.
- Integer operating quantities are game abstractions, not calibrated clinical,
  financial, or policy units.

## Design implications

- Preserve source-specific contracts and code versions.
- Compare aggregate descriptive summaries only after validating each source's
  internal trace and hash continuity.
- If a candidate signal appears, route it to a later bounded difficulty design
  gate; do not modify runtime values in this evidence slice.

## Risks

- Monotonic counts can be an artifact of scripted policies or source rules, not
  evidence that a human experiences difficulty in the same way.
- Different code versions make cross-source endpoint comparisons unsafe.
- A complete Expert matrix can be overread as general winnability; the report
  must name the tested profiles and seeds every time.
