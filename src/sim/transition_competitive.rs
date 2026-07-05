use crate::model::{
  AggregatedMonthlyActions, CompetitiveCommand, CompetitiveRuleset, CompetitiveValidationError,
  CompetitiveWorldState, Event, InvestDomain, PendingEffect, PendingEffectKind, PledgeType,
  PublicActionEntry, SystemMonthlyBatch, hash_competitive_state,
};

use super::effects::push_effect;
use super::validate_competitive::validate_competitive_batch;

const PUBLIC_INVEST_THRESHOLD: i32 = 20;

pub fn transition_competitive(
  prior: &CompetitiveWorldState,
  aggregated: AggregatedMonthlyActions,
  ruleset: &CompetitiveRuleset,
) -> Result<crate::model::CompetitiveTransition, CompetitiveValidationError> {
  if aggregated.month_index != prior.policy_calendar.month_index {
    return Err(CompetitiveValidationError::MonthIndexMismatch {
      expected: prior.policy_calendar.month_index,
      provided: aggregated.month_index,
    });
  }

  for batch in &aggregated.batches {
    let system = prior
      .systems
      .iter()
      .find(|system| system.system_id == batch.system_id)
      .ok_or(CompetitiveValidationError::UnknownSystemId {
        system_id: batch.system_id,
      })?;
    validate_competitive_batch(&batch.commands, &system.resources, ruleset)?;
  }

  let mut next = prior.clone();
  let mut events = Vec::new();
  let mut effects = Vec::new();

  // Deduct active project monthly draws for ongoing capital projects
  for system in &mut next.systems {
    let draws = system.resources.active_project_monthly_draws;
    if draws > 0 {
      if system.system_id == 0
        && next.scenario_id == "exemplary-competitive-v1"
        && next.event_metadata.get("rna_strike_active") == Some(&"true".to_string())
      {
        events.push(Event {
          actor: "finance",
          description: "Riverside: active capital project draws suspended due to strike"
            .to_string(),
        });
      } else {
        system.resources.cash -= draws;
        push_effect(&mut effects, "active project monthly draw", "cash", -draws);
        events.push(Event {
          actor: "finance",
          description: format!(
            "{}: monthly draw of {draws} cash for ongoing capital projects",
            system.name
          ),
        });
      }
    }
  }

  let month_index = prior.policy_calendar.month_index;

  for batch in &aggregated.batches {
    apply_system_batch(
      &mut next,
      batch,
      month_index,
      ruleset,
      &mut events,
      &mut effects,
    )?;
  }

  next.turn = prior.turn + 1;
  next.policy_calendar = prior.policy_calendar.advance();
  refresh_monthly_resources(&mut next, ruleset);

  apply_staffing_constraints(&mut next, ruleset, &mut events, &mut effects);

  let state_hash = hash_competitive_state(&next, ruleset);

  Ok(crate::model::CompetitiveTransition {
    prior: prior.clone(),
    aggregated,
    events,
    effects,
    next,
    state_hash,
  })
}

fn refresh_monthly_resources(world: &mut CompetitiveWorldState, ruleset: &CompetitiveRuleset) {
  let human_id = world.human_system().map(|s| s.system_id).unwrap_or(0);
  for system in &mut world.systems {
    system.resources.ap_budget = if system.system_id == human_id {
      world.difficulty.human_ap_per_month()
    } else {
      world.difficulty.cpu_ap_per_month()
    };
    system.resources.refresh_political_capital(ruleset);
  }
}

fn apply_system_batch(
  world: &mut CompetitiveWorldState,
  batch: &SystemMonthlyBatch,
  month_index: u32,
  ruleset: &CompetitiveRuleset,
  events: &mut Vec<Event>,
  effects: &mut Vec<crate::model::AttributedEffect>,
) -> Result<(), CompetitiveValidationError> {
  let system_idx = world
    .systems
    .iter()
    .position(|system| system.system_id == batch.system_id)
    .ok_or(CompetitiveValidationError::UnknownSystemId {
      system_id: batch.system_id,
    })?;

  for command in &batch.commands {
    apply_command(
      world,
      system_idx,
      *command,
      month_index,
      ruleset,
      events,
      effects,
    )?;
  }

  Ok(())
}

