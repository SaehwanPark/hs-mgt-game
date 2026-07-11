# Strategy-Space Diagnostic Report
This diagnostic summary maps strategic actions, outcome distributions, and strategy-cluster classifications.

## Live-Capture Diagnostics for `results.json`
- **Batch id:** v0.10.50-teachability-observation-capture
- **Code version:** 0.10.50
- **Campaign:** competitive-regional-v1
- **Difficulty:** hard
- **Seed:** 42, 43, 44
- **Evidence type:** deterministic observation-driven competitive MCP capture for teachability, command comprehension, follow-through, and debrief use

### Profile Outcomes
| Profile | Status | Months | Cash | Access | Quality | Workforce Trust | Community Trust | Market Share | PC | Beds | Validation Failures | Access Pledges | Final Hash |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Fiscal Steward / hard / seed 42 | complete | 24 | 60 | 68 | 74 | 60 | 64 | 24 | 15 | 118 | 0 | 0 | 013adf62dc95a77c |
| Access Expansion Advocate / hard / seed 42 | complete | 24 | 35 | 73 | 75 | 58 | 65 | 24 | 15 | 118 | 0 | 0 | 114593ef75a3670f |
| First-Time Executive / hard / seed 42 | complete | 24 | 60 | 68 | 74 | 60 | 64 | 25 | 15 | 118 | 0 | 0 | 577c2f27dc380d80 |
| Fiscal Steward / hard / seed 43 | complete | 24 | 60 | 68 | 74 | 60 | 64 | 24 | 15 | 118 | 0 | 0 | f83b06d5791ab74a |
| Access Expansion Advocate / hard / seed 43 | complete | 24 | 35 | 73 | 75 | 58 | 65 | 24 | 15 | 118 | 0 | 0 | 717192ae8cb12881 |
| First-Time Executive / hard / seed 43 | complete | 24 | 60 | 68 | 74 | 60 | 64 | 25 | 15 | 118 | 0 | 0 | 173d64972226c27e |
| Fiscal Steward / hard / seed 44 | complete | 24 | 60 | 68 | 74 | 60 | 64 | 24 | 15 | 118 | 0 | 0 | 9bf5e7df9320f873 |
| Access Expansion Advocate / hard / seed 44 | complete | 24 | 35 | 73 | 75 | 58 | 65 | 24 | 15 | 118 | 0 | 0 | fbe9ddfcdf0e658b |
| First-Time Executive / hard / seed 44 | complete | 24 | 60 | 68 | 74 | 60 | 64 | 25 | 15 | 118 | 0 | 0 | 15f74b5bde30c4a3 |

### Action Frequency Signals
| Profile | Holds | Action Commands | Monitor | Recruit | Invest | Negotiate | Commit | Project | Top Non-Hold Verb | Strategy Classification |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Fiscal Steward / hard / seed 42 | 24 | 5 | 4 | 0 | 0 | 0 | 1 | 0 | Monitor (4) | Conservative / Passive |
| Access Expansion Advocate / hard / seed 42 | 22 | 10 | 4 | 1 | 0 | 2 | 3 | 0 | Monitor (4) | Intel-Gatherer |
| First-Time Executive / hard / seed 42 | 24 | 7 | 4 | 0 | 0 | 1 | 2 | 0 | Monitor (4) | Conservative / Passive |
| Fiscal Steward / hard / seed 43 | 24 | 5 | 4 | 0 | 0 | 0 | 1 | 0 | Monitor (4) | Conservative / Passive |
| Access Expansion Advocate / hard / seed 43 | 22 | 10 | 4 | 1 | 0 | 2 | 3 | 0 | Monitor (4) | Intel-Gatherer |
| First-Time Executive / hard / seed 43 | 24 | 7 | 4 | 0 | 0 | 1 | 2 | 0 | Monitor (4) | Conservative / Passive |
| Fiscal Steward / hard / seed 44 | 24 | 5 | 4 | 0 | 0 | 0 | 1 | 0 | Monitor (4) | Conservative / Passive |
| Access Expansion Advocate / hard / seed 44 | 22 | 10 | 4 | 1 | 0 | 2 | 3 | 0 | Monitor (4) | Intel-Gatherer |
| First-Time Executive / hard / seed 44 | 24 | 7 | 4 | 0 | 0 | 1 | 2 | 0 | Monitor (4) | Conservative / Passive |

### Live Retry Signals
| Profile | Difficulty | Final Validation Failures | Live Retries | Cash-Overrun Retries | Other Retries | Representative Retry Details |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Fiscal Steward / hard / seed 42 | hard | 0 | 0 | 0 | 0 | None |
| Access Expansion Advocate / hard / seed 42 | hard | 0 | 0 | 0 | 0 | None |
| First-Time Executive / hard / seed 42 | hard | 0 | 0 | 0 | 0 | None |
| Fiscal Steward / hard / seed 43 | hard | 0 | 0 | 0 | 0 | None |
| Access Expansion Advocate / hard / seed 43 | hard | 0 | 0 | 0 | 0 | None |
| First-Time Executive / hard / seed 43 | hard | 0 | 0 | 0 | 0 | None |
| Fiscal Steward / hard / seed 44 | hard | 0 | 0 | 0 | 0 | None |
| Access Expansion Advocate / hard / seed 44 | hard | 0 | 0 | 0 | 0 | None |
| First-Time Executive / hard / seed 44 | hard | 0 | 0 | 0 | 0 | None |

### Evidence Limits
- Live-capture diagnostics use actor-visible observations, submitted commands, transition summaries, and debrief text from the captured MCP wrapper artifact.
- Live retry signals come from optional wrapper metadata and describe rejected or retried decision attempts before the accepted command stream; they are separate from final replay validation failures.
- These diagnostics support gameplay, command-surface, and explanation review; they are not human-learning, empirical-calibration, policy-validity, or balance evidence.
- Do not use a single seed, difficulty, or scripted persona batch to justify runtime tuning.

---
