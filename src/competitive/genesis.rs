use crate::model::{
  AiProfile, AiStyleWeights, CompetitiveRuleset, CompetitiveWorldState, Difficulty,
  HealthSystemState, PendingEffect, PlayerController, PlayerResources, PlayerSlot, PolicyCalendar,
  PublicActionEntry, SharedMarketFields, default_competitive_ruleset,
};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct RivalTemplate {
  name: &'static str,
  style: AiStyleWeights,
  staffed_beds: i32,
  outpatient_capacity: i32,
  nurses: i32,
  physicians: i32,
  admins: i32,
  access_index: i32,
  quality_index: i32,
  workforce_trust: i32,
  community_trust: i32,
  market_share_index: i32,
}

const RIVERSIDE: RivalTemplate = RivalTemplate {
  name: "Riverside Community Health",
  style: AiStyleWeights {
    growth: 25,
    margin: 25,
    access: 30,
    political: 20,
  },
  staffed_beds: 118,
  outpatient_capacity: 100,
  nurses: 24,
  physicians: 10,
  admins: 11,
  access_index: 68,
  quality_index: 72,
  workforce_trust: 60,
  community_trust: 64,
  market_share_index: 24,
};

const NORTHLAKE: RivalTemplate = RivalTemplate {
  name: "Northlake Health",
  style: AiStyleWeights::growth_focused(),
  staffed_beds: 132,
  outpatient_capacity: 150,
  nurses: 27,
  physicians: 15,
  admins: 15,
  access_index: 64,
  quality_index: 70,
  workforce_trust: 55,
  community_trust: 58,
  market_share_index: 28,
};

const SUMMIT: RivalTemplate = RivalTemplate {
  name: "Summit Care",
  style: AiStyleWeights::margin_focused(),
  staffed_beds: 104,
  outpatient_capacity: 120,
  nurses: 21,
  physicians: 12,
  admins: 12,
  access_index: 66,
  quality_index: 74,
  workforce_trust: 60,
  community_trust: 61,
  market_share_index: 22,
};

const VALLEY: RivalTemplate = RivalTemplate {
  name: "Valley Regional",
  style: AiStyleWeights::access_focused(),
  staffed_beds: 96,
  outpatient_capacity: 100,
  nurses: 20,
  physicians: 10,
  admins: 10,
  access_index: 71,
  quality_index: 69,
  workforce_trust: 57,
  community_trust: 67,
  market_share_index: 18,
};

const METRO: RivalTemplate = RivalTemplate {
  name: "Metro Academic",
  style: AiStyleWeights::political_focused(),
  staffed_beds: 148,
  outpatient_capacity: 180,
  nurses: 30,
  physicians: 18,
  admins: 17,
  access_index: 63,
  quality_index: 78,
  workforce_trust: 54,
  community_trust: 56,
  market_share_index: 26,
};

fn rivals_for_difficulty(difficulty: Difficulty) -> &'static [RivalTemplate] {
  match difficulty {
    Difficulty::Easy => &[NORTHLAKE],
    Difficulty::Normal => &[NORTHLAKE, SUMMIT],
    Difficulty::Hard => &[NORTHLAKE, SUMMIT, VALLEY],
    Difficulty::Expert => &[NORTHLAKE, SUMMIT, VALLEY, METRO],
  }
}

fn system_from_template(
  system_id: u32,
  template: &RivalTemplate,
  resources: PlayerResources,
) -> HealthSystemState {
  HealthSystemState {
    system_id,
    name: template.name.to_string(),
    staffed_beds: template.staffed_beds,
    outpatient_capacity: template.outpatient_capacity,
    nurses: template.nurses,
    physicians: template.physicians,
    admins: template.admins,
    access_index: template.access_index,
    quality_index: template.quality_index,
    workforce_trust: template.workforce_trust,
    community_trust: template.community_trust,
    market_share_index: template.market_share_index,
    resources,
  }
}

pub fn genesis_competitive_world(difficulty: Difficulty) -> CompetitiveWorldState {
  genesis_competitive_world_with_ruleset(difficulty, &default_competitive_ruleset())
}

pub fn genesis_competitive_world_with_ruleset(
  difficulty: Difficulty,
  ruleset: &CompetitiveRuleset,
) -> CompetitiveWorldState {
  let rivals = rivals_for_difficulty(difficulty);
  let mut systems = Vec::with_capacity(rivals.len() + 1);
  let mut players = Vec::with_capacity(rivals.len() + 1);

  let human_resources = PlayerResources::genesis(difficulty, ruleset);
  systems.push(system_from_template(0, &RIVERSIDE, human_resources));
  players.push(PlayerSlot {
    system_id: 0,
    controller: PlayerController::Human,
  });

  for (index, rival) in rivals.iter().enumerate() {
    let system_id = (index + 1) as u32;
    let mut resources = PlayerResources::genesis(difficulty, ruleset);
    resources.ap_budget = difficulty.cpu_ap_per_month();
    systems.push(system_from_template(system_id, rival, resources));
    players.push(PlayerSlot {
      system_id,
      controller: PlayerController::Ai(AiProfile {
        org_name: rival.name,
        style: rival.style,
      }),
    });
  }

  CompetitiveWorldState {
    difficulty,
    turn: 0,
    market: SharedMarketFields {
      regional_demand_index: 102,
      commercial_payer_pressure: 48,
      policy_pressure: 36,
    },
    systems,
    players,
    public_action_log: Vec::<PublicActionEntry>::new(),
    effect_queue: Vec::<PendingEffect>::new(),
    policy_calendar: PolicyCalendar::new_month(1),
    scenario_id: "default-competitive".to_string(),
    event_metadata: std::collections::HashMap::new(),
  }
}

pub fn genesis_roster_lines(world: &CompetitiveWorldState) -> Vec<String> {
  world
    .players
    .iter()
    .filter_map(|slot| {
      let system = world.systems.get(slot.system_id as usize)?;
      let controller = match &slot.controller {
        PlayerController::Human => "human player".to_string(),
        PlayerController::Ai(profile) => {
          format!("AI ({})", profile.style.style_label())
        }
      };
      Some(format!(
        "  {} — {} beds, {} clinics, access {}, share index {} ({})",
        system.name,
        system.staffed_beds,
        system.outpatient_capacity,
        system.access_index,
        system.market_share_index,
        controller
      ))
    })
    .collect()
}

#[cfg(test)]
#[path = "genesis_tests.rs"]
mod genesis_tests;