fn apply_command(
  world: &mut CompetitiveWorldState,
  system_idx: usize,
  command: CompetitiveCommand,
  month_index: u32,
  _ruleset: &CompetitiveRuleset,
  events: &mut Vec<Event>,
  effects: &mut Vec<crate::model::AttributedEffect>,
) -> Result<(), CompetitiveValidationError> {
  let system_id = world.systems[system_idx].system_id;
  let system_name = world.systems[system_idx].name.clone();
  let cost = command.action_cost();

  {
    let system = &mut world.systems[system_idx];
    system.resources.cash -= cost.cash_cost;
    system.resources.political_capital = system
      .resources
      .political_capital
      .saturating_sub(cost.political_capital);
    push_effect(effects, "action cost", "cash", -cost.cash_cost);
  }

  match command {
    CompetitiveCommand::Hold => {}
    CompetitiveCommand::Recruit { role, headcount } => {
      let delay = role.recruit_delay_months();
      let summary = format!("{system_name}: recruiting {headcount} {role:?} staff");
      if is_public_command(&command) {
        push_public_log(world, month_index, system_id, summary.clone());
      }
      if delay == 0 {
        apply_recruit_immediate(world, system_idx, role, headcount, effects);
      } else {
        enqueue_effect(
          world,
          system_id,
          month_index,
          month_index + delay,
          PendingEffectKind::Recruit { role, headcount },
          format!("{summary} (resolves month {})", month_index + delay),
        );
      }
      events.push(Event {
        actor: "health_system",
        description: summary,
      });
    }
    CompetitiveCommand::Invest { domain, amount } => {
      let summary = format!("{system_name}: investing {amount} in {domain:?}");
      if is_public_command(&command) {
        push_public_log(world, month_index, system_id, summary.clone());
      }
      match domain {
        InvestDomain::Beds => {
          let beds_delta = amount / 5;
          let access_delta = amount / 10;
          let system = &mut world.systems[system_idx];
          system.access_index = crate::model::clamp_metric(system.access_index + access_delta);
          system.market_share_index =
            crate::model::clamp_metric(system.market_share_index + amount / 20);
          push_effect(effects, "capacity investment", "access_index", access_delta);

          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 1,
            PendingEffectKind::BedsCapacity {
              capacity_delta: beds_delta,
              project_draw: None,
            },
            format!("{summary} (med-surg bed capacity expansion)"),
          );
        }
        InvestDomain::Outpatient => {
          let capacity_delta = amount / 10;
          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 1,
            PendingEffectKind::OutpatientCapacity {
              capacity_delta,
              project_draw: None,
            },
            format!("{summary} (outpatient capacity expansion)"),
          );
        }
        InvestDomain::Technology => {
          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 2,
            PendingEffectKind::TechnologyQuality {
              quality_delta: 2,
              project_draw: None,
            },
            format!("{summary} (technology rollout)"),
          );
        }
      }
      events.push(Event {
        actor: "health_system",
        description: summary,
      });
    }
    CompetitiveCommand::Monitor { target, depth } => {
      events.push(Event {
        actor: "health_system",
        description: format!("{system_name}: monitoring {target:?} at depth {depth}"),
      });
    }
    CompetitiveCommand::Negotiate {
      payer,
      rate_posture,
    } => {
      let system = &mut world.systems[system_idx];
      if matches!(payer, crate::model::PayerId::Medicaid) {
        system.access_index = crate::model::clamp_metric(system.access_index + 3);
        world.market.policy_pressure = crate::model::clamp_metric(world.market.policy_pressure - 3);
        push_effect(effects, "Medicaid compliance", "access_index", 3);
        push_effect(effects, "Medicaid compliance", "policy_pressure", -3);
        events.push(Event {
          actor: "health_system",
          description: format!(
            "{system_name}: Medicaid compliance alignment (improved access, reduced policy pressure)"
          ),
        });
      } else {
        system.market_share_index = crate::model::clamp_metric(system.market_share_index + 1);
        push_effect(effects, "payer negotiation", "market_share_index", 1);
        if world.scenario_id == "exemplary-competitive-v1"
          && system_id == 0
          && matches!(payer, crate::model::PayerId::CarrierA)
        {
          world
            .event_metadata
            .insert("blue_shield_negotiated".to_string(), "true".to_string());
        }
        events.push(Event {
          actor: "health_system",
          description: format!(
            "{system_name}: negotiating with {payer:?} ({rate_posture:?} posture)"
          ),
        });
      }
    }
    CompetitiveCommand::Commit { pledge_type, level } => {
      let summary = format!("{system_name}: public {pledge_type:?} pledge level {level}");
      push_public_log(world, month_index, system_id, summary.clone());
      let system = &mut world.systems[system_idx];
      match pledge_type {
        PledgeType::Access => {
          system.access_index =
            crate::model::clamp_metric(system.access_index + (level as i32) * 2);
          system.community_trust =
            crate::model::clamp_metric(system.community_trust + level as i32);
          push_effect(effects, "public pledge", "access_index", (level as i32) * 2);
        }
        PledgeType::Quality => {
          system.quality_index =
            crate::model::clamp_metric(system.quality_index + (level as i32) * 2);
          push_effect(
            effects,
            "public pledge",
            "quality_index",
            (level as i32) * 2,
          );
        }
        PledgeType::Workforce => {
          if world.scenario_id == "exemplary-competitive-v1" && system_id == 0 {
            world
              .event_metadata
              .insert("rna_wage_increase_accepted".to_string(), "true".to_string());
            events.push(Event {
              actor: "health_system",
              description: format!(
                "{system_name}: Settle RNA wage dispute (wages increased permanent +$50k/month)"
              ),
            });
          }
        }
      }
      events.push(Event {
        actor: "health_system",
        description: summary,
      });
    }
    CompetitiveCommand::Project { kind, budget } => {
      let resolve_months = kind.resolve_months();
      let monthly_draw = budget / (resolve_months as i32);
      let summary = format!("{system_name}: started {kind:?} project (budget {budget})");
      push_public_log(world, month_index, system_id, summary.clone());

      if world.scenario_id == "exemplary-competitive-v1" && system_id == 0 {
        if matches!(
          kind,
          crate::model::ProjectKind::EhrEpic | crate::model::ProjectKind::EhrCerner
        ) {
          world.event_metadata.insert(
            "ehr_project_started_month".to_string(),
            month_index.to_string(),
          );
        }
        if matches!(kind, crate::model::ProjectKind::ClinicNetwork) {
          world.event_metadata.insert(
            "clinic_project_start_month".to_string(),
            month_index.to_string(),
          );
        }
      }

      let effect_kind = match kind {
        crate::model::ProjectKind::Tower => PendingEffectKind::BedsCapacity {
          capacity_delta: 20,
          project_draw: Some(monthly_draw),
        },
        crate::model::ProjectKind::ClinicNetwork => PendingEffectKind::OutpatientCapacity {
          capacity_delta: 30,
          project_draw: Some(monthly_draw),
        },
        crate::model::ProjectKind::EhrEpic | crate::model::ProjectKind::EhrCerner => {
          PendingEffectKind::TechnologyQuality {
            quality_delta: 5,
            project_draw: Some(monthly_draw),
          }
        }
      };

      enqueue_effect(
        world,
        system_id,
        month_index,
        month_index + resolve_months,
        effect_kind,
        format!(
          "{summary} (completes month {})",
          month_index + resolve_months
        ),
      );
      let system = &mut world.systems[system_idx];
      system.resources.active_projects += 1;
      system.resources.active_project_monthly_draws += monthly_draw;
      events.push(Event {
        actor: "health_system",
        description: summary,
      });
    }
  }

  Ok(())
}

