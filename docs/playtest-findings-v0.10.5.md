# Phase 7 Free-Form Hard Evidence Synthesis v0.10.5

- **Status:** Phase 7 evidence synthesis
- **Date:** 2026-07-07
- **Code version:** 0.10.5
- **Campaign:** `competitive-regional-v1`
- **Difficulty:** `hard`
- **Source artifacts:** `v0.10.0`, `v0.10.1`, `v0.10.2`, and `v0.10.4`

These findings synthesize existing free-form **simulated-agent** evidence only.
They do not add new runs, runtime mechanics, command rules, scenario schemas,
MCP DTOs, replay formats, balance values, or state hashes. They do not measure
human learning, classroom effectiveness, empirical calibration, real-world
policy validity, numerical balance, or equilibrium behavior.

## Source Matrix

| Source | Question | Sessions | Seeds | Variants | Validation failures |
| --- | --- | ---: | --- | --- | ---: |
| `docs/playtest-findings-v0.10.0.md` | Can three free-form Hard profiles complete seed 42? | 3 | 42 | baseline | 0 |
| `docs/playtest-findings-v0.10.1.md` | Do the same profiles complete seeds 42-44? | 9 | 42, 43, 44 | baseline | 0 |
| `docs/playtest-findings-v0.10.2.md` | Can bounded operator variants reduce access-pledge loops? | 27 | 42, 43, 44 | baseline, cooldown, threshold | 0 |
| `docs/playtest-findings-v0.10.4.md` | Can post-guidance behavior be represented by a bounded policy? | 18 | 42, 43, 44 | baseline, guidance-aware | 0 |

The four artifacts contain 57 recorded sessions, all completed without
validation failures. That total should not be treated as 57 independent pieces
of evidence: the seed-42 baseline appears in multiple artifacts, and the
baseline seed/profile matrix is intentionally repeated as a control.

## Synthesis Findings

1. **Completion is no longer the main risk for these policies.** The three
   free-form Hard profiles completed the 24-month competitive campaign across
   seeds `42`, `43`, and `44`, and the diagnostic variants also completed
   without validation failures.
2. **The repetitive access-pledge loop is a behavior and guidance issue before
   it is a runtime issue.** The baseline access-heavy profiles repeated access
   pledges under persistent scrutiny cues. The `v0.10.2` cooldown and threshold
   variants reduced aggregate pledges from 162 to 72 and 60, respectively.
3. **The `v0.10.3` player-facing guidance is behaviorally plausible but not
   balance evidence.** The `v0.10.4` guidance-aware variant reduced aggregate
   pledges from 162 to 60 across the same seed/profile matrix with zero
   validation failures.
4. **Reduced pledge repetition changes endpoint tradeoffs.** Access-heavy
   profiles ended with lower access and/or community trust when repeated pledges
   were redirected to fallback commands, so lower pledge counts cannot be
   interpreted as automatically better gameplay outcomes.
5. **Runtime cooldowns and formula tuning remain unsupported.** The current
   evidence supports guidance, operator-policy diagnostics, and future
   evidence-gated investigation. It does not justify changing pledge effects,
   adding command cooldowns, or tuning balance values.

## Evidence Limits

- Operator policies are deterministic observation heuristics, not LLM or human
  play.
- All synthesized runs use one campaign, one difficulty tier, three seeds, and
  three profiles.
- The diagnostic fallback commands are controls, not recommended strategies.
- Endpoint metrics come from MCP transition summaries and debriefs rather than
  full replay artifacts.
- Repeated baseline matrices are useful controls but must not be double-counted
  as independent player evidence.

## Next Evidence Gate

Do not implement runtime access-pledge cooldowns or pledge-effect tuning from
the current artifacts. If future LLM or human play still repeats access pledges
after the `v0.10.3` guidance, run a new evidence slice that captures the
player's stated rationale, actor-visible observations, submitted commands,
validation failures, and debrief interpretation before changing mechanics.

If the next work stays within simulated-agent validation, prefer one of:

- an LLM/sub-agent play slice that tests whether the same loop appears without
  deterministic operator heuristics;
- a debrief-quality review focused on explaining public pledges versus durable
  operational follow-through;
- a guidance-only wording revision followed by a new post-guidance validation
  artifact.
