use crate::model::{ResolvedInputs, Ruleset, WorldState, clamp_metric};

use super::rng::{bounded_i32, bounded_u32, stream_rng};
use super::streams::{
  STREAM_ACCESS_DELAY, STREAM_ACCESS_NOISE, STREAM_COALITION, STREAM_LABOR, STREAM_MEASUREMENT,
  STREAM_POLICY, STREAM_REVISION,
};

pub fn resolve_inputs(seed: u64, prior: &WorldState, _ruleset: &Ruleset) -> ResolvedInputs {
  // `_ruleset` is reserved for future ruleset-gated stream bounds.
  let turn = prior.turn;

  let measurement_noise = bounded_i32(stream_rng(seed, turn, STREAM_MEASUREMENT), -5, 5);
  let access_delay = bounded_u32(stream_rng(seed, turn, STREAM_ACCESS_DELAY), 2, 8);
  let access_noise = bounded_i32(stream_rng(seed, turn, STREAM_ACCESS_NOISE), -2, 2);
  let delayed_access_report = clamp_metric(prior.access_index - access_delay as i32 + access_noise);
  let labor_sick_call_delta = bounded_i32(stream_rng(seed, turn, STREAM_LABOR), -5, 0);
  let policy_signal = bounded_i32(stream_rng(seed, turn, STREAM_POLICY), 1, 6);
  let coalition_leverage_signal = bounded_i32(stream_rng(seed, turn, STREAM_COALITION), 1, 6);
  let access_measurement_revision = if turn > 0 {
    bounded_i32(stream_rng(seed, turn, STREAM_REVISION), -3, 3)
  } else {
    0
  };

  ResolvedInputs {
    measurement_noise,
    delayed_access_report,
    labor_sick_call_delta,
    policy_signal,
    coalition_leverage_signal,
    access_measurement_revision,
  }
}
