use crate::affiliation::observe_affiliation;
use crate::debrief::{affiliation_debrief, competitive_player_debrief, educational_debrief};
use crate::inputs::resolve_inputs;
use crate::model::{
  AffiliationObservation, AffiliationRuleset, AffiliationStage, AffiliationWorldState,
  CompetitiveHistory, CompetitiveWorldState, History, Observation, PlayerObservation, Ruleset,
  WorldState,
};
use crate::sim::observe_for_human;
use crate::sim::observe_for_player;

use super::action::competitive_action_catalog;
use super::presentation::ReadOnlyResources;
use super::session::{TransitionSummary, affiliation_legal_commands, stabilization_legal_commands};

pub const CAMPAIGN_COVERAGE_SCHEMA_VERSION: &str = "campaign-coverage-v1";

#[derive(
  Clone, Debug, PartialEq, Eq, serde::Deserialize, serde::Serialize, schemars::JsonSchema,
)]
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
  #[serde(default, skip_serializing_if = "Option::is_none")]
  pub audio: Option<CampaignCoverageAudio>,
  pub replay: CampaignCoverageReplayMetadata,
}

#[derive(
  Clone, Debug, PartialEq, Eq, serde::Deserialize, serde::Serialize, schemars::JsonSchema,
)]
pub struct CampaignCoverageSession {
  pub session_id: String,
  pub campaign: String,
  pub seed: u64,
  pub turn: u32,
  pub max_turns: u32,
  pub done: bool,
}

#[derive(
  Clone, Debug, PartialEq, Eq, serde::Deserialize, serde::Serialize, schemars::JsonSchema,
)]
pub struct CampaignCoverageStage {
  pub id: String,
  pub label: String,
  pub detail: String,
  pub source: String,
}

#[derive(
  Clone, Debug, PartialEq, Eq, serde::Deserialize, serde::Serialize, schemars::JsonSchema,
)]
pub struct CampaignCoverageBriefing {
  pub kind: String,
  pub title: String,
  pub detail: String,
  pub source: String,
}

#[derive(
  Clone, Debug, PartialEq, Eq, serde::Deserialize, serde::Serialize, schemars::JsonSchema,
)]
pub struct CampaignCoverageMetric {
  pub label: String,
  pub value: String,
  pub unit: String,
  pub source: String,
  pub equivalent: String,
}

#[derive(
  Clone, Debug, PartialEq, Eq, serde::Deserialize, serde::Serialize, schemars::JsonSchema,
)]
pub struct CampaignCoverageActor {
  pub id: String,
  pub label: String,
  pub role: String,
  pub status: String,
  pub detail: String,
  pub source: String,
}

#[derive(
  Clone, Debug, PartialEq, Eq, serde::Deserialize, serde::Serialize, schemars::JsonSchema,
)]
pub struct CampaignCoverageProcess {
  pub id: String,
  pub label: String,
  pub detail: String,
  pub status: String,
  pub source: String,
}

#[derive(
  Clone, Debug, PartialEq, Eq, serde::Deserialize, serde::Serialize, schemars::JsonSchema,
)]
pub struct CampaignCoverageDecision {
  pub id: String,
  pub label: String,
  pub command_template: String,
  pub uncertainty: String,
  pub source: String,
  pub parameters: Vec<CampaignCoverageParameter>,
}

#[derive(
  Clone, Debug, PartialEq, Eq, serde::Deserialize, serde::Serialize, schemars::JsonSchema,
)]
pub struct CampaignCoverageParameter {
  pub name: String,
  pub label: String,
  pub input_type: String,
  pub options: Vec<CampaignCoverageOption>,
  pub min: Option<i32>,
  pub max: Option<i32>,
}

#[derive(
  Clone, Debug, PartialEq, Eq, serde::Deserialize, serde::Serialize, schemars::JsonSchema,
)]
pub struct CampaignCoverageOption {
  pub label: String,
  pub value: String,
}

#[derive(
  Clone, Debug, PartialEq, Eq, serde::Deserialize, serde::Serialize, schemars::JsonSchema,
)]
pub struct CampaignCoverageReplayMetadata {
  pub transition_count: usize,
  pub state_hash: Option<String>,
}

#[derive(
  Clone, Debug, PartialEq, Eq, serde::Deserialize, serde::Serialize, schemars::JsonSchema,
)]
pub struct CampaignCoverageAudio {
  pub music_state_id: String,
  pub audio_cue_ids: Vec<String>,
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
  let decisions = if done {
    Vec::new()
  } else {
    stabilization_decisions(turn, ruleset)
  };
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

