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

  ResolutionEnvelope {
    schema_version: RESOLUTION_SCHEMA_VERSION.to_string(),
    session_id,
    campaign: "competitive-regional-v1".to_string(),
    turn: transition.next.turn,
    before,
    after,
    steps,
    effects,
    replay: ResolutionReplayMetadata {
      selected_turn: transition.next.turn,
      transition_count,
      state_hash: transition.state_hash.clone(),
    },
  }
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
