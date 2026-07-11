# Decision-Load and Pacing Proxy Evidence 0.10.52

- **Status:** Phase 7 competitive teachability and validation evidence
- **Source artifact:** `_workspace/experiments/v0.10.50-teachability-observation-capture/results.json`
- **Campaign:** `competitive-regional-v1`
- **Source runs:** 9 complete of 9

This is a deterministic read-only audit of existing turn-level traces. It does not launch new sessions or change runtime behavior.

## Profile summaries

| Profile | Runs | Seeds stable | Action commands | Active months | Holds | Multi-action months | Max actions/month | Status |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| fiscal_steward | 3 | True | 5 | 5 | 24 | 0 | 1 | supported |
| access_expansion_advocate | 3 | True | 10 | 8 | 22 | 2 | 2 | supported |
| first_time_executive | 3 | True | 7 | 7 | 24 | 0 | 1 | supported |

## Run-level decision-load signals

| Profile | Seed | Actions | Active months | Holds | Multi-action months | Max actions/month | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| fiscal_steward | 42 | 5 | 5 | 24 | 0 | 1 | supported |
| access_expansion_advocate | 42 | 10 | 8 | 22 | 2 | 2 | supported |
| first_time_executive | 42 | 7 | 7 | 24 | 0 | 1 | supported |
| fiscal_steward | 43 | 5 | 5 | 24 | 0 | 1 | supported |
| access_expansion_advocate | 43 | 10 | 8 | 22 | 2 | 2 | supported |
| first_time_executive | 43 | 7 | 7 | 24 | 0 | 1 | supported |
| fiscal_steward | 44 | 5 | 5 | 24 | 0 | 1 | supported |
| access_expansion_advocate | 44 | 10 | 8 | 22 | 2 | 2 | supported |
| first_time_executive | 44 | 7 | 7 | 24 | 0 | 1 | supported |

## Promotion decision

Runtime promotion: deferred

Turn-level decision-load signals are descriptive pacing proxies. No player-facing, instructor-facing, or domain-review gap justifies runtime promotion from this artifact.

The metrics expose temporal command concentration that aggregate action totals do not show. They do not establish that a player experienced overload, that one profile is superior, or that a runtime change is needed.

## Structural gaps

None identified in the source artifact.

## Evidence limits

- This audit is deterministic simulated-policy evidence, not human or classroom evidence.
- Action concentration and active-month cadence are pacing and action-overload proxies, not cognitive-load measurements.
- Profile trajectories and endpoint metrics do not establish strategy quality, causality, balance, winnability, or optimality.
- Runtime and interface promotion remains deferred until a player-facing, instructor-facing, or domain-review gap is identified.
