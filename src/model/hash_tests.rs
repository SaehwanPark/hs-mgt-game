use crate::model::{default_ruleset, genesis_state, hash_state, state_hash_record};

#[test]
fn identical_state_records_produce_identical_hashes() {
  let ruleset = default_ruleset();
  let state = genesis_state();

  assert_eq!(hash_state(&state, &ruleset), hash_state(&state, &ruleset));
  assert_eq!(
    state_hash_record(&state, &ruleset),
    "state-hash-v1|ruleset=demo-ruleset-0.1.9|turn=0|cash=100|staffed_beds=120|access_index=70|quality_index=78|workforce_trust=62|community_trust=66|commercial_rate=100|policy_pressure=30"
  );
}
#[test]
fn changed_state_field_changes_hash() {
  let ruleset = default_ruleset();
  let mut changed = genesis_state();
  changed.cash -= 1;

  assert_ne!(
    hash_state(&genesis_state(), &ruleset),
    hash_state(&changed, &ruleset)
  );
}