  let stage = CampaignCoverageStage {
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
  };
  let actors = vec![actor(
    "health-system-executive",
    "Health system executive",
    "Player decision-maker",
    "observing",
    "Allocates visible resources and commitments while other institutions respond.",
    "Stabilization campaign role",
  )];
  let processes = vec![process(
    "stabilization-stage",
    "Stage response",
    if done {
      "No further stage response is available.".to_string()
    } else {
      "One host-defined response is available for this stabilization turn.".to_string()
    },
    if done { "complete" } else { "active" },
    "Stabilization stage and legal command surface",
  )];
  let audio = campaign_audio(
    "stabilization-v1",
    done,
    &stage,
    &briefings,
    &actors,
    &processes,
    history,
  );

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
    stage,
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
    actors,
    processes,
    decisions,
    history: history.to_vec(),
    debrief: if done {
      educational_debrief(typed_history)
    } else {
      Vec::new()
    },
    audio: Some(audio),
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

  let decisions = if done {
    Vec::new()
  } else {
    affiliation_decisions(state, ruleset)
  };
  let stage = CampaignCoverageStage {
    id: format!("{:?}", observation.stage).to_ascii_lowercase(),
    label: affiliation_stage_label(observation.stage).to_string(),
    detail: if done {
      "Review the partner, stakeholder, and integration tradeoffs in the debrief.".to_string()
    } else {
      "The current stage exposes a bounded institutional decision; later responses remain uncertain.".to_string()
    },
    source: "AffiliationObservation.stage".to_string(),
  };
  let actors = vec![
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
  ];
  let processes = affiliation_processes(&observation);
  let audio = campaign_audio(
    "regional-affiliation-v1",
    done,
    &stage,
    &briefings,
    &actors,
    &processes,
    history,
  );
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
    stage,
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
    actors,
    processes,
    decisions,
    history: history.to_vec(),
    debrief: if done {
      affiliation_debrief(typed_history)
    } else {
      Vec::new()
    },
    audio: Some(audio),
    replay: CampaignCoverageReplayMetadata {
      transition_count: history.len(),
      state_hash: latest_hash,
    },
  }
}

