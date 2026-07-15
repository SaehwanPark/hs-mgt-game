use crate::affiliation::observe_affiliation;
use crate::debrief::{affiliation_debrief, educational_debrief};
use crate::inputs::resolve_inputs;
use crate::model::{
  AffiliationObservation, AffiliationRuleset, AffiliationStage, AffiliationWorldState, History,
  Observation, Ruleset, WorldState,
};
use crate::sim::observe_for_player;

use super::session::{TransitionSummary, affiliation_legal_commands, stabilization_legal_commands};

pub const CAMPAIGN_COVERAGE_SCHEMA_VERSION: &str = "campaign-coverage-v1";

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct CampaignCoverageEnvelope {
  pub schema_version: String,
  pub session: CampaignCoverageSession,
  pub campaign_role: String,
  pub stage: CampaignCoverageStage,
  pub briefing: Vec<CampaignCoverageBriefing>,
  pub metrics: Vec<CampaignCoverageMetric>,
  pub actors: Vec<CampaignCoverageActor>,
  pub processes: Vec<CampaignCoverageProcess>,
  pub decisions: Vec<CampaignCoverageDecision>,
  pub history: Vec<TransitionSummary>,
  pub debrief: Vec<String>,
  pub replay: CampaignCoverageReplayMetadata,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct CampaignCoverageSession {
  pub session_id: String,
  pub campaign: String,
  pub seed: u64,
  pub turn: u32,
  pub max_turns: u32,
  pub done: bool,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct CampaignCoverageStage {
  pub id: String,
  pub label: String,
  pub detail: String,
  pub source: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct CampaignCoverageBriefing {
  pub kind: String,
  pub title: String,
  pub detail: String,
  pub source: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct CampaignCoverageMetric {
  pub label: String,
  pub value: String,
  pub unit: String,
  pub source: String,
  pub equivalent: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct CampaignCoverageActor {
  pub id: String,
  pub label: String,
  pub role: String,
  pub status: String,
  pub detail: String,
  pub source: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct CampaignCoverageProcess {
  pub id: String,
  pub label: String,
  pub detail: String,
  pub status: String,
  pub source: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct CampaignCoverageDecision {
  pub id: String,
  pub label: String,
  pub command_template: String,
  pub uncertainty: String,
  pub source: String,
  pub parameters: Vec<CampaignCoverageParameter>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct CampaignCoverageParameter {
  pub name: String,
  pub label: String,
  pub input_type: String,
  pub options: Vec<CampaignCoverageOption>,
  pub min: Option<i32>,
  pub max: Option<i32>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct CampaignCoverageOption {
  pub label: String,
  pub value: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct CampaignCoverageReplayMetadata {
  pub transition_count: usize,
  pub state_hash: Option<String>,
}

pub(crate) fn from_stabilization(
  session_id: String,
  seed: u64,
  done: bool,
  state: &WorldState,
  ruleset: &Ruleset,
  history: &[TransitionSummary],
  typed_history: &History,
) -> CampaignCoverageEnvelope {
  let observation = if done {
    typed_history
      .transitions
      .last()
      .map(|transition| transition.observation.clone())
      .unwrap_or(Observation {
        actor: "health_system_ceo",
        reported_access_index: state.access_index,
        reported_quality_index: state.quality_index,
        prior_access_revision: 0,
        policy_briefing: "stabilization session complete",
        market_competition_briefing: "",
      })
  } else {
    let resolved_inputs = resolve_inputs(seed, state, ruleset);
    observe_for_player(state, &resolved_inputs)
  };
  let turn = if done { state.turn } else { state.turn + 1 };
  let decisions = stabilization_decisions(turn, ruleset);
  let latest_hash = history.last().map(|entry| entry.state_hash.clone());
  let mut briefings = vec![briefing(
    "policy",
    "Policy signal",
    observation.policy_briefing,
    "Stabilization player observation",
  )];
  if !observation.market_competition_briefing.is_empty() {
    briefings.push(briefing(
      "market",
      "Market signal",
      observation.market_competition_briefing,
      "Stabilization player observation",
    ));
  }
  if observation.prior_access_revision != 0 {
    briefings.push(briefing(
      "revision",
      "Reported access revision",
      &observation.prior_access_revision.to_string(),
      "Stabilization player observation",
    ));
  }

  CampaignCoverageEnvelope {
    schema_version: CAMPAIGN_COVERAGE_SCHEMA_VERSION.to_string(),
    session: CampaignCoverageSession {
      session_id,
      campaign: "stabilization-v1".to_string(),
      seed,
      turn,
      max_turns: crate::model::INTERACTIVE_TURN_COUNT,
      done,
    },
    campaign_role: "tutorial-oriented stabilization".to_string(),
    stage: CampaignCoverageStage {
      id: format!("turn-{turn}"),
      label: if done {
        "Stabilization complete".to_string()
      } else {
        format!("Stabilization turn {turn}")
      },
      detail: if done {
        "Review the committed tradeoffs in the educational debrief.".to_string()
      } else {
        "Choose the response for this stage; future outcomes remain uncertain.".to_string()
      },
      source: "Stabilization session stage".to_string(),
    },
    briefing: briefings,
    metrics: vec![
      metric(
        "Cash",
        state.cash,
        "game units",
        "Stabilization visible report",
        "Current resource",
      ),
      metric(
        "Staffed beds",
        state.staffed_beds,
        "beds",
        "Stabilization visible report",
        "Current capacity",
      ),
      metric(
        "Reported access",
        observation.reported_access_index,
        "index",
        "Stabilization player observation",
        "Reported access measure",
      ),
      metric(
        "Reported quality",
        observation.reported_quality_index,
        "index",
        "Stabilization player observation",
        "Reported quality measure",
      ),
    ],
    actors: vec![actor(
      "health-system-executive",
      "Health system executive",
      "Player decision-maker",
      "observing",
      "Allocates visible resources and commitments while other institutions respond.",
      "Stabilization campaign role",
    )],
    processes: vec![process(
      "stabilization-stage",
      "Stage response",
      if done {
        "No further stage response is available.".to_string()
      } else {
        "One host-defined response is available for this stabilization turn.".to_string()
      },
      if done { "complete" } else { "active" },
      "Stabilization stage and legal command surface",
    )],
    decisions,
    history: history.to_vec(),
    debrief: if done {
      educational_debrief(typed_history)
    } else {
      Vec::new()
    },
    replay: CampaignCoverageReplayMetadata {
      transition_count: history.len(),
      state_hash: latest_hash,
    },
  }
}

pub(crate) fn from_affiliation(
  session_id: String,
  seed: u64,
  done: bool,
  state: &AffiliationWorldState,
  ruleset: &AffiliationRuleset,
  history: &[TransitionSummary],
  typed_history: &crate::model::AffiliationHistory,
) -> CampaignCoverageEnvelope {
  let observation = observe_affiliation(state);
  let latest_hash = history.last().map(|entry| entry.state_hash.clone());
  let condition = observation
    .reported_condition
    .map(|value| format!("{value:?}"))
    .unwrap_or_else(|| "Not yet assessed".to_string());
  let mut briefings = vec![
    briefing(
      "partner",
      "Partner condition",
      &format!("{} · {condition}", observation.partner_name),
      "AffiliationObservation.partner_name/reported_condition",
    ),
    briefing(
      "status",
      "Affiliation status",
      &format!("{:?}", observation.status),
      "AffiliationObservation.status",
    ),
  ];
  briefings.extend(observation.assumptions.iter().map(|assumption| {
    briefing(
      "assumption",
      "Scenario assumption",
      assumption,
      "AffiliationObservation.assumptions",
    )
  }));

  let decisions = affiliation_decisions(state, ruleset);
  CampaignCoverageEnvelope {
    schema_version: CAMPAIGN_COVERAGE_SCHEMA_VERSION.to_string(),
    session: CampaignCoverageSession {
      session_id,
      campaign: "regional-affiliation-v1".to_string(),
      seed,
      turn: if done { state.turn } else { state.turn + 1 },
      max_turns: crate::model::AFFILIATION_TURN_COUNT,
      done,
    },
    campaign_role: "institutional fit and obligation process".to_string(),
    stage: CampaignCoverageStage {
      id: format!("{:?}", observation.stage).to_ascii_lowercase(),
      label: affiliation_stage_label(observation.stage).to_string(),
      detail: if done {
        "Review the partner, stakeholder, and integration tradeoffs in the debrief.".to_string()
      } else {
        "The current stage exposes a bounded institutional decision; later responses remain uncertain.".to_string()
      },
      source: "AffiliationObservation.stage".to_string(),
    },
    briefing: briefings,
    metrics: vec![
      metric(
        "Riverside cash",
        observation.cash,
        "game units",
        "AffiliationObservation.cash",
        "Current resource",
      ),
      metric(
        "Access",
        observation.access_index,
        "index",
        "AffiliationObservation.access_index",
        "Visible Riverside outcome",
      ),
      metric(
        "Quality",
        observation.quality_index,
        "index",
        "AffiliationObservation.quality_index",
        "Visible Riverside outcome",
      ),
      metric(
        "Workforce trust",
        observation.workforce_trust,
        "index",
        "AffiliationObservation.workforce_trust",
        "Visible workforce relationship",
      ),
      metric(
        "Community trust",
        observation.community_trust,
        "index",
        "AffiliationObservation.community_trust",
        "Visible community relationship",
      ),
      metric(
        "Market share",
        observation.market_share_index,
        "index",
        "AffiliationObservation.market_share_index",
        "Visible market position",
      ),
      metric(
        "Community commitment",
        observation.commitments.community,
        "commitment units",
        "AffiliationObservation.commitments",
        "Visible obligation",
      ),
      metric(
        "Workforce commitment",
        observation.commitments.workforce,
        "commitment units",
        "AffiliationObservation.commitments",
        "Visible obligation",
      ),
      metric(
        "Continuity commitment",
        observation.commitments.continuity,
        "commitment units",
        "AffiliationObservation.commitments",
        "Visible obligation",
      ),
    ],
    actors: vec![
      actor(
        "riverside",
        &observation.riverside_name,
        "Player institution",
        &format!("{:?}", observation.status),
        "Sets posture, commitments, review choices, and integration decision.",
        "AffiliationObservation Riverside fields",
      ),
      actor(
        "partner",
        &observation.partner_name,
        "Potential partner",
        &condition,
        "Partner condition is reported only when the campaign stage makes it visible.",
        "AffiliationObservation.partner_name/reported_condition",
      ),
      actor(
        "labor",
        "Labor response",
        "Stakeholder",
        &format!("{:?}", observation.labor_response),
        "Labor response is separate from Riverside workforce trust.",
        "AffiliationObservation.labor_response",
      ),
      actor(
        "payer",
        "Payer response",
        "Stakeholder",
        &format!("{:?}", observation.payer_response),
        "Payer response is separate from Riverside market share.",
        "AffiliationObservation.payer_response",
      ),
      actor(
        "community",
        "Community response",
        "Stakeholder",
        &format!("{:?}", observation.community_response),
        "Community response is separate from Riverside community trust.",
        "AffiliationObservation.community_response",
      ),
    ],
    processes: affiliation_processes(&observation),
    decisions,
    history: history.to_vec(),
    debrief: if done {
      affiliation_debrief(typed_history)
    } else {
      Vec::new()
    },
    replay: CampaignCoverageReplayMetadata {
      transition_count: history.len(),
      state_hash: latest_hash,
    },
  }
}

fn stabilization_decisions(turn: u32, ruleset: &Ruleset) -> Vec<CampaignCoverageDecision> {
  let command = stabilization_legal_commands(turn)
    .into_iter()
    .next()
    .unwrap_or_default();
  let command_template = match command.as_str() {
    "staffed_beds capital_spend requested_rate" => {
      "{{staffed_beds}} {{capital_spend}} {{requested_rate}}"
    }
    "advocacy_spend access_commitment" => "{{advocacy_spend}} {{access_commitment}}",
    "retention_spend schedule_relief" => "{{retention_spend}} {{schedule_relief}}",
    "coalition_investment shared_access_commitment" => "{{coalition_investment}} {{shared_access}}",
    "defensive_capital access_posture" => "{{defensive_capital}} {{access_posture}}",
    _ => return Vec::new(),
  };
  let (id, label, uncertainty, parameters) = match turn {
    1 => (
      "stabilize-access",
      "Stabilize access and capacity",
      "Insurer, policy, labor, and operating responses remain uncertain.",
      vec![
        number_parameter("staffed_beds", "Add staffed beds", Some(1), None),
        number_parameter(
          "capital_spend",
          "Capital spend",
          Some(0),
          Some(ruleset.max_capital_spend),
        ),
        number_parameter("requested_rate", "Requested commercial rate", None, None),
      ],
    ),
    2 => (
      "respond-to-policy",
      "Respond to state access mandate",
      "State policy may grant flexibility, impose friction, or change pressure.",
      vec![
        number_parameter(
          "advocacy_spend",
          "Advocacy spend",
          Some(0),
          Some(ruleset.max_advocacy_spend),
        ),
        number_parameter("access_commitment", "Access commitment", Some(1), None),
      ],
    ),
    3 => (
      "respond-to-workforce",
      "Respond to workforce pressure",
      "Workforce and operating responses may remain unfavorable despite a valid commitment.",
      vec![
        number_parameter(
          "retention_spend",
          "Retention spend",
          Some(0),
          Some(ruleset.max_retention_spend),
        ),
        number_parameter(
          "schedule_relief",
          "Schedule-relief commitment",
          Some(1),
          Some(ruleset.max_schedule_relief_commitment),
        ),
      ],
    ),
    4 => (
      "join-access-coalition",
      "Join regional access coalition",
      "Coalition partners may provide limited support or withdraw despite a valid commitment.",
      vec![
        number_parameter(
          "coalition_investment",
          "Coalition investment",
          Some(0),
          Some(ruleset.max_coalition_investment),
        ),
        number_parameter(
          "shared_access",
          "Shared-access commitment",
          Some(1),
          Some(ruleset.max_shared_access_commitment),
        ),
      ],
    ),
    5 => (
      "respond-to-competitor",
      "Respond to competitor capacity move",
      "Rival capacity and community responses remain uncertain.",
      vec![
        number_parameter(
          "defensive_capital",
          "Defensive capital commitment",
          Some(0),
          Some(ruleset.max_defensive_capital_commitment),
        ),
        number_parameter(
          "access_posture",
          "Access posture",
          Some(1),
          Some(ruleset.max_access_posture),
        ),
      ],
    ),
    _ => return Vec::new(),
  };
  vec![decision(
    id,
    label,
    command_template.to_string(),
    uncertainty,
    "Stabilization legal command surface",
    parameters,
  )]
}

fn affiliation_decisions(
  state: &AffiliationWorldState,
  ruleset: &AffiliationRuleset,
) -> Vec<CampaignCoverageDecision> {
  let command = affiliation_legal_commands(state)
    .into_iter()
    .next()
    .unwrap_or_default();
  let (id, label, uncertainty, parameters) = match command.as_str() {
    "assess" => (
      "assess-partner",
      "Assess partner condition",
      "The report is bounded and noisy; it is not a true partner forecast.",
      Vec::new(),
    ),
    "posture choice=independent|defer|pursue" => (
      "choose-posture",
      "Choose affiliation posture",
      "Independence, deferral, and pursuit preserve different outside options.",
      vec![select_parameter(
        "posture",
        "Posture",
        vec![
          option("Independent", "independent"),
          option("Defer", "defer"),
          option("Pursue", "pursue"),
        ],
      )],
    ),
    "commit community=1..8 workforce=1..8 continuity=1..8" => (
      "set-commitments",
      "Set affiliation commitments",
      "Partner fit and stakeholder responses remain uncertain after commitment.",
      vec![
        number_parameter(
          "community",
          "Community commitment",
          Some(ruleset.min_commitment),
          Some(ruleset.max_commitment),
        ),
        number_parameter(
          "workforce",
          "Workforce commitment",
          Some(ruleset.min_commitment),
          Some(ruleset.max_commitment),
        ),
        number_parameter(
          "continuity",
          "Continuity commitment",
          Some(ruleset.min_commitment),
          Some(ruleset.max_commitment),
        ),
      ],
    ),
    "submit_review" => (
      "submit-review",
      "Submit institutional review",
      "Review may approve, condition, delay, or reject the proposal.",
      Vec::new(),
    ),
    "await_review" => (
      "await-review",
      "Await institutional review",
      "Review timing and response remain outside Riverside authority.",
      Vec::new(),
    ),
    "integrate decision=begin|decline" => (
      "choose-integration",
      "Choose integration or decline",
      "Integration creates obligations and drag; decline preserves a different path.",
      vec![select_parameter(
        "decision",
        "Integration decision",
        vec![
          option("Begin integration", "begin"),
          option("Decline", "decline"),
        ],
      )],
    ),
    "hold" => (
      "hold-stage",
      "Hold at current stage",
      "Holding preserves the current state while the stage advances according to campaign rules.",
      Vec::new(),
    ),
    _ => return Vec::new(),
  };
  let command_template = match command.as_str() {
    "assess" => "assess",
    "posture choice=independent|defer|pursue" => "posture choice={{posture}}",
    "commit community=1..8 workforce=1..8 continuity=1..8" => {
      "commit community={{community}} workforce={{workforce}} continuity={{continuity}}"
    }
    "submit_review" => "submit_review",
    "await_review" => "await_review",
    "integrate decision=begin|decline" => "integrate decision={{decision}}",
    "hold" => "hold",
    _ => return Vec::new(),
  };
  vec![decision(
    id,
    label,
    command_template.to_string(),
    uncertainty,
    "Affiliation legal command surface",
    parameters,
  )]
}

fn affiliation_processes(observation: &AffiliationObservation) -> Vec<CampaignCoverageProcess> {
  let mut processes = vec![process(
    "affiliation-stage",
    "Institutional stage",
    affiliation_stage_label(observation.stage),
    if observation.stage == AffiliationStage::Complete {
      "complete"
    } else {
      "active"
    },
    "AffiliationObservation.stage",
  )];
  if matches!(
    observation.stage,
    AffiliationStage::SubmitReview | AffiliationStage::ResolveReview
  ) {
    processes.push(process(
      "institutional-review",
      "Institutional review",
      "Review timing and response are visible as a process, not a guaranteed outcome.",
      "pending",
      "Affiliation stage and review response observation",
    ));
  }
  if matches!(
    observation.stage,
    AffiliationStage::IntegrateOrDecline | AffiliationStage::Complete
  ) {
    processes.push(process(
      "integration-obligation",
      "Integration obligation",
      "Review the visible commitments and stakeholder responses before choosing integration or decline.",
      "visible",
      "AffiliationObservation.commitments and stakeholder responses",
    ));
  }
  processes
}

fn affiliation_stage_label(stage: AffiliationStage) -> &'static str {
  match stage {
    AffiliationStage::AssessPartner => "Assess partner",
    AffiliationStage::ChoosePosture => "Choose posture",
    AffiliationStage::NegotiateCommitments => "Negotiate commitments",
    AffiliationStage::SubmitReview => "Submit review",
    AffiliationStage::ResolveReview => "Resolve review",
    AffiliationStage::IntegrateOrDecline => "Integrate or decline",
    AffiliationStage::Complete => "Affiliation complete",
  }
}

fn briefing(kind: &str, title: &str, detail: &str, source: &str) -> CampaignCoverageBriefing {
  CampaignCoverageBriefing {
    kind: kind.to_string(),
    title: title.to_string(),
    detail: detail.to_string(),
    source: source.to_string(),
  }
}

fn metric(
  label: &str,
  value: i32,
  unit: &str,
  source: &str,
  equivalent: &str,
) -> CampaignCoverageMetric {
  CampaignCoverageMetric {
    label: label.to_string(),
    value: value.to_string(),
    unit: unit.to_string(),
    source: source.to_string(),
    equivalent: equivalent.to_string(),
  }
}

fn actor(
  id: &str,
  label: &str,
  role: &str,
  status: &str,
  detail: &str,
  source: &str,
) -> CampaignCoverageActor {
  CampaignCoverageActor {
    id: id.to_string(),
    label: label.to_string(),
    role: role.to_string(),
    status: status.to_string(),
    detail: detail.to_string(),
    source: source.to_string(),
  }
}

fn process(
  id: &str,
  label: &str,
  detail: impl Into<String>,
  status: &str,
  source: &str,
) -> CampaignCoverageProcess {
  CampaignCoverageProcess {
    id: id.to_string(),
    label: label.to_string(),
    detail: detail.into(),
    status: status.to_string(),
    source: source.to_string(),
  }
}

fn decision(
  id: &str,
  label: &str,
  command_template: String,
  uncertainty: &str,
  source: &str,
  parameters: Vec<CampaignCoverageParameter>,
) -> CampaignCoverageDecision {
  CampaignCoverageDecision {
    id: id.to_string(),
    label: label.to_string(),
    command_template,
    uncertainty: uncertainty.to_string(),
    source: source.to_string(),
    parameters,
  }
}

fn number_parameter(
  name: &str,
  label: &str,
  min: Option<i32>,
  max: Option<i32>,
) -> CampaignCoverageParameter {
  CampaignCoverageParameter {
    name: name.to_string(),
    label: label.to_string(),
    input_type: "number".to_string(),
    options: Vec::new(),
    min,
    max,
  }
}

fn select_parameter(
  name: &str,
  label: &str,
  options: Vec<CampaignCoverageOption>,
) -> CampaignCoverageParameter {
  CampaignCoverageParameter {
    name: name.to_string(),
    label: label.to_string(),
    input_type: "select".to_string(),
    options,
    min: None,
    max: None,
  }
}

fn option(label: &str, value: &str) -> CampaignCoverageOption {
  CampaignCoverageOption {
    label: label.to_string(),
    value: value.to_string(),
  }
}
