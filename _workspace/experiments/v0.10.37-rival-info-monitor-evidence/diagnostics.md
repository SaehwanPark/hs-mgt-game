# Strategy-Space Diagnostic Report
This diagnostic summary maps strategic actions, outcome distributions, and strategy-cluster classifications.

## Live-Capture Diagnostics for `results.json`
- **Batch id:** v0.10.37-rival-info-monitor-evidence
- **Code version:** 0.10.37
- **Campaign:** competitive-regional-v1
- **Difficulty:** hard, expert
- **Seed:** 42
- **Evidence type:** paired live MCP capture comparing monitored and unmonitored rival information policies at Hard and Expert difficulty

### Profile Outcomes
| Profile | Status | Months | Cash | Access | Quality | Workforce Trust | Community Trust | Market Share | PC | Beds | Validation Failures | Access Pledges | Final Hash |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Rival Information Monitored / hard | complete | 24 | 34 | 71 | 77 | 59 | 64 | 28 | 15 | 118 | 0 | 0 | df8d6c0da2f78dfb |
| Rival Information Unmonitored / hard | complete | 24 | 34 | 71 | 77 | 59 | 64 | 28 | 15 | 118 | 0 | 0 | df8d6c0da2f78dfb |
| Rival Information Monitored / expert | complete | 24 | 34 | 71 | 77 | 59 | 64 | 28 | 15 | 118 | 0 | 0 | a77df3947ba47a33 |
| Rival Information Unmonitored / expert | complete | 24 | 34 | 71 | 77 | 59 | 64 | 28 | 15 | 118 | 0 | 0 | a77df3947ba47a33 |

### Action Frequency Signals
| Profile | Holds | Action Commands | Monitor | Recruit | Invest | Negotiate | Commit | Project | Top Non-Hold Verb | Strategy Classification |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Rival Information Monitored / hard | 24 | 23 | 12 | 1 | 2 | 6 | 2 | 0 | Monitor (12) | Intel-Gatherer |
| Rival Information Unmonitored / hard | 24 | 11 | 0 | 1 | 2 | 6 | 2 | 0 | Negotiate (6) | Revenue-Optimizer |
| Rival Information Monitored / expert | 24 | 23 | 12 | 1 | 2 | 6 | 2 | 0 | Monitor (12) | Intel-Gatherer |
| Rival Information Unmonitored / expert | 24 | 11 | 0 | 1 | 2 | 6 | 2 | 0 | Negotiate (6) | Revenue-Optimizer |

### Live Retry Signals
| Profile | Difficulty | Final Validation Failures | Live Retries | Cash-Overrun Retries | Other Retries | Representative Retry Details |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Rival Information Monitored / hard | hard | 0 | 0 | 0 | 0 | None |
| Rival Information Unmonitored / hard | hard | 0 | 0 | 0 | 0 | None |
| Rival Information Monitored / expert | expert | 0 | 0 | 0 | 0 | None |
| Rival Information Unmonitored / expert | expert | 0 | 0 | 0 | 0 | None |

### Rival Information Signals
| Profile | Difficulty | Variant | Monitor Intel Lines | Public Rival Lines | Private Activity Gaps | No Public Signal Lines | Example Signal |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Rival Information Monitored / hard | hard | monitored | 3 | 46 | 23 | 3 | month 4: Market: Rival Summit Care (monitor intel, month 3): Summit Care: private payer talks with CarrierA (Aggressive) |
| Rival Information Unmonitored / hard | hard | unmonitored | 0 | 46 | 23 | 3 | month 2: Market: Rival Northlake Health (observed, prior month): Northlake Health: investing 25 in Beds |
| Rival Information Monitored / expert | expert | monitored | 3 | 69 | 23 | 4 | month 4: Market: Rival Summit Care (monitor intel, month 3): Summit Care: private payer talks with CarrierA (Aggressive) |
| Rival Information Unmonitored / expert | expert | unmonitored | 0 | 69 | 23 | 4 | month 2: Market: Rival Northlake Health (observed, prior month): Northlake Health: investing 25 in Beds |

### Evidence Limits
- Live-capture diagnostics use actor-visible observations, submitted commands, transition summaries, and debrief text from the captured MCP wrapper artifact.
- Live retry signals come from optional wrapper metadata and describe rejected or retried decision attempts before the accepted command stream; they are separate from final replay validation failures.
- These diagnostics support gameplay, command-surface, and explanation review; they are not human-learning, empirical-calibration, policy-validity, or balance evidence.
- Do not use a single seed, difficulty, or scripted persona batch to justify runtime tuning.

---
