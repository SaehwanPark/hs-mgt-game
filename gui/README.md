# GUI executive desktop and adapter reference

## Players: use the live GUI host

From the repository root, run:

```bash
cargo run --bin hs-mgt-game-gui
```

Keep the process running and open the printed loopback URL. The live GUI
currently supports `competitive-regional-v1`. Complete instructions and
troubleshooting are in [`docs/guides/gui-how-to-play.md`](../docs/guides/gui-how-to-play.md).

Opening `gui/index.html` directly or through a generic static server intentionally
shows fixture/demo mode; it cannot start a live scenario by itself.

## SVG rendering proof

Open `gui/svg-proof.html` directly or through a static server to inspect the
Phase 1.2 deterministic SVG fixture. It uses `scene.mjs` and the selected
Variant A vocabulary, exposes institution/facility selection through keyboard
reachable SVG controls, and includes explicit generic/uncertain fallbacks. The
proof page is fixture-only: it does not load a host, submit a command, or create
simulation state.

## Riverside identity proof — shared health-system kits

Open `gui/identity-proof.html` directly or through a static server to inspect
the Phase 2.1 fictional Riverside, Northlake, and Summit identity kits. It
shows the selected source and release mark, monochrome treatment, compact
marker, facility sign, report header, text badge, audio motif reference, and
generic fallback. The proof is fixture-only and does not load host state or
change a session.

## Actor-family language proof

Open `gui/actor-family-proof.html` directly or through a static server to
inspect the shared Phase 2.2 fictional payer, regulator, labor, employer,
community, board, policy coalition, and independent-provider language. It
shows each family’s glyph, report-frame pattern, written notification style,
optional identity-sonic tag, visible source, and generic fallback. The proof is
fixture-only and does not load host state or change a session.

## Facility component proof

Open `gui/facility-proof.html` directly or through a static server to inspect
the Phase 3.1 fictional general-hospital base, patient-tower, and
emergency-department components. It
shows the selected compact release derivative, seven composable layers, visible
layer sources, written equivalents, non-color patterns, and generic facility
fallback. The proof is fixture-only and does not load host state or change a
session.

## Audio direction proof

Open `gui/audio-proof.html` directly or through a static server to inspect the
Phase 1.3 generated Web Audio direction candidates. It documents loudness,
peak, duration, loop, and ducking targets and exposes visible source/text
equivalents beside confirmation, rejection, report, identity, ambience,
pressure, and environmental previews. The proof is fixture-only: it does not
load a host, change a session, or replace the live audio client.

## Developers: adapter contracts

This is a dependency-free browser surface over typed actor-visible MCP
presentation, action, and resolution contracts plus optional generated audio.
For static integration work, open `gui/index.html` through a static file server and
provide a live or recorded read-only adapter:

```js
window.HsMgtGameReadOnlyAdapter = {
  sessionId: "session-1",
  async startSession({ campaign, seed, difficulty }) {},
  async getPresentation(sessionId) {
    // Call get_presentation or return a recorded envelope with the same schema.
  },
  async getRegionalWorld(sessionId) {},
  async getCampaignCoverage(sessionId) {},
};
```

The read-only client expects `schema_version: "competitive-read-only-v1"` and
renders the typed `session`, `resources`, `observation`, `institutions`,
`pending_effects`, `history`, `latest_transition`, and `replay` fields. It can
consume live MCP output or a recorded envelope without knowing which source
provided it. The demo envelope is display fixture data, not a second simulation
state, and remains available when no read-only adapter is configured.

For the Phase 3/4 action and resolution path, inject a separate host adapter with
`getPresentation`, `getActionCatalog`, `validateTurn`, and `submitTurn`. The
page then renders forms from the host action catalog, keeps draft rows locally,
and submits only an unchanged batch that the host marked valid:

