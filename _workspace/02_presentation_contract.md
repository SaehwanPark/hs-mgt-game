# Presentation Contract — Phase 6.2 First-month resolution sequence

## Authorized outcome

Make one committed `competitive-regional-v1` month understandable as an
ordered, skippable, replay-stable browser presentation. The host remains the
only source of commands, outcomes, observations, history, and hashes.

## Storyboard and source ledger

| Stage | Player-facing question | Authorized source | Display-only synchronization | Safe fallback |
| --- | --- | --- | --- | --- |
| submitted | What batch did I commit? | `ResolutionStep{submitted}` / `TransitionSummary.command` | Action queue and resolution heading | “Submitted batch unavailable.” |
| responses | What visible institutions responded? | `ResolutionStep{responses}` / committed events | Board links and report list | “No visible institutional responses.” |
| processes | What pending work advanced? | Before/after `pending_effects` | Pending-process panel | Count-only before/after text |
| operations | What operating result is visible? | After `observation.operations` | Metric summary | Exact “Unavailable” values |
| resources | What resources changed? | Before/after `ReadOnlyResources` | Resource header | Exact “Unavailable” values |
| effects | Which effects did the host commit? | `ResolutionEffect` / `TransitionSummary.effects` | Direct-effect list | “No direct committed effects.” |
| information | What new information arrived? | After actor-visible market/policy/gap fields | Briefing/report panel | “No new visible information.” |
| pending | What remains in flight? | After actor-visible pending effects | Pending panel | “No pending processes.” |

The sequence may attach a bounded attention priority to visible stages so that
critical committed effects are easy to find. This is a rendering order, not a
severity, probability, moral-valence, or hidden-state claim. The sequence must
not infer private rival intent, causal relationships, or outcomes from text.

## Host/client boundary

- Rust `competitive-resolution-v1` remains immutable and host-shaped.
- The browser may plan local order, focus, pacing, cue selection, and skip state.
- The browser must not submit commands, call transitions, resolve randomness,
  mutate history, write hashes, or turn a local comparison into causality.
- All step text is rendered immediately. Play and skip only change emphasis and
  progress, so no report can disappear when animation is skipped.

## Accessibility and fallback contract

- Every stage is a keyboard-reachable list item with source text.
- Play, pause, advance, skip, review, and historical-turn loading remain native
  buttons/inputs with visible status updates.
- Reduced motion uses immediate step selection; written content is unchanged.
- Audio is optional. A cue ID may be synchronized to a visible stage, but mute,
  unavailable audio, or reduced notifications leave the same text and board
  information available.
- Missing or malformed steps fall back to an explicit unavailable message.

## Replay and evidence limits

The same envelope and declared sequence policy must yield the same ordered
stage IDs, attention priorities, cue IDs, and surface synchronization metadata.
This is deterministic technical evidence, not evidence of first-time human
comprehension or usability. A keyboard-oriented fixture test verifies that a
first-time player can reach every control and that the written consequence chain
is present; human evaluation remains a later roadmap item.