fn apply_recruit_immediate(
  world: &mut CompetitiveWorldState,
  system_idx: usize,
  role: crate::model::RecruitRole,
  headcount: u32,
  effects: &mut Vec<crate::model::AttributedEffect>,
) {
  let system = &mut world.systems[system_idx];
  match role {
    crate::model::RecruitRole::Nurse => {
      system.nurses += headcount as i32;
      push_effect(effects, "recruitment", "nurses", headcount as i32);
    }
    crate::model::RecruitRole::Physician => {
      system.physicians += headcount as i32;
      push_effect(effects, "recruitment", "physicians", headcount as i32);
    }
    crate::model::RecruitRole::Admin => {
      system.admins += headcount as i32;
      push_effect(effects, "recruitment", "admins", headcount as i32);
    }
  }
  system.workforce_trust = crate::model::clamp_metric(system.workforce_trust - headcount as i32);
  push_effect(
    effects,
    "recruitment",
    "workforce_trust",
    -(headcount as i32),
  );
}

fn enqueue_effect(
  world: &mut CompetitiveWorldState,
  system_id: u32,
  enqueue_month: u32,
  resolve_month: u32,
  kind: PendingEffectKind,
  summary: String,
) {
  let id = world.effect_queue.len() as u32 + 1;
  world.effect_queue.push(PendingEffect {
    id,
    system_id,
    enqueue_month,
    resolve_month,
    kind,
    summary,
  });
}

