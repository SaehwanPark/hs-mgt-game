use crate::model::{
  AggregatedMonthlyActions, CashRunwaySignal, CompetitiveWorldState, HealthSystemState,
  PlayerObservation,
};
use crate::sim::observe_for_human;

use super::presentation::{ReadOnlyMetric, ReadOnlySession};
use super::session::COMPETITIVE_MONTH_LIMIT;

pub const REGIONAL_WORLD_SCHEMA_VERSION: &str = "competitive-regional-world-v1";
const PUBLIC_RIVAL_LAG_MONTHS: u32 = 1;

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct RegionalWorldEnvelope {
  pub schema_version: String,
  pub session: ReadOnlySession,
  pub entities: Vec<RegionalWorldEntity>,
  pub overlays: Vec<RegionalWorldOverlay>,
  pub navigation: Vec<RegionalWorldNavigation>,
  pub missing: Vec<RegionalWorldMissing>,
  pub replay: RegionalWorldReplayMetadata,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct RegionalWorldEntity {
  pub id: String,
  pub name: String,
  pub role: String,
  pub visibility: String,
  pub layout_slot: u32,
  pub status: String,
  pub status_label: String,
  pub source: String,
  pub facilities: Vec<RegionalWorldFacility>,
  pub signals: Vec<RegionalWorldSignal>,
  pub processes: Vec<RegionalWorldProcess>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct RegionalWorldFacility {
  pub name: String,
  pub kind: String,
  pub component_id: String,
  pub metrics: Vec<ReadOnlyMetric>,
  pub source: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct RegionalWorldSignal {
  pub text: String,
  pub observed_month: u32,
  pub source: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct RegionalWorldProcess {
  pub label: String,
  pub detail: String,
  pub source: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct RegionalWorldOverlay {
  pub id: String,
  pub label: String,
  pub value: String,
  pub unit: String,
  pub source: String,
  pub equivalent: String,
  pub operational_overlay_id: Option<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct RegionalWorldNavigation {
  pub id: String,
  pub label: String,
  pub target: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct RegionalWorldMissing {
  pub id: String,
  pub label: String,
  pub detail: String,
  pub source: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct RegionalWorldReplayMetadata {
  pub transition_count: usize,
  pub state_hash: Option<String>,
}

pub(crate) fn from_competitive_world(
  session_id: String,
  seed: u64,
  done: bool,
  world: &CompetitiveWorldState,
  prior_aggregated: Option<&AggregatedMonthlyActions>,
  transition_count: usize,
  state_hash: Option<String>,
) -> RegionalWorldEnvelope {
  let observation = observe_for_human(world, prior_aggregated);
  let human_id = world
    .human_system()
    .map(|system| system.system_id)
    .expect("regional world must include human system");
  let session = ReadOnlySession {
    session_id,
    campaign: "competitive-regional-v1".to_string(),
    seed,
    difficulty: Some(world.difficulty.label().to_string()),
    year: world.policy_calendar.year,
    month: world.policy_calendar.month_in_year,
    month_name: world.policy_calendar.month_name().to_string(),
    turn: if done { world.turn } else { world.turn + 1 },
    max_turns: COMPETITIVE_MONTH_LIMIT,
    done,
  };
  let mut entities = Vec::new();
  let mut missing = Vec::new();
  for (index, system) in world.systems.iter().enumerate() {
    let is_human = system.system_id == human_id;
    let (entity, entity_missing) = if is_human {
      let entity = player_entity(system, &observation, index as u32);
      let missing = if entity.processes.is_empty() {
        vec![RegionalWorldMissing {
          id: format!("system-{}-process", system.system_id),
          label: "Player pending process".to_string(),
          detail: "No in-flight player process is reported.".to_string(),
          source: "PlayerObservation.in_flight_projects".to_string(),
        }]
      } else {
        Vec::new()
      };
      (entity, missing)
    } else {
      rival_entity(world, system, index as u32)
    };
    entities.push(entity);
    missing.extend(entity_missing);
  }

  RegionalWorldEnvelope {
    schema_version: REGIONAL_WORLD_SCHEMA_VERSION.to_string(),
    session,
    entities,
    overlays: overlays(&observation),
    navigation: vec![
      navigation("briefing", "Executive briefing", "#briefing-heading"),
      navigation("map", "Regional map", "#map-heading"),
      navigation("detail", "Selected detail", "#entity-heading"),
      navigation("timeline", "Pending timeline", "#timeline-heading"),
    ],
    missing,
    replay: RegionalWorldReplayMetadata {
      transition_count,
      state_hash,
    },
  }
}

fn player_entity(
  system: &HealthSystemState,
  observation: &PlayerObservation,
  layout_slot: u32,
) -> RegionalWorldEntity {
  let pressure = observation.monthly_unmet_demand > 0
    || observation.monthly_operating_margin < 0
    || observation
      .cash_runway_signal
      .label()
      .to_ascii_lowercase()
      .contains("strained");
  let status = if pressure { "watch" } else { "stable" };
  let mut processes = Vec::new();
  if !observation.in_flight_projects.eq_ignore_ascii_case("none")
    && !observation.in_flight_projects.is_empty()
  {
    processes.push(RegionalWorldProcess {
      label: "In-flight project".to_string(),
      detail: observation.in_flight_projects.clone(),
      source: "PlayerObservation.in_flight_projects".to_string(),
    });
  }
  RegionalWorldEntity {
    id: format!("system-{}", system.system_id),
    name: system.name.clone(),
    role: "Player system".to_string(),
    visibility: "owned".to_string(),
    layout_slot,
    status: status.to_string(),
    status_label: if pressure { "Watch" } else { "Stable" }.to_string(),
    source: "Host-projected player identity + PlayerObservation".to_string(),
    facilities: player_facilities(observation),
    signals: Vec::new(),
    processes,
  }
}

fn rival_entity(
  world: &CompetitiveWorldState,
  system: &HealthSystemState,
  layout_slot: u32,
) -> (RegionalWorldEntity, Vec<RegionalWorldMissing>) {
  let observed_month = world
    .policy_calendar
    .month_index
    .saturating_sub(PUBLIC_RIVAL_LAG_MONTHS);
  let signals = world
    .public_action_log
    .iter()
    .filter(|entry| entry.system_id == system.system_id && entry.month_index == observed_month)
    .map(|entry| RegionalWorldSignal {
      text: entry.summary.clone(),
      observed_month: entry.month_index,
      source: "PublicActionEntry via one-month observation lag".to_string(),
    })
    .collect::<Vec<_>>();
  let mut missing = vec![RegionalWorldMissing {
    id: format!("system-{}-private-detail", system.system_id),
    label: format!("{} private detail", system.name),
    detail: "Private rival operations, facilities, resources, and projects are unavailable."
      .to_string(),
    source: "Standard player observation boundary".to_string(),
  }];
  if signals.is_empty() {
    missing.push(RegionalWorldMissing {
      id: format!("system-{}-public-signal", system.system_id),
      label: format!("{} public signal", system.name),
      detail: format!("No public signal reported for observed month {observed_month}."),
      source: "PublicActionEntry via one-month observation lag".to_string(),
    });
  }
  (
    RegionalWorldEntity {
      id: format!("system-{}", system.system_id),
      name: system.name.clone(),
      role: "Public rival".to_string(),
      visibility: "public identity".to_string(),
      layout_slot,
      status: "reported".to_string(),
      status_label: "Public signal only".to_string(),
      source: "Host-projected public identity".to_string(),
      facilities: Vec::new(),
      signals,
      processes: Vec::new(),
    },
    missing,
  )
}

fn player_facilities(observation: &PlayerObservation) -> Vec<RegionalWorldFacility> {
  vec![
    facility(
      "Inpatient beds",
      "Owned capacity",
      "general-hospital-base",
      vec![metric("Staffed beds", observation.staffed_beds)],
    ),
    facility(
      "Outpatient clinics",
      "Owned capacity",
      "ambulatory-center",
      vec![metric(
        "Outpatient capacity",
        observation.outpatient_capacity,
      )],
    ),
    facility(
      "Emergency and ICU",
      "Owned capacity",
      "emergency-department",
      vec![
        metric("Emergency", observation.emergency_capacity),
        metric("ICU", observation.icu_capacity),
      ],
    ),
    facility(
      "Specialty lines",
      "Owned capacity",
      "specialty-center",
      vec![
        metric("Obstetrics", observation.obstetrics_capacity),
        metric("Psychiatric", observation.psychiatric_capacity),
        metric("Cardiology", observation.cardiology_capacity),
        metric("Oncology", observation.oncology_capacity),
        metric("Infusion", observation.infusion_capacity),
        metric("Neurology", observation.neurology_capacity),
        metric("ASC", observation.asc_capacity),
      ],
    ),
  ]
}

fn facility(
  name: &str,
  kind: &str,
  component_id: &str,
  metrics: Vec<ReadOnlyMetric>,
) -> RegionalWorldFacility {
  RegionalWorldFacility {
    name: name.to_string(),
    kind: kind.to_string(),
    component_id: component_id.to_string(),
    metrics,
    source: "PlayerObservation capacity fields".to_string(),
  }
}

fn metric(label: &str, value: i32) -> ReadOnlyMetric {
  ReadOnlyMetric {
    label: label.to_string(),
    value,
  }
}

fn overlays(observation: &PlayerObservation) -> Vec<RegionalWorldOverlay> {
  let mut overlays = vec![
    overlay(
      "demand",
      "Reported demand",
      observation.monthly_demand.to_string(),
      "demand units",
      "PlayerObservation.monthly_demand",
      "Monthly demand line",
    ),
    overlay(
      "access",
      "Reported access",
      observation.reported_access_index.to_string(),
      "index",
      "PlayerObservation.reported_access_index",
      "Access status and source-linked metric",
    ),
    overlay(
      "unmet-demand",
      "Unmet demand",
      observation.monthly_unmet_demand.to_string(),
      "demand units",
      "PlayerObservation.monthly_unmet_demand",
      "Operating result and pressure explanation",
    ),
    overlay(
      "staffed-beds",
      "Staffed beds",
      observation.staffed_beds.to_string(),
      "beds",
      "PlayerObservation.staffed_beds",
      "Owned inpatient capacity marker",
    ),
    overlay(
      "pending-processes",
      "Pending processes",
      observation.in_flight_projects.clone(),
      "reported process",
      "PlayerObservation.in_flight_projects",
      "Pending timeline and selected detail",
    ),
  ];
  overlays.extend(operational_overlays(observation));
  overlays
}

fn operational_overlays(observation: &PlayerObservation) -> Vec<RegionalWorldOverlay> {
  let mut overlays = Vec::new();
  if observation.monthly_unmet_demand > 0 {
    overlays.push(operational_overlay(
      "operational-demand-pressure",
      "Demand pressure",
      observation.monthly_unmet_demand.to_string(),
      "demand units",
      "PlayerObservation.monthly_unmet_demand",
      "Demand pressure; visible unmet-demand value is reported",
    ));
  }
  if !observation.in_flight_projects.trim().is_empty()
    && !observation.in_flight_projects.eq_ignore_ascii_case("none")
  {
    overlays.push(operational_overlay(
      "operational-active-capital-project",
      "Active capital project",
      observation.in_flight_projects.clone(),
      "reported process",
      "PlayerObservation.in_flight_projects",
      "Active capital project; host-reported project timing is visible",
    ));
  }
  if observation.monthly_operating_margin < 0
    || matches!(observation.cash_runway_signal, CashRunwaySignal::Strained)
  {
    overlays.push(operational_overlay(
      "operational-financial-distress",
      "Financial distress",
      format!(
        "margin {}; runway {}",
        observation.monthly_operating_margin,
        observation.cash_runway_signal.label()
      ),
      "reported status",
      "PlayerObservation.monthly_operating_margin + PlayerObservation.cash_runway_signal",
      "Financial distress; visible cash/runway signal is reported",
    ));
  }
  if observation
    .community_trust_summary
    .eq_ignore_ascii_case("watch")
  {
    overlays.push(operational_overlay(
      "operational-community-trust-concern",
      "Community-trust concern",
      observation.community_trust_summary.clone(),
      "reported status",
      "PlayerObservation.community_trust_summary",
      "Community-trust concern; visible trust status is reported",
    ));
  }
  if !observation.intel_gaps.is_empty() || observation.prior_access_revision.is_some() {
    let gap_summary = observation.intel_gaps.join("; ");
    let value = if let Some((turn, revised_value)) = observation.prior_access_revision {
      format!(
        "{}; prior access revision at turn {}: {}",
        if gap_summary.is_empty() {
          "No additional intelligence gap"
        } else {
          &gap_summary
        },
        turn,
        revised_value
      )
    } else {
      observation.intel_gaps.join("; ")
    };
    overlays.push(operational_overlay(
      "operational-uncertain-stale-intelligence",
      "Uncertain or stale intelligence",
      value,
      "reported information status",
      "PlayerObservation.intel_gaps / PlayerObservation.prior_access_revision",
      "Uncertain or stale intelligence; missingness or revision remains explicit",
    ));
  }
  overlays
}

fn overlay(
  id: &str,
  label: &str,
  value: String,
  unit: &str,
  source: &str,
  equivalent: &str,
) -> RegionalWorldOverlay {
  RegionalWorldOverlay {
    id: id.to_string(),
    label: label.to_string(),
    value,
    unit: unit.to_string(),
    source: source.to_string(),
    equivalent: equivalent.to_string(),
    operational_overlay_id: None,
  }
}

fn operational_overlay(
  id: &str,
  label: &str,
  value: String,
  unit: &str,
  source: &str,
  equivalent: &str,
) -> RegionalWorldOverlay {
  RegionalWorldOverlay {
    id: id.to_string(),
    label: label.to_string(),
    value,
    unit: unit.to_string(),
    source: source.to_string(),
    equivalent: equivalent.to_string(),
    operational_overlay_id: Some(id.to_string()),
  }
}

fn navigation(id: &str, label: &str, target: &str) -> RegionalWorldNavigation {
  RegionalWorldNavigation {
    id: id.to_string(),
    label: label.to_string(),
    target: target.to_string(),
  }
}

#[cfg(test)]
mod tests {
  use super::*;

  #[test]
  fn operational_overlay_bindings_use_only_direct_visible_conditions() {
    let observation = PlayerObservation {
      org_name: "Riverside".to_string(),
      reported_access_index: 70,
      prior_access_revision: Some((2, 68)),
      reported_quality_index: 72,
      workforce_trust_summary: "strained".to_string(),
      community_trust_summary: "watch".to_string(),
      staffed_beds: 100,
      outpatient_capacity: 100,
      emergency_capacity: 10,
      icu_capacity: 5,
      obstetrics_capacity: 4,
      psychiatric_capacity: 4,
      cardiology_capacity: 4,
      oncology_capacity: 4,
      infusion_capacity: 4,
      neurology_capacity: 4,
      asc_capacity: 4,
      nurses: 10,
      physicians: 10,
      admins: 10,
      monthly_demand: 120,
      monthly_treated_volume: 108,
      monthly_unmet_demand: 12,
      monthly_operating_revenue: 90,
      monthly_operating_cost: 100,
      monthly_operating_margin: -10,
      in_flight_projects: "tower (month 2 of 12)".to_string(),
      cash_runway_signal: CashRunwaySignal::Strained,
      market_bullets: Vec::new(),
      policy_bullets: Vec::new(),
      annual_policy_review: None,
      consultant_options: Vec::new(),
      intel_gaps: vec!["Northlake activity last month".to_string()],
      rna_strike_active: false,
    };

    let categories = operational_overlays(&observation);
    assert_eq!(
      categories
        .iter()
        .map(|overlay| overlay.operational_overlay_id.as_deref())
        .collect::<Vec<_>>(),
      vec![
        Some("operational-demand-pressure"),
        Some("operational-active-capital-project"),
        Some("operational-financial-distress"),
        Some("operational-community-trust-concern"),
        Some("operational-uncertain-stale-intelligence"),
      ]
    );
    assert!(
      categories
        .iter()
        .all(|overlay| overlay.source.starts_with("PlayerObservation"))
    );

    let all = overlays(&observation);
    assert_eq!(
      all
        .iter()
        .find(|overlay| overlay.id == "demand")
        .and_then(|overlay| overlay.operational_overlay_id.as_deref()),
      None
    );
  }
}
