use super::{CompetitiveRuleset, CompetitiveWorldState, stable_hash_hex};

// v7: added neuro= field to record format (2026-07-05, feat/neurology-service-line)
pub const COMPETITIVE_STATE_HASH_SCHEMA_VERSION: &str = "competitive-state-hash-v7";

pub fn competitive_state_hash_record(
  state: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
) -> String {
  let mut systems = String::new();
  for system in &state.systems {
    systems.push_str(&format!(
      "|sys{}:beds={}|outpatient={}|emergency={}|icu={}|obs={}|psych={}|cardio={}|onco={}|infuse={}|neuro={}|nurses={}|physicians={}|admins={}|access={}|quality={}|share={}|cash={}|pc={}|ap={}|projects={}|trust_wf={}|trust_comm={}",
      system.system_id,
      system.staffed_beds,
      system.outpatient_capacity,
      system.emergency_capacity,
      system.icu_capacity,
      system.obstetrics_capacity,
      system.psychiatric_capacity,
      system.cardiology_capacity,
      system.oncology_capacity,
      system.infusion_capacity,
      system.neurology_capacity,
      system.nurses,
      system.physicians,
      system.admins,
      system.access_index,
      system.quality_index,
      system.market_share_index,
      system.resources.cash,
      system.resources.political_capital,
      system.resources.ap_budget,
      system.resources.active_projects,
      system.workforce_trust,
      system.community_trust,
    ));
  }

  format!(
    "{}|ruleset={}|turn={}|month={}|demand={}|payer={}|policy={}|log={}|queue={}{}",
    COMPETITIVE_STATE_HASH_SCHEMA_VERSION,
    ruleset.version,
    state.turn,
    state.policy_calendar.month_index,
    state.market.regional_demand_index,
    state.market.commercial_payer_pressure,
    state.market.policy_pressure,
    state.public_action_log.len(),
    state.effect_queue.len(),
    systems,
  )
}

pub fn hash_competitive_state(
  state: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
) -> String {
  stable_hash_hex(&competitive_state_hash_record(state, ruleset))
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::model::{Difficulty, default_competitive_ruleset};

  #[test]
  fn competitive_hash_is_stable_for_same_state() {
    let world = crate::competitive::genesis_competitive_world_with_ruleset(
      Difficulty::Normal,
      &default_competitive_ruleset(),
    );
    let ruleset = default_competitive_ruleset();
    let first = hash_competitive_state(&world, &ruleset);
    let second = hash_competitive_state(&world, &ruleset);
    assert_eq!(first, second);
    assert_eq!(first.len(), 16);
  }
}
