# Evidence Map - Rival Information Follow-Through

## Scope

Extend the v0.10.37 monitor-value evidence from exposure to next-turn
decision traceability.

## Sources Reviewed

- Canonical project and harness documents.
- `docs/playtest-findings-v0.10.37.md` and `docs/playtest-findings-v0.10.42.md`.
- The v0.10.37 monitor capture and current MCP wrapper.

## Mechanisms and Institutions

- The human-led health system receives delayed, partial rival information.
- Monitoring is an observation-surface action; this slice does not change its
  modeled cost or transition effects.
- The three policy arms are evidence controls, not new strategic actors.

## Actor Incentives and Information

- Reactive policies inspect only the current actor-visible observation and
  visible resource hints.
- Monitor-ignoring policies receive the same monitor signals but deliberately
  retain the baseline command stream.
- Unmonitored controls do not receive monitor-intel lines.

## Assumptions

- Signal-to-command linkage is a gameplay/evidence abstraction, not a model of
  human cognition or validated decision quality.
- Repeated deterministic runs are regression evidence, not human samples.
- Different reactive commands make endpoint comparisons non-causal.

## Unresolved Questions

- Whether human or instructor-facing users find the signal-to-response trace
  sufficiently clear remains untested.
- Whether any future runtime information change is needed remains unresolved.

## Design Implications

- Preserve the current observation, history, debrief, and replay boundaries.
- Report signal exposure, ignored signals, and next-turn responses separately.
- Keep difficulty and monitor mechanics deferred absent a concrete gap.

## Risks

- A deterministic reactive wrapper can be mistaken for human monitor use.
- Reactive endpoint differences can be misread as causal monitor benefit.
- Signal wording changes could silently break the parser; focused parser tests
  and a complete matrix must expose that failure.
