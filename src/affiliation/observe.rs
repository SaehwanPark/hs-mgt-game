use crate::model::{
  AffiliationObservation, AffiliationStage, AffiliationWorldState, CommunityResponse,
  LaborResponse, PayerResponse,
};

pub fn observe_affiliation(state: &AffiliationWorldState) -> AffiliationObservation {
  let mut alternatives = vec![
    "Remain independent: preserve cash and autonomy without affiliation effects".to_string(),
    "Defer: preserve the option while accepting no immediate affiliation benefit".to_string(),
  ];
  if matches!(state.stage, AffiliationStage::ChoosePosture) {
    alternatives
      .push("Pursue: spend resources for possible continuity and regional leverage".to_string());
  }

  AffiliationObservation {
    turn: state.turn + 1,
    stage: state.stage,
    status: state.status,
    riverside_name: state.riverside.name.clone(),
    cash: state.riverside.cash,
    access_index: state.riverside.access_index,
    quality_index: state.riverside.quality_index,
    workforce_trust: state.riverside.workforce_trust,
    community_trust: state.riverside.community_trust,
    market_share_index: state.riverside.market_share_index,
    partner_name: state.partner.name.clone(),
    reported_condition: state.partner.reported_condition,
    commitments: state.commitments.clone(),
    review_response: state.review.response,
    labor_response: state.labor_response,
    payer_response: state.payer_response,
    community_response: state.community_response,
    alternatives,
    assumptions: vec![
      "Partner condition and institutional review are stylized game inputs, not legal forecasts."
        .to_string(),
      "Community, labor, payer, and integration responses are outside Riverside authority."
        .to_string(),
    ],
  }
}

#[allow(dead_code)]
fn _response_labels(_labor: LaborResponse, _payer: PayerResponse, _community: CommunityResponse) {}
