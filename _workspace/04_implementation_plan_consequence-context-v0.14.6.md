# Implementation Plan — Consequence timing and replay context v0.14.6

## Target slice

Make the existing visible consequence-link surface answer “when did this appear
and where can I locate it in the committed sequence?” using fields already
present in `consequence-links.mjs`. Keep private rival detail and future claims
out of the browser.

## Design

1. Add a pure formatter for link context that prefers `observed_month` for
   public signals and `turn` for committed effects/processes.
2. Include a replay state hash only when it is a non-empty host-provided string;
   otherwise show an explicit unavailable fallback without fabricating a hash.
3. Render the context as text adjacent to the existing source/detail and retain
   board focus and information-boundary copy unchanged.
4. Add deterministic module/renderer tests, update current docs/contracts, bump
   the patch version, and preserve historical records.

## In scope

- `gui/consequence-links.mjs`, the existing consequence renderer, and focused
  tests.
- Current core/presentation docs, changelog, release metadata, generated
  credits, and append-only workspace evidence.

## Out of scope

- Host routes/schemas, Rust simulation, commands, history/replay formats,
  persistence, assets/audio, or non-default browsers.

## Exit criteria

- Every visible link has deterministic timing text and explicit hash fallback;
  private/missing data stays unavailable rather than inferred.
- Existing target filtering, source labels, focus controls, all campaigns, and
  text-first fallback behavior remain intact.
- Focused/full checks, one medium-effort review, merged PR, and branch cleanup
  pass.
