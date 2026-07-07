# LLM Access-Pledge Evidence v0.10.7

- **Status:** Phase 7 simulated-agent evidence
- **Date:** 2026-07-07
- **Code version:** 0.10.7
- **Campaign:** `competitive-regional-v1`
- **Difficulty:** `hard`
- **Seed:** `42`
- **Harness:** sub-agent generated command plans replayed through MCP

This artifact tests whether the repeated access-pledge loop seen in earlier
deterministic operator policies appears in a small sub-agent command-planning
slice after the v0.10.3 guidance and v0.10.6 debrief QA work. It is simulated
agent evidence only. It does not measure human learning, classroom
effectiveness, empirical calibration, policy validity, numerical balance, or
equilibrium behavior.

## Run Matrix

| Profile | Completed months | Validation failures | Access pledges | Final hash |
| --- | ---: | ---: | ---: | --- |
| Fiscal Steward | 24 | 0 | 0 | `0b1c11afea47e6d4` |
| Access Expansion Advocate | 24 | 0 | 1 | `3795c0b09482fe17` |
| First-Time Executive | 24 | 0 | 1 | `3563f1698a8b80b0` |

The replay artifact is
`_workspace/experiments/v0.10.7-llm-access-pledge-evidence/results.json`.
The replay script is
`_workspace/experiments/v0.10.7-llm-access-pledge-evidence/run_sessions.py`.

## Findings

1. **No repeated access-pledge loop appeared in this slice.** The fiscal profile
   made no access pledges. The access-expansion and first-time profiles each
   made one access pledge, then shifted to staffing, monitoring, payer, or
   service-line actions.
2. **Sub-agent plans still needed MCP validation.** Initial command plans
   included too-small project budgets, unsupported non-neutral public-payer
   postures, and Hard-mode cash overcommitments. The committed replay uses
   minimal legal adjustments, mostly replacing unaffordable later actions with
   `hold`.
3. **Operational follow-through was legible but conservative.** The access
   profile followed its initial pledge with Medicaid negotiation, outpatient
   investment, recruitment, emergency/psychiatric/obstetrics actions, and
   monitoring before later cash conservation.
4. **The evidence supports guidance and debrief framing, not tuning.** This
   small slice does not justify runtime cooldowns, pledge-effect changes, or
   balance edits.

## Endpoint Notes

- Fiscal Steward ended with cash `6`, access `68`, quality `77`, workforce trust
  `52`, community trust `64`, market share `26`.
- Access Expansion Advocate ended with cash `20`, access `75`, quality `75`,
  workforce trust `56`, community trust `66`, market share `26`.
- First-Time Executive ended with cash `8`, access `73`, quality `72`,
  workforce trust `52`, community trust `65`, market share `25`.

## Evidence Limits

- Three profiles, one seed, one campaign, and one difficulty tier.
- Sub-agents produced command plans without live month-by-month MCP tool access;
  the replay artifact validates the accepted command sequences afterward.
- The command-plan corrections are operator adjustments, not autonomous player
  retries.
- The results are not human-playtest, LLM-runner, or balance-calibration
  evidence.

## Follow-Up Routing

- Keep access-pledge work in guidance, debrief, and evidence review unless later
  live LLM or human play repeats access pledges after seeing current guidance.
- If future runs need live observation-by-observation decision capture, add the
  smallest MCP automation affordance that records prompts, observations,
  commands, validation errors, and retries. Do not add a general LLM runner from
  this slice alone.
