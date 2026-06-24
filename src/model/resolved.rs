#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ResolvedInputs {
  pub measurement_noise: i32,
  pub delayed_access_report: i32,
  pub labor_sick_call_delta: i32,
  pub policy_signal: i32,
  pub coalition_leverage_signal: i32,
  pub access_measurement_revision: i32,
}
