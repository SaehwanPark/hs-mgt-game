use super::{AffiliationRuleset, AffiliationWorldState, stable_hash_hex};

pub fn affiliation_state_hash_record(
  state: &AffiliationWorldState,
  ruleset: &AffiliationRuleset,
) -> String {
  format!(
    "{}|ruleset={}|scenario={}|turn={}|stage={:?}|status={:?}|cash={}|access={}|quality={}|workforce={}|community={}|share={}|partner_condition={}|partner_fit={}|autonomy={}|continuity_risk={}|reported={:?}|commitments={},{},{}|review={:?}|conditions={}|integration={},{},{}|responses={:?},{:?},{:?},{:?}",
    super::AFFILIATION_STATE_HASH_SCHEMA_VERSION,
    ruleset.version,
    state.scenario_id,
    state.turn,
    state.stage,
    state.status,
    state.riverside.cash,
    state.riverside.access_index,
    state.riverside.quality_index,
    state.riverside.workforce_trust,
    state.riverside.community_trust,
    state.riverside.market_share_index,
    state.partner.condition_index,
    state.partner.fit_index,
    state.partner.autonomy_need,
    state.partner.continuity_risk,
    state.partner.reported_condition,
    state.commitments.community,
    state.commitments.workforce,
    state.commitments.continuity,
    state.review.response,
    state.review.conditions,
    state.integration.progress,
    state.integration.drag_applied,
    state.integration.continuity_shock_applied,
    state.partner_response,
    state.labor_response,
    state.payer_response,
    state.community_response,
  )
}

pub fn hash_affiliation_state(
  state: &AffiliationWorldState,
  ruleset: &AffiliationRuleset,
) -> String {
  stable_hash_hex(&affiliation_state_hash_record(state, ruleset))
}
