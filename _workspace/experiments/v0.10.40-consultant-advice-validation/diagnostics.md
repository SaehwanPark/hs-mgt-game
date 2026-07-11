# Consultant Advice Validation Diagnostics — `v0.10.40-consultant-advice-validation`

- Code version: `0.10.40`
- Campaign: `competitive-regional-v1`
- Matrix: four existing policies × seeds `[42, 43, 44]` × difficulties `['normal', 'hard']`
- Evidence type: simulated-agent MCP traceability and debrief-retention validation

## Run outcomes

| Profile | Status | Months | Advice months | Debrief options | Debrief comparisons | Signatures | Validation failures | Final hash |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Fiscal Caution / normal / seed 42 | complete | 24 | 24 | 24 | 24 | 3 | 0 | db396cb8c5362ddc |
| Capacity Growth / normal / seed 42 | complete | 24 | 24 | 24 | 24 | 2 | 0 | 16ace0dc772b82e0 |
| Balanced Strategy / normal / seed 42 | complete | 24 | 24 | 24 | 24 | 3 | 0 | cef701ede4d5c162 |
| Naive First-Time / normal / seed 42 | complete | 24 | 24 | 24 | 24 | 3 | 0 | 71b814663df88a84 |
| Fiscal Caution / normal / seed 43 | complete | 24 | 24 | 24 | 24 | 3 | 0 | 07ea95139054c286 |
| Capacity Growth / normal / seed 43 | complete | 24 | 24 | 24 | 24 | 2 | 0 | 9cf1e60776f2c4da |
| Balanced Strategy / normal / seed 43 | complete | 24 | 24 | 24 | 24 | 3 | 0 | c88d320130c55d40 |
| Naive First-Time / normal / seed 43 | complete | 24 | 24 | 24 | 24 | 3 | 0 | 655949d617c7121a |
| Fiscal Caution / normal / seed 44 | complete | 24 | 24 | 24 | 24 | 3 | 0 | 0aab9a565fac80e4 |
| Capacity Growth / normal / seed 44 | complete | 24 | 24 | 24 | 24 | 2 | 0 | 7503824ce07c4047 |
| Balanced Strategy / normal / seed 44 | complete | 24 | 24 | 24 | 24 | 3 | 0 | 818a67d0a862c481 |
| Naive First-Time / normal / seed 44 | complete | 24 | 24 | 24 | 24 | 3 | 0 | 82e1ce0125a6758c |
| Fiscal Caution / hard / seed 42 | complete | 24 | 24 | 24 | 24 | 3 | 0 | 8a86dd27fdbddcc5 |
| Capacity Growth / hard / seed 42 | complete | 24 | 24 | 24 | 24 | 2 | 0 | 89521249dead95f1 |
| Balanced Strategy / hard / seed 42 | complete | 24 | 24 | 24 | 24 | 3 | 0 | 96d17f648d3e550f |
| Naive First-Time / hard / seed 42 | complete | 24 | 24 | 24 | 24 | 3 | 0 | ff9b08b306d4bf17 |
| Fiscal Caution / hard / seed 43 | complete | 24 | 24 | 24 | 24 | 3 | 0 | 000b772a2b97925f |
| Capacity Growth / hard / seed 43 | complete | 24 | 24 | 24 | 24 | 2 | 0 | 2731a64474b9178f |
| Balanced Strategy / hard / seed 43 | complete | 24 | 24 | 24 | 24 | 3 | 0 | 3024ec77a1c8d1c1 |
| Naive First-Time / hard / seed 43 | complete | 24 | 24 | 24 | 24 | 3 | 0 | 9442870e9be85371 |
| Fiscal Caution / hard / seed 44 | complete | 24 | 24 | 24 | 24 | 3 | 0 | f686e31fdad48c21 |
| Capacity Growth / hard / seed 44 | complete | 24 | 24 | 24 | 24 | 2 | 0 | dd23f8f160dfd370 |
| Balanced Strategy / hard / seed 44 | complete | 24 | 24 | 24 | 24 | 3 | 0 | f134baa3c7b6dc16 |
| Naive First-Time / hard / seed 44 | complete | 24 | 24 | 24 | 24 | 3 | 0 | dd401fe5d3a1cc4b |

## Interpretation

- The capture verifies that the existing advice surface is present, varies with visible observation categories, and remains available for month-by-month debrief comparison.
- Submitted commands are retained beside the options for discussion; this artifact does not score advice adherence or identify a correct action.
- Normal/Hard coverage exercises the same observation boundary under two fixtures; it is not a difficulty, balance, or Expert-winnability claim.

## Evidence limits

- These are deterministic simulated-agent policies, not human classroom observations.
- Repeated policy/seed coverage is evidence about reproducibility and inspectability, not independent player samples.
- No advice-quality, learning, calibration, policy-validity, or advisor-market conclusion is made.
- No runtime tuning, roster, payroll, hiring, AI advice behavior, or transition change is justified by this artifact alone.