pub(crate) fn from_competitive(
  session_id: String,
  seed: u64,
  done: bool,
  state: &CompetitiveWorldState,
  prior_aggregated: Option<&crate::model::AggregatedMonthlyActions>,
  history: &[TransitionSummary],
  typed_history: &CompetitiveHistory,
) -> CampaignCoverageEnvelope {
  let observation = observe_for_human(state, prior_aggregated);
  let player = state
    .human_system()
    .expect("competitive campaign coverage requires a human system");
  let turn = if done { state.turn } else { state.turn + 1 };
  let latest_hash = history.last().map(|entry| entry.state_hash.clone());
  let mut briefings = vec![briefing(
    "organization",
    "Player system",
    &format!(
      "{} · {} runway",
      observation.org_name,
      observation.cash_runway_signal.label()
    ),
    "PlayerObservation.org_name/cash_runway_signal",
  )];
  briefings.extend(observation.market_bullets.iter().map(|detail| {
    briefing(
      "market",
      "Market signal",
      detail,
      "PlayerObservation.market_bullets",
    )
  }));
  briefings.extend(observation.policy_bullets.iter().map(|detail| {
    briefing(
      "policy",
      "Policy signal",
      detail,
      "PlayerObservation.policy_bullets",
    )
  }));

  let stage = CampaignCoverageStage {
    id: format!("month-{turn}"),
    label: if done {
      "Competitive campaign complete".to_string()
    } else {
      format!("Competitive month {turn}")
    },
    detail: if done {
      "Review the committed strategic tradeoffs in the host terminal debrief.".to_string()
    } else {
      "Choose from the canonical competitive action catalog; rival responses and delayed operating outcomes remain uncertain.".to_string()
    },
    source: "Competitive session turn and host completion state".to_string(),
  };

  let public_rival_signals = observation
    .market_bullets
    .iter()
    .filter(|detail| detail.to_ascii_lowercase().contains("rival"))
    .cloned()
    .collect::<Vec<_>>();
  let player_status = format!(
    "access {}, quality {}, workforce {}, community {}",
    observation.reported_access_index,
    observation.reported_quality_index,
    observation.workforce_trust_summary,
    observation.community_trust_summary
  );
  let rival_detail = if public_rival_signals.is_empty() {
    "Only public and lagged signals are available; private rival activity remains unobserved."
      .to_string()
  } else {
    public_rival_signals.join(" ")
  };
  let policy_detail = if observation.policy_bullets.is_empty() {
    "No current policy signal is reported in the player observation.".to_string()
  } else {
    observation.policy_bullets.join(" ")
  };
  let actors = vec![
    actor(
      "player-system",
      &observation.org_name,
      "Player institution",
      &player_status,
      "Allocates visible resources while regional institutions and other stakeholders respond.",
      "PlayerObservation actor-visible fields",
    ),
    actor(
      "regional-rivals",
      "Regional rivals",
      "Strategic institutions",
      if public_rival_signals.is_empty() {
        "no new public signal"
      } else {
        "public signals reported"
      },
      &rival_detail,
      "PlayerObservation.market_bullets",
    ),
    actor(
      "policy-institutions",
      "Policy institutions",
      "External stakeholders",
      if observation.policy_bullets.is_empty() {
        "no current policy signal"
      } else {
        "policy signals reported"
      },
      &policy_detail,
      "PlayerObservation.policy_bullets",
    ),
  ];

  let processes = competitive_processes(&observation);
  let decisions = if done {
    Vec::new()
  } else {
    competitive_decisions(
      session_id.clone(),
      turn,
      ReadOnlyResources {
        cash: player.resources.cash,
        action_points: player.resources.ap_budget,
        political_capital: player.resources.political_capital,
      },
    )
  };
  let audio = campaign_audio(
    "competitive-regional-v1",
    done,
    &stage,
    &briefings,
    &actors,
    &processes,
    history,
  );

  CampaignCoverageEnvelope {
    schema_version: CAMPAIGN_COVERAGE_SCHEMA_VERSION.to_string(),
    session: CampaignCoverageSession {
      session_id,
      campaign: "competitive-regional-v1".to_string(),
      seed,
      turn,
      max_turns: crate::mcp::session::COMPETITIVE_MONTH_LIMIT,
      done,
    },
    campaign_role: "nonprofit health-system lead in a competitive regional market".to_string(),
    stage,
    briefing: briefings,
    metrics: vec![
      metric(
        "Cash",
        player.resources.cash,
        "game units",
        "HealthSystemState.resources.cash",
        "Current resource",
      ),
      metric(
        "Action points",
        player.resources.ap_budget as i32,
        "AP",
        "HealthSystemState.resources.ap_budget",
        "Current monthly action budget",
      ),
      metric(
        "Political capital",
        player.resources.political_capital as i32,
        "capital units",
        "HealthSystemState.resources.political_capital",
        "Current resource",
      ),
      metric(
        "Access",
        observation.reported_access_index,
        "index",
        "PlayerObservation.reported_access_index",
        "Visible player outcome",
      ),
      metric(
        "Quality",
        observation.reported_quality_index,
        "index",
        "PlayerObservation.reported_quality_index",
        "Visible player outcome",
      ),
      metric(
        "Staffed beds",
        observation.staffed_beds,
        "beds",
        "PlayerObservation.staffed_beds",
        "Current capacity",
      ),
      metric(
        "Monthly demand",
        observation.monthly_demand,
        "visits",
        "PlayerObservation.monthly_demand",
        "Current operating pressure",
      ),
      metric(
        "Treated volume",
        observation.monthly_treated_volume,
        "visits",
        "PlayerObservation.monthly_treated_volume",
        "Current operating result",
      ),
      metric(
        "Unmet demand",
        observation.monthly_unmet_demand,
        "visits",
        "PlayerObservation.monthly_unmet_demand",
        "Current operating pressure",
      ),
      metric(
        "Operating margin",
        observation.monthly_operating_margin,
        "game units",
        "PlayerObservation.monthly_operating_margin",
        "Current operating result",
      ),
    ],
    actors,
    processes,
    decisions,
    history: history.to_vec(),
    debrief: if done {
      competitive_player_debrief(typed_history)
    } else {
      Vec::new()
    },
    audio: Some(audio),
    replay: CampaignCoverageReplayMetadata {
      transition_count: history.len(),
      state_hash: latest_hash,
    },
  }
}

fn competitive_processes(observation: &PlayerObservation) -> Vec<CampaignCoverageProcess> {
  let mut processes = vec![process(
    "in-flight-projects",
    "In-flight projects",
    observation.in_flight_projects.clone(),
    if observation.in_flight_projects == "none" {
      "idle"
    } else {
      "active"
    },
    "PlayerObservation.in_flight_projects",
  )];
  processes.push(process(
    "information-gaps",
    "Information gaps",
    if observation.intel_gaps.is_empty() {
      "No explicit intelligence gap is currently reported.".to_string()
    } else {
      observation.intel_gaps.join(" ")
    },
    if observation.intel_gaps.is_empty() {
      "clear"
    } else {
      "open"
    },
    "PlayerObservation.intel_gaps",
  ));
  if let Some(review) = &observation.annual_policy_review {
    processes.push(process(
      "annual-policy-review",
      "Annual policy review",
      review.join(" "),
      "reported",
      "PlayerObservation.annual_policy_review",
    ));
  }
  if observation.rna_strike_active {
    processes.push(process(
      "rna-strike",
      "Workforce disruption",
      "A workforce disruption is currently reported in the player observation.",
      "active",
      "PlayerObservation.rna_strike_active",
    ));
  }
  processes
}

