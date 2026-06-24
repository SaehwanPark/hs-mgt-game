#[derive(Clone, Debug, PartialEq, Eq)]
pub struct WorldState {
  pub turn: u32,
  pub cash: i32,
  pub staffed_beds: i32,
  pub access_index: i32,
  pub quality_index: i32,
  pub workforce_trust: i32,
  pub community_trust: i32,
  pub commercial_rate: i32,
  pub policy_pressure: i32,
}

pub fn genesis_state() -> WorldState {
  WorldState {
    turn: 0,
    cash: 100,
    staffed_beds: 120,
    access_index: 70,
    quality_index: 78,
    workforce_trust: 62,
    community_trust: 66,
    commercial_rate: 100,
    policy_pressure: 30,
  }
}
