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
    staffed_beds: human.staffed_beds,
    outpatient_capacity: human.outpatient_capacity,
    emergency_capacity: human.emergency_capacity,
    icu_capacity: human.icu_capacity,
    obstetrics_capacity: human.obstetrics_capacity,
    nurses: human.nurses,
    physicians: human.physicians,
    admins: human.admins,
    in_flight_projects: in_flight_projects_label(world, human.system_id),
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
  let human_id = world.human_system().map(|s| s.system_id).unwrap_or(0);
  let Some(human_batch) = aggregated.batch_for_system(human_id) else {
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
  let human_id = world.human_system().map(|s| s.system_id).unwrap_or(0);

  for system in &world.systems {
    if system.system_id == human_id {
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
  target.system_id()
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

pub fn in_flight_projects_label(world: &CompetitiveWorldState, human_id: u32) -> String {
  let mut projects = Vec::new();
  let observation_month = world.policy_calendar.month_index;

  for effect in &world.effect_queue {
    if effect.system_id == human_id {
      match &effect.kind {
        crate::model::PendingEffectKind::BedsCapacity {
          project_draw: Some(draw),
          ..
        } => {
          let remaining = effect.resolve_month.saturating_sub(observation_month);
          projects.push(format!(
            "Tower ({} mos left, ${}k/mo draw)",
            remaining, draw
          ));
        }
        crate::model::PendingEffectKind::OutpatientCapacity {
          project_draw: Some(draw),
          ..
        } => {
          let remaining = effect.resolve_month.saturating_sub(observation_month);
          projects.push(format!(
            "ClinicNetwork ({} mos left, ${}k/mo draw)",
            remaining, draw
          ));
        }
        crate::model::PendingEffectKind::EmergencyCapacity {
          project_draw: Some(draw),
          ..
        } => {
          let remaining = effect.resolve_month.saturating_sub(observation_month);
          projects.push(format!(
            "EmergencyPavilion ({} mos left, ${}k/mo draw)",
            remaining, draw
          ));
        }
        crate::model::PendingEffectKind::IcuCapacity {
          project_draw: Some(draw),
          ..
        } => {
          let remaining = effect.resolve_month.saturating_sub(observation_month);
          projects.push(format!(
            "IcuWing ({} mos left, ${}k/mo draw)",
            remaining, draw
          ));
        }
        crate::model::PendingEffectKind::ObstetricsCapacity {
          project_draw: Some(draw),
          ..
        } => {
          let remaining = effect.resolve_month.saturating_sub(observation_month);
          projects.push(format!(
            "ObstetricsUnit ({} mos left, ${}k/mo draw)",
            remaining, draw
          ));
        }
        crate::model::PendingEffectKind::TechnologyQuality {
          project_draw: Some(draw),
          ..
        } => {
          let remaining = effect.resolve_month.saturating_sub(observation_month);
          let label = if effect.summary.contains("started EhrCerner") {
            "EhrCerner"
          } else {
            "EhrEpic"
          };
          projects.push(format!(
            "{} ({} mos left, ${}k/mo draw)",
            label, remaining, draw
          ));
        }
        _ => {}
      }
    }
  }

  if projects.is_empty() {
    "none".to_string()
  } else {
    projects.join(", ")
  }
}

fn default_policy_bullets() -> Vec<String> {
  vec![
    "State Medicaid director signal: access reporting scrutiny increasing".to_string(),
    "Hospital association lobbying: workforce retention tax credit under committee review"
      .to_string(),
    "Labor market note: recruit commands spend cash now, resolve after role-specific delays, and can strain workforce trust while capacity comes online".to_string(),
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
      SystemMonthlyBatch {
        system_id: 0,
        commands: vec![
          CompetitiveCommand::Hold,
          CompetitiveCommand::Monitor {
            target: MonitorTarget::Northlake,
            depth: 1,
          },
        ],
        rationale: None,
      },
      SystemMonthlyBatch {
        system_id: 1,
        commands: vec![
          CompetitiveCommand::Invest {
            domain: InvestDomain::Beds,
            amount: 25,
          },
          CompetitiveCommand::Recruit {
            role: RecruitRole::Nurse,
            headcount: 2,
          },
        ],
        rationale: Some("AI prioritized growth this month".to_string()),
      },
      SystemMonthlyBatch {
        system_id: 2,
        commands: vec![CompetitiveCommand::Commit {
          pledge_type: PledgeType::Access,
          level: 2,
        }],
        rationale: Some("AI prioritized access trust signal".to_string()),
      },
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

  #[test]
  fn observation_explains_recruitment_timing_tradeoff() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let observation = observe_for_human(&world, None);
    let policy_text = observation.policy_bullets.join("\n");

    assert!(policy_text.contains("recruit commands spend cash now"));
    assert!(policy_text.contains("role-specific delays"));
    assert!(policy_text.contains("strain workforce trust"));
  }

  #[test]
  fn test_active_projects_observation() {
    let mut world = genesis_competitive_world(Difficulty::Normal);

    world.effect_queue.push(crate::model::PendingEffect {
      id: 1,
      system_id: 0,
      enqueue_month: 1,
      resolve_month: 10,
      kind: crate::model::PendingEffectKind::OutpatientCapacity {
        capacity_delta: 30,
        project_draw: Some(2),
      },
      summary: "Riverside Community Health: started clinic_network project (budget 18)".to_string(),
    });

    world.effect_queue.push(crate::model::PendingEffect {
      id: 2,
      system_id: 0,
      enqueue_month: 1,
      resolve_month: 13,
      kind: crate::model::PendingEffectKind::TechnologyQuality {
        quality_delta: 5,
        project_draw: Some(10),
      },
      summary: "Riverside Community Health: started EhrEpic project (budget 120)".to_string(),
    });

    world.policy_calendar.month_index = 2;

    let observation = observe_for_human(&world, None);

    assert!(
      observation
        .in_flight_projects
        .contains("ClinicNetwork (8 mos left, $2k/mo draw)")
    );
    assert!(
      observation
        .in_flight_projects
        .contains("EhrEpic (11 mos left, $10k/mo draw)")
    );
  }
}
