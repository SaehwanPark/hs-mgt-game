# Visual and Audio Phase 4 — Resolution and Causal Feedback

Status: Implemented, reviewed once, and merged in PR #171.

Phase 4 makes one committed `competitive-regional-v1` month legible without
changing the transition. The host returns a typed, actor-visible resolution
envelope; the browser supplies only local pacing and review controls. Audio and
assets remain Phase 5 work.

## Typed resolution contract

The planned `competitive-resolution-v1` envelope is a non-mutating read of a
committed transition. It contains:

- session/campaign/turn and committed state-hash metadata;
- decision-time and post-transition actor-visible snapshots, including
  resources and operating observations;
- eight ordered steps: submitted batch, visible responses, process advancement,
  operating result, resource changes, direct effects, newly visible information,
  and updated pending processes;
- existing committed event/effect source text and direct effect metadata; and
- replay selection metadata for the requested committed turn.

The read accepts `get_resolution(session_id, turn?)`. Omitted `turn` selects the
latest committed month; a supplied turn selects an immutable historical month.
The tool rejects unsupported campaigns and unavailable history explicitly and
never calls `submit_turn`.

## Source and authority map

| Presentation | Source | Boundary |
| --- | --- | --- |
| Submitted batch | committed `TransitionSummary.command`/existing action response | host history |
| Institutional responses | committed transition events | host history |
| Process advancement | actor-visible pending effects before/after | `observe_for_human` projection |
| Operating result | actor-visible `ReadOnlyOperations` before/after | player observation |
| Resource changes | actor-visible `ReadOnlyResources` before/after | player resources |
| Direct effects | accepted committed transition effect surface | host transition summary |
| New information | actor-visible market/policy/information-gap fields | player observation |
| Pending processes | actor-visible pending-effect projection | player observation |

The client may compare before/after values to label a change. It must not turn
that comparison into an inferred causal graph. Direct effect labels remain
host-sourced, and hidden true state, resolved stochastic inputs, private rival
actions, and effect queues remain unavailable.

## Browser behavior

After a successful Phase 3 submit, the action adapter may call `getResolution`
and render the committed month. The page keeps all textual step content
available immediately, then uses local highlighting/pacing for play. Pause,
skip-to-end, and review controls change only presentation state. A historical
month can be loaded through the same read-only adapter without advancing the
session. Native `prefers-reduced-motion` disables pacing transitions while
preserving the complete result.

If the optional resolution read or subsequent presentation refresh fails after
`submitTurn` has succeeded, the UI reports the committed response separately
from the refresh error and does not claim that the transition was rejected.

## Static review checklist

1. Submit a valid graphical batch and confirm the committed resolution loads.
2. Locate all eight ordered steps, the before/after operations/resources, the
   state hash, direct effects, new information, and pending processes.
3. Pause and skip the sequence; confirm all textual results remain available.
4. Review a historical committed month and confirm the session turn/history/
   hash do not change.
5. Exercise missing, unsupported, invalid-turn, and refresh-error states.
6. Enable reduced motion and verify no result or control disappears.
7. Confirm no private rival, true-state, resolved-input, effect-queue, causal
   graph, audio, asset, or network behavior appears.

These are technical/interface-task checks only. They do not establish human comprehension,
usability, lived accessibility, learning, engagement,
calibration, balance, domain validity, or policy validity.

## Explicit non-goals and next gate

This phase does not add transition formulas, stochastic inputs, a causal
inference engine, audio playback, assets, a general replay editor, other
campaigns, mobile redesign, or an instructor true-state view. It does not
change command legality, history, hashes, replay verification, or debrief
generation.

Phase 5 is the next candidate: bounded music/cue presentation with independent
controls, visual equivalents, provenance/credits, and deterministic mapping
from visible committed conditions.
