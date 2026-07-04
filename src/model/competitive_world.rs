use super::{Difficulty, PlayerResources, PolicyCalendar, RecruitRole};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct SharedMarketFields {
  pub regional_demand_index: i32,
  pub commercial_payer_pressure: i32,
  pub policy_pressure: i32,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct AiStyleWeights {
  pub growth: u32,
  pub margin: u32,
  pub access: u32,
  pub political: u32,
}

impl AiStyleWeights {
  pub const fn growth_focused() -> Self {
    Self {
      growth: 50,
      margin: 20,
      access: 15,
      political: 15,
    }
  }

  pub const fn margin_focused() -> Self {
    Self {
      growth: 15,
      margin: 50,
      access: 20,
      political: 15,
    }
  }

  pub const fn access_focused() -> Self {
    Self {
      growth: 15,
      margin: 20,
      access: 50,
      political: 15,
    }
  }

  pub const fn political_focused() -> Self {
    Self {
      growth: 15,
      margin: 20,
      access: 15,
      political: 50,
    }
  }

  pub fn style_label(self) -> &'static str {
    let max = self
      .growth
      .max(self.margin)
      .max(self.access)
      .max(self.political);
    if max == self.growth {
      "growth"
    } else if max == self.margin {
      "margin"
    } else if max == self.access {
      "access"
    } else {
      "political"
    }
  }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct AiProfile {
  pub org_name: &'static str,
  pub style: AiStyleWeights,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PlayerController {
  Human,
  Ai(AiProfile),
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PlayerSlot {
  pub system_id: u32,
  pub controller: PlayerController,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct HealthSystemState {
  pub system_id: u32,
  pub name: String,
  pub staffed_beds: i32,
  pub outpatient_capacity: i32,
  pub nurses: i32,
  pub physicians: i32,
  pub admins: i32,
  pub access_index: i32,
  pub quality_index: i32,
  pub workforce_trust: i32,
  pub community_trust: i32,
  pub market_share_index: i32,
  pub resources: PlayerResources,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PublicActionEntry {
  pub month_index: u32,
  pub system_id: u32,
  pub summary: String,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PendingEffectKind {
  Recruit {
    role: RecruitRole,
    headcount: u32,
  },
  BedsCapacity {
    capacity_delta: i32,
    project_draw: Option<i32>,
  },
  OutpatientCapacity {
    capacity_delta: i32,
    project_draw: Option<i32>,
  },
  TechnologyQuality {
    quality_delta: i32,
    project_draw: Option<i32>,
  },
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PendingEffect {
  pub id: u32,
  pub system_id: u32,
  pub enqueue_month: u32,
  pub resolve_month: u32,
  pub kind: PendingEffectKind,
  pub summary: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CompetitiveWorldState {
  pub difficulty: Difficulty,
  pub turn: u32,
  pub market: SharedMarketFields,
  pub systems: Vec<HealthSystemState>,
  pub players: Vec<PlayerSlot>,
  pub public_action_log: Vec<PublicActionEntry>,
  pub effect_queue: Vec<PendingEffect>,
  pub policy_calendar: PolicyCalendar,
}

impl CompetitiveWorldState {
  pub fn human_system(&self) -> Option<&HealthSystemState> {
    let human_slot = self
      .players
      .iter()
      .find(|slot| matches!(slot.controller, PlayerController::Human))?;
    self
      .systems
      .iter()
      .find(|system| system.system_id == human_slot.system_id)
  }

  pub fn rival_count(&self) -> usize {
    self.systems.len().saturating_sub(1)
  }
}
