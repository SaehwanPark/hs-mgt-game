# Rival Information Follow-Through Diagnostics

- **Batch id:** v0.10.43-rival-info-follow-through
- **Code version:** 0.10.43
- **Evidence type:** deterministic MCP capture comparing monitor-reactive, monitor-ignoring, and unmonitored simulated policies

## Run Summary

| Variant | Seed | Difficulty | Status | Transitions | Signals | Responses | Safe hold | Final hash |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| monitor-reactive | 42 | hard | complete | 24 | 3 | 3 | 0 | ca629c8f278b2843 |
| monitor-ignoring | 42 | hard | complete | 24 | 3 | 0 | 0 | df8d6c0da2f78dfb |
| unmonitored | 42 | hard | complete | 24 | 0 | 0 | 0 | df8d6c0da2f78dfb |
| monitor-reactive | 42 | expert | complete | 24 | 3 | 3 | 0 | 725fd80af1453047 |
| monitor-ignoring | 42 | expert | complete | 24 | 3 | 0 | 0 | a77df3947ba47a33 |
| unmonitored | 42 | expert | complete | 24 | 0 | 0 | 0 | a77df3947ba47a33 |
| monitor-reactive | 43 | hard | complete | 24 | 3 | 3 | 0 | 14d0b2709d3be26d |
| monitor-ignoring | 43 | hard | complete | 24 | 3 | 0 | 0 | 74126a29dfb9a8f9 |
| unmonitored | 43 | hard | complete | 24 | 0 | 0 | 0 | 74126a29dfb9a8f9 |
| monitor-reactive | 43 | expert | complete | 24 | 3 | 3 | 0 | 99c380c6d258386d |
| monitor-ignoring | 43 | expert | complete | 24 | 3 | 0 | 0 | d125eaeaf2085635 |
| unmonitored | 43 | expert | complete | 24 | 0 | 0 | 0 | d125eaeaf2085635 |
| monitor-reactive | 44 | hard | complete | 24 | 3 | 3 | 0 | 7aabf1c5a0108ce4 |
| monitor-ignoring | 44 | hard | complete | 24 | 3 | 0 | 0 | 972a868068f480bb |
| unmonitored | 44 | hard | complete | 24 | 0 | 0 | 0 | 972a868068f480bb |
| monitor-reactive | 44 | expert | complete | 24 | 3 | 3 | 0 | 1e04093dc7e96f26 |
| monitor-ignoring | 44 | expert | complete | 24 | 3 | 0 | 0 | 6ddb220d4aeb2973 |
| unmonitored | 44 | expert | complete | 24 | 0 | 0 | 0 | 6ddb220d4aeb2973 |

## Follow-Through Records

| Variant | Seed | Difficulty | Signal month | Response month | Kind | Mode | Command |
| --- | ---: | --- | ---: | ---: | --- | --- | --- |
| monitor-reactive | 42 | hard | 3 | 4 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-reactive | 42 | hard | 11 | 12 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-reactive | 42 | hard | 19 | 20 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-ignoring | 42 | hard | 3 | 4 | payer | ignored | recruit role=nurse headcount=1; hold |
| monitor-ignoring | 42 | hard | 11 | 12 | payer | ignored | negotiate payer=medicare rate_posture=neutral; hold |
| monitor-ignoring | 42 | hard | 19 | 20 | payer | ignored | negotiate payer=carrier_a rate_posture=conservative; hold |
| monitor-reactive | 42 | expert | 3 | 4 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-reactive | 42 | expert | 11 | 12 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-reactive | 42 | expert | 19 | 20 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-ignoring | 42 | expert | 3 | 4 | payer | ignored | recruit role=nurse headcount=1; hold |
| monitor-ignoring | 42 | expert | 11 | 12 | payer | ignored | negotiate payer=medicare rate_posture=neutral; hold |
| monitor-ignoring | 42 | expert | 19 | 20 | payer | ignored | negotiate payer=carrier_a rate_posture=conservative; hold |
| monitor-reactive | 43 | hard | 3 | 4 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-reactive | 43 | hard | 11 | 12 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-reactive | 43 | hard | 19 | 20 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-ignoring | 43 | hard | 3 | 4 | payer | ignored | recruit role=nurse headcount=1; hold |
| monitor-ignoring | 43 | hard | 11 | 12 | payer | ignored | negotiate payer=medicare rate_posture=neutral; hold |
| monitor-ignoring | 43 | hard | 19 | 20 | payer | ignored | negotiate payer=carrier_a rate_posture=conservative; hold |
| monitor-reactive | 43 | expert | 3 | 4 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-reactive | 43 | expert | 11 | 12 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-reactive | 43 | expert | 19 | 20 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-ignoring | 43 | expert | 3 | 4 | payer | ignored | recruit role=nurse headcount=1; hold |
| monitor-ignoring | 43 | expert | 11 | 12 | payer | ignored | negotiate payer=medicare rate_posture=neutral; hold |
| monitor-ignoring | 43 | expert | 19 | 20 | payer | ignored | negotiate payer=carrier_a rate_posture=conservative; hold |
| monitor-reactive | 44 | hard | 3 | 4 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-reactive | 44 | hard | 11 | 12 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-reactive | 44 | hard | 19 | 20 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-ignoring | 44 | hard | 3 | 4 | payer | ignored | recruit role=nurse headcount=1; hold |
| monitor-ignoring | 44 | hard | 11 | 12 | payer | ignored | negotiate payer=medicare rate_posture=neutral; hold |
| monitor-ignoring | 44 | hard | 19 | 20 | payer | ignored | negotiate payer=carrier_a rate_posture=conservative; hold |
| monitor-reactive | 44 | expert | 3 | 4 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-reactive | 44 | expert | 11 | 12 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-reactive | 44 | expert | 19 | 20 | payer | responded | negotiate payer=carrier_a rate_posture=neutral; hold |
| monitor-ignoring | 44 | expert | 3 | 4 | payer | ignored | recruit role=nurse headcount=1; hold |
| monitor-ignoring | 44 | expert | 11 | 12 | payer | ignored | negotiate payer=medicare rate_posture=neutral; hold |
| monitor-ignoring | 44 | expert | 19 | 20 | payer | ignored | negotiate payer=carrier_a rate_posture=conservative; hold |

These are deterministic simulated-policy traces. They establish visible signal-to-command traceability only; they do not establish causal value, decision quality, human learning, balance, or policy validity.
