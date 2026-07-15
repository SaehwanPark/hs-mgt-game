use super::session::TransitionSummary;
use crate::model::{ConsultantOption, HealthSystemState, PlayerObservation};

pub const PRESENTATION_SCHEMA_VERSION: &str = "competitive-read-only-v1";

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ReadOnlyPresentationEnvelope {
  pub schema_version: String,
  pub session: ReadOnlySession,
  pub resources: ReadOnlyResources,
  pub observation: ReadOnlyObservation,
  pub institutions: Vec<ReadOnlyInstitution>,
  pub pending_effects: Vec<ReadOnlyPendingEffect>,
  pub history: Vec<TransitionSummary>,
  pub latest_transition: Option<TransitionSummary>,
  pub replay: ReadOnlyReplayMetadata,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ReadOnlySession {
  pub session_id: String,
  pub campaign: String,
  pub seed: u64,
  pub difficulty: Option<String>,
  pub year: u32,
  pub month: u32,
  pub month_name: String,
  pub turn: u32,
  pub max_turns: u32,
  pub done: bool,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ReadOnlyResources {
  pub cash: i32,
  pub action_points: u32,
  pub political_capital: u32,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ReadOnlyObservation {
  pub organization_name: String,
  pub access_index: i32,
  pub prior_access_revision: Option<ReadOnlyRevision>,
  pub quality_index: i32,
  pub workforce_trust: String,
  pub community_trust: String,
  pub staffing: Vec<ReadOnlyMetric>,
  pub capacity: Vec<ReadOnlyMetric>,
  pub operations: ReadOnlyOperations,
  pub in_flight_projects: String,
  pub cash_runway_signal: String,
  pub market_bullets: Vec<String>,
  pub policy_bullets: Vec<String>,
  pub annual_policy_review: Option<Vec<String>>,
  pub consultant_options: Vec<ConsultantOption>,
  pub information_gaps: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ReadOnlyRevision {
  pub turn: u32,
  pub value: i32,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ReadOnlyMetric {
  pub label: String,
  pub value: i32,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ReadOnlyOperations {
  pub demand: i32,
  pub treated_volume: i32,
  pub unmet_demand: i32,
  pub revenue: i32,
  pub cost: i32,
  pub margin: i32,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ReadOnlyInstitution {
  pub id: String,
  pub name: String,
  pub role: String,
  pub facilities: Vec<ReadOnlyFacility>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ReadOnlyFacility {
  pub name: String,
  pub kind: String,
  pub metrics: Vec<ReadOnlyMetric>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ReadOnlyPendingEffect {
  pub label: String,
  pub detail: String,
  pub source: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ReadOnlyReplayMetadata {
  pub seed: u64,
  pub transition_count: usize,
  pub latest_state_hash: Option<String>,
}

pub(crate) fn from_competitive_observation(
  session: ReadOnlySession,
  player: &HealthSystemState,
  observation: &PlayerObservation,
  history: &[TransitionSummary],
) -> ReadOnlyPresentationEnvelope {
  let transitions = history.to_vec();
  let latest_transition = transitions.last().cloned();
  let latest_state_hash = latest_transition
    .as_ref()
    .map(|entry| entry.state_hash.clone());
  let pending_effects = pending_effects(observation);

  ReadOnlyPresentationEnvelope {
    schema_version: PRESENTATION_SCHEMA_VERSION.to_string(),
    replay: ReadOnlyReplayMetadata {
      seed: session.seed,
      transition_count: transitions.len(),
      latest_state_hash,
    },
    resources: ReadOnlyResources {
      cash: player.resources.cash,
      action_points: player.resources.ap_budget,
      political_capital: player.resources.political_capital,
    },
    institutions: vec![player_institution(player, observation)],
    observation: ReadOnlyObservation::from(observation),
    pending_effects,
    history: transitions,
    latest_transition,
    session,
  }
}

impl From<&PlayerObservation> for ReadOnlyObservation {
  fn from(observation: &PlayerObservation) -> Self {
    Self {
      organization_name: observation.org_name.clone(),
      access_index: observation.reported_access_index,
      prior_access_revision: observation
        .prior_access_revision
        .map(|(turn, value)| ReadOnlyRevision { turn, value }),
      quality_index: observation.reported_quality_index,
      workforce_trust: observation.workforce_trust_summary.clone(),
      community_trust: observation.community_trust_summary.clone(),
      staffing: vec![
        metric("Nurses", observation.nurses),
        metric("Physicians", observation.physicians),
        metric("Admins", observation.admins),
      ],
      capacity: vec![
        metric("Staffed beds", observation.staffed_beds),
        metric("Outpatient", observation.outpatient_capacity),
        metric("Emergency", observation.emergency_capacity),
        metric("ICU", observation.icu_capacity),
        metric("Obstetrics", observation.obstetrics_capacity),
        metric("Psychiatric", observation.psychiatric_capacity),
        metric("Cardiology", observation.cardiology_capacity),
        metric("Oncology", observation.oncology_capacity),
        metric("Infusion", observation.infusion_capacity),
        metric("Neurology", observation.neurology_capacity),
        metric("ASC", observation.asc_capacity),
      ],
      operations: ReadOnlyOperations {
        demand: observation.monthly_demand,
        treated_volume: observation.monthly_treated_volume,
        unmet_demand: observation.monthly_unmet_demand,
        revenue: observation.monthly_operating_revenue,
        cost: observation.monthly_operating_cost,
        margin: observation.monthly_operating_margin,
      },
      in_flight_projects: observation.in_flight_projects.clone(),
      cash_runway_signal: observation.cash_runway_signal.label().to_string(),
      market_bullets: observation.market_bullets.clone(),
      policy_bullets: observation.policy_bullets.clone(),
      annual_policy_review: observation.annual_policy_review.clone(),
      consultant_options: observation.consultant_options.clone(),
      information_gaps: observation.intel_gaps.clone(),
    }
  }
}

fn player_institution(
  player: &HealthSystemState,
  observation: &PlayerObservation,
) -> ReadOnlyInstitution {
  ReadOnlyInstitution {
    id: "player-system".to_string(),
    name: player.name.clone(),
    role: "Player system".to_string(),
    facilities: vec![ReadOnlyFacility {
      name: "Observed service capacity".to_string(),
      kind: "Player-visible capacity lines".to_string(),
      metrics: ReadOnlyObservation::from(observation).capacity,
    }],
  }
}

fn pending_effects(observation: &PlayerObservation) -> Vec<ReadOnlyPendingEffect> {
  let mut effects = Vec::new();
  if !observation.in_flight_projects.is_empty()
    && observation.in_flight_projects != "none"
    && observation.in_flight_projects != "None"
  {
    effects.push(ReadOnlyPendingEffect {
      label: "In-flight projects".to_string(),
      detail: observation.in_flight_projects.clone(),
      source: "PlayerObservation.in_flight_projects".to_string(),
    });
  }
  if let Some(review) = &observation.annual_policy_review {
    effects.push(ReadOnlyPendingEffect {
      label: "Annual policy review".to_string(),
      detail: review.join("; "),
      source: "PlayerObservation.annual_policy_review".to_string(),
    });
  }
  effects
}

fn metric(label: &str, value: i32) -> ReadOnlyMetric {
  ReadOnlyMetric {
    label: label.to_string(),
    value,
  }
}
