use crate::model::{
  AffiliationCommand, AffiliationResolvedInputs, AffiliationStatus, AffiliationWorldState,
  CommunityResponse, LaborResponse, PartnerResponse, PayerResponse, ReviewResponse,
};

use super::rng::{bounded_i32, stream_rng};
use super::streams::{
  STREAM_AFFILIATION_COMMUNITY, STREAM_AFFILIATION_CONTINUITY, STREAM_AFFILIATION_DRAG,
  STREAM_AFFILIATION_LABOR, STREAM_AFFILIATION_PARTNER, STREAM_AFFILIATION_PAYER,
  STREAM_AFFILIATION_REPORT, STREAM_AFFILIATION_REVIEW,
};

pub fn resolve_affiliation_inputs(
  seed: u64,
  prior: &AffiliationWorldState,
  command: &AffiliationCommand,
) -> AffiliationResolvedInputs {
  let turn = prior.turn;
  let report_noise = bounded_i32(stream_rng(seed, turn, STREAM_AFFILIATION_REPORT), -8, 8);
  let mut inputs = AffiliationResolvedInputs {
    partner_report_noise: report_noise,
    partner_response: PartnerResponse::NotEngaged,
    review_response: ReviewResponse::NotEngaged,
    labor_response: LaborResponse::NotEngaged,
    payer_response: PayerResponse::NotEngaged,
    community_response: CommunityResponse::NotEngaged,
    integration_drag: bounded_i32(stream_rng(seed, turn, STREAM_AFFILIATION_DRAG), 0, 8),
    continuity_shock: bounded_i32(stream_rng(seed, turn, STREAM_AFFILIATION_CONTINUITY), 0, 6),
  };

  match command {
    AffiliationCommand::SetCommitments {
      community,
      workforce,
      continuity,
    } if matches!(prior.status, AffiliationStatus::Pursuing) => {
      let total = community + workforce + continuity;
      let package_strength = total * 100 / 18;
      let draw = bounded_i32(stream_rng(seed, turn, STREAM_AFFILIATION_PARTNER), -10, 10);
      let score =
        (prior.partner.fit_index + prior.partner.condition_index + package_strength) / 3 + draw;
      inputs.partner_response = if score >= 70 {
        PartnerResponse::Accepted
      } else if score >= 55 {
        PartnerResponse::Conditioned
      } else {
        PartnerResponse::Rejected
      };
    }
    AffiliationCommand::AwaitReview if prior.status == AffiliationStatus::ReviewPending => {
      let total = prior.commitments.total();
      let package_strength = total * 100 / 18;
      let commitment_strength =
        (prior.commitments.community + prior.commitments.workforce + prior.commitments.continuity)
          * 100
          / 24;
      let review_draw = bounded_i32(stream_rng(seed, turn, STREAM_AFFILIATION_REVIEW), -10, 10);
      let review_score =
        (prior.partner.fit_index + package_strength + commitment_strength) / 3 + review_draw;
      inputs.review_response = if review_score >= 72 {
        ReviewResponse::Approved
      } else if review_score >= 58 {
        ReviewResponse::Conditional
      } else if review_score >= 45 {
        ReviewResponse::Delayed
      } else {
        ReviewResponse::Rejected
      };

      let labor_score = prior.commitments.workforce * 10
        + bounded_i32(stream_rng(seed, turn, STREAM_AFFILIATION_LABOR), -10, 10);
      inputs.labor_response = if labor_score >= 60 {
        LaborResponse::Support
      } else if labor_score >= 35 {
        LaborResponse::Concern
      } else if labor_score >= 15 {
        LaborResponse::Opposition
      } else {
        LaborResponse::Disruption
      };

      let payer_score = prior.commitments.continuity * 10
        + prior.commitments.community * 5
        + bounded_i32(stream_rng(seed, turn, STREAM_AFFILIATION_PAYER), -10, 10);
      inputs.payer_response = if payer_score >= 75 {
        PayerResponse::Support
      } else if payer_score >= 45 {
        PayerResponse::Neutral
      } else if payer_score >= 25 {
        PayerResponse::Leverage
      } else {
        PayerResponse::Retrenchment
      };

      let community_score = prior.commitments.community * 10
        + prior.commitments.continuity * 5
        + bounded_i32(
          stream_rng(seed, turn, STREAM_AFFILIATION_COMMUNITY),
          -10,
          10,
        );
      inputs.community_response = if community_score >= 70 {
        CommunityResponse::Support
      } else if community_score >= 40 {
        CommunityResponse::Conditional
      } else {
        CommunityResponse::Opposition
      };
    }
    _ => {}
  }

  inputs
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::model::{AffiliationCommand, AffiliationPosture};
  use crate::scenario::default_regional_affiliation_scenario;

  #[test]
  fn affiliation_inputs_are_deterministic() {
    let state = default_regional_affiliation_scenario()
      .unwrap()
      .initial_affiliation_world_state()
      .unwrap();
    let command = AffiliationCommand::ChoosePosture {
      posture: AffiliationPosture::Pursue,
    };
    assert_eq!(
      resolve_affiliation_inputs(42, &state, &command),
      resolve_affiliation_inputs(42, &state, &command)
    );
  }
}
