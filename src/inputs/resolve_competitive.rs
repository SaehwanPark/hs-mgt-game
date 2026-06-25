use crate::model::CompetitiveResolvedInputs;

use super::rng::{bounded_i32, stream_rng};
use super::streams::{STREAM_ANNUAL_POLICY, STREAM_MONTHLY_EVENTS};

pub fn resolve_competitive_inputs(
  seed: u64,
  month_index: u32,
  is_annual_tick: bool,
) -> CompetitiveResolvedInputs {
  let monthly_event_signal =
    bounded_i32(stream_rng(seed, month_index, STREAM_MONTHLY_EVENTS), -4, 6);
  let monthly_event_description = match monthly_event_signal {
    s if s >= 4 => format!("Regional labor market shock (+{s} pressure on recruitment timelines)"),
    s if s <= -2 => format!("Mild flu season eases inpatient demand ({s})"),
    _ => "Routine month; no major exogenous shock reported".to_string(),
  };

  let (annual_policy_signal, annual_policy_description) = if is_annual_tick {
    let signal = bounded_i32(stream_rng(seed, month_index, STREAM_ANNUAL_POLICY), 2, 8);
    (
      signal,
      Some(format!(
        "Annual policy tick: commercial renewal scrutiny intensifies (+{signal} policy pressure)"
      )),
    )
  } else {
    (0, None)
  };

  CompetitiveResolvedInputs {
    monthly_event_signal,
    annual_policy_signal,
    monthly_event_description,
    annual_policy_description,
  }
}

#[cfg(test)]
mod resolve_competitive_tests {
  use super::*;

  #[test]
  fn competitive_inputs_are_deterministic_for_seed_and_month() {
    let first = resolve_competitive_inputs(42, 2, false);
    let second = resolve_competitive_inputs(42, 2, false);
    assert_eq!(first, second);
  }

  #[test]
  fn annual_tick_populates_policy_description() {
    let inputs = resolve_competitive_inputs(42, 12, true);
    assert!(inputs.annual_policy_description.is_some());
    assert!(inputs.annual_policy_signal > 0);
  }
}
