use crate::model::{
  AggregatedMonthlyActions, CashRunwaySignal, CompetitiveCommand, CompetitiveWorldState,
  MonitorTarget, PlayerObservation,
};

use super::transition_competitive::{command_intel_summary, is_public_command};

const PUBLIC_INTEL_LAG_MONTHS: u32 = 1;

pub fn observe_for_human(
  world: &CompetitiveWorldState,
  prior_aggregated: Option<&AggregatedMonthlyActions>,
) -> PlayerObservation {
  let human = world
    .human_system()
    .expect("competitive world must include human system");
  let observation_month = world.policy_calendar.month_index;
  let intel_month = observation_month.saturating_sub(PUBLIC_INTEL_LAG_MONTHS);

  let mut market_bullets = vec![
    "Regional inpatient demand: stable-to-rising (+0.8% vs prior month, reported)".to_string(),
    "Commercial payer mix: two major carriers; renewal discussions expected Q4".to_string(),
  ];

  for entry in &world.public_action_log {
    if entry.month_index == intel_month && entry.system_id != human.system_id {
      market_bullets.push(format!(
        "Rival {} (observed, prior month): {}",
        rival_name(world, entry.system_id),
        entry.summary
      ));
    }
  }

  if let Some(aggregated) = prior_aggregated {
    apply_monitor_intel(world, aggregated, observation_month, &mut market_bullets);
  }

  let intel_gaps = build_intel_gaps(world, prior_aggregated, observation_month);

  PlayerObservation {
    org_name: human.name.clone(),
    reported_access_index: human.access_index,
    prior_access_revision: None,
    reported_quality_index: human.quality_index,
    workforce_trust_summary: workforce_trust_summary(human.workforce_trust),
    community_trust_summary: if human.community_trust >= 60 {
      "stable".to_string()
    } else {
      "watch".to_string()
    },
    in_flight_projects: in_flight_projects_label(human.resources.active_projects),
    cash_runway_signal: cash_runway_signal(&human.resources),
    market_bullets,
    policy_bullets: default_policy_bullets(),
    annual_policy_review: None,
    consultant_options: Vec::new(),
    intel_gaps,
  }
}

fn rival_name(world: &CompetitiveWorldState, system_id: u32) -> String {
  world
    .systems
    .iter()
    .find(|system| system.system_id == system_id)
    .map(|system| system.name.clone())
    .unwrap_or_else(|| format!("system {system_id}"))
}

fn apply_monitor_intel(
  world: &CompetitiveWorldState,
  aggregated: &AggregatedMonthlyActions,
  observation_month: u32,
  market_bullets: &mut Vec<String>,
) {
  let Some(human_batch) = aggregated.batch_for_system(0) else {
    return;
  };

  for command in &human_batch.commands {
    let CompetitiveCommand::Monitor { target, depth } = command else {
      continue;
    };
    if aggregated.month_index + *depth < observation_month {
      continue;
    }
    let target_id = monitor_target_system_id(*target);
    let Some(target_batch) = aggregated.batch_for_system(target_id) else {
      continue;
    };
    let target_name = rival_name(world, target_id);
    for rival_command in &target_batch.commands {
      if is_public_command(rival_command) {
        continue;
      }
      if let Some(summary) = command_intel_summary(rival_command, &target_name) {
        market_bullets.push(format!(
          "Rival {} (monitor intel, month {}): {}",
          target_name, aggregated.month_index, summary
        ));
      }
    }
  }
}

fn build_intel_gaps(
  world: &CompetitiveWorldState,
  prior_aggregated: Option<&AggregatedMonthlyActions>,
  observation_month: u32,
) -> Vec<String> {
  let mut gaps = Vec::new();
  let intel_month = observation_month.saturating_sub(PUBLIC_INTEL_LAG_MONTHS);

  for system in &world.systems {
    if system.system_id == 0 {
      continue;
    }
    let has_public = world
      .public_action_log
      .iter()
      .any(|entry| entry.month_index == intel_month && entry.system_id == system.system_id);
    let has_private = prior_aggregated.is_some_and(|aggregated| {
      aggregated
        .batch_for_system(system.system_id)
        .is_some_and(|batch| batch.commands.iter().any(|cmd| !is_public_command(cmd)))
    });
    if has_private && !has_public {
      gaps.push(format!(
        "{} private activity last month (not publicly disclosed)",
        system.name
      ));
    } else if !has_public && !has_private {
      gaps.push(format!(
        "{} activity last month (no public signals)",
        system.name
      ));
    }
  }

  if world.rival_count() >= 2 {
    gaps.push("Summit capital budget allocation beyond marketing (unobserved)".to_string());
  }

  gaps
}

