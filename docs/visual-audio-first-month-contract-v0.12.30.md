# Visual/audio first-month contract audit v0.12.30

**Status:** Complete for the bounded technical/interface-task contract
**Scope:** Proposal-aligned `competitive-regional-v1` first-month evidence
**Version:** 0.12.30

## Result

The Phase 0–13 technical visual/audio sequence is complete for the first
competitive month. The deterministic audit reports
`visual-audio-first-month-contract-v1` with status `complete`. It checks the
current browser source, focused contract tests, presentation boundary, and
generated provenance records without starting the game or calling a host.

The durable compact result is
`_workspace/experiments/v0.12.30-first-month-contract-audit/audit.json`.
Regenerate the full evidence projection with:

```bash
python3 scripts/audit_visual_audio_contract.py --pretty
```

## Contract coverage

| Obligation | Source evidence | Focused test evidence | Result |
| --- | --- | --- | --- |
| Start or load a host session | `gui/app.mjs` session launcher | `tests/test_gui_session_launch.py` | Pass |
| Inspect the actor-visible regional market | `gui/app.mjs` regional-world renderer | `tests/test_gui_regional_world.py` | Pass |
| Inspect Riverside and facilities | `gui/app.mjs` selected-entity fixture/renderer | `tests/test_gui_static_desktop.py` | Pass |
| Identify workforce/capacity and payer/rival context | `gui/app.mjs`, `gui/visual-catalog.json` | static desktop and regional-world tests | Pass |
| Draft two contextual actions with canonical metadata | `gui/app.mjs` catalog/draft path | contextual-action and first-month tests | Pass |
| Validate and submit through the host | `gui/app.mjs` validation/submit boundary | contextual-action and first-month tests | Pass |
| Review resolution metrics | `gui/app.mjs` resolution snapshots | `tests/test_gui_resolution.py` | Pass |
| Review direct effects and pending processes | `gui/app.mjs` effects/pending rendering | `tests/test_gui_resolution.py` | Pass |
| Receive optional audio and complete text equivalents | `gui/audio.mjs`, `gui/index.html` | audio and accessibility tests | Pass |
| Continue to the next observation | `gui/first-month.mjs`, `gui/app.mjs` | `tests/test_gui_first_month.py` | Pass |

All 14 phase documents from alignment through first-month continuity are
present. Generated visual/audio catalogs and `ASSET_CREDITS.md` are present.
The first-month rail's presentation-only boundary has no transition,
resolved-input, effect-queue, network, or WebSocket marker.

## Authority and limits

The host remains authoritative for session identity, actor-visible observations,
canonical commands, validation, stochastic inputs, transitions, committed
effects, history, state hashes, replay, and debriefs. The audit is repository
evidence only; it does not add a DTO, command, simulation rule, dependency,
transport, asset, audio source, or browser-owned game state.

This closure does not establish browser transport correctness, real viewport
rendering, contrast, screen-reader behavior, hardware audio, human usability,
lived accessibility, learning, engagement, calibration, balance, policy
validity, or domain-expert agreement. Third-party asset acquisition, detailed
geography, mobile support, and production deployment remain explicit
non-goals.

## Reopening gate

Reopen the technical track only when a new source-backed finding identifies a
missing visible relationship, an authority-boundary failure, or a reproducible
interface-task gap that current contracts cannot express. Human and educational
evaluation require a separately authorized evidence plan.
