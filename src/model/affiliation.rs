use super::{AttributedEffect, Event};

pub const AFFILIATION_TURN_COUNT: u32 = 6;
pub const AFFILIATION_RULESET_VERSION: &str = "regional-affiliation-ruleset-0.1.0";
pub const AFFILIATION_STATE_HASH_SCHEMA_VERSION: &str = "regional-affiliation-state-hash-v1";
pub const AFFILIATION_REPLAY_ARTIFACT_VERSION: &str = "regional-affiliation-replay-v1";

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum AffiliationStage {
  AssessPartner,
  ChoosePosture,
  NegotiateCommitments,
  SubmitReview,
  ResolveReview,
  IntegrateOrDecline,
  Complete,
}

impl AffiliationStage {
  pub fn next(self) -> Self {
    match self {
      Self::AssessPartner => Self::ChoosePosture,
      Self::ChoosePosture => Self::NegotiateCommitments,
      Self::NegotiateCommitments => Self::SubmitReview,
      Self::SubmitReview => Self::ResolveReview,
      Self::ResolveReview => Self::IntegrateOrDecline,
      Self::IntegrateOrDecline | Self::Complete => Self::Complete,
    }
  }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum AffiliationStatus {
  Unassessed,
  Independent,
  Deferred,
  Pursuing,
  PartnerAccepted,
  PartnerConditioned,
  PartnerRejected,
  ReviewPending,
  Approved,
  ConditionallyApproved,
  ReviewDelayed,
  ReviewRejected,
  Integrated,
  IntegrationDeclined,
}

impl AffiliationStatus {
  pub fn is_terminal(self) -> bool {
    matches!(
      self,
      Self::PartnerRejected
        | Self::ReviewDelayed
        | Self::ReviewRejected
        | Self::Integrated
        | Self::IntegrationDeclined
    )
  }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum AffiliationPosture {
  Independent,
  Deferred,
  Pursue,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum PartnerConditionBand {
  Fragile,
  Stable,
  Strong,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum PartnerResponse {
  Accepted,
  Conditioned,
  Rejected,
  NotEngaged,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum ReviewResponse {
  Approved,
  Conditional,
  Delayed,
  Rejected,
  NotEngaged,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum LaborResponse {
  Support,
  Concern,
  Opposition,
  Disruption,
  NotEngaged,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum PayerResponse {
  Support,
  Neutral,
  Leverage,
  Retrenchment,
  NotEngaged,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum CommunityResponse {
  Support,
  Conditional,
  Opposition,
  NotEngaged,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum IntegrationDecision {
  Begin,
  Decline,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum AffiliationCommand {
  AssessPartner,
  ChoosePosture {
    posture: AffiliationPosture,
  },
  SetCommitments {
    community: i32,
    workforce: i32,
    continuity: i32,
  },
  SubmitReview,
  AwaitReview,
  ChooseIntegration {
    decision: IntegrationDecision,
  },
  Hold,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AffiliationRuleset {
  pub version: String,
  pub starting_cash: i32,
  pub assessment_cash_cost: i32,
  pub review_submission_cash_cost: i32,
  pub integration_start_cash_cost: i32,
  pub min_commitment: i32,
  pub max_commitment: i32,
  pub max_total_commitment: i32,
}

pub fn default_affiliation_ruleset() -> AffiliationRuleset {
  AffiliationRuleset {
    version: AFFILIATION_RULESET_VERSION.to_string(),
    starting_cash: 60,
    assessment_cash_cost: 2,
    review_submission_cash_cost: 6,
    integration_start_cash_cost: 8,
    min_commitment: 1,
    max_commitment: 8,
    max_total_commitment: 18,
  }
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AffiliationRiversideState {
  pub name: String,
  pub cash: i32,
  pub access_index: i32,
  pub quality_index: i32,
  pub workforce_trust: i32,
  pub community_trust: i32,
  pub market_share_index: i32,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AffiliationPartnerState {
  pub name: String,
  pub condition_index: i32,
  pub fit_index: i32,
  pub autonomy_need: i32,
  pub continuity_risk: i32,
  pub reported_condition: Option<PartnerConditionBand>,
}

#[derive(Clone, Debug, Default, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AffiliationCommitments {
  pub community: i32,
  pub workforce: i32,
  pub continuity: i32,
}

impl AffiliationCommitments {
  pub fn total(&self) -> i32 {
    self.community + self.workforce + self.continuity
  }
}

#[derive(Clone, Debug, Default, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AffiliationReviewState {
  pub response: Option<ReviewResponse>,
  pub conditions: i32,
}

#[derive(Clone, Debug, Default, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AffiliationIntegrationState {
  pub progress: i32,
  pub drag_applied: i32,
  pub continuity_shock_applied: i32,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AffiliationWorldState {
  pub scenario_id: String,
  pub turn: u32,
  pub stage: AffiliationStage,
  pub status: AffiliationStatus,
  pub riverside: AffiliationRiversideState,
  pub partner: AffiliationPartnerState,
  pub commitments: AffiliationCommitments,
  pub review: AffiliationReviewState,
  pub integration: AffiliationIntegrationState,
  pub partner_response: PartnerResponse,
  pub labor_response: LaborResponse,
  pub payer_response: PayerResponse,
  pub community_response: CommunityResponse,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AffiliationObservation {
  pub turn: u32,
  pub stage: AffiliationStage,
  pub status: AffiliationStatus,
  pub riverside_name: String,
  pub cash: i32,
  pub access_index: i32,
  pub quality_index: i32,
  pub workforce_trust: i32,
  pub community_trust: i32,
  pub market_share_index: i32,
  pub partner_name: String,
  pub reported_condition: Option<PartnerConditionBand>,
  pub commitments: AffiliationCommitments,
  pub review_response: Option<ReviewResponse>,
  pub labor_response: LaborResponse,
  pub payer_response: PayerResponse,
  pub community_response: CommunityResponse,
  pub alternatives: Vec<String>,
  pub assumptions: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AffiliationResolvedInputs {
  pub partner_report_noise: i32,
  pub partner_response: PartnerResponse,
  pub review_response: ReviewResponse,
  pub labor_response: LaborResponse,
  pub payer_response: PayerResponse,
  pub community_response: CommunityResponse,
  pub integration_drag: i32,
  pub continuity_shock: i32,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AffiliationActorDecision {
  pub actor: String,
  pub outcome: String,
  pub rationale: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AffiliationTransition {
  pub prior: AffiliationWorldState,
  pub command: AffiliationCommand,
  pub observation: AffiliationObservation,
  pub resolved_inputs: AffiliationResolvedInputs,
  pub actor_decisions: Vec<AffiliationActorDecision>,
  pub events: Vec<Event>,
  pub effects: Vec<AttributedEffect>,
  pub next: AffiliationWorldState,
  pub state_hash: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AffiliationHistory {
  pub genesis: AffiliationWorldState,
  pub transitions: Vec<AffiliationTransition>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AffiliationReplayArtifact {
  pub artifact_version: String,
  pub seed: u64,
  pub ruleset_version: String,
  pub history: AffiliationHistory,
}

impl AffiliationHistory {
  pub fn final_state(&self) -> &AffiliationWorldState {
    self
      .transitions
      .last()
      .map(|transition| &transition.next)
      .unwrap_or(&self.genesis)
  }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum AffiliationValidationError {
  WrongStage {
    expected: AffiliationStage,
    actual: AffiliationStage,
  },
  InvalidCommandForStatus,
  CommitmentOutOfRange {
    value: i32,
    min: i32,
    max: i32,
  },
  TotalCommitmentExceeded {
    total: i32,
    max: i32,
  },
  InsufficientCash {
    required: i32,
    available: i32,
  },
  TerminalState,
  ReplayStateMismatch,
  ObservationMismatch,
  StateHashMismatch {
    turn: u32,
    expected: String,
    actual: String,
  },
}

impl AffiliationValidationError {
  pub fn message(&self) -> String {
    match self {
      Self::WrongStage { expected, actual } => {
        format!("command belongs to stage {expected:?}, current stage is {actual:?}")
      }
      Self::InvalidCommandForStatus => {
        "command is not valid for the current affiliation status".to_string()
      }
      Self::CommitmentOutOfRange { value, min, max } => {
        format!("commitment {value} outside range {min}..{max}")
      }
      Self::TotalCommitmentExceeded { total, max } => {
        format!("total commitments {total} exceed maximum {max}")
      }
      Self::InsufficientCash {
        required,
        available,
      } => {
        format!("cash required {required} exceeds available {available}")
      }
      Self::TerminalState => "affiliation scenario is already complete".to_string(),
      Self::ReplayStateMismatch => {
        "affiliation replay prior state does not match history".to_string()
      }
      Self::ObservationMismatch => {
        "affiliation replay observation does not match the decision-time state".to_string()
      }
      Self::StateHashMismatch {
        turn,
        expected,
        actual,
      } => {
        format!("affiliation state hash mismatch at turn {turn}: expected {expected}, got {actual}")
      }
    }
  }
}