pub fn monitor_target_system_id(target: MonitorTarget) -> u32 {
  match target {
    MonitorTarget::Northlake => 1,
    MonitorTarget::Summit => 2,
    MonitorTarget::Valley => 3,
    MonitorTarget::Metro => 4,
  }
}

fn cash_runway_signal(resources: &crate::model::PlayerResources) -> CashRunwaySignal {
  if resources.cash >= 70 {
    CashRunwaySignal::Comfortable
  } else if resources.cash >= 45 {
    CashRunwaySignal::Watch
  } else {
    CashRunwaySignal::Strained
  }
}

fn workforce_trust_summary(trust: i32) -> String {
  if trust >= 60 {
    "moderate; vacancy rate elevated in nursing".to_string()
  } else {
    "strained; vacancy rate elevated in nursing".to_string()
  }
}

fn in_flight_projects_label(active_projects: u32) -> String {
  if active_projects == 0 {
    "none".to_string()
  } else {
    format!("{active_projects} active project(s)")
  }
}

fn default_policy_bullets() -> Vec<String> {
  vec![
    "State Medicaid director signal: access reporting scrutiny increasing".to_string(),
    "Hospital association lobbying: workforce retention tax credit under committee review"
      .to_string(),
    "No federal rule change this month".to_string(),
  ]
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::competitive::genesis_competitive_world;
  use crate::model::{
    CompetitiveCommand, Difficulty, InvestDomain, MonitorTarget, PledgeType, RecruitRole,
    SystemMonthlyBatch, default_competitive_ruleset,
  };
  use crate::sim::resolve::resolve_monthly_batches;
  use crate::sim::transition_competitive::transition_competitive;

  fn month1_batches() -> Vec<SystemMonthlyBatch> {
    vec![
      SystemMonthlyBatch::new(
        0,
        vec![
          CompetitiveCommand::Hold,
          CompetitiveCommand::Monitor {
            target: MonitorTarget::Northlake,
            depth: 1,
          },
        ],
      ),
      SystemMonthlyBatch::new(
        1,
        vec![
          CompetitiveCommand::Invest {
            domain: InvestDomain::Beds,
            amount: 25,
          },
          CompetitiveCommand::Recruit {
            role: RecruitRole::Nurse,
            headcount: 2,
          },
        ],
      ),
      SystemMonthlyBatch::new(
        2,
        vec![CompetitiveCommand::Commit {
          pledge_type: PledgeType::Access,
          level: 2,
        }],
      ),
    ]
  }

  #[test]
  fn month2_observation_surfaces_lagged_public_actions() {
    let prior = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();
    let aggregated = resolve_monthly_batches(&prior, &month1_batches(), &ruleset).expect("resolve");
    let transition =
      transition_competitive(&prior, aggregated.clone(), &ruleset).expect("transition");
    let observation = observe_for_human(&transition.next, Some(&aggregated));

    assert!(
      observation
        .market_bullets
        .iter()
        .any(|bullet| bullet.contains("Northlake") && bullet.contains("investing"))
    );
    assert!(
      observation
        .market_bullets
        .iter()
        .any(|bullet| bullet.contains("Summit") && bullet.contains("pledge"))
    );
  }

  #[test]
  fn monitor_reveals_private_rival_activity_in_month2_report() {
    let prior = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();
    let mut batches = month1_batches();
    batches[1].commands.push(CompetitiveCommand::Negotiate {
      payer: crate::model::PayerId::CarrierA,
      rate_posture: crate::model::RatePosture::Aggressive,
    });
    let aggregated = resolve_monthly_batches(&prior, &batches, &ruleset).expect("resolve");
    let transition =
      transition_competitive(&prior, aggregated.clone(), &ruleset).expect("transition");
    let observation = observe_for_human(&transition.next, Some(&aggregated));

    assert!(
      observation
        .market_bullets
        .iter()
        .any(|bullet| bullet.contains("monitor intel") && bullet.contains("private payer"))
    );
  }

  #[test]
  fn genesis_observation_uses_fixture_when_no_prior_aggregated() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let observation = observe_for_human(&world, None);
    assert_eq!(observation.org_name, "Riverside Community Health");
    assert!(!observation.market_bullets.is_empty());
  }
}
