# Implementation Plan — Phase 12 regional-affiliation stage-transition sequence v0.13.35

## Task restatement

Continue Phase 12.2 with a bounded current stage-transition sequence record for
`regional-affiliation-v1`. Make the deterministic host-owned six-stage path and
terminal completion legible through typed stages, successor mapping, legal
command gates, visible labels, history, and replay without claiming a new
browser animation or instructor surface.

## Current understanding

- `AffiliationStage` defines six decision stages followed by `Complete`, and
  `AffiliationStage::next` owns the deterministic successor relation.
- The affiliation transition validates commands against the current stage and
  advances exactly one stage per committed transition.
- Campaign coverage exposes a host-owned stage label, process, history, and
  replay metadata; the current live browser launcher remains
  `competitive-regional-v1` only.

## Target slice

Add `docs/evaluation/phase12-regional-affiliation-stage-transition-sequence.json`
and a parity test that record:

- the ordered six-stage plus completion sequence and successor IDs;
- the command gate for each decision stage and the written uncertainty boundary;
- host stage/process labels, one-transition advancement, history/replay
  alignment, and terminal completion behavior; and
- the no-browser-animation, no-hidden-input, no-new-asset, and human-review
  limits.

## Assumptions

- This is current host-projected sequence evidence, not a new campaign route or
  direct browser-native affiliation sequence implementation.
- A stage transition may expose the committed stage, command/result, source,
  status, effects, and uncertainty, but not resolved inputs or future outcomes.
- Existing CLI and host history/replay contracts are the authoritative sources;
  written stage labels remain complete if visual/audio presentation is absent.

## Minimal implementation plan

1. Add the stage-transition sequence ledger and source-parity test.
2. Check the Phase 12.2 sequence item and synchronize canonical docs, lessons,
   version metadata, generated credits, and additive request/contract/QA/handoff
   records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next roadmap item.

## Non-goals

- Do not add browser-native affiliation animation, new route, runtime field,
  persistence, screenshot, instructor view, visual/audio asset, or authority
  path.
- Do not expose resolved inputs, private rationale, hidden thresholds, legal
  validity, causal certainty, or future partner/integration outcomes.

## Stop conditions

Stop if the ordered sequence cannot be source-linked to typed host stages,
successor logic, legal command gates, visible labels, history/replay, and
written fallback without changing runtime behavior or authority.

## Risk label

Risk: low

Reason: The slice records already-implemented deterministic host transitions
and presentation boundaries without changing the simulation or browser route.
