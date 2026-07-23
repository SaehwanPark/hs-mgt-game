use crate::model::{AggregatedMonthlyActions, CompetitiveTransition, Difficulty};
use crate::sim::observe_for_human;

use super::presentation::{
  ReadOnlyObservation, ReadOnlyPendingEffect, ReadOnlyPresentationEnvelope, ReadOnlyResources,
  ReadOnlySession,
};
use super::session::{COMPETITIVE_MONTH_LIMIT, TransitionSummary};

pub const RESOLUTION_SCHEMA_VERSION: &str = "competitive-resolution-v1";

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ResolutionEnvelope {
  pub schema_version: String,
  pub session_id: String,
  pub campaign: String,
  pub turn: u32,
  pub before: ResolutionSnapshot,
  pub after: ResolutionSnapshot,
  pub steps: Vec<ResolutionStep>,
  pub effects: Vec<ResolutionEffect>,
  pub audio_cue_ids: Vec<String>,
  pub replay: ResolutionReplayMetadata,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ResolutionSnapshot {
  pub turn: u32,
  pub resources: ReadOnlyResources,
  pub observation: ReadOnlyObservation,
  pub pending_effects: Vec<ReadOnlyPendingEffect>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ResolutionStep {
  pub id: String,
  pub label: String,
  pub source: String,
  pub items: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ResolutionEffect {
  pub source: String,
  pub metric: String,
  pub delta: i32,
  pub text: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ResolutionReplayMetadata {
  pub selected_turn: u32,
  pub transition_count: usize,
  pub state_hash: String,
}

pub(crate) fn from_competitive_transition(
  session_id: String,
  seed: u64,
  difficulty: Difficulty,
  transition: &CompetitiveTransition,
  prior_aggregated: Option<&AggregatedMonthlyActions>,
  transition_count: usize,
  summary: TransitionSummary,
) -> ResolutionEnvelope {
  let before = snapshot(
    session_id.as_str(),
    seed,
    difficulty,
    &transition.prior,
    prior_aggregated,
    false,
  );
  let after = snapshot(
    session_id.as_str(),
    seed,
    difficulty,
    &transition.next,
    Some(&transition.aggregated),
    transition.next.turn >= COMPETITIVE_MONTH_LIMIT,
  );
  let effects = transition
    .effects
    .iter()
    .map(|effect| ResolutionEffect {
      source: effect.source.to_string(),
      metric: effect.metric.to_string(),
      delta: effect.delta,
      text: format!(
        "{} changed {} by {}",
        effect.source, effect.metric, effect.delta
      ),
    })
    .collect::<Vec<_>>();
  let steps = vec![
    step(
      "submitted",
      "Submitted batch",
      "TransitionSummary.command",
      vec![summary.command.clone()],
    ),
    step(
      "responses",
      "Visible institutional responses",
      "TransitionSummary.events",
      summary.events.clone(),
    ),
    step(
      "processes",
      "Process advancement",
      "PlayerObservation.in_flight_projects",
      process_changes(&before.pending_effects, &after.pending_effects),
    ),
    step(
      "operations",
      "Operating result",
      "PlayerObservation.operations",
      operations_items(&after.observation),
    ),
    step(
      "resources",
      "Resource changes",
      "PlayerResources",
      resource_changes(&before.resources, &after.resources),
    ),
    step(
      "effects",
      "Direct committed effects",
      "TransitionSummary.effects",
      summary.effects.clone(),
    ),
    step(
      "information",
      "Newly visible information",
      "PlayerObservation",
      information_items(&after.observation),
    ),
    step(
      "pending",
      "Updated pending processes",
      "PlayerObservation.in_flight_projects",
      pending_items(&after.pending_effects),
    ),
  ];
  let audio_cue_ids = visible_event_cue_ids(
    &summary,
    before.observation.operations.margin,
    after.observation.operations.margin,
    &after.observation,
  );

  ResolutionEnvelope {
    schema_version: RESOLUTION_SCHEMA_VERSION.to_string(),
    session_id,
    campaign: "competitive-regional-v1".to_string(),
    turn: transition.next.turn,
    before,
    after,
    steps,
    effects,
    audio_cue_ids,
    replay: ResolutionReplayMetadata {
      selected_turn: transition.next.turn,
      transition_count,
      state_hash: transition.state_hash.clone(),
    },
  }
}

fn visible_event_cue_ids(
  summary: &TransitionSummary,
  before_margin: i32,
  after_margin: i32,
  after_observation: &ReadOnlyObservation,
) -> Vec<String> {
  let mut visible_text = summary.events.join(" ");
  visible_text.push(' ');
  visible_text.push_str(&summary.effects.join(" "));
  visible_text.push(' ');
  visible_text.push_str(&after_observation.workforce_trust);
  visible_text.push(' ');
  visible_text.push_str(&after_observation.in_flight_projects);
  for metric in &after_observation.staffing {
    visible_text.push(' ');
    visible_text.push_str(&metric.label);
    visible_text.push(' ');
    visible_text.push_str(&metric.value.to_string());
  }
  let visible_text = visible_text.to_lowercase();
  let mut cue_ids = Vec::new();
  if visible_text.contains("project") && visible_text.contains("complete") {
    cue_ids.push("event.project-complete".to_string());
  }
  if ["staffing", "staffed", "vacancy", "workforce constraint"]
    .iter()
    .any(|word| visible_text.contains(word))
  {
    cue_ids.push("event.staffing-constraint".to_string());
  }
  if after_margin < 0 {
    cue_ids.push("event.operating-loss".to_string());
  }
  if after_margin > before_margin {
    cue_ids.push("event.operating-recovery".to_string());
  }
  if visible_text.contains("payer") {
    cue_ids.push("event.payer-decision".to_string());
  }
  if visible_text.contains("regulat") || visible_text.contains("policy decision") {
    cue_ids.push("event.regulatory-decision".to_string());
  }
  if (visible_text.contains("rival")
    && (visible_text.contains("expand") || visible_text.contains("expansion")))
    || (visible_text.contains("expan") && visible_text.contains("rival"))
  {
    cue_ids.push("event.rival-expansion".to_string());
  }
  if visible_text.contains("affiliation milestone")
    || visible_text.contains("integration milestone")
  {
    cue_ids.push("event.affiliation-milestone".to_string());
  }
  cue_ids
}

fn snapshot(
  session_id: &str,
  seed: u64,
  difficulty: Difficulty,
  world: &crate::model::CompetitiveWorldState,
  prior_aggregated: Option<&AggregatedMonthlyActions>,
  done: bool,
) -> ResolutionSnapshot {
  let observation = observe_for_human(world, prior_aggregated);
  let player = world
    .human_system()
    .expect("competitive resolution must include human system");
  let session = ReadOnlySession {
    session_id: session_id.to_string(),
    campaign: "competitive-regional-v1".to_string(),
    seed,
    difficulty: Some(difficulty.label().to_string()),
    year: world.policy_calendar.year,
    month: world.policy_calendar.month_in_year,
    month_name: world.policy_calendar.month_name().to_string(),
    turn: if done { world.turn } else { world.turn + 1 },
    max_turns: COMPETITIVE_MONTH_LIMIT,
    done,
  };
  let projection: ReadOnlyPresentationEnvelope =
    super::presentation::from_competitive_observation(session, player, &observation, &[]);
  ResolutionSnapshot {
    turn: projection.session.turn,
    resources: projection.resources,
    observation: projection.observation,
    pending_effects: projection.pending_effects,
  }
}

fn step(id: &str, label: &str, source: &str, items: Vec<String>) -> ResolutionStep {
  ResolutionStep {
    id: id.to_string(),
    label: label.to_string(),
    source: source.to_string(),
    items,
  }
}

fn process_changes(
  before: &[ReadOnlyPendingEffect],
  after: &[ReadOnlyPendingEffect],
) -> Vec<String> {
  let mut items = Vec::new();
  items.push(format!("Before: {} pending processes", before.len()));
  items.push(format!("After: {} pending processes", after.len()));
  items
}

fn operations_items(observation: &ReadOnlyObservation) -> Vec<String> {
  let operations = &observation.operations;
  vec![
    format!("Demand: {}", operations.demand),
    format!("Treated volume: {}", operations.treated_volume),
    format!("Unmet demand: {}", operations.unmet_demand),
    format!("Revenue: {}", operations.revenue),
    format!("Cost: {}", operations.cost),
    format!("Margin: {}", operations.margin),
  ]
}

fn resource_changes(before: &ReadOnlyResources, after: &ReadOnlyResources) -> Vec<String> {
  vec![
    format!("Cash: {} → {}", before.cash, after.cash),
    format!(
      "Action points: {} → {}",
      before.action_points, after.action_points
    ),
    format!(
      "Political capital: {} → {}",
      before.political_capital, after.political_capital
    ),
  ]
}

fn information_items(observation: &ReadOnlyObservation) -> Vec<String> {
  observation
    .market_bullets
    .iter()
    .chain(observation.policy_bullets.iter())
    .chain(observation.information_gaps.iter())
    .cloned()
    .collect()
}

fn pending_items(pending: &[ReadOnlyPendingEffect]) -> Vec<String> {
  pending
    .iter()
    .map(|effect| format!("{}: {}", effect.label, effect.detail))
    .collect()
}

#[cfg(test)]
mod tests {
  use super::super::presentation::{ReadOnlyMetric, ReadOnlyObservation, ReadOnlyOperations};
  use super::visible_event_cue_ids;
  use crate::mcp::session::TransitionSummary;

  fn observation() -> ReadOnlyObservation {
    ReadOnlyObservation {
      organization_name: "Test Health System".to_string(),
      access_index: 60,
      prior_access_revision: None,
      quality_index: 70,
      workforce_trust: "workforce constraint reported".to_string(),
      community_trust: "stable".to_string(),
      staffing: vec![ReadOnlyMetric {
        label: "Nurses".to_string(),
        value: 20,
      }],
      capacity: Vec::new(),
      operations: ReadOnlyOperations {
        demand: 100,
        treated_volume: 90,
        unmet_demand: 10,
        revenue: 90,
        cost: 100,
        margin: -10,
      },
      in_flight_projects: "Project complete reported".to_string(),
      cash_runway_signal: "strained".to_string(),
      market_bullets: Vec::new(),
      policy_bullets: Vec::new(),
      annual_policy_review: None,
      consultant_options: Vec::new(),
      information_gaps: Vec::new(),
    }
  }

  fn summary() -> TransitionSummary {
    TransitionSummary {
      turn: 1,
      command: "hold".to_string(),
      events: vec![
        "Payer decision was reported".to_string(),
        "Regulatory policy decision was reported".to_string(),
        "Public rival expansion was observed".to_string(),
        "Affiliation milestone was committed".to_string(),
      ],
      effects: vec!["Project complete reported".to_string()],
      state_hash: "hash-1".to_string(),
      consultant_options: Vec::new(),
    }
  }

  #[test]
  fn visible_event_cue_projection_covers_supported_event_cues() {
    let ids = visible_event_cue_ids(&summary(), 10, -10, &observation());

    assert_eq!(
      ids,
      vec![
        "event.project-complete",
        "event.staffing-constraint",
        "event.operating-loss",
        "event.payer-decision",
        "event.regulatory-decision",
        "event.rival-expansion",
        "event.affiliation-milestone",
      ]
    );
  }

  #[test]
  fn visible_event_cue_projection_emits_recovery_only_when_margin_improves() {
    let mut after = observation();
    after.workforce_trust = "stable".to_string();
    after.in_flight_projects = "none".to_string();
    after.operations.margin = 10;

    let ids = visible_event_cue_ids(
      &TransitionSummary {
        events: Vec::new(),
        effects: Vec::new(),
        ..summary()
      },
      -10,
      10,
      &after,
    );

    assert_eq!(ids, vec!["event.operating-recovery"]);
  }

  #[test]
  fn visible_event_cue_projection_is_empty_without_visible_triggers() {
    let mut after = observation();
    after.workforce_trust = "stable".to_string();
    after.in_flight_projects = "none".to_string();
    after.operations.margin = 10;

    let ids = visible_event_cue_ids(
      &TransitionSummary {
        events: Vec::new(),
        effects: Vec::new(),
        ..summary()
      },
      10,
      10,
      &after,
    );

    assert!(ids.is_empty());
  }
}