fn push_public_log(
  world: &mut CompetitiveWorldState,
  month_index: u32,
  system_id: u32,
  summary: String,
) {
  world.public_action_log.push(PublicActionEntry {
    month_index,
    system_id,
    summary,
  });
}

pub fn is_public_command(command: &CompetitiveCommand) -> bool {
  match command {
    CompetitiveCommand::Hold
    | CompetitiveCommand::Monitor { .. }
    | CompetitiveCommand::Negotiate { .. } => false,
    CompetitiveCommand::Recruit { .. }
    | CompetitiveCommand::Commit { .. }
    | CompetitiveCommand::Project { .. } => true,
    CompetitiveCommand::Invest { amount, .. } => *amount >= PUBLIC_INVEST_THRESHOLD,
  }
}

pub fn command_intel_summary(command: &CompetitiveCommand, system_name: &str) -> Option<String> {
  if is_public_command(command) {
    return None;
  }
  match command {
    CompetitiveCommand::Monitor { target, depth } => Some(format!(
      "{system_name}: intelligence gathering on {target:?} (depth {depth})"
    )),
    CompetitiveCommand::Negotiate {
      payer,
      rate_posture,
    } => {
      if matches!(payer, crate::model::PayerId::Medicaid) {
        Some(format!("{system_name}: Medicaid compliance alignment"))
      } else {
        Some(format!(
          "{system_name}: private payer talks with {payer:?} ({rate_posture:?})"
        ))
      }
    }
    CompetitiveCommand::Hold => Some(format!("{system_name}: held position (no public moves)")),
    CompetitiveCommand::Invest { domain, amount } => Some(format!(
      "{system_name}: quiet {domain:?} spend ({amount} units, below disclosure threshold)"
    )),
    _ => None,
  }
}
fn apply_staffing_constraints(
  world: &mut CompetitiveWorldState,
  _ruleset: &CompetitiveRuleset,
  events: &mut Vec<Event>,
  effects: &mut Vec<crate::model::AttributedEffect>,
) {
  for system in &mut world.systems {
    let target_nurses = (system.staffed_beds + 4) / 5;
    let target_physicians = (system.outpatient_capacity + 9) / 10;
    let target_admins = (system.staffed_beds + system.outpatient_capacity + 19) / 20;

    let nurse_deficit = (target_nurses - system.nurses).max(0);
    let physician_deficit = (target_physicians - system.physicians).max(0);
    let admin_deficit = (target_admins - system.admins).max(0);
    let total_deficit = nurse_deficit + physician_deficit + admin_deficit;

    if total_deficit > 0 {
      system.workforce_trust = crate::model::clamp_metric(system.workforce_trust - total_deficit);
      push_effect(
        effects,
        "staffing deficit burnout",
        "workforce_trust",
        -total_deficit,
      );
      events.push(Event {
        actor: "workforce",
        description: format!(
          "{}: staffing deficit of {} staff ({} nurses, {} physicians, {} admins) causes burnout",
          system.name, total_deficit, nurse_deficit, physician_deficit, admin_deficit
        ),
      });
    }

    let mut effective_beds = system.staffed_beds.min(system.nurses * 5);
    let mut effective_outpatient = system.outpatient_capacity.min(system.physicians * 10);

    if system.system_id == 0
      && world.scenario_id == "exemplary-competitive-v1"
      && world.event_metadata.get("rna_strike_active") == Some(&"true".to_string())
    {
      effective_beds /= 2;
      effective_outpatient /= 2;
    }

    let total_physical = system.staffed_beds + system.outpatient_capacity;
    let total_effective = effective_beds + effective_outpatient;

    if total_physical > 0 && total_effective < total_physical {
      let utility_ratio = total_effective as f32 / total_physical as f32;
      let penalty_pct = 1.0 - utility_ratio;
      let penalty = (penalty_pct * 15.0).round() as i32;

      if penalty > 0 {
        let access_before = system.access_index;
        let quality_before = system.quality_index;

        system.access_index = crate::model::clamp_metric(system.access_index - penalty);
        system.quality_index = crate::model::clamp_metric(system.quality_index - penalty);

        let access_delta = system.access_index - access_before;
        let quality_delta = system.quality_index - quality_before;

        if access_delta != 0 {
          push_effect(
            effects,
            "staffing capacity constraint",
            "access_index",
            access_delta,
          );
        }
        if quality_delta != 0 {
          push_effect(
            effects,
            "staffing capacity constraint",
            "quality_index",
            quality_delta,
          );
        }

        events.push(Event {
          actor: "operations",
          description: format!(
            "{}: understaffing reduces operational capacity (-{} to access/quality; effective/physical: {}/{})",
            system.name, penalty, total_effective, total_physical
          ),
        });
      }
    }
  }
}

