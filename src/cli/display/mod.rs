mod briefing;
mod dashboard;
mod forecast;
mod interactive;

pub use briefing::{turn_executive_briefing, turn_resolution_summary};
pub use dashboard::{
  describe_strategy_commitments, executive_dashboard, print_pre_run_briefing, strategy_commitments,
  strategy_previews,
};
pub use forecast::{turn_uncertainty_preview, turn_uncertainty_preview_header};
pub use interactive::print_interactive_results;

#[cfg(test)]
#[path = "briefing_tests.rs"]
mod briefing_tests;
#[cfg(test)]
#[path = "dashboard_tests.rs"]
mod dashboard_tests;
#[cfg(test)]
#[path = "forecast_tests.rs"]
mod forecast_tests;
