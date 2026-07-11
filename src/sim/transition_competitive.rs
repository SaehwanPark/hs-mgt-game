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
    consultant_options: Vec::new(),
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
        InvestDomain::Emergency => {
          let emergency_delta = amount / 15;
          let access_delta = amount / 15;
          let system = &mut world.systems[system_idx];
          system.access_index = crate::model::clamp_metric(system.access_index + access_delta);
          system.market_share_index =
            crate::model::clamp_metric(system.market_share_index + amount / 30);
          push_effect(effects, "capacity investment", "access_index", access_delta);

          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 1,
            PendingEffectKind::EmergencyCapacity {
              capacity_delta: emergency_delta,
              project_draw: None,
            },
            format!("{summary} (emergency capacity expansion)"),
          );
        }
        InvestDomain::Icu => {
          let icu_delta = amount / 30;
          let access_delta = amount / 30;
          let system = &mut world.systems[system_idx];
          system.access_index = crate::model::clamp_metric(system.access_index + access_delta);
          system.market_share_index =
            crate::model::clamp_metric(system.market_share_index + amount / 60);
          push_effect(effects, "capacity investment", "access_index", access_delta);

          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 1,
            PendingEffectKind::IcuCapacity {
              capacity_delta: icu_delta,
              project_draw: None,
            },
            format!("{summary} (icu capacity expansion)"),
          );
        }
        InvestDomain::Obstetrics => {
          let obs_delta = amount / 25;
          let access_delta = amount / 25;
          let system = &mut world.systems[system_idx];
          system.access_index = crate::model::clamp_metric(system.access_index + access_delta);
          system.market_share_index =
            crate::model::clamp_metric(system.market_share_index + amount / 50);
          push_effect(effects, "capacity investment", "access_index", access_delta);

          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 1,
            PendingEffectKind::ObstetricsCapacity {
              capacity_delta: obs_delta,
              project_draw: None,
            },
            format!("{summary} (obstetrics capacity expansion)"),
          );
        }
        InvestDomain::Psychiatric => {
          let psych_delta = amount / 20;
          let access_delta = amount / 20;
          let system = &mut world.systems[system_idx];
          system.access_index = crate::model::clamp_metric(system.access_index + access_delta);
          system.market_share_index =
            crate::model::clamp_metric(system.market_share_index + amount / 40);
          push_effect(effects, "capacity investment", "access_index", access_delta);

          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 1,
            PendingEffectKind::PsychiatricCapacity {
              capacity_delta: psych_delta,
              project_draw: None,
            },
            format!("{summary} (psychiatric capacity expansion)"),
          );
        }
        InvestDomain::Cardiology => {
          let cardio_delta = amount / 20;
          let access_delta = amount / 20;
          let system = &mut world.systems[system_idx];
          system.access_index = crate::model::clamp_metric(system.access_index + access_delta);
          system.market_share_index =
            crate::model::clamp_metric(system.market_share_index + amount / 40);
          push_effect(effects, "capacity investment", "access_index", access_delta);

          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 1,
            PendingEffectKind::CardiologyCapacity {
              capacity_delta: cardio_delta,
              project_draw: None,
            },
            format!("{summary} (cardiology capacity expansion)"),
          );
        }
        InvestDomain::Oncology => {
          let oncology_delta = amount / 20;
          let access_delta = amount / 20;
          let system = &mut world.systems[system_idx];
          system.access_index = crate::model::clamp_metric(system.access_index + access_delta);
          system.market_share_index =
            crate::model::clamp_metric(system.market_share_index + amount / 40);
          push_effect(effects, "capacity investment", "access_index", access_delta);

          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 1,
            PendingEffectKind::OncologyCapacity {
              capacity_delta: oncology_delta,
              project_draw: None,
            },
            format!("{summary} (oncology capacity expansion)"),
          );
        }
        InvestDomain::Infusion => {
          let infusion_delta = amount / 15;
          let access_delta = amount / 15;
          let system = &mut world.systems[system_idx];
          system.access_index = crate::model::clamp_metric(system.access_index + access_delta);
          system.market_share_index =
            crate::model::clamp_metric(system.market_share_index + amount / 30);
          push_effect(effects, "capacity investment", "access_index", access_delta);

          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 1,
            PendingEffectKind::InfusionCapacity {
              capacity_delta: infusion_delta,
              project_draw: None,
            },
            format!("{summary} (infusion capacity expansion)"),
          );
        }
        InvestDomain::Neurology => {
          let neuro_delta = amount / 20;
          let access_delta = amount / 20;
          let system = &mut world.systems[system_idx];
          system.access_index = crate::model::clamp_metric(system.access_index + access_delta);
          system.market_share_index =
            crate::model::clamp_metric(system.market_share_index + amount / 40);
          push_effect(effects, "capacity investment", "access_index", access_delta);

          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 1,
            PendingEffectKind::NeurologyCapacity {
              capacity_delta: neuro_delta,
              project_draw: None,
            },
            format!("{summary} (neurology capacity expansion)"),
          );
        }
        InvestDomain::Asc => {
          let asc_delta = amount / 20;
          let access_delta = amount / 20;
          let system = &mut world.systems[system_idx];
          system.access_index = crate::model::clamp_metric(system.access_index + access_delta);
          system.market_share_index =
            crate::model::clamp_metric(system.market_share_index + amount / 40);
          push_effect(effects, "capacity investment", "access_index", access_delta);

          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 1,
            PendingEffectKind::AscCapacity {
              capacity_delta: asc_delta,
              project_draw: None,
            },
            format!("{summary} (ASC capacity expansion)"),
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
      } else if matches!(payer, crate::model::PayerId::Medicare) {
        system.quality_index = crate::model::clamp_metric(system.quality_index + 3);
        world.market.policy_pressure = crate::model::clamp_metric(world.market.policy_pressure - 3);
        push_effect(effects, "Medicare compliance", "quality_index", 3);
        push_effect(effects, "Medicare compliance", "policy_pressure", -3);
        events.push(Event {
          actor: "health_system",
          description: format!(
            "{system_name}: Medicare compliance alignment (improved quality, reduced policy pressure)"
          ),
        });
      } else {
        system.market_share_index = crate::model::clamp_metric(system.market_share_index + 1);
        push_effect(effects, "payer negotiation", "market_share_index", 1);
        if system_id == 0 && matches!(payer, crate::model::PayerId::CarrierA) {
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
          if system_id == 0 {
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

      if system_id == 0 {
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
        crate::model::ProjectKind::EmergencyPavilion => PendingEffectKind::EmergencyCapacity {
          capacity_delta: 15,
          project_draw: Some(monthly_draw),
        },
        crate::model::ProjectKind::IcuWing => PendingEffectKind::IcuCapacity {
          // 10 ICU beds regardless of budget; budget size controls monthly cash draw only
          capacity_delta: 10,
          project_draw: Some(monthly_draw),
        },
        crate::model::ProjectKind::ObstetricsUnit => PendingEffectKind::ObstetricsCapacity {
          capacity_delta: 6,
          project_draw: Some(monthly_draw),
        },
        crate::model::ProjectKind::PsychiatricUnit => PendingEffectKind::PsychiatricCapacity {
          capacity_delta: 5,
          project_draw: Some(monthly_draw),
        },
        crate::model::ProjectKind::CardiologyUnit => PendingEffectKind::CardiologyCapacity {
          capacity_delta: 4,
          project_draw: Some(monthly_draw),
        },
        crate::model::ProjectKind::OncologyUnit => PendingEffectKind::OncologyCapacity {
          capacity_delta: 6,
          project_draw: Some(monthly_draw),
        },
        crate::model::ProjectKind::InfusionCenter => PendingEffectKind::InfusionCapacity {
          capacity_delta: 8,
          project_draw: Some(monthly_draw),
        },
        crate::model::ProjectKind::NeurologyUnit => PendingEffectKind::NeurologyCapacity {
          capacity_delta: 6,
          project_draw: Some(monthly_draw),
        },
        crate::model::ProjectKind::AscUnit => PendingEffectKind::AscCapacity {
          capacity_delta: 6,
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
      } else if matches!(payer, crate::model::PayerId::Medicare) {
        Some(format!("{system_name}: Medicare compliance alignment"))
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
  let regional_demand_index = world.market.regional_demand_index;
  let payer_pressure = world.market.commercial_payer_pressure;
  let human_system_id = world.human_system().map(|system| system.system_id);
  for system in &mut world.systems {
    let target_nurses = (system.staffed_beds + 4) / 5
      + (system.emergency_capacity + 1) / 2
      + system.icu_capacity
      + (system.obstetrics_capacity + 1) / 2
      + (system.psychiatric_capacity + 3) / 4
      + (system.cardiology_capacity + 2) / 3
      + (system.oncology_capacity + 2) / 3
      + (system.infusion_capacity + 3) / 4
      + (system.neurology_capacity + 2) / 3
      + (system.asc_capacity + 1) / 2;
    let target_physicians = (system.outpatient_capacity + 9) / 10
      + (system.emergency_capacity + 3) / 4
      + (system.icu_capacity + 1) / 2
      + (system.obstetrics_capacity + 4) / 5
      + (system.psychiatric_capacity + 9) / 10
      + (system.cardiology_capacity + 7) / 8
      + (system.oncology_capacity + 7) / 8
      + (system.infusion_capacity + 14) / 15
      + (system.neurology_capacity + 5) / 6
      + (system.asc_capacity + 3) / 4;
    let target_admins = (system.staffed_beds + system.outpatient_capacity + 19) / 20
      + (system.emergency_capacity + 9) / 10
      + (system.icu_capacity + 4) / 5
      + (system.obstetrics_capacity + 9) / 10
      + (system.psychiatric_capacity + 14) / 15
      + (system.cardiology_capacity + 11) / 12
      + (system.oncology_capacity + 11) / 12
      + (system.infusion_capacity + 19) / 20
      + (system.neurology_capacity + 9) / 10
      + (system.asc_capacity + 11) / 12;

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

    // Hierarchical staffing allocation: ICU first, Obstetrics second, Med-Surg beds third, Cardiology fourth, Psychiatric fifth, Neurology sixth, Oncology seventh, Infusion eighth, ASC ninth, Outpatient Clinics tenth (for physicians), ED eleventh/last
    let target_nurses_icu = system.icu_capacity;
    let nurses_icu = system.nurses.min(target_nurses_icu);
    let remaining_nurses_obs = (system.nurses - nurses_icu).max(0);

    let target_nurses_obs = (system.obstetrics_capacity + 1) / 2;
    let nurses_obs = remaining_nurses_obs.min(target_nurses_obs);
    let remaining_nurses_ms = (remaining_nurses_obs - nurses_obs).max(0);

    let target_nurses_beds = (system.staffed_beds + 4) / 5;
    let nurses_beds = remaining_nurses_ms.min(target_nurses_beds);
    let remaining_nurses_cardio = (remaining_nurses_ms - nurses_beds).max(0);

    let target_nurses_cardio = (system.cardiology_capacity + 2) / 3;
    let nurses_cardio = remaining_nurses_cardio.min(target_nurses_cardio);
    let remaining_nurses_psych = (remaining_nurses_cardio - nurses_cardio).max(0);

    let target_nurses_psych = (system.psychiatric_capacity + 3) / 4;
    let nurses_psych = remaining_nurses_psych.min(target_nurses_psych);
    let remaining_nurses_neuro = (remaining_nurses_psych - nurses_psych).max(0);

    let target_nurses_neuro = (system.neurology_capacity + 2) / 3;
    let nurses_neuro = remaining_nurses_neuro.min(target_nurses_neuro);
    let remaining_nurses_oncology = (remaining_nurses_neuro - nurses_neuro).max(0);

    let target_nurses_oncology = (system.oncology_capacity + 2) / 3;
    let nurses_oncology = remaining_nurses_oncology.min(target_nurses_oncology);
    let remaining_nurses_infusion = (remaining_nurses_oncology - nurses_oncology).max(0);

    let target_nurses_infusion = (system.infusion_capacity + 3) / 4;
    let nurses_infusion = remaining_nurses_infusion.min(target_nurses_infusion);
    let remaining_nurses_asc = (remaining_nurses_infusion - nurses_infusion).max(0);

    let target_nurses_asc = (system.asc_capacity + 1) / 2;
    let nurses_asc = remaining_nurses_asc.min(target_nurses_asc);
    let remaining_nurses_ed = (remaining_nurses_asc - nurses_asc).max(0);

    let target_nurses_ed = (system.emergency_capacity + 1) / 2;
    let nurses_ed = remaining_nurses_ed.min(target_nurses_ed);

    let target_physicians_icu = (system.icu_capacity + 1) / 2;
    let physicians_icu = system.physicians.min(target_physicians_icu);
    let remaining_physicians_obs = (system.physicians - physicians_icu).max(0);

    let target_physicians_obs = (system.obstetrics_capacity + 4) / 5;
    let physicians_obs = remaining_physicians_obs.min(target_physicians_obs);
    let remaining_physicians_cardio = (remaining_physicians_obs - physicians_obs).max(0);

    let target_physicians_cardio = (system.cardiology_capacity + 7) / 8;
    let physicians_cardio = remaining_physicians_cardio.min(target_physicians_cardio);
    let remaining_physicians_psych = (remaining_physicians_cardio - physicians_cardio).max(0);

    let target_physicians_psych = (system.psychiatric_capacity + 9) / 10;
    let physicians_psych = remaining_physicians_psych.min(target_physicians_psych);
    let remaining_physicians_neuro = (remaining_physicians_psych - physicians_psych).max(0);

    let target_physicians_neuro = (system.neurology_capacity + 5) / 6;
    let physicians_neuro = remaining_physicians_neuro.min(target_physicians_neuro);
    let remaining_physicians_oncology = (remaining_physicians_neuro - physicians_neuro).max(0);

    let target_physicians_oncology = (system.oncology_capacity + 7) / 8;
    let physicians_oncology = remaining_physicians_oncology.min(target_physicians_oncology);
    let remaining_physicians_infusion =
      (remaining_physicians_oncology - physicians_oncology).max(0);

    let target_physicians_infusion = (system.infusion_capacity + 14) / 15;
    let physicians_infusion = remaining_physicians_infusion.min(target_physicians_infusion);
    let remaining_physicians_asc = (remaining_physicians_infusion - physicians_infusion).max(0);

    let target_physicians_asc = (system.asc_capacity + 3) / 4;
    let physicians_asc = remaining_physicians_asc.min(target_physicians_asc);
    let remaining_physicians_op = (remaining_physicians_asc - physicians_asc).max(0);

    let target_physicians_outpatient = (system.outpatient_capacity + 9) / 10;
    let physicians_outpatient = remaining_physicians_op.min(target_physicians_outpatient);
    let remaining_physicians_ed = (remaining_physicians_op - physicians_outpatient).max(0);

    let target_physicians_ed = (system.emergency_capacity + 3) / 4;
    let physicians_ed = remaining_physicians_ed.min(target_physicians_ed);

    let mut effective_icu = system.icu_capacity.min(nurses_icu).min(physicians_icu * 2);
    let mut effective_obs = system
      .obstetrics_capacity
      .min(nurses_obs * 2)
      .min(physicians_obs * 5);
    let mut effective_beds = system.staffed_beds.min(nurses_beds * 5);
    let mut effective_cardio = system
      .cardiology_capacity
      .min(nurses_cardio * 3)
      .min(physicians_cardio * 8);
    let mut effective_psych = system
      .psychiatric_capacity
      .min(nurses_psych * 4)
      .min(physicians_psych * 10);
    let mut effective_oncology = system
      .oncology_capacity
      .min(nurses_oncology * 3)
      .min(physicians_oncology * 8);
    let mut effective_infusion = system
      .infusion_capacity
      .min(nurses_infusion * 4)
      .min(physicians_infusion * 15);
    let mut effective_neuro = system
      .neurology_capacity
      .min(nurses_neuro * 3)
      .min(physicians_neuro * 6);
    let mut effective_asc = system
      .asc_capacity
      .min(nurses_asc * 2)
      .min(physicians_asc * 4);
    let mut effective_outpatient = system.outpatient_capacity.min(physicians_outpatient * 10);
    let mut effective_emergency = system
      .emergency_capacity
      .min(nurses_ed * 2)
      .min(physicians_ed * 4);

    if system.system_id == 0
      && world.event_metadata.get("rna_strike_active") == Some(&"true".to_string())
    {
      effective_beds /= 2;
      effective_outpatient /= 2;
      effective_emergency /= 2;
      effective_icu /= 2;
      effective_obs /= 2;
      effective_psych /= 2;
      effective_cardio /= 2;
      effective_oncology /= 2;
      effective_infusion /= 2;
      effective_neuro /= 2;
      effective_asc /= 2;
    }

    // ED Boarding Calculation.
    // NOTE: critical_admissions uses physical staffed_beds, not effective_beds.
    // During a nurse strike, supply (effective_icu) is halved but demand is not.
    // This is intentional: ICU shortage compounds during workforce crises, which
    // reflects real-world boarding dynamics and creates an educational lesson.
    let critical_admissions = (system.staffed_beds + 19) / 20;
    let boarded_patients = (critical_admissions - effective_icu).max(0);
    effective_emergency = (effective_emergency - boarded_patients).max(0);

    if boarded_patients > 0 {
      events.push(Event {
        actor: "operations",
        description: format!(
          "{}: {} critical care patients boarded in ED due to ICU capacity constraints",
          system.name, boarded_patients
        ),
      });
    }

    // Cardiology ED Boarding & Diversion Calculation.
    let cardiology_demand = (system.cardiology_capacity + 9) / 10;
    let cardiology_overflow = (cardiology_demand - effective_cardio).max(0);
    let boarded_cardio = cardiology_overflow.min(effective_emergency);
    effective_emergency = (effective_emergency - boarded_cardio).max(0);
    let diverted_cardio = (cardiology_overflow - boarded_cardio).max(0);

    if boarded_cardio > 0 {
      events.push(Event {
        actor: "operations",
        description: format!(
          "{}: {} cardiology patients boarded in ED due to cardiology bed constraints",
          system.name, boarded_cardio
        ),
      });
    }

    if diverted_cardio > 0 {
      let trust_penalty = diverted_cardio * 2;
      let quality_penalty = diverted_cardio * 2;
      system.community_trust = crate::model::clamp_metric(system.community_trust - trust_penalty);
      system.quality_index = crate::model::clamp_metric(system.quality_index - quality_penalty);

      push_effect(
        effects,
        "cardiology diversion",
        "community_trust",
        -trust_penalty,
      );
      push_effect(
        effects,
        "cardiology diversion",
        "quality_index",
        -quality_penalty,
      );

      events.push(Event {
        actor: "operations",
        description: format!(
          "{}: {} cardiology patients diverted due to lack of ED holding capacity",
          system.name, diverted_cardio
        ),
      });
    }

    // Psychiatric ED Boarding & Diversion Calculation.
    let psychiatric_demand = (system.psychiatric_capacity + 9) / 10;
    let psychiatric_overflow = (psychiatric_demand - effective_psych).max(0);
    let boarded_psych = psychiatric_overflow.min(effective_emergency);
    effective_emergency = (effective_emergency - boarded_psych).max(0);
    let diverted_psych = (psychiatric_overflow - boarded_psych).max(0);

    if boarded_psych > 0 {
      events.push(Event {
        actor: "operations",
        description: format!(
          "{}: {} psychiatric patients boarded in ED due to psychiatric bed constraints",
          system.name, boarded_psych
        ),
      });
    }

    if diverted_psych > 0 {
      let trust_penalty = diverted_psych;
      let quality_penalty = diverted_psych;
      system.community_trust = crate::model::clamp_metric(system.community_trust - trust_penalty);
      system.quality_index = crate::model::clamp_metric(system.quality_index - quality_penalty);

      push_effect(
        effects,
        "psychiatric diversion",
        "community_trust",
        -trust_penalty,
      );
      push_effect(
        effects,
        "psychiatric diversion",
        "quality_index",
        -quality_penalty,
      );

      events.push(Event {
        actor: "operations",
        description: format!(
          "{}: {} psychiatric patients diverted due to lack of ED holding capacity",
          system.name, diverted_psych
        ),
      });
    }

    // Oncology ED Boarding & Diversion Calculation.
    let oncology_demand = (system.oncology_capacity + 9) / 10;
    let oncology_overflow = (oncology_demand - effective_oncology).max(0);
    let boarded_oncology = oncology_overflow.min(effective_emergency);
    effective_emergency = (effective_emergency - boarded_oncology).max(0);
    let diverted_oncology = (oncology_overflow - boarded_oncology).max(0);

    if boarded_oncology > 0 {
      events.push(Event {
        actor: "operations",
        description: format!(
          "{}: {} oncology patients boarded in ED due to oncology bed constraints",
          system.name, boarded_oncology
        ),
      });
    }

    if diverted_oncology > 0 {
      let trust_penalty = diverted_oncology * 2;
      let quality_penalty = diverted_oncology * 2;
      system.community_trust = crate::model::clamp_metric(system.community_trust - trust_penalty);
      system.quality_index = crate::model::clamp_metric(system.quality_index - quality_penalty);

      push_effect(
        effects,
        "oncology diversion",
        "community_trust",
        -trust_penalty,
      );
      push_effect(
        effects,
        "oncology diversion",
        "quality_index",
        -quality_penalty,
      );

      events.push(Event {
        actor: "operations",
        description: format!(
          "{}: {} oncology patients diverted due to lack of ED holding capacity",
          system.name, diverted_oncology
        ),
      });
    }

    // Neurology ED Boarding & Diversion Calculation.
    let neurology_demand = (system.neurology_capacity + 7) / 8;
    let neurology_overflow = (neurology_demand - effective_neuro).max(0);
    let boarded_neuro = neurology_overflow.min(effective_emergency);
    effective_emergency = (effective_emergency - boarded_neuro).max(0);
    let diverted_neuro = (neurology_overflow - boarded_neuro).max(0);

    if boarded_neuro > 0 {
      events.push(Event {
        actor: "operations",
        description: format!(
          "{}: {} neurology patients boarded in ED due to neurology bed constraints",
          system.name, boarded_neuro
        ),
      });
    }

    if diverted_neuro > 0 {
      let trust_penalty = diverted_neuro * 2;
      let quality_penalty = diverted_neuro * 2;
      system.community_trust = crate::model::clamp_metric(system.community_trust - trust_penalty);
      system.quality_index = crate::model::clamp_metric(system.quality_index - quality_penalty);

      push_effect(
        effects,
        "neurology diversion",
        "community_trust",
        -trust_penalty,
      );
      push_effect(
        effects,
        "neurology diversion",
        "quality_index",
        -quality_penalty,
      );

      events.push(Event {
        actor: "operations",
        description: format!(
          "{}: {} neurology patients diverted due to lack of ED holding capacity",
          system.name, diverted_neuro
        ),
      });
    }

    // Infusion Center Deferral Calculation.
    let infusion_demand = (system.infusion_capacity + 4) / 5;
    let deferred_infusion = (infusion_demand - effective_infusion).max(0);

    if deferred_infusion > 0 {
      let trust_penalty = deferred_infusion;
      let share_penalty = deferred_infusion;
      system.community_trust = crate::model::clamp_metric(system.community_trust - trust_penalty);
      system.market_share_index =
        crate::model::clamp_metric(system.market_share_index - share_penalty);

      push_effect(
        effects,
        "infusion deferral",
        "community_trust",
        -trust_penalty,
      );
      push_effect(
        effects,
        "infusion deferral",
        "market_share_index",
        -share_penalty,
      );

      events.push(Event {
        actor: "operations",
        description: format!(
          "{}: {} chemotherapy infusion sessions deferred due to infusion center capacity constraints",
          system.name, deferred_infusion
        ),
      });
    }

    // ASC Deferral Calculation.
    let asc_demand = (system.asc_capacity + 7) / 8;
    let deferred_asc = (asc_demand - effective_asc).max(0);

    if deferred_asc > 0 {
      let trust_penalty = deferred_asc;
      let share_penalty = deferred_asc;
      system.community_trust = crate::model::clamp_metric(system.community_trust - trust_penalty);
      system.market_share_index =
        crate::model::clamp_metric(system.market_share_index - share_penalty);

      push_effect(effects, "ASC deferral", "community_trust", -trust_penalty);
      push_effect(
        effects,
        "ASC deferral",
        "market_share_index",
        -share_penalty,
      );

      events.push(Event {
        actor: "operations",
        description: format!(
          "{}: {} outpatient surgery procedures deferred due to ASC capacity constraints",
          system.name, deferred_asc
        ),
      });
    }

    // Obstetric Diversion Calculation.
    let obstetric_demand = (system.obstetrics_capacity + 9) / 10;
    let diverted_patients = (obstetric_demand - effective_obs).max(0);
    if diverted_patients > 0 {
      let trust_penalty = diverted_patients * 2;
      let share_penalty = diverted_patients;
      system.community_trust = crate::model::clamp_metric(system.community_trust - trust_penalty);
      system.market_share_index =
        crate::model::clamp_metric(system.market_share_index - share_penalty);

      push_effect(
        effects,
        "obstetric diversion",
        "community_trust",
        -trust_penalty,
      );
      push_effect(
        effects,
        "obstetric diversion",
        "market_share_index",
        -share_penalty,
      );

      events.push(Event {
        actor: "operations",
        description: format!(
          "{}: {} obstetric patients diverted due to L&D capacity constraints",
          system.name, diverted_patients
        ),
      });
    }

    let total_physical = system.staffed_beds
      + system.outpatient_capacity
      + system.emergency_capacity
      + system.icu_capacity
      + system.obstetrics_capacity
      + system.psychiatric_capacity
      + system.cardiology_capacity
      + system.oncology_capacity
      + system.infusion_capacity
      + system.neurology_capacity
      + system.asc_capacity;
    let total_effective = effective_beds
      + effective_outpatient
      + effective_emergency
      + effective_icu
      + effective_obs
      + effective_psych
      + effective_cardio
      + effective_oncology
      + effective_infusion
      + effective_neuro
      + effective_asc;

    apply_monthly_operating_cycle(
      system,
      (regional_demand_index, payer_pressure),
      (total_physical, total_effective),
      human_system_id == Some(system.system_id),
      events,
      effects,
    );

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

fn apply_monthly_operating_cycle(
  system: &mut crate::model::HealthSystemState,
  market: (i32, i32),
  capacity: (i32, i32),
  expose_to_player: bool,
  events: &mut Vec<Event>,
  effects: &mut Vec<crate::model::AttributedEffect>,
) {
  let (regional_demand_index, payer_pressure) = market;
  let (total_physical_capacity, total_effective_capacity) = capacity;
  let demand = (regional_demand_index.max(0) * system.market_share_index.max(0) + 50) / 100;
  let volume_capacity = (total_effective_capacity.max(0) + 4) / 8;
  let treated = demand.min(volume_capacity);
  let unmet = demand - treated;

  // These integer units are visible game abstractions, not calibrated dollars
  // or encounters. Quality improves realization while payer pressure suppresses it.
  let revenue_rate = (150 + system.quality_index - payer_pressure).max(25);
  let revenue = (treated * revenue_rate + 50) / 100;
  let workforce_cost = (system.nurses + system.physicians + system.admins + 1) / 2;
  let footprint_cost = (total_physical_capacity.max(0) + 10) / 20;
  let cost = workforce_cost + footprint_cost;
  let margin = revenue - cost;

  system.monthly_demand = demand;
  system.monthly_treated_volume = treated;
  system.monthly_unmet_demand = unmet;
  system.monthly_operating_revenue = revenue;
  system.monthly_operating_cost = cost;
  system.monthly_operating_margin = margin;
  system.resources.cash += margin;

  if expose_to_player {
    push_effect(
      effects,
      "monthly demand allocation",
      "monthly_demand",
      demand,
    );
    push_effect(
      effects,
      "staffed volume resolution",
      "monthly_treated_volume",
      treated,
    );
    push_effect(effects, "capacity shortfall", "monthly_unmet_demand", unmet);
    push_effect(
      effects,
      "revenue realization",
      "monthly_operating_revenue",
      revenue,
    );
    push_effect(effects, "operating expense", "monthly_operating_cost", cost);
    push_effect(effects, "monthly operating cycle", "cash", margin);
    events.push(Event {
      actor: "operations",
      description: format!(
        "{}: treated {treated}/{demand} demand units; operating revenue {revenue}, cost {cost}, margin {margin:+}",
        system.name
      ),
    });
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
  fn monthly_operating_cycle_connects_demand_capacity_cost_and_cash() {
    let prior = genesis_competitive_world(Difficulty::Normal);
    let starting_cash = prior.systems[0].resources.cash;
    let transition = resolve_month1(&prior);
    let human = &transition.next.systems[0];

    assert!(human.monthly_demand > 0);
    assert!(human.monthly_treated_volume <= human.monthly_demand);
    assert_eq!(
      human.monthly_unmet_demand,
      human.monthly_demand - human.monthly_treated_volume
    );
    assert_eq!(
      human.monthly_operating_margin,
      human.monthly_operating_revenue - human.monthly_operating_cost
    );
    assert_eq!(
      human.resources.cash,
      starting_cash + human.monthly_operating_margin
    );
    assert!(transition.events.iter().any(|event| {
      event.actor == "operations" && event.description.contains("operating revenue")
    }));
    assert!(!transition.events.iter().any(|event| {
      event.description.contains("Northlake Health: treated")
        || event.description.contains("Summit Care: treated")
    }));
    assert!(transition.effects.iter().any(|effect| {
      effect.source == "staffed volume resolution" && effect.metric == "monthly_treated_volume"
    }));
  }

  #[test]
  fn staffing_shortage_limits_volume_and_can_create_unmet_demand() {
    let mut world = genesis_competitive_world(Difficulty::Normal);
    world.systems[0].nurses = 0;
    world.systems[0].physicians = 0;

    let mut events = Vec::new();
    let mut effects = Vec::new();
    apply_staffing_constraints(
      &mut world,
      &default_competitive_ruleset(),
      &mut events,
      &mut effects,
    );

    assert_eq!(world.systems[0].monthly_treated_volume, 0);
    assert_eq!(
      world.systems[0].monthly_unmet_demand,
      world.systems[0].monthly_demand
    );
    assert!(world.systems[0].monthly_operating_margin < 0);
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

    // Cash includes the negotiation cost and the resolved operating margin.
    assert_eq!(
      transition.next.systems[0].resources.cash,
      55 + transition.next.systems[0].monthly_operating_margin
    );
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
  fn test_medicare_negotiation_lobbying() {
    let mut prior = genesis_competitive_world(Difficulty::Normal);
    prior.systems[0].resources.cash = 60;
    prior.systems[0].quality_index = 68;
    prior.market.policy_pressure = 30;
    prior.systems[0].market_share_index = 25;

    let ruleset = default_competitive_ruleset();
    let batch = SystemMonthlyBatch {
      system_id: prior.systems[0].system_id,
      commands: vec![CompetitiveCommand::Negotiate {
        payer: PayerId::Medicare,
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

    // Cash includes the negotiation cost and the resolved operating margin.
    assert_eq!(
      transition.next.systems[0].resources.cash,
      50 + transition.next.systems[0].monthly_operating_margin
    );
    // Quality: 68 starting + 3 = 71
    assert_eq!(transition.next.systems[0].quality_index, 71);
    // Policy pressure: 30 starting - 3 = 27
    assert_eq!(transition.next.market.policy_pressure, 27);
    // Market share remains unchanged
    assert_eq!(transition.next.systems[0].market_share_index, 25);

    assert!(transition.events.iter().any(
      |e| e.actor == "health_system" && e.description.contains("Medicare compliance alignment")
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

  #[test]
  fn test_emergency_department_mechanics() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();

    // 1. Initially emergency_capacity is 0
    assert_eq!(world.systems[0].emergency_capacity, 0);

    // 2. Invest in Emergency capacity: domain=emergency, amount=30
    let batches = vec![
      SystemMonthlyBatch {
        system_id: 0,
        commands: vec![CompetitiveCommand::Invest {
          domain: InvestDomain::Emergency,
          amount: 30,
        }],
        rationale: None,
      },
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

    let aggregated = resolve_monthly_batches(&world, &batches, &ruleset).expect("resolve");
    let transition = transition_competitive(&world, aggregated, &ruleset).expect("transition");

    // After transition, the next state is advanced to Month 2, but the start-of-month tick hasn't run.
    // So emergency_capacity is still 0.
    assert_eq!(transition.next.systems[0].emergency_capacity, 0);
    // access_index at genesis was 68. 68 + 2 = 70.
    assert_eq!(transition.next.systems[0].access_index, 70);
    // market_share_index at genesis was 24. 24 + 1 = 25.
    assert_eq!(transition.next.systems[0].market_share_index, 25);

    // 3. Tick Month 2 to resolve the pending EmergencyCapacity effect
    let mut next_world = transition.next.clone();
    let inputs = crate::inputs::resolve_competitive_inputs(42, 2, false);
    let mut events = Vec::new();
    super::super::effects_competitive::apply_month_start_tick(
      &mut next_world,
      &inputs,
      &mut events,
    );

    // Now emergency capacity increases by 30 / 15 = 2.
    assert_eq!(next_world.systems[0].emergency_capacity, 2);

    // 4. Staffing target increases:
    // Staffed beds: 118, Outpatient: 100, Emergency capacity: 2
    // target_nurses: 118/5 (24) + 2/2 (1) = 25 nurses
    // target_physicians: 100/10 (10) + 2/4 (1) = 11 physicians
    // target_admins: (118 + 100 + 19)/20 (11) + (2 + 9)/10 (1) = 12 admins
    // Riverside starts with 24 nurses, 10 physicians, 11 admins.
    // So there is a deficit of 1 nurse, 1 physician, and 1 admin.
    let mut events_staffing = Vec::new();
    let mut effects_staffing = Vec::new();
    apply_staffing_constraints(
      &mut next_world,
      &ruleset,
      &mut events_staffing,
      &mut effects_staffing,
    );

    // Workforce trust drops by 3 (deficit of 1 nurse + 1 physician + 1 admin)
    assert_eq!(next_world.systems[0].workforce_trust, 60 - 3);

    // Effective capacity:
    // Nurses beds target: 24. Nurses assigned beds: 24 (nurses = 24). Remaining nurses: 0. Nurses ED: 0.
    // Physicians outpatient target: 10. Physicians assigned outpatient: 10 (physicians = 10). Remaining physicians: 0. Physicians ED: 0.
    // Effective beds: 118
    // Effective outpatient: 100
    // Effective emergency: 0
    // Total physical: 118 + 100 + 2 = 220
    // Total effective: 118 + 100 + 0 = 218
    // Capacity utility ratio = 218 / 220 = 0.9909
    // Penalty pct = 1.0 - 0.9909 = 0.0091
    // Penalty = (0.0091 * 15.0).round() = 0.
    // Quality/access should remain at 72 / 70 respectively.
    assert_eq!(next_world.systems[0].quality_index, 72);
    assert_eq!(next_world.systems[0].access_index, 70);
  }

  #[test]
  fn test_icu_department_mechanics() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();

    // 1. Initially icu_capacity is 0
    assert_eq!(world.systems[0].icu_capacity, 0);

    // 2. Invest in ICU capacity: domain=icu, amount=30 (yields +1 beds)
    let batches = vec![
      SystemMonthlyBatch {
        system_id: 0,
        commands: vec![CompetitiveCommand::Invest {
          domain: InvestDomain::Icu,
          amount: 30,
        }],
        rationale: None,
      },
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

    let aggregated = resolve_monthly_batches(&world, &batches, &ruleset).expect("resolve");
    let transition = transition_competitive(&world, aggregated, &ruleset).expect("transition");

    // After transition, the next state is advanced to Month 2, but the start-of-month tick hasn't run.
    assert_eq!(transition.next.systems[0].icu_capacity, 0);
    // access_index at genesis was 68. 68 + 1 = 69.
    assert_eq!(transition.next.systems[0].access_index, 69);
    // market_share_index at genesis was 24. 24 + 0 = 24.
    assert_eq!(transition.next.systems[0].market_share_index, 24);

    // 3. Tick Month 2 to resolve the pending IcuCapacity effect
    let mut next_world = transition.next.clone();
    let inputs = crate::inputs::resolve_competitive_inputs(42, 2, false);
    let mut events = Vec::new();
    super::super::effects_competitive::apply_month_start_tick(
      &mut next_world,
      &inputs,
      &mut events,
    );

    // Now ICU capacity increases by 30 / 30 = 1.
    assert_eq!(next_world.systems[0].icu_capacity, 1);

    // 4. Staffing target increases:
    // target_nurses: 118/5 (24) + 1 (ICU) = 25 nurses
    // target_physicians: 100/10 (10) + (1 + 1)/2 (1 ICU intensivist) = 11 physicians
    // target_admins: (118 + 100 + 19)/20 (11) + (1 + 4)/5 (1 ICU admin) = 12 admins
    // Riverside starts with 24 nurses, 10 physicians, 11 admins.
    // Deficit: 1 nurse, 1 physician, 1 admin. Total deficit = 3 staff.
    let mut events_staffing = Vec::new();
    let mut effects_staffing = Vec::new();
    apply_staffing_constraints(
      &mut next_world,
      &ruleset,
      &mut events_staffing,
      &mut effects_staffing,
    );

    // Workforce trust drops by 3
    assert_eq!(next_world.systems[0].workforce_trust, 60 - 3);

    // Effective capacities:
    // Nurses: 1 ICU first, 23 Beds (target 24). Effective beds = 23 * 5 = 115.
    // Physicians: 1 ICU first, 9 Outpatient (target 10). Effective clinics = 9 * 10 = 90.
    // Effective ICU: 1 beds.
    // Critical care admissions = (118 + 19) / 20 = 6 patients.
    // ED Boarding = (6 - 1).max(0) = 5 boarded patients.
    // Boarded patients deduct from effective emergency: 0 - 5 = 0.
    // Total physical = 118 (beds) + 100 (clinics) + 1 (ICU) = 219
    // Total effective = 115 (beds) + 90 (clinics) + 1 (ICU) = 206
    // Utility ratio = 206 / 219 = 0.9406
    // Penalty pct = 1.0 - 0.9406 = 0.0594
    // Penalty = (0.0594 * 15.0).round() = 1.
    // Access index: 69 - 1 = 68.
    // Quality index: 72 - 1 = 71.
    assert_eq!(next_world.systems[0].quality_index, 71);
    assert_eq!(next_world.systems[0].access_index, 68);
    assert!(
      events_staffing
        .iter()
        .any(|e| e.description.contains("boarded in ED"))
    );
  }

  #[test]
  fn test_obstetrics_department_mechanics() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();

    // 1. Initially obstetrics_capacity is 0
    assert_eq!(world.systems[0].obstetrics_capacity, 0);

    // 2. Invest in Obstetrics capacity: domain=obstetrics, amount=25 (yields +1 beds)
    let batches = vec![
      SystemMonthlyBatch {
        system_id: 0,
        commands: vec![CompetitiveCommand::Invest {
          domain: InvestDomain::Obstetrics,
          amount: 25,
        }],
        rationale: None,
      },
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

    let aggregated = resolve_monthly_batches(&world, &batches, &ruleset).expect("resolve");
    let transition = transition_competitive(&world, aggregated, &ruleset).expect("transition");

    // After transition, capacity has not resolved yet
    assert_eq!(transition.next.systems[0].obstetrics_capacity, 0);
    assert_eq!(transition.next.systems[0].access_index, 69); // 68 + 1

    // 3. Tick Month 2 to resolve the pending ObstetricsCapacity effect
    let mut next_world = transition.next.clone();
    let inputs = crate::inputs::resolve_competitive_inputs(42, 2, false);
    let mut events = Vec::new();
    super::super::effects_competitive::apply_month_start_tick(
      &mut next_world,
      &inputs,
      &mut events,
    );

    // Now Obstetrics capacity increases by 25 / 25 = 1.
    assert_eq!(next_world.systems[0].obstetrics_capacity, 1);

    // 4. Staffing target increases:
    // target_nurses: 118/5 (24) + (1 + 1)/2 (1) = 25 nurses
    // target_physicians: 100/10 (10) + (1 + 4)/5 (1) = 11 physicians
    // target_admins: (118 + 100 + 19)/20 (11) + (1 + 9)/10 (1) = 12 admins
    // Riverside starts with 24 nurses, 10 physicians, 11 admins.
    // Deficit: 1 nurse, 1 physician, 1 admin.
    let mut events_staffing = Vec::new();
    let mut effects_staffing = Vec::new();
    apply_staffing_constraints(
      &mut next_world,
      &ruleset,
      &mut events_staffing,
      &mut effects_staffing,
    );

    // Workforce trust drops by 3
    assert_eq!(next_world.systems[0].workforce_trust, 60 - 3);
    // Effective obs is 1 (allocated 1 nurse and 1 physician).
    // Demand is (1 + 9)/10 = 1. Diverted is 0.
    assert_eq!(next_world.systems[0].community_trust, 64);

    // 5. Test diversion under severe deficit
    let mut scarce_world = transition.next.clone();
    super::super::effects_competitive::apply_month_start_tick(
      &mut scarce_world,
      &inputs,
      &mut events,
    );
    // Reduce nurses to 0 so effective_obs will be 0.
    scarce_world.systems[0].nurses = 0;

    let mut events_div = Vec::new();
    let mut effects_div = Vec::new();
    apply_staffing_constraints(
      &mut scarce_world,
      &ruleset,
      &mut events_div,
      &mut effects_div,
    );

    // Effective obs is 0 (0 nurses allocated).
    // Demand is (1 + 9)/10 = 1. Diverted is 1 patient.
    // Penalty is -2 community trust and -1 market share.
    assert_eq!(scarce_world.systems[0].community_trust, 64 - 2);
    assert_eq!(scarce_world.systems[0].market_share_index, 24 - 1);
    assert!(
      events_div
        .iter()
        .any(|e| e.description.contains("obstetric patients diverted"))
    );
  }

  #[test]
  fn test_psychiatric_department_mechanics() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();

    // 1. Initially psychiatric_capacity is 0
    assert_eq!(world.systems[0].psychiatric_capacity, 0);

    // 2. Invest in Psychiatric capacity: domain=psychiatric, amount=20 (yields +1 beds next month)
    let batches = vec![
      SystemMonthlyBatch {
        system_id: 0,
        commands: vec![CompetitiveCommand::Invest {
          domain: InvestDomain::Psychiatric,
          amount: 20,
        }],
        rationale: None,
      },
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

    let aggregated = resolve_monthly_batches(&world, &batches, &ruleset).expect("resolve");
    let transition = transition_competitive(&world, aggregated, &ruleset).expect("transition");

    // After transition, capacity has not resolved yet
    assert_eq!(transition.next.systems[0].psychiatric_capacity, 0);
    assert_eq!(transition.next.systems[0].access_index, 69); // 68 + 1

    // 3. Tick Month 2 to resolve the pending PsychiatricCapacity effect
    let mut next_world = transition.next.clone();
    let inputs = crate::inputs::resolve_competitive_inputs(42, 2, false);
    let mut events = Vec::new();
    super::super::effects_competitive::apply_month_start_tick(
      &mut next_world,
      &inputs,
      &mut events,
    );

    // Now Psychiatric capacity increases by 20 / 20 = 1.
    assert_eq!(next_world.systems[0].psychiatric_capacity, 1);

    // 4. Staffing target increases:
    // target_nurses: 118/5 (24) + (1 + 3)/4 (1) = 25 nurses
    // target_physicians: 100/10 (10) + (1 + 9)/10 (1) = 11 physicians
    // target_admins: (118 + 100 + 19)/20 (11) + (1 + 14)/15 (1) = 12 admins
    // Riverside starts with 24 nurses, 10 physicians, 11 admins.
    // Deficit: 1 nurse, 1 physician, 1 admin.
    let mut events_staffing = Vec::new();
    let mut effects_staffing = Vec::new();
    apply_staffing_constraints(
      &mut next_world,
      &ruleset,
      &mut events_staffing,
      &mut effects_staffing,
    );

    // Workforce trust drops by 3
    assert_eq!(next_world.systems[0].workforce_trust, 60 - 3);

    // 5. Test boarding in ED
    let mut scarce_world = transition.next.clone();
    super::super::effects_competitive::apply_month_start_tick(
      &mut scarce_world,
      &inputs,
      &mut events,
    );
    // Trigger RNA strike to halve effective capacities (effective psychiatric capacity becomes 0)
    scarce_world.scenario_id = "exemplary-competitive-v1".to_string();
    scarce_world
      .event_metadata
      .insert("rna_strike_active".to_string(), "true".to_string());
    // Give enough staff to fully staff Beds, Psychiatric, and ED (so emergency capacity is > 0)
    // Reduce staffed_beds to 0 to prevent ICU boarding from crowding out the ED
    scarce_world.systems[0].staffed_beds = 0;
    scarce_world.systems[0].nurses = 35;
    scarce_world.systems[0].physicians = 15;
    scarce_world.systems[0].emergency_capacity = 10;

    let mut events_board = Vec::new();
    let mut effects_board = Vec::new();
    apply_staffing_constraints(
      &mut scarce_world,
      &ruleset,
      &mut events_board,
      &mut effects_board,
    );

    // Effective psych is halved by strike to 0.
    // Demand is (1 + 9)/10 = 1. Overflow is 1 patient.
    // Since ED is staffed, effective emergency is 10 / 2 = 5, so patient boards in the ED.
    assert!(
      events_board
        .iter()
        .any(|e| e.description.contains("psychiatric patients boarded in ED"))
    );
    assert_eq!(scarce_world.systems[0].community_trust, 64); // no diversion

    // 6. Test diversion when ED is full / has 0 capacity (by setting nurses to 0)
    let mut full_ed_world = transition.next.clone();
    super::super::effects_competitive::apply_month_start_tick(
      &mut full_ed_world,
      &inputs,
      &mut events,
    );
    full_ed_world.systems[0].staffed_beds = 0;
    full_ed_world.systems[0].nurses = 0; // makes effective psychiatric capacity 0
    full_ed_world.systems[0].physicians = 12; // staffs outpatient fully to avoid understaffing penalty
    full_ed_world.systems[0].emergency_capacity = 0; // ED cannot hold anyone

    let mut events_div = Vec::new();
    let mut effects_div = Vec::new();
    apply_staffing_constraints(
      &mut full_ed_world,
      &ruleset,
      &mut events_div,
      &mut effects_div,
    );

    // Diverted is 1 patient.
    // Penalty is -1 community trust and -1 quality index.
    assert_eq!(full_ed_world.systems[0].community_trust, 64 - 1);
    assert_eq!(full_ed_world.systems[0].quality_index, 72 - 1);
    assert!(
      events_div
        .iter()
        .any(|e| e.description.contains("psychiatric patients diverted"))
    );
  }

  #[test]
  fn test_cardiology_department_mechanics() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();

    // 1. Initially cardiology_capacity is 0
    assert_eq!(world.systems[0].cardiology_capacity, 0);

    // 2. Invest in Cardiology capacity: domain=cardiology, amount=20 (yields +1 beds next month)
    let batches = vec![
      SystemMonthlyBatch {
        system_id: 0,
        commands: vec![CompetitiveCommand::Invest {
          domain: InvestDomain::Cardiology,
          amount: 20,
        }],
        rationale: None,
      },
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

    let aggregated = resolve_monthly_batches(&world, &batches, &ruleset).expect("resolve");
    let transition = transition_competitive(&world, aggregated, &ruleset).expect("transition");

    // After transition, capacity has not resolved yet
    assert_eq!(transition.next.systems[0].cardiology_capacity, 0);
    assert_eq!(transition.next.systems[0].access_index, 69); // 68 + 1

    // 3. Tick Month 2 to resolve the pending CardiologyCapacity effect
    let mut next_world = transition.next.clone();
    let inputs = crate::inputs::resolve_competitive_inputs(42, 2, false);
    let mut events = Vec::new();
    super::super::effects_competitive::apply_month_start_tick(
      &mut next_world,
      &inputs,
      &mut events,
    );

    // Now Cardiology capacity increases by 20 / 20 = 1.
    assert_eq!(next_world.systems[0].cardiology_capacity, 1);

    // 4. Staffing target increases:
    // target_nurses: 118/5 (24) + (1 + 2)/3 (1) = 25 nurses
    // target_physicians: 100/10 (10) + (1 + 7)/8 (1) = 11 physicians
    // target_admins: (118 + 100 + 19)/20 (11) + (1 + 11)/12 (1) = 12 admins
    // Riverside starts with 24 nurses, 10 physicians, 11 admins.
    // Deficit: 1 nurse, 1 physician, 1 admin.
    let mut events_staffing = Vec::new();
    let mut effects_staffing = Vec::new();
    apply_staffing_constraints(
      &mut next_world,
      &ruleset,
      &mut events_staffing,
      &mut effects_staffing,
    );

    // Workforce trust drops by 3
    assert_eq!(next_world.systems[0].workforce_trust, 60 - 3);

    // 5. Test boarding in ED
    let mut scarce_world = transition.next.clone();
    super::super::effects_competitive::apply_month_start_tick(
      &mut scarce_world,
      &inputs,
      &mut events,
    );
    // Trigger RNA strike to halve effective capacities (effective cardiology capacity becomes 0)
    scarce_world.scenario_id = "exemplary-competitive-v1".to_string();
    scarce_world
      .event_metadata
      .insert("rna_strike_active".to_string(), "true".to_string());
    // Give enough staff to fully staff Beds, Cardiology, and ED (so emergency capacity is > 0)
    // Reduce staffed_beds to 0 to prevent ICU boarding from crowding out the ED
    scarce_world.systems[0].staffed_beds = 0;
    scarce_world.systems[0].nurses = 35;
    scarce_world.systems[0].physicians = 15;
    scarce_world.systems[0].emergency_capacity = 10;

    let mut events_board = Vec::new();
    let mut effects_board = Vec::new();
    apply_staffing_constraints(
      &mut scarce_world,
      &ruleset,
      &mut events_board,
      &mut effects_board,
    );

    // Effective cardio is halved by strike to 0.
    // Demand is (1 + 9)/10 = 1. Overflow is 1 patient.
    // Since ED is staffed, effective emergency is 10 / 2 = 5, so patient boards in the ED.
    assert!(
      events_board
        .iter()
        .any(|e| e.description.contains("cardiology patients boarded in ED"))
    );
    assert_eq!(scarce_world.systems[0].community_trust, 64); // no diversion

    // 6. Test diversion when ED is full / has 0 capacity (by setting nurses to 0)
    let mut full_ed_world = transition.next.clone();
    super::super::effects_competitive::apply_month_start_tick(
      &mut full_ed_world,
      &inputs,
      &mut events,
    );
    full_ed_world.systems[0].staffed_beds = 0;
    full_ed_world.systems[0].nurses = 0; // makes effective cardiology capacity 0
    full_ed_world.systems[0].physicians = 12; // staffs outpatient fully to avoid understaffing penalty
    full_ed_world.systems[0].emergency_capacity = 0; // ED cannot hold anyone

    let mut events_div = Vec::new();
    let mut effects_div = Vec::new();
    apply_staffing_constraints(
      &mut full_ed_world,
      &ruleset,
      &mut events_div,
      &mut effects_div,
    );

    // Diverted is 1 patient.
    // Penalty is -2 community trust and -2 quality index.
    assert_eq!(full_ed_world.systems[0].community_trust, 64 - 2);
    assert_eq!(full_ed_world.systems[0].quality_index, 72 - 2);
    assert!(
      events_div
        .iter()
        .any(|e| e.description.contains("cardiology patients diverted"))
    );
  }

  #[test]
  fn test_oncology_and_infusion_department_mechanics() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();

    // 1. Initially oncology_capacity and infusion_capacity are 0
    assert_eq!(world.systems[0].oncology_capacity, 0);
    assert_eq!(world.systems[0].infusion_capacity, 0);

    // 2. Invest in Oncology capacity (amount=20, yields +1 beds next month) and Infusion capacity (amount=15, yields +1 bays next month)
    let batches = vec![
      SystemMonthlyBatch {
        system_id: 0,
        commands: vec![
          CompetitiveCommand::Invest {
            domain: InvestDomain::Oncology,
            amount: 20,
          },
          CompetitiveCommand::Invest {
            domain: InvestDomain::Infusion,
            amount: 15,
          },
        ],
        rationale: None,
      },
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

    let aggregated = resolve_monthly_batches(&world, &batches, &ruleset).expect("resolve");
    let transition = transition_competitive(&world, aggregated, &ruleset).expect("transition");

    // After transition, capacity has not resolved yet
    assert_eq!(transition.next.systems[0].oncology_capacity, 0);
    assert_eq!(transition.next.systems[0].infusion_capacity, 0);
    assert_eq!(transition.next.systems[0].access_index, 68 + 1 + 1); // access delta: +1 from oncology, +1 from infusion

    // 3. Tick Month 2 to resolve the pending effects
    let mut next_world = transition.next.clone();
    let inputs = crate::inputs::resolve_competitive_inputs(42, 2, false);
    let mut events = Vec::new();
    super::super::effects_competitive::apply_month_start_tick(
      &mut next_world,
      &inputs,
      &mut events,
    );

    // Now capacities increase by 1
    assert_eq!(next_world.systems[0].oncology_capacity, 1);
    assert_eq!(next_world.systems[0].infusion_capacity, 1);

    // 4. Staffing target increases:
    // target_nurses: 118/5 (24) + (1 + 2)/3 (1) + (1 + 3)/4 (1) = 26 nurses (up by 2)
    // target_physicians: 100/10 (10) + (1 + 7)/8 (1) + (1 + 14)/15 (1) = 12 physicians (up by 2)
    // target_admins: (118 + 100 + 19)/20 (11) + (1 + 11)/12 (1) + (1 + 19)/20 (1) = 13 admins (up by 2)
    // Riverside starts with 24 nurses, 10 physicians, 11 admins.
    // Deficit: 2 nurses, 2 physicians, 2 admins = total 6 deficit.
    let mut events_staffing = Vec::new();
    let mut effects_staffing = Vec::new();
    apply_staffing_constraints(
      &mut next_world,
      &ruleset,
      &mut events_staffing,
      &mut effects_staffing,
    );

    // Workforce trust drops by 6
    assert_eq!(next_world.systems[0].workforce_trust, 60 - 6);

    // 5. Test Oncology boarding in ED and Infusion deferrals under strike
    let mut scarce_world = transition.next.clone();
    super::super::effects_competitive::apply_month_start_tick(
      &mut scarce_world,
      &inputs,
      &mut events,
    );
    // Trigger RNA strike to halve effective capacities (effective capacities become 0)
    scarce_world.scenario_id = "exemplary-competitive-v1".to_string();
    scarce_world
      .event_metadata
      .insert("rna_strike_active".to_string(), "true".to_string());

    // Give enough staff to fully staff Beds, Psychiatric, Cardiology, Oncology, Infusion, and ED
    scarce_world.systems[0].staffed_beds = 0;
    scarce_world.systems[0].nurses = 45;
    scarce_world.systems[0].physicians = 20;
    scarce_world.systems[0].emergency_capacity = 10;

    let mut events_board = Vec::new();
    let mut effects_board = Vec::new();
    apply_staffing_constraints(
      &mut scarce_world,
      &ruleset,
      &mut events_board,
      &mut effects_board,
    );

    // Effective oncology is halved by strike to 0. Inpatient Oncology demand is (1 + 9)/10 = 1. Overflow = 1 boards in ED.
    assert!(
      events_board
        .iter()
        .any(|e| e.description.contains("oncology patients boarded in ED"))
    );
    // Effective infusion is halved by strike to 0. Infusion demand is (1 + 4)/5 = 1. Overflow = 1 session deferred.
    assert!(events_board.iter().any(|e| {
      e.description
        .contains("chemotherapy infusion sessions deferred")
    }));
    // Trust penalties for infusion deferral: -1 community trust, -1 market share.
    assert_eq!(scarce_world.systems[0].community_trust, 64 - 1);
    assert_eq!(scarce_world.systems[0].market_share_index, 24 - 1);

    // 6. Test Oncology diversion when ED is full (by setting nurses to 0)
    let mut full_ed_world = transition.next.clone();
    super::super::effects_competitive::apply_month_start_tick(
      &mut full_ed_world,
      &inputs,
      &mut events,
    );
    full_ed_world.systems[0].staffed_beds = 0;
    full_ed_world.systems[0].nurses = 0; // makes effective oncology/infusion capacities 0
    full_ed_world.systems[0].physicians = 12;
    full_ed_world.systems[0].emergency_capacity = 0; // ED cannot hold anyone

    let mut events_div = Vec::new();
    let mut effects_div = Vec::new();
    apply_staffing_constraints(
      &mut full_ed_world,
      &ruleset,
      &mut events_div,
      &mut effects_div,
    );

    // Diverted is 1 oncology patient. Penalty: -2 community trust and -2 quality index.
    // Infusion is deferred: Penalty: -1 community trust and -1 market share.
    // Net trust drop: -2 (oncology) - 1 (infusion) = -3. Community trust = 64 - 3 = 61.
    // Net quality drop: -2 (oncology). Quality = 72 - 2 = 70.
    // Net market share drop: -1 (infusion). Market share = 24 - 1 = 23.
    assert_eq!(full_ed_world.systems[0].community_trust, 64 - 3);
    assert_eq!(full_ed_world.systems[0].quality_index, 72 - 2);
    assert_eq!(full_ed_world.systems[0].market_share_index, 24 - 1);
    assert!(
      events_div
        .iter()
        .any(|e| e.description.contains("oncology patients diverted"))
    );
  }

  #[test]
  fn test_neurology_department_mechanics() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();

    // 1. Initially neurology_capacity is 0
    assert_eq!(world.systems[0].neurology_capacity, 0);

    // 2. Invest in Neurology capacity: domain=neurology, amount=20 (yields +1 beds next month)
    let batches = vec![
      SystemMonthlyBatch {
        system_id: 0,
        commands: vec![CompetitiveCommand::Invest {
          domain: InvestDomain::Neurology,
          amount: 20,
        }],
        rationale: None,
      },
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

    let aggregated = resolve_monthly_batches(&world, &batches, &ruleset).expect("resolve");
    let transition = transition_competitive(&world, aggregated, &ruleset).expect("transition");

    // After transition, capacity has not resolved yet
    assert_eq!(transition.next.systems[0].neurology_capacity, 0);
    assert_eq!(transition.next.systems[0].access_index, 69); // 68 + 1

    // 3. Tick Month 2 to resolve the pending NeurologyCapacity effect
    let mut next_world = transition.next.clone();
    let inputs = crate::inputs::resolve_competitive_inputs(42, 2, false);
    let mut events = Vec::new();
    super::super::effects_competitive::apply_month_start_tick(
      &mut next_world,
      &inputs,
      &mut events,
    );

    // Now Neurology capacity increases by 20 / 20 = 1.
    assert_eq!(next_world.systems[0].neurology_capacity, 1);

    // 4. Staffing target increases:
    // target_nurses: 118/5 (24) + (1 + 2)/3 (1) = 25 nurses
    // target_physicians: 100/10 (10) + (1 + 5)/6 (1) = 11 physicians
    // target_admins: (118 + 100 + 19)/20 (11) + (1 + 9)/10 (1) = 12 admins
    // Riverside starts with 24 nurses, 10 physicians, 11 admins.
    // Deficit: 1 nurse, 1 physician, 1 admin.
    let mut events_staffing = Vec::new();
    let mut effects_staffing = Vec::new();
    apply_staffing_constraints(
      &mut next_world,
      &ruleset,
      &mut events_staffing,
      &mut effects_staffing,
    );

    // Workforce trust drops by 3
    assert_eq!(next_world.systems[0].workforce_trust, 60 - 3);

    // 5. Test boarding in ED
    let mut scarce_world = transition.next.clone();
    super::super::effects_competitive::apply_month_start_tick(
      &mut scarce_world,
      &inputs,
      &mut events,
    );
    // Trigger RNA strike to halve effective capacities (effective neurology capacity becomes 0)
    scarce_world.scenario_id = "exemplary-competitive-v1".to_string();
    scarce_world
      .event_metadata
      .insert("rna_strike_active".to_string(), "true".to_string());
    // Give enough staff to fully staff Beds, Neurology, and ED
    scarce_world.systems[0].staffed_beds = 0;
    scarce_world.systems[0].nurses = 35;
    scarce_world.systems[0].physicians = 15;
    scarce_world.systems[0].emergency_capacity = 10;

    let mut events_board = Vec::new();
    let mut effects_board = Vec::new();
    apply_staffing_constraints(
      &mut scarce_world,
      &ruleset,
      &mut events_board,
      &mut effects_board,
    );

    // Effective neuro is halved by strike to 0.
    // Demand is (1 + 7)/8 = 1. Overflow is 1 patient.
    // Since ED is staffed, effective emergency is 10 / 2 = 5, so patient boards in the ED.
    assert!(
      events_board
        .iter()
        .any(|e| e.description.contains("neurology patients boarded in ED"))
    );
    assert_eq!(scarce_world.systems[0].community_trust, 64); // no diversion

    // 6. Test diversion when ED is full / has 0 capacity (by setting nurses to 0)
    let mut full_ed_world = transition.next.clone();
    super::super::effects_competitive::apply_month_start_tick(
      &mut full_ed_world,
      &inputs,
      &mut events,
    );
    full_ed_world.systems[0].staffed_beds = 0;
    full_ed_world.systems[0].nurses = 0; // makes effective neurology capacity 0
    full_ed_world.systems[0].physicians = 12; // staffs outpatient fully to avoid understaffing penalty
    full_ed_world.systems[0].emergency_capacity = 0; // ED cannot hold anyone

    let mut events_div = Vec::new();
    let mut effects_div = Vec::new();
    apply_staffing_constraints(
      &mut full_ed_world,
      &ruleset,
      &mut events_div,
      &mut effects_div,
    );

    // Diverted is 1 patient.
    // Penalty is -2 community trust and -2 quality index.
    assert_eq!(full_ed_world.systems[0].community_trust, 64 - 2);
    assert_eq!(full_ed_world.systems[0].quality_index, 72 - 2);
    assert!(
      events_div
        .iter()
        .any(|e| e.description.contains("neurology patients diverted"))
    );
  }

  #[test]
  fn test_asc_department_mechanics() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();

    // 1. Initially asc_capacity is 0
    assert_eq!(world.systems[0].asc_capacity, 0);

    // 2. Invest in ASC capacity: domain=asc, amount=20 (yields +1 bays next month)
    let batches = vec![
      SystemMonthlyBatch {
        system_id: 0,
        commands: vec![CompetitiveCommand::Invest {
          domain: InvestDomain::Asc,
          amount: 20,
        }],
        rationale: None,
      },
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

    let aggregated = resolve_monthly_batches(&world, &batches, &ruleset).expect("resolve");
    let transition = transition_competitive(&world, aggregated, &ruleset).expect("transition");

    // After transition, capacity has not resolved yet
    assert_eq!(transition.next.systems[0].asc_capacity, 0);
    assert_eq!(transition.next.systems[0].access_index, 69); // 68 + 1

    // 3. Tick Month 2 to resolve the pending AscCapacity effect
    let mut next_world = transition.next.clone();
    let inputs = crate::inputs::resolve_competitive_inputs(42, 2, false);
    let mut events = Vec::new();
    super::super::effects_competitive::apply_month_start_tick(
      &mut next_world,
      &inputs,
      &mut events,
    );

    // Now ASC capacity increases by 20 / 20 = 1.
    assert_eq!(next_world.systems[0].asc_capacity, 1);

    // 4. Staffing target increases:
    // target_nurses: 118/5 (24) + (1 + 1)/2 (1) = 25 nurses
    // target_physicians: 100/10 (10) + (1 + 3)/4 (1) = 11 physicians
    // target_admins: (118 + 100 + 19)/20 (11) + (1 + 11)/12 (1) = 12 admins
    // Riverside starts with 24 nurses, 10 physicians, 11 admins.
    // Deficit: 1 nurse, 1 physician, 1 admin.
    let mut events_staffing = Vec::new();
    let mut effects_staffing = Vec::new();
    apply_staffing_constraints(
      &mut next_world,
      &ruleset,
      &mut events_staffing,
      &mut effects_staffing,
    );

    // Workforce trust drops by 3
    assert_eq!(next_world.systems[0].workforce_trust, 60 - 3);

    // 5. Test ASC deferral under strike
    let mut scarce_world = transition.next.clone();
    super::super::effects_competitive::apply_month_start_tick(
      &mut scarce_world,
      &inputs,
      &mut events,
    );
    // Trigger RNA strike to halve effective capacities
    scarce_world.scenario_id = "exemplary-competitive-v1".to_string();
    scarce_world
      .event_metadata
      .insert("rna_strike_active".to_string(), "true".to_string());
    // Give enough staff to avoid understaffing penalties on other units
    scarce_world.systems[0].staffed_beds = 0;
    scarce_world.systems[0].nurses = 35;
    scarce_world.systems[0].physicians = 15;

    let mut events_defer = Vec::new();
    let mut effects_defer = Vec::new();
    apply_staffing_constraints(
      &mut scarce_world,
      &ruleset,
      &mut events_defer,
      &mut effects_defer,
    );

    // Effective ASC is halved by strike to 0.
    // Demand is (1 + 7)/8 = 1. Overflow is 1 outpatient surgery procedure deferred.
    assert!(events_defer.iter().any(|e| {
      e.description
        .contains("outpatient surgery procedures deferred due to ASC capacity constraints")
    }));
    // Deferral penalty: -1 community trust, -1 market share.
    assert_eq!(scarce_world.systems[0].community_trust, 64 - 1);
    assert_eq!(scarce_world.systems[0].market_share_index, 24 - 1);
  }
}