#[cfg(test)]
mod transition_competitive_tests {
  use super::*;
  use crate::competitive::genesis_competitive_world;
  use crate::model::{
    Difficulty, InvestDomain, MonitorTarget, PayerId, PledgeType, RatePosture, RecruitRole,
    default_competitive_ruleset,
  };
  use crate::sim::resolve::resolve_monthly_batches;

  fn month1_preset_batches() -> Vec<SystemMonthlyBatch> {
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
        rationale: None,
      },
      SystemMonthlyBatch {
        system_id: 2,
        commands: vec![CompetitiveCommand::Commit {
          pledge_type: PledgeType::Access,
          level: 2,
        }],
        rationale: None,
      },
    ]
  }

  fn resolve_month1(prior: &CompetitiveWorldState) -> crate::model::CompetitiveTransition {
    let ruleset = default_competitive_ruleset();
    let aggregated =
      resolve_monthly_batches(prior, &month1_preset_batches(), &ruleset).expect("resolve");
    transition_competitive(prior, aggregated, &ruleset).expect("transition")
  }

  #[test]
  fn transition_advances_calendar_and_turn() {
    let prior = genesis_competitive_world(Difficulty::Normal);
    let transition = resolve_month1(&prior);
    assert_eq!(transition.next.turn, 1);
    assert_eq!(transition.next.policy_calendar.month_index, 2);
  }

  #[test]
  fn transition_populates_public_action_log() {
    let prior = genesis_competitive_world(Difficulty::Normal);
    let transition = resolve_month1(&prior);
    assert!(
      transition
        .next
        .public_action_log
        .iter()
        .any(|entry| entry.system_id == 1 && entry.summary.contains("investing"))
    );
    assert!(
      transition
        .next
        .public_action_log
        .iter()
        .any(|entry| entry.system_id == 2 && entry.summary.contains("pledge"))
    );
    assert_eq!(
      transition
        .next
        .public_action_log
        .iter()
        .filter(|entry| entry.month_index == 1)
        .count(),
      3
    );
  }

  #[test]
  fn transition_enqueues_delayed_recruit_effect() {
    let prior = genesis_competitive_world(Difficulty::Normal);
    let transition = resolve_month1(&prior);
    assert!(
      transition
        .next
        .effect_queue
        .iter()
        .any(|effect| effect.system_id == 1 && effect.summary.contains("recruiting"))
    );
  }

  #[test]
  fn permutation_invariant_final_state_hash() {
    let prior = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();
    let ordered = month1_preset_batches();
    let mut reversed = ordered.clone();
    reversed.reverse();

    let aggregated_ordered = resolve_monthly_batches(&prior, &ordered, &ruleset).expect("ordered");
    let aggregated_reversed =
      resolve_monthly_batches(&prior, &reversed, &ruleset).expect("reversed");

    let next_ordered =
      transition_competitive(&prior, aggregated_ordered, &ruleset).expect("transition ordered");
    let next_reversed =
      transition_competitive(&prior, aggregated_reversed, &ruleset).expect("transition reversed");

    assert_eq!(next_ordered.state_hash, next_reversed.state_hash);
    assert_eq!(next_ordered.next, next_reversed.next);
  }

  #[test]
  fn invest_below_threshold_is_private() {
    assert!(!is_public_command(&CompetitiveCommand::Invest {
      domain: InvestDomain::Technology,
      amount: 10,
    }));
    assert!(is_public_command(&CompetitiveCommand::Invest {
      domain: InvestDomain::Beds,
      amount: 25,
    }));
  }

  #[test]
  fn test_staffing_deficit_penalties() {
    let mut world = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();

    // Set admins to target (ceil(218/20) = 11) to avoid admin deficit
    world.systems[0].admins = 11;
    // Induce a nurse deficit of 14 (118 beds needs 24 nurses, we set to 10)
    world.systems[0].nurses = 10;

    let mut events = Vec::new();
    let mut effects = Vec::new();
    let trust_before = world.systems[0].workforce_trust;

    apply_staffing_constraints(&mut world, &ruleset, &mut events, &mut effects);

    // Deficit of 14 nurses: trust should drop by 14
    assert_eq!(world.systems[0].workforce_trust, trust_before - 14);

    // Total physical capacity = 118 beds + 100 clinics = 218
    // Total effective capacity = (10 nurses * 5 beds) + 100 clinics = 150
    // Capacity utility ratio = 150 / 218 = ~0.68807
    // Expected access = 68 - 5 = 63
    // Expected quality = 72 - 5 = 67
    assert_eq!(world.systems[0].access_index, 63);
    assert_eq!(world.systems[0].quality_index, 67);

    assert!(
      events
        .iter()
        .any(|e| e.actor == "workforce" && e.description.contains("burnout"))
    );
    assert!(
      events
        .iter()
        .any(|e| e.actor == "operations" && e.description.contains("understaffing"))
    );
  }

  #[test]
  fn test_medicaid_negotiation_lobbying() {
    let mut prior = genesis_competitive_world(Difficulty::Normal);
    prior.systems[0].resources.cash = 60;
    prior.systems[0].access_index = 68;
    prior.market.policy_pressure = 30;
    prior.systems[0].market_share_index = 25;

    let ruleset = default_competitive_ruleset();
    let batch = SystemMonthlyBatch {
      system_id: prior.systems[0].system_id,
      commands: vec![CompetitiveCommand::Negotiate {
        payer: PayerId::Medicaid,
        rate_posture: RatePosture::Neutral,
      }],
      rationale: None,
    };
    let batches = vec![
      batch,
      SystemMonthlyBatch {
        system_id: prior.systems[1].system_id,
        commands: vec![CompetitiveCommand::Hold],
        rationale: None,
      },
      SystemMonthlyBatch {
        system_id: prior.systems[2].system_id,
        commands: vec![CompetitiveCommand::Hold],
        rationale: None,
      },
    ];

    let aggregated = resolve_monthly_batches(&prior, &batches, &ruleset).expect("resolve");
    let transition = transition_competitive(&prior, aggregated, &ruleset).expect("transition");

    // Cash: 60 starting - 5 cost = 55
    assert_eq!(transition.next.systems[0].resources.cash, 55);
    // Access: 68 starting + 3 = 71
    assert_eq!(transition.next.systems[0].access_index, 71);
    // Policy pressure: 30 starting - 3 = 27
    assert_eq!(transition.next.market.policy_pressure, 27);
    // Market share remains unchanged (does not increase like commercial negotiation)
    assert_eq!(transition.next.systems[0].market_share_index, 25);

    assert!(transition.events.iter().any(
      |e| e.actor == "health_system" && e.description.contains("Medicaid compliance alignment")
    ));
  }

  #[test]
  fn test_exemplary_scenario_timeline_month8_burnout_and_strike_warning() {
    let mut world = genesis_competitive_world(Difficulty::Normal);
    world.scenario_id = "exemplary-competitive-v1".to_string();
    world.policy_calendar = crate::model::PolicyCalendar::new_month(8);

    // Induce staffing ratio below 80%: 118 staffed beds needs 24 nurses. We set nurses to 18 (18 * 5 = 90 capacity, which is < 118 * 0.8 = 94.4)
    world.systems[0].nurses = 18;

    let inputs = crate::inputs::resolve_competitive_inputs(42, 8, false);
    let mut events = Vec::new();
    let trust_before = world.systems[0].workforce_trust;

    super::super::effects_competitive::apply_month_start_tick(&mut world, &inputs, &mut events);

    // Workforce trust drops by 15% due to burnout
    assert_eq!(world.systems[0].workforce_trust, trust_before - 15);
    // Strike warning is triggered
    assert_eq!(
      world.event_metadata.get("rna_strike_warning"),
      Some(&"true".to_string())
    );
    assert!(
      events
        .iter()
        .any(|e| e.description.contains("STRIKE WARNING"))
    );
  }

  #[test]
  fn test_exemplary_scenario_timeline_workforce_wage_commitment() {
    let mut prior = genesis_competitive_world(Difficulty::Normal);
    prior.scenario_id = "exemplary-competitive-v1".to_string();
    prior.policy_calendar = crate::model::PolicyCalendar::new_month(8);
    prior.systems[0].resources.political_capital = 5;

    let ruleset = default_competitive_ruleset();
    let batch = SystemMonthlyBatch {
      system_id: 0,
      commands: vec![CompetitiveCommand::Commit {
        pledge_type: PledgeType::Workforce,
        level: 1,
      }],
      rationale: None,
    };

    let batches = vec![
      batch,
      SystemMonthlyBatch {
        system_id: 1,
        commands: vec![CompetitiveCommand::Hold],
        rationale: None,
      },
      SystemMonthlyBatch {
        system_id: 2,
        commands: vec![CompetitiveCommand::Hold],
        rationale: None,
      },
    ];

    let aggregated = resolve_monthly_batches(&prior, &batches, &ruleset).expect("resolve");
    let transition = transition_competitive(&prior, aggregated, &ruleset).expect("transition");

    // Wages increase accepted metadata flag set
    assert_eq!(
      transition
        .next
        .event_metadata
        .get("rna_wage_increase_accepted"),
      Some(&"true".to_string())
    );
    assert!(
      transition
        .events
        .iter()
        .any(|e| e.description.contains("Settle RNA wage dispute"))
    );
  }

  #[test]
  fn test_exemplary_scenario_timeline_month10_strike_and_con_objection() {
    let mut world = genesis_competitive_world(Difficulty::Normal);
    world.scenario_id = "exemplary-competitive-v1".to_string();
    world.policy_calendar = crate::model::PolicyCalendar::new_month(10);
    world.systems[0].resources.cash = 50;
    world.systems[0].resources.political_capital = 1; // low PC, low cash so CON challenge will delay project

    // Queue a clinic build project
    world.effect_queue.push(crate::model::PendingEffect {
      id: 1,
      system_id: 0,
      enqueue_month: 6,
      resolve_month: 15,
      kind: PendingEffectKind::OutpatientCapacity {
        capacity_delta: 30,
        project_draw: Some(10),
      },
      summary: "clinic network project".to_string(),
    });

    // Trigger strike warning
    world
      .event_metadata
      .insert("rna_strike_warning".to_string(), "true".to_string());

    let inputs = crate::inputs::resolve_competitive_inputs(42, 10, false);
    let mut events = Vec::new();

    super::super::effects_competitive::apply_month_start_tick(&mut world, &inputs, &mut events);

    // Strike is active and months left set to 2
    assert_eq!(
      world.event_metadata.get("rna_strike_active"),
      Some(&"true".to_string())
    );
    assert_eq!(
      world.event_metadata.get("rna_strike_months_left"),
      Some(&"2".to_string())
    );

    // CON challenge delayed clinic network project by 3 months (15 + 3 = 18)
    assert_eq!(world.effect_queue[0].resolve_month, 18);

    // Strike cost not deducted yet on the first Month 10 tick when strike starts
    assert_eq!(world.systems[0].resources.cash, 50);
  }

  #[test]
  fn test_exemplary_scenario_timeline_month12_blue_shield_renewal_and_month18_ehr_lag() {
    let mut world = genesis_competitive_world(Difficulty::Normal);
    world.scenario_id = "exemplary-competitive-v1".to_string();
    world.policy_calendar = crate::model::PolicyCalendar::new_month(18);
    world.systems[0].resources.cash = 500;

    // Blue Shield NOT negotiated
    // EHR NOT started (underfunded)

    let inputs = crate::inputs::resolve_competitive_inputs(42, 18, false);
    let mut events = Vec::new();

    super::super::effects_competitive::apply_month_start_tick(&mut world, &inputs, &mut events);

    // Out of network triggers volume drop (40% of share_before: 24 * 0.6 = 14)
    assert_eq!(world.systems[0].market_share_index, 14);
    assert_eq!(
      world.event_metadata.get("blue_shield_out_of_network"),
      Some(&"true".to_string())
    );

    // EHR underfunded lag cost $20k deducted
    // (Note: Month 18 tick also applies OON if not done, so cash = 500 - 20 = 480)
    assert_eq!(world.systems[0].resources.cash, 480);
    assert!(
      events
        .iter()
        .any(|e| e.description.contains("EHR increases operating costs"))
    );
  }
}
