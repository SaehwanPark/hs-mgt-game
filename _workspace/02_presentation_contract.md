# Presentation Contract — Phase 5.1 semantic information containers v0.12.66

## Goal and authorization

Differentiate the executive desktop’s major information classes through
structure, typography, iconography, and restrained header treatment without
creating a client-side causal or simulation model.

## Container source ledger

| Container | Existing surface | Allowed presentation |
| --- | --- | --- |
| Board packet | Regional board and public signal panel | Orient actor-visible regional state with period/source context |
| Operations ledger | Selected system and facility detail | Show visible operating commitments, resources, and status |
| Intelligence report | Executive briefing | Separate public signals, timing, source, and information gaps |
| Regulatory letter | Current observation | Present bounded oversight/policy notice language |
| Project sheet | Pending processes | Track host-reported commitments and timing without promises |
| News wire | Committed history and replay | Group dated public reports and visible signal history |
| Executive action queue | Contextual action panel | Present host-catalogued decisions and local draft state |
| After-action report | Monthly result and resolution | Explain committed effects, history, and retrospective evidence |

## Visual and interaction contract

- `gui/semantic-containers.mjs` is the single catalog for eight classes. Each
  entry documents semantic purpose, header treatment, icon/marker,
  compact/expanded variants, accessibility label, large-text behavior,
  narrow-width behavior, print behavior, reduced-motion behavior, and the
  source/status preservation rule.
- `gui/index.html` applies one semantic-container class and data attribute to
  each existing panel. Non-color marker patterns and restrained borders add
  hierarchy while the current heading, source, status, exact-value, and text
  surfaces remain intact.
- `gui/semantic-container-proof.html` renders all catalog entries in a shared
  grid with a compact/expanded toggle, print/export control, responsive
  single-column reflow, and reduced-motion static behavior.

## Accessibility and fallback requirements

- Container distinctions use existing headings, visible text, ordinary DOM
  semantics, and non-color markers. Color, motion, and optional audio are not
  required to identify or understand the content.
- Compact and expanded variants preserve text meaning; large text reflows,
  narrow widths stack headers/content, and print keeps headings, borders,
  source/status text, and labels.
- The live panel content remains in the DOM and retains keyboard navigation.

## Authority, history, and replay boundaries

The catalog and proof accept static presentation definitions only. They do not
call a host, submit a command, mutate simulation state, resolve stochastic
inputs, rewrite history, change a state hash, or create debrief facts. Existing
host-sourced source/status language and actor-visible data remain authoritative.

## Asset provenance and verification

`visual.runtime-semantic-containers` is a project-generated registry-approved
semantic asset with source hash, visible-source description, accessible
equivalent, and no release image. Focused semantic-container tests, existing
GUI tests, asset/credits/metadata/documentation checks, full Python/Rust,
formatting, presentation-contract, and diff checks are required before merge.

## Non-goals and next gate

This slice does not add new host fields, facility geometry transitions,
client-side causality, private rival actions, metric visualization, motion,
audio, or a browser replay engine. Later roadmap phases own metric
visualization, motion, audio, and broader testing/QA.
