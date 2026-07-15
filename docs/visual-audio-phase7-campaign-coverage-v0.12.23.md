# Visual and Audio Phase 7 — Campaign Coverage

Status: Implemented, verified, and reviewed on the Phase 7 branch.

Phase 7 extends the validated presentation boundary to the existing
`stabilization-v1` and `regional-affiliation-v1` campaigns. It adds a shared
campaign shell and campaign-specific views; it does not make their state or
decisions interchangeable.

## Typed campaign-coverage contract

`campaign-coverage-v1` is a non-mutating host envelope containing:

- session and campaign-role metadata;
- current stage, source-linked briefing, visible metrics, actors, and
  processes/obligations;
- host-shaped decisions with command templates, parameters, uncertainty, and
  source labels;
- committed transition summaries, replay count/hash metadata, and terminal
  campaign-specific debrief lines.

The contract is additive. Competitive `competitive-read-only-v1`, action,
resolution, audio, and regional-world contracts remain unchanged.

## Campaign distinctions

| Campaign | Product role | Visible focus | Not substituted by |
| --- | --- | --- | --- |
| Stabilization | onboarding-oriented executive loop | reported access/quality, cash/capacity, policy/market briefing, stage response | competitive map or monthly rival dashboard |
| Affiliation | institutional fit and obligation process | partner condition, posture, commitments, review, labor/payer/community responses, integration | universal affiliation score or market optimization |

## Browser behavior

The shared route renders stage, briefing, metrics, source labels, campaign actor
cards, processes/obligations, decisions, history, and debrief. Forms are created
from host parameter metadata and submit only the host-provided command template
with entered values. Rejections keep the current coverage view and explain the
next recovery step; successful submissions reload the host read.

Audio uses existing generated recipes and cues: visible pressure maps to
pressure music, completed sessions map to debrief music, and committed
affiliation-stage refreshes may record the affiliation milestone cue. Audio is
never required to understand or complete a campaign.

## Source and visibility boundary

Stabilization values derive from its established player observation and current
visible report. Affiliation values derive from `AffiliationObservation`, not
from true partner condition, resolved inputs, or future outcomes. History and
debrief reuse committed summaries and existing campaign-specific functions.

## Static review checklist

The host read is `get_campaign_coverage(session_id)` and remains non-mutating;
the canonical `submit_turn` path is used for decisions.

1. Load stabilization and confirm onboarding role, stage-specific fields,
   uncertainty, host command template, history, and debrief behavior.
2. Load affiliation and confirm partner/fit, commitments, review, stakeholder,
   integration, and obligation distinctions remain visible.
3. Submit a valid host-shaped decision and confirm the refreshed read/history.
4. Submit an invalid decision and confirm actionable error text plus unchanged
   current view/session.
5. Use keyboard navigation and reduced motion; confirm forms and written
   equivalents remain complete with audio unavailable or muted.
6. Confirm competitive regional-world/action/resolution behavior is unchanged.
7. Confirm no true state, resolved stochastic inputs, formulas, assets, or
   network calls appear in the browser or coverage DTO.

These checks are technical/interface-task evidence only. They do not establish
human comprehension, usability, lived accessibility, learning, engagement,
calibration, balance, domain validity, policy validity, or legal validity.

## Explicit non-goals and next gate

This phase does not add new commands or mechanics, a universal campaign model,
true-state/instructor views, asset-backed campaign identity, mobile redesign,
deployment, or human evaluation.

Phase 8 is the next candidate: AI-agent testplay readiness for onboarding,
settings/accessibility/error recovery, and structured interaction capture.
