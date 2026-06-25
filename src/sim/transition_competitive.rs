use crate::model::{
  AggregatedMonthlyActions, CompetitiveCommand, CompetitiveRuleset, CompetitiveValidationError,
  CompetitiveWorldState, Event, InvestDomain, PendingEffect, PledgeType, PublicActionEntry,
  SystemMonthlyBatch, hash_competitive_state,
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
  for system in &mut world.systems {
    system.resources.ap_budget = if system.system_id == 0 {
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
        apply_recruit_immediate(world, system_idx, headcount, effects);
      } else {
        enqueue_effect(
          world,
          system_id,
          month_index,
          month_index + delay,
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
          system.staffed_beds += beds_delta;
          system.access_index = crate::model::clamp_metric(system.access_index + access_delta);
          system.market_share_index =
            crate::model::clamp_metric(system.market_share_index + amount / 20);
          push_effect(effects, "capacity investment", "staffed_beds", beds_delta);
          push_effect(effects, "capacity investment", "access_index", access_delta);
        }
        InvestDomain::Outpatient => {
          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 1,
            format!("{summary} (outpatient expansion)"),
          );
        }
        InvestDomain::Technology => {
          enqueue_effect(
            world,
            system_id,
            month_index,
            month_index + 2,
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
      system.market_share_index = crate::model::clamp_metric(system.market_share_index + 1);
      push_effect(effects, "payer negotiation", "market_share_index", 1);
      events.push(Event {
        actor: "health_system",
        description: format!(
          "{system_name}: negotiating with {payer:?} ({rate_posture:?} posture)"
        ),
      });
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
      enqueue_effect(
        world,
        system_id,
        month_index,
        month_index + resolve_months,
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
  headcount: u32,
  effects: &mut Vec<crate::model::AttributedEffect>,
) {
  let system = &mut world.systems[system_idx];
  let beds_delta = headcount as i32;
  system.staffed_beds += beds_delta;
  system.workforce_trust = crate::model::clamp_metric(system.workforce_trust - headcount as i32);
  push_effect(effects, "recruitment", "staffed_beds", beds_delta);
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
  summary: String,
) {
  let id = world.effect_queue.len() as u32 + 1;
  world.effect_queue.push(PendingEffect {
    id,
    system_id,
    enqueue_month,
    resolve_month,
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
    } => Some(format!(
      "{system_name}: private payer talks with {payer:?} ({rate_posture:?})"
    )),
    CompetitiveCommand::Hold => Some(format!("{system_name}: held position (no public moves)")),
    CompetitiveCommand::Invest { domain, amount } => Some(format!(
      "{system_name}: quiet {domain:?} spend ({amount} units, below disclosure threshold)"
    )),
    _ => None,
  }
}

#[cfg(test)]
mod transition_competitive_tests {
  use super::*;
  use crate::competitive::genesis_competitive_world;
  use crate::model::{
    Difficulty, InvestDomain, MonitorTarget, PledgeType, RecruitRole, default_competitive_ruleset,
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
      },
      SystemMonthlyBatch {
        system_id: 2,
        commands: vec![CompetitiveCommand::Commit {
          pledge_type: PledgeType::Access,
          level: 2,
        }],
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
}