```js
window.HsMgtGameActionAdapter = {
  sessionId: "session-1",
  async startSession({ campaign, seed, difficulty }) {},
  async getPresentation(sessionId) {},
  async getRegionalWorld(sessionId) {},
  async getActionCatalog(sessionId) {},
  async validateTurn(sessionId, commandText) {},
  async getResolution(sessionId, turn) {},
  async submitTurn(commandText) {},
  async getCampaignCoverage(sessionId) {},
};
```

`createReadOnlyClient` never calls `submitTurn`. The action-builder path is
enabled only when `HsMgtGameActionAdapter` is supplied; it submits only an
unchanged host-validated batch. The legacy `createThinClient` and
`HsMgtGameAdapter.submitTurn` export remain available for compatibility with
the earlier thin-client proof, but are not wired into the Phase 3/4 page.
Host/core code remains authoritative for commands, transitions, randomness,
history, hashes, and debriefs.

After a successful action submission, `getResolution(sessionId, turn)` may
return `schema_version: "competitive-resolution-v1"`. The page renders the
eight host-sourced resolution steps, before/after operating/resource values,
direct committed effects, and state hash. Play, pause, skip, review, and a
historical-turn read are local presentation controls; `getResolution` never
advances the session. Text remains in the DOM when paused or reduced motion is
enabled.

When supplied, `getRegionalWorld(sessionId)` returns
`schema_version: "competitive-regional-world-v1"`. The page renders a
schematic identity map, visible demand/access/process overlays, owned facility
detail, and lagged public rival signals. Map selection and navigation are local
presentation state; rival private detail remains explicitly unavailable.

When supplied, `getCampaignCoverage(sessionId)` returns
`schema_version: "campaign-coverage-v1"` for the `stabilization` or
`regional-affiliation` campaign. The projection keeps each campaign's briefing,
visible metrics, actor signals, process status, decision forms, immutable
history, replay metadata, and host-provided debrief distinct. Decision forms
substitute only host-provided parameter values into the host command template;
the existing `submitTurn` path remains the only mutation path. Host rejection is
shown as a recoverable error and does not fabricate a local transition.

For reproducible interface-task traces, inject an optional recorder from
`playtest.mjs` into any client. It emits `schema_version: "gui-playtest-v1"`
with declared campaign/role/task metadata, allowlisted onboarding/settings/
recovery/command/validation/audio/history/hash/semantic-snapshot events, and
separate evidence lanes. It never stores raw adapter payloads, true state,
resolved inputs, effect queues, private rival actions, hidden DOM payloads, or
model hidden reasoning:

```js
import { createPlaytestRecorder } from "./playtest.mjs";

const recorder = createPlaytestRecorder({
  metadata: {
    campaign: "stabilization-v1",
    role: "first-time",
    task: "complete-first-decision",
    interface_mode: "browser-adapter",
    accessibility_mode: "reduced-motion",
    capture_method: "semantic-recorder",
  },
});
const client = HsMgtGui.createReadOnlyClient({ recorder });
recorder.attach(document);
await client.load();
console.log(recorder.toJSON());
```

Run the deterministic diagnostic over a capture with
`python3 scripts/diagnose_gui_playtests.py capture.json`. The protocol records
interface-task evidence only; it does not score strategies or establish human
usability, accessibility, learning, engagement, calibration, balance, or policy
validity.

For repeated declared captures, run the Phase 9 comparison with
`python3 scripts/analyze_gui_playtests.py tests/fixtures/gui_playtest_matrix`.
The analysis preserves campaign/role/task/seed/accessibility distinctions and
emits only deterministic evidence-gap/recovery hypotheses plus explicit limits;
it never changes the GUI, simulation, or host history.

Phase 2/3/4/5/6/7/8/10/11/12/13 review checklist:

- load a live or recorded envelope and observe the loading-to-loaded state;
- locate typed cash, AP, political capital, trust, and session metadata;
- inspect current observation, observed player capacity/facility metrics, and
  public market/information-gap signals;
