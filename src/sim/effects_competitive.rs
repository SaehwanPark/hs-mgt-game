use crate::model::{
  AggregatedMonthlyActions, CompetitiveResolvedInputs, CompetitiveWorldState, Event,
  PendingEffectKind, clamp_metric,
};

pub fn apply_month_start_tick(
  world: &mut CompetitiveWorldState,
  inputs: &CompetitiveResolvedInputs,
  events: &mut Vec<Event>,
) {
  apply_due_pending_effects(world, events);
  world.market.regional_demand_index =
    clamp_metric(world.market.regional_demand_index + inputs.monthly_event_signal);
  events.push(Event {
    actor: "environment",
    description: inputs.monthly_event_description.clone(),
  });

  if let Some(description) = &inputs.annual_policy_description {
    world.market.policy_pressure =
      clamp_metric(world.market.policy_pressure + inputs.annual_policy_signal);
    events.push(Event {
      actor: "policy",
      description: description.clone(),
    });
  }
}

pub fn apply_due_pending_effects(world: &mut CompetitiveWorldState, events: &mut Vec<Event>) {
  let month_index = world.policy_calendar.month_index;
  let due: Vec<_> = world
    .effect_queue
    .iter()
    .filter(|effect| effect.resolve_month == month_index)
    .cloned()
    .collect();

  for effect in due {
    apply_pending_effect(world, &effect, events);
    world.effect_queue.retain(|queued| queued.id != effect.id);
  }
}

fn apply_pending_effect(
  world: &mut CompetitiveWorldState,
  effect: &crate::model::PendingEffect,
  events: &mut Vec<Event>,
) {
  let Some(system_idx) = world
    .systems
    .iter()
    .position(|system| system.system_id == effect.system_id)
  else {
    return;
  };

  match effect.kind {
    PendingEffectKind::Recruit { role, headcount } => {
      let system = &mut world.systems[system_idx];
      match role {
        crate::model::RecruitRole::Nurse => {
          system.nurses += headcount as i32;
        }
        crate::model::RecruitRole::Physician => {
          system.physicians += headcount as i32;
        }
        crate::model::RecruitRole::Admin => {
          system.admins += headcount as i32;
        }
      }
      system.workforce_trust = clamp_metric(system.workforce_trust - headcount as i32);
      events.push(Event {
        actor: "health_system",
        description: format!(
          "{}: delayed recruitment resolves (+{headcount} {role:?})",
          system.name,
          role = role
        ),
      });
    }
    PendingEffectKind::BedsCapacity { capacity_delta } => {
      let system = &mut world.systems[system_idx];
      system.staffed_beds += capacity_delta;
      events.push(Event {
        actor: "health_system",
        description: format!(
          "{}: capital project expands bed capacity (+{capacity_delta} staffed beds)",
          system.name
        ),
      });
    }
    PendingEffectKind::OutpatientCapacity { capacity_delta } => {
      let system = &mut world.systems[system_idx];
      system.outpatient_capacity += capacity_delta;
      events.push(Event {
        actor: "health_system",
        description: format!(
          "{}: capacity expansion improves clinic capacity (+{capacity_delta} units)",
          system.name
        ),
      });
    }
    PendingEffectKind::TechnologyQuality { quality_delta } => {
      let system = &mut world.systems[system_idx];
      system.quality_index = clamp_metric(system.quality_index + quality_delta);
      events.push(Event {
        actor: "health_system",
        description: format!(
          "{}: technology rollout improves reported quality",
          system.name
        ),
      });
    }
  }
}

pub fn apply_institution_phase(
  world: &mut CompetitiveWorldState,
  aggregated: &AggregatedMonthlyActions,
  events: &mut Vec<Event>,
) {
  let negotiate_count = aggregated
    .batches
    .iter()
    .flat_map(|batch| batch.commands.iter())
    .filter(|command| matches!(command, crate::model::CompetitiveCommand::Negotiate { .. }))
    .count() as i32;

  if negotiate_count > 0 {
    world.market.commercial_payer_pressure =
      clamp_metric(world.market.commercial_payer_pressure + negotiate_count);
    events.push(Event {
      actor: "payer",
      description: format!(
        "Commercial payers note {negotiate_count} active rate negotiations this month"
      ),
    });
  }

  let access_pledges = aggregated
    .batches
    .iter()
    .flat_map(|batch| batch.commands.iter())
    .filter(|command| {
      matches!(
        command,
        crate::model::CompetitiveCommand::Commit {
          pledge_type: crate::model::PledgeType::Access,
          ..
        }
      )
    })
    .count() as i32;

  if access_pledges > 0 {
    world.market.policy_pressure = clamp_metric(world.market.policy_pressure + access_pledges);
    events.push(Event {
      actor: "state",
      description: format!("State regulators track {access_pledges} new public access pledge(s)"),
    });
  }
}

#[cfg(test)]
mod effects_competitive_tests {
  use super::*;
  use crate::competitive::genesis_competitive_world;
  use crate::inputs::resolve_competitive_inputs;
  use crate::model::{Difficulty, PendingEffect, PendingEffectKind, clamp_metric};

  #[test]
  fn due_recruit_effect_applies_at_resolve_month() {
    let mut world = genesis_competitive_world(Difficulty::Normal);
    world.policy_calendar = crate::model::PolicyCalendar::new_month(2);
    world.effect_queue.push(PendingEffect {
      id: 1,
      system_id: 1,
      enqueue_month: 1,
      resolve_month: 2,
      kind: PendingEffectKind::Recruit {
        role: crate::model::RecruitRole::Nurse,
        headcount: 2,
      },
      summary: "recruiting".to_string(),
    });
    let nurses_before = world.systems[1].nurses;
    let mut events = Vec::new();
    apply_due_pending_effects(&mut world, &mut events);
    assert_eq!(world.systems[1].nurses, nurses_before + 2);
    assert!(world.effect_queue.is_empty());
  }

  #[test]
  fn month_start_tick_applies_event_signal() {
    let mut world = genesis_competitive_world(Difficulty::Normal);
    let inputs = resolve_competitive_inputs(42, 1, false);
    let demand_before = world.market.regional_demand_index;
    let mut events = Vec::new();
    apply_month_start_tick(&mut world, &inputs, &mut events);
    assert_eq!(
      world.market.regional_demand_index,
      clamp_metric(demand_before + inputs.monthly_event_signal)
    );
    assert!(!events.is_empty());
  }
}
