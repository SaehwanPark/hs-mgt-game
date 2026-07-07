# Strategy-Space Diagnostic Report
This diagnostic summary maps strategic actions, outcome distributions, and strategy-cluster classifications.

## Live-Capture Diagnostics for `results.json`
- **Batch id:** v0.10.12-live-difficulty-pressure
- **Code version:** 0.10.12
- **Campaign:** competitive-regional-v1
- **Difficulty:** normal, hard
- **Seed:** 42, 43, 44
- **Evidence type:** live observation-by-observation MCP capture matrix with deterministic difficulty-pressure policies

### Profile Outcomes
| Profile | Months | Cash | Access | Quality | Workforce Trust | Community Trust | Market Share | PC | Beds | Validation Failures | Access Pledges | Final Hash |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Fiscal Caution / normal / seed 42 | 24 | 5 | 75 | 77 | 57 | 66 | 24 | 15 | 118 | 0 | 2 | db396cb8c5362ddc |
| Capacity Growth / normal / seed 42 | 24 | 9 | 73 | 80 | 34 | 66 | 27 | 15 | 121 | 0 | 1 | 16ace0dc772b82e0 |
| Balanced Strategy / normal / seed 42 | 24 | 1 | 75 | 76 | 48 | 67 | 27 | 15 | 121 | 0 | 2 | cef701ede4d5c162 |
| Naive First-Time / normal / seed 42 | 24 | 20 | 75 | 77 | 58 | 66 | 24 | 15 | 118 | 0 | 2 | 71b814663df88a84 |
| Fiscal Caution / normal / seed 43 | 24 | 5 | 75 | 77 | 57 | 66 | 24 | 15 | 118 | 0 | 2 | 07ea95139054c286 |
| Capacity Growth / normal / seed 43 | 24 | 9 | 73 | 80 | 34 | 66 | 27 | 15 | 121 | 0 | 1 | 9cf1e60776f2c4da |
| Balanced Strategy / normal / seed 43 | 24 | 1 | 75 | 76 | 48 | 67 | 27 | 15 | 121 | 0 | 2 | c88d320130c55d40 |
| Naive First-Time / normal / seed 43 | 24 | 20 | 75 | 77 | 58 | 66 | 24 | 15 | 118 | 0 | 2 | 655949d617c7121a |
| Fiscal Caution / normal / seed 44 | 24 | 5 | 75 | 77 | 57 | 66 | 24 | 15 | 118 | 0 | 2 | 0aab9a565fac80e4 |
| Capacity Growth / normal / seed 44 | 24 | 9 | 73 | 80 | 34 | 66 | 27 | 15 | 121 | 0 | 1 | 7503824ce07c4047 |
| Balanced Strategy / normal / seed 44 | 24 | 1 | 75 | 76 | 48 | 67 | 27 | 15 | 121 | 0 | 2 | 818a67d0a862c481 |
| Naive First-Time / normal / seed 44 | 24 | 20 | 75 | 77 | 58 | 66 | 24 | 15 | 118 | 0 | 2 | 82e1ce0125a6758c |
| Fiscal Caution / hard / seed 42 | 24 | 7 | 75 | 77 | 57 | 66 | 24 | 15 | 118 | 0 | 2 | df92b5b32a0a2807 |
| Capacity Growth / hard / seed 42 | 24 | 18 | 72 | 80 | 58 | 66 | 27 | 15 | 119 | 0 | 1 | 6e735edc9552c773 |
| Balanced Strategy / hard / seed 42 | 24 | 10 | 74 | 76 | 55 | 67 | 27 | 15 | 119 | 0 | 2 | fa89fd6d8acf11f5 |
| Naive First-Time / hard / seed 42 | 24 | 20 | 75 | 77 | 58 | 66 | 24 | 15 | 118 | 0 | 2 | ff9b08b306d4bf17 |
| Fiscal Caution / hard / seed 43 | 24 | 7 | 75 | 77 | 57 | 66 | 24 | 15 | 118 | 0 | 2 | 5f31485ce8a3dcdd |
| Capacity Growth / hard / seed 43 | 24 | 18 | 72 | 80 | 58 | 66 | 27 | 15 | 119 | 0 | 1 | d6709b0ad7ae26b5 |
| Balanced Strategy / hard / seed 43 | 24 | 10 | 74 | 76 | 55 | 67 | 27 | 15 | 119 | 0 | 2 | 15e334456da3c1df |
| Naive First-Time / hard / seed 43 | 24 | 20 | 75 | 77 | 58 | 66 | 24 | 15 | 118 | 0 | 2 | 9442870e9be85371 |
| Fiscal Caution / hard / seed 44 | 24 | 7 | 75 | 77 | 57 | 66 | 24 | 15 | 118 | 0 | 2 | 1ccbf550ea7d9453 |
| Capacity Growth / hard / seed 44 | 24 | 18 | 72 | 80 | 58 | 66 | 27 | 15 | 119 | 0 | 1 | 927e1ae4b3b4d14c |
| Balanced Strategy / hard / seed 44 | 24 | 10 | 74 | 76 | 55 | 67 | 27 | 15 | 119 | 0 | 2 | da744877b28b8fe6 |
| Naive First-Time / hard / seed 44 | 24 | 20 | 75 | 77 | 58 | 66 | 24 | 15 | 118 | 0 | 2 | dd401fe5d3a1cc4b |

