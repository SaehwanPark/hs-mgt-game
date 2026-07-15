# Evidence Map — Phase 10 accessibility and visual-language hardening v0.12.26

## Scope

This map supports a presentation-only accessibility slice. It does not support
claims about lived accessibility or human comprehension. The artifact must make
the existing actor-visible GUI easier to navigate and interpret while keeping
host authority, written results, and campaign semantics unchanged.

## Sources Reviewed

- `SPEC.md` sections `Visual and motion language`, `Assets, licensing, and
  accessibility`, `First competitive vertical slice`, and `Verification and AI
  testplay`.
- `docs/visual_audio_upgrade_proposal.md` Sections 6.3–6.9, 7, 9, 13, 14,
  15, and 16.
- `gui/index.html`: current semantic sections, CSS status classes, controls,
  responsive breakpoints, and reduced-motion media rule.
- `gui/app.mjs`: local presentation settings, status rendering, onboarding,
  and the host-bound read/action/resolution clients.
- Existing GUI tests and Phase 8 readiness protocol.
- Canonical project docs and the harness team spec.

## Mechanisms and Institutions

This slice has no new simulation mechanism or actor. The presentation mechanism
is a visible information hierarchy:

```text
first-run player intent
  -> keyboard landmark/skip navigation
  -> briefing, action, result, or debrief surface
  -> explicit status language and source/equivalent text
```

The executive player remains the only user authority in the client. The host
continues to own command legality, transition resolution, stochastic inputs,
history, hashes, replay, and debrief content.

## Actor Incentives and Information

- The player needs to distinguish observed, uncertain, delayed, revised, and
  committed information without relying on color, animation, or audio.
- A keyboard-only or enlarged-text user needs a predictable route to the same
  visible information and controls.
- The AI-agent test harness needs stable semantic IDs and deterministic setting
  state; it must not receive hidden model or simulation fields.
- Contributors need a small presentation contract that can be inspected without
  a browser driver.

## Assumptions

- Native HTML landmarks, focus behavior, CSS custom properties, and local
  storage are sufficient; no accessibility framework or browser dependency is
  required.
- Status labels already supplied by the host or fixture are the authoritative
  category vocabulary; the client may add shape/pattern cues but may not infer
  a new severity or outcome.
- Text scaling is a local presentation preference and must not change layout
  data, command text, host validation, history, hashes, or audio classification.
- Cue-equivalent visibility can be scoped to explanatory audio text while the
  written monthly result, observation, and debrief remain always present.

## Unresolved Questions

- Lived screen-reader behavior, contrast perception, cognitive load, and text
  scaling comfort require people and remain outside this technical slice.
- Whether the first competitive experience needs a browser launch/session API
  cannot be answered by the current host contracts and is deferred rather than
  simulated locally.
- Exact visual identity, licensed art, and map assets remain separate future
  governance work; this slice uses existing CSS/generated symbols only.

## Design Implications

- Add a skip link and a small navigation landmark to make the current briefing,
  action, resolution, result, and debrief regions reachable in a stable order.
- Keep `main` out of the live-region boundary; use targeted status/live nodes so
  a refresh does not make the entire desktop noisy to assistive technology.
- Add a visible status legend with text, symbol, and pattern language for every
  supported status category. Status rendering must expose a machine-readable
  status value and accessible label.
- Add a persisted standard/large text-scale control and keep reduced motion
  independent. The setting must apply immediately and degrade safely when
  storage is unavailable.
- Make the existing cue-equivalent setting actually control only optional audio
  explanatory copy; never hide decision results or causal/debrief text.
- Add focused static tests for the contract because browser automation is out of
  scope; label these checks as technical proxies.

## Risks

- A global live region can cause excessive announcements; targeted status nodes
  and a skip path reduce that risk without changing host data.
- Scaling may expose overflow at small widths; existing responsive breakpoints
  and focused CSS markers must remain intact.
- A cue-equivalent preference could accidentally hide essential information;
  the implementation must scope it to optional audio explanation only.
- A client-side status mapping could leak or invent hidden state; it must use
  only the existing status string/category and never derive a score.
