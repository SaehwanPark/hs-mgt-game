# Strategy-Space Diagnostic Report
This diagnostic summary maps strategic actions, outcome distributions, and strategy-cluster classifications.

## Live-Capture Diagnostics for `results.json`
- **Batch id:** v0.10.15-live-llm-difficulty-gate
- **Code version:** 0.10.15
- **Campaign:** competitive-regional-v1
- **Difficulty:** normal, hard
- **Seed:** 42
- **Evidence type:** live month-by-month sub-agent decisions captured from actor-visible MCP observations and replayed through the observation-by-observation wrapper

### Profile Outcomes
| Profile | Months | Cash | Access | Quality | Workforce Trust | Community Trust | Market Share | PC | Beds | Validation Failures | Access Pledges | Final Hash |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Live Fiscal Steward / normal / seed 42 | 24 | 33 | 71 | 77 | 58 | 64 | 26 | 15 | 118 | 0 | 0 | 57a5496602fccaf6 |
| Live Fiscal Steward / hard / seed 42 | 24 | 40 | 68 | 72 | 56 | 64 | 28 | 15 | 118 | 0 | 0 | 23d4f7b21ec7386d |
| Live Competitive Analyst / normal / seed 42 | 24 | 20 | 68 | 80 | 60 | 64 | 27 | 15 | 118 | 0 | 0 | 19aefaeb7adfe428 |
| Live Competitive Analyst / hard / seed 42 | 24 | 18 | 68 | 81 | 60 | 64 | 26 | 15 | 118 | 0 | 0 | a40f40a8fce52d0c |
| Live Access Operator / normal / seed 42 | 24 | 0 | 71 | 72 | 50 | 65 | 34 | 15 | 120 | 0 | 1 | ac0dfcdf3cf099e4 |
| Live Access Operator / hard / seed 42 | 24 | 0 | 75 | 81 | 56 | 66 | 29 | 15 | 119 | 0 | 2 | 8b14af9072eb9c1c |

### Action Frequency Signals
| Profile | Holds | Action Commands | Monitor | Recruit | Invest | Negotiate | Commit | Project | Top Non-Hold Verb | Strategy Classification |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Live Fiscal Steward / normal / seed 42 | 24 | 16 | 8 | 1 | 1 | 4 | 2 | 0 | Monitor (8) | Intel-Gatherer |
| Live Fiscal Steward / hard / seed 42 | 24 | 14 | 8 | 2 | 0 | 4 | 0 | 0 | Monitor (8) | Intel-Gatherer |
| Live Competitive Analyst / normal / seed 42 | 24 | 18 | 8 | 0 | 5 | 5 | 0 | 0 | Monitor (8) | Intel-Gatherer |
| Live Competitive Analyst / hard / seed 42 | 24 | 17 | 8 | 0 | 4 | 5 | 0 | 0 | Monitor (8) | Intel-Gatherer |
| Live Access Operator / normal / seed 42 | 0 | 36 | 19 | 3 | 1 | 10 | 3 | 0 | Monitor (19) | Intel-Gatherer |
| Live Access Operator / hard / seed 42 | 1 | 47 | 19 | 4 | 5 | 7 | 12 | 0 | Monitor (19) | Intel-Gatherer |

### Evidence Limits
- Live-capture diagnostics use actor-visible observations, submitted commands, transition summaries, and debrief text from the captured MCP wrapper artifact.
- These diagnostics support gameplay, command-surface, and explanation review; they are not human-learning, empirical-calibration, policy-validity, or balance evidence.
- Do not use a single seed, difficulty, or scripted persona batch to justify runtime tuning.

---
