# Visual/audio Phase 10 — Accessibility and visual-language hardening

**Status:** Implemented and verified on the Phase 10 branch; PR/CI/merge pending
**Scope:** Keyboard navigation, text scaling, status language, and optional cue-explanation presentation
**Version:** 0.12.26

## User and use context

The first target is a first-time executive player using a laptop browser. A
reproducible AI-agent profile and a contributor without browser automation are
secondary users of the same semantic contract. The immediate job is to find the
briefing, move to a decision or result, understand visible status categories,
and retain written information when audio or motion is unavailable or unwanted.

These checks are technical interface proxies. They do not establish human
usability, lived accessibility, learning, engagement, or domain-expert validity.

## Implemented contract

### Navigation and focus

- A skip link moves keyboard focus to the executive briefing.
- A presentation navigation landmark links to briefing, action, resolution, and
  debrief regions using stable IDs.
- Focus-visible controls use a high-contrast outline with an offset; the
  existing responsive layout and reduced-motion rule remain in place.
- The desktop is no longer one global live region. Existing targeted status and
  polite live nodes report loading, settings, audio, recovery, and resolution
  state without re-announcing every rendered panel.

### Status language

The status vocabulary remains supplied by host/fixture presentation data:
`Stable`, `Improving`, `Watch`, `Uncertain`, `Constrained`, `Delayed`,
`Critical`, `Revised`, and `Reported`. The legend pairs each visible label with
  a non-color symbol/pattern cue. Rendered status nodes expose `data-status`, a symbol, and
an accessible label; the client does not derive severity from hidden or
unavailable metrics.

### Text scale and cue explanations

- `Standard` and `Large` text sizes are local presentation settings persisted
  through the existing settings storage boundary when available.
- Settings remain session-local when storage is unavailable or malformed.
- Reduced motion, text scale, and optional cue explanations are independent.
- Turning off cue explanations hides only the optional audio explanation
  paragraph. Written observations, decisions, results, history, resolution,
  causal effects, and debrief content remain present.

## Authority and determinism

No new host/MCP endpoint or DTO is introduced. Navigation, CSS, and settings do
not submit commands or alter host state. Text scale and cue-explanation state
are not included in command text, simulation transitions, stochastic inputs,
history, state hashes, replay artifacts, audio-source classification, or
debrief output.

## Verification and limits

Focused static tests check stable landmarks, status vocabulary and metadata,
text-scale persistence markers, targeted live-region semantics, boundary
exclusions, and Node syntax. The focused suite has 56 passing tests and the
full Python suite has 288; Rust, formatting, clippy, release metadata, and
diff checks also pass. Without a
browser driver, contrast measurement, screen-reader behavior, viewport
rendering, and lived accessibility remain unresolved human questions.

## Deferred work

- No real campaign launch/session-creation flow or local simulation is added.
- No visual asset download, licensed art registry expansion, map redesign, or
  audio-source change is included.
- The broader first competitive vertical slice, asset governance, and human
  evaluation remain separate bounded items in `SPEC.md`.
