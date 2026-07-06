# AI-Agent Project-Command Playtest Coverage v0.9.7

- **Status:** Phase 7 targeted project-command diagnostics slice
- **Date:** 2026-07-06
- **Code version:** 0.9.7
- **Harness:** `python3 scripts/run_automated_playtests.py --target project-coverage --json-output ...`
  followed by `python3 scripts/diagnose_runs.py ...`
- **Campaigns:** `stabilization-v1`, `competitive-regional-v1`
- **Seeds:** `42`, `43`, `44`
- **Difficulty:** normal for competitive runs
- **Agent profile:** Project Coverage

These diagnostics summarize simulated-agent evidence only. They do not measure
human learning, classroom effectiveness, empirical calibration, real-world
policy validity, numerical balance, or equilibrium behavior.

## Run Matrix

| Campaign | Seeds | Profiles | Completed sessions | Validation failures |
| --- | --- | ---: | ---: | ---: |
| `stabilization-v1` | 42, 43, 44 | 1 | 3 | 0 |
| `competitive-regional-v1` | 42, 43, 44 | 1 | 3 | 0 |

The targeted batch completed without crashes, hangs, incomplete sessions, or
command validation failures. It is intentionally narrower than the default
baseline batch and exists to exercise capital-project command paths under the
current 24-month competitive scenario constraints.

## Competitive Project Coverage

| Profile | Project commands | Project kinds | Final active projects | Final monthly draws | Representative hashes |
| --- | ---: | --- | ---: | ---: | --- |
| Project Coverage | 15 | EmergencyPavilion, ClinicNetwork, AscUnit, NeurologyUnit, InfusionCenter | 2 | 2 | `ce152fd849fbd9ed`, `1a7ab37a9d3e1bd7`, `be523f3d648f3f45` |

The policy uses minimal divisible project budgets to avoid invalid monthly draw
or cash states while preserving a clear project-command signal. It also avoids
more than two concurrent projects, including scenario-driven project delays.

## Competitive Outcome Signals

| Metric | Value |
| --- | ---: |
| Cash | 16 |
| Access | 27 |
| Beds | 118 |
| Workforce trust | 0 |
| Community trust | 53 |
| Political capital | 15 |

The profile is not a recommended player strategy. It deliberately starts
projects with low budgets and insufficient workforce investment, which produces
poor access and workforce outcomes. Treat this as command-path coverage and
diagnostic evidence, not balance evidence.

## Gameplay Validity Hypotheses

- **A focused project-command policy can complete through MCP:** Pass. All six
  expected sessions completed with zero validation failures.
- **The diagnostics can distinguish project commands from generic action
  counts:** Pass. The report now shows project-command counts, project kinds,
  final active projects, and final monthly draws.
- **The target supports balance tuning:** Fail. This evidence is intentionally
  synthetic and narrow.

## Evidence Limits

- Batch diagnostics use MCP transition summaries and debriefs, not full replay
  artifacts.
- The project-coverage policy is diagnostic, not a plausible full strategy.
- Scenario timeline effects and project-concurrency limits constrain how many
  project kinds can be safely exercised in one 24-month run.
- These findings do not support formula tuning, empirical calibration, human
  learning claims, or policy-validity claims.

## Prioritized Follow-Up

1. Keep `--target project-coverage` as a focused diagnostic target rather than
   folding it into the default baseline batch.
2. Use future targeted playtest policies only for named command families or
   scenario questions that remain under-exercised.
3. Do not change balance or runtime mechanics from this artifact alone.
