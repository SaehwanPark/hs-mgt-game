# Consultant Advice Usage Diagnostics for `results.json`
- **Batch id:** v0.10.41-consultant-advice-usage
- **Code version:** 0.10.41
- **Evidence type:** deterministic MCP capture of advice-aware and advice-ignoring simulated policy decisions

## Run Results
| Profile | Mode | Seed | Difficulty | Months | Validation failures | Exact continuity | Debrief records | Final hash | Control hashes |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | --- | --- |
| Fiscal Caution | control | 42 | normal | 24 | 0 | 24 | 24 | db396cb8c5362ddc | True |
| Fiscal Caution | advice-aware | 42 | normal | 24 | 0 | 24 | 24 | 782d0f39ef52031d | n/a |
| Naive First-Time | control | 42 | normal | 24 | 0 | 24 | 24 | 71b814663df88a84 | True |
| Naive First-Time | advice-aware | 42 | normal | 24 | 0 | 24 | 24 | 022bffde13bfd469 | n/a |
| Fiscal Caution | control | 42 | hard | 24 | 0 | 24 | 24 | 8a86dd27fdbddcc5 | True |
| Fiscal Caution | advice-aware | 42 | hard | 24 | 0 | 24 | 24 | cec31e0fd5ed21c3 | n/a |
| Naive First-Time | control | 42 | hard | 24 | 0 | 24 | 24 | ff9b08b306d4bf17 | True |
| Naive First-Time | advice-aware | 42 | hard | 24 | 0 | 24 | 24 | c8807ab59cb05aef | n/a |
| Fiscal Caution | control | 43 | normal | 24 | 0 | 24 | 24 | 07ea95139054c286 | True |
| Fiscal Caution | advice-aware | 43 | normal | 24 | 0 | 24 | 24 | 18f7454f6a6cdbbf | n/a |
| Naive First-Time | control | 43 | normal | 24 | 0 | 24 | 24 | 655949d617c7121a | True |
| Naive First-Time | advice-aware | 43 | normal | 24 | 0 | 24 | 24 | 0c49b5a9457e0e5f | n/a |
| Fiscal Caution | control | 43 | hard | 24 | 0 | 24 | 24 | 000b772a2b97925f | True |
| Fiscal Caution | advice-aware | 43 | hard | 24 | 0 | 24 | 24 | bcc8430aeec6f235 | n/a |
| Naive First-Time | control | 43 | hard | 24 | 0 | 24 | 24 | 9442870e9be85371 | True |
| Naive First-Time | advice-aware | 43 | hard | 24 | 0 | 24 | 24 | 3c3ed79ce01ae2c1 | n/a |
| Fiscal Caution | control | 44 | normal | 24 | 0 | 24 | 24 | 0aab9a565fac80e4 | True |
| Fiscal Caution | advice-aware | 44 | normal | 24 | 0 | 24 | 24 | 084c9c140e6f40b1 | n/a |
| Naive First-Time | control | 44 | normal | 24 | 0 | 24 | 24 | 82e1ce0125a6758c | True |
| Naive First-Time | advice-aware | 44 | normal | 24 | 0 | 24 | 24 | 92030862ab3ef7d2 | n/a |
| Fiscal Caution | control | 44 | hard | 24 | 0 | 24 | 24 | f686e31fdad48c21 | True |
| Fiscal Caution | advice-aware | 44 | hard | 24 | 0 | 24 | 24 | d42181d9d9400258 | n/a |
| Naive First-Time | control | 44 | hard | 24 | 0 | 24 | 24 | dd401fe5d3a1cc4b | True |
| Naive First-Time | advice-aware | 44 | hard | 24 | 0 | 24 | 24 | 9d5cf61621b38a92 | n/a |

## Advice-Aware Decision Signals
These counts describe deterministic policy choices and command alignment. They do not measure advice uptake, quality, causal impact, or learning.

| Profile | Seed | Difficulty | Followed | Fallback | Safe hold | Declined | A | B | C | D |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Fiscal Caution | 42 | normal | 24 | 0 | 0 | 0 | 0 | 0 | 24 | 0 |
| Naive First-Time | 42 | normal | 12 | 9 | 3 | 0 | 0 | 24 | 0 | 0 |
| Fiscal Caution | 42 | hard | 24 | 0 | 0 | 0 | 0 | 0 | 24 | 0 |
| Naive First-Time | 42 | hard | 12 | 9 | 3 | 0 | 0 | 24 | 0 | 0 |
| Fiscal Caution | 43 | normal | 24 | 0 | 0 | 0 | 0 | 0 | 24 | 0 |
| Naive First-Time | 43 | normal | 12 | 9 | 3 | 0 | 0 | 24 | 0 | 0 |
| Fiscal Caution | 43 | hard | 24 | 0 | 0 | 0 | 0 | 0 | 24 | 0 |
| Naive First-Time | 43 | hard | 12 | 9 | 3 | 0 | 0 | 24 | 0 | 0 |
| Fiscal Caution | 44 | normal | 24 | 0 | 0 | 0 | 0 | 0 | 24 | 0 |
| Naive First-Time | 44 | normal | 12 | 9 | 3 | 0 | 0 | 24 | 0 | 0 |
| Fiscal Caution | 44 | hard | 24 | 0 | 0 | 0 | 0 | 0 | 24 | 0 |
| Naive First-Time | 44 | hard | 12 | 9 | 3 | 0 | 0 | 24 | 0 | 0 |

## Evidence Limits
- Advice-aware and control policies are deterministic simulated agents, not human players.
- Changing the policy changes commands and outcomes; paired runs do not establish causal advice value.
- The capture tests visible option interpretation, fallback behavior, and observation/history/debrief continuity.
- A future advisor-market slice remains deferred unless a separate finding identifies a concrete limitation in the generic baseline.
