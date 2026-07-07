# Strategy-Space Diagnostic Report
This diagnostic summary maps strategic actions, outcome distributions, and strategy-cluster classifications.

## Live-Capture Diagnostics for `results.json`
- **Batch id:** v0.10.9-live-mcp-capture
- **Code version:** 0.10.9
- **Campaign:** competitive-regional-v1
- **Difficulty:** hard
- **Seed:** 42
- **Evidence type:** live observation-by-observation MCP capture with deterministic persona policies

### Profile Outcomes
| Profile | Months | Cash | Access | Quality | Workforce Trust | Community Trust | Market Share | PC | Beds | Validation Failures | Access Pledges | Final Hash |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Solvency Monitor | 24 | 60 | 68 | 74 | 60 | 64 | 24 | 15 | 118 | 0 | 0 | 013adf62dc95a77c |
| Access Operations | 24 | 35 | 73 | 75 | 58 | 65 | 24 | 15 | 118 | 0 | 1 | 114593ef75a3670f |
| Workforce Quality | 24 | 60 | 68 | 74 | 60 | 64 | 25 | 15 | 118 | 0 | 0 | 577c2f27dc380d80 |

### Action Frequency Signals
| Profile | Holds | Action Commands | Monitor | Recruit | Invest | Negotiate | Commit | Project | Top Non-Hold Verb | Strategy Classification |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Solvency Monitor | 24 | 5 | 4 | 0 | 0 | 0 | 1 | 0 | Monitor (4) | Conservative / Passive |
| Access Operations | 22 | 10 | 4 | 1 | 0 | 2 | 3 | 0 | Monitor (4) | Intel-Gatherer |
| Workforce Quality | 24 | 7 | 4 | 0 | 0 | 1 | 2 | 0 | Monitor (4) | Conservative / Passive |

### Evidence Limits
- Live-capture diagnostics use actor-visible observations, submitted commands, transition summaries, and debrief text from the captured MCP wrapper artifact.
- These diagnostics support gameplay, command-surface, and explanation review; they are not human-learning, empirical-calibration, policy-validity, or balance evidence.
- Do not use a single seed, difficulty, or scripted persona batch to justify runtime tuning.

---
