# Strategy-Space Diagnostic Report
This diagnostic summary maps strategic actions, outcome distributions, and strategy-cluster classifications.

## Playtest Batch Diagnostics for `results.json`
- **Code version:** 0.9.7
- **Target:** difficulty-sweep
- **Seeds:** 42, 43, 44
- **Competitive difficulties:** easy, hard
- **Stabilization sessions:** 12
- **Competitive sessions:** 24

### Competitive Profile Outcomes
| Group | Sessions | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Validation Failures | Representative Hashes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Fiscal Caution | 6 | 5 | 75 | 118 | 57 | 66 | 15 | 0 | 88d40bbfabf028ad, 8a86dd27fdbddcc5, 1de4ee0675d753b3 |
| Capacity Growth | 6 | 9 | 73 | 121 | 34 | 66 | 15 | 0 | 5d86f296694e3170, 89521249dead95f1, 6c291c1f5f3b10c2 |
| Balanced Strategy | 6 | 1 | 75 | 121 | 48 | 67 | 15 | 0 | 905fe9285a486d82, 96d17f648d3e550f, eccbe926dcf9ec30 |
| Naive First-Time | 6 | 20 | 75 | 118 | 58 | 66 | 15 | 0 | e3182f259c9374e3, ff9b08b306d4bf17, 0e9cfc6c74ce9ba5 |

### Competitive Outcomes by Difficulty
| Group | Sessions | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Validation Failures | Representative Hashes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| easy | 12 | 1-20 | 73-75 | 118-121 | 34-58 | 66-67 | 15 | 0 | 88d40bbfabf028ad, 5d86f296694e3170, 905fe9285a486d82 |
| hard | 12 | 1-20 | 73-75 | 118-121 | 34-58 | 66-67 | 15 | 0 | 8a86dd27fdbddcc5, 89521249dead95f1, 96d17f648d3e550f |

### Competitive Profile Outcomes by Difficulty
| Group | Sessions | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Validation Failures | Representative Hashes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Fiscal Caution / easy | 3 | 5 | 75 | 118 | 57 | 66 | 15 | 0 | 88d40bbfabf028ad, 1de4ee0675d753b3, 07e85aaf5eed3d01 |
| Capacity Growth / easy | 3 | 9 | 73 | 121 | 34 | 66 | 15 | 0 | 5d86f296694e3170, 6c291c1f5f3b10c2, 82216be1f11e8261 |
| Balanced Strategy / easy | 3 | 1 | 75 | 121 | 48 | 67 | 15 | 0 | 905fe9285a486d82, eccbe926dcf9ec30, 74c9226a7696469b |
| Naive First-Time / easy | 3 | 20 | 75 | 118 | 58 | 66 | 15 | 0 | e3182f259c9374e3, 0e9cfc6c74ce9ba5, 78c900b73c6ab72f |
| Fiscal Caution / hard | 3 | 5 | 75 | 118 | 57 | 66 | 15 | 0 | 8a86dd27fdbddcc5, 000b772a2b97925f, f686e31fdad48c21 |
| Capacity Growth / hard | 3 | 9 | 73 | 121 | 34 | 66 | 15 | 0 | 89521249dead95f1, 2731a64474b9178f, dd23f8f160dfd370 |
| Balanced Strategy / hard | 3 | 1 | 75 | 121 | 48 | 67 | 15 | 0 | 96d17f648d3e550f, 3024ec77a1c8d1c1, f134baa3c7b6dc16 |
| Naive First-Time / hard | 3 | 20 | 75 | 118 | 58 | 66 | 15 | 0 | ff9b08b306d4bf17, 9442870e9be85371, dd401fe5d3a1cc4b |

### Competitive Action Frequency Signals
| Profile | Holds | Action Commands | Project Commands | Top Non-Hold Verb | Strategy Classification |
| --- | ---: | ---: | ---: | --- | --- |
| Fiscal Caution | 144 | 114 | 0 | Monitor (36) | Balanced Strategy |
| Capacity Growth | 126 | 138 | 0 | Monitor (48) | Balanced Strategy |
| Balanced Strategy | 132 | 150 | 0 | Monitor (60) | Intel-Gatherer |
| Naive First-Time | 144 | 90 | 0 | Monitor (24) | Balanced Strategy |

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
