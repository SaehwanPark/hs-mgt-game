use super::{Ruleset, WorldState};

pub const STATE_HASH_SCHEMA_VERSION: &str = "state-hash-v1";
const FNV_OFFSET_BASIS: u64 = 0xcbf2_9ce4_8422_2325;
const FNV_PRIME: u64 = 0x0000_0100_0000_01b3;

pub fn state_hash_record(state: &WorldState, ruleset: &Ruleset) -> String {
  format!(
    "{}|ruleset={}|turn={}|cash={}|staffed_beds={}|access_index={}|quality_index={}|workforce_trust={}|community_trust={}|commercial_rate={}|policy_pressure={}",
    STATE_HASH_SCHEMA_VERSION,
    ruleset.version,
    state.turn,
    state.cash,
    state.staffed_beds,
    state.access_index,
    state.quality_index,
    state.workforce_trust,
    state.community_trust,
    state.commercial_rate,
    state.policy_pressure
  )
}

pub fn hash_state(state: &WorldState, ruleset: &Ruleset) -> String {
  stable_hash_hex(&state_hash_record(state, ruleset))
}

pub fn stable_hash_hex(input: &str) -> String {
  let mut hash = FNV_OFFSET_BASIS;

  for byte in input.as_bytes() {
    hash ^= u64::from(*byte);
    hash = hash.wrapping_mul(FNV_PRIME);
  }

  format!("{hash:016x}")
}
