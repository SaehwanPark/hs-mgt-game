# Implementation Plan — Visible institutional response links v0.14.8

## Target slice

Project the existing host `ResolutionStep` response items into the shared
consequence-link panel so visible actor reactions can be reviewed with the
same source and replay context as effects. Keep the browser presentation-only;
the host remains authoritative for response text, ordering, and history.

## Boundaries

- In scope: a strict response-link projection from `steps[id=responses]`, a
  renderer wiring change, focused malformed/empty tests, current docs, and
  synchronized provenance/device evidence.
- Out of scope: Rust/MCP routes or DTOs, event/effect generation, persistence/
  replay formats, action legality, assets/audio, campaign rules, and other
  browser engines.

## Acceptance criteria

1. Non-empty response items preserve host order and carry turn/state-hash
   context and a visible-source boundary.
2. A present empty/malformed response step yields written unavailable detail;
   an absent step yields no fabricated response link.
3. Response links do not receive target focus or effect delta claims unless the
   existing host item already supplies such data (it does not today).
4. Existing effect links, timing/hash context, source labels, and private-state
   exclusions remain unchanged.
5. Focused tests, full suites, documentation currentness, and presentation
   audits pass; the sole medium-effort reviewer reports no actionable issue.

## Verification plan

- `python3 -m unittest tests.test_consequence_links`
- Full Python discovery, Rust format/clippy/tests, Node syntax, documentation
  currentness/links, release metadata, asset/provenance/security/release,
  browser/offline/loading/audio/raster/contract, and device-proxy checks.
- Refresh only current device/provenance measurements after source changes;
  preserve historical evidence records.
