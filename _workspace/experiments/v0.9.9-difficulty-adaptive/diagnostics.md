# Strategy-Space Diagnostic Report
This diagnostic summary maps strategic actions, outcome distributions, and strategy-cluster classifications.

## Playtest Batch Diagnostics for `results.json`
- **Code version:** 0.9.9
- **Target:** difficulty-adaptive
- **Seeds:** 42, 43, 44
- **Competitive difficulties:** easy, hard
- **Stabilization sessions:** 12
- **Competitive sessions:** 24

### Competitive Profile Outcomes
| Group | Sessions | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Validation Failures | Representative Hashes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Fiscal Caution | 6 | 5-7 | 75 | 118 | 57 | 66 | 15 | 0 | 88d40bbfabf028ad, df92b5b32a0a2807, 1de4ee0675d753b3 |
| Capacity Growth | 6 | 9-18 | 72-73 | 119-121 | 34-58 | 66 | 15 | 0 | 5d86f296694e3170, 6e735edc9552c773, 6c291c1f5f3b10c2 |
| Balanced Strategy | 6 | 1-10 | 74-75 | 119-121 | 48-55 | 67 | 15 | 0 | 905fe9285a486d82, fa89fd6d8acf11f5, eccbe926dcf9ec30 |
| Naive First-Time | 6 | 20 | 75 | 118 | 58 | 66 | 15 | 0 | e3182f259c9374e3, ff9b08b306d4bf17, 0e9cfc6c74ce9ba5 |

### Competitive Outcomes by Difficulty
| Group | Sessions | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Validation Failures | Representative Hashes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| easy | 12 | 1-20 | 73-75 | 118-121 | 34-58 | 66-67 | 15 | 0 | 88d40bbfabf028ad, 5d86f296694e3170, 905fe9285a486d82 |
| hard | 12 | 7-20 | 72-75 | 118-119 | 55-58 | 66-67 | 15 | 0 | df92b5b32a0a2807, 6e735edc9552c773, fa89fd6d8acf11f5 |

### Competitive Profile Outcomes by Difficulty
| Group | Sessions | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Validation Failures | Representative Hashes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Fiscal Caution / easy | 3 | 5 | 75 | 118 | 57 | 66 | 15 | 0 | 88d40bbfabf028ad, 1de4ee0675d753b3, 07e85aaf5eed3d01 |
| Capacity Growth / easy | 3 | 9 | 73 | 121 | 34 | 66 | 15 | 0 | 5d86f296694e3170, 6c291c1f5f3b10c2, 82216be1f11e8261 |
| Balanced Strategy / easy | 3 | 1 | 75 | 121 | 48 | 67 | 15 | 0 | 905fe9285a486d82, eccbe926dcf9ec30, 74c9226a7696469b |
| Naive First-Time / easy | 3 | 20 | 75 | 118 | 58 | 66 | 15 | 0 | e3182f259c9374e3, 0e9cfc6c74ce9ba5, 78c900b73c6ab72f |
| Fiscal Caution / hard | 3 | 7 | 75 | 118 | 57 | 66 | 15 | 0 | df92b5b32a0a2807, 5f31485ce8a3dcdd, 1ccbf550ea7d9453 |
| Capacity Growth / hard | 3 | 18 | 72 | 119 | 58 | 66 | 15 | 0 | 6e735edc9552c773, d6709b0ad7ae26b5, 927e1ae4b3b4d14c |
| Balanced Strategy / hard | 3 | 10 | 74 | 119 | 55 | 67 | 15 | 0 | fa89fd6d8acf11f5, 15e334456da3c1df, da744877b28b8fe6 |
| Naive First-Time / hard | 3 | 20 | 75 | 118 | 58 | 66 | 15 | 0 | ff9b08b306d4bf17, 9442870e9be85371, dd401fe5d3a1cc4b |

### Difficulty-Adaptive Action Comparison
| Difficulty | Holds | Action Commands | Monitor | Invest | Recruit | Commit |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| easy | 273 | 246 | 84 | 48 | 21 | 63 |
| hard | 282 | 309 | 147 | 48 | 21 | 63 |

- Adaptive hard policies should show more holds and monitors than easy when rival pressure triggers the adaptation layer.
- Compare player tradeoff metrics in the difficulty tables above against the static `difficulty-sweep` batch to see whether adaptation differentiates Easy/Hard endpoints for the same seed/profile.

### Competitive Action Frequency Signals
| Profile | Holds | Action Commands | Project Commands | Top Non-Hold Verb | Strategy Classification |
| --- | ---: | ---: | ---: | --- | --- |
| Fiscal Caution | 144 | 129 | 0 | Monitor (51) | Balanced Strategy |
| Capacity Growth | 129 | 153 | 0 | Monitor (63) | Intel-Gatherer |
| Balanced Strategy | 138 | 159 | 0 | Monitor (69) | Intel-Gatherer |
| Naive First-Time | 144 | 114 | 0 | Monitor (48) | Intel-Gatherer |

### Competitive Project Coverage
| Profile | Project Kinds | Final Active Projects | Final Monthly Draws |
| --- | --- | ---: | ---: |
| Fiscal Caution | None | 0 | 0 |
| Capacity Growth | None | 0 | 0 |
| Balanced Strategy | None | 0 | 0 |
| Naive First-Time | None | 0 | 0 |

### Evidence Limits
- Batch diagnostics use MCP transition summaries, final observations, and debriefs; they are not full replay artifacts.
- These diagnostics support gameplay and explanation review, not human-learning, empirical calibration, or policy-validity claims.
- Treat formula tuning or runtime expansion as a separate follow-up requiring stronger evidence.

---
