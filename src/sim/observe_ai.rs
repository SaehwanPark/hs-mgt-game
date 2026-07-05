use crate::model::{
  CompetitiveWorldState, HealthSystemState, PlayerController, SharedMarketFields,
};

const PUBLIC_INTEL_LAG_MONTHS: u32 = 1;

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct LaggedRivalAction {
  pub system_id: u32,
  pub rival_name: String,
  pub summary: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct AiPlayerObservation {
  pub system_id: u32,
  pub system_name: String,
  pub staffed_beds: i32,
  pub outpatient_capacity: i32,
  pub emergency_capacity: i32,
  pub icu_capacity: i32,
  pub obstetrics_capacity: i32,
  pub access_index: i32,
  pub quality_index: i32,
  pub market_share_index: i32,
  pub community_trust: i32,
  pub cash: i32,
  pub ap_budget: u32,
  pub political_capital: u32,
  pub active_projects: u32,
  pub nurses: i32,
  pub physicians: i32,
  pub admins: i32,
  pub month_index: u32,
  pub market: SharedMarketFields,
  pub lagged_rival_actions: Vec<LaggedRivalAction>,
  pub intel_gaps: Vec<String>,
}

pub fn observe_for_ai(world: &CompetitiveWorldState, system_id: u32) -> AiPlayerObservation {
  let system = world
    .systems
    .iter()
    .find(|system| system.system_id == system_id)
    .expect("AI observation requires a known system_id");
  let observation_month = world.policy_calendar.month_index;
  let intel_month = observation_month.saturating_sub(PUBLIC_INTEL_LAG_MONTHS);

  let lagged_rival_actions = world
    .public_action_log
    .iter()
    .filter(|entry| entry.month_index == intel_month && entry.system_id != system_id)
    .map(|entry| LaggedRivalAction {
      system_id: entry.system_id,
      rival_name: rival_name(world, entry.system_id),
      summary: entry.summary.clone(),
    })
    .collect();

  let intel_gaps = build_intel_gaps(world, system_id, intel_month);

  observation_from_system(
    system,
    observation_month,
    &world.market,
    lagged_rival_actions,
    intel_gaps,
  )
}

fn observation_from_system(
  system: &HealthSystemState,
  month_index: u32,
  market: &SharedMarketFields,
  lagged_rival_actions: Vec<LaggedRivalAction>,
  intel_gaps: Vec<String>,
) -> AiPlayerObservation {
  AiPlayerObservation {
    system_id: system.system_id,
    system_name: system.name.clone(),
    staffed_beds: system.staffed_beds,
    outpatient_capacity: system.outpatient_capacity,
    emergency_capacity: system.emergency_capacity,
    icu_capacity: system.icu_capacity,
    obstetrics_capacity: system.obstetrics_capacity,
    access_index: system.access_index,
    quality_index: system.quality_index,
    market_share_index: system.market_share_index,
    community_trust: system.community_trust,
    cash: system.resources.cash,
    ap_budget: system.resources.ap_budget,
    political_capital: system.resources.political_capital,
    active_projects: system.resources.active_projects,
    nurses: system.nurses,
    physicians: system.physicians,
    admins: system.admins,
    month_index,
    market: market.clone(),
    lagged_rival_actions,
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

fn build_intel_gaps(
  world: &CompetitiveWorldState,
  observer_system_id: u32,
  intel_month: u32,
) -> Vec<String> {
  let mut gaps = Vec::new();

  for system in &world.systems {
    if system.system_id == observer_system_id {
      continue;
    }
    let has_public = world
      .public_action_log
      .iter()
      .any(|entry| entry.month_index == intel_month && entry.system_id == system.system_id);
    if !has_public && intel_month > 0 {
      gaps.push(format!(
        "{} activity last month (no public signals)",
        system.name
      ));
    }
  }

  gaps
}

pub fn ai_profile_for_system(
  world: &CompetitiveWorldState,
  system_id: u32,
) -> Option<crate::model::AiProfile> {
  world.players.iter().find_map(|slot| {
    if slot.system_id != system_id {
      return None;
    }
    match slot.controller {
      PlayerController::Ai(profile) => Some(profile),
      PlayerController::Human => None,
    }
  })
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::competitive::genesis_competitive_world;
  use crate::model::{
    CompetitiveCommand, Difficulty, InvestDomain, PledgeType, SystemMonthlyBatch,
    default_competitive_ruleset,
  };
  use crate::sim::resolve::resolve_monthly_batches;
  use crate::sim::transition_competitive::transition_competitive;

  #[test]
  fn genesis_ai_observation_excludes_other_system_private_state() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let obs = observe_for_ai(&world, 1);

    assert_eq!(obs.system_id, 1);
    assert_eq!(obs.system_name, "Northlake Health");
    assert!(obs.lagged_rival_actions.is_empty());
    assert_eq!(obs.cash, world.systems[1].resources.cash);
  }

  #[test]
  fn ai_observation_surfaces_lagged_public_rival_moves() {
    let prior = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();
    let batches = vec![
      SystemMonthlyBatch::new(0, vec![CompetitiveCommand::Hold]),
      SystemMonthlyBatch::new(
        1,
        vec![CompetitiveCommand::Invest {
          domain: InvestDomain::Beds,
          amount: 25,
        }],
      ),
      SystemMonthlyBatch::new(
        2,
        vec![CompetitiveCommand::Commit {
          pledge_type: PledgeType::Access,
          level: 2,
        }],
      ),
    ];
    let aggregated = resolve_monthly_batches(&prior, &batches, &ruleset).expect("resolve");
    let transition = transition_competitive(&prior, aggregated, &ruleset).expect("transition");
    let obs = observe_for_ai(&transition.next, 2);

    assert!(
      obs
        .lagged_rival_actions
        .iter()
        .any(|action| action.summary.contains("investing"))
    );
  }

  #[test]
  fn ai_profile_lookup_returns_none_for_human_system() {
    let world = genesis_competitive_world(Difficulty::Normal);
    assert!(ai_profile_for_system(&world, 0).is_none());
    assert!(ai_profile_for_system(&world, 1).is_some());
  }
}