### Action Frequency Signals
| Profile | Holds | Action Commands | Monitor | Recruit | Invest | Negotiate | Commit | Project | Top Non-Hold Verb | Strategy Classification |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Fiscal Caution / normal / seed 42 | 24 | 19 | 6 | 2 | 4 | 2 | 5 | 0 | Monitor (6) | Balanced Strategy |
| Capacity Growth / normal / seed 42 | 21 | 23 | 8 | 1 | 5 | 3 | 6 | 0 | Monitor (8) | Balanced Strategy |
| Balanced Strategy / normal / seed 42 | 22 | 25 | 10 | 2 | 4 | 3 | 6 | 0 | Monitor (10) | Intel-Gatherer |
| Naive First-Time / normal / seed 42 | 24 | 15 | 4 | 2 | 3 | 2 | 4 | 0 | Monitor (4) | Balanced Strategy |
| Fiscal Caution / normal / seed 43 | 24 | 19 | 6 | 2 | 4 | 2 | 5 | 0 | Monitor (6) | Balanced Strategy |
| Capacity Growth / normal / seed 43 | 21 | 23 | 8 | 1 | 5 | 3 | 6 | 0 | Monitor (8) | Balanced Strategy |
| Balanced Strategy / normal / seed 43 | 22 | 25 | 10 | 2 | 4 | 3 | 6 | 0 | Monitor (10) | Intel-Gatherer |
| Naive First-Time / normal / seed 43 | 24 | 15 | 4 | 2 | 3 | 2 | 4 | 0 | Monitor (4) | Balanced Strategy |
| Fiscal Caution / normal / seed 44 | 24 | 19 | 6 | 2 | 4 | 2 | 5 | 0 | Monitor (6) | Balanced Strategy |
| Capacity Growth / normal / seed 44 | 21 | 23 | 8 | 1 | 5 | 3 | 6 | 0 | Monitor (8) | Balanced Strategy |
| Balanced Strategy / normal / seed 44 | 22 | 25 | 10 | 2 | 4 | 3 | 6 | 0 | Monitor (10) | Intel-Gatherer |
| Naive First-Time / normal / seed 44 | 24 | 15 | 4 | 2 | 3 | 2 | 4 | 0 | Monitor (4) | Balanced Strategy |
| Fiscal Caution / hard / seed 42 | 24 | 24 | 11 | 2 | 4 | 2 | 5 | 0 | Monitor (11) | Intel-Gatherer |
| Capacity Growth / hard / seed 42 | 22 | 28 | 13 | 1 | 5 | 3 | 6 | 0 | Monitor (13) | Intel-Gatherer |
| Balanced Strategy / hard / seed 42 | 24 | 28 | 13 | 2 | 4 | 3 | 6 | 0 | Monitor (13) | Intel-Gatherer |
| Naive First-Time / hard / seed 42 | 24 | 23 | 12 | 2 | 3 | 2 | 4 | 0 | Monitor (12) | Intel-Gatherer |
| Fiscal Caution / hard / seed 43 | 24 | 24 | 11 | 2 | 4 | 2 | 5 | 0 | Monitor (11) | Intel-Gatherer |
| Capacity Growth / hard / seed 43 | 22 | 28 | 13 | 1 | 5 | 3 | 6 | 0 | Monitor (13) | Intel-Gatherer |
| Balanced Strategy / hard / seed 43 | 24 | 28 | 13 | 2 | 4 | 3 | 6 | 0 | Monitor (13) | Intel-Gatherer |
| Naive First-Time / hard / seed 43 | 24 | 23 | 12 | 2 | 3 | 2 | 4 | 0 | Monitor (12) | Intel-Gatherer |
| Fiscal Caution / hard / seed 44 | 24 | 24 | 11 | 2 | 4 | 2 | 5 | 0 | Monitor (11) | Intel-Gatherer |
| Capacity Growth / hard / seed 44 | 22 | 28 | 13 | 1 | 5 | 3 | 6 | 0 | Monitor (13) | Intel-Gatherer |
| Balanced Strategy / hard / seed 44 | 24 | 28 | 13 | 2 | 4 | 3 | 6 | 0 | Monitor (13) | Intel-Gatherer |
| Naive First-Time / hard / seed 44 | 24 | 23 | 12 | 2 | 3 | 2 | 4 | 0 | Monitor (12) | Intel-Gatherer |

### Evidence Limits
- Live-capture diagnostics use actor-visible observations, submitted commands, transition summaries, and debrief text from the captured MCP wrapper artifact.
- These diagnostics support gameplay, command-surface, and explanation review; they are not human-learning, empirical-calibration, policy-validity, or balance evidence.
- Do not use a single seed, difficulty, or scripted persona batch to justify runtime tuning.

---
