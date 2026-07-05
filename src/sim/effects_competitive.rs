use crate::model::{
  AggregatedMonthlyActions, CompetitiveResolvedInputs, CompetitiveWorldState, Event,
  PendingEffectKind, clamp_metric,
};

#[allow(clippy::collapsible_if)]
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

  if world.scenario_id == "exemplary-competitive-v1" {
    let month_index = world.policy_calendar.month_index;

    // 1. RNA Wage increase cost ($50k/month)
    if world.event_metadata.get("rna_wage_increase_accepted") == Some(&"true".to_string()) {
      if let Some(riverside) = world.systems.iter_mut().find(|sys| sys.system_id == 0) {
        riverside.resources.cash -= 50;
        events.push(Event {
          actor: "finance",
          description: "Riverside: paid permanent RNA wage agreement cost ($50k)".to_string(),
        });
      }
    }

    // 2. Active Nurse Strike cost ($30k/month) and project delay
    if world.event_metadata.get("rna_strike_active") == Some(&"true".to_string()) {
      if let Some(riverside) = world.systems.iter_mut().find(|sys| sys.system_id == 0) {
        riverside.resources.cash -= 30;
        events.push(Event {
          actor: "workforce",
          description: "Riverside: paid emergency travel nurse strike costs ($30k)".to_string(),
        });
      }

      // Delay Riverside's capital projects in the queue by 1 month
      for effect in &mut world.effect_queue {
        if effect.system_id == 0 && effect.resolve_month >= month_index {
          match effect.kind {
            PendingEffectKind::BedsCapacity { .. }
            | PendingEffectKind::OutpatientCapacity { .. }
            | PendingEffectKind::TechnologyQuality { .. } => {
              effect.resolve_month += 1;
            }
            _ => {}
          }
        }
      }
    }

    // 3. EHR underfunded lag cost ($20k/month starting Month 18)
    if month_index >= 18
      && world.event_metadata.get("ehr_project_fully_funded") != Some(&"true".to_string())
    {
      if let Some(riverside) = world.systems.iter_mut().find(|sys| sys.system_id == 0) {
        riverside.resources.cash -= 20;
        events.push(Event {
          actor: "operations",
          description: "Riverside: data system lag from underfunded EHR increases operating costs (+$20k/month)".to_string(),
        });
      }
    }

    // 4. Out-of-network Blue Shield penalty (starting Month 12)
    if month_index >= 12
      && world.event_metadata.get("blue_shield_negotiated") != Some(&"true".to_string())
    {
      if world.event_metadata.get("blue_shield_out_of_network") != Some(&"true".to_string()) {
        world
          .event_metadata
          .insert("blue_shield_out_of_network".to_string(), "true".to_string());
        if let Some(riverside) = world.systems.iter_mut().find(|sys| sys.system_id == 0) {
          riverside.market_share_index =
            (riverside.market_share_index as f32 * 0.60).round() as i32;
          events.push(Event {
            actor: "payer",
            description: "Riverside is OUT-OF-NETWORK with Blue Shield! Commercial patient volume drops by 40%.".to_string(),
          });
        }
      }
    }

    // Timeline Events
    // Month 8: Nurse Burnout Crisis
    if month_index == 8 {
      if let Some(riverside) = world.systems.iter_mut().find(|sys| sys.system_id == 0) {
        riverside.workforce_trust = clamp_metric(riverside.workforce_trust - 15);
        events.push(Event {
          actor: "workforce",
          description:
            "Nurse Burnout Crisis: Regional nurse shortage drops Riverside nurse trust by 15%."
              .to_string(),
        });

        // Check staffing ratio < 80%
        let target_nurses = (riverside.staffed_beds + 4) / 5;
        let staffing_ratio = if target_nurses > 0 {
          riverside.nurses as f32 / target_nurses as f32
        } else {
          1.0
        };
        if staffing_ratio < 0.80 {
          world
            .event_metadata
            .insert("rna_strike_warning".to_string(), "true".to_string());
          events.push(Event {
            actor: "workforce",
            description: "RNA issues a STRIKE WARNING due to low nurse staffing ratio (<80%). Settle wages by submitting 'commit pledge_type=workforce level=1' before Month 10 or face a strike.".to_string(),
          });
        }
      }
    }

    // Month 10: CON Legal Challenge & Strike Active Trigger
    if month_index == 10 {
      // 1. Strike trigger check
      if world.event_metadata.get("rna_strike_warning") == Some(&"true".to_string())
        && world.event_metadata.get("rna_wage_increase_accepted") != Some(&"true".to_string())
      {
        world
          .event_metadata
          .insert("rna_strike_active".to_string(), "true".to_string());
        world
          .event_metadata
          .insert("rna_strike_months_left".to_string(), "2".to_string());
        events.push(Event {
          actor: "workforce",
          description: "RNA STRIKE BEGINS! Riverside emergency operation mode active (capacities halved, projects suspended).".to_string(),
        });
      }

      // 2. CON Legal Challenge Check
      let has_clinic_project = world.effect_queue.iter().any(|effect| {
        effect.system_id == 0 && matches!(effect.kind, PendingEffectKind::OutpatientCapacity { .. })
      });
      if has_clinic_project {
        events.push(Event {
          actor: "regulator",
          description:
            "Northlake Health files a formal CON objection to Riverside's clinic expansion project."
              .to_string(),
        });
        if let Some(riverside) = world.systems.iter_mut().find(|sys| sys.system_id == 0) {
          if riverside.resources.political_capital >= 3 {
            riverside.resources.political_capital -= 3;
            events.push(Event {
              actor: "health_system",
              description: "Riverside spends 3 Political Capital to expedite CON approval. Clinic project proceeds.".to_string(),
            });
          } else if riverside.resources.cash >= 100 {
            riverside.resources.cash -= 100;
            events.push(Event {
              actor: "health_system",
              description: "Riverside spends $100k in legal fees to expedite CON approval. Clinic project proceeds.".to_string(),
            });
          } else {
            // Suspend project for 3 months
            for effect in &mut world.effect_queue {
              if effect.system_id == 0
                && matches!(effect.kind, PendingEffectKind::OutpatientCapacity { .. })
              {
                effect.resolve_month += 3;
              }
            }
            events.push(Event {
              actor: "regulator",
              description: "Clinic project suspended for 3 months due to CON legal challenge."
                .to_string(),
            });
          }
        }
      }
    }

    // Strike decrement logic
    if month_index > 10 {
      if let Some(months_left_str) = world.event_metadata.get("rna_strike_months_left").cloned() {
        if let Ok(months_left) = months_left_str.parse::<u32>() {
          if months_left > 0 {
            let new_left = months_left - 1;
            world
              .event_metadata
              .insert("rna_strike_months_left".to_string(), new_left.to_string());
            if new_left == 0 {
              world
                .event_metadata
                .insert("rna_strike_active".to_string(), "false".to_string());
              events.push(Event {
                actor: "workforce",
                description: "RNA strike has ended. Riverside operations return to normal."
                  .to_string(),
              });
            }
          }
        }
      }
    }

    // Month 18 Delayed Strike Consequences
    if month_index == 18 {
      if world.event_metadata.get("rna_strike_active") == Some(&"true".to_string())
        || world.event_metadata.contains_key("rna_strike_months_left")
      {
        if let Some(riverside) = world.systems.iter_mut().find(|sys| sys.system_id == 0) {
          riverside.community_trust = clamp_metric(riverside.community_trust - 20);
          riverside.market_share_index = clamp_metric(riverside.market_share_index - 10);
          events.push(Event {
            actor: "community",
            description: "Delayed Strike Consequences: Patient safety drops, decreasing Riverside community trust by 20% and market share by 10%.".to_string(),
          });
        }
      }
    }
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
    PendingEffectKind::BedsCapacity {
      capacity_delta,
      project_draw,
    } => {
      let system = &mut world.systems[system_idx];
      system.staffed_beds += capacity_delta;
      if let Some(draw) = project_draw {
        system.resources.active_projects = system.resources.active_projects.saturating_sub(1);
        system.resources.active_project_monthly_draws =
          (system.resources.active_project_monthly_draws - draw).max(0);
      }
      events.push(Event {
        actor: "health_system",
        description: format!(
          "{}: capital project expands bed capacity (+{capacity_delta} staffed beds)",
          system.name
        ),
      });
    }
    PendingEffectKind::OutpatientCapacity {
      capacity_delta,
      project_draw,
    } => {
      let system = &mut world.systems[system_idx];
      system.outpatient_capacity += capacity_delta;
      if let Some(draw) = project_draw {
        system.resources.active_projects = system.resources.active_projects.saturating_sub(1);
        system.resources.active_project_monthly_draws =
          (system.resources.active_project_monthly_draws - draw).max(0);
      }
      events.push(Event {
        actor: "health_system",
        description: format!(
          "{}: capacity expansion improves clinic capacity (+{capacity_delta} units)",
          system.name
        ),
      });
    }
    PendingEffectKind::TechnologyQuality {
      quality_delta,
      project_draw,
    } => {
      let system = &mut world.systems[system_idx];
      system.quality_index = clamp_metric(system.quality_index + quality_delta);
      if let Some(draw) = project_draw {
        system.resources.active_projects = system.resources.active_projects.saturating_sub(1);
        system.resources.active_project_monthly_draws =
          (system.resources.active_project_monthly_draws - draw).max(0);
      }
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
    .filter(|command| {
      if let crate::model::CompetitiveCommand::Negotiate { payer, .. } = command {
        !matches!(
          payer,
          crate::model::PayerId::Medicaid | crate::model::PayerId::Medicare
        )
      } else {
        false
      }
    })
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