fn competitive_decisions(
  session_id: String,
  turn: u32,
  resources: ReadOnlyResources,
) -> Vec<CampaignCoverageDecision> {
  competitive_action_catalog(session_id, turn, resources)
    .actions
    .into_iter()
    .map(|action| {
      let uncertainty = format!(
        "{}; {} Constraint: {}",
        action.delay_label, action.uncertainty_label, action.constraint_label
      );
      decision(
        &action.id,
        &action.label,
        action.command_template,
        &uncertainty,
        "competitive-actions-v1 ActionSpec",
        action
          .parameters
          .into_iter()
          .map(competitive_parameter)
          .collect(),
      )
    })
    .collect()
}

fn competitive_parameter(parameter: super::action::ActionParameter) -> CampaignCoverageParameter {
  CampaignCoverageParameter {
    name: parameter.name,
    label: parameter.label,
    input_type: parameter.input_type,
    options: parameter
      .options
      .into_iter()
      .map(|value| option(&value, &value))
      .collect(),
    min: parameter.min,
    max: parameter.max,
  }
}

fn campaign_audio(
  campaign: &str,
  done: bool,
  stage: &CampaignCoverageStage,
  briefings: &[CampaignCoverageBriefing],
  actors: &[CampaignCoverageActor],
  processes: &[CampaignCoverageProcess],
  history: &[TransitionSummary],
) -> CampaignCoverageAudio {
  let visible_text = [
    stage.label.as_str(),
    stage.detail.as_str(),
    &briefings
      .iter()
      .flat_map(|entry| [entry.title.as_str(), entry.detail.as_str()])
      .collect::<Vec<_>>()
      .join(" "),
    &actors
      .iter()
      .flat_map(|entry| {
        [
          entry.label.as_str(),
          entry.role.as_str(),
          entry.status.as_str(),
          entry.detail.as_str(),
        ]
      })
      .collect::<Vec<_>>()
      .join(" "),
    &processes
      .iter()
      .flat_map(|entry| {
        [
          entry.label.as_str(),
          entry.status.as_str(),
          entry.detail.as_str(),
        ]
      })
      .collect::<Vec<_>>()
      .join(" "),
  ]
  .join(" ")
  .to_ascii_lowercase();
  let music_state_id = if done {
    "debrief"
  } else if campaign == "regional-affiliation-v1" || visible_text.contains("affiliation") {
    "affiliation_negotiation"
  } else if campaign == "competitive-regional-v1"
    && (visible_text.contains("rival") || visible_text.contains("competition"))
  {
    "competitive_escalation"
  } else if visible_text.contains("regulat") || visible_text.contains("policy review") {
    "regulatory_scrutiny"
  } else if [
    "pressure",
    "strained",
    "shortage",
    "constraint",
    "unmet",
    "negative",
  ]
  .iter()
  .any(|word| visible_text.contains(word))
  {
    "pressure"
  } else {
    "stable_operations"
  };

  let transition_text = history
    .last()
    .map(|summary| {
      summary
        .events
        .iter()
        .chain(summary.effects.iter())
        .map(String::as_str)
        .collect::<Vec<_>>()
        .join(" ")
        .to_ascii_lowercase()
    })
    .unwrap_or_default();
  let mut audio_cue_ids = Vec::new();
  let mut add_cue = |cue_id: &str| {
    if !audio_cue_ids.iter().any(|existing| existing == cue_id) {
      audio_cue_ids.push(cue_id.to_string());
    }
  };
  if transition_text.contains("project") && transition_text.contains("complete") {
    add_cue("event.project-complete");
  }
  if ["staffing", "staffed", "vacancy", "workforce constraint"]
    .iter()
    .any(|word| transition_text.contains(word))
  {
    add_cue("event.staffing-constraint");
  }
  if transition_text.contains("operating loss") || transition_text.contains("negative margin") {
    add_cue("event.operating-loss");
  }
  if transition_text.contains("operating recovery") || transition_text.contains("recovery") {
    add_cue("event.operating-recovery");
  }
  if transition_text.contains("payer") {
    add_cue("event.payer-decision");
  }
  if transition_text.contains("regulat") || transition_text.contains("policy decision") {
    add_cue("event.regulatory-decision");
  }
  if (transition_text.contains("rival")
    && (transition_text.contains("expand") || transition_text.contains("expansion")))
    || (transition_text.contains("expan") && transition_text.contains("rival"))
  {
    add_cue("event.rival-expansion");
  }
  if transition_text.contains("affiliation milestone")
    || transition_text.contains("integration milestone")
  {
    add_cue("event.affiliation-milestone");
  }

  CampaignCoverageAudio {
    music_state_id: music_state_id.to_string(),
    audio_cue_ids,
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