- follow a pending process and monthly result back to its typed source;
- inspect committed transitions and state hashes without changing the turn;
- exercise empty, missing, unsupported-schema, and adapter-error states; and
- verify that the read-only path does not expose or call command submission.
- with the action adapter, add/revise/remove drafts, validate through the host,
  and confirm submit is unavailable until validation passes.
- after a committed submit, locate all eight resolution steps and compare the
  before/after snapshots without treating differences as inferred causality;
- pause, skip, review a historical committed turn, and enable reduced motion;
  confirm text remains complete and no session transition occurs.
- enable optional audio, exercise independent channels, mute, focus loss, and
  reduced notifications; confirm the same visual/text result remains complete.
- load the regional-world projection, select each public/owned entity, switch
  overlays, follow navigation links, and confirm public-signal lag and missing
  private detail remain labeled.
- load stabilization and regional-affiliation campaign coverage, confirm their
  distinct role/stage/briefing/metric/actor/process surfaces, and submit a
  host-shaped decision through the canonical command path.
- exercise a rejected campaign command, confirm the error is recoverable, and
  verify history/replay/debrief output remains host-sourced.
- open onboarding/settings, toggle reduced motion and written equivalents,
  activate retry after an adapter failure, attach a `gui-playtest-v1` recorder,
  and verify semantic snapshots contain only allowlisted visible controls.
- run the deterministic diagnostic on the capture twice and confirm failure
  classes and evidence lanes are stable.
- use the skip link or presentation navigation to reach briefing, actions,
  resolution, and debrief without pointer input;
- switch Standard/Large text size and confirm the local setting is reflected
  without changing host commands or session data;
- open the status-language legend and confirm each status has text plus a
  non-color symbol/pattern cue;
- hide optional cue explanations and confirm written results, observations,
  history, resolution, and debrief remain visible.
- start `competitive-regional-v1` through an adapter that maps to the existing
  host session-start operation, confirm the returned session ID loads typed
  presentation, then load an existing session ID;
- exercise missing start capability, malformed session envelopes, invalid seed,
  and failed replacement loads without losing the current rendered session or
  calling command submission.
- follow the first-month path rail from start/load through visible inspection,
  two local drafts, host validation, unchanged submission, resolution, and
  refreshed presentation; confirm it reaches Continue only after both host reads
  succeed.
- revise or remove a draft after validation and confirm the rail returns to its
  draft/validation handoff without limiting the existing draft controls; reject
  a host operation and confirm the current session and path remain recoverable.

This checklist is a technical/interface-task proxy, not human usability or
lived-accessibility evidence.

Visual identity and marker tokens come from the project-generated
`visual-catalog-v1` in `visual.mjs`; they label visible systems, facilities,
overlays, and processes while preserving source/status text. Unknown identities
and categories use explicit generic fallbacks. The registry and credits are
`visual-catalog.json` and `ASSET_CREDITS.md`.

Asset audit: zero downloaded assets, external fonts, network calls, or image/audio
files. CSS, HTML, JavaScript, generated visual glyphs, and generated Web Audio
recipes are the complete surface. The typed projection contains no true-world state, resolved stochastic
inputs, private rival actions, or client-side cost formula. Phase 5 audio, Phase 6
regional-world projection, and Phase 7 campaign coverage are optional,
visible-only, registry-recorded, and presentation-only; Phase 8 capture and
diagnostics plus Phase 9 comparison are optional, allowlisted, and
 presentation/test evidence only. Phase 10 accessibility behavior is local
presentation state and does not establish human accessibility. Phase 11
session launch/load is an optional host adapter boundary and does not create
local session state. Phase 12 visual identity/marker lookup is a generated,
visible-only vocabulary and does not create host facts or local game state. Phase
13 first-month continuity is a local text-first stage projection; it does not
create a host payload, client-side legality/outcome rule, transition, or local
simulation state.
Richer causal
overlays, recorded assets, true geography, and broader campaign expansion
require a new bounded proposal.
